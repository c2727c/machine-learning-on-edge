#coding:utf-8

#相关配置

image_train_path='/home/ubuntu/MyFiles/data/fer2013/train/'
label_train_path='/home/ubuntu/MyFiles/data/fer2013/labels_train.txt'
tfRecord_train='/home/ubuntu/MyFiles/data/fer2013/fer2013_train.tfrecords'
image_valid_path='/home/ubuntu/MyFiles/data/fer2013/valid/'
label_valid_path='/home/ubuntu/MyFiles/data/fer2013/labels_valid.txt'
tfRecord_valid='/home/ubuntu/MyFiles/data/fer2013/fer2013_valid.tfrecords'
image_test_path='/home/ubuntu/MyFiles/data/fer2013/test/'
label_test_path='/home/ubuntu/MyFiles/data/fer2013/labels_test.txt'
tfRecord_test='/home/ubuntu/MyFiles/data/fer2013/fer2013_test.tfrecords'

data_path='/home/ubuntu/MyFiles/data/fer2013/fer2013.csv'
train_data_path='/home/ubuntu/MyFiles/data/fer2013/fer2013_train.csv'
valid_data_path='/home/ubuntu/MyFiles/data/fer2013/fer2013_valid.csv'
test_data_path='/home/ubuntu/MyFiles/data/fer2013/fer2013_test.csv'


data_file='/home/ubuntu/MyFiles/data/fer2013'
#模型存储路径
MODEL_SAVE_PATH="/home/ubuntu/MyFiles/model/fer_cliquenet"
#模型名称
MODEL_NAME="fer_model"
#图片高
img_height=48
#图片宽
img_width=48

# forward cliq参数
NUM_CHANNELS=1
OUTPUT_NODE=7

# backward cliq 参数
BATCH_SIZE = 128
LEARNING_RATE_BASE = 0.0005
LEARNING_RATE_DECAY = 0.99
REGULARIZER = 1e-4
STEPS = 3000
MOVING_AVERAGE_DECAY = 0.99
train_num_examples=28709

# 临时参数
temporary_img_path = '/home/ubuntu/MyFiles/data/fer2013/temporary/image/'
temporary_label_path = '/home/ubuntu/MyFiles/data/fer2013/temporary/labels_tmp.txt'
