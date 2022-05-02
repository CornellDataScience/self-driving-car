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
    print('Command sent!')


temp = 360

time.sleep(0.5)

while True:
    write(str(temp))
    time.sleep(1)

#Problem: Trade off between delay and length of turn? Can go 360 degrees with no problem using a delay of 1 second, but going longer is questionable
