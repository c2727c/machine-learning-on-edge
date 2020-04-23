import socket
import threading
import pickle
from lib.TLV import *
sys.path.append('..')
import lib.macro as mc

# create the socket
s = socket.socket()
# connect to the server
s.connect(('localhost', 5488))

def read_from_server(s):
    try:
        # d = mc.recv_all(s,2048)
        # print("d:",d)
        # data = pickle.loads(d)
        data = pickle.loads(s.recv(1024))
        # test
        tlvp = TLVParser(data.buffer, t_ext=7, l_ext=7)
        for avp in tlvp.parse():
            print("%d(%d): %s" % (avp["type"], avp["length"], avp["value"]))
        # return s.recv(2048).decode('utf-8')
        return tlvp
    # If an exception is caught, the client corresponding to the socket is closed
    except:
        # delete the socket
        socket_list.remove(s)   #1

def read_server(s):
    try:
        while True:
                contend = read_from_server(s)
                if contend is None:
                        break
    except:
        print(Exception)

# start a thread to read from server continiously
threading.Thread(target=read_server, args=(s, )).start()