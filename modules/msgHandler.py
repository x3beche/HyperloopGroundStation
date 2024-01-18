from flask_login import user_logged_out
from files.graphical_interface import *
from time import sleep, time
from json import dumps

class GeneralMsgHander(QtCore.QThread):
    
    sensor_verileri = QtCore.pyqtSignal(dict)
    terminal_out = QtCore.pyqtSignal(str)
    latency_out  = QtCore.pyqtSignal(str)
    rx_buffer_len = QtCore.pyqtSignal(int)
    tx_buffer_len = QtCore.pyqtSignal(int)
    user_out = QtCore.pyqtSignal(str)

    def __init__(self, comPipe, parent = None):
        super(GeneralMsgHander, self).__init__(parent)
        self.comPipe = comPipe
    
        self.sensor_value_request_interval = 0.05
        self.sensor_value_request_cache = time()

        self.latency_request_interval = 0.5
        self.latency_request_cache = time()

    def run(self):
        self.comPipe.send("getLatency")
        self.comPipe.send("getUser")
        
        while self.comPipe.clientConnectionStatus:
            
            sleep(0.01)
            
            if len(self.comPipe.bufferRX) > 0:
                buffer = self.comPipe.bufferRX[0]
                try:
                    
                    if buffer["type"] == "sensorData":
                        self.sensor_verileri.emit(buffer)
                    
                    elif buffer["type"] == "alert":
                        self.terminal_out.emit(buffer['data']['msg'])

                    elif buffer["type"] == "latencyCheck":
                        latency = str(int((time() - buffer['data']['msg'])*1000/2))+"ms"
                        self.latency_out.emit(latency)

                    elif buffer['type'] == "userCheck":
                        user = str(buffer["data"]['msg'])
                        self.user_out.emit(user)

                except:
                    #self.terminal_out.emit(dumps(buffer))
                    pass

                self.comPipe.bufferRX.pop(0) 
            
            # get sensor values
            if time()-self.sensor_value_request_cache >= self.sensor_value_request_interval and self.comPipe.clientConnectionStatus:
                self.comPipe.send("getSensorValues")
                self.sensor_value_request_cache = time()

            # get latency
            if time()-self.latency_request_cache >= self.latency_request_interval and self.comPipe.clientConnectionStatus:
                self.comPipe.send("getLatency")
                self.latency_request_cache = time()

            # sending buffer informations
            self.rx_buffer_len.emit(len(self.comPipe.bufferRX))
            self.tx_buffer_len.emit(len(self.comPipe.bufferTX))
        