# Botão no pino 23
import lgpio
import time

BOTAO = 23 #pino do BOTÃO
h = lgpio.gpiochip_open(0) # Abre o chip dos GPIOS, cria uma referência dele
i = 0
try:
	while True:
		bt_read = lgpio.gpio_read(h, BOTAO)
		print(bt_read, i)
		if not (bt_read == 1):
#			print("Você pressionou o botão")
			pass
		i+=1

except KeyboardInterrupt:
	lgpio.gpiochip_close(h)#fecha o chip do gpio

# acessado via FTP