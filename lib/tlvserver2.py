import socket
import threading
import pickle
import sys
import time
import traceback
from lib.TLV import *
from lib.macro import *

# a list to remain active sockets


print('start')
socket_list = []
# create socket
ss = socket.socket()
ss.bind(('localhost', 5449))
# listening from the clients, set the maximum number of connections
ss.listen(5)
tlv_obj = TLV(t_ext=7, l_ext=7)

print('start')


def server_target(s):
    print('server_target')
    try:
        while True:
            line = ('localhost', 5448)
            # line = input()
            line2 = input()
            if line is None or line == 'exit':
                break
            print('ok')
            # time.sleep(2)
            tlv_obj.add_obj(8, line)
            print(b_str(tlv_obj.buffer))
            s.send(tlv_obj.pop_buf())
            tlv_obj.add_obj(9, line2)
            print(b_str(tlv_obj.buffer))
            s.send(tlv_obj.pop_buf())
    except Exception:
        traceback.print_exc()


while True:
    # wait for a connection
    s, addr = ss.accept()
    # socket_list.append(s)
    # start threads for each client
    threading.Thread(target=server_target, args=(s,)).start()
