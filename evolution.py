import random
import settings
import genetics


def assignFitness(phenome, desideratum=0):
    '''TO DO'''
    try:
        phenome.fitness = 1 / abs(desideratum - phenome.expression)
    except ZeroDivisionError:
        phenome.fitness = 1

    return phenome.fitness


def roulette(genomes):
    '''Pick a random number and return the phenome with the associated proportional fitness'''

    total_fitness = sum([genome.phenome.fitness for genome in genomes])
    stochastic_variable = random.uniform(0, total_fitness)
    current = 0

    for genome in genomes:
        current += genome.phenome.fitness
        if current > stochastic_variable:
            return genome


def crossover(offspring_1_genome, offspring_2_genome):

    if random.random() < settings.CROSSOVER_RATE:
        random_crossover_point = random.randint(1, len(offspring_1_genome.sequence))

        offspring_1_crossed_sequence = offspring_1_genome.sequence[0:random_crossover_point] + offspring_2_genome.sequence[random_crossover_point:settings.GENOME_LENGTH * 4]

        offspring_2_crossed_sequence = offspring_2_genome.sequence[0:random_crossover_point] + offspring_1_genome.sequence[random_crossover_point:settings.GENOME_LENGTH * 4]

        offspring_1_genome = genetics.Genome(genes=[offspring_1_crossed_sequence[i:i + 4] for i in range(0, settings.GENOME_LENGTH * 4, 4)])
        offspring_2_genome = genetics.Genome(genes=[offspring_2_crossed_sequence[i:i + 4] for i in range(0, settings.GENOME_LENGTH * 4, 4)])

    return offspring_1_genome, offspring_2_genome