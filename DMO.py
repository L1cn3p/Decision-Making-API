from deap import base, creator, tools, algorithms
from utils import *
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

HARD_CONSTRAINT_PENALTY = 2
RANDOM_SEED = 58
random.seed(RANDOM_SEED)
# Genetic Algorithm constants:
POPULATION_SIZE = 100
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 200
HALL_OF_FAME_SIZE = 10

