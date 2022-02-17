#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import sys

def main():
    for i in range(5):
        rsid = "rs06"
        t0 = time.time()
        time.sleep(1)
        t1 = time.time()
        # print('%s-rgbd-->fps: %04f\n' % (rsid, 1.0 / (t1 - t0)))
        sys.stdout.write("stdout1\n")
        sys.stdout.write("stderr2\n")

if __name__ == '__main__':
    main()