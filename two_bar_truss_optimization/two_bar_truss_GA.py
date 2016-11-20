import numpy as np
import pandas as pd
import genops as op

#python -m cProfile -s cumtime lwn2pocket.py

def two_bar_truss(density, modulus, load, width, thickness, height, diameter):
    length = ((width/2.0)**2.0 + height**2)**0.5
    area = np.pi * diameter * thickness
    iovera = (diameter**2.0 + thickness**2.0)/8.0
    weight = 2.0 * density * length * area
    stress = load * length/(2.0 * area * height)
    buckling = np.pi**2.0 * modulus * iovera/(length**2.0)
    deflection = load * length**3.0/(2.0 * modulus * area * height**2.0)
    return(weight, stress, buckling, deflection)


# Return the best individual of two selected at random
def get_random_best_individual(population, spec):
    sz = population.shape[0]
    p1 = np.random.randint(0,sz)
    p2 = np.random.randint(0,sz)
    t1 = population[p1]
    t2 = population[p2]
    f1 = fitness(t1, spec)
    f2 = fitness(t2, spec)
    if f1 < f2:
        return t1
    else:
        return t2

# Tournament selection
def tournament_select(population, spec):
    sz = population.shape[0] # Number of rows in population
    ind_size = population.shape[1] # Number of columns (individuals)
    new_pop = np.zeros((sz,ind_size))
    for i in range(0,sz,2):
        best1 = get_random_best_individual(population, spec)
        best2 = get_random_best_individual(population, spec)
        child1, child2 = crossover(best1, best2,1,0,1)
        child1 = mutate(child1,0.1,1,0,1)
        child2 = mutate(child2,0.1,1,0,1)
        new_pop[i] = child1
        new_pop[i+1] = child2
    return new_pop

# SBX Crossover
def crossover(parent1,parent2,eta,low,up):
    child1 = np.zeros(len(parent1))
    child2 = np.zeros(len(parent2))
    for i in range(0,len(parent1)):
        child1[i], child2[i] = op.sbx_real(parent1[i],parent2[i],eta,low,up)
    return child1,child2

# Real mutation
def mutate(individual, prob, eta, low, up):
    for i in range(0,len(individual)):
        individual[i] = op.mutate_real(individual[i],prob, eta, low, up)
    return individual

# Add together new and old populations and grab top 50 results
# sorted by lowest first
def best_population(pop,new_pop, spec):
    final = np.vstack((pop,new_pop))
    ind_size = pop.shape[1]
    pop_sz = pop.shape[0]
    df = pd.DataFrame(final, columns=range(0,ind_size))
    sz = df.shape[0]
    ind_size = df.shape[1]
    fit = []
    for i in range(0,sz):
        f = fitness(final[i], spec)
        fit.append(f)
    df['fit'] = fit
    df = df.sort_values('fit',ascending=True) # Sort by lowest first
    df = df.iloc[0:pop_sz] # Grab top 50
    df = df.drop('fit',axis=1) # Remove fitness measure
    return df.as_matrix()

# Calculate fitness of each inidividual
def fitness(individual, spec):
    #d = decode(individual)
    width = individual[0]*100+1
    thick = individual[1]*100+1
    w,s,b,d = two_bar_truss(spec['density'],spec['modulus'],spec['load']
                                ,spec['width'],spec['thickness'],width,thick) 
    #w,s,b,d = two_bar_truss(0.3,30000,66,60,0.15,d[0],d[1])
    # If any value exceeds contraints weight result
    if s > 100:
        w = w * 2
    if d > 0.25:
        w = w * 2
    if s-b > 0.0:
        w = w * 2
    return w

def generate_valid_individual(spec):
    for i in range(0,1000): 
        temp = np.random.rand(2)
        w,s,b,d = two_bar_truss(spec['density'],spec['modulus'],spec['load']
                                ,spec['width'],spec['thickness'],(temp[0]*100)+1,(temp[1]*100)+1) 
        if s < 100.0 and d < 0.25 and s-b < 0.0:
            return temp

# Generate a random population
def generate(ind_size,pop_size, spec):
    pop = np.zeros((pop_size,ind_size))
    for i in range (0, pop_size):
        pop[i] = generate_valid_individual(spec)
    return pop

# Decode individuals to floating point
# Height and diameter are converted
def decode(individual):
    return(individual*[100,100]+[1,1])


# Main Loop
POP_SIZE = 50
IND_SIZE = 2
DENSITY = 0.3
MODULUS = 30000
LOAD = 66
WIDTH = 60
THICKNESS = 0.15

specifications = {'density':DENSITY,'modulus':MODULUS,'load':LOAD,'width':WIDTH,'thickness':THICKNESS}

import time

start_time = time.time()

pop = generate(IND_SIZE,POP_SIZE, specifications)

for i in range(0,300):
    new_pop = tournament_select(pop, specifications)
    pop = best_population(pop,new_pop, specifications)
    #print fitness(pop[0])
    
print i, fitness(pop[0], specifications)
print decode(pop[0])
print("--- %s seconds ---" % (time.time() - start_time))