import subprocess
import time
import lgpio

LED = 17

def get_temp():
        cpu_temp = subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp")
        cpu_temp = int(cpu_temp)/1000
        return cpu_temp

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, LED)

try:
    while True:
        # Turn the GPIO pin on
        temp = get_temp()
        if temp > 60: lgpio.gpio_write(h, LED, 1)
        elif temp < 50: lgpio.gpio_write(h, LED, 0)
        else: pass
        time.sleep(2) 

except KeyboardInterrupt:
    lgpio.gpio_write(h, LED, 0)
    lgpio.gpiochip_close(h)