import serial
import time

def write(x, port):
    port.write(x.encode('UTF-8'))

def spin(x, port):
    write(str(x), port)
    time.sleep(0.0856)
    write(str(x), port)
    time.sleep(0.0856)