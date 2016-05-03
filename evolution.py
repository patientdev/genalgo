import random

def assignFitness(phenome, desiderata):
    '''TO DO'''
    try:
        phenome.fitness = 1/abs(desiderata - phenome.expression)
    except ZeroDivisionError:
        phenome.fitness = 1

    return phenome.fitness


def roulette(phenomes):
    '''Pick a random number and return the phenome with the associated proportional fitness'''

    total_fitness = sum([phenome.fitness for phenome in phenomes])
    stochastic_variable = random.uniform(0, total_fitness)
    current = 0

    for phenome in phenomes:
        current += phenome.fitness
        if current > stochastic_variable:
            return phenome


def crossover(offspring_1, offspring_2):

    CROSSOVER_RATE = 0.7

    if random.random() < CROSSOVER_RATE:
        random_crossover_point = int(random.random() * len(offspring_1.genome.sequence))

        t1 = offspring_1.genome.sequence[0:random_crossover_point] + offspring_2.genome.sequence[random_crossover_point:len(offspring_2.genome.sequence)]

        t2 = offspring_2.genome.sequence[0:random_crossover_point] + offspring_1.genome.sequence[random_crossover_point:len(offspring_1.genome.sequence)]

        return (t1, t2)

    else:
        return (None, None)