import simpleSocket

sock = simpleSocket.SimpleSocket(5000, simpleSocket.POINT_B)

while True:
    print(sock.data)