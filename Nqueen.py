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

board = []
result = []

def init_board(board, N):
    for i in range(N):
        board.append(['.'] * N)

def backtrack(row, board):
    N = len(board)
    if row == N:
        global result
        g = copy.deepcopy(board)
        result.append(g)
        return

    for col in range(N):
        if not validate(board, row, col):
            continue
        board[row][col] = 'Q'
        backtrack(row+1, board)
        board[row][col] = '.'


def validate(board, row, col):
    N = len(board)
    if row == 0:
        return True
    else:
        i = 1
        while row-i >= 0:
            if col + i < N and board[row-i][col+i] == 'Q':
                return False
            if col - i >= 0 and board[row-i][col-i] == 'Q':
                return False
            if board[row-i][col] == 'Q':
                return False
            i += 1
        return True

init_board(board, 10)
for row in board:
    logging.info('{}'.format(row))

start = time.time()
backtrack(0, board)
start = time.time() - start


for item in result:
    logging.info("---------------------------")
    for i in range(len(item)):
        logging.info(item[i])
    break

logging.info("elapse time: {}".format(start))
logging.info("count: {}".format(len(result)))