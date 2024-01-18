#  Blink an LED with the LGPIO library
#  Uses lgpio library, compatible with kernel 5.11
#  Author: William 'jawn-smith' Wilson

from time import sleep
import lgpio

BUZZER = 23

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, BUZZER)

try:
    while True:
        lgpio.gpio_write(h, BUZZER, 1)
        sleep(0.3)
        lgpio.gpio_write(h, BUZZER, 0)
        sleep(0.3)
except KeyboardInterrupt:
    lgpio.gpio_write(h, BUZZER, 0)
