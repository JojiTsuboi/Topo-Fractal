# -*- coding: utf-8 -*-

import random
from deap import base
from deap import creator
from deap import tools
import force_multi
import random_arr_test
import os
import csv
import shutil
import numpy as np
import pandas as pd
from scoop import futures
from concurrent.futures import ThreadPoolExecutor
import time

path = "fractal_text.txt"
param = "0.01_smooth1.0.txt"

var_num = 52

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, var_num)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

database = {}
eval_count = 0

def change_decimal_ind(individual):
    num = str(individual[0])
    for i in range(1,var_num):
        num = num + str(individual[i])
    decimal_ind = int(num,2)

    return decimal_ind

def calc_fractal(number, individual, decimal_ind):
    fractal_bat = "fractal_test" + number + ".bat"
    os.system(fractal_bat)
    with open(path) as f:
        s = f.read().splitlines()
    square_error = (1.5 - float(s[0])) ** 2
    with open('ga_log.txt', 'a') as f:
        f.write(str(individual) + " : " + str(s[0]) + "\n")
    bdf_copy_name = "bdf/new_point_test" + number +"_result.bdf"
    bdf_file_name = "result/" + str(decimal_ind) + "_" + str(s[0]) +  ".bdf"
    shutil.copyfile(bdf_copy_name, bdf_file_name)
    database[decimal_ind] = square_error

    return square_error,

def calc_topology(number):
    force_bat = "start force_test" + number + ".bat"
    # force_bat2 = "force" + number + ".bat"
    # if number % 3 == 0:
        # os.system(force_bat2)
    # else: 
    os.system(force_bat)


def eval_fractal(pop):
    global eval_count
    eval_count += 1

    shutil.rmtree('bdf')
    time.sleep(1)
    os.makedirs('bdf', exist_ok=True)

    decimal_pop = list(map(change_decimal_ind, pop))

    for i in range(len(pop)):
        random_arr_test.fractal(pop[i], str(i))

    arr = []
    
    bdf_path_fin = "bdf/" + str(len(pop)-1) + ".txt"
    print(bdf_path_fin)
    i = 0
    # for i in range(len(pop)):
    while (os.path.exists(bdf_path_fin) == False):
        bdf_path1 = "bdf/" + str(i-1) + ".txt"
        bdf_path2 = "bdf/" + str(i-2) + ".txt"
        bdf_path3 = "bdf/" + str(i-3) + ".txt"
        print("i-------", i)

        if (i >= 3):
            while True:
                if (os.path.exists(bdf_path1) == True):
                    print("i-------", i)
                    calc_topology(str(i))
                    i +=1
                    break
                elif (os.path.exists(bdf_path2) == True):
                    print("i-------", i)
                    calc_topology(str(i))
                    i += 1
                    break
                elif (os.path.exists(bdf_path3) == True):
                    print("i-------", i)
                    calc_topology(str(i))
                    i += 1
                    break
        else:
            calc_topology(str(i))
            i += 1


    for i in range(len(pop)):
        square_error = calc_fractal(str(i), pop[i], decimal_pop[i])
        print("error", square_error)
        arr.append(square_error)

    return arr

# toolbox.register("evaluate", eval_fractal)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    with open('ga_log.txt', 'w') as f:
        f.write("")

    os.makedirs('result', exist_ok=True)

    random.seed(64)
    
    pop = toolbox.population(n=10)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 10
    
    print("Start of evolution")
    fitnesses = eval_fractal(pop)

    # a = input()

    with open('ga_log.txt', 'a') as f:
        f.write("pop" + str(pop) + "\n")
    with open('ga_log.txt', 'a') as f:
        f.write("fitnesses" + str(fitnesses) + "\n")
        
    for decimal_ind, fit in zip(pop, fitnesses):
        with open('ga_log.txt', 'a') as f:
            f.write("decimal_ind" + str(decimal_ind) + "\n")
        with open('ga_log.txt', 'a') as f:
            f.write("fit" + str(fit) + "\n")
        print("decimal_ind", decimal_ind)
        print("fit", fit)
        decimal_ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    with open('ga_log.txt', 'a') as f:
            f.write("  Evaluated %i individuals\n" % len(pop))
    
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        with open('ga_log.txt', 'a') as f:
            f.write("-- Generation %i --\n" % g)
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

    
        invalid_ind = [decimal_ind for decimal_ind in offspring if not decimal_ind.fitness.valid]
        fitnesses = eval_fractal(invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        with open('ga_log.txt', 'a') as f:
            f.write("  Evaluated %i individuals\n" % len(invalid_ind))
        pop[:] = offspring
        
        fits = [decimal_ind.fitness.values[0] for decimal_ind in pop]
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        global eval_count 
        print ("eval_count >> ", eval_count)
    
    print("-- End of (successful) evolution --")
    with open('ga_log.txt', 'a') as f:
        f.write("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]

    num = str(best_ind[0])
    for i in range(1,var_num):
        num = num + str(best_ind[i])
    decimal_best_ind = int(num,2)
    decimal_best_ind = str(decimal_best_ind)

    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    with open('ga_log.txt', 'a') as f:
            f.write("Best individual is %s, %s, %s\n" % (best_ind, decimal_best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()