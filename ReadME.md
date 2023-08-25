# How to run the code

For this code to properly run, you first need to upload the `laser2023.ino` to an Arduino board connected via USB. Normally, it should be detected automatically, but you can always set the COM port if it isn't detected.

Once the code is successfully uploaded to the Arduino, you can run the Python code in `connect.py`. This code contains input verifications that will verify and transform your inputs into something that can be sent to the Arduino board. 

After choosing a number of steps, a voltage value for the laser and a delay, the code will start taking your data. After the steps are completed, the code will also show you a quick graph of the data you took and save it to a `csv` file saved in the `DAQ` folder.

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
