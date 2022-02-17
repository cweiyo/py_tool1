import numpy as np


class KM_Algorithm:
    def __init__(self, Net=None):
        # Net = [[3,4,6,4,9],[6,4,5,3,8],[7,5,3,4,2],[6,3,2,2,5],[8,4,5,4,7]]  #NGraphic net
        # self.Net = [[2,3,0,0],[0,4,4,0],[5,6,0,0],[0,0,7,0]]
        # Net = [[1,1,0,0],[0,1,1,0],[1,1,0,0],[0,0,1,0]]
        # Net = [[2,1,1],[3,2,1],[1,1,1]]
        if Net is None:
            # Net = [[3, 4, 6, 4, 9],
            #        [6, 4, 5, 3, 8],
            #        [7, 5, 3, 4, 2],
            #        [6, 3, 2, 2, 5],
            #        [8, 4, 5, 4, 7]]

            Net = [[3, 4, 6, 4],
                   [6, 4, 5, 3],
                   [7, 5, 3, 4],
                   [6, 3, 2, 2]]
        self.Net = Net
        self.Number = len(self.Net)
        self.ux, self.uy = np.zeros(self.Number, dtype=int), np.zeros(self.Number,
                                                                      dtype=int)  # variable for record path
        self.lx, self.ly = np.zeros(self.Number, dtype=int), np.zeros(self.Number, dtype=int)  # sign
        self.result = np.zeros(self.Number, dtype=int)  # Store the final result
        self.inc = 99999

    def match(self, u):

        #  global inc
        u = int(u)
        self.ux[u] = 1  # record node that was explored
        for v in range(self.Number):

            # if(Net[u][v] == lx[u] + ly[v] and uy[v] == 0):
            if self.uy[v] == 0:
                t = self.lx[u] + self.ly[v] - self.Net[u][v]  # 所谓顶标 = self.lx[u] + self.ly[v]，类比为，person找track的标准 + track找person的标准
                if t == 0:  # it means here is possible to find a pair   可访问的条件，必须等于顶标，而匈牙利算法只需要有连接，不需看权重
                    self.uy[v] = 1

                    if self.result[v] == -1 or self.match(self.result[v]):  # 和匈牙利算法一致，可找到匹配点才记录结果
                        self.result[v] = u
                        return 1
                elif self.inc > t:  # 如果没有符合的条件，计算下一次顶标需放宽的权重，而不是躺平啥都不做就返回
                    self.inc = t
        return 0

    def Kuh_Munkras(self):
        # initialize lx,ly
        for p in range(self.Number):
            self.ly[p] = 0
            self.result[p] = -1
            self.lx[p] = -999999  # minus infinite
            for q in range(self.Number):
                if self.lx[p] < self.Net[p][q]:  # Choose the biggest value to lx[i]
                    self.lx[p] = self.Net[p][q]

        # find the perfect match
        for u in range(self.Number):
            while 1:  # 匈牙利算法不需要while，找到就找到找不到就算，KM，需降低标准，找到为止，总会找到的
                self.inc = 999999  # the minimum gap
                self.coverUsed()
                if self.match(u):
                    break

                for i in range(self.Number):  # Change sign,and try again
                    if self.ux[i]:
                        self.lx[i] -= self.inc  # person找track的标准要降低
                    if self.uy[i]:
                        self.ly[i] += self.inc  # track找person的标准提高相应的分值

    def calculateSum(self):
        sum = 0
        for i in range(self.Number):
            sum += self.Net[self.result[i]][i]
        return sum

    def getResult(self):
        return self.result

    def set_Net(self, Net):
        self.Net = Net

    def coverUsed(self):
        self.ux, self.uy = np.zeros(self.Number, dtype=int), np.zeros(self.Number,
                                                                      dtype=int)  # variable for record path


if __name__ == '__main__':
    sum = 0
    Net = []
    if Net == []:
        print("System is ready to use defaulted setting to start!")
        km = KM_Algorithm()

    else:
        km = KM_Algorithm(Net)

    km.Kuh_Munkras()
    print('final result:')
    print(km.result)
    print(km.calculateSum())
