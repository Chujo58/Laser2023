#----------------------------------------------------------------------------
# Created by : Chloé Legué and Kevin Nguyen
# Current version date : 2023/08/23
#----------------------------------------------------------------------------
"""
This code was made for the optical experiment with a solid-state laser at McGill University for the PHYS 339 course.

This is the Python code that runs the commands send to the Arduino. All input verifications are done in here to simplify the Arduino/C++ code.
"""
import arduino_connect as arduino
from ValidInputs import ValidInputs as vi
import pandas as pd
import numpy as np
from datetime import datetime
import os, time
import matplotlib.pyplot as plt

monitor = arduino.ArduinoControl(debug=True)

print("Enter the number of steps you want the motor to do!")
steps = vi.IntCMDInput()
monitor.write(f"STEPS {steps}")
time.sleep(2)

print("Enter the voltage of the laser!")
laser_voltage = vi.IntCMDInputFromA(0, 4095)
monitor.write(f"LASER {laser_voltage}")
time.sleep(2)

print("Enter the delay in milliseconds between each step of the motor!")
delay = vi.IntCMDInput()
monitor.write(f"DELAY {delay}")

time.sleep(2)
monitor.write("START")
time.sleep(2)
monitor.write("STOP")
time.sleep(2)

data_list = []

data_sending = True
while data_sending:
    data = monitor.device.in_waiting

    if data > 0: # Checks if the data from the serial monitor is bigger than one byte:
        data_str = monitor.read()
        if data_str.startswith("DATA: "):
            data_from_sensor = int(data_str.split(": ")[-1])
            data_list.append(data_from_sensor)

        if data_str.startswith("DATA ACQUISITION"):
            data_sending = False

df = pd.DataFrame().from_dict({"PhotoTransistor Data":data_list})

now = datetime.now().strftime("%Y-%m-%d %H-%M")

if not os.path.isdir("DAQ"):
    os.mkdir("DAQ")
    
csv_file_name = f"DAQ/{now}.csv"

df.to_csv(csv_file_name, index=False)

monitor.write("LASER 0")
monitor.close()

x_axis = np.arange(0, steps, 1)

fig, axs = plt.subplots(1,1)
axs.plot(x_axis, data_list, label="Light")
axs.legend()
axs.set_xlabel("Step")
axs.set_ylabel("Light level from the phototransistor")
plt.show()