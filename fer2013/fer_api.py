#coding:utf-8
#python 3.5

import tensorflow as tf
import numpy as np
from PIL import Image
import fer2013.fer_forward as fw
import fer2013.fer_backward as bk
import fer2013.fer_app as app
import fer2013.fer_config as config

# predic one picture
def run_app(pic_path):
    testPicArr=app.pre_pic(pic_path)
    preValue=app.restore_model(testPicArr)
    print("The prediction class is: %s"%app.classes[preValue[0]])
    return app.classes[preValue[0]]

def train_model():
	#配置：1新模型名称config.MODEL_SAVE_PATH, config.MODEL_NAME
	#配置：2新数据集路径BATCH_SIZE,config.tfRecord_train
	#配置：3训练步数和BATCHSIZE
	#开始训练
	new_tfr = ''
	bk.backward(tfrecord_path=new_tfr,step_num=1000)
	#更新：最新模型名称，模型名称列表

def get_model_path():
	#找到：最新模型路径=模型保存路径+最新模型名称
	pass