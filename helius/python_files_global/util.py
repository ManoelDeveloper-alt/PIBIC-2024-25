import subprocess

def comand(cmd): # execulta um comando de tertminal
	resp = subprocess.run(
		cmd, # comando
		shell=True, # comando como string inteira
		text=True, # retorno em texto
		capture_output=True # pegar a saida
	)
	return resp.stdout # retorna a saida
