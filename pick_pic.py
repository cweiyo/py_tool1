#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#按标签移动到某个位置，用于观察百度的遮挡标准
import json
import os
import numpy as np
import shutil
import re

path_ori = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/JD/Train/eye_standard/occ/'
path_dest = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/JD/Train/eye_standard/no_glasses_occ/'

def run():
    file_ls = os.listdir(path_ori)
    regtxt = r'.+?\.txt'
    txtre = re.compile(regtxt)
    sample_list = []
    for fi in file_ls:
        istxt = re.findall(txtre, fi)
        if istxt:
            sample_list.append(fi.split('.')[0])

    for fi in sample_list:
        f = open(os.path.join(path_ori, fi+'.txt'))
        label_str = f.readline()
        f.close()
        labels = label_str.split(',')
        label_occlusions = labels[-2].split(' ')
        glasses_type = label_occlusions[0]
        if glasses_type == 'none':
            os.system('mv ' + path_ori+fi+'* ' + path_dest)







if __name__ == '__main__':
    run()