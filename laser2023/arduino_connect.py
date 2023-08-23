#----------------------------------------------------------------------------
# Created by : Chloé Legué and Kevin Nguyen
# Current version date : 2023/08/23
#----------------------------------------------------------------------------
"""
This code can be used as a general way to control an Arduino using the Serial monitor in Python. In the solid-state laser experiment, the Arduino code uses a `CONFIG.h` file which contains the `BAUD_RATE` and the `COM` port. 
This is to simplify the Python code so that you do not have to manually enter the baud rate and COM port. 
If you did not properly set the COM port, the code will simply not be able to find the Arduino board and will not be able to communicate properly to it.
The baud rate is shared with the Arduino code, so you do not have to worry about setting it up properly.
"""
import serial

SERIAL_PORT = ""
BAUD_RATE = 0

with open("CONFIG.h", "r") as f:
    config = f.readlines()

for line in config:
    words = line.split(" ")
    var = words[1] if len(words) > 2 else None
    if var is not None:
        if var == "COM":
            com = words[2].split('\n')[0]
            SERIAL_PORT = f"COM{com}"

        if var == "BAUD_RATE":
            BAUD_RATE = int(words[2])

class ArduinoControl:
    """ArduinoControl Class.
    Allows the user to control the Arduino from the serial line.

    Parameters
    ----------
    device : str, optional
        Serial port, by default will be the port selected in the `CONFIG.h` file.
    debug : bool, optional
        If we launch the controller in debug mode or not (gives extra messages), by default False
    """
    def __init__(self, device = SERIAL_PORT, debug = False) -> None:
        self.debug = debug
        if self.debug : print("Debug mode activated!")
        try:
            # Let's connect to the selected serial port.
            self.device = serial.Serial(device, baudrate=BAUD_RATE)
            if self.debug: print(f"Connect to the Arduino on port: {device}.")
        except:
            print(f"Arduino board not found at the selected port: {device}.")
            return
        
        # Let's forcefully reboot the Arduino.
        self.device.setDTR(1);
        self.device.setDTR(0);
        self.device.setDTR(1);

        exceptions = 0
        attemps = 0
        while True:
            try:
                # Let's check the first line sent out by the Arduino on the serial port.
                if "LASER 2023" == self.read():
                    if self.debug: print("Arduino is communicating!")
                    return # We leave the loop since the Arduino seems to be connected properly.
            except:
                if self.debug: print("An exception occured!")
                exceptions += 1 #Counts the number of exceptions that have occured.

            attemps += 1 #Counts the number of attemps that have been made.
            if 5 == attemps: #Let's stop after 5 attemps/exceptions... This probably means that it is not possible to connect to the Arduino.
                print(f"Unable to conenct to the Arduino after {exceptions} exceptions.")
                break 

    def write(self, message: str):
        """Sends a message to the Arduino via the Serial monitor.

        Parameters
        ----------
        message : str
            Message to be sent to the Arduino.
        """
        message += "\n" # Returns the line at the end of it.
        self.device.write(message.encode()) #Encodes the message and sends it to the Serial monitor.
        if self.debug: print(f"Sent '{message}'")

    def read(self) -> str:
        """Reads a message sent from the Arduino via the Serial monitor.

        Returns
        -------
        str
            Message from the Arduino.
        """
        if self.debug: print("Waiting for a response from the arduino...")
        data_str = self.device.readline().decode().split('\r\n')[0]
        if self.debug: print(f"Got response: {data_str}")
        return data_str
    
    def close(self):
        """Closes the serial port.
        """
        self.device.close()
        print("Port is now closed.")
