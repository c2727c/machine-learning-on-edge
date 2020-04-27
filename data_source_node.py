import socket
import pickle
import os
import struct

import conf.parameters as para
import conf.msg_dic as md
from lib.tlvtree import TLVTree
from lib.TLV import *
import sys

class data_source_client:

	def __init__(self,server_port):
		self.server_addr = ('<broadcast>',server_port)#represent a broadcast IP address

	def register(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		#type = 1, length = 0
		myrawdata = "\x01\x01\xac"
		tlv = TLVTree(myrawdata,debug=True)
		data = pickle.dumps(tlv)
		s.sendto(data,self.server_addr)
		data, self.server_addr = s. recvfrom(2048)
		s.close()

	def send_data(self,filepath):
		# try to connect to the server
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.server_addr))
		except socket.error as error_msg:
			print (error_msg)
			sys.exit(1)
		print(s.recv(1024))

		# examine the filepath
		if not os.path.isfile(filepath):
			print('file doesn\'t exit!')
			return
		
		# firstly,send file info head
		# fileinfo_size = struct.calcsize('128sl')
		fhead = struct.pack('128sl',os.path.basename(filepath),
							os.stat(filepath).st_size)
		s.send(fhead)
		print ('client filepath: {0}'.format(filepath))

		fp = open(para.FILEPATH,'rb')
		while True:
			data = fp.read(1024)
			if not data:
				print('file: {}, send over.'.format(para.FILEPATH))
				break
			s.send(data)
		s.close()

if __name__ =='__main__':
	c = data_source_client(para.EDGE_SERVER_PORT)
	c.register()
	print(c.server_addr)
	c.send_data(para.FILEPATH)



