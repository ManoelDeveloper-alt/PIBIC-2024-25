import subprocess
import os

p = subprocess.Popen('chmod a+rw /dev/ttyAMA0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
	print(line.decode(), end='')
retval = p.wait()

#p = subprocess.Popen('pibicjr', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#rtval = p.wait()
os.system("echo Feita!")

while True:
	pass
