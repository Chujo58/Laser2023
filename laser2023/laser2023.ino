#include "Adafruit_MotorShield.h"
#define BAUD_RATE 115200

// #define ADDRESS 0x62

// Here we will define all the of global scope variables.

unsigned int counter = 0;
int mode = 0;
unsigned steps = 1000;
unsigned delays = 20;
unsigned value = 0;

// Here we call the motor shield which will connect us to the stepper motor connected.
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

// Here we connect to the stepper motor and we specify that we are using 200 steps per revolution.
Adafruit_StepperMotor * myMotor = AFMS.getStepper(200, 1);

void setup(){
    // To communicate with Python we will do so via the Serial monitor. So we will first initialize it.
    Serial.begin(BAUD_RATE);
    Serial.println("LASER 2023");

    // Let's start the motor shield with the default frequency of 1.6kHz. The frequency can always be changed at the top of this file.
    AFMS.begin();
}

void loop(){
    
}