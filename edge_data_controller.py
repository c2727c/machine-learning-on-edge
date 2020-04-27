# coding=utf-8
from flask import Flask
app = Flask(__name__)
'''
EDGE DATA SERVER
数据结构
训练批次

'''

# TODO
'''
Para:{图片，标注信息}列表
Action:数据预处理，存储到批次格式中，更新训练批次状态，检验训练批次状态
Result:返回ok（以及是否凑够新的训练批次）
此接口面向普通用户
'''
@app.route('/data/mark_data')
def mark_data():
	pass

# TODO
'''
Para:{图片，标注信息}列表
Action:数据预处理，存储到批次格式中，更新训练批次状态，检验训练批次状态
Result:返回ok（以及是否凑够新的训练批次）
此接口面向普通用户
'''
@app.route('/data/upload_data')
def mark_data():
	pass


# TODO
'''
Para:None
Action:检查新标注数据是否凑够一个训练批次
Result:返回是/否
此接口面向程序员
'''
@app.route('/data/check_train_batch')
def check_train_batch():
	pass