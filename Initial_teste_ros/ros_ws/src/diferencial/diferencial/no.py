# 
#sensores 11, 12, 13, 17 - linha 16

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import json
import serial
import time
from threading import Thread

#mtd,mte
mt = [0,0]
decodificar = ""
necessario = 0
sensores = [0,0,0,0]
linha = 0
velocidade = [0,0]


class Diferencial(Node):

    def __init__(self):
        super().__init__('no')
        self.connect()
        #motor sub -escultar
        self.subscription = self.create_subscription(
            String,
            'motor',
            self.motor,
            10)
        timer_period = 0.05  # seconds
        #sensor pub - mandar a cada 5ms
        self.publisher_sensor = self.create_publisher(String, 'sensor', 10)

        self.publisher_velocidade = self.create_publisher(String, 'velocidade', 10)

        self.timer = self.create_timer(timer_period, self.send_data)
        
        self.subscription  # prevent unused variable warning
        t1 = Thread(target=self.comunicacao)
        t1.start()

    def send_data(self):
         global necessario, sensores, linha, velocidade
         #decodificar o dado recebido
         if necessario==1:
            dts = ["","","","","","",""]
            dados = decodificar
            i = 0
            while not dados.find(",")==-1:
                dts[i] = dados[0:dados.find(",")]
                dados = dados[dados.find(",")+1:]
                i+=1
            dts[i] = dados
            sensores = dts[0:4]
            linha = dts[4]
            velocidade = dts[5:7]
            necessario = 0
         self.sensor()
         self.velocidade()

    def connect(self):
        while True:
            try:
                self.ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.01)
                break
            except:
                pass
        time.sleep(0.01)
        self.enviar("manoel")
        print("conectado!")

    def motor(self, msg):
        global mt
        dt = msg.data
        obj = json.loads(dt)
        mt2 = obj['motor']
        fe = int(mt2['FE'])
        fd = int(mt2['FD'])
        mt[0] = fd
        mt[1] = fe

    def sensor(self):
            msg = String()
            msg.data = '{"sensores":['+str(sensores[0])+','+str(sensores[1])+','+str(sensores[2])+','+str(sensores[3])+'],"linha":'+str(linha)+'}'
            #print(msg.data)
            self.publisher_sensor.publish(msg)

    def velocidade(self):
            msg = String()
            msg.data = '{"mtd":'+str(velocidade[0])+',"mte":'+str(velocidade[1])+'}'
            #print(msg.data)
            self.publisher_velocidade.publish(msg)

    #ARDUINO ==============================
    def comunicacao(self):
        global decodificar, necessario
        while True:
            dt = (str(mt[0])+","+str(mt[1]))
            print("enviado:("+dt+")")
            p = self.enviar(dt)
            decodificar = p
            necessario = 1
            print("recebido:"+str(p))
            time.sleep(0.001)

    def enviar(self,data):
         t = time.time()
         self.ser.write(data.encode('utf-8'))
         lido = ""
         while True:
              lido = self.ser.readline()
              if not lido==b'':
                   break
         self.ser.flush()
         print(time.time()-t, "s")
         return lido.decode().strip()



def main(args=None):
    rclpy.init(args=args)

    robo = Diferencial()

    rclpy.spin(robo)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    robo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
