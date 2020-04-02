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

path = "fractal_text.txt"
var_num = 52

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, var_num)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

database = {}
eval_count = 0

def calc_fractal(individual, decimal_ind):
    random_arr.fractal(individual)
    os.system("force.bat")
    os.system("fractal.bat")
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

toolbox.register("evaluate", eval_fractal)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    with open('ga_log.txt', 'w') as f:
        f.write("")

    os.makedirs('result', exist_ok=True)

    random.seed(64)
    
    pop = toolbox.population(n=52)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 52
    
    print("Start of evolution")

    fitnesses = list(map(toolbox.evaluate, pop))
    print(fitnesses)
    
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
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for decimal_ind, fit in zip(invalid_ind, fitnesses):
            decimal_ind.fitness.values = fit
        
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