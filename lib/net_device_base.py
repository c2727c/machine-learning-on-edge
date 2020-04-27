from lib.TLV import *
import threading
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
import conf.msg_dic as md
from lib.macro import *


def send_msg(skt, type, body):
	# 2 try to connect, pack TLV, send send_data_req.
	tlv_obj = TLV(t_ext=7, l_ext=7)
	tlv_obj.add_obj(type, body)
	skt.send(tlv_obj.pop_buf())


def expect_msg(skt, exp_type):
	tlvp = TLVParser("", t_ext=7, l_ext=7, socket=skt)
	tlvp.add_buf(skt.recv(1024))
	for msg in tlvp.parse_obj():
		if msg['t'] == exp_type:
			return msg
		else:
			return None


class NetDeviceBase:

	def __init__(self, server_addr):
		self.server_addr = server_addr
		self.tlv_obj = TLV(t_ext=7, l_ext=7)
		self.tcp_clients_dict = {}
		# self.udp_clients_dict = {}

	def start(self):
		t = threading.Thread(target=self.tcp_listen)
		t.start()

	def tcp_listen(self):
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
			t1 = threading.Thread(target=self.deal_addr, args=(addr,))
			t2 = threading.Thread(target=self.deal_conn, args=(conn,))
			t1.start()
			t2.start()

	def deal_addr(self,addr):
		logging.debug('NetDeviceBase - deal addr ...')
		logging.info('Accepted new connection from{}'.format(addr))

	def deal_conn(self):
		logging.debug('NetDeviceBase - deal conn ...')

	@staticmethod
	def upload_file(filepath, addr):
		# 1 examine the filepath
		if not os.path.isfile(filepath):
			logging.error("Upload failed: file doesn\'t exit!")
			return

		# 2 create new socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			# 2.1 try to connect, pack TLV, send send_data_req.
			s.connect(addr)
			f_head = {"name": os.path.basename(filepath), "size": os.stat(filepath).st_size}
			send_msg(s, md.SEND_DATA_REQ, f_head)
		except socket.error as e:
			logging.error("Upload failed: {}".format(e))
			traceback.print_exc()
			sys.exit(1)

		# 3 try to recv send_data_cfm from server
		msg = expect_msg(s, md.SEND_DATA_CFM)
		if msg:
			send_file(s, filepath)
		else:
			logging.error("Upload failed: expected cfm not received.")
		s.close()
