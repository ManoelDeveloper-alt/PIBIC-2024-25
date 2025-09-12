#include <Arduino.h>
#include <libmaple/timer.h>
// Definir os pinos dos encoders (TIM2 e TIM3)
// para zerar use timer_set_count(TIMERx, 0)

#define ENCODER1_A PA0
#define ENCODER1_B PA1
#define ENCODER2_A PA6
#define ENCODER2_B PA7

void setup() {
    Serial1.begin(115200);

    // Configurar TIM2 para Encoder 1
    pinMode(ENCODER1_A, INPUT_PULLUP);
    pinMode(ENCODER1_B, INPUT_PULLUP);
    timer_pause(TIMER2);
    timer_set_mode(TIMER2, TIMER_CH1, TIMER_ENCODER);
    timer_set_mode(TIMER2, TIMER_CH2, TIMER_ENCODER);
    timer_generate_update(TIMER2);
    timer_resume(TIMER2);

    // Configurar TIM3 para Encoder 2
    pinMode(ENCODER2_A, INPUT_PULLUP);
    pinMode(ENCODER2_B, INPUT_PULLUP);
    timer_pause(TIMER3);
    timer_set_mode(TIMER3, TIMER_CH1, TIMER_ENCODER);
    timer_set_mode(TIMER3, TIMER_CH2, TIMER_ENCODER);
    timer_generate_update(TIMER3);
    timer_resume(TIMER3);
}

void loop() {
    int16_t encoder1 = timer_get_count(TIMER2);  // Lê o contador do TIM2
    int16_t encoder2 = timer_get_count(TIMER3);  // Lê o contador do TIM3

    Serial1.print("Encoder 1: ");
    Serial1.print(encoder1);
    Serial1.print(" | Encoder 2: ");
    Serial1.println(encoder2);

    delay(100);
}

