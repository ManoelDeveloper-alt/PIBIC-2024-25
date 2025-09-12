import lgpio
import time
import I2C_LCD_driver
import smbus

menu_actived = False
ultima_contagem = 0
time_actived = 0
MAX_TIME = 120

lcdi2c = I2C_LCD_driver.lcd()
lcdi2c.backlight(0)

localizacao = [0]
opcoes = [
{
		"titulo":"Rede", "submenu":True,
		"content":[{
			"titulo":"Status", "submenu":False, "id":0
		},{
			"titulo":"Conectar-se", "submenu":False, "id":1
		}]
},
{		"titulo":"Perifericos","submenu":True,
		"content":[{
			"titulo":"Distancia","submenu":True,
			"content":[{
				"titulo":"S0", "submenu":False,"id":2
			},{
				"titulo":"S1", "submenu":False,"id":3
			}
			]
		},{
			"titulo":"Linha","submenu":True,
			"content":[{
				"titulo":"L0","submenu":False,"id":4
				},{
				"titulo":"L1","submenu":False,"id":5
				},{
				"titulo":"L3","submenu":False,"id":6
			}]
		},{
			"titulo":"Motores","submenu":True,
			"content":[{
				"titulo":"MOTOR 1","submenu":False,"id":7
			},{
				"titulo":"MOTOR 2","submenu":False,"id":8
			}]
		}]
}
]

delay_time = 300 # tempo de atrasso entre os clicks (ms)
BOTAO = [ 17, 27, 22, 23, 24] # pinos dos botões na ordem
h = lgpio.gpiochip_open(0) # Abre o chip dos GPIOS, cria uma referência dele
borda = [] #usado para salvar o estado anterior

for bot in BOTAO:
	lgpio.gpio_claim_input(h, bot) # Define o pino como entrada
	borda.append(0) #assume que o botão está solto

def clear_lcd():
	lcdi2c.lcd_display_string("                ",1,0)
	lcdi2c.lcd_display_string("                ",2,0)

def getlist_and_move(mov):
	atual_list = opcoes
	for i in localizacao[0:len(localizacao)-1]:
		atual_op = atual_list[i]
		atual_list = atual_op["content"]
	line = localizacao[len(localizacao)-1]
	if (mov<0 and line>0) or (mov>0 and line<len(atual_list)-1):
		localizacao[len(localizacao)-1] = line+mov
		line = line+mov
	return [atual_list, line]

def upmenu(mov):
	data = getlist_and_move(mov)
	clear_lcd()
	p = 1
	next = 1
	if data[1]==len(data[0])-1:
		p = 2
		next = -1
	sel1 = data[0][data[1]]["titulo"] # selecionado
	if len(sel1)>14: sel1 = sel1[:11]+"...<"
	else:
		for i in range(14-len(sel1)):
			sel1+=" "
		sel1+="<"
	sel2 = data[0][data[1]+next]["titulo"] # não selecionado
	if len(sel2)>16: sel2 = sel2[:13]+"..."
	if len(data[0])>1:
		lcdi2c.lcd_display_string(">"+sel1, p, 0)
		lcdi2c.lcd_display_string(" "+sel2, p+next, 0)
	else:
		lcdi2c.lcd_display_string(">"+sel1, 1, 0)

def enter():
	data = getlist_and_move(0)
	if data[0][data[1]]["submenu"]==True:
		localizacao.append(0)
		upmenu(0)
	else:
		id = data[0][data[1]]["id"]
		if id==0:
			clear_lcd()
			
def back():
	global localizacao
	if len(localizacao)>1:
		localizacao = localizacao[:len(localizacao)-2]
		localizacao.append(0)
		upmenu(0)
	else:
		desable()
def desable():
	global menu_actived
	menu_actived = False
	clear_lcd()
	lcdi2c.backlight(0)
def menu():
	global borda, localizacao, menu_actived, ultima_contagem, time_actived
	id = 0
	while True:
		bt = lgpio.gpio_read(h, BOTAO[id]) # valor atual do botao
		if not (bt == borda[id]): # se o botão mudou de estado
			if bt == 1: # se o botão foi pressionado
				ultima_contagem = time.time() # matem o menu "ligado"
				if menu_actived: # se o mneu está ativado move o mesmo
					if id==0:
						upmenu(1)
					if id==1:
						upmenu(-1)
					if id==2:
						enter()
					if id==4: back()
				else:
					if id==2:
						menu_actived=True
						localizacao = [0]
						upmenu(0)
				time.sleep(delay_time/1000)
			borda[id] = bt # atualiza o estado do botão

		id+=1 # passa para olhar o próximo
		if id==len(BOTAO): id = 0
		# verifica se passou o tempo parado
		if (time.time()-ultima_contagem)>MAX_TIME and menu_actived:
			desable()
	clear_lcd()
	lcdi2c.backlight(0)

try:
	menu()

except KeyboardInterrupt:
	lgpio.gpiochip_close(h)#fecha o chip do gpio
	clear_lcd()
	lcdi2c.backlight(0)
