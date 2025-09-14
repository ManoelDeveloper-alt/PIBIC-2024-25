class Fila():
    def __init__(self):
        self.elementos = []
    def put(self, item):
        self.elementos.append(item)
    def get(self):
        menores_f_score = []
        menor_h = False
        indice = 0
        for el in self.elementos:
            if len(menores_f_score)>0:
                if menores_f_score[0][0]>el[0]:
                    menores_f_score = [[el[0],indice]]
                elif menores_f_score[0][0]==el[0]:
                    menores_f_score.append([el[0],indice])
            else:
                menores_f_score.append([el[0],indice])
            indice+=1
        if len(menores_f_score)>1:
            for f in menores_f_score:
                if menor_h==False:
                    menor_h = f
                else:
                    if (self.elementos[menor_h[1]][1])>(self.elementos[f[1]][1]):
                        menor_h = f
            menores_f_score = [menor_h]
        saida = self.elementos[menores_f_score[0][1]]
        del self.elementos[menores_f_score[0][1]]
        return saida

    def empty(self):
        return len(self.elementos)==0
