import socket
import threading
import pickle
import traceback

from lib.TLV import *

sys.path.append('..')
import lib.macro as mc

# create the socket
s = socket.socket()
# connect to the server
s.connect(('localhost', 5449))


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
        for avp in tlvp.parse_obj():
            print("%d(): %s" % (avp["type"], avp["value"].__str__()))
            print(avp["value"])
            print('----parse once---')

        # return s.recv(2048).decode('utf-8')
        return tlvp
    # If an exception is caught, the client corresponding to the socket is closed
    except Exception as e:
        traceback.print_exc()
        # delete the socket



def read_server(s):
    try:
        while True:
            contend = read_from_server(s)
            if contend is None:
                break
    except:
        print(Exception)


# start a thread to read from server continiously
threading.Thread(target=read_server, args=(s,)).start()
