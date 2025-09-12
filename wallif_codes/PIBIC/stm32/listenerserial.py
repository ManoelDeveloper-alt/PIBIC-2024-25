import serial
import time
while True:
	try:
		stm32 = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
		break
	except:
		print("Erro! - Tentando novamente em 1s")
		time.sleep(1)
		pass
try:
	while True:
		time.sleep(0.5)
		print(stm32.read())
except KeyboardInterrupt:
	stm32.close()