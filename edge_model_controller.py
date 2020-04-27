# coding=utf-8
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hey')
def hey():
    return 'hey!'



# EdgeModelManager【数据结构】
# 当前模型版本号（列表第一个）
# 过往模型列表：版本号，日期，大小，路径（或 “重新下载”按钮）
# 是否是最新模型

#Para:要识别的图片
#Action:调转模型app代码，得到识别结果
#Result:返回识别结果
@app.route('/model/run')
def run_model():
	pass

# TODO
'''
#Action:要求云服务器训练最新模型，云服务器动作：检查是否有新一批数据，若有，则进行训练，新
#Result:云服务器返回已开始训练或无法开始训练
'''
@app.route('/model/train_new')
def train_new():
	pass


# TODO
@app.route('/model/check_for_new')
def check_for_new_model():
	#边缘服务器向云服务器发消息，内容为当前版本号
	# # 云服务器核对版本号，如果和最新一致，则返回pos；如果落后，则返回neg；
	# 边缘服务器检验来自云服务器的回复，如果pos，则返回pos，前端显示√最新模型
	# 如果neg，则返回neg，前端显示落后…个版本，是否更新？
    return 'hey!'
# TODO
@app.route('/model/ask_for_new')
# 边缘服务器向云服务器发消息，内容为更新请求，等待云服务器的upload_data请求
def check_for_new_model():
	pass

# TODO
@app.route('/model/ask_for_model')
# 边缘服务器向云服务器发消息，内容为更新请求，等待云服务器的upload_data请求
def check_for_model():
	pass
