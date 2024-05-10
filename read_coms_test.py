import serial.tools.list_ports_windows
import time


arduino = serial.Serial(port= "COM3",baudrate=115200, timeout=1)


def read():
    arduino.write(bytes("g",  'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data)


while True:
    read()