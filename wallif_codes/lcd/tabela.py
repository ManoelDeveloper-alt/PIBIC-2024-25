from rich.console import Console
from rich.table import Table
from rich.layout import Layout
import time

console = Console()

def update_table(data, nome):

    table = Table(title=nome) # Cria uma tabela e  dá um titulo a ela

    table.add_column("REF", justify="center", style="cyan") # Adiciona uma coluna
    table.add_column("DATA", justify="center", style="magenta") # Adiciona coluna

    for row in data:
        table.add_row(*row) # Adiciona uma linha

    return table

data_sensores = [
    ["S0", "0cm"],
    ["S1", "12cm"],
    ["S2", "15cm"]
] # data tabela 1
data_motores = [
    ["MT1", "200rpm"],
    ["MT2", "127rpm"]
] # data tabela 2

i = 0
while True:
    console.clear() # limpa o console

    layout = Layout() # cria um layout
    layout.split_column(Layout(name="top")) # adiciona uma coluna ao layout
    layout["top"].split_row(
        update_table(data_sensores, "sensores"),
        update_table(data_motores, "motores")
    ) # adicion aas duas tabelas em uma unica linha

    console.print(layout) # desenha as tabelas
    time.sleep(0.3) # taxa de atualização (3 vezes por segundo)
    data_sensores[0][1] = str(i)+"cm" # atualiza os valores
    i+=1