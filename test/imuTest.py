from mpu6050 import MPU
from time import time

# Set up class
gyro = 250      # 250, 500, 1000, 2000 [deg/s]
acc = 2         # 2, 4, 7, 16 [g]
tau = 0.98
mpu = MPU(gyro, acc, tau)

# Set up sensor and calibrate gyro with N points
mpu.setUp()

input("Press key for start calibration")
mpu.calibrateGyro(500)

def acceleration_test(x = 0):
    while True:
        mpu.compFilter()
        acceleration = mpu.ax * 9.80665
        if acceleration < -5 or acceleration > 5:
            print("%.2f" % acceleration, time()-x )
        x = time()

def angle_test(x = 0):
    while True:
        mpu.compFilter()
        print(mpu.pitch, mpu.roll, mpu.yaw, time() - x)
        x = time()

x = input("Select test:\n1-) Acceleration Test\n2-) Angle Test\nSelection > ")
if x.isnumeric():
    if int(x) == 1: acceleration_test()
    elif int(x) == 2: angle_test()
    else: pass
else: pass