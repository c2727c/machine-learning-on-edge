# coding=utf-8
from lib.TLV import *
from lib.macro import *
import os
import logging

logging.basicConfig(level=logging.NOTSET)
import conf.parameters as para
import conf.msg_dic as md
from lib.net_device_base import NetDeviceBase


# class ENF:
# 	def __init__(self, name, addr, uptodate):
# 		self.name = name
# 		self.addr = addr
# 		self.uptodate = uptodate


class CloudServer(NetDeviceBase):

	def __init__(self, server_ip, server_port):
		NetDeviceBase.__init__(self, (server_ip, server_port))

	def deal_addr(self,addr):
		logging.debug('CloudServer - deal addr ...')
		logging.info('Accepted new connection from{}'.format(addr))
		if self.tcp_clients_dict.has_key(addr) and \
				self.tcp_clients_dict[addr] == para.EN_UP_TO_DATE:
			return
		self.tcp_clients_dict[addr] = para.EN_FALL_BEHIND
		logging.debug('CloudServer - clients_dict :{}'.format(self.tcp_clients_dict))
		self.send_module()

	def deal_conn(self, conn):
		logging.debug('CloudServer - deal conn ...')
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
			self.tlv_obj.add_obj(md.SEND_DATA_CFM, '')
			conn.send(self.tlv_obj.pop_buf())
			# 接收文件
			new_filename = os.path.join('test/cloud_server', fname)
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

	def send_module(self):
		logging.debug('CloudServer - send_module ...')
		pass

if __name__ == '__main__':
	cs = CloudServer(para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT)
	cs.start()
	# time.sleep(5)
	# cs.upload_file(para.FILEPATH2,(para.EDGE_SERVER_IP, para.EDGE_SERVER_PORT))
