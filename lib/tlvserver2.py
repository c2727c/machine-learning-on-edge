import socket
import threading
import pickle
import sys
import time
import traceback
from TLV import *
# a list to remain active sockets


print('start')
socket_list = []
# create socket
ss = socket.socket()
ss.bind(('localhost',5448))
# listening from the clients, set the maximum number of connections
ss.listen(5)
tlv_obj = TLV(t_ext=7, l_ext=7)

print('start')
def server_target(s):
    print('server_target')
    try:
        while True:
            line = ('localhost',5448)
            line2 = sys.stdin.readline()
            if line is None or line == 'exit':
                break
            print('ok')
            # time.sleep(2)
            tlv_obj.add(8,line)
            print(tlv_obj.buffer)
            s.send(tlv_obj.pop_buf())
            tlv_obj.add(9,line2)
            print(tlv_obj.buffer)
            s.send(tlv_obj.pop_buf())
    except Exception:
        traceback.print_exc()

while True:
    # wait for a connection
    s, addr = ss.accept()
    #socket_list.append(s)
    # start threads for each client
    threading.Thread(target=server_target, args=(s, )).start()