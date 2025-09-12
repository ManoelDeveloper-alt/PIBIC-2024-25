import socket

UDP_IP = '127.0.0.1'
request = 5001
response = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, request))

class data():
    def __init__(self):
        self.data = ''
    def setData(self, valor):
        self.data = valor

DATA = data()

def received():
    data,addr = sock.recvfrom(1024)
    rcv = data.decode ()
    DATA.setData(rcv)
    return rcv

def responded():
    sock.sendto("OKAY".encode(),(UDP_IP,response))

while True:
    dt = received()
    print("Data recebida: ", dt)
    responded()