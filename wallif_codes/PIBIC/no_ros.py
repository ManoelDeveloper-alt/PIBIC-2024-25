import simpleSocket

VELOCIDADE = [125,125]

dataEnviada = {
    "S0":22,
    "S1":127,
    "S2":255,
    "S3":13
}

sock = simpleSocket.SimpleSocket(5000, simpleSocket.POINT_B)

i = 0
while True:
    sock.setData("S"+str(i), dataEnviada["S"+str(i)])
    print("enviado ","S"+str(i), " -> ", dataEnviada["S"+str(i)])
    i+=1
    if i ==4:
        i = 0