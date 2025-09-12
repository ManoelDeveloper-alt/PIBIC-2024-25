import lgpio
import time

delay_time = 300 # tempo de atrasso entre os clicks (ms)
BOTAO = [ 17, 27, 22, 23, 24] # pinos dos botões na ordem
h = lgpio.gpiochip_open(0) # Abre o chip dos GPIOS, cria uma referência dele
borda = [] #usado para salvar o estado anterior
id = 0 # variavel para mapeamento
for bot in BOTAO:
	lgpio.gpio_claim_input(h, bot) # Define o pino como entrada
	borda.append(0) #assume que o botão está solto

try:
	while True:
		bt = lgpio.gpio_read(h, BOTAO[id]) # valor atual do botao
		if not (bt == borda[id]): # se o botão mudou de estado
			if bt == 1: # se o botão foi pressionado
				print("Você pressionou o botão:", end="")
				if id==0: print("up")
				if id==1: print("down")
				if id==2: print("enter")
				if id==3: print("back")
				if id==4: print("power")
				time.sleep(delay_time/1000)
			borda[id] = bt # atualiza o estado do botão

		id+=1 # passa para olhar o próximo
		if id==len(BOTAO): id = 0

except KeyboardInterrupt:
	lgpio.gpiochip_close(h)#fecha o chip do gpio

