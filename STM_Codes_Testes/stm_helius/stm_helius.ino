/* Author: Manoel Messias
 * Date: 03 de Fevereiro de 2025
 * Description: Código para controle total da placa-mãe do robô helius através da serial.
 */

#define TRIG_PIN_SERIAL1 PA11 // pino de controle de comunicação 
#define TIME_LED 500 // tempo para o led mudar de estado(ms)
#define LINES_OUT 3 // quantidade de linhas na matriz de saida
#define LINES_IN 1 // quantidade de linhas na matriz de entrada

// mapeamento de perifericos
#define MOTOR1_A PB1
#define MOTOR1_B PB0 
#define ENCODER1 PB8

#define MOTOR2_A PA7
#define MOTOR2_B PA6
#define ENCODER2 PB9

#define LINHA1 PB3
#define LINHA2 PB12
#define LINHA3 PB13
// constantes
#define RESOLUCAO 180

volatile bool readFlag = false; // indica se existe dados para ler
volatile bool responseFlag = false; // indica se o dispositivo mestre solicita a leitura de uma informação

byte linha = 0; // linha de saida
byte coluna = 0; // coluna de saida

volatile unsigned int count_encoder1 = 0;
volatile unsigned int count_encoder2 = 0;
unsigned long int last_time_count_encoder = 0;

byte dataIn[LINES_IN][8] = { // matriz de entrada
  {0, 0, 0, 0, 0, 0, 0, 0}
};

byte dataOut[LINES_OUT][8] = { // matriz de saida
  {0, 0, 0, 0, 0, 0, 0, 0}, // velo1_msb,  velo1_lsb,  velo2_msb,  velo2_lsb,  line1,      line2,    line3,    acellX_msb
  {0, 0, 0, 0, 0, 0, 0, 0}, // acellX_lsb, acellY_msb, acellY_lsb, acellZ_msb, acellZ_lsb, GirX_msb, GirX_lsb, GirY_msb
  {0, 0, 0, 0, 0, 0, 0, 0}  // GirY_lsb,   GirZ_msb,   GirZ_lsb,   null,       null,       null,     null,     null
};

int led_state = 0; // estado do led

void setup() {
  // comunicação serial
  Serial1.begin(230000); // Habilita a uart1 com baud rate de 0.23Mbps bits por segundo
  pinMode(TRIG_PIN_SERIAL1, INPUT_PULLUP); // pino de disparo como entrada
  attachInterrupt(digitalPinToInterrupt(TRIG_PIN_SERIAL1), handlePulse, CHANGE); // Ativação de interrupção

  // perifericos
  pinMode(MOTOR1_A, OUTPUT); // controle A (IN1) do motor 1 (out1 e out2)
  pinMode(MOTOR1_B, OUTPUT); // controle B (IN2) do motor 1 (out1 e out2)
  pinMode(ENCODER1, INPUT); // Encoder do motor 1
  attachInterrupt(digitalPinToInterrupt(ENCODER1), encoder1, RISING); // Ativação de interrupção
  pinMode(MOTOR2_A, OUTPUT); // controle A (IN3) do motor 2 (out4 e out3)
  pinMode(MOTOR2_B, OUTPUT); // controle B (IN4) do motor 2 (out4 e out3)
  pinMode(ENCODER2, INPUT); // Encoder do motor 2
  attachInterrupt(digitalPinToInterrupt(ENCODER2), encoder2, RISING); // Ativação de interrupção

  pinMode(LINHA1, INPUT);
  pinMode(LINHA2, INPUT);
  pinMode(LINHA3, INPUT);

  // led interno para teste
  pinMode(PC13, OUTPUT); // led para representação
  digitalWrite(PC13, 0); // led apaga
}

//controle do led piscando feito pelo millis()
unsigned long int last_state_time_led = 0; // varivel para salvar o tempo da ultima mudança de estado do led

void loop() {
  unsigned long int atual_time = millis(); // valor atual de tempo
  // parte para testes (pisca led)
  if((atual_time-last_state_time_led) >= TIME_LED){ // se passar o tempo para mundança
    led_state = !led_state; // mude o estado
    last_state_time_led = atual_time; // atualize o tempo da ultima mudança
  }
  // mede a velocidade do encoder
  if((atual_time-last_time_count_encoder)>100){ // a cada 100ms (10 vezes por segundo)
    unsigned long int decorred_time = atual_time-last_time_count_encoder;
    last_time_count_encoder = atual_time;
    // velocidade do motor 1
    float velocity1_base = ((float)count_encoder1/RESOLUCAO)*60*(1000/decorred_time); // voltas por minuto
    int velocity1_x10 = (int)(velocity1_base*10); // para trabalharmos com as duas casas decimais
    uint8_t velocity1_msb = (uint8_t)((velocity1_x10 & 0xFF00) >> 8); // pega apenas o segundo byte e o move tornando-o primeiro
    uint8_t velocity1_lsb = (uint8_t)(velocity1_x10 & 0x00FF); // pega os ultimos bytes
    dataOut[0][0] = velocity1_msb;
    dataOut[0][1] = velocity1_lsb;
    count_encoder1 = 0;
    // velocidade motor 2
    float velocity2_base = ((float)count_encoder2/RESOLUCAO)*60*(1000/decorred_time); // voltas por minuto
    int velocity2_x10 = (int)(velocity2_base*10); // para trabalharmos com as duas casas decimais
    uint8_t velocity2_msb = (uint8_t)((velocity2_x10 & 0xFF00) >> 8); // pega apenas o segundo byte e o move tornando-o primeiro
    uint8_t velocity2_lsb = (uint8_t)(velocity2_x10 & 0x00FF); // pega os ultimos bytes
    dataOut[0][2] = velocity2_msb;
    dataOut[0][3] = velocity2_lsb;
    count_encoder2 = 0;
  }

  if(readFlag){ // ler a data recebida
    byte qt_bits = Serial1.available();//recebe a quantidade de bytes a serem lidos
    byte receveid[qt_bits]; // cria um buffer para armazenar os bytes que serão lidos
    for(byte i = 0; i < qt_bits; i++){ // ler os bytes 
      receveid[i] = Serial1.read(); // ler o byte atual
      delayMicroseconds(100); // espera para que o buffer interno possa preparar o próximo byte para a leitura (9 bytes 10us cada - 90us ~ 0.1ms)
    }
    byte l = receveid[0]; // recebe a linha
    // sempre serão recebidos 8 bytes de dados
    for(byte i = 0; i<8; i++){ // altera os bytes
      dataIn[l][i] = receveid[1+i]; // adiciona no matriz
    }
    readFlag = false; // indidca que o que tinha de ser recebido já foi recebido
  }

  if(responseFlag){ // escreve a resposta solicitada
    //os 5 primeiros bits são a linha, os 3 ultimos a coluna
    byte info[9] = {linha,0,0,0,0,0,0,0,0}; // cria um buffer para juntar as informações a serem enviadas
    for(int i = 0; i<8; i++){ // preenche o buffer de saida
      info[i+1] = dataOut[linha][i];
    }
    Serial1.write(info, 9); // escreve o buffer na serial
    linha = (linha == LINES_OUT-1)?0:linha+1; // atualiza para escrever a próxima linha
    responseFlag = false; // indica que os dados já foram escritos
  }

  analogWrite(MOTOR1_A, dataIn[0][0]); // aplica o sinal pwm no controle A do motor 1
  analogWrite(MOTOR1_B, dataIn[0][1]); // aplica o sinal pwm no controle B do motor 1
  analogWrite(MOTOR2_A, dataIn[0][2]); // aplica o sinal pwm no controle A do motor 2
  analogWrite(MOTOR2_B, dataIn[0][3]); // aplica o sinal pwm no controle B do motor 2

  digitalWrite(PC13, led_state); // aplica o estado da variavel no led

  dataOut[0][4] = digitalRead(LINHA1);
  dataOut[0][6] = digitalRead(LINHA2);
  dataOut[0][7] = digitalRead(LINHA3);
}

// interrupção para contagem da velocidade do motor 1
void encoder1(){ // disparada pela subida
  if(digitalRead(ENCODER1) == HIGH){
    count_encoder1++;
  }
}
// interrupção para contagem da velocidade do motor 2
void encoder2(){ // disparada pela subida
  if(digitalRead(ENCODER2) == HIGH){
    count_encoder2++;
  }
}

void handlePulse(){ // função disparada pelo pino de controle de comunicação do dispositivo mestre
  if(digitalRead(TRIG_PIN_SERIAL1) == LOW){ // decida
    readFlag = true; // leitura
  }else{ // subida
    responseFlag = true; // escrita
  }
}
