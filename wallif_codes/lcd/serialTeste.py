import serial

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
# porta, taxa de transmissão, tempo maximo de espera para uma resposta (em segundos)

ser.write(b"Hello world") #escreve na serial
# string codificada ou bytearray

while True:
    if ser.in_waiting>0: # ver a quantidade de dados disponiveis para leitura
        lido = ser.read(ser.in_waiting) # ler a quantidade de dados pedido
        print(lido)