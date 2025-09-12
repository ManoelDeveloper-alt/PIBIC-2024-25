import I2C_LCD_driver
import subprocess
import smbus
import time

###################################  LCD COMANDS   ######################################

lcdi2c = 0 # cria a variavel que salva o lcd

def loadLCD():
	global lcdi2c
	while True: #fica preso no loop até achar o lcd
		try: #tentar carregar o lcd
			lcdi2c = I2C_LCD_driver.lcd() #carrega o objeto lcd
			break #se carregar, pula do loop
		except: #caso não consiga
			print("LCD não encontrado!")
			time.sleep(1) #espera 1 segundo
			pass #tenta de novo

def printlcd(str, l, c):
	try: #tenta escrever no display
		lcdi2c.lcd_display_string(str, l, c) #escreve no display
	except: #se não conseguir
		loadLCD() #tenta recarregar o lcd

def clear_lcd(l): #limpa o display
	printlcd("                ", l, 0)

def backlight(b): #apaga a luz de fundo do display
	try: #tenta apagar a luz de fundo
		lcdi2c.backlight(b)
	except: #se não conseguir
		loadLCD() #tenta recarregar o LCD

##################################   SHELL COMANDS ############################################

def send(cmd): #manda um comando para ser execultado pelo sistema
	resposta = subprocess.run(
		cmd, #comando
		shell = True, #comando é string
		text=True, #retorno em texto
		capture_output=True #capta a saida
	)
	return resposta.stdout #retorna a saida do comando no formato de texto

#################################  COMANDOS DE REDE   ###########################################

def verify_rede(): #verifica se o dispositivo esta conectado a internet
	if send("ip route | grep default") == "":
		return 0 #não conectado
	else:
		return 1 #conectado

def is_wifi(): #verifica se o tipo de conexão é wi-fi
	if send("iwgetid") == "": #ethernet
		return 0 #não é wi-fi
	else:
		return 1 #é wi-fi
def ssid():
	return send("iwgetid -r")

def getIp(hardware): #retiorna o ip do dispositivo (em wifi ou ethernet)
	return send("ip -4 addr show "+hardware+" | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'")

##########################   CODIGO PRINCIPAL   ####################################################

try:
	t = time.time() #marca o tempo para contagem paralela
	last_verify_rede = t-5 # marca o tempo da ultima verificação de rede (t-5 para roda logo no inicio)
	last_time_piscada = t
	state_piscada = 0
	state_rede = [ 2, 2, "nao verificado", "no ip"] #[ não verificado(conexão), não verificado(tipo de conexão), não verificado (ssid),não verificado(ip)]
	last_state_rede = [ 2, 2, "nao verificado", "no ip"] #antes das verificação

	while True:
		t = time.time()
		if (t-last_verify_rede)>=5: #verifica se há internet a cada 5 segundos
			last_verify_rede = t
			state_rede[0] = verify_rede() # atualiza o status de conexão
			if not (state_rede[0]==last_state_rede[0]): # houve alteração na conectividade
				last_state_rede[0] = state_rede[0] # atualiza a ultima verificação de conectividade
				if state_rede[0]==0: # sem conexão
					clear_lcd(1) #limpa a primeira linha
					printlcd("Não conectado", 1, 1)
				else: # com conexão
					state_rede[1] = is_wifi() # verifica se a conexão é wifi
					if not (state_rede[1]==last_state_rede[1]): #houve mudança no tipo de conexão (prioriza wifi)
						last_state_rede[1] = state_rede[1] #atualiza o status d o tipo de conexão
						hardware = "wlan0" #hardware do wifi
						if state_rede==0: #ethernet
							hardware = "eth0" #hardware da ethernet
							clear_lcd(1) #limpa a linha 1
							printlcd("Cabo", 1, 5)
						else: #wifi
							state_rede[2] = ssid()
							if not (state_rede[2]==last_state_rede[2]): #houve mudança no wifi no qual estava conectado
								last_state_rede[2] = state_rede[2] #atualiz ao ssid
								clear_lcd(1) #limpa a linha 1
								printlcd(state_rede[2], 1, 0) #escreve o ssid
						state_rede[3] = getIp(hardware) # capta o ip idepententemente do tipo de conexão
						if not (state_rede[3] == last_state_rede[3]): #houve mudança no ip
							last_state_rede[3] = state_rede[3] # atualiza o ip
							clear_lcd(2) # limpa a linha 2
							printlcd(state_rede[3], 2, 2) # escreve o ip
		#pisca o display
		dif = t-last_time_piscada
		if (dif>=1 and state_piscada==0) or (dif>=5 and state_piscada==1):
			state_piscada = not state_piscada
			last_time_piscada = t
			backlight(state_piscada)

except KeyboardInterrupt:
	clear_lcd(1)
	clear_lcd(2)
	backlight(0)
