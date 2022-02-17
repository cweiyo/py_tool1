# -*- coding: utf-8 -*-

from aug.ImageProcess import ImageAug
import PIL.Image as Image
import os
import glob
import numpy as np
import time

if __name__ == "__main__":
    outfile = '/home/liusiwei/门口facedoor/iphone负样本/aug'
    im = Image.open('/home/liusiwei/门口facedoor/iphone负样本/ir_face_03.jpg')
    ad = ImageAug()

    new_im = ad.img_resize(im, (50, 50))
    new_im.save(os.path.join(outfile, 'resize001.jpg'))

    new_im = ad.img_crop(im)
    new_im.save(os.path.join(outfile, 'crop001.jpg'))

    epoch_num = 10
    for ep in range(epoch_num):
        for fi in glob.glob('/home/liusiwei/门口facedoor/iphone负样本/' + '*.jpg'):
            ti = time.time()
            t = int(ti) * 1000
            t = int(round(ti * 1000)) - t
            time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            time_str = "{0}_{1}".format(time_str, t)
            im = Image.open(fi)
            new_im = ad.img_crop(im)
            new_im.save(os.path.join(outfile, 'crop0_{}.jpg'.format(time_str)))



    print("hello world")

