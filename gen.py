import genetics
import evolution
import settings
import json
import sys
from db_results import ResultsDatabase

import time

desideratum = int(input('What number should we try for?: '))

# Customize paramaters, defaulting to settings module
customize = input('Would you like to customize parameters? [y/N]')
if any(input in customize for input in ('Y', 'y')):
    settings.POPULATION_SIZE = int(input('POPULATION_SIZE [{}]? '.format(settings.POPULATION_SIZE)) or settings.POPULATION_SIZE)
    settings.GENOME_LENGTH = int(input('GENOME_LENGTH [{}]? '.format(settings.GENOME_LENGTH)) or settings.GENOME_LENGTH)
    settings.CROSSOVER_RATE = float(input('CROSSOVER_RATE [{}]? '.format(settings.CROSSOVER_RATE)) or settings.CROSSOVER_RATE)
    settings.MUTATION_RATE = float(input('MUTATION_RATE [{}]? '.format(settings.MUTATION_RATE)) or settings.MUTATION_RATE)

# Halt program if desideratum exceeds highest possible result
if desideratum > 9**(settings.GENOME_LENGTH / 4):
    print('\033[91mError:\033[0m This will never work :(')
    sys.exit(1)

# Output settings
print('\n\033[95mPopulation initialized with the following settings:\033[0m')
print('POPULATION_SIZE:', settings.POPULATION_SIZE)
print('GENOME_LENGTH:', settings.GENOME_LENGTH)
print('CROSSOVER_RATE:', settings.CROSSOVER_RATE)
print('MUTATION_RATE:', settings.MUTATION_RATE)
print('GENES:', json.dumps(settings.GENES, indent=2))  # Using json.dumps for formatting

# Set a flag for which to generate loop
match_found = False

# Init generations counter
generations = 0

# Init first population
population = genetics.Population()

# Start timer for our primary loop
start = time.time()

while not match_found:

    for genome in population.genomes:

        phenome = genome.phenome
        phenome.fitness = evolution.assignFitness(phenome, desideratum=desideratum)

        if phenome.expression == desideratum:

            match_found = True
            break

    if not match_found:
        # Produce next population, for next loop iteration
        generations += 1
        next_population = []

        for genome in population.genomes:
            offspring_1_genome = evolution.roulette(population)
            offspring_2_genome = evolution.roulette(population)

            t1, t2 = evolution.crossover(offspring_1_genome, offspring_2_genome)

            mutated_offspring_1 = evolution.mutate(t1)
            mutated_offspring_2 = evolution.mutate(t2)

            next_population.append(mutated_offspring_1)
            next_population.append(mutated_offspring_2)

        population = genetics.Population(genomes=next_population)

# We found a match, so print report
if match_found:

    # Stop timer
    duration = round(time.time() - start, 2)

    # Print various results
    print('\n\033[92m✓ Found after {:,} generations over {} seconds\033[0m'.format(generations, duration))

    print('↳ {}'.format(genome.sequence))

    print('↳ {} = 0 {}'.format(desideratum, ' '.join(str(codon) for codon in phenome.genome.normalized_rna)))

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