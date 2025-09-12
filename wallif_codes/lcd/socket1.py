# Fala
import socket
import time

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
i = 0

while True:
    sock.sendto(str(i).encode(), ( "127.0.0.1", 5000))
    # string codificada a ser enviada, 
    # tupla com o ip padrão de comunicação interna e a porta na qual ela vai ocorrer
    print("Enviado: ", i)
    time.sleep(1)
    i += 1