# -*- coding:utf-8 -*-

import cv2

img = cv2.imread('/home/liusiwei/Downloads/rgbir/ir/20211207_142424_024.ir.png')

if __name__ == '__main__':
    cv2.namedWindow("img")
    # cv2.setMouseCallback("img", mouse_click)
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey() == ord(' '):
            break
    cv2.destroyAllWindows()