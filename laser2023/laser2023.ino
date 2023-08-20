#include "Adafruit_MotorShield.h"
#include "CONFIG.h"
#include "Wire.h"

#define ADDRESS 0x62 //This is used to control the voltage that goes to the laser.
#define CHLOE_TEST
// Here we will define all the of global scope variables.

unsigned int counter = 0; //Counts the number of steps done by the stepper motor.
unsigned steps = 1000; //Numbers of steps we want to do in total.
unsigned delays = 20; //Delay between each step.
unsigned value = 0; //Information sent to the laser directly.
bool running = false; //Whether the loop should take data or not.
bool restart = false; //Whehter we restart the acquisition once done.

#ifndef CHLOE_TEST
// Here we call the motor shield which will connect us to the stepper motor connected.
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

// Here we connect to the stepper motor and we specify that we are using 200 steps per revolution.
Adafruit_StepperMotor * myMotor = AFMS.getStepper(200, 1);
#endif


void setup(){
    // To communicate with Python we will do so via the Serial monitor. So we will first initialize it.
    Serial.begin(BAUD_RATE);
    Serial.println("LASER 2023");
    #ifndef CHLOE_TEST
    // Let's start the motor shield with the default frequency of 1.6kHz. The frequency can always be changed at the top of this file.
    AFMS.begin();

    // Let's give the motor a default rotation speed of 10 RPM:
    myMotor->setSpeed(DEFAULT_MOTOR_SPEED); //Since myMotor is a pointer we can call the setSpeed function using the ->.
    #endif
}

void loop(){
    if (Serial.available()) read_input();
    if (!running) return; //Stops the loop once the data acquisition is over.

    #ifndef CHLOE_TEST
    myMotor->step(1, FORWARD, SINGLE); //Move the motor by one step forward.
    #endif
    delay(delays); //Delays each step of the motor by a set amount of time.

    Serial.println(analogRead(PHOTO_TRANSISTOR_PIN));
    Serial.flush();
    counter++;

    if (steps == counter) counter = 0; //Resets the counter of steps done.
    if (!counter && !restart) running = false; //Sets running to false if we are done with the steps and if we are not restarting the loop.
}

void setDAC(int voltage) {
    char cmd[3];
    voltage <<= 4;
    cmd[0] = 0x40;
    cmd[1] = voltage >> 8;
    cmd[2] = voltage & 0xff;
    Wire.beginTransmission(ADDRESS);
    if (3 != Wire.write(cmd, 3)) {
        Serial.println("FOUL!");
    }
    Wire.endTransmission();
}

void read_input() {
    long start = millis(); // Let's grab the current time.
    while (! Serial.available()) {//This checks if the Serial line is not available.
        if ((millis() - start) > 2000) {//This checks if the Serial line has not been available for more than 2 seconds.
            Serial.println("Timeout!");
            return;
        }
    }

    String input = Serial.readString(); //Reads the Serial monitor.
    //Start the acquisition loop
    if (input.substring(0,5) == "START") {
        if (running) return;
        Serial.println("Starting the acquisition!");
        running = true;
        return;
    }
    //
    if (input.substring(0,4) == "STOP") {
        if (!running) return;
        restart = false;
        return;
    }
    if (input.substring(0,5) == "ABORT") {
        running = false;
        restart = false;
        counter = 0;
        return;
    }

}