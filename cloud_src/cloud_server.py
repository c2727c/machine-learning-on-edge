# coding=utf-8
from lib.TLV import *
from lib.macro import *
import os
import logging
logger = logging.getLogger()
sh = logging.StreamHandler()
formater = logging.Formatter('%(asctime)s-%(thread)d-%(levelname)s-%(message)s')
sh.setFormatter(formater)
logger.addHandler(sh)
logger.setLevel(10)

import conf.parameters as para
import conf.msg_dic as md
import fer2013.fer_config as fer_conf
from lib.net_device_base import NetDeviceBase,FileManagerBase,send_msg,expect_msg


# class ENF:
# 	def __init__(self, name, addr, uptodate):
# 		self.name = name
# 		self.addr = addr
# 		self.uptodate = uptodate
def train():
	pass

class CloudServer(NetDeviceBase,FileManagerBase):

	def __init__(self, server_ip, server_port):
		NetDeviceBase.__init__(self, (server_ip, server_port))
		self.model_save_path = para.CLOUD_MODEL_SAVE_PATH
		self.data_save_path = para.CLOUD_DATA_SAVE_PATH

	def deal_addr(self,addr):
		logging.debug('CloudServer - deal addr ...')
		logging.info('Accepted new connection from{}'.format(addr))
		if addr in self.tcp_clients_dict and \
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
				tlvp = TLVParser(socket=conn)
				tlvp.add_buf(buf)
				for msg in tlvp.parse_obj():
					logging.debug("CloudServer - deal_conn: new msg:{} ".format(msg))
					tp = msg['t']
					if tp == md.SEND_DATA_REQ:
						self.deal_send_data_req(conn, msg)
					elif tp == md.GET_MODEL_LIST_REQ:
						# self.deal_get_model_list_req(conn, msg)
						self.deal_get_model_list_req2(conn, msg)
					elif tp == md.GET_MODEL_REQ:
						self.deal_get_model_req(conn, msg)
					elif tp == md.TRAIN_MODEL_REQ:
						self.deal_train_model_req(conn, msg)
					else:
						logging.error("CloudServer - deal_conn: Unrecognized request.")
			# conn.close()
			logging.info("deal_conn:end one round.")
			break

	def deal_send_data_req(self, conn, msg):
		fhead = msg['v']
		fname = fhead['name']
		fsize = fhead['size']
		if self.recv_file_ok():
			# 返回cfm
			send_msg(conn, md.SEND_DATA_CFM, '')
			# 接收文件
			new_filename = os.path.join(self.data_save_path, fname)
			logging.info('Prepared to receive file! new filename:{0}, filesize:{1}'.format(new_filename, fsize))
			recv_file(socket=conn, filename=new_filename, filesize=fsize)
			logging.info('end receiving...')
		else:
			send_msg(conn, md.SEND_DATA_REJ, '')

	def deal_get_model_list_req2(self, conn, msg):
		type = msg['v']
		l=''
		if type =='model':
			l = self.listdir2(self.model_save_path)
		elif type == 'data':
			l = self.listdir2(self.data_save_path)
		send_msg(conn,md.GET_MODEL_LIST_CFM,l)

	def deal_get_model_req(self, conn, msg):
		model_name = msg['v']
		model_path = os.path.join(self.model_save_path,model_name)
		self.upload_file(conn,model_path)

	def deal_train_model_req(self,conn, msg):
		value = msg['v']
		dataset_name = value["dataset"]
		steps = value["steps"]
		train_from_scratch = value["from_scratch"]
		fer_api.train_model(dataset_name,steps,train_from_scratch)
		pass


	def send_module(self):
		logging.debug('CloudServer - send_module ...')
		pass

if __name__ == '__main__':
	cs = CloudServer(para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT)
	cs.start()
	# time.sleep(5)
	# cs.connect_and_upload_file(para.FILEPATH2,(para.EDGE_SERVER_IP, para.EDGE_SERVER_PORT))
