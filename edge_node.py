from lib.TLV import *
import os
import logging

logging.basicConfig(level=logging.DEBUG)
import conf.parameters as para
from lib.net_device_base import NetDeviceBase

import conf.msg_dic as md

from lib.macro import *

class EdgeNode(NetDeviceBase):

	def __init__(self, server_addr, cloud_addr):
		NetDeviceBase.__init__(self, server_addr)
		self.cloud_addr = cloud_addr

	def deal_conn(self, conn):
		logging.debug('EdgeNode - deal conn ...')
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
			self.tlv_obj.add_obj(md.SEND_DATA_CFM, '')
			conn.send(self.tlv_obj.pop_buf())
			new_filename = os.path.join('test/edge_node', fname)
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
	es = EdgeNode((para.EDGE_SERVER_IP, para.EDGE_SERVER_PORT),
					(para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT))
	es2 = EdgeNode((para.EDGE_SERVER_IP, 6980),
	               (para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT))
	# es.start()
	# time.sleep(5)
	es.upload_file(para.FILEPATH, es.cloud_addr)
	es2.upload_file(para.FILEPATH2, es.cloud_addr)




# es.download_model()
# es.get_cloud_status()
# es.start_training()
# es.stop_training()
# es.manage_local_models()
