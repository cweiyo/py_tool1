import numpy as np
import os
import json

import shutil

import glob


jsonpath = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/人脸关键点框数据/yicheng/'
multifaces = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/人脸关键点框数据/duolian/'
hardface = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/人脸关键点框数据/nanlian/'

json_change = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/人脸关键点框数据/161/hardface/'

# for fi in os.listdir(jsonpath):
#     with open(os.path.join(jsonpath,fi), 'r') as json_file:
#         data = json.load(json_file)
#         for shape in data["shapes"]:
#             if shape["label"] == "difficult":
#                 shutil.move(os.path.join(jsonpath,fi), os.path.join(hardface,fi))

for fi in os.listdir(json_change):
    with open(os.path.join(json_change, fi), 'r') as json_file:
        data = json.load(json_file)
        data["imagePath"] = fi.split('.')[0] + '.jpg'
        data["imageData"] = None

    with open(os.path.join(json_change, fi), 'w+') as json_file:
        json.dump(data, json_file)
