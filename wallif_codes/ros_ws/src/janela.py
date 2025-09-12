import tkinter as tk

janela = tk.Tk()
janela.title("Controlador")
janela.resizable(False, False)


#linha
def line(dataQ, table, parent=janela, startcol = 0, ctcol=1, pd=[1,1], fundo = ['lightgray'], border=1):
    r = len(table)
    res = []
    w = ctcol*10+(ctcol-1)
    for i in range(len(dataQ)):
        f = fundo[len(fundo)-1]
        if len(fundo)>i:
            f = fundo[i]
        t1 = tk.Label(parent, text=dataQ[i], borderwidth=border, relief="solid", width=w, background=f)
        t1.grid(column=startcol+(i*ctcol), row=r, columnspan=ctcol, padx=pd[0], pady=pd[1])
        res.append(t1)
    return res


frame1 = tk.Frame(janela, background='lightgray')
frame1.grid(row=0,column=0, padx=20, pady=2, rowspan=5)
table1 = []
def add(n, v, color=['lightgray'], border=1):
    table1.append(line([n, v], table1, parent=frame1, fundo=color, border=border))
add("S0", "10.03cm", ["lightblue", "white"])
add("S1", "2.35cm", ["lightblue", "white"])
add("S2", "0.00cm", ["lightblue", "white"])
add("S3", "24.87cm", ["lightblue", "white"])
add("S4", "10.03cm", border=0)
add("S5", "2.35cm", border=0)
add("S6", "0.00cm", border=0)
add("S7", "24.87cm", border=0)
add("L0", "0", ["lightgreen", "white"])
add("L1", "1", border=0)


frame2a = tk.Frame(janela, background='lightgray')
frame2a.grid(row=3, column=1, padx=20, pady=5, rowspan=2)
table2a = []
def add2a(vetor, color=['lightgray']):
    table2a.append(line(vetor, table2a, frame2a, fundo=color))
add2a(["mt1","mt2","mt3","mt4"], color=['orange', 'orange', 'lightgray'])
add2a(["200rpm","127rpm","0rpm","0rpm"], color=['white', 'white', 'lightgray'])

frame3 = tk.Frame(janela, background='lightgray')
frame3.grid(row=0, column=1, padx=20, pady=5, rowspan=3)
table3 = []
def add3(v, stcol = 0, border =1):
    table3.append(line(v, table3, parent=frame3, startcol=stcol, border=border))

add3(["x","y"], 1, border=0)
add3(["velo","1.23m/s","2.09m/s"], border=0)
add3(["pos", "3.72cm", "4.75cm"], border=0)
add3(["ori","27.21°", "32.07°"], border=0) 

frame4 = tk.Frame(janela, background='lightgray')
frame4.grid(row=0, column=2, rowspan=5, padx=20, pady=5)
table4 = []
def add4(vt, ctcol = 1, pd = [0,0], color = ['white']):
    table4.append(line(vt,table4,frame4, ctcol=ctcol, pd=pd, fundo=color))
add4(["STOP"], 2 , color=['red'])
add4(["FRENTE","TRAS"], pd=[1,1])
add4(["DIREITA", "ESQUERDA"], pd=[1,1])
add4(["ROT. HOR.", "ROT. ANT."], pd=[1,1])

janela.mainloop()