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
void setup() {
  Serial.begin(9600);
  Serial.print("inicando");
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);

  //Inicializa o MPU-6050
  Wire.write(0);
  Wire.endTransmission(true);
  Serial.print("iniciado...");
  Wire.beginTransmission(MPU);

  Wire.write(0x1C); // sensibilidade
  //Altera sensibilidade do acelerometro +/- 8g (baixa sensibilidade) - 16g 0x18, 8g 0x10, 2g padrao
  Wire.write(0x18);
  Wire.endTransmission(true);
  Serial.print("sensibilidade");
}
unsigned long int last = 0;
float velo = 0;
void loop() {
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

 float acel_x = AcX * 9.81;
  Serial.print("AcX = ");
  Serial.print(acel_x / (2048.0));
  Serial.print(" / ");
  Serial.println(AcX);
 /* float acel_y = (AcY * 981) / (2048.0 * 2);
  Serial3.print(" | AcY = ");
  Serial3.print(acel_y);
  float acel_z = (AcZ * 981) / (2048.0 * 2);
  Serial3.print(" | AcZ = ");
  Serial3.print(acel_z);


  Serial3.print(" | Tmp = ");
  Serial3.print(Tmp / 340.00 + 36.53);

  Serial3.print(" | GyX = ");
  Serial3.println(GyX);

  Serial3.print(" | GyY = ");
  Serial3.print(GyY);

  Serial3.print(" | GyZ = ");
  Serial3.println(GyZ);*/

  delay(200);
}