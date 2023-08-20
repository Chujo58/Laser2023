import arduino_connect as arduino
from ValidInputs import ValidInputs as vi

monitor = arduino.ArduinoControl()

print("Enter the number of steps you want the motor to do!")
steps = vi.IntCMDInput()
print("Enter the voltage of the laser!")
laser_voltage = vi.IntCMDInputFromA(0, 4095)
print("Enter the delay between each step of the motor!")
delay = vi.IntCMDInput()