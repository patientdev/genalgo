import genetics
import evolution
import settings
import json
import sys
from db_results import ResultsDatabase

import time

while True:
    try:
        desideratum = int(input('What number should we try for?: '))
        break
    except ValueError:
        print('Input an integer')

# Customize paramaters, defaulting to settings module
customize = input('Would you like to customize parameters? [y/N]')
if any(input in customize for input in ('Y', 'y')):
    settings.POPULATION_SIZE = int(input('POPULATION_SIZE [{}]? '.format(settings.POPULATION_SIZE)) or settings.POPULATION_SIZE)
    settings.GENOME_LENGTH = int(input('GENOME_LENGTH [{}]? '.format(settings.GENOME_LENGTH)) or settings.GENOME_LENGTH)
    settings.CROSSOVER_RATE = float(input('CROSSOVER_RATE [{}]? '.format(settings.CROSSOVER_RATE)) or settings.CROSSOVER_RATE)
    settings.MUTATION_RATE = float(input('MUTATION_RATE [{}]? '.format(settings.MUTATION_RATE)) or settings.MUTATION_RATE)
    settings.ROULETTE_METHOD = 'roulette' if input('[1] Stochastic O(1)  // default\n[2] Linear O(n)\n') == '2' else 'stochastic_acceptance_roulette'

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
print('ROULETTE_METHOD:', 'Stochastic O(1)' if settings.ROULETTE_METHOD == 'stochastic_acceptance_roulette' else 'Linear O(n)')

# Set a flag for which to generate loop
match_found = False

# Init generations counter
generations = 1

# Init first population
population = genetics.Population()

# Start timer for our primary loop
start = time.time()

print("\n\033[36m==Status==\033[0m")
while not match_found:

    print("Generation: {}, Population size: {}".format(generations, len(population.genomes)))

    for genome in population.genomes:

        phenome = genome.phenome
        phenome.fitness = evolution.assignFitness(phenome, desideratum=desideratum)
        population.max_fitness = sum([genome.phenome.fitness for genome in population.genomes])

        # We found a match, so break the loop
        if phenome.expression == desideratum:
            match_found = True
            break

    if not match_found:

        # Produce next population, for next loop iteration
        generations += 1
        next_population = []

        for genome in population.genomes:

            # Fitness proportionate selection (aka roulette wheel selection)
            offspring_1_genome = getattr(evolution, settings.ROULETTE_METHOD)(population)
            offspring_2_genome = getattr(evolution, settings.ROULETTE_METHOD)(population)

            # Chromosomal crossover
            t1, t2 = evolution.crossover(offspring_1_genome, offspring_2_genome)

            # Bit mutation
            mutated_offspring_1 = evolution.mutate(t1)
            mutated_offspring_2 = evolution.mutate(t2)

            # Add evolved children to next population
            next_population.append(mutated_offspring_1)
            next_population.append(mutated_offspring_2)

        # Init new population
        population = genetics.Population(genomes=next_population)

# We found a match, so print report
if match_found:

    # Stop timer
    duration = round(time.time() - start, 2)

    # Print various results
    print('\n\033[92m✓ Found after {:,} generations over {} seconds\033[0m'.format(generations, duration))

    print('↳ {}'.format(genome.sequence))

    print('↳ {} = 0 {}'.format(desideratum, ' '.join(str(codon) for codon in phenome.genome.normalized_rna)))

    # Save run in database
    with ResultsDatabase() as results_db:
        # Prep results for database
        results_db = ResultsDatabase()
        results = {
            'given_number': desideratum,
            'duration': duration,
            'successful_sequence': phenome.genome.sequence,
            'generations': generations,
            'roulette_method': settings.ROULETTE_METHOD
        }

        # Add results to database
        results_db.insert_results(results=results)