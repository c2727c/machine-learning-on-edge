from edge_src import app,edge_server
from werkzeug.utils import secure_filename
from flask import render_template, jsonify, request, make_response, send_from_directory
import os
import logging
from edge_src.util import *
# from fer2013 import fer_api

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/model')
def model_page():
	return render_template('model.html',current_model = app.config['CURRENT_MODEL'])

'''
上传实时推断所需图片
'''


@app.route('/model/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
	# 定义服务器上的存储目录
	file_dir = os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER'])
	if not os.path.exists(file_dir):
		# 如果不存在，就创建
		os.makedirs(file_dir)
	# 从request中读取图片，request是一个flask提供的全局对象，通过它，来获取当前请求中的数据
	# files是request中的一个成员，是一个MultiDict object，其中有着当前请求中的所有的附件，通过key来取用
	# 文件的key是通过html模板中，<input type="file" name="">的标签设置的，通过该input“填写”的数据就会被保存到request对象的flies词典中
	f = request.files['photo']
	if f and allowed_file(f.filename):
		# 这里是生成一个新的文件名
		fname = secure_filename(f.filename)
		ext = fname.rsplit('.', 1)[1]
		new_filename = Pic_str().create_uuid() + '.' + ext
		# request的files列表中是 FileStorage 对象，它们会有一个save方法用于将文件保存到文件系统。
		# 如果进行标注的话，还需要打开标注文件进行标注
		new_filepath = os.path.join(file_dir, new_filename)
		f.save(new_filepath)
		return render_template('hello.html', show_img_url='/show/' + new_filename, show_img_path=new_filepath)

	else:
		return jsonify({"error": 1001, "msg": "上传失败"})


'''运行模型
input:服务器上某图片路径
action:预处理图片，新路径，调取接口
return:该图片预测结果
'''


@app.route('/model/run', methods=['POST'], strict_slashes=False)
def api_run_model():
	model_path = os.path.join(app.config['MODEL_FOLDER'],
	                        app.config['MODEL'])# FIXME
	form = request.values
	path = form.get("path")
	logging.debug("model/run:"+path)
	ans = fer_api.run_app(path)
	return ans


'''查询模型列表
input:
action:
1.向云服务器发出请求，查询云服务器上的模型
2.在本地配置的文件夹中搜索获取模型文件列表
3.比较两个列表，生成状态向量
return:[模型id，模型大小，生成时间，是否存在边缘]的列表
'''


@app.route('/model/list', methods=['GET','POST'], strict_slashes=False)
def get_model_list():
	f_list = edge_server.get_model_list_request2()
	print(f_list)
	return jsonify(f_list)



'''下载模型
input:模型id
action:
1.向云服务器发出请求，expect 一个DATA_SEND_REQ 然后 deal_data_send_req
return:
'''
@app.route('/model/download', methods=['GET','POST'], strict_slashes=False)
def download_model():
	model_fname = request.values.get('fname')
	edge_server.download_model_request(model_fname)
	return 'OK'


'''训练模型
input:服务器上某已上传云服务器的数据集id，训练step数
action:生成新模型该有的名称，传话给云服务器
云服务器算出数据集在本机路径，
调用训练模型接口，
传入数据集路径和step数，开始训练
return:成功+新模型id/失败
'''


@app.route('/model/train', methods=['POST'], strict_slashes=False)
def api_train_model():
	form = request.values
	dataset_name = form.get("item_id")
	steps = form.get("training_steps")
	batch_size = form.get("batch_size")
	train_from_scratch = form.get("from_scratch")
	# edge_server.train_model_request(dataset_name,steps,train_from_scratch)
	return "OK:{};{};{};{};".format(dataset_name,steps,batch_size,train_from_scratch)