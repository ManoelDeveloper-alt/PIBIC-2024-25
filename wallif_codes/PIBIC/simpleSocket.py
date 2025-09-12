import socket
from threading import Thread
import json

POINT_A = 'A'
POINT_B = 'B'

class SimpleSocket():
    def __init__(self, port, ponto=POINT_A):
        self.UDP_IP = '127.0.0.1'# IP, padrão para comunicação interna
        self.portA = port #A fala B escuta
        self.portB = port+1 #B fala A escuta
        self.fala = port #salvara para onde vai falar

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#inicia o socket

        if(ponto==POINT_A):self.pointA()#define um padrão inicial
        else:self.pointB()#define um padrão inicial

        self.data = {
            #data a ser repassada e recebida
            #o codigo garante que esse diretório será o mesmo para os dois pontos de comunicação
            'wait':0#valor que indica se estamos esperando o codigo chegar lá ou não
        }

        #ciar a atualização constante da data
        self.t1 = Thread(target=self.listener)
        self.t1.start()
    
    def pointA(self):#define como esse sendo o ponto A
        self.sock.bind((self.UDP_IP, self.portB)) #escuta de B
        self.fala = self.portA #fala como A

    def pointB(self):
        self.sock.bind((self.UDP_IP, self.portA)) #escuta de A
        self.fala = self.portB#fala como B
    
    def setData(self, key, value):
        self.data['wait'] = 1 #indica que estamos esperando uma indicação de que o valor foi recebido
        self.data[key] = value

        #passa o valor para o outro ponto de comunicação
        #chamada após uma alteração de dados
        dado = value
        if(type(value)==str):dado = '"'+str(value)+'"'#trata o dado (pode ser string ou int)
        dataSend = '{"_keys_repassed":"'+key+'","'+key+'":'+str(dado)+'}'#monta um json com o dado a ser repassado + chave que foi passada

        self.sock.sendto(dataSend.encode(),(self.UDP_IP,self.fala))#envia pela porta prredefinida

    def listener(self):
        while True: #escuta eternamente
            data,addr = self.sock.recvfrom(1024)#recebe o dado
            rcv = data.decode ()#decodidifica
            obj = json.loads(rcv)#transforma em json
            key_received = obj['_keys_repassed']#ver qual foi a data recebida
            self.data[key_received] = obj[key_received]#atualiza a data
            self.setData("wait", 0)#indica que o valor foi recebido

    def wait(self):
        return self.data['wait']