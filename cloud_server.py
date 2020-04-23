# coding=utf-8
import socket
import lib.tlvtree
from lib.TLV import *
from lib.macro import *
import pickle
import time
import threading
import struct
import os
import sys
import logging
logging.basicConfig(level=logging.NOTSET)
import config.parameters as para
import config.msg_dic as md

# class ENF:
# 	def __init__(self, name, addr, uptodate):
# 		self.name = name
# 		self.addr = addr
# 		self.uptodate = uptodate



class CloudServer:
	def __init__(self, server_ip, server_port, file_server_port):
		self.server_addr = (server_ip, server_port)
		self.file_server_addr = (server_ip, file_server_port)
		self.clients_dict = {}
		self.tlv_obj = TLV(t_ext=7, l_ext=7)

	def ts_listen(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind(self.server_addr)
			s.listen(10)
		except socket.error as e:
			logging.error("Socket failure: {}".format(e))
			sys.exit(1)
		logging.info('Waiting TCP connection at:{}'.format(s.getsockname()))

		while True:
			conn, addr = s.accept()
			t = threading.Thread(target=self.deal_conn, args=(conn, addr))
			t.start()

	def deal_conn(self, conn, addr):
		logging.info('Accepted new connection from{}'.format(addr))
		# conn.send('Server({0}):Connection established!'.format(self.server_addr))
		while True:
			buf = conn.recv(1024)
			if buf:
				tlvp = TLVParser("", t_ext=7, l_ext=7, socket=conn)
				tlvp.add_buf(buf)
				for msg in tlvp.parse_obj():
					logging.debug("MSG = tlvp.parse_obj(): {}".format(msg))
					if msg['t'] == md.SEND_DATA_REQ:
						self.deal_send_data_req(conn, msg)
					else:
						logging.error("Upload failed: Unrecognized request.")
			conn.close()
			break

	def deal_send_data_req(self, conn, msg):
		fhead = msg['v']
		fname = fhead['name']
		fsize = fhead['size']
		if self.recv_file_ok():
			# 返回cfm
			self.tlv_obj.add_obj(md.SEND_DATA_CFM, self.file_server_addr)
			conn.send(self.tlv_obj.pop_buf())
			# 接收文件
			new_filename = os.path.join('cloud_server', fname)
			logging.info('Prepared to receive file! new filename:{0}, filesize:{1}'.format(new_filename, fsize))
			recv_file(socket=conn, filename=new_filename, filesize=fsize)
			logging.info('end receiving...')
			conn.close()

		else:
			self.tlv_obj.add(md.SEND_DATA_REJ, '')
			conn.send(self.tlv_obj.pop_buf())
			conn.close()

	def recv_file_ok(self):
		return True






if __name__ == '__main__':
	cs = CloudServer(para.CLOUD_SERVER_IP,para.CLOUD_SERVER_PORT,para.CLOUD_FILE_SERVER_PORT)
	cs.ts_listen()
# 	new_filename = os.path.join('./', 'edge_node', filename)
# 	print('Prepared to receive file! filename:{0},filesize:{1}'.format(new_filename, filesize))
#
# 	recvsize = 0
# 	fp = open(new_filename, 'wb')
# 	print ('start receiving...')
# 	while not recvsize == filesize:
# 		if filesize - recvsize > 1024:
# 			data = conn.recv(1024)
# 			recvsize += len(data)
# 		else:
# 			data = conn.recv(filesize - recvsize)
# 			recvsize = filesize
# 		fp.write(data)
# 	fp.close()
# 	print('end receiving...')
#
#
# conn.close()
# break
