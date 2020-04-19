import socket
import threading
import pickle
import traceback

from TLV import *
sys.path.append('..')
import lib.macro as mc

# create the socket
s = socket.socket()
# connect to the server
s.connect(('localhost', 5448))


def read_from_server(s):
    # [FIXME]
    tlvp = TLVParser("", t_ext=7, l_ext=7, socket=s)
    try:
        # d = mc.recv_all(s,2048)
        # print("d:",d)
        # data = pickle.loads(d)
        tlvp.add_buf(s.recv(10))
        print('----recv once---')
        # test
        for avp in tlvp.parse():
            print("%d(%d): %s" % (avp["type"], avp["length"], avp["value"]))
            print('----parse once---')
        # return s.recv(2048).decode('utf-8')
        return tlvp
    # If an exception is caught, the client corresponding to the socket is closed
    except Exception, e:
        traceback.print_exc()
        # delete the socket
        socket_list.remove(s)   #1


def read_from_server2(s):
    tlvp = TLVParser("", t_ext=7, l_ext=7, socket=s)
    try:
        # d = mc.recv_all(s,2048)
        # print("d:",d)
        # data = pickle.loads(d)
        flag = True
        while flag:
            tlvp.add_buf(s.recv(10))
            print('----recv once---')
            try:    
                # test
                for avp in tlvp.parse():
                    print("%d(%d): %s" % (avp["type"], avp["length"], avp["value"]))
                    print('----parse once---')
                # return s.recv(2048).decode('utf-8')
                flag = False
            except TLVError, e:
                # traceback.print_exc()
                flag = True
        return tlvp
    # If an exception is caught, the client corresponding to the socket is closed
    except Exception, e:
        traceback.print_exc()
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