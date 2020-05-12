from edge_src import app,edge_server
import logging
from flask import render_template, jsonify, request, make_response, send_from_directory
import os
from edge_src.util import *

import pandas as pd
import numpy as np
# 读取CSV文件中数据
def read_data(path):
    data = pd.read_csv(path)
    images=[np.array(p.split(" "),dtype=int) for p in data["pixels"]]
    print(len(images[0]))
    labels=data["emotion"]
    return images,labels

import csv
from PIL import Image
import numpy as np


def get_img_str(img_path):
	img_shape = app.config['IMG_SHAPE']
	pixels_num = img_shape[0]*img_shape[1]
	img = Image.open(img_path).convert('L').resize(img_shape)
	img_array_1d = np.array(img).reshape(pixels_num)
	img_list_int = img_array_1d.tolist()
	img_list_str = [str(i) for i in img_list_int]
	img_str = " ".join(img_list_str)
	return img_str


def append_csv(csv_path,img_str,label):
	df = pd.DataFrame(data={"pixels": [img_str], "emotion": [label]},
	                  columns=["pixels", "emotion"])
	df.to_csv(csv_path,mode='a',header=False)

def listdir(dirpath,rdb=None):
	l=[]
	for root,dirs,files in os.walk(dirpath):
		for f in files:
			if rdb and os.path.splitext(f)[1].upper()!=rdb.upper():
				continue
			l.append(f)
	return l


@app.route('/data')
def data_page():
	return render_template('data.html')

@app.route('/data2')
def data_page2():
	edge_server.listdir(app.config['DATASET_COLLECTING_FOLDER'])
	l = listdir(app.config['DATASET_COLLECTING_FOLDER'])
	print(l)
	return render_template('data.html', table_col_list=[l])


'''
标注数据 
input:服务器上某图片id&正确标签
action:打开csv文件，写入新行，关闭csv文件
return:
'''


@app.route('/data/mark', methods=['POST'], strict_slashes=False)
def mark_data():  # TODO
	csv_path = os.path.join(app.config['DATASET_COLLECTING_FOLDER'],
	                        app.config['DATASET_COLLECTING_CSV'])
	form = request.values
	img_path = form.get("path")
	label = form.get("label")
	logging.info(img_path,label)
	img_str = get_img_str(img_path)
	logging.debug(img_str)
	append_csv(csv_path, img_str, label)
	ans = 'OK'  # ans = fer_app.run_app(filename)
	return ans


'''
请求数据集列表
input:
action:搜索目录下的文件，返回列表 json？
return:数据集目录下的文件
'''
@app.route('/data/list', methods=['GET','POST'], strict_slashes=False)
def get_dataset_csvlist():
	f_list = edge_server.get_data_list_request()
	print(f_list)
	return jsonify(f_list)

'''
由边缘端向云上传数据集
input:服务器上某csv文件id
action:将该csv文件转换成tfrecord，开启后台上传文件进程
return:
'''


@app.route('/data/upload_to_cloud', methods=['GET','POST'], strict_slashes=False)
def upload_data():  # TODO
	form = request.values
	f_name = form.get("fname")
	print(f_name)
	f_path = os.path.join(app.config['DATASET_COLLECTING_FOLDER'], f_name)
	print(f_path)
	ans = edge_server.connect_and_upload_file(f_path, edge_server.cloud_addr)  # ans = fer_app.run_app(filename)
	return ans

'''
由用户端向边缘端上传数据集
input:服务器上某csv文件id
action:将该csv文件转换成tfrecord，开启后台上传文件进程
return:
'''