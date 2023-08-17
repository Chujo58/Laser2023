#include "Adafruit_MotorShield.h"
#include "CONFIG.h"

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

    // Let's give the motor a default rotation speed of 10 RPM:
    myMotor->setSpeed(DEFAULT_MOTOR_SPEED); //Since myMotor is a pointer we can call the setSpeed function using the ->.
}

void loop(){
    read_input();
    delay(5000);
}

void read_input() {
    long start = millis(); // Let's grab the current time.
    while (! Serial.available()) {//This checks if the Serial line is not available.
        if ((millis() - start) > 2000) {//This checks if the Serial line has not been available for more than 2 seconds.
            Serial.println("Timeout!");
            return;
        }
    }

    char input = Serial.read();
    String input_string = String(input);
    Serial.println("Testing the read");
    Serial.println(input_string);

}