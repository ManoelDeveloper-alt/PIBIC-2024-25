from util import comand
import re

WIFI_TYPE = "wlan0"
ETHERNET_TYPE = "eth0"
NON_WIFI = 2

def is_conected(): # indica se há conexão com a internet
	if comand("ip route | grep default") == "":
		return False
	else:
		return True

def net_type(): # verifica o tipo de conexão "wifi" ou "ethernet"
	if not(comand("iwgetid") == ""):
		return WIFI_TYPE
	else:
		return ETHERNET_TYPE

def get_ssid(): # retorna o nome da rede wifi da qual esta conectado
	if net_type()==WIFI_TYPE:
		return (comand("iwgetid -r")).strip()
	else:
		return NON_WIFI

def getIP(n_type): # dado o tipo de rede retorna o ip da mesma
	return  (comand("ip -4 addr show "+n_type+" | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'")).strip()

def listRedes(): # lista as redes wi-fi disponiveis em um vetor
	if net_type()==WIFI_TYPE:
		redes =  comand("iwlist wlan0 scan")

		# Usa regex para extrair os SSIDs das redes encontradas
		padrao_ssid = re.compile(r'ESSID:"(.*?)"')
		ssids = padrao_ssid.findall(redes)

        # retorna redes disponíveis
		return ssids
	else:
		return []
