import serial
import time

comm = serial.Serial(port='/dev/tty.usbmodem33274401',
                     baudrate=115200, timeout=10)

'''
def led_on_off():
    user_input = input("\n Type on / off / quit : ")
    if user_input == "on":
        print("LED is on...")
        time.sleep(0.1)
        teensy.write(b'H')
        led_on_off()
    elif user_input == "off":
        print("LED is off...")
        time.sleep(0.1)
        teensy.write(b'L')
        led_on_off()
    elif user_input == "quit" or user_input == "q":
        print("Program Exiting")
        time.sleep(0.1)
        teensy.write(b'L')
        teensy.close()
    else:
        print("Invalid input. Type on / off / quit.")
        led_on_off()


time.sleep(2)  # wait for the serial connection to initialize

led_on_off()
'''


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


while True:
    for i in range(10, 60):
        value = write_read(str(i))
        print(value)

# while True:
    # comm.write(bytes(128))
    # time.sleep(0.5)
    #val = comm.read()
    '''
    comm.write(bytes(1))
    val = int.from_bytes(comm.readlines(), 'little')
    print(val)
    '''
