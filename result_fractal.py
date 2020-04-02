# -*- coding: utf-8 -*-
import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# file_name = "3retu_11point_result.bdf"
file_name = sys.argv[1]

fractal_result = "fractal_text.txt"

arr = [0 for i in range(29750)]

with open(file_name, encoding="cp932") as f:
    data = f.readlines()

for line in data:
    if line.find("CHEXA") >= 0:
        # print(int(line.split()[1]))
        arr[int(line.split()[1])-1] = 1

arr = np.array(arr)
arr = np.reshape(arr, (350, 85))

np.set_printoptions(threshold=np.inf)

def count(arr, x, y, b):
    i = 0
    j = 0
    c = 0

    while i < x and j < y:
        flag = False
        zero_flag = False
        iti_flag = False
        for k in range(0, b):
            for l in range(0, b):
                if i+k < x and j+l < y:
                    if arr[i+k][j+l] == 0:
                        zero_flag = True
                    if arr[i+k][j+l] == 1:
                        iti_flag = True
                    if (zero_flag == True) and (iti_flag == True):
                        c += 1
                        flag = True
                        break
            if flag:
                break
        i += b
        if i >= x:
            """ ボックスが右端に達したら左端に戻す """
            i = 0
            j += b

    return c # 図形が含まれていたボックスの数を返す

x = 350
y = 85
graph_x = []
graph_y = []

i = 2
while x >= i:
    n = count(arr, x, y, i)
    # print(n)
    graph_x.append(math.log(i))
    graph_y.append(math.log(n))
    # print(i, n)
    # print (math.log(i), math.log(n))
    i *= 2

graph_x = np.array(graph_x).reshape((len(graph_x), 1)) # 1列にする
graph_y = np.array(graph_y).reshape((len(graph_y), 1))

model_lr = LinearRegression()
model_lr.fit(graph_x, graph_y)

plt.plot(graph_x, graph_y, 'o')
plt.plot(graph_x, model_lr.predict(graph_x), linestyle="solid")

# plt.xlabel("")
# plt.ylabel("気温（℃）")

# print("回帰係数=", model_lr.coef_) # フラクタル次元
# print('決定係数 R^2： ', model_lr.score(graph_x, graph_y))

# plt.show()

fractal = model_lr.coef_[0][0] * -1

with open(fractal_result, mode='w') as f:
    f.write('%s\n' % (fractal))


