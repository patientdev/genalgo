import genetics
import evolution
import settings
from db_results import ResultsDatabase

import time

desiderata = int(raw_input('What number should we try for?: '))

match_found = False
generations = 0

population = genetics.Population()

# Start timer for our primary loop
start = time.time()
while not match_found:

    for genome in population.genomes:
        phenome = genome.phenome
        phenome.fitness = evolution.assignFitness(phenome, desiderata=desiderata)
        if phenome.expression == desiderata:
            print '{} = 0 {}'.format(desiderata, ' '.join(str(codon) for codon in phenome.genome.normalized_rna))

            duration = round(time.time() - start, 2)
            print 'Found in {:,} generations in {} seconds'.format(generations, duration)
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
