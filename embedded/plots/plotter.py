import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# from serial import Serial
import serial 
#note hardcoded serial port
telem = serial.Serial('/dev/ttyUSB0', 57600)

timecnt = 100
totallen = 100
xar = [x for x in range(totallen)]
alt = [5 for x in range(totallen)]
var1 = [-40 for x in range(totallen)]
lin_acc_z = [-40 for x in range(totallen)]

def listgen(input_string):
    print(input_string)
    ret = input_string.replace(',',';').split(";")
    ret = [x for x in ret if x != '']
    ret = [float(x) for x in ret]
    return ret

# while(len(alt)!=10):
#     xar += [timecnt]
#     alt += [listgen(telem.readline().strip().decode("utf-8"))[0]]
#     timecnt += 1

def animate(i):
    # pullData = open("sampleText.txt","r").read()
    # dataArray = pullData.split('\n')
    # xar = []
    # yar = []
    # for eachLine in dataArray:
    #     if len(eachLine)>1:
    #         x,y = eachLine.split(',')
    #         xar.append(int(x))
    #         yar.append(int(y))
    global timecnt, alt, xar, var1, lin_acc_z

    telem_data = listgen(telem.readline().strip().decode("utf-8"))

    xar = xar[1:] + [timecnt]
    timecnt += 1

    alt_index = 1
    lin_acc_z_index = 4
    
    alt = alt[1:] + [telem_data[alt_index]]
    lin_acc_z = lin_acc_z[1:] + [telem_data[lin_acc_z_index] + 112.5]

    ax1.clear()
    #plt.ylim(-41,-40)
    # ax1.set_ylim(top=-40)
    # ax1.set_ylim(bottom=-41)
    ax1.set_ylim(110, 115)
    #print(alt)
    ax1.plot(xar,alt)
    ax1.plot(xar, lin_acc_z)
    
fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)


ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
