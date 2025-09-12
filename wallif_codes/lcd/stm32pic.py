import serial
import time

ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0)

line = 0
def send_line(data):
    global line
    ser.write(data)
    print(f"Enviado: {data}")

    while ser.in_waiting==0:
        print(".", end="")
    print("")
    print("Proxima linha - ", line)
    line+=1

def hexTobin(hex):
    data = [
        "0","1","2","3",
        "4","5","6","7",
        "8","9","A","B",
        "C","D","E","F"
    ]
    a = data.index(hex[0])*16
    b = data.index(hex[1])

    return a+b


with open('arquivo.hex') as file:
    while True:
        fl = file.readline().strip()
        qt = len(fl)
        if fl=="":
            break
        data = [0]
        for i in range(1, int((qt-1)/2)+1):
            hex = fl[(i*2)-1:(i*2)+1]
            data.append(hexTobin(hex))
        send_line(data)

ser.close()