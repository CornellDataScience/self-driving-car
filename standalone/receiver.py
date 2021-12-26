import socket
import numpy as np
import pickle

UDP_IP = "192.168.1.109"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
    reassembled_dict = pickle.loads(data)
    print(reassembled_dict)