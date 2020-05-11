import os
import logging
from lib.macro import recv_file

# 0-100
# data source node --> edge node
DSNODE_REGISTER = 1

# data source node <-- edge node


# 100-200
# data source node --> edge node


# data source node <-- edge node





# 200-300
# edge node --> cloud
SEND_DATA_REQ = 11
GET_MODEL_REQ = 21
GET_MODEL_LIST_REQ = 31
TRAIN_MODEL_REQ = 41
SEND_DATA = 4

# edge node <-- cloud
SEND_DATA_CFM = 12
GET_MODEL_LIST_CFM = 32
TRAIN_MODEL_CMF = 42
REJ = 14

def dump_send_data_req():
    pass
def load_send_data_req():
    pass




def deal_send_data_req(cloud_server,conn, msg):
    fhead = msg['v']
    fname = fhead['name']
    fsize = fhead['size']
    if cloud_server.recv_file_ok():
        # return cfm
        cloud_server.tlv_obj.add_obj(SEND_DATA_CFM, '')
        conn.send(cloud_server.tlv_obj.pop_buf())
        # receive file
        new_filename = os.path.join('cloud_server', fname)
        logging.info('Prepared to receive file! new filename:{0}, filesize:{1}'.format(new_filename, fsize))
        recv_file(socket=conn, filename=new_filename, filesize=fsize)
        logging.info('end receiving...')

    else:
        cloud_server.tlv_obj.add(SEND_DATA_REJ, '')
        conn.send(cloud_server.tlv_obj.pop_buf())


MSG_DIC = {
    SEND_DATA_REQ:[],
    SEND_DATA_CFM:[]

}