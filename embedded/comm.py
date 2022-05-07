import serial
import time

comm = serial.Serial(port='/dev/tty.usbmodem142101',
                     baudrate=115200, timeout=10)

def write(x):
    comm.write(x.encode('UTF-8'))

time.sleep(0.5)

def spin(x):
    write(str(x))
    time.sleep(0.0856)
    write(str(x))
    time.sleep(0.0856)

def execute(): 
    spin(360)
    time.sleep(3)
    spin(-360)
    #time.sleep(0.1)

execute()