# -*- coding: utf-8 -*-

import random
from deap import base
from deap import creator
from deap import tools
import force_multi
import random_arr
import os
import csv
import shutil
import numpy as np
import pandas as pd
from scoop import futures
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

path = "fractal_text.txt"
pop = [[1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
[0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]]

eval_count = 0
database = {}
var_num = 52

def calc_fractal(individual, decimal_ind, num):
    random_arr.fractal(individual)
    os.system("force1.bat")
    os.system("fractal1.bat")
    with open(path) as f:
        s = f.read().splitlines()
    square_error = (1.5 - float(s[0])) ** 2
    with open('ga_log.txt', 'a') as f:
        f.write(str(individual) + " : " + str(s[0]) + "\n")
    bdf_file_name = "result/" + str(decimal_ind) + "_" + str(s[0]) +  ".bdf"
    shutil.copyfile("bdf/new_point_result.bdf", bdf_file_name)
    database[decimal_ind] = square_error

    return square_error

def eval_fractal(individual):
    global eval_count
    eval_count += 1

    num = str(individual[0])
    for i in range(1,var_num):
        num = num + str(individual[i])
    decimal_ind = int(num,2)
    decimal_ind = str(decimal_ind)

    if eval_count == 1:
        square_error = calc_fractal(individual, decimal_ind)

    elif eval_count >= 2:
        if (decimal_ind in database) == True:
            with open('ga_log.txt', 'a') as f:
                f.write(str(individual) + " : database\n")
            return database[decimal_ind],

        else:
            square_error = calc_fractal(individual, decimal_ind)

    return square_error,



def main():
    with open('ga_log.txt', 'w') as f:
        f.write("")

    a1 = multiprocessing.Process(target=eval_fractal, args=(pop[0],))
    a2 = multiprocessing.Process(target=eval_fractal, args=(pop[1],))
    a3 = multiprocessing.Process(target=eval_fractal, args=(pop[2],))
    a4 = multiprocessing.Process(target=eval_fractal, args=(pop[3],))

    a1.start()
    a2.start()
    a3.start()
    a4.start()
    
    # fitnesses = []
    # tpe = ThreadPoolExecutor(max_workers=4)
    # for i in range(len(pop)):
    #     future = tpe.submit(eval_fractal, pop)
    #     fitnesses.append(future)
    # fitnesses = list(map(eval_fractal, pop))

if __name__ == "__main__":
    main()