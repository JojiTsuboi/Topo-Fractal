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

database = {}
database[5] = 25
database[10] = 100

header = ["5", "0"]



with open('testooo.csv', 'w') as f:
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    writer.writerows(database)

with open('testooo.csv') as f:
    print(f.read())