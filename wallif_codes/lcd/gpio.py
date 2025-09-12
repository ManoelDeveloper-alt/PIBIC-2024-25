#  Piscando um LED no pino 23
import time
import lgpio

LED = 23 #pino do LED

h = lgpio.gpiochip_open(0) # Abre o chip dos GPIOS, cria uma referência para ele
lgpio.gpio_claim_output(h, LED) # Define o pino como saída

try:
    while True:
        lgpio.gpio_write(h, LED, 1) # Acende o Led
        time.sleep(1)
        lgpio.gpio_write(h, LED, 0) # Apaga o Led
        time.sleep(1)

except KeyboardInterrupt:
    lgpio.gpio_write(h, LED, 0) #apaga o led
    lgpio.gpiochip_close(h)