import simpleSocket

sock = simpleSocket.SimpleSocket(5000, simpleSocket.POINT_A)

i = 0
while True:
    if(not sock.wait()):
        i+=1
        sock.setData("i", i)
    