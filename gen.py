import genetics
import evolution
import settings
from db_results import ResultsDatabase

import time


def main():
    desiderata = int(raw_input('What number should we try for?: '))

    match_found = False
    generations = 0

    start = time.time()
    while not match_found:

        population = genetics.Population()

        next_population = []

        for phenome in population.phenomes:
            phenome.fitness = evolution.assignFitness(phenome, desiderata)
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

                while len(next_population) < len(population.phenomes):
                    offspring_1 = evolution.roulette(population.phenomes)
                    offspring_2 = evolution.roulette(population.phenomes)

                    t1, t2 = evolution.crossover(offspring_1, offspring_2)

                    next_population.append(t1)
                    next_population.append(t2)

        population.phenomes = [next_population[i:i+4] for i in range(0, len(next_population), 4)]

if __name__ == '__main__':
    main()
