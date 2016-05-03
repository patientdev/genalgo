import genetics
import evolution

def main():
    desiderata = int(raw_input('What number should we try for?: '))

    match_found = False
    generations = 0

    while not match_found:

        population = genetics.Population()

        next_population = []

        for phenome in population.phenomes:
            phenome.fitness = evolution.assignFitness(phenome, desiderata)
            if phenome.expression == desiderata:
                if not isinstance(phenome.genome.normalized_rna[-1], int):
                    del phenome.genome.normalized_rna[-1]
                print '{} = 0 {}'.format(desiderata, ' '.join(str(codon) for codon in phenome.genome.normalized_rna))
                print 'Found in {:,} generations'.format(generations)
                match_found = True
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
