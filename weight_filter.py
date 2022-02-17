#!/usr/bin/python3
# -*- coding: utf-8 -*-

weight_seq = [-1, 0, 1, 10, 10, 20, 50, 80, 79, 81,
              80, 82, 81, 99, 50, 56, 43, 45, 48, 40,
              35, 32, 31, 30, 2, 1, 0, 1, 0]
status_seq = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1,
              1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 1, 1, 1]
time_seq = [0, 0, 0, 300, 420, 635, 800, 960, 1100, 1120,
            1260, 1400, 1600, 1800, 2100, 2200, 2300, 2400, 2500, 3300,
            3400, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300]

print(len(weight_seq), len(status_seq), len(time_seq))

if __name__ == "__main__":
    # initial variables
    wt = weight_seq[0]
    t0 = time_seq[0]
    s = status_seq[0]
    W = 0
    T = 0
    stamp = 0
    is_stable = 1

    for i in range(1, len(weight_seq)):
        wt1 = weight_seq[i]  # get weight
        s = status_seq[i]  # get status
        T = time_seq[i]  # time stamp of receiving the message
        delta_w = wt1 - wt
        if abs(delta_w) > 5 and T - t0 < 1000:
            W += delta_w
            wt = wt1
            if s == 1:
                if is_stable == 1:
                    stamp = T
                print('normal weight changes: ', W, ' at ', stamp)
                is_stable = 1
                stamp = T
                W = 0
                t0 = T
            elif s == 0 and is_stable == 1:
                stamp = T
                is_stable = 0

        elif abs(delta_w) <= 5 and T - t0 < 1000:
            W += delta_w
            wt = wt1
            if s == 1:
                if is_stable == 1:
                    stamp = T
                t0 = T
                if abs(W) > 5:
                    print('normal weight changes: ', W, ' at ', stamp)
                    is_stable = 1
                    stamp = T
                    W = 0
            elif s == 0 and is_stable == 1:
                stamp = T
                is_stable = 0

        elif T - t0 >= 1000:  # keep unstable for over 1000ms, stop accumulating the delta weight
            W += delta_w
            if abs(W) > 5:
                is_stable = 1
                print('timeout weight changes: ', W, ' at ', stamp)
                stamp = T
                W = 0
                wt = wt1
                t0 = T
