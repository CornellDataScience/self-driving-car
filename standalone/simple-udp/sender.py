import socket
import numpy as np
import json
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

my_dict = {'a': 1,
           'b': 2,
           'c': "foo",
           'd': [1, 2, 3],
           'e': np.array([1, 2, 3])}

data_string = pickle.dumps(my_dict, -1)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(data_string, (UDP_IP, UDP_PORT))