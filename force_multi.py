# -*- coding: utf-8 -*-

# モデルの表面と裏面に荷重を加える
import os
import numpy as np
import sys

def fractal(row, point_num):

    file_name = "point.bdf"
    topology_bat_name = "force.bat"
    fractal_bat_name = "fractal.bat"

    param = "0.01_smooth1.0.txt"

    # diff_dict = {"351":172, "176":344, "71":860, "51":1204, "36":1720, "26":2408, "15":4300, "11":6020, "8":8600, "6":12040}
    diff_dict = {"0":172, "1":344, "2":860, "3":1204, "4":1720, "5":2408, "6":4300, "7":6020, "8":8600, "9":12040}

    with open(file_name, encoding="cp932") as f:
        data = f.readlines()

    array = np.arange(2, 173, 2)

    # row = 5     # forceを置く列数 retu
    # point_num = "26"     # 1列に置くforceの数 point
    row = int(row)
    point_num = str(point_num)

    diff = diff_dict[point_num]
    col = 86    # 横の節点数

    x = 1.0
    y = 0.0
    z = 0.0

    insert_line = 16    # bdfファイルにforceを追記する行
    ct = 0   # 荷重の数カウント

    for i in range(row):
        start_pos = array[int((col / (row+1)) * (i+1))]
        end_pos = start_pos + 60200
        start_pos_tmp = start_pos
        end_pos_tmp = end_pos

        # 表面のforce
        if (len(str(start_pos)) == 2): 
            data.insert(insert_line, "FORCE          2      %s       00.500000%8s%8s%8s\n" % (start_pos, x, y, z))
            insert_line += 1
        elif (len(str(start_pos)) == 3):
            data.insert(insert_line, "FORCE          2     %s       00.500000%8s%8s%8s\n" % (start_pos, x, y, z))
            insert_line += 1
        while(start_pos < end_pos-diff):
            ct += 1
            start_pos += diff
            if (len(str(start_pos)) == 2): 
                data.insert(insert_line, "FORCE          2      %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
            elif (len(str(start_pos)) == 3):
                data.insert(insert_line, "FORCE          2     %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
            elif (len(str(start_pos)) == 4):
                data.insert(insert_line, "FORCE          2    %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
            elif (len(str(start_pos)) == 5):
                data.insert(insert_line, "FORCE          2   %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
        data.insert(insert_line, "FORCE          2   %s       00.500000%8s%8s%8s\n" % (end_pos, x, y, z))

        # 裏面のforce
        start_pos = start_pos_tmp - 1
        end_pos = end_pos_tmp - 1
        insert_line += 1
        if (len(str(start_pos)) == 2): 
            data.insert(insert_line, "FORCE          2      %s       00.500000%8s%8s%8s\n" % (start_pos, x, y, z))
            insert_line += 1
        elif (len(str(start_pos)) == 3):
            data.insert(insert_line, "FORCE          2     %s       00.500000%8s%8s%8s\n" % (start_pos, x, y, z))
            insert_line += 1
        while(start_pos < end_pos-diff):
            start_pos += diff
            if (len(str(start_pos)) == 2): 
                data.insert(insert_line, "FORCE          2      %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
            elif (len(str(start_pos)) == 3):
                data.insert(insert_line, "FORCE          2     %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
            elif (len(str(start_pos)) == 4):
                data.insert(insert_line, "FORCE          2    %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
            elif (len(str(start_pos)) == 5):
                data.insert(insert_line, "FORCE          2   %s       01.000000%8s%8s%8s\n" % (start_pos, x, y, z))
                insert_line += 1
        data.insert(insert_line, "FORCE          2   %s       00.500000%8s%8s%8s\n" % (end_pos, x, y, z))
        insert_line += 1

    file_name_to_save = "bdf/new_point.bdf"
    # file_name_to_save = "bdf\\" + str(row) + "row_" + str(int(ct/row+2)) + "point.bdf"
    file_name_to_fractal = str(row) + "row_" + str(int(ct/row+2)) + "point_result" + ".bdf"

    with open(file_name_to_save, mode="w", encoding="cp932") as f:
        f.writelines(data)

    # with open(topology_bat_name, mode='a') as f:
    #     f.write('\"C:\\Program Files\\Quint\\OPTISHAPE-TS2019\\optishape-tf\"	\"param\\%s\"	\"%s\"\n' % (param, file_name_to_save))

    # with open(fractal_bat_name, mode='a') as f:
    #     f.write('C:\\Users\\kumanomi\\AppData\\Local\\Programs\\Python\\Python37\\python.exe result_fractal.py \"bdf\\%s\n' % file_name_to_fractal)
