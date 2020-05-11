#coding:utf-8
import tensorflow as tf
from PIL import Image
import os
import random
import pandas as pd
import numpy as np
import fer2013.fer_config as config
#将训练集和测试集分开
def devide_train_data():
    data = pd.read_csv(config.data_path)
    images = data["pixels"]
    labels = data["emotion"]
    usages = data["Usage"]
    img_train=[]
    img_valid = []
    img_test=[]
    label_train=[]
    label_valid = []
    label_test=[]
    for i in range(len(images)):
        # 训练集
        if usages[i]=="Training":
            img_train.append(images[i])
            label_train.append(labels[i])
        # 验证集
        elif usages[i]=="PrivateTest":
            img_valid.append(images[i])
            label_valid.append(labels[i])
        # 测试集
        else:
            img_test.append(images[i])
            label_test.append(labels[i])
    data_train=pd.DataFrame(data={"pixels":img_train,"emotion":label_train},
                           columns=["pixels","emotion"])
    data_valid = pd.DataFrame(data={"pixels": img_valid, "emotion": label_valid},
                              columns=["pixels", "emotion"])
    data_test=pd.DataFrame(data={"pixels":img_test,"emotion":label_test},
                           columns=["pixels","emotion"])
    # 存入CSV文件
    data_train.to_csv(config.train_data_path, encoding="utf_8_sig", index=False)
    data_valid.to_csv(config.valid_data_path, encoding="utf_8_sig", index=False)
    data_test.to_csv(config.test_data_path, encoding="utf_8_sig", index=False)

# 生成图片和label文件
def generate_images_and_labels():
    images_train, labels_train=read_data(config.train_data_path)
    images_valid, labels_valid = read_data(config.valid_data_path)
    images_test, labels_test = read_data(config.test_data_path)

    def generate(images,labels,images_path,lables_path):
        with open(lables_path, 'w', encoding="utf-8") as f:
            for i in range(len(images)):
                # 转为灰度图
                image = Image.fromarray(np.reshape(images[i], (config.img_width, config.img_height))).convert('L')
                img_path = str(i) + "_" + str(labels[i]) + '.png'
                # 存储图片
                image.save(images_path + img_path)
                # 写入label文件
                f.write(img_path + " " + str(labels[i]))
                f.write("\n")
                print('the number of picture saved:', i)
        f.close()


    generate(images_train,labels_train,config.image_train_path,config.label_train_path)
    print("end generating train_images")

    generate(images_valid, labels_valid, config.image_valid_path, config.label_valid_path)
    print("end generating valid_images")

    generate(images_test, labels_test, config.image_test_path, config.label_test_path)
    print("end generating test_images")

# 读取CSV文件中数据
def read_data(path):
    data = pd.read_csv(path)
    images=[np.array(p.split(" "),dtype=int) for p in data["pixels"]]
    print(len(images[0]))
    labels=data["emotion"]
    return images,labels

# 写入tfRecord文件
def write_tfRecord(tfRecordName, image_path, label_path):
    #### 【1】读出数行，打乱行序，contents是打乱行序之后的数据
    # 得到一个TFRecordWriter
    writer = tf.python_io.TFRecordWriter(tfRecordName)
    num_pic = 0
    f = open(label_path, 'r')
    contents = f.readlines()
    # 打乱数据
    random.shuffle(contents)
    f.close()
    for content in contents:
        #### 【2】从每一行中获得图片路径和标签值，读取文件得到对应图片字节数据img_raw,转换标签值得到标签向量labels
        value = content.split()
        img_path = image_path + value[0]
        img = Image.open(img_path).convert("L")
        img_raw = img.tobytes()
        labels = [0] * 7#[0,0,0,0,0,0,0]
        labels[int(value[1])] = 1
        #### 【3】以img_raw和labels生成一个tf.train.Example实例，并将它写入指定路径的TFRecord
        example = tf.train.Example(
            features=tf.train.Features(feature={
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=labels))
            }))
        writer.write(example.SerializeToString())
        num_pic += 1
        print('the number of picture:', num_pic)
    writer.close()
    print('write tfrecord successful')
# 生成tfRecord文件
def generate_tfRecord():
    isExists = os.path.exists(config.data_file)
    if not isExists:
        os.makedirs(config.data_file)
        print('The directory was created successfully')
    else:
        print('directory already exists')
    write_tfRecord(config.tfRecord_train, config.image_train_path, config.label_train_path)
    write_tfRecord(config.tfRecord_valid, config.image_valid_path, config.label_valid_path)
    write_tfRecord(config.tfRecord_test, config.image_test_path, config.label_test_path)
# 读取tfRecord文件
def read_tfRecord(tfRecord_path):
    filename_queue = tf.train.string_input_producer([tfRecord_path])
    reader = tf.TFRecordReader()
    _,serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label':tf.FixedLenFeature([7],tf.int64),
                                           'img_raw':tf.FixedLenFeature([],tf.string)
                                                 })
    img = tf.decode_raw(features['img_raw'],tf.uint8)
    img.set_shape([config.img_height * config.img_height])

    img = tf.cast(img,tf.float32)*(1./255)
    label = tf.cast(features['label'],tf.float32)
    return img,label


# 批量读取数据【数据取用】输入batch_size，tfRecord_path来取用一定量的数据
def get_tfrecord(num, tfRecord_path):
    img,label=read_tfRecord(tfRecord_path)
    img_batch,label_batch = tf.train.shuffle_batch([img,label],
                                                   batch_size =num,
                                                   num_threads=2,
                                                   capacity=10000,
                                                   min_after_dequeue=5000)
    return img_batch,label_batch

##【数据生成】
def main():
    #第一步，将fer2013.csv按照标签分割成fer2013_train.csv / fer2013_valid.csv / fer2013_test.csv存入文件系统
    devide_train_data()
    #第二步，再读入上述的三个文件，读出其图片列[]和标签列[]
    # 图片，按照'编号_标签值' 的格式命名后存入指定路径       fer2013/train/???.png
    # 标签，按照‘图片路径 标签值’的格式一行一行写入指定文件  fer2013/labels_train.txt
    generate_images_and_labels()
    #第三步，再根据标签文件，一个个打开读取图片字节数据raw_img，生成标签向量，将这两个东西生成tf.Example，
    # 写入预先规定路径TFRecord中
    generate_tfRecord()

if __name__ == '__main__':
    main()






