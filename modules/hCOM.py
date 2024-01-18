import socket
from json import dumps, loads
from threading import Thread, activeCount
from time import time, sleep
import uuid
import logging

class hComModule:
    def __init__(self, configurations, **kwargs):
        
        # importing configurations
        for config      in configurations: setattr(self, config, configurations[config])
        for key, value  in kwargs.items(): setattr(self, key, value)
        self.logger = logging.getLogger(self.logging_identity)
        self.ADDR = (self.IP, self.PORT)
        self.clientConnectionStatus = False
        self.clientHandlerStatus = False
        self.clientCloseStatus = False
        self.clientMsgSendStatus = False
        self.activeUsers = 0
        self.clients = []
        self.bufferTX, self.bufferRX = [], []

    def serverMsgHandler(self, conn, msg):
            
            try:
                message = loads(msg)
                #print(message)

                # latency check
                if message['data']['msg'] == "getLatency":
                    to_send = {
                                "id": message['id'],
                                "time":time(),
                                "type":"latencyCheck",
                                "data": {"msg": message['time']}
                              }
                    self.serverSendMsgToClient(conn, dumps(to_send))        
                
                # sensor handler
                elif message['data']['msg'] == "getSensorValues":
                    to_send = {
                                "id": message['id'],
                                "time":time(),
                                "type":"sensorData",
                                "data":{"msg":self.sensorHandler.sensorValues()}
                              }
                    self.serverSendMsgToClient(conn, dumps(to_send))    
                
                elif message['data']['msg'] == "getUser":
                    self.activeUsers = activeCount() - 3
                    to_send = {
                                "id": message['id'],
                                "time":time(),
                                "type":"userCheck",
                                "data":{"msg":self.activeUsers}
                              }
                    self.serverSendMsgToClient(conn, dumps(to_send))  

                # wrong parameter handler
                else: 
                    to_send = {
                                "id": message['id'],
                                "time":time(),
                                "data": {"msg":False}
                              }
                    self.serverSendMsgToClient(conn, dumps(to_send))
            except:
                to_send = {    
                            "id": False,
                            "time":time(),
                            "data": {"msg":False}
                            }
                self.serverSendMsgToClient(conn, dumps(to_send))

    def initPipe(self):
        # setting handler role
        self.ADDR = (self.IP, self.PORT)
        if self.comRole == "SW": self.serverStartup()
        elif self.comRole == "CL": 
            self.clientHandlerStatus = True
            self.clientStartup()
            
    def serverStartup(self):
        self.serverThread = Thread(target=self.serverUserAgent)
        self.serverThread.start()

    def serverUserAgent(self):
        self.sw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sw.bind(("localhost", 6644))
        self.sw.listen()
        while True:
            conn, addr = self.sw.accept()
            threadRX = Thread(target=self.serverHandler, args=(conn, addr))
            threadRX.start()
            self.activeUsers = activeCount() - 2

    def serverHandler(self, conn, addr):
        try:
            # authentication part
            self.clients.append(conn)
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                try: 
                    message = loads(msg)
                except:
                    connected = False
                    conn.close()
                if message['data']['msg'] == self.AUTHENTICATION_KEY:
                    self.serverSendMsgToClient(conn, dumps({"id": message['id'], "time":time(), "data":{"msg":"Authentication Success!"}}))
                    connected = True
                    print(f"{addr} connected!")
            else:
                connected = False
                try : 
                    self.serverSendMsgToClient(conn, dumps({"id": message['id'], "time":time(), "data":{"msg":"Authentication Failed!"}}))
                    conn.close()
                except : 
                    pass
                
            # communication
            while connected:

                #receive msg
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:

                    # receiving command
                    
                        msg_length = int(msg_length)
                        msg = conn.recv(msg_length).decode(self.FORMAT)
                        # disconnect handler
                        try:
                            #print(msg)
                            if loads(msg)['data']['msg'] == self.DISCONNECT_MESSAGE: 
                                connected = False
                                self.serverSendMsgToClient(conn, dumps({"id": loads(msg)['id'], "time":time(), "data":{"msg":"Disconnect Confirmed!"}}))
                                break
                            else:
                                threadMSG = Thread(target=self.serverMsgHandler, args=(conn, msg))
                                threadMSG.start()
                        except: pass
                    
                else: pass     

            # close connection
            try: self.clients.remove(conn)
            except: print("Client already removed.")
            conn.close()
            print(f"Connection is closed on {addr}")
        except:
            self.clients.remove(conn)
            conn.close()
            print(f"Connection down detected on {addr}")

    def serverSendMsg(self, to_send):
        for conn in self.clients:
            try:
                ray_id = str(uuid.uuid4())
                msg = dumps({
                    "id" : ray_id,
                    "time": time(),
                    "type": "alert",
                    "data": {"msg":to_send}
                })
                print(msg)
                message = msg.encode(self.FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(self.FORMAT)
                send_length += b' ' * (self.HEADER- len(send_length))
                conn.send(send_length)
                conn.send(message)
            except: 
                self.clients.remove(conn)
                conn.close()
                print(f"Connection down detected on {conn}")

    def serverSendMsgToClient(self, conn, to_send):
            try:
                msg = to_send
                message = msg.encode(self.FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(self.FORMAT)
                send_length += b' ' * (self.HEADER- len(send_length))
                conn.sendall(send_length)
                conn.sendall(message)
            except:
                self.clients.remove(conn)
                conn.close()
                print(f"Connection down detected on {conn}")

    def clientStartup(self):
        self.cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            self.cl.connect(self.ADDR)
            self.clientConnectionStatus = True
        except Exception as e: print(e)
        if self.clientConnectionStatus == True:
            self.clientSendMsg(self.AUTHENTICATION_KEY)
            self.clientRXThread = Thread(target=self.clientRXHandler)
            self.clientRXThread.start()
            self.clientTXThread = Thread(target=self.clientTXHandler)
            self.clientTXThread.start()

    def clientRXHandler(self):
        while self.clientHandlerStatus == True:
            try: msg_length = self.cl.recv(self.HEADER).decode(self.FORMAT)
            except: pass
            if msg_length:
                try: 
                    msg_length = int(msg_length)
                    try: msg = self.cl.recv(msg_length).decode(self.FORMAT)
                    except: pass
                    print(msg)
                    self.logger.debug(f"Client RX : {msg}")
                    try: 
                        msg_buffer = loads(msg)
                        try:
                            if msg_buffer['data']['msg'] == "Disconnect Confirmed!": self.clientCloseStatus = True
                        except: pass
                        try:
                            self.bufferRX.append(msg_buffer)
                        except: pass
                    except: pass
                except : pass
    
    def clientTXHandler(self):
        while self.clientConnectionStatus == True:
            sleep(0.0001)
            if len(self.bufferTX) > 0:
                self.clientSendMsg(self.bufferTX[0])
                self.bufferTX.pop(0)
            else: pass

    def send(self, msg):
        if self.comRole == 'CL':
            self.bufferTX.append(msg)

    def clientSendMsg(self, to_send):
        self.clientMsgSendStatus = True
        ray_id = str(uuid.uuid4())
        to_send_buffer = to_send
        to_send = dumps({"id":ray_id, "time": time(), "data":{"msg":to_send}})
        message = to_send.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER- len(send_length))
        try:
            self.cl.send(send_length)
            self.cl.send(message)
        except: pass
        self.logger.debug(f"Client TX : {message.decode(self.FORMAT)}")
        if to_send_buffer == self.DISCONNECT_MESSAGE:
            while self.clientCloseStatus == False and self.clientMsgSendStatus == False: pass
            self.clientCloseStatus = False
            self.clientHandlerStatus = False
            self.clientConnectionStatus = False
            self.cl.close()
        self.clientMsgSendStatus == False

    def clientClose(self):
        self.clientSendMsg(self.DISCONNECT_MESSAGE)