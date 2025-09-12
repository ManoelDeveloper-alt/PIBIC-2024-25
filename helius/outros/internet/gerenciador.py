import subprocess
import re
import os

# Função para listar as redes Wi-Fi disponíveis
def listar_redes_wifi():
    try:
        # Executa o comando iwlist para escanear redes Wi-Fi
        resultado = subprocess.run(["iwlist", "wlan0", "scan"], capture_output=True, text=True, check=True)
        redes = resultado.stdout
        
        # Usa regex para extrair os SSIDs das redes encontradas
        padrao_ssid = re.compile(r'ESSID:"(.*?)"')
        ssids = padrao_ssid.findall(redes)
        
        # Exibe as redes disponíveis com índice numérico
        print("Redes Wi-Fi disponíveis:")
        for indice, ssid in enumerate(ssids):
            print(f"{indice}: {ssid}")
        
        return ssids
    except subprocess.CalledProcessError as e:
        print("Erro ao listar redes Wi-Fi:", e)
        return []

# Função para conectar a uma rede Wi-Fi especificada pelo usuário usando wpa_cli
def conectar_wifi(ssid):
    senha = input(f"Digite a senha para a rede {ssid}: ")
    try:
        # Criar um arquivo de configuração temporário para wpa_passphrase
        config_path = "/tmp/wifi_config.conf"
        with open(config_path, "w") as f:
            subprocess.run(["wpa_passphrase", ssid, senha], stdout=f, check=True)
        
        # Adicionar a rede ao wpa_supplicant e ativá-la
        subprocess.run(["wpa_cli", "-i", "wlan0", "reconfigure"], check=True)
        subprocess.run(["wpa_cli", "-i", "wlan0", "add_network"], check=True)
        subprocess.run(["wpa_cli", "-i", "wlan0", "set_network", "0", "ssid", f'"{ssid}"'], check=True)
        subprocess.run(["wpa_cli", "-i", "wlan0", "set_network", "0", "psk", f'"{senha}"'], check=True)
        subprocess.run(["wpa_cli", "-i", "wlan0", "enable_network", "0"], check=True)
        
        # Obter endereço IP usando udhcpc
        subprocess.run(["udhcpc", "-i", "wlan0"], check=True)
        
        print(f"Conectado à rede {ssid} com sucesso!")
    except subprocess.CalledProcessError as e:
        print("Erro ao conectar-se à rede Wi-Fi:", e)
    finally:
        # Remover o arquivo de configuração temporário
        os.remove(config_path)

if __name__ == "__main__":
    # Lista as redes disponíveis e permite ao usuário escolher uma
    redes_disponiveis = listar_redes_wifi()
    if redes_disponiveis:
        try:
            indice_escolhido = int(input("Digite o número da rede que deseja conectar: "))
            if 0 <= indice_escolhido < len(redes_disponiveis):
                conectar_wifi(redes_disponiveis[indice_escolhido])
            else:
                print("Índice inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
