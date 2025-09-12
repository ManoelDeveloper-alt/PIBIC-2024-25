# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import json
import time

from std_msgs.msg import String
import serial

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('no')
        self.dataM = [ 0, 0, 0, 0]
        self.subscription = self.create_subscription(
            String,
            'motor',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        try:
            self.ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
            print("Conectado with ttyAMA0!")
        except:
            print("Erro ao conectar!")

        key = "manoel"
        self.ser.write(key.encode('utf-8'))
        self.lido = self.ser.readline().rstrip()
        print(self.lido.decode())

    def timer_callback(self):
        print(self.dataM)
        print(self.send(self.dataM[0], self.dataM[1], self.dataM[2], self.dataM[3]))

    def listener_callback(self, msg):
        dt = msg.data
        data = json.loads(dt)
        obj = data['motor']
        td = int(obj['TD'])
        te = int(obj['TE'])
        fd = int(obj['FD'])
        fe = int(obj['FE'])

        self.dataM = [td, te, fd, fe]
    
    def send(self, td,te,fd,fe):
        m1 = 0
        if td<0:
            m1=1
            td = td*(-1)
        m2 = 0
        if te<0:
            m2=1
            te = te*(-1)
        m3 = 0
        if fd<0:
            m3=1
            fd = fd*(-1)
        m4 = 0
        if fe<0:
            m4=1
            fe = fe*(-1)
        
        print([ m1, td, m2, te, m3, fd, m4, fe])
        self.ser.write([ m1, td, m2, te, m3, fd, m4, fe])
        lido = b''
        while lido==b'0':
            lido = self.ser.readline()
        self.ser.flush()
        return lido.decode()


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
