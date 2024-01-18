from random import randint, uniform
from time import time

class sensorMonModule:
    def __init__(self):
        self.hiz = 0
        self.ivme = 0
        self.reflektor_sayici = 0
        self.batarya_v = 0
        self.batarya_a = 0
        self.motor_a = 0
        self.levitasyon_a = 0
        self.fren_a = 0
        self.fren_basinc = 0
        self.kapsul_basinc = 0
        self.fren_sicaklik = 0
        self.batarya_sicaklik = 0
        self.kapsul_sicaklik = 0
        self.bms_sicaklik = 0
        self.esc_sicaklik = 0
        self.konum = 0
        self.brake_force = 0
        self.mission_time = 0
        self.fren_status = "Kapalı"
        self.levitasyon_status = "Kapalı"
        self.asama = "0"

    def updateSensorValues(self):
        try:
            if self.konum == 0:
                self.asama = "7"
                self.reflektor_sayici = 0
                self.batarya_a = 0
                self.currentTime = time()
                self.levitasyon_status = "Açık"
                self.fren_status = "Kapalı"
            if self.konum <= 1650: self.mission_time = time() - self.currentTime

            if self.konum <= 2500:
                if self.konum <= 1800:
                    self.reflektor_sayici = int(self.konum / 10.6)
                    self.capsule_status = "Hareket Halinde"
                    self.levitasyon_a = randint(57,60)
                    
                elif self.konum > 1800:
                    self.levitasyon_a = 0
                    self.batarya_a = 0
                    self.asama = "Final"
                    self.capsule_status = "Kapsül Durduruldu"
                    self.levitasyon_status = "Kapalı"
                    self.fren_status = "Kapalı"
                    self.hiz = randint(0,1)
                    self.ivme = 0

                self.konum += 6
                self.kapsul_basinc = randint(0,1)
                self.fren_basinc = randint(12,14)
                self.batarya_a = self.fren_a + self.levitasyon_a + self.motor_a + randint(3,4)
                self.batarya_v = round(uniform(23.4,24.0),2)
            else:
                self.cacheTime = time()
                self.konum = 0

            if self.konum <= 400:
                self.ivme = randint(3,5)
                self.motor_a = randint(23, 25)
                self.hiz += self.ivme
            elif self.konum > 400 and self.konum <= 1200: 
                self.ivme = randint(1,2)
                self.motor_a = randint(32, 34)
                self.hiz += self.ivme
            elif self.konum > 1200 and self.konum <= 1400:
                self.ivme = randint(0,1)
                self.motor_a = randint(25, 40)
                self.hiz += self.ivme
                self.brake_force = self.hiz / 33.5
            elif self.konum > 1400 and self.konum <= 1800:
                self.asama = "8"
                self.motor_a = 0
                self.fren_sicaklik += randint(0,1)
                self.hiz = int(self.hiz - self.brake_force)
                if self.konum <= 1600: self.ivme = -1*int(self.brake_force)
                else: self.ivme = 0
                self.fren_status = "Açık"
                self.fren_a = randint(20,22)
                if self.hiz < 0: self.hiz = 0
            else: 
                self.fren_a = 0
                self.motor_a = 0
                
            if self.konum <= 200:
                self.fren_sicaklik = randint(25,27)
                self.batarya_sicaklik = randint(32,33)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 200 and self.konum <= 400:
                self.fren_sicaklik = randint(25,27)
                self.batarya_sicaklik = randint(34,35)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 400 and self.konum <= 600:
                self.fren_sicaklik = randint(25,27)
                self.batarya_sicaklik = randint(34,35)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 600 and self.konum <= 800:
                self.fren_sicaklik = randint(25,27)
                self.batarya_sicaklik = randint(34,35)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 1000 and self.konum <= 1200:
                self.fren_sicaklik = randint(25,27)
                self.batarya_sicaklik = randint(36,37)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 1200 and self.konum <= 1400:
                self.fren_sicaklik = randint(25,27)
                self.batarya_sicaklik = randint(36,37)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 1400 and self.konum <= 1800:
                self.batarya_sicaklik = randint(36,37)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 1800 and self.konum <= 2300:
                self.fren_sicaklik = randint(42,45)
                self.batarya_sicaklik = randint(36,37)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
            elif self.konum > 2300 and self.konum <= 2500:
                self.fren_sicaklik -= randint(0,1)
            else:
                self.batarya_sicaklik = randint(32,33)
                self.kapsul_sicaklik = randint(27,28)
                self.bms_sicaklik = randint(32,33)
                self.esc_sicaklik = randint(29,31)
        except Exception as e: print(e) 
    def sensorValues(self):
        #self.updateSensorValues()

        return {"hiz":              self.hiz,
                "ivme":             self.ivme,
                "reflektor_sayici": self.reflektor_sayici,
                "batarya_v":        self.batarya_v,
                "batarya_a":        self.batarya_a,
                "motor_a":          self.motor_a,
                "levitasyon_a":     self.levitasyon_a,
                "fren_a":           self.fren_a,
                "fren_basinc":      self.fren_basinc,
                "kapsul_basinc":    self.kapsul_basinc,
                "fren_sicaklik":    self.fren_sicaklik,
                "batarya_sicaklik": self.batarya_sicaklik,
                "kapsul_sicaklik":  self.kapsul_sicaklik,
                "bms_sicaklik":     self.bms_sicaklik,
                "esc_sicaklik":     self.esc_sicaklik,
                "konum":            self.konum,
                "mission_time":     self.mission_time,
                "capsule_status":   self.capsule_status,
                "fren_status":      self.fren_status,
                "levitasyon_status":self.levitasyon_status,
                "asama":            self.asama}