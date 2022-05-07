import serial
import time

comm = serial.Serial(port='/dev/tty.usbmodem142101',
                     baudrate=115200, timeout=10)

def write_read(x):
    #bytestring = bytes(x, 'utf-8')
    # print(bytestring)
    comm.write(x.encode('UTF-8'))
    while(not comm.in_waiting):
        time.sleep(0.01);
        pass
    time.sleep(0.01)
    data = comm.readline()
    return data

def write(x):
    comm.write(x.encode('UTF-8'))

time.sleep(0.5)

def full_rotate_right():
    while True: 
        write(str(360))
        time.sleep(1)
        if comm.in_waiting: 
            data = comm.readline()
            print(str(data))
            if '3240' in str(data): 
                break

def full_rotate_left():
    while True:
        write(str(-360))
        time.sleep(1)
        if comm.in_waiting:
            data = comm.readline()
            if '-3240' in str(data): 
                break

def execute(): 
    time.sleep(0.5)
    '''
    temp = 360
    while True: 
        write(str(temp))
        if comm.in_waiting: 
            data = comm.readline()
            print(data)
        time.sleep(1)
    '''
    full_rotate_right()
    full_rotate_left()

execute()

#Problem: Trade off between delay and length of turn? Can go 360 degrees with no problem using a delay of 1 second, but going longer is questionable
