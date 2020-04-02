# -*- coding: utf-8 -*-

from stl import mesh
# from mpl_toolkits import mplot3d
# import matplotlib.pyplot as plt
import numpy as np
import math
# from sklearn.linear_model import LinearRegression
import os
import sys

# def count():
#     i = j = k = c = 0

#     while i < x and j < y and k < z:
#         for m in range(0, b):
#             for n in range(0, b):
#                 if 

def min_and_max(data):
    x_arr = []
    y_arr = []
    z_arr = []
    
    for i in range(len(data)):
    # for i in range(1):

        a1 = a2 = a3 = 1/3

        x1 = data.vectors[i][0][0]
        x2 = data.vectors[i][1][0]
        x3 = data.vectors[i][2][0]

        y1 = data.vectors[i][0][1]
        y2 = data.vectors[i][1][1]
        y3 = data.vectors[i][2][1]
        
        z1 = data.vectors[i][0][2]
        z2 = data.vectors[i][1][2]
        z3 = data.vectors[i][2][2]

        x_arr.append(x1)
        x_arr.append(x2)
        x_arr.append(x3)

        y_arr.append(y1)
        y_arr.append(y2)
        y_arr.append(y3)

        z_arr.append(z1)
        z_arr.append(z2)
        z_arr.append(z3)

        # new_x = a1*x1 + a2*x2 + a3*x3
        # new_y = a1*y1 + a2*y2 + a3*y3
        # new_z = a1*z1 + a2*z2 + a3*z3

        # print(new_x, new_y, new_z)

    x_max = max(x_arr)
    y_max = max(y_arr)
    z_max = max(z_arr)
    x_min = min(x_arr)
    y_min = min(y_arr)
    z_min = min(z_arr)

    # print("x Max " + str(x_max))
    # print("y Max " + str(y_max))
    # print("z Max " + str(z_max))
    # print("x min " + str(x_min))
    # print("y min " + str(y_min))
    # print("z min " + str(z_min))
    return x_max, y_max, z_max, x_min, y_min, z_min


def calcu(array3d, a1, a2, a3, x1, x2, x3, y1, y2, y3, z1, z2, z3, x_max, y_max, z_max, x_min, y_min, z_min):

    new_x = a1*x1 + a2*x2 + a3*x3
    new_y = a1*y1 + a2*y2 + a3*y3
    new_z = a1*z1 + a2*z2 + a3*z3
    print(new_x, new_y, new_z)

    x_point = int((new_x - x_min) / 0.5) - 1
    y_point = int((new_y - y_min) / 0.5) - 1
    z_point = int((new_z - z_min) / 0.5) - 1

    print(x_point)
    print(y_point)
    print(z_point)

    array3d[x_point][y_point][z_point] = 1

    return x_point, y_point, z_point

def show(data, x_max, y_max, z_max, x_min, y_min, z_min):

    array3d = np.zeros((800,200,2))
    np.set_printoptions(threshold=np.inf)
    # print(array3d)

    # figure = plt.figure()
    # axes = mplot3d.Axes3D(figure)

    # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(data.vectors))
    # scale = data.points.flatten()
    # axes.auto_scale_xyz(scale, scale, scale)

    print(len(data))
    x_arr = []
    y_arr = []
    z_arr = []
    
    for i in range(len(data)):
    # for i in range(1):

        a1 = a2 = a3 = 1/3
        

        x1 = data.vectors[i][0][0]
        x2 = data.vectors[i][1][0]
        x3 = data.vectors[i][2][0]

        y1 = data.vectors[i][0][1]
        y2 = data.vectors[i][1][1]
        y3 = data.vectors[i][2][1]
        
        z1 = data.vectors[i][0][2]
        z2 = data.vectors[i][1][2]
        z3 = data.vectors[i][2][2]

        x_arr.append(x1)
        x_arr.append(x2)
        x_arr.append(x3)

        y_arr.append(y1)
        y_arr.append(y2)
        y_arr.append(y3)

        z_arr.append(z1)
        z_arr.append(z2)
        z_arr.append(z3)

        x_point, y_point, z_point = calcu(array3d, a1, a2, a3, x1, x2, x3, y1, y2, y3, z1, z2, z3, x_max, y_max, z_max, x_min, y_min, z_min)

        print(x_point)
        print(y_point)
        print(z_point)

        array3d[x_point][y_point][z_point] = 1

    print(array3d[400][:][:])
    ct_1 = np.count_nonzero(array3d == 1)
    print(array3d.size)
    print(ct_1)

    x_max = max(x_arr)
    y_max = max(y_arr)
    z_max = max(z_arr)
    x_min = min(x_arr)
    y_min = min(y_arr)
    z_min = min(z_arr)
    # plt.show()

    return ct_1

def main():

    data = mesh.Mesh.from_file('3retu_8point.stl')

    graph_x = []
    graph_y = []

    x_max, y_max, z_max, x_min, y_min, z_min = min_and_max(data)
    # print("x Max " + str(x_max))
    # print("y Max " + str(y_max))
    # print("z Max " + str(z_max))
    # print("x min " + str(x_min))
    # print("y min " + str(y_min))
    # print("z min " + str(z_min))

    i = 0.5
    # while x >= i:
    n = show(data, x_max, y_max, z_max, x_min, y_min, z_min)
    # print(n)
    graph_x.append(math.log(i))
    graph_y.append(math.log(n))
    # print(i, n)
    # print (math.log(i), math.log(n))
    i *= 2

    # print((math.log(i))/(math.log(n)))
    # print((math.log(n))/(math.log(i)))

    graph_x = np.array(graph_x).reshape((len(graph_x), 1)) # 1列にする
    graph_y = np.array(graph_y).reshape((len(graph_y), 1))

    # model_lr = LinearRegression()
    # model_lr.fit(graph_x, graph_y)

    # fractal = model_lr.coef_[0][0] * -1

    # print(fractal)

if __name__ == "__main__":
    main()