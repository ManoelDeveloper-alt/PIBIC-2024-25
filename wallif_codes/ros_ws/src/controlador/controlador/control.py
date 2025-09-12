# 17 - NOV - 2024
# Manoel Messias
# Controlador usando tkinter e ROS 2
#
# -> Recebe os dados dos sensores em uma lista em um json na propriendade 'sensor' e 'linha'
# -> Recebe os dados de posição, velocidade e orientação em um json
#       -- 'velocidade' -> lista de 2 -> x e y
#       -- 'posicao' -> lista de 2 -> x e y
#       -- 'orientacao' -> lista de 2 -> relação a x, relação a y

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import tkinter as tk
from threading import Thread

#tkinter
janela = tk.Tk()
janela.title("Controlador")
janela.resizable(False, False)

#linha
def line(dataQ, table, parent=janela, startcol = 0, ctcol=1):
    r = len(table)
    res = []
    w = ctcol*10+(ctcol-1)
    for i in range(len(dataQ)):
        t1 = tk.Label(parent, text=dataQ[i], borderwidth=0, relief="solid", width=w, background='lightgray')
        t1.grid(column=startcol+(i*ctcol), row=r, columnspan=ctcol, padx=1, pady=1)
        res.append(t1)
    return res

#tabela dos sensores
sensores_frame = tk.Frame(janela, background='lightgray')
sensores_frame.grid(row=0,column=0, padx=20, pady=10, rowspan=5)
sensores_table = []
def add(n, v):
    sensores_table.append(line([n, v], sensores_table, parent=sensores_frame))
add("S0", "---")
add("S1", "---")
add("S2", "---")
add("S3", "---")
add("S4", "---")
add("S5", "---")
add("S6", "---")
add("S7", "---")
add("L0", "---")
add("L1", "---")

#ortogometria data
ortogometria_frame = tk.Frame(janela, background='lightgray')
ortogometria_frame.grid(row=0, column=1, padx=20, pady=5, rowspan=3)
ortogometria_table = []
def add3(v, stcol = 0):
    ortogometria_table.append(line(v, ortogometria_table, parent=ortogometria_frame, startcol=stcol))
add3(["x","y"], 1)
add3(["velo","---","---"])
add3(["pos", "---", "---"])
add3(["ori","---", "---"]) 

#motores
motores_frame = tk.Frame(janela, background='lightgray')
motores_frame.grid(row=3, column=1, padx=20, pady=5, rowspan=2)
motores_table = []
def add2a(vetor):
    motores_table.append(line(vetor, motores_table, motores_frame))
add2a(["mt1","mt2","mt3","mt4"])
add2a(["---","---","---","---"])

#controle
controle_frame = tk.Frame(janela, background='lightgray')
controle_frame.grid(row=0, column=2, rowspan=5, padx=20, pady=5)
controle_tabela = []
def add4(vt, ctcol = 1):
    controle_tabela.append(line(vt,controle_tabela,controle_frame, ctcol=ctcol))
add4(["STOP"], 2 )
add4(["FRENTE","TRAS"])
add4(["DIREITA", "ESQUERDA"])
add4(["ROT. HOR.", "ROT. ANT."])

#funcao para mudar cor da dada tabela
def cor(table, lec, cor, borda=1):
    for c in lec:
        table[c[0]][c[1]].config(background=cor, borderwidth=borda)

cor(controle_tabela, [(0,0)], 'red')


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('control')
        self.SENSORES = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.LINHA = [0,0]
        self.VELOCIDADE = [0.0, 0.0]
        self.POSICAO = [0,0]
        self.ORIENTACAO = [0,0]

        #tabela
        #self.timer = self.create_timer(0.0001, janela.update)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

