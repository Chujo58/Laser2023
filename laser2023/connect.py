import arduino_connect as arduino
from ValidInputs import ValidInputs as vi
import pandas as pd
from datetime import datetime

monitor = arduino.ArduinoControl()

print("Enter the number of steps you want the motor to do!")
steps = vi.IntCMDInput()
print("Enter the voltage of the laser!")
laser_voltage = vi.IntCMDInputFromA(0, 4095)
print("Enter the delay in milliseconds between each step of the motor!")
delay = vi.IntCMDInput()

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

now = datetime.now().strftime("%Y-%m-%d %H:%M")
csv_file_name = f"DAQ - {now}.csv"

df.to_csv(csv_file_name)