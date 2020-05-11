from edge_src import app
from flask import render_template, request, make_response, send_from_directory
import os


@app.route('/')
def hello():
	return render_template('hello.html')

@app.route('/test')
def test():
	return render_template('test.html')


@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
	if request.method == "GET":
		if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
			return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
		pass


# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
	file_dir = os.path.join(app.config['BASEDIR'], app.config['UPLOAD_FOLDER'])
	if request.method == 'GET':
		if filename is None:
			pass
		else:
			# 读入图像数据
			# python的open方法，参数主要是文件路径和打开模式，返回一个file对象
			# file对象的read(size)方法，若不给出size，则默认读入整个文件
			image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
			# 读入的字节数据，放入response中，并设置Content-Type为图片，这样返回给浏览器时浏览器便能够解析显示。
			response = make_response(image_data)
			response.headers['Content-Type'] = 'image/png'
			return response
	else:
		pass