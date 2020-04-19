import sys
sys.path.append('..')
import socket
import lib.macro as mc




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#establish the tcp connection
s.connect(("www.z2727c.com",80))
#send request
s.send(b'GET / HTTP/1.1\r\nHost:www.z2727c.com\r\nConnection:close\r\n\r\n')
#receive data
# buffer = []
# receive_all_2(s,buffer)
# data = b''.join(buffer)


data = mc.receive_all(s) 
# while True:
# 	d = s.recv(2048)
# 	if d:
# 		buffer.append(d)
# 	else:
# 		break
#join the bytes

#close connection
s.close()
#read data
with open('2727c.html','wb') as f:
	f.write(data)

