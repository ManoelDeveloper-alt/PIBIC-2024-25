#  Botão no pino 23
import lgpio
from time import sleep

BOTAO = 23 #pino do BOTÃO

h = lgpio.gpiochip_open(0) # Abre o chip dos GPIOS, cria uma referência para ele
lgpio.gpio_claim_input(h, BOTAO) # Define o pino como entrada

try:
    while True:
        if(lgpio.gpio_read(h, BOTAO)==1):
            print("Você pressionou o botão")

except KeyboardInterrupt:
    lgpio.gpiochip_close(h)#fecha o chip do gpio
