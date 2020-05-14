import os
import shutil
import logging


def cleardir(dirpath):
	try:
		shutil.rmtree(dirpath)  # 能删除该文件夹和文件夹下所有文件
		os.mkdir(dirpath)
	except PermissionError as e1:
		print(e1)
	except Exception as e:
		print('no such dirpath, create one ...')
		os.mkdir(dirpath)


import tensorflow as tf
import numpy as np
from PIL import Image
import cliquenet as fer_forward
import fer_config as config
import fer_generateds as fer_gen
import fer_backward_cliq as fer_backward

# 面部表情类别
classes = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}


class FER2013:
	def __init__(self):
		self.x = None
		self.y = None
		self.preValue = None
		self.sess = None

		self.t_progress = 0

	def __del__(self):
		if (self.sess):
			self.sess.close()

	def pre_data(self, picName):
		img = Image.open(picName)
		# 将图片大小转为config.img_width*config.img_height像素并做平滑处理
		reIm = img.resize((config.img_width, config.img_height), Image.ANTIALIAS)

		# 将图片转为灰度图并存为array
		im_arr = np.array(reIm.convert('L'))
		# 将config.img_width*config.img_height的array拉直
		nm_arr = im_arr.reshape([1, config.img_width * config.img_height])
		# nm_arr内数字类型转换为float32
		nm_arr = nm_arr.astype(np.float32)
		# nm_arr内数字除以255，转为0到1的浮点数
		img_ready = np.multiply(nm_arr, 1.0 / 255.0)
		# 转换成喂入所需形状
		img_ready = np.reshape(img_ready, (1,
		                                   config.img_width,
		                                   config.img_height,
		                                   config.NUM_CHANNELS))
		return img_ready

	def prepare_sess(self, tModel=''):
		if self.sess:
			sess.close()
		if tModel == '':
			ckpt = tf.train.get_checkpoint_state(config.MODEL_SAVE_PATH)
			# 如果模型存在
			if ckpt and ckpt.model_checkpoint_path:
				tModel = ckpt.model_checkpoint_path
		print('model path :' + tModel)
		if not os.path.isfile(tModel + '.index'):
			raise Exception("Wrong Model Path!")
			return

		# 【定义要存储的变量 define variable to save】
		# 输入x占位
		self.x = tf.placeholder(tf.float32, [1, config.img_width,
		                                     config.img_height, config.NUM_CHANNELS])
		# 获得输出y的前向传播计算图
		self.y = fer_forward.forward(self.x, False, None)
		# 定义预测值为y中最大值的索引号
		self.preValue = tf.argmax(self.y, 1)

		# 【创建保存模型的对象 在此之前必须定义好要存储的变量】
		# 定义滑动平均
		variable_averages = tf.train.ExponentialMovingAverage(config.MOVING_AVERAGE_DECAY)
		# 将影子变量直接映射到变量的本身
		variables_to_restore = variable_averages.variables_to_restore()
		# 创建一个保存模型的对象
		saver = tf.train.Saver(variables_to_restore)
		self.sess = tf.Session()
		saver.restore(self.sess, tModel)

	def sess_perform(self, datapath):
		input_x = self.pre_data(datapath)
		ans = self.sess.run(self.preValue, feed_dict={self.x: input_x})
		return [classes[label] for label in ans]

	def csv_to_tfrecord(self, csv_path, tfr_path=config.tfRecord_train):
		images_train, labels_train = fer_gen.read_data(csv_path)
		fer_gen.generate(images_train, labels_train, config.temporary_img_path, config.temporary_label_path)
		fer_gen.write_tfRecord(tfr_path, config.temporary_img_path, config.temporary_label_path)
		cleardir(config.temporary_img_path)
		os.remove(config.temporary_label_path)

	def incre_train(self, datapath, step_num=1000, save_interval=500):
		fer_backward.backward(tfr_path=datapath, steps=step_num)

	def train_progress(self):
		print(fer_backward.training_progress)

	def get_newest(self):
		# 通过checkpoint文件找到模型文件名
		ckpt = tf.train.get_checkpoint_state(config.MODEL_SAVE_PATH)
		# 如果模型存在
		if ckpt and ckpt.model_checkpoint_path:
			# 加载模型继续训练
			saver.restore(sess, ckpt.model_checkpoint_path)


api = FER2013()