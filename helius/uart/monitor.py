import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
# porta, taxa de transmissão, tempo maximo de espera para uma resposta (em segundos)ser.write(b"Hello world") #escreve na serial
# string codificada ou bytearray
while True:
	if ser.in_waiting>0: # ver a quantidade de dados disponiveis para leitura
		time.sleep(0.1) # espera para receber todos os dados
		lido = ser.readline() # ler uma linha
		print(lido.decode())
