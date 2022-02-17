# -*- coding: utf-8 -*-

import numpy as np
import os
import time
import logging
import copy

# Logging等级设置为INFO
logging.basicConfig(level=logging.INFO, filename='new.log',
                    filemode='w+', format='%(asctime)s %(levelname)s: %(message)s')
# CRITICAL > ERROR > WARNING > INFO > DEBUG

N = 5
groups = [None] * 5

#第row行，Q的排列情况
def dp(row):

    if row == 1:
        groups[row - 1] = [[i] for i in range(N)]
        return [[i] for i in range(N)]
    new_q_list = []
    if not groups[row - 1] is None:
        Q_list = groups[row - 1]
    else:
        Q_list = dp(row - 1)
    for col in range(N):
        for Q in Q_list:
            if not validate(Q, col):
                continue
            q = Q.copy()
            q.append(col)
            new_q_list.append(q)

    groups[row-1] = new_q_list
    return new_q_list

def validate(queue, new_col):
    for i in range(1, len(queue)+1):
        if new_col == queue[-i] or queue[-i] == new_col-i or queue[-i] == new_col+i:
            return False
    return True

start = time.time()
dp(5)
print(time.time()-start)
print(groups[4])