import os
# edge node server port
EDGE_SERVER_IP = '127.0.0.1'
EDGE_SERVER_PORT = 5025

CLOUD_SERVER_IP = '127.0.0.1'
CLOUD_SERVER_PORT = 5027
CLOUD_FILE_SERVER_PORT = 5029
BASEDIR = 'C:\\Users\\ezhayuc\\Desktop\\repo\\whostheme\\machine-learning-on-edge'
FILEPATH = os.path.join(BASEDIR,
                        'test','data_source_node',
                        'ai_challenger_wf2018_testb1_20180829-20181028.nc')
EDGE_MODEL_SAVE_PATH =  os.path.join(BASEDIR,
                        'edge_src','data','model')
CLOUD_MODEL_SAVE_PATH =  os.path.join(BASEDIR,
                        'cloud_src','data','model')

T_EXT = 7
L_EXT = 7


#edge_node_status
EN_FALL_BEHIND = 0
EN_UP_TO_DATE = 1
