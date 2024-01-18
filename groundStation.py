from files.graphical_interface import *
from modules.msgHandler import *
from modules.camHandler import *
from modules.hCOM import hComModule
from yaml import safe_load
from collections import deque
from time import ctime

class Arayuz(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.kapsulKonum.setRange(0,1600)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.sensorArayuzGraphColor = False
        self.sensorArayuzGraphCache = 7
        self.sensorMonitorizeStatus = True
        self.comStat = False
        self.kapsulKameraStatus = False
        self.aemKameraStatus = False
        self.info_color = "#FFD801"
        self.warning_color = "#ff0f0f"
        self.success_color = "#FF4CAF50"
        self.chat_time_color = "#D3D3D3"
        self.chat_user_color = "#F6F6F6"
        self.chat_root_color = "#5B9EFE"

        with open("config.yaml") as file: self.configurations = safe_load(file)
        self.terminal("SUCCESS", "Config dosyaları içe aktarıldı.")

        self.initInterface()
        self.initConnections()
        self.initButtons()
        self.initsensorArayuzGraphs()

        self.x = deque(maxlen=300)
        self.y = deque(maxlen=300)

        self.comPipe = hComModule(self.configurations['communication'],
                comRole = "CL",
                logging_identity = self.configurations["logging_idendity"])
        self.terminal("INFO", "Haberleşme handler'ları başlatıldı.")

        """self.ui.motor_slider.setValue(50)
        self.ui.lvtsyn_slider.setValue(70)
        self.ui.light_slider.setValue(20)"""

    def initsensorArayuzGraphs(self):


        self.ui.hizPlotAnlik.setRange(yRange=[0,500])
        self.ui.hizPlotAnlik.setBackground(background=None)

        self.ui.hizPlotGecmis.setRange(yRange=[0,500])
        self.ui.hizPlotGecmis.setMouseEnabled(x=False, y=False)
        self.ui.hizPlotGecmis.setBackground(background=None)

        self.ui.hiz_plot.hideAxis('bottom')
        self.ui.hiz_plot.hideAxis('left')
        self.hiz_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.hiz_plot.setRange(yRange=[0,500])
        self.ui.hiz_plot.setBackground(background=None)

        self.ui.ivme_plot.hideAxis('bottom')
        self.ui.ivme_plot.hideAxis('left')
        self.ivme_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.ivme_plot.setRange(yRange=[-20,20])
        self.ui.ivme_plot.setBackground(background=None)

        self.ui.reflektor_sayaci_plot.hideAxis('bottom')
        self.ui.reflektor_sayaci_plot.hideAxis('left')
        self.reflektor_sayaci_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.reflektor_sayaci_plot.setRange(yRange=[0,150])
        self.ui.reflektor_sayaci_plot.setBackground(background=None)

        self.ui.kapsul_sicaklik_plot.hideAxis('bottom')
        self.ui.kapsul_sicaklik_plot.hideAxis('left')
        self.kapsul_sicaklik_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.kapsul_sicaklik_plot.setRange(yRange=[20,30])
        self.ui.kapsul_sicaklik_plot.setBackground(background=None)

        self.ui.bms_sicaklik_plot.hideAxis('bottom')
        self.ui.bms_sicaklik_plot.hideAxis('left')
        self.bms_sicaklik_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.bms_sicaklik_plot.setRange(yRange=[25,35])
        self.ui.bms_sicaklik_plot.setBackground(background=None)

        self.ui.esc_sicaklik_plot.hideAxis('bottom')
        self.ui.esc_sicaklik_plot.hideAxis('left')
        self.esc_sicaklik_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.esc_sicaklik_plot.setRange(yRange=[25,35])
        self.ui.esc_sicaklik_plot.setBackground(background=None)

        self.ui.batarya_volt_plot.hideAxis('bottom')
        self.ui.batarya_volt_plot.hideAxis('left')
        self.batarya_volt_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.batarya_volt_plot.setRange(yRange=[20,25])
        self.ui.batarya_volt_plot.setBackground(background=None)

        self.ui.batarya_akimi_plot.hideAxis('bottom')
        self.ui.batarya_akimi_plot.hideAxis('left')
        self.batarya_akimi_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.batarya_akimi_plot.setRange(yRange=[0,150])
        self.ui.batarya_akimi_plot.setBackground(background=None)

        self.ui.motor_akimi_plot.hideAxis('bottom')
        self.ui.motor_akimi_plot.hideAxis('left')
        self.motor_akimi_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.motor_akimi_plot.setRange(yRange=[0,35])
        self.ui.motor_akimi_plot.setBackground(background=None)

        self.ui.levitasyon_akimi_plot.hideAxis('bottom')
        self.ui.levitasyon_akimi_plot.hideAxis('left')
        self.levitasyon_akimi_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.levitasyon_akimi_plot.setRange(yRange=[0,70])
        self.ui.levitasyon_akimi_plot.setBackground(background=None)

        self.ui.fren_akimi_plot.hideAxis('bottom')
        self.ui.fren_akimi_plot.hideAxis('left')
        self.fren_akimi_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.fren_akimi_plot.setRange(yRange=[0,30])
        self.ui.fren_akimi_plot.setBackground(background=None)

        self.ui.fren_basinci_plot.hideAxis('bottom')
        self.ui.fren_basinci_plot.hideAxis('left')
        self.fren_basinci_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.fren_basinci_plot.setRange(yRange=[0,20])
        self.ui.fren_basinci_plot.setBackground(background=None)

        self.ui.kapsul_basinci_plot.hideAxis('bottom')
        self.ui.kapsul_basinci_plot.hideAxis('left')
        self.kapsul_basinci_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.kapsul_basinci_plot.setRange(yRange=[0,5])
        self.ui.kapsul_basinci_plot.setBackground(background=None)

        self.ui.fren_sicaklik_plot.hideAxis('bottom')
        self.ui.fren_sicaklik_plot.hideAxis('left')
        self.fren_sicaklik_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.fren_sicaklik_plot.setRange(yRange=[25,50])
        self.ui.fren_sicaklik_plot.setBackground(background=None)

        self.ui.batarya_sicaklik_plot.hideAxis('bottom')
        self.ui.batarya_sicaklik_plot.hideAxis('left')
        self.batarya_sicaklik_plot_deq = deque([], maxlen=self.sensorArayuzGraphCache)
        self.ui.batarya_sicaklik_plot.setRange(yRange=[25,40])
        self.ui.batarya_sicaklik_plot.setBackground(background=None)

        self.terminal("SUCCESS", "Grafik motorları başlatıldı.")

    def initInterface(self):

        self.ui.port.setText(str(self.configurations['communication']['PORT']))
        self.ui.adres.setText(self.configurations['communication']['IP'])
        self.ui.port_arayuz.setText(str(self.configurations['communication']['PORT']))
        self.ui.adres_arayuz.setText(self.configurations['communication']['IP'])
        self.ui.terminal.setReadOnly(True)
        self.terminal("SUCCESS", "Arayüz başlatıldı.")

    def initConnections(self):

        self.ui.baglan.clicked.connect(self.initCommunication)
        self.ui.baglantiyi_kes.clicked.connect(self.terminateCommunication)
        self.ui.baglanArayuz.clicked.connect(self.initCommunication)
        self.ui.baglantiyiKesArayuz.clicked.connect(self.terminateCommunication)
        self.ui.yenile.clicked.connect(self.refreshCommunication)
        self.ui.port.textChanged.connect(self.connectionTextSync)
        self.ui.adres.textChanged.connect(self.connectionTextSync)
        self.ui.kapsul_kamera_button.clicked.connect(self.kapsulKameraHandler)
        self.ui.aem_kamera_button.clicked.connect(self.aemKameraHandler)

        self.ui.simulasyon.clicked.connect(self.simulasyonHandler)
        self.ui.exitButton.clicked.connect(self.exitHandler)
        self.ui.hiz_grafigi_limit_5.clicked.connect(self.changeHizDeque5)
        self.ui.hiz_grafigi_limit_20.clicked.connect(self.changeHizDeque20)
        self.ui.hiz_grafigi_limit_45.clicked.connect(self.changeHizDeque45)
        self.ui.hiz_grafigi_limit_90.clicked.connect(self.changeHizDeque90)
        self.ui.hiz_grafigi_limit_150.clicked.connect(self.changeHizDeque150)
        self.ui.hiz_grafigi_limit_350.clicked.connect(self.changeHizDeque350)

        self.ui.motor_slider.valueChanged.connect(self.motorUpdate)
        self.ui.lvtsyn_slider.valueChanged.connect(self.lvtsynUpdate)
        self.ui.brake_slider.valueChanged.connect(self.brakeUpdate)
        self.ui.light_slider.valueChanged.connect(self.lightUpdate)

        self.terminal("SUCCESS", "Arayüz bağlantıları başarılı bir şekilde oluşturuldu.")

    def simulasyonHandler(self):
        self.terminal("INFO", "Simulasyon Başlatıldı.")
        self.initCommunication()
        self.kapsulKameraHandler()

    def initButtons(self):
        self.ui.baglanti_kilit_kaldirma.setEnabled(True)
        self.ui.baglantiyi_kes.setEnabled(False)
        #self.ui.latency_check_button.setEnabled(False)
        #self.ui.current_user_button.setEnabled(False)
        self.ui.yenile.setEnabled(False)
        self.ui.latency.setEnabled(False)
        self.ui.user.setEnabled(False)
        self.ui.baglantiyiKesArayuz.setEnabled(False)

    def initCommunication(self):

        try:
            self.comPipe.PORT = int(self.ui.port.text())
            self.comPipe.IP   = self.ui.adres.text()
            self.comPipe.initPipe()
            self.comStat = True
        except: pass

        if self.comStat == True:
            self.terminal("SUCCESS", f"{self.comPipe.IP}:{self.comPipe.PORT} haberleşmesi başlatıldı.")
            self.initThreads()
            self.ui.router_and_capsule.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;background-color: #092215;color: #00e640;border-radius: 7px;}")
            self.ui.router_and_capsule.setText('✓')
            self.ui.baglan.setEnabled(False)
            self.ui.baglanArayuz.setEnabled(False)
            self.ui.baglantiyi_kes.setEnabled(True)
            self.ui.baglantiyiKesArayuz.setEnabled(True)
            #self.ui.latency_check_button.setEnabled(True)
            #self.ui.current_user_button.setEnabled(True)
            self.ui.yenile.setEnabled(True)
            self.ui.port.setEnabled(False)
            self.ui.adres.setEnabled(False)
        else: pass

    def initThreads(self):

        self.GeneralMsgHanderThread = GeneralMsgHander(self.comPipe)
        self.GeneralMsgHanderThread.sensor_verileri.connect(self.sensorArayuz)
        self.GeneralMsgHanderThread.terminal_out.connect(self.AryuzTerminal)
        self.GeneralMsgHanderThread.rx_buffer_len.connect(self.rxBufferTextUpdate)
        self.GeneralMsgHanderThread.tx_buffer_len.connect(self.txBufferTextUpdate)
        self.GeneralMsgHanderThread.latency_out.connect(self.latencyUpdate)
        self.GeneralMsgHanderThread.user_out.connect(self.userUpdate)
        self.GeneralMsgHanderThread.start()

        self.terminal("INFO", "Haberleşme thread'leri ve arayüz sinyalleri oluşturuldu.")

    def sensorArayuzGraphUpdate(self):

        graph_pen = "w"

        self.ui.hiz_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.hiz_plot_deq[0] > self.hiz_plot_deq[-1]: graph_pen = "r"
            elif self.hiz_plot_deq[0] < self.hiz_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.hiz_plot.plot([i for i in range(0,len(self.hiz_plot_deq))], self.hiz_plot_deq, pen=graph_pen)

        self.ui.ivme_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.ivme_plot_deq[0] > self.ivme_plot_deq[-1]: graph_pen = "r"
            elif self.ivme_plot_deq[0] < self.ivme_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.ivme_plot.plot([i for i in range(0,len(self.ivme_plot_deq))], self.ivme_plot_deq, pen=graph_pen)

        self.ui.reflektor_sayaci_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.reflektor_sayaci_plot_deq[0] > self.reflektor_sayaci_plot_deq[-1]: graph_pen = "r"
            elif self.reflektor_sayaci_plot_deq[0] < self.reflektor_sayaci_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.reflektor_sayaci_plot.plot([i for i in range(0,len(self.reflektor_sayaci_plot_deq))], self.reflektor_sayaci_plot_deq, pen=graph_pen)

        self.ui.batarya_volt_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.batarya_volt_plot_deq[0] > self.batarya_volt_plot_deq[-1]: graph_pen = "r"
            elif self.batarya_volt_plot_deq[0] < self.batarya_volt_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.batarya_volt_plot.plot([i for i in range(0,len(self.batarya_volt_plot_deq))], self.batarya_volt_plot_deq, pen=graph_pen)

        self.ui.batarya_akimi_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.batarya_akimi_plot_deq[0] > self.batarya_akimi_plot_deq[-1]: graph_pen = "r"
            elif self.batarya_akimi_plot_deq[0] < self.batarya_akimi_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.batarya_akimi_plot.plot([i for i in range(0,len(self.batarya_akimi_plot_deq))], self.batarya_akimi_plot_deq, pen=graph_pen)

        self.ui.motor_akimi_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.motor_akimi_plot_deq[0] > self.motor_akimi_plot_deq[-1]: graph_pen = "r"
            elif self.motor_akimi_plot_deq[0] < self.motor_akimi_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.motor_akimi_plot.plot([i for i in range(0,len(self.motor_akimi_plot_deq))], self.motor_akimi_plot_deq, pen=graph_pen)

        self.ui.levitasyon_akimi_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.levitasyon_akimi_plot_deq[0] > self.levitasyon_akimi_plot_deq[-1]: graph_pen = "r"
            elif self.levitasyon_akimi_plot_deq[0] < self.levitasyon_akimi_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.levitasyon_akimi_plot.plot([i for i in range(0,len(self.levitasyon_akimi_plot_deq))], self.levitasyon_akimi_plot_deq, pen=graph_pen)

        self.ui.fren_akimi_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.fren_akimi_plot_deq[0] > self.fren_akimi_plot_deq[-1]: graph_pen = "r"
            elif self.fren_akimi_plot_deq[0] < self.fren_akimi_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.fren_akimi_plot.plot([i for i in range(0,len(self.fren_akimi_plot_deq))], self.fren_akimi_plot_deq, pen=graph_pen)

        self.ui.fren_basinci_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.fren_basinci_plot_deq[0] > self.fren_basinci_plot_deq[-1]: graph_pen = "r"
            elif self.fren_basinci_plot_deq[0] < self.fren_basinci_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.fren_basinci_plot.plot([i for i in range(0,len(self.fren_basinci_plot_deq))], self.fren_basinci_plot_deq, pen=graph_pen)

        self.ui.kapsul_basinci_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.kapsul_basinci_plot_deq[0] > self.kapsul_basinci_plot_deq[-1]: graph_pen = "r"
            elif self.kapsul_basinci_plot_deq[0] < self.kapsul_basinci_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.kapsul_basinci_plot.plot([i for i in range(0,len(self.kapsul_basinci_plot_deq))], self.kapsul_basinci_plot_deq, pen=graph_pen)

        self.ui.fren_sicaklik_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.fren_sicaklik_plot_deq[0] > self.fren_sicaklik_plot_deq[-1]: graph_pen = "r"
            elif self.fren_sicaklik_plot_deq[0] < self.fren_sicaklik_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.fren_sicaklik_plot.plot([i for i in range(0,len(self.fren_sicaklik_plot_deq))], self.fren_sicaklik_plot_deq, pen=graph_pen)

        self.ui.batarya_sicaklik_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.batarya_sicaklik_plot_deq[0] > self.batarya_sicaklik_plot_deq[-1]: graph_pen = "r"
            elif self.batarya_sicaklik_plot_deq[0] < self.batarya_sicaklik_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.batarya_sicaklik_plot.plot([i for i in range(0,len(self.batarya_sicaklik_plot_deq))], self.batarya_sicaklik_plot_deq, pen=graph_pen)

        self.ui.kapsul_sicaklik_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.kapsul_sicaklik_plot_deq[0] > self.kapsul_sicaklik_plot_deq[-1]: graph_pen = "r"
            elif self.kapsul_sicaklik_plot_deq[0] < self.kapsul_sicaklik_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.kapsul_sicaklik_plot.plot([i for i in range(0,len(self.kapsul_sicaklik_plot_deq))], self.kapsul_sicaklik_plot_deq, pen=graph_pen)

        self.ui.bms_sicaklik_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.bms_sicaklik_plot_deq[0] > self.bms_sicaklik_plot_deq[-1]: graph_pen = "r"
            elif self.bms_sicaklik_plot_deq[0] < self.bms_sicaklik_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.bms_sicaklik_plot.plot([i for i in range(0,len(self.bms_sicaklik_plot_deq))], self.bms_sicaklik_plot_deq, pen=graph_pen)

        self.ui.esc_sicaklik_plot.clear()
        if self.sensorArayuzGraphColor == True:
            if self.esc_sicaklik_plot_deq[0] > self.esc_sicaklik_plot_deq[-1]: graph_pen = "r"
            elif self.esc_sicaklik_plot_deq[0] < self.esc_sicaklik_plot_deq[-1]: graph_pen = "g"
            else: graph_pen = "w"
        self.ui.esc_sicaklik_plot.plot([i for i in range(0,len(self.esc_sicaklik_plot_deq))], self.esc_sicaklik_plot_deq, pen=graph_pen)

    def sensorArayuz(self, generalData):

        data = generalData['data']['msg']
        self.ui.hiz_text.setText(str(data['hiz']))
        self.hiz_plot_deq.append(data['hiz'])

        self.x.append(ctime(generalData['time']).split(" ")[3])
        self.y.append(data["hiz"])

        self.ui.ivme_text.setText(str(data['ivme']))
        self.ivme_plot_deq.append(data['ivme'])

        self.ui.reflektor_sayaci_text.setText(str(data['reflektor_sayici']))
        self.reflektor_sayaci_plot_deq.append(data["reflektor_sayici"])

        self.ui.batarya_volt_text.setText(str(data['batarya_v']))
        self.batarya_volt_plot_deq.append(data['batarya_v'])

        self.ui.batarya_akimi_text.setText(str(data['batarya_a']))
        self.batarya_akimi_plot_deq.append(data['batarya_a'])

        self.ui.motor_akimi_text.setText(str(data['motor_a']))
        self.motor_akimi_plot_deq.append(data['motor_a'])

        self.ui.levitasyon_akimi_text.setText(str(data['levitasyon_a']))
        self.levitasyon_akimi_plot_deq.append(data['levitasyon_a'])

        self.ui.fren_akimi_text.setText(str(data['fren_a']))
        self.fren_akimi_plot_deq.append(data['fren_a'])

        self.ui.fren_basinci_text.setText(str(data['fren_basinc']))
        self.fren_basinci_plot_deq.append(data['fren_basinc'])

        self.ui.kapsul_basinci_text.setText(str(data['kapsul_basinc']))
        self.kapsul_basinci_plot_deq.append(data['kapsul_basinc'])

        self.ui.fren_sicaklik_text.setText(str(data['fren_sicaklik']))
        self.fren_sicaklik_plot_deq.append(data['fren_sicaklik'])

        self.ui.batarya_sicaklik_text.setText(str(data['batarya_sicaklik']))
        self.batarya_sicaklik_plot_deq.append(data['batarya_sicaklik'])

        self.ui.kapsul_sicaklik_text.setText(str(data['kapsul_sicaklik']))
        self.kapsul_sicaklik_plot_deq.append(data['kapsul_sicaklik'])

        self.ui.bms_sicaklik_text.setText(str(data['bms_sicaklik']))
        self.bms_sicaklik_plot_deq.append(data['bms_sicaklik'])

        self.ui.esc_sicaklik_text.setText(str(data['esc_sicaklik']))
        self.esc_sicaklik_plot_deq.append(data['esc_sicaklik'])

        self.ui.kapsulKonum.setValue(data['konum'])
        self.ui.sure.setText(f"{round(data['mission_time'], 5)} / 17.00000")
        self.ui.kapsul_durumu.setText(data['capsule_status'])

        fren_status = data['fren_status']
        levitasyon_status = data['levitasyon_status']

        self.ui.asama.setText(data['asama'])
        self.ui.fren.setText(fren_status)
        self.ui.levitasyon.setText(levitasyon_status)

        if fren_status == "Açık": self.ui.fren.setStyleSheet('QLabel{font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;background-color: #092215;color: #00e640;border-radius: 10px;}')
        else: self.ui.fren.setStyleSheet('QLabel{font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;background-color: #380000;color: #ff2400;border-radius: 10px;}')
        if levitasyon_status == "Açık": self.ui.levitasyon.setStyleSheet('QLabel{font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;background-color: #092215;color: #00e640;border-radius: 10px;}')
        else: self.ui.levitasyon.setStyleSheet('QLabel{font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;background-color: #380000;color: #ff2400;border-radius: 10px;}')


        self.sensorArayuzGraphUpdate()
        self.draw()

    def draw(self):

        if len(self.x) > 1 and len(self.y) > 1:
            self.ui.hizPlotAnlik.clear()
            self.ui.hizPlotGecmis.clear()

            try:
                if self.y[-2] > self.y[-1]: penColor = "r"
                if self.y[-2] < self.y[-1]: penColor = "g"
                if self.y[-2] == self.y[-1]: penColor = "w"
            except:pass

            self.ui.hizPlotAnlik.plot([0,1], [self.y[-2], self.y[-1]], pen=penColor, symbol='o', symbolPen=penColor, symbolBrush=0.2, name='green')
            self.ui.hizPlotGecmis.plot(range(len(self.y)), self.y)

            b = []
            for x in range(len(self.x)-2): b.append("")
            a = [self.x[0]] + b + [self.x[-1]]

            ticks = [list(zip(range(len(self.x)), a))]

            xax = self.ui.hizPlotGecmis.getAxis('bottom')
            xax.setTicks(ticks)

    def exitHandler(self):
        if self.comStat == True: self.terminateCommunication()
        if self.kapsulKameraStatus == True: self.kapsulKameraHandler()
        if self.aemKameraHandler == True: self.aemKameraHandler()
        sleep(0.1)
        exit()

    def latencyCheck(self):
        self.comPipe.send("getLatency")

    def latencyUpdate(self, val):
        self.ui.latency.setText(val)
        self.ui.latencyArayuz.setText(val.replace('ms',""))

    def refreshCommunication(self):
        self.terminateCommunication()
        sleep(0.1)
        self.initCommunication()

    def userCheck(self):
        self.comPipe.send("getUser")

    def userUpdate(self, val):
        self.ui.user.setText(val)

    def kapsulKameraHandler(self):
        if self.kapsulKameraStatus == False:
            self.GeneralKapsulCamHandlerThread = GeneralKapsulCamHander()
            self.GeneralKapsulCamHandlerThread.ImageUpdate.connect(self.kapsulCamUpdate)
            self.GeneralKapsulCamHandlerThread.start()
            self.GeneralKapsulCamHandlerThread.terminal_out.connect(self.AryuzTerminal)
            self.ui.kapsul_kamera_button.setText("OFF")
            self.ui.capsule_and_cam1.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;background-color: #092215;color: #00e640;border-radius: 7px;}")
            self.ui.capsule_and_cam1.setText('✓')
            self.kapsulKameraStatus = True

        elif self.kapsulKameraStatus == True:
            self.GeneralKapsulCamHandlerThread.stop()
            self.ui.capsule_and_cam1.setStyleSheet("QLabel{	font-family: Arial;	font-style: normal;	font-size: 12pt;	font-weight: bold;	background-color: #380000;	color: #ff2400;border-radius: 7px;}")
            self.ui.capsule_and_cam1.setText('x')
            self.kapsulKameraStatus = False
            self.ui.kapsul_kamera_button.setText("ON")

    def aemKameraHandler(self):
        if self.aemKameraStatus == False:
            self.GeneralAemCamHandlerThread = GeneralAemCamHander()
            self.GeneralAemCamHandlerThread.ImageUpdate.connect(self.aemCamUpdate)
            self.GeneralAemCamHandlerThread.start()
            self.GeneralKapsulCamHandlerThread.terminal_out.connect(self.AryuzTerminal)
            self.ui.aem_kamera_button.setText("OFF")
            self.ui.capsule_and_cam2.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;background-color: #092215;color: #00e640;border-radius: 7px;}")
            self.ui.capsule_and_cam2.setText('✓')
            self.aemKameraStatus = True

        elif self.aemKameraStatus == True:
            self.GeneralAemCamHandlerThread.stop()
            self.ui.capsule_and_cam2.setStyleSheet("QLabel{	font-family: Arial;	font-style: normal;	font-size: 12pt;	font-weight: bold;	background-color: #380000;	color: #ff2400;border-radius: 7px;}")
            self.ui.capsule_and_cam2.setText('x')
            self.aemKameraStatus = False
            self.ui.aem_kamera_button.setText("ON")

    def kapsulCamUpdate(self, Image):
        self.ui.kapsul_kamera_label.setPixmap(QtGui.QPixmap.fromImage(Image))

    def aemCamUpdate(self, Image):
        self.ui.aem_kamera_label.setPixmap(QtGui.QPixmap.fromImage(Image))

    def terminateCommunication(self):

        self.comStat = False
        self.terminal("WARNING", f"{self.comPipe.IP}:{self.comPipe.PORT} haberleşmesi sonlandırıldı.")
        self.ui.router_and_capsule.setStyleSheet("QLabel{	font-family: Arial;	font-style: normal;	font-size: 12pt;	font-weight: bold;	background-color: #380000;	color: #ff2400;border-radius: 7px;}")
        self.ui.router_and_capsule.setText('x')
        self.ui.baglantiyi_kes.setEnabled(False)
        self.ui.baglantiyiKesArayuz.setEnabled(False)
        #self.ui.latency_check_button.setEnabled(False)
        #self.ui.current_user_button.setEnabled(False)
        self.ui.yenile.setEnabled(False)
        self.ui.port.setEnabled(True)
        self.ui.adres.setEnabled(True)
        self.comPipe.clientClose()
        self.ui.baglan.setEnabled(True)
        self.ui.baglanArayuz.setEnabled(True)
        self.terminal("WARNING", "Haberleşme thread'leri ve arayüz sinyalleri sinyalleri durduruldu.")

    def communicationGecikme(self, gecikme):
        self.ui.latency.setText(str(gecikme)+"ms")

    def AryuzTerminal(self, msg):
        self.terminal("INFO", msg)

    def terminal(self, status, msg):

        if status ==      "INFO": self.ui.terminal.insertHtml(f'<font color={self.chat_user_color}><strong>INFO :: </strong></font><font color="white">{msg}</font><br>')
        elif status == "WARNING": self.ui.terminal.insertHtml(f'<font color={self.warning_color  }><strong>WARNING :: </strong></font><font color="white">{msg}</font><br>')
        elif status == "SUCCESS": self.ui.terminal.insertHtml(f'<font color={self.success_color  }><strong>SUCCESS :: </strong></font><font color="white">{msg}</font><br>')
        self.ui.terminal.verticalScrollBar().setValue(self.ui.terminal.verticalScrollBar().maximum())

    def connectionTextSync(self):

        self.ui.port_arayuz.setText(self.ui.port.text())
        self.ui.adres_arayuz.setText(self.ui.adres.text())

    def txBufferTextUpdate(self, val):
        self.ui.tx_buffer.setText(str(val))

    def rxBufferTextUpdate(self, val):
        self.ui.rx_buffer.setText(str(val))

    def motorUpdate(self):
        self.ui.motor_slider_lcd.display(self.ui.motor_slider.value())
    def lvtsynUpdate(self):
        self.ui.lvtsyn_slider_lcd.display(self.ui.lvtsyn_slider.value())
    def brakeUpdate(self):
        self.ui.brake_slider_lcd.display(self.ui.brake_slider.value())
    def lightUpdate(self):
        self.ui.light_slider_lcd.display(self.ui.light_slider.value())
    def changeHizDeque5(self):
        self.x = deque(maxlen=5)
        self.y = deque(maxlen=5)
    def changeHizDeque20(self):
        self.x = deque(maxlen=20)
        self.y = deque(maxlen=20)
    def changeHizDeque45(self):
        self.x = deque(maxlen=45)
        self.y = deque(maxlen=45)
    def changeHizDeque90(self):
        self.x = deque(maxlen=90)
        self.y = deque(maxlen=90)
    def changeHizDeque150(self):
        self.x = deque(maxlen=150)
        self.y = deque(maxlen=150)
    def changeHizDeque350(self):
        self.x = deque(maxlen=350)
        self.y = deque(maxlen=350)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Arayuz()
    ui.showMaximized()
    sys.exit(app.exec())
