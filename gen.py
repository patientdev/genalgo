import genetics
import evolution
import settings
import json
from db_results import ResultsDatabase

import time

desiderata = int(raw_input('What number should we try for?: '))
customize = raw_input('Would you like to customize parameters? [y/N]')
if any(input in customize for input in ('Y', 'y')):
    settings.POPULATION_SIZE = int(raw_input('POPULATION_SIZE [100]? ') or settings.POPULATION_SIZE)
    settings.GENOME_LENGTH = int(raw_input('GENOME_LENGTH [20]? ') or settings.GENOME_LENGTH)
    settings.CROSSOVER_RATE = float(raw_input('CROSSOVER_RATE [0.7]? ') or settings.CROSSOVER_RATE)

match_found = False
generations = 0

population = genetics.Population()

print '\n\033[95mPopulation initialized with the following settings:\033[0m'
print 'POPULATION_SIZE:', settings.POPULATION_SIZE
print 'GENOME_LENGTH:', settings.GENOME_LENGTH
print 'CROSSOVER_RATE:', settings.CROSSOVER_RATE
print 'GENES:', json.dumps(settings.GENES, indent=2)

# Start timer for our primary loop
start = time.time()
while not match_found:

    for genome in population.genomes:
        phenome = genome.phenome
        phenome.fitness = evolution.assignFitness(phenome, desiderata=desiderata)
        if phenome.expression == desiderata:

            duration = round(time.time() - start, 2)

            print '\n\033[92m{} Found after {:,} generations over {} seconds\033[0m'.format(u'\u2713'.encode('utf-8'), generations, duration)

            print '{} {}'.format(u'\u21B3'.encode('utf-8'), genome.sequence)

            print '{} {} = 0 {}'.format(u'\u21B3'.encode('utf-8'), desiderata, ' '.join(str(codon) for codon in phenome.genome.normalized_rna))

            match_found = True

            results_db = ResultsDatabase()
            results = {
                'given_number': desiderata,
                'duration': duration,
                'successful_sequence': phenome.genome.sequence,
                'generations': generations
            }
            results_db.insert_results(results=results)

            break
        else:
            generations += 1
            next_population = []

            # print generations, len(population.genomes)

            for genome in population.genomes:
                offspring_1_genome = evolution.roulette(population.genomes)
                offspring_2_genome = evolution.roulette(population.genomes)

                t1, t2 = evolution.crossover(offspring_1_genome, offspring_2_genome)

                next_population.append(t1)
                next_population.append(t2)

    population = genetics.Population(genomes=next_population)
