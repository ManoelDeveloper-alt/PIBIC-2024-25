import I2C_LCD_driver
import subprocess
import time

def processo(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	saida = ""
	for line in p.stdout.readlines():
		print(line.decode(), end='')
		saida += line.decode()
	retval = p.wait()
	return saida

lcdi2c = I2C_LCD_driver.lcd()
last_ip = ""
last_rede = ""
ip = ""
rede = ""
def updata():
	global ip, rede
	ip = processo("hostname -I")
	rede = processo("nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d':' -f2")
	
last_time_updata = 0
updata()

while True:
	atual = time.time()
	if (atual-last_time_updata)>10:
		last_time_updata = atual
		updata()
	if not (last_ip==ip) or not(last_rede==rede):
		last_ip = ip
		last_rede = rede
		lcdi2c.lcd_clear()
		lcdi2c.lcd_display_string(ip, 1, 0)
		lcdi2c.lcd_display_string(rede, 2, 0)
		
	lcdi2c.backlight(0)
	time.sleep(0.2)
	lcdi2c.backlight(1)
	time.sleep(3)