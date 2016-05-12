import genetics
import evolution
import settings
import json
import sys
from db_results import ResultsDatabase

import time

desideratum = int(raw_input('What number should we try for?: '))

# Customize paramaters, defaulting to settings module
customize = raw_input('Would you like to customize parameters? [y/N]')
if any(input in customize for input in ('Y', 'y')):
    settings.POPULATION_SIZE = int(raw_input('POPULATION_SIZE [{}]? '.format(settings.POPULATION_SIZE)) or settings.POPULATION_SIZE)
    settings.GENOME_LENGTH = int(raw_input('GENOME_LENGTH [{}]? '.format(settings.GENOME_LENGTH)) or settings.GENOME_LENGTH)
    settings.CROSSOVER_RATE = float(raw_input('CROSSOVER_RATE [{}]? '.format(settings.CROSSOVER_RATE)) or settings.CROSSOVER_RATE)

# Halt program if desideratum exceeds highest possible result
if desideratum > 9**(settings.GENOME_LENGTH / 4):
    print '\033[91mError:\033[0m This will never work :('
    sys.exit(1)

# Output settings
print '\n\033[95mPopulation initialized with the following settings:\033[0m'
print 'POPULATION_SIZE:', settings.POPULATION_SIZE
print 'GENOME_LENGTH:', settings.GENOME_LENGTH
print 'CROSSOVER_RATE:', settings.CROSSOVER_RATE
print 'GENES:', json.dumps(settings.GENES, indent=2)  # Using json.dumps for formatting

# Set a flag for which to generate loop
match_found = False

# Init generations counter
generations = 0

# Init first population
population = genetics.Population()

# Start timer for our primary loop
start = time.time()
while not match_found:

    print len(population.genomes)

    for genome in population.genomes:

        phenome = genome.phenome
        phenome.fitness = evolution.assignFitness(phenome, desideratum=desideratum)

        if phenome.expression == desideratum:

            generations += 1
            match_found = True

            # Stop timer
            duration = round(time.time() - start, 2)

            # Print various results
            print '\n\033[92m{} Found after {:,} generations over {} seconds\033[0m'.format(u'\u2713'.encode('utf-8'), generations, duration)

            print '{} {}'.format(u'\u21B3'.encode('utf-8'), genome.sequence)

            print '{} {} = 0 {}'.format(u'\u21B3'.encode('utf-8'), desideratum, ' '.join(str(codon) for codon in phenome.genome.normalized_rna))

            # Prep results for database
            results_db = ResultsDatabase()
            results = {
                'given_number': desideratum,
                'duration': duration,
                'successful_sequence': phenome.genome.sequence,
                'generations': generations
            }

            # Add results to database
            results_db.insert_results(results=results)

            break

    # Produce next population, for next loop iteration
    generations += 1
    next_population = []

    for genome in population.genomes:
        offspring_1_genome = evolution.roulette(population.genomes)
        offspring_2_genome = evolution.roulette(population.genomes)

        t1, t2 = evolution.crossover(offspring_1_genome, offspring_2_genome)

        next_population.append(t1)
        next_population.append(t2)

    population = genetics.Population(genomes=next_population)
