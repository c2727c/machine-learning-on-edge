import socket
import threading
import pickle
import sys
import time
from lib.TLV import *
# a list to remain active sockets


print('start')
socket_list = []
# create socket
ss = socket.socket()
ss.bind(('localhost',5488))
# listening from the clients, set the maximum number of connections
ss.listen(5)
tlv = TLV(t_ext=7, l_ext=7)
print('start')
def server_target(s):
    print('server_target')
    try:
        while True:
            line = sys.stdin.readline()
            if line is None or line == 'exit':
                break
            print('ok')
            time.sleep(2)
            tlv.add(8,line)
            data = pickle.dumps(tlv)
            s.send(data)
    except Exception:
        print(Exception)

while True:
    # wait for a connection
    s, addr = ss.accept()
    #socket_list.append(s)
    # start threads for each client
    threading.Thread(target=server_target, args=(s, )).start()