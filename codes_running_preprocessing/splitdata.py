# -*- coding: utf-8 -*-
"""splitData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/110wQRBmFQcP56GjvlcWaqIAvpcYq-PlF
"""

import os
import numpy as np
import cv2
import random

def get_file_paths(base_dir):

  everything_in_folder = os.listdir(base_dir)
  all_files = map(lambda x: os.path.join(base_dir,x), everything_in_folder)
  file_list = list(filter(os.path.isfile, all_files))

  return file_list

def get_save_file(dst, capture):

  if not os.path.exists(dst):
      os.mkdir(dst)

  return os.path.join(dst, capture)

cd /content/drive/MyDrive/MinneApple

!mkdir dataset

cd dataset/

!mkdir train

ls

!mkdir test

cd /content/drive/MyDrive/MinneApple/dataset/test

cd /content/drive/MyDrive/MinneApple/dataset/train

!mkdir images

!mkdir masks

cd /content/drive/MyDrive/MinneApple/dataset/test

!mkdir images

!mkdir masks

cd /content/drive/MyDrive/MinneApple/dataset

!mkdir prediction

cd /content/drive/MyDrive/MinneApple/dataset/prediction

!mkdir images

!mkdir masks

def genetation_train_val_test():

    scr_imgs_dir = '/content/drive/MyDrive/dataset/images'
    scr_masks_dir = '/content/drive/MyDrive/dataset/masks'

    dst_test_imgs_dir = '/content/drive/MyDrive/MinneApple/dataset1/test/images'
    dst_test_masks_dir = '/content/drive/MyDrive/MinneApple/dataset1/test/masks'

    dst_train_imgs_dir = '/content/drive/MyDrive/MinneApple/dataset1/train/images'
    dst_train_masks_dir = '/content/drive/MyDrive/MinneApple/dataset1/train/masks'

    dst_pre_imgs_dir = '/content/drive/MyDrive/MinneApple/dataset1/prediction/ref/images'
    dst_pre_masks_dir = '/content/drive/MyDrive/MinneApple/dataset1/prediction/ref/masks'

    trainval_percent = 0.3
    train_percent = 0.9


    scr_data_path = get_file_paths(scr_imgs_dir)

    num = len(scr_data_path)
    list = range(num)

    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)

    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    print("train and val size", tv)
    print("train size", tr)

    for i in list:

      file = scr_data_path[i]
      img_name = file.split('/')[-1].split('.')[0]
      img = cv2.imread(file)
      mask = cv2.imread(os.path.join(scr_masks_dir, img_name + '.png'))
      dst_img_name = '%06d' % (i + 1)
      print(img_name)
      print(dst_img_name)
      if i in trainval:

        if i in train:
          
          cv2.imwrite(os.path.join(dst_train_imgs_dir, dst_img_name + '.png'), img)
          cv2.imwrite(os.path.join(dst_train_masks_dir, dst_img_name + '.png'), mask)

        else:

          cv2.imwrite(os.path.join(dst_test_imgs_dir, dst_img_name + '.png'), img)
          cv2.imwrite(os.path.join(dst_test_masks_dir, dst_img_name + '.png'), mask)

      else:

          cv2.imwrite(os.path.join(dst_pre_imgs_dir, dst_img_name + '.png'), img)
          cv2.imwrite(os.path.join(dst_pre_masks_dir, dst_img_name + '.png'), mask)

cd /content/drive/MyDrive/dataset

!mkdir yolo

cd /content/drive/MyDrive/dataset/yolo

!mkdir images

!mkdir labels

genetation_train_val_test()





def box_and_num(label):

  n_apple = label.max()

  boxs = []
  for i in range(1, n_apple+1):

    pos = np.where(label[:,:,1] == i)
    pos = np.array([pos[0].tolist(), pos[1].tolist()])

    x_min = pos[1].min() / 719
    x_max = pos[1].max() / 719
    w = x_max - x_min
    x_c = (x_max + x_min) / 2

    y_min = pos[0].min() / 1279
    y_max = pos[0].max() / 1279
    h = y_max - y_min
    y_c = (y_max + y_min) / 2

       
      

    boxs.append([0.00, x_c, y_c, w, h])
  

  return boxs

def genetation_yolo_data():

    scr_imgs_dir = '/content/drive/MyDrive/dataset/images'
    scr_masks_dir = '/content/drive/MyDrive/dataset/masks'
    
    
    # dst_test_imgs_dir = '/content/drive/MyDrive/MinneApple/dataset/test/images'
    # dst_test_masks_dir = '/content/drive/MyDrive/MinneApple/dataset/test/masks'

    dst_train_imgs_dir = '/content/drive/MyDrive/dataset/yolo/images'
    dst_train_labels_dir = '/content/drive/MyDrive/dataset/yolo/labels'

    # dst_pre_imgs_dir = '/content/drive/MyDrive/MinneApple/dataset/prediction/images'
    # dst_pre_masks_dir = '/content/drive/MyDrive/MinneApple/dataset/prediction/masks'

    # trainval_percent = 0.86
    # train_percent = 0.9


    scr_data_path = get_file_paths(scr_imgs_dir)

    num = len(scr_data_path)
    list = range(num)

    # tv = int(num * trainval_percent)
    # tr = int(tv * train_percent)

    # trainval = random.sample(list, tv)
    # train = random.sample(trainval, tr)

    # print("train and val size", tv)
    # print("train size", tr)

    for i in list:

      file = scr_data_path[i]
      img_name = file.split('/')[-1].split('.')[0]
      img = cv2.imread(file)
      mask = cv2.imread(os.path.join(scr_masks_dir, img_name + '.png'))
      dst_img_name = '%06d' % (i + 1)
      print(img_name)
      print(dst_img_name)
      cv2.imwrite(os.path.join(dst_train_imgs_dir, dst_img_name + '.png'), img)
      boxes = box_and_num(mask)
      
      np.savetxt(os.path.join(dst_train_labels_dir, dst_img_name + '.txt'), boxes)
      # if i in trainval:

      #   if i in train:
          
      #     cv2.imwrite(os.path.join(dst_train_imgs_dir, dst_img_name + '.png'), img)
      #     cv2.imwrite(os.path.join(dst_train_masks_dir, dst_img_name + '.png'), mask)

      #   else:

      #     cv2.imwrite(os.path.join(dst_test_imgs_dir, dst_img_name + '.png'), img)
      #     cv2.imwrite(os.path.join(dst_test_masks_dir, dst_img_name + '.png'), mask)

      # else:

      #     cv2.imwrite(os.path.join(dst_pre_imgs_dir, dst_img_name + '.png'), img)
      #     cv2.imwrite(os.path.join(dst_pre_masks_dir, dst_img_name + '.png'), mask)

genetation_yolo_data()

