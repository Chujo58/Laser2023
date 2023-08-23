import arduino_connect as arduino
from ValidInputs import ValidInputs as vi
import pandas as pd
from datetime import datetime
import os, time

monitor = arduino.ArduinoControl(debug=True)

print("Enter the number of steps you want the motor to do!")
steps = vi.IntCMDInput()
print("Enter the voltage of the laser!")
laser_voltage = vi.IntCMDInputFromA(0, 4095)
print("Enter the delay in milliseconds between each step of the motor!")
delay = vi.IntCMDInput()

monitor.write(f"LASER {laser_voltage}")
time.sleep(2)
monitor.write(f"STEPS {steps}")
time.sleep(2)
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

df.to_csv(csv_file_name)

# monitor.write("LASER 0")
# monitor.close()