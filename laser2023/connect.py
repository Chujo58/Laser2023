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
            SERIAL_PORT = f"COM{words[2]}"

        if var == "BAUD_RATE":
            BAUD_RATE = int(words[2])

monitor = serial.Serial(SERIAL_PORT, BAUD_RATE)
monitor.setDTR(1);
monitor.setDTR(0);
monitor.setDTR(1);
monitor.open()

monitor.write("TESTING STUFF AGAIN".encode())