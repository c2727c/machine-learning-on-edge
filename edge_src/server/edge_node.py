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
	expect_msg,send_msg

import conf.msg_dic as md

from lib.macro import *

class EdgeServer(NetDeviceBase,FileManagerBase):

	def __init__(self, server_addr, cloud_addr):
		NetDeviceBase.__init__(self, server_addr)
		self.cloud_addr = cloud_addr
		self.model_save_path = para.EDGE_MODEL_SAVE_PATH

	def deal_conn(self, conn):
		logging.debug('EdgeNode - deal conn ...')
		while True:
			buf = conn.recv(1024)
			if buf:
				tlvp = TLVParser(t_ext=7, l_ext=7, socket=conn)
				tlvp.add_buf(buf)
				for msg in tlvp.parse_obj():
					logging.debug("MSG = tlvp.parse_obj(): {}".format(msg))
					if msg['t'] == md.SEND_DATA_REQ:
						self.deal_send_data_request(conn, msg)
					else:
						logging.error("Upload failed: Unrecognized request.")
			logging.info("deal_conn:end one round.")
			# conn.close()
			break

	def deal_send_data_request(self, conn, msg, folder='../../test/edge_node'):
		fhead = msg['v']
		fname = fhead['name']
		fsize = fhead['size']
		if self.recv_file_ok():
			send_msg(conn,md.SEND_DATA_CFM, '')
			new_filename = os.path.join(folder, fname)
			logging.info('Prepared to receive file! new filename:{0}, filesize:{1}'.format(new_filename, fsize))
			recv_file(socket=conn, filename=new_filename, filesize=fsize)
			logging.info('end receiving...')

		else:
			self.tlv_obj.add(md.SEND_DATA_REJ, '')
			conn.send(self.tlv_obj.pop_buf())

	def get_model_list_request(self):
		cf_list,cf_size_lizt,cf_time_list = self.get_remote_model_list(self.cloud_addr)
		ef_list,ef_size_lizt,ef_time_list = self.listdir(self.model_save_path)
		i = 0
		while i<len(cf_list):
			if cf_list[i] in ef_list:
				del cf_list[i]
				del cf_size_lizt[i]
				del cf_time_list[i]
			else:
				i = i+1
		cf_stat_list = [0] * len(cf_list)
		ef_stat_list = [1 for i in range(len(ef_list))]
		f_list = ef_list+cf_list
		f_size_lizt = ef_size_lizt + cf_size_lizt
		f_time_list = ef_time_list + cf_time_list
		f_stat_list = ef_stat_list+cf_stat_list
		return f_list,f_size_lizt,f_time_list,f_stat_list

	def get_model_list_request2(self):
		logging.debug('get_model_list_request2 - start!!')
		l_c = self.get_remote_model_list2(self.cloud_addr)
		l_e = self.listdir2(self.model_save_path)
		i = 0
		while i<len(l_c):
			if l_c[i] in l_e:
				del l_c[i]
			else:
				i = i+1
		for i in range(len(l_c)):
			logging.debug('l_c[i]:{}'.format(l_c[i]))
			for j in range(len(l_e)):
				if l_c[i] == l_e[j]:
					l_e[j]['status']='on_edge'
			l_c[i]['status']='on_cloud'
			l_e.append(l_c[i])
		return l_e

	def download_model_request(self,fname):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if try_connect_and_send_msg(s, self.cloud_addr, md.GET_MODEL_REQ, fname):
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
	# es2 = EdgeServer((para.EDGE_SERVER_IP, 6980),
	#                  (para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT))
	# es.start()
	# time.sleep(5)
	# es.connect_and_upload_file(para.FILEPATH, es.cloud_addr)
	# # es2.connect_and_upload_file(para.FILEPATH2, es.cloud_addr)
	# l,l_size,l_mtime = es.listdir('../')
	print(es.get_model_list_request2())
	# es.download_model('modeloncloud')
	# print(es.get_model_list())




# es.download_model()
# es.get_cloud_status()
# es.start_training()
# es.stop_training()
# es.manage_local_models()
