from edge_src.server.edge_node import EdgeServer
import conf.parameters as para
edge_server = EdgeServer((para.EDGE_SERVER_IP, para.EDGE_SERVER_PORT),
	                (para.CLOUD_SERVER_IP, para.CLOUD_SERVER_PORT))


from flask import Flask
import os
app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app.config['BASEDIR'] = BASEDIR
app.config['UPLOAD_FOLDER'] = os.path.join(BASEDIR,'data', 'upload-img')
app.config['DATASET_COLLECTING_FOLDER'] = os.path.join(BASEDIR,'data', 'dataset')
app.config['DATASET_COLLECTING_CSV'] = 'FER2013_NEW_DATASET.CSV'
app.config['MODEL_FOLDER'] = para.EDGE_MODEL_SAVE_PATH


app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'JPG', 'PNG'])
app.config['IMG_SHAPE'] = (48,48) #前行后列，前高后宽
from edge_src import route_data,route_hello,route_model


