import evolution
import genetics
import settings

import unittest
import mock


class EvolutionTests(unittest.TestCase):

    def setUp(self):
        self.genomes = genetics.Population().genomes
        self.desideratum = 42

    def test_assign_fitness_exact(self):

        for genome in self.genomes:
            genome.phenome.expression = self.desideratum

        assigned_fitnesses = [evolution.assignFitness(genome.phenome, desideratum=self.desideratum) for genome in self.genomes]

        # Assert that the sum of the assigned_fitnesses is equal to the length of self.genomes since all phenomes have a fitness of 1
        self.assertEqual(sum(assigned_fitnesses), 1 * len(self.genomes))

    def test_assign_fitness_inexact(self):

        assigned_fitnesses = [evolution.assignFitness(genome.phenome, desideratum=self.desideratum) for genome in self.genomes]

        self.assertEqual(len(assigned_fitnesses), len(self.genomes))

    def test_roulette(self):

        for genome in self.genomes:
            evolution.assignFitness(genome.phenome, desideratum=self.desideratum)

        self.assertIsInstance(evolution.roulette(self.genomes), genetics.Genome)

    @mock.patch('random.random')
    @mock.patch('random.randint')
    def test_crossover(self, randint_call, random_call):
        '''First half of daughter_1's sequence should equal the first half of parent_2's sequence for an equally divided crossover point'''

        parent_1 = self.genomes[0]
        parent_2 = self.genomes[1]

        settings.CROSSOVER_RATE = 0.2
        random_call.return_value = 0.1
        randint_call.return_value = settings.GENOME_LENGTH * 2  # Halfway crossover point

        daughter_1, daughter_2 = evolution.crossover(parent_1, parent_2)

        self.assertEqual(daughter_1.sequence[settings.GENOME_LENGTH * 2:], parent_2.sequence[settings.GENOME_LENGTH * 2:])

    @mock.patch('random.random')
    def test_mutation(self, random_call):

        offspring_genome = self.genomes[0]
        offspring_genome.sequence = '00000001'
        random_call.return_value = 0.0001

        mutate_genome = evolution.mutate(offspring_genome)

        self.assertEqual(mutate_genome.sequence, '11111110')

    @mock.patch('random.random')
    def test_no_mutation(self, random_call):

        offspring_genome = self.genomes[0]
        offspring_genome.sequence = '00000001'
        random_call.return_value = 0.1

        mutate_genome = evolution.mutate(offspring_genome)

        self.assertEqual(mutate_genome.sequence, offspring_genome.sequence)
