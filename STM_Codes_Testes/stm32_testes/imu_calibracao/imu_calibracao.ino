//Programa : Teste MPU6050 e LCD 20x4
//Alteracoes e adaptacoes : MakerHero
//
//Baseado no programa original de JohnChi

//Carrega a biblioteca Wire
#include <Wire.h>

//Endereco I2C do MPU6050
const int MPU = 0x68;
//Variaveis para armazenar valores dos sensores
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
float baseAcX = 0;
void setup() {
  Serial3.begin(460800);
  delay(2000);
  Serial3.println("iniciando...");
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);

  //Inicializa o MPU-6050
  Wire.write(0);
  Wire.endTransmission(true);
  Serial3.println("iniciado!");
  Wire.beginTransmission(MPU);

  Wire.write(0x1C); // sensibilidade
  //Altera sensibilidade do acelerometro +/- 8g (baixa sensibilidade) - 16g 0x18, 8g 0x10, 2g padrao
  Wire.write(0x18);
  Wire.endTransmission(true);
  Serial3.println("sensibilidade 16g");
  Serial3.println("calibrando");
  int soma = 0;
  for(int i = 0; i<100; i++){
    updateData();
    soma += AcX;
    delay(50);
  }
  baseAcX = soma/100.0;
  Serial3.println(baseAcX*9.81/2048.0);
  delay(3000);
}
unsigned long int last = 0;

float velo = 0;

void loop() {
  updateData();
 float acel_x = (AcX-baseAcX) * 981;
  Serial3.print("AcX = ");
  Serial3.print(acel_x / (2048.0));
  Serial3.print(" / ");
  Serial3.print(AcX);
  Serial3.print(" / ");
  Serial3.println(baseAcX);

  delay(200);
}

void updateData(){
   Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  //Solicita os dados do sensor
  Wire.requestFrom(MPU, 14, true);
  //Armazena o valor dos sensores nas variaveis correspondentes
  AcX = Wire.read() << 8 | Wire.read();  //0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY = Wire.read() << 8 | Wire.read();  //0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read() << 8 | Wire.read();  //0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp = Wire.read() << 8 | Wire.read();  //0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX = Wire.read() << 8 | Wire.read();  //0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY = Wire.read() << 8 | Wire.read();  //0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ = Wire.read() << 8 | Wire.read();  //0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}