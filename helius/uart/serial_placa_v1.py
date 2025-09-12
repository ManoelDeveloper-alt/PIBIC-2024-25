import lgpio
import serial
import time

DAT_PIN = 4 # pino de controle de comunicação
RESET_PIN = 18 # pino que reseta o stm32

h = lgpio.gpiochip_open(0) # Abre o chip dos GPIOS, cria uma referência para ele
lgpio.gpio_claim_output(h, DAT_PIN) # Define o pino como saída
lgpio.gpio_claim_output(h, RESET_PIN) # Define o pino como saída

lgpio.gpio_write(h, RESET_PIN, 0) # aqui ele bloqueia o stm32
lgpio.gpio_write(h, DAT_PIN, 1) # dá a ele o valor 1
time.sleep(0.1) # espera um tempinho para garantir que o raspberry terá reiniciado
lgpio.gpio_write(h, RESET_PIN, 1) # aqui ele desbloqueia o stm32

stm32 = serial.Serial('/dev/ttyAMA0', 230000, timeout=0.1) # cria a counicação com o stm32

pwm = 0x00
pwm2 = 0x00
contagem = 0x01
ant = 0
last = 0
dt = [
    0x00,
    0x00,
    0x00,
    0x00
]

try:
    while True:
        send = [0x00, pwm,0x00, pwm2, 0x00, contagem, 0x00, 0x00, 0x00] # este é o dado (line d0-d7)
        stm32.write(send) # envia o dado
        time.sleep(0.001) # espera para garantir que os dados foram escritos
        lgpio.gpio_write(h, DAT_PIN, 0) # diz que enviou um dado
        time.sleep(0.001) # espera ele ler (50us para cada byte + espera do loop 0.1ms = 0.5ms)
        lgpio.gpio_write(h, DAT_PIN, 1) # diz que quer ler um dado
        #espera a resposta
        while stm32.in_waiting<8: 
            pass # espera existir uma resposta (pelo menos 9 bytes - line d0-d7)
        line = int.from_bytes(stm32.read(), "big") # a linha
        data = stm32.read(8) # os dados
        dt[line] = list(data)
        if line == 0x02:
            print((time.time() - last)*1000, "ms")
            for i in range(3):
                print(dt[i])
                pass
            print("========================")
            last = time.time()
        if (time.time()-ant)>5:
             #ant = time.time()
             #pwm = pwm+1
             #if pwm > 0xFF: pwm = 0
             #contagem = 0x00
             pass

except KeyboardInterrupt:
    lgpio.gpio_write(h, RESET_PIN, 0) # aqui ele bloqueia o stm32
    lgpio.gpio_write(h, DAT_PIN, 1) # para finalizar com o valor 1
    pass
