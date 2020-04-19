import socket
import lib.tlvtree
from lib.TLV import *
import pickle
import time
import threading
import struct
import os

import config.parameters as para
import config.msg_dic as md

class edge_server:

	def __init__(self,server_port):
		self.server_addr = ('',server_port)
		self.clients_dict = {}

	def ds_listen(self):
		# create a socket, here, SOCK_DGRAM suggested the tpye of the socket -- UDP
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		# bind the socket to a address, same way as TCP.
		# the only difference is: no need of listen() method 
		# bind() function: assign a address and port where the server 'spy' on
		# and where the clients send to 
		s.bind(self.server_addr)
		print('Listening for UDP broadcast at',s.getsockname())

		# time.sleep(5)
		for i in range (5):
			data, client_addr = s. recvfrom(1024)
			# get the message dict
			tlv = pickle.loads(data)
			message_dict = tlv.get_dict()
			# parse the messages in the dict
			for k in message_dict.keys():
				if k == 1:
					self.clients_dict[client_addr] = message_dict[k]
					print('Server received from{}'.format(client_addr))

			# reply to the client
			s.sendto(b'Hello,{}! I\'m {}'.format(client_addr,self.server_addr),client_addr)
		s.close()
		print(self.clients_dict)

	def ts_listen(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
			s.bind(self.server_addr)
			s.listen(10)
		except socket.error as msg:
			print(msg)
			sys.exit(1)
		print('Waiting TCP connection at:',s.getsockname())

		# continiously checking if there is new connection 
		# and start a thread to deal it when it arrives
		while True:
			conn,addr = s.accept()
			t = threading.Thread(target=self.deal_conn,args=(conn,addr))
			t.start()

	def start(self):
		t1 = threading.Thread(target = self.ds_listen)
		t2 = threading.Thread(target = self.ts_listen)
		t1.start()
		t2.start()

	def upload_data(self,filepath):
		# 1 examine the filepath
		if not os.path.isfile(filepath):
			print('file doesn\'t exit!')
			return

		pass

	def deal_conn(self,conn,addr):
		print('Accepted new connection from{0}'.format(addr))
		conn.send('Server({0}):Connection established!'.format(self.server_addr))

		while True:
			fileinfo_size = struct.calcsize('128sl')
			buf = conn.recv(fileinfo_size)
			if buf:
				filename,filesize = struct.unpack('128sl',buf)
				filename = filename.strip('\00')
				new_filename = os.path.join('./','edge_node',filename)
				print('Prepared to receive file! filename:{0},filesize:{1}'.format(new_filename,filesize))

				recvsize = 0
				fp = open(new_filename,'wb')
				print ('start receiving...')
				while not recvsize == filesize:
					if filesize - recvsize > 1024:
						data = conn.recv(1024)
						recvsize += len(data)
					else:
						data = conn.recv(filesize - recvsize)
						recvsize = filesize
					fp.write(data)
				fp.close()
				print('end receiving...')
			conn.close()
			break


if __name__ == '__main__':
	es = edge_server(para.EDGE_SERVER_PORT)
	es.start()
	# es.upload_train_data()
	# es.download_model()
	# es.get_cloud_status()
	# es.start_training()
	# es.stop_training()
	# es.manage_local_models()
