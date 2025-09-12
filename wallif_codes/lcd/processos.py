import subprocess

resposta = subprocess.run(
     "ls ./",
     shell=True,
     text=True,
     capture_output=True)
print(resposta.stdout)