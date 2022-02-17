#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import numpy as np
import shutil
import math
import cv2


'''
'bbox_x', 'bbox_y', 'bbox_w', 'bbox_h',
'eye_x1', 'eye_y1', 'eye_x2', 'eye_y2',
'occ_x', 'occ_y', 'occ_w', 'occ_h',
'occ_type', 'occ_degree', 'gender', 'race', 'orientation',
'glasses_x', 'glasses_y', 'glasses_w', 'glasses_h'


'common_mask', 'complex_mask', 'prof_mask', 'body or hand', 'common_glasses', 'color_glasses', 'other',
'left_eye', 'right_eye', 'nose', 'mouth', 'chin', 'left_cheek', 'right_cheek',
'illumination', 'blur', 'completeness'

'rotation'

'''

label_name = ['bbox_x', 'bbox_y', 'bbox_w', 'bbox_h',
              'face_type', 'occ_x', 'occ_y', 'occ_w', 'occ_h',
              'occ_type', 'occ_degree', 'gender', 'race', 'orientation',
              'glasses_x', 'glasses_y', 'glasses_w', 'glasses_h']

label_name_train = ['bbox_x', 'bbox_y', 'bbox_w', 'bbox_h',
                    'eye_x1', 'eye_y1', 'eye_x2', 'eye_y2',
                    'occ_x', 'occ_y', 'occ_w', 'occ_h',
                    'occ_type', 'occ_degree', 'gender', 'race', 'orientation',
                    'glasses_x', 'glasses_y', 'glasses_w', 'glasses_h']

multi_label_key = ['common_mask', 'complex_mask', 'prof_mask', 'body or hand', 'common_glasses', 'color_glasses', 'other',
               'left_eye', 'right_eye', 'nose', 'mouth', 'chin', 'left_cheek', 'right_cheek',
               'illumination', 'blur', 'completeness']

'''
the format is stored in a 18d array (x,y,w,h,face_type,x1,y1,w1,h1, occ_type, occ_degree, gender, race, orientation, x2,y2,w2,h2),  where              
(a) (x,y,w,h) is the bounding box of a face, 
(b) face_type stands for the face type and has: 1 for masked face, 2 for unmasked face and 3 for invalid face.
(c) (x1,y1,w1,h1) is the bounding box of the occluder. Note that (x1,y1) is related to the face bounding box position (x,y)
(d) occ_type stands for the occluder type and has: 1 for simple, 2 for complex and 3 for human body.
(e) occ_degree stands for the number of occluded face parts
(f) gender and race stand for the gender and race of one face
(g) orientation stands for the face orientation/pose, and has: 1-left, 2-left frontal, 3-frontal, 4-right frontal, 5-right
(h) (x2,y2,w2,h2) is the bounding box of the glasses and is set to (-1,-1,-1,-1) when no glasses.  Note that (x2,y2) is related to the face bounding box position (x,y)

the format is stored in a 18d array (x,y,w,h, x1,y1,x2,y2, x3,y3,w3,h3, occ_type, occ_degree, gender, race, orientation, x4,y4,w4,h4),  where        
    (a) (x,y,w,h) is the bounding box of a face, 
    (b) (x1,y1,x2,y2) is the position of two eyes.
    (c) (x3,y3,w3,h3) is the bounding box of the occluder. Note that (x3,y3) is related to the face bounding box position (x,y)
    (d) occ_type stands for the occluder type and has: 1 for simple, 2 for complex and 3 for human body.
    (e) occ_degree stands for the number of occluded face parts
    (f) gender and race stand for the gender and race of one face
    (g) orientation stands for the face orientation/pose, and has: 1-left, 2-left frontal, 3-frontal, 4-right frontal, 5-right
    (h) (x4,y4,w4,h4) is the bounding box of the glasses and is set to (-1,-1,-1,-1) when no glasses.  Note that (x4,y4) is related to the face bounding box position (x,y)

'''

#label transfer dict
race_dict = {'yellow' : '2', 'white' : '1', 'black':'3', 'arabs':'4'}
gender_dict = {'male':'1', 'female':'2'}

select_list_path = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/hand/hand.txt'
img_crop_path = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/hand/picture_crop/'
face_bbox_path = '/abc/'
json_path = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/hand/json/'
img_path = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/hand/hand/'

draw_path = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/hand/draw/'
target_path = '/media/zhihua/34760B0B760ACD94/人脸检测数据集/papa人脸数据/hand/comma_label/'

def draw_bbox(left, top, width, height, rotation, img):
    left = int(left)
    top = int(top)
    width = int(width)
    height = int(height)

    Theta = rotation / 57.3

    X0 = int(left)
    Y0 = int(top)

    X1 = int(left) + int(width)
    X1 = X1 if X1 < img.shape[1] else (img.shape[1] - 1)
    Y1 = int(top) + int(height)
    Y1 = Y1 if Y1 < img.shape[0] else (img.shape[0] - 1)
    A = (X0, Y0)
    B = (X1, Y0)
    C = (X1, Y1)
    D = (X0, Y1)

    # cv2.line(img, A, B, (0, 255, 255), 2)
    # cv2.line(img, B, C, (0, 255, 255), 2)
    # cv2.line(img, C, D, (0, 255, 255), 2)
    # cv2.line(img, D, A, (0, 255, 255), 2)

    #=================================================
    A = (int(left), int(top))
    B = (int(left) + int(width * math.cos(Theta)),
         int(top) + int(width * math.sin(Theta)))
    AC_Len = math.sqrt(width ** 2 + height ** 2)
    AC_Theta = math.atan(height / width) + rotation / 57.3  ####或者是？？？
    C = (int(left) + int(AC_Len * math.cos(AC_Theta)), int(top) + int(AC_Len * math.sin(AC_Theta)))
    D = (int(left) - int(height * math.sin(Theta)),
         int(top) + int(height * math.cos(Theta)))
    # cv2.line(img, A, B, (0, 0, 255), 2)
    # cv2.line(img, B, C, (0, 0, 255), 2)
    # cv2.line(img, C, D, (0, 0, 255), 2)
    # cv2.line(img, D, A, (0, 0, 255), 2)

    #==================================================
    X0 = min([A[0], B[0], C[0], D[0]])
    X0 = X0 if X0 > 0 else 0
    Y0 = min([A[1], B[1], C[1], D[1]])
    Y0 = Y0 if Y0 > 0 else 0
    X1 = max([A[0], B[0], C[0], D[0]])
    X1 = X1 if X1 < img.shape[1] else (img.shape[1] - 1)
    Y1 = max([A[1], B[1], C[1], D[1]])
    Y1 = Y1 if Y1 < img.shape[0] else (img.shape[0] - 1)

    A = (X0, Y0)
    B = (X1, Y0)
    C = (X1, Y1)
    D = (X0, Y1)

    cv2.line(img, A, B, (255, 0, 255), 2)
    cv2.line(img, B, C, (255, 0, 255), 2)
    cv2.line(img, C, D, (255, 0, 255), 2)
    cv2.line(img, D, A, (255, 0, 255), 2)

    return A + C, img


def run():
    selected_ls = np.loadtxt(select_list_path, dtype=str)

    for fi in selected_ls:
        img = img_path + fi + '.jpg'
        baidu_json = json_path + fi + '.json'
        bbox_rect = face_bbox_path + fi + '.rect'
        print(fi)
        
        with open(baidu_json, 'r') as json_file:
            data = json.load(json_file)

        num = data['face_num']  # 这里都是1？
        if not num == 1:
            continue
        content = data['face_list'][0]

        im = cv2.imread(img)
        if os.path.exists(bbox_rect):
            with open(bbox_rect, 'r') as rect_fi:
                data = rect_fi.readline()

            rect = data.split(' ')
            rect = list(map(int, rect))

            bbox, im = draw_bbox(rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1], 0, im)

        else:
            location = content['location']
            bbox, im = draw_bbox(int(location['left']),  int(location['top']), int(location['width']), int(location['height']), float(location['rotation']), im)

        cv2.imwrite(draw_path + fi + '.jpg', im)
        
        
        
        comma_label = {}
        comma_label['bbox_x'] = bbox[0]
        comma_label['bbox_y'] = bbox[1]
        comma_label['bbox_w'] = bbox[2] - bbox[0]
        comma_label['bbox_h'] = bbox[3] - bbox[1]
        comma_label['rotation'] = 361

        comma_label['gender'] = gender_dict[content['gender']['type']]
        comma_label['race'] = race_dict[content['race']['type']]

        comma_label['left_eye'] = float(content['quality']['occlusion']['left_eye'])
        comma_label['right_eye'] = float(content['quality']['occlusion']['right_eye'])
        comma_label['nose'] = float(content['quality']['occlusion']['nose'])
        comma_label['mouth'] = float(content['quality']['occlusion']['mouth'])
        comma_label['chin'] = float(content['quality']['occlusion']['chin_contour'])
        comma_label['left_cheek'] = float(content['quality']['occlusion']['left_cheek'])
        comma_label['right_cheek'] = float(content['quality']['occlusion']['right_cheek'])
        comma_label['illumination'] = float(content['quality']['illumination'])
        comma_label['blur'] = float(content['quality']['blur'])
        comma_label['completeness'] = float(content['quality']['completeness'])

        comma_label['common_mask'] = 0.0
        comma_label['complex_mask'] = 0.0
        comma_label['prof_mask'] = 0.0
        comma_label['body or hand'] = 1.0
        comma_label['other'] = 0.0

        comma_label['orientation'] = '0'

        if content['angle']['yaw'] > 45:
            comma_label['orientation'] = '1'
        elif content['angle']['yaw'] > 20 and content['angle']['yaw'] <= 45:
            comma_label['orientation'] = '2'
        elif abs(content['angle']['yaw']) <=20:
            comma_label['orientation'] = '3'
        elif content['angle']['yaw'] < -20 and content['angle']['yaw'] >= -45:
            comma_label['orientation'] = '4'
        elif content['angle']['yaw'] < -45:
            comma_label['orientation'] = '5'

        if content['glasses']['type'] == 'common':
            comma_label['common_glasses'] = 1.0
        elif content['glasses']['type'] == 'sun':
            comma_label['color_glasses'] = 1.0
        elif content['glasses']['type'] == 'none':
            comma_label['common_glasses'] = 0.0
            comma_label['color_glasses'] = 0.0
        else:
            comma_label['common_glasses'] = 1.0


        face_list = []
        face_list.append(comma_label)

        comma_json = {'face_num':1, 'face_list':face_list}

        with open(target_path + fi + '_comma.json', 'w') as json_file:
            json.dump(comma_json, json_file)

        
        


    # for im in ls:
    #     sample_name = im.split('.')[0]
    #     if not os.path.exists(json_path + '/' + sample_name+'.json'):
    #         continue
    #     with open(json_path + '/' + sample_name+'.json') as json_file:
    #         data = json.load(json_file)
    #     face_prob = data['face_list'][0]['face_probability']
    #     # if face_prob < 0.85:
    #     #     continue
    #     f = open(os.path.join(label_path, sample_name + '.txt'))
    #     label_str = f.readline()
    #     labels = label_str.split(',')
    #     label_occlusions = labels[-2].split(' ')
    #     label_righteye = float(label_occlusions[2])
    #     label_lefteye = float(label_occlusions[1])
    #     label_righteye = float(label_occlusions[7])
    #     label_lefteye = float(label_occlusions[6])
    #     print(label_lefteye, label_righteye)
    #     f.close()
    #     if label_lefteye > 0.1 or label_righteye > 0.1:
    #         shutil.copyfile(os.path.join(img_path, sample_name + '.jpg'), os.path.join(eye_path, sample_name + '.jpg'))
    #         shutil.copyfile(os.path.join(label_path, sample_name + '.txt'), os.path.join(eye_path, sample_name + '.txt'))
    #         shutil.copyfile(os.path.join(img_path, sample_name + '.jpg'), os.path.join(eye_path,
    #                                                                                    sample_name + '_' +
    #                                                                                    str(label_lefteye) + '_' +
    #                                                                                    str(label_righteye) + '.jpg'))
    #     else:
    #         shutil.copyfile(os.path.join(img_path, sample_name + '.jpg'), os.path.join(no_occl_eye_path, sample_name + '_' + str(label_lefteye) + '_' + str(label_righteye) + '.jpg'))
    #         shutil.copyfile(os.path.join(img_path, sample_name + '.jpg'), os.path.join(no_occl_eye_path, sample_name + '.jpg'))
    #         shutil.copyfile(os.path.join(label_path, sample_name + '.txt'), os.path.join(no_occl_eye_path, sample_name + '.txt'))

if __name__ == '__main__':
    run()