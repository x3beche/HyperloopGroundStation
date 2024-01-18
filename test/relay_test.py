from time import sleep
import lgpio

RELAY_2 = 19
RELAY_4 = 13
RELAY_3 = 5
RELAY_1 = 6

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, RELAY_1)
lgpio.gpio_claim_output(h, RELAY_2)
lgpio.gpio_claim_output(h, RELAY_3)
lgpio.gpio_claim_output(h, RELAY_4)
lgpio.gpio_write(h, RELAY_1, 1)
lgpio.gpio_write(h, RELAY_2, 1)
lgpio.gpio_write(h, RELAY_3, 1)
lgpio.gpio_write(h, RELAY_4, 1)

try:
    while True:
        lgpio.gpio_write(h, RELAY_1, 0)
        lgpio.gpio_write(h, RELAY_4, 1)
        sleep(1)
        lgpio.gpio_write(h, RELAY_2, 0)
        lgpio.gpio_write(h, RELAY_1, 1)
        sleep(1)
        lgpio.gpio_write(h, RELAY_3, 0)
        lgpio.gpio_write(h, RELAY_2, 1)
        sleep(1)
        lgpio.gpio_write(h, RELAY_4, 0)
        lgpio.gpio_write(h, RELAY_3, 1)
        sleep(1)

except KeyboardInterrupt:
    lgpio.gpio_write(h, RELAY_1, 1)
    lgpio.gpio_write(h, RELAY_2, 1)
    lgpio.gpio_write(h, RELAY_3, 1)
    lgpio.gpio_write(h, RELAY_4, 1)