# Who to contact in case the code doesn't work?
Here are the two people who contributed to this code: Chloé Legué and Kevin Nguyen. If you need to contact them because of coding issues here are their emails:
* Chloé : chloe.legue@mail.mcgill.ca
* Kevin : xyan.g.nguyen@mail.mcgill.ca

# How to run the code

For this code to properly run, you first need to upload the `laser2023.ino` to an Arduino board connected via USB. Normally, it should be detected automatically, but you can always set the COM port if it isn't detected.

Once the code is successfully uploaded to the Arduino, you can run the Python code in `connect.py`. This code contains input verifications that will verify and transform your inputs into something that can be sent to the Arduino board. 

After choosing a number of steps, a voltage value for the laser and a delay, the code will start taking your data. After the steps are completed, the code will also show you a quick graph of the data you took and save it to a `csv` file saved in the `DAQ` folder.

## Change configurations

If you really need to change some settings in the configuration, such as the default speed of the motor and your COM port, you can modify the `CONFIG.h` file. Here are the different settings that can be changed and the variable attached to them:
* Baud rate - BAUD_RATE : The default baud rate used by both Arduino and Python to connect to the Serial monitor.
* Default motor speed - DEFAULT_MOTOR_SPEED : The default speed at which the motor rotates. This is given in rpm.
* COM port - COM : The COM port to which the Arduino is connected. If not set properly, you can still select a value when running the Python code.
* Phototransistor pin - PHOTO_TRANSISTOR_PIN : The phototransistor should be connected to one of the Analog pins, you can select it in here.
* Motor mode : MOTOR_MODE : The stepping mode of the motor. Can be `SINGLE`, `DOUBLE`, `MICROSTEP`. `MICROSTEP` might be smoother for some applications.
* Motor direction : MOTOR_DIRECTION : The direction in which the motor spins.

# Adafruit_Motorshield.cpp library patch
The official release of Adafruit's MotorShield library has a mistake in the `step` function. At low speeds, the `step` function will go much faster than the speed you select.
> Ex: A speed of 1rpm with the official library goes faster than 10rpm. 
Usually, with speeds lower than 10rpm, the observed speed does not match. 

## Locating the Adafruit library folder
In order to fix this problem and be able to use low speed, you will need to locate where your Arduino libraries are installed. For most Windows machines, it should be in the `Documents\Arduino\libraries`. If you have already installed the Adafruit MotorShield library, you should see a folder called `Adafruit_Motor_Shield_V2_library`. 

## Code to change
In the `Adafruit_MotorShield.cpp`, the lines `345` to `348` need to be modified. For reference, here is the original code from the official library:

```
while (steps--) {
    // Serial.println("step!"); Serial.println(uspers);
    onestep(dir, style);
    delayMicroseconds(uspers);
#ifdef ESP8266
    yield(); // required for ESP8266
#endif
  }
```

Here is the updated code, for the speed to work normally:
```
while (steps--) {
    // Serial.println("step!"); Serial.println(uspers);
    onestep(dir, style);
    if (uspers <= 16383){
      delayMicroseconds(uspers);
    }
    else{
      delay(int(uspers/1000));
    }
#ifdef ESP8266
    yield(); // required for ESP8266
#endif
  }
```


# Errors that you can run into

The first error that you might encounter is that Python cannot find the `CONFIG.h` file. This just means you are running the code from outside the `laser2023` folder. You normally want to be outside of this folder to upload the `laser2023.ino` to the Arduino. You will want to run the `connect.py` file inside of `laser2023`. When setting up the experiment, do not put the mount flush to the motor. The friction may stop the motor from spinning. 
