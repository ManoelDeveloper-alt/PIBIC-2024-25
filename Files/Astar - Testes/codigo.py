import tkinter as tk
import math
from mapa import mapa 
from Fila import Fila
import time

janela = tk.Tk()
janela.title("A esterla")


totais = 0
verificadas = []
for linha in mapa:
    for casa in linha:
        if not casa==1:
            totais+=1

#criação da malha

canvasScale = 15*30/int(len(mapa))
canvas = tk.Canvas(janela, width=len(mapa[0])*canvasScale, height=len(mapa)*canvasScale)
canvas.pack()

def draw(x,y,color='black'):
    canvas.create_rectangle(x*canvasScale,y*canvasScale,(x+1)*canvasScale,(y+1)*canvasScale,fill=color)

class Celula:
    def __init__(self, line : int, col : int, data : int):
        self.line = line
        self.col = col
        self.f_score = float("inf")
        self.g_score = 0
        self.h_score = 0
        self.type = data #0 para disponivel, 1 para colisão
    def setScore(self, g : int, h:int):
        self.f_score = g+h
        self.g_score = g
        self.h_score = h

class Celulas:
    def __init__(self, map : list[list[int]]):
        self.celulas = []
        self.startIndex = [0,0] #2
        self.finishIndex = [0,0] #3
        atual_line = 0
        for line in map:
            self.celulas.append([])
            atual_col = 0
            for data in line:
                celula = Celula(atual_line, atual_col, data)
                if data == 2:
                    self.startIndex = [atual_line, atual_col]
                if data == 3:
                    self.finishIndex = [atual_line, atual_col]
                self.celulas[atual_line].append(celula)
                #desenhar
                cor = 'white'
                if data==1:
                    cor = 'black'
                elif data==2:#start
                    cor = 'blue'
                elif data==3:#finish
                    cor = 'red'
                draw(atual_col,atual_line,cor)
                atual_col += 1
            atual_line+=1
    def getCelula(self,dado:list):
        if dado[0]<len(self.celulas) and dado[0]>-1 and dado[1]<len(self.celulas[0]) and dado[1]>-1:
            return self.celulas[dado[0]][dado[1]]
        else:
            return False
    def getStart(self):
        return self.getCelula(self.startIndex)
    def getFinish(self):
        return self.getCelula(self.finishIndex)


paredes = Celulas(mapa)

start = paredes.getStart()
finish = paredes.getFinish()

def h_score(celula):#distancia até o fim
    D = 1
    D2 = math.sqrt(2)
    dx = abs(celula.col - finish.col)#absolute x
    dy = abs(celula.line - finish.line)#absolute y
    return D * (dx+dy) + (D2 - 2*D) * min(dx,dy)

#calcular valor da celula inicial
start_h_score = h_score(start)
start.setScore(0, start_h_score)

fila = Fila()#fila

def addInFila(casa):
    item = [casa.f_score, casa.h_score, casa]
    fila.put(item)

addInFila(start)

startTime = time.time()
caminho = {}
gray = 0
def aestrela():
    global verificadas, gray
    if not fila.empty():#apenas se a fila de verificação não estiver vazia
        casa = fila.get()[2]
        if casa == finish:#se a casa verificada for a destino, pare
            return getCaminho()
        
        #verifica se existe alguma parede em uma das quatros direções (cima, baixo, esquerda, direita)
        x = casa.col
        y = casa.line
        for i in [[y-1,x],[y+1,x],[y,x-1],[y,x+1],  [y-1,x-1],[y-1,x+1],[y+1,x-1],[y+1,x+1]]:#nessa ordem:cima(y-1),baixo(y+1),esquerda(x-1),direita(x+1)
            #top-left(y-1,x-1),top-right(y-1,x+1),bottom-left(y+1,x-1),bottom-right(y+1,x+1)
            proxima = paredes.getCelula(i)
            if proxima:#existe, isto é, está dentro do labirinto
                if not proxima.type == 1:#não é uma parede
                    novo_g_score = casa.g_score+1
                    novo_f_score =novo_g_score+h_score(proxima)
                    if novo_f_score<proxima.f_score:
                        proxima.setScore(novo_g_score,h_score(proxima))
                        addInFila(proxima)
                        chave = (proxima.line,proxima.col)
                        caminho[chave] = (casa.line,casa.col)
                        if casa!=start and casa!=finish:
                            draw(casa.col,casa.line,'gray')
                            gray+=1
                        if not (casa.col, casa.line) in verificadas:
                            verificadas.append((casa.col, casa.line))
        janela.after(1,aestrela) 
    else:
        print("Caminho impossível ou não encontrado!")
def getCaminho():
    caminhoFinal = {}
    destino = (finish.line,finish.col)
    celula_analisada = destino
    while celula_analisada!=(start.line,start.col):
        caminhoFinal[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]
    
    desenharCaminho(destino,caminhoFinal,len(caminhoFinal))
def desenharCaminho(dest,cam, i):
    index = 0
    for key in cam:
        #draw(key[1],key[0],'green')
        if cam[key] != dest and i==index:
            draw(cam[key][1],cam[key][0],'green')
        index+=1
    if not i==0:
        janela.after(10, lambda:desenharCaminho(dest,cam, i-1))
    else:
        print('%d%% das casas verificadas.' % (len(verificadas)*100/totais))
        print(f'{len(verificadas)} casas verificadas de {totais} casas totais')
        print(f'caminho encontrado em {int(time.time()-startTime)}s')
aestrela()
janela.mainloop()