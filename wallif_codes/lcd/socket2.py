# Escuta
import socket

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(
    ( "127.0.0.1", 5000) # IP padrão de comunicação interna, porta para comunicação
)

while True:
    data, addr = sock.recvfrom(1024) # espera um dado ser recebido (bloqueante)
    rcv = data.decode() #decodifica a string recebida
    print("Recebido: ", rcv)