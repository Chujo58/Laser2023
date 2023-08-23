# How to run the code

For this code to properly run, you first need to upload the `laser2023.ino` to an Arduino board connected via USB. Normally, it should be detected automatically, but you can always set the COM port if it isn't detected.

Once the code is successfully uploaded to the Arduino, you can run the Python code in `connect.py`. This code contains input verifications that will verify and transform your inputs into something that can be sent to the Arduino board. 

After choosing a number of steps, a voltage value for the laser and a delay, the code will start taking your data. After the steps are completed, the code will also show you a quick graph of the data you took and save it to a `csv` file saved in the `DAQ` folder.

# Errors that you can run into

The first error that you might encounter is that Python cannot find the `CONFIG.h` file. This just means you are running the code from outside the `laser2023` folder. You normally want to be outside of this folder to upload the `laser2023.ino` to the Arduino. You will want to run the `connect.py` file inside of `laser2023`.
