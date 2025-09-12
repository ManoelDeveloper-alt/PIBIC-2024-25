from RPLCD.i2c import CharLCD
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

lcd = CharLCD(
    i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2,dotsize=8
)

while True:
	ip = processo("hostname -I")
	rede = processo("nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d':' -f2")
	lcd.clear()

	lcd.write_string(ip)

	lcd.cursor_pos = (1,0)
	lcd.write_string(rede)
	for i in range(5):
		lcd.backlight_enabled = False
		time.sleep(1)
		lcd.backlight_enabled = True
		time.sleep(1)