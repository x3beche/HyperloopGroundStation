from files.graphical_interface import *
from time import sleep
import pafy
import cv2

class GeneralKapsulCamHander(QtCore.QThread):
    ImageUpdate = QtCore.pyqtSignal(QtGui.QImage)
    terminal_out = QtCore.pyqtSignal(str)

    def run(self):
        self.ImageUpdate.emit(QtGui.QImage("files/img/cam_connecting.png"))
        self.ThreadActive = True

        """url = "files/warr.mp4"
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")"""
        
        
        Capture = cv2.VideoCapture("files/warr.mp4")
        self.terminal_out.emit("Kaspsül kamerasına bağlanıldı.")

        while self.ThreadActive:
            
            try:
                sleep(0.016)
                ret, frame = Capture.read()
                
                if ret:
                    FlippedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                  
                    ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)
                else: 
                    self.ImageUpdate.emit(QtGui.QImage("files/img/kapsul.png"))
                    sleep(1)
                    Capture = cv2.VideoCapture("files/warr.mp4")
            except: pass

        self.ImageUpdate.emit(QtGui.QImage("files/img/kapsul.png"))
        self.terminal_out.emit("Kapsül kamerasının bağlantısı kesildi")
    
    def stop(self):
        self.ThreadActive = False
        self.quit()

class GeneralAemCamHander(QtCore.QThread):
    ImageUpdate = QtCore.pyqtSignal(QtGui.QImage)
    terminal_out = QtCore.pyqtSignal(str)

    def run(self):
        self.ImageUpdate.emit(QtGui.QImage("files/img/cam_connecting.png"))
        self.ThreadActive = True

        url = "https://www.youtube.com/watch?v=2yJU7oq9sNQ"
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        
        Capture = cv2.VideoCapture(best.url)
        self.terminal_out.emit("AEM kamerasına bağlanıldı.")
        while self.ThreadActive:
            try:
                sleep(0.016)
                ret, frame = Capture.read()
                
                if ret:
                    FlippedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                  
                    ConvertToQtFormat = QtGui.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QtGui.QImage.Format.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)
            except: pass

        self.ImageUpdate.emit(QtGui.QImage("files/img/aem.png"))
        self.terminal_out.emit("AEM kamerasının bağlantısı kesildi")
        
    def stop(self):
        self.ThreadActive = False
        self.quit()