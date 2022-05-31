from flask import Flask
from flask import jsonify
import threading
import time
import serial

import json 

# import argparse
# parser = argparse.ArgumentParser(description='Flask Sever: USB Port')

# parser.add_argument('-a', action="store_true", default=False)

# print(parser.parse_args())

with open('telem.json') as f:
  telem_index = json.load(f)
reverse_telem_index = {v:k for (k,v) in telem_index.items()}
# dummy data to be over written
telem_data = {k:v for (k,v) in telem_index.items()}

POOL_TIME = 0.001
altitude = 0
incr = 0
ccno = 0
dataLock = threading.Lock()
threadHandler = threading.Thread()


telem = serial.Serial('/dev/ttyACM0')
# telem = serial.Serial('/dev/ttyUSB0', 57600)
telem.reset_input_buffer()

def str_to_val(field):
    '''
    Automatically detects floats, ints and bools

    Returns a float, int or bool
    '''
    if 'nan' in field:
        return float("NAN")
    elif '.' in field:
        return float(field)
    elif field == 'true':
        return True
    elif field == 'false':
        return False
    else:
        return int(field)

def parse_token(ret):
    if ',' in ret:
        # ret is a list
        list_of_strings = ret.split(',')
        list_of_strings = [x for x in list_of_strings if x is not '']
        list_of_vals = [str_to_val(x) for x in list_of_strings]
        return list_of_vals
    else:
        return str_to_val(ret)


def listgen(input_string):
    ret = input_string.split(";")
    ret = [x for x in ret if x != '']
    ret = [parse_token(x) for x in ret]
    return ret


def interrupt():
    global threadHandler
    threadHandler.cancel()

def doStuff():
    global altitude
    global threadHandler
    global incr
    global ccno
    global telem_index, telem_data

    with dataLock:
    # Do your stuff with commonDataStruct Here
        raw_bytes = telem.readline().strip().decode("utf-8")
        print(raw_bytes)
        # tokens = listgen(raw_bytes)
        # if len(tokens) != len(telem_index):
        #     print(f"INVALID NUMBER TOKENS, got: {len(tokens)}, expected: {len(telem_index)}")
            
        # else:
        #     for i in range(len(tokens)):
        #         telem_data[reverse_telem_index[i]] = tokens[i]

        #     # print(telem_data)
        #     ccno = tokens[0]
        #     # print(ccno)
        #     altitude = tokens[1]
        #     incr += 1

    # Set the next thread to happen
    threadHandler = threading.Timer(POOL_TIME, doStuff, ())
    threadHandler.start()   

def doStuffStart():
    # Do initialisation stuff here
    global threadHandler
    # Create your thread
    threadHandler = threading.Timer(POOL_TIME, doStuff, ())
    threadHandler.start()

doStuffStart()

app = Flask(__name__)

@app.route('/query', methods = ['POST'])
def get_query_from_react():
    return "Flask Server Yeet."

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/ccno')
def get_ccno():
    global ccno
    with dataLock:
        return {'ccno': ccno}

@app.route('/altitude')
def get_altitude():
    global dataLock, altitude, incr
    with dataLock:
        return {'altitude': altitude}

@app.route('/altitudes')
def get_altitudes():
    global dataLock, altitude, ccno
    with dataLock:
        return jsonify(cc=ccno,alt = altitude)

@app.route('/telem_packet')
def get_telem_packet():
    global dataLock, telem_data
    with dataLock:
        return jsonify(telem_data)