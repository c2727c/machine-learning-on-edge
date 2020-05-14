from lib.TLV import *
import os
import logging

logger = logging.getLogger()
sh = logging.StreamHandler()
formater = logging.Formatter('%(asctime)s-%(thread)d-%(levelname)s-%(message)s')
sh.setFormatter(formater)
logger.addHandler(sh)
logger.setLevel(10)
import conf.parameters as para
from lib.net_device_base import \
	NetDeviceBase,FileManagerBase,try_connect_and_send_msg,\
	expect_msg,send_msg,recv_data

import conf.msg_dic as md

from lib.macro import *



class EdgeServer(NetDeviceBase,FileManagerBase):

	def __init__(self, server_addr, cloud_addr):
		NetDeviceBase.__init__(self, server_addr)
		self.cloud_addr = cloud_addr
		self.model_save_path = para.EDGE_MODEL_SAVE_PATH
		self.data_save_path = para.EDGE_DATA_SAVE_PATH

	def deal_conn(self, conn):
		logging.debug('EdgeNode - deal conn ...')
		while True:
			buf = conn.recv(1024)
			if buf:
				tlvp = TLVParser(socket=conn)
				tlvp.add_buf(buf)
				for msg in tlvp.parse_obj():
					logging.debug("MSG = tlvp.parse_obj(): {}".format(msg))
					if msg['t'] == md.SEND_DATA_REQ:
						self.deal_send_data_request(conn, msg)
					else:
						logging.error("Upload failed: Unrecognized request.")
			logging.info("deal_conn:end one round.")
			break

	def deal_send_data_request(self, conn, msg, folder='../../test/edge_node'):
		fhead = msg['v']
		fname = fhead['name']
		fsize = fhead['size']
		if self.recv_file_ok():
			send_msg(conn,md.SEND_DATA_CFM, '')
			new_filename = os.path.join(folder, fname)
			logging.info('Prepared to receive file! new filename:{0}, filesize:{1}'.format(new_filename, fsize))
			recv_data(socket=conn, filename=new_filename, filesize=fsize)
			logging.info('end receiving...')
		else:
			self.tlv_obj.add(md.SEND_DATA_REJ, '')
			conn.send(self.tlv_obj.pop_buf())

	def get_data_list_request(self):
		logging.debug('get_data_list_request - start!!')
		l_c = self.get_remote_file_list(self.cloud_addr,'data')
		l_e = self.listdir2(self.data_save_path)
		self.merge_list_with_mark(l_e,l_c)
		return l_e

	def get_model_list_request2(self):
		logging.debug('get_model_list_request2 - start!!')
		l_c = self.get_remote_file_list(self.cloud_addr,'model')
		l_e = self.listdir2(self.model_save_path)
		self.merge_list_with_mark(l_e,l_c)
		return l_e

	def download_model_request(self,fname):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if try_connect_and_send_msg(s, self.cloud_addr, md.GET_FILE_REQ, fname):
			msg = expect_msg(s, md.SEND_DATA_REQ)
			if msg:
				self.deal_send_data_request(s, msg, folder=self.model_save_path)

	def train_model_request(self,dataset_name,steps,train_from_scratch):
		conn = self.get_new_tcp_connection(self.cloud_addr)
		send_msg(conn,md.TRAIN_MODEL_REQ,
		         {"detaset":dataset_name, "steps": steps,"from_scratch":train_from_scratch})
		pass

if __name__ == '__main__':
	es = EdgeServer((para.EDGE_SERVER_IP, para.EDGE_SERVER_PORT),
	                (para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT))
	print(es.get_data_list_request())