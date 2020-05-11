from lib.TLV import *
import threading
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
import conf.msg_dic as md


def send_msg(skt, type, body):
	tlv_obj = TLV(t_ext=7, l_ext=7)
	tlv_obj.add_obj(type, body)
	msg = tlv_obj.pop_buf()
	logging.debug('send_msg:| type-{} | length--{} | value-{} |'.format(type,len(msg), body))
	skt.send(msg)

def try_connect_and_send_msg(skt,addr, t, v):
	try:
		# 2.1 try to connect, pack TLV, send send_data_req.
		skt.connect(addr)
		send_msg(skt, t, v)
	except socket.error as e:
		traceback.print_exc()
		return False
	return True

def expect_msg(conn, exp_type):
	logging.debug('expect_msg!:{}'.format(exp_type))
	while True:
		buf = conn.recv(1024)
		if buf:
			logging.debug('expect_msg!: valid buf!{}'.format(buf))
			tlvp = TLVParser(t_ext=7, l_ext=7, socket=conn)
			logging.debug('expect_msg!: new tlvp.buffer!{}'.format(tlvp.buffer))
			tlvp.add_buf(buf)
			logging.debug('expect_msg!: added tlvp.buffer!{}'.format(tlvp.buffer))
			for msg in tlvp.parse_obj():
				logging.debug('expect_msg!: parsed msg!:{}'.format(msg))
				if msg['t'] == exp_type:
					logging.info("expect_msg:got expected msg type:{}".format(msg['t']))
					return msg
				else:
					logging.error("expect_msg:got wrong msg type:{}".format(msg['t'] ))
					return None

def send_file(socket, filename, step = 1024):
    fp = open(filename, 'rb')
    while True:
        data = fp.read(step)
        if not data:
            logging.info("Upload success! file: {}, send over.".format(filename))
            break
        socket.send(data)
    fp.close()


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
	def connect_and_upload_file(filepath, addr):
		s = NetDeviceBase.get_new_tcp_connection(addr)
		NetDeviceBase.upload_file(s, filepath)
		s.close()
		return "Request Sent!"

	@staticmethod
	def get_new_tcp_connection(addr):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			# 2.1 try to connect, pack TLV, send send_data_req.
			s.connect(addr)
		except socket.error as e:
			logging.error("Upload failed:connection failure: {}".format(e))
			traceback.print_exc()
			sys.exit(1)
		return s

	@staticmethod
	def upload_file(conn,filepath):
		# 1 examine the filepath
		if not os.path.isfile(filepath):
			logging.error("Upload failed: file doesn\'t exit!")
			return
		# 2 prepare req data
		f_head = {"name": os.path.basename(filepath), "size": os.stat(filepath).st_size}
		# 3 try send req
		try:
			send_msg(conn, md.SEND_DATA_REQ, f_head)
		except socket.error as e:
			logging.error("Upload failed: {}".format(e))
			traceback.print_exc()
			sys.exit(1)
		# 4 try recv send_data_cfm from server
		msg = expect_msg(conn, md.SEND_DATA_CFM)
		if msg:
			send_file(conn, filepath)
			pass
		else:
			logging.error("Upload failed: expected cfm not received.")
		return "Request Sent!"

	def recv_file_ok(self):
		return True



class FileManagerBase:
	@staticmethod
	def listdir(dirpath, rdb=None):
		l = []
		l_size = []
		l_mtime = []
		root, dirs, files = next(os.walk(dirpath))
		# print("root:{}\ndirs:{}\nfiles:{}\n".format(root, dirs, files))
		for f in files:
			f_info = os.stat(os.path.join(root,f))
			if rdb and os.path.splitext(f)[1].upper() != rdb.upper():
				continue
			l.append(f)
			l_size.append(f_info.st_size)
			l_mtime.append(f_info.st_mtime)
		return l,l_size,l_mtime

	@staticmethod
	def listdir2(dirpath, rdb=None):
		l = []
		root, dirs, files = next(os.walk(dirpath))
		for f in files:
			f_info = os.stat(os.path.join(root,f))
			if rdb and os.path.splitext(f)[1].upper() != rdb.upper():
				continue
			l.append({'filename':f,'size':f_info.st_size,'mtime':f_info.st_mtime})
		logging.debug('listdir:{}'.format(l))
		return l

	@staticmethod
	def get_remote_model_list(addr):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if try_connect_and_send_msg(s, addr, md.GET_MODEL_LIST_REQ, ''):
			msg = expect_msg(s, md.GET_MODEL_LIST_CFM)
			s.close()
			if msg:
				return msg['v']
		s.close()
		return None

	@staticmethod
	def get_remote_model_list2(addr):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if try_connect_and_send_msg(s, addr, md.GET_MODEL_LIST_REQ, ''):
			msg = expect_msg(s, md.GET_MODEL_LIST_CFM)
			logging.debug('get_remote_model_list2:msg:{}'.format(msg))
			s.close()
			if msg:
				return msg['v']
		s.close()
		return None
