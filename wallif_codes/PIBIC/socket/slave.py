import socket

UDP_IP = '127.0.0.1'
response = 5000
request = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, response))

class data():
    def __init__(self):
        self.data = 'Manoel'
    def setData(self, valor):
        self.data = valor

DATA = data()

def send():
    sock.sendto(DATA.data.encode(),(UDP_IP,request))

def res():
    data,addr = sock.recvfrom(1024)
    return data.decode ()

while True:
    entrada = input("->")
    DATA.setData(str(entrada))
    send()
    print(res())