import unittest
from genetics import *
from evolution import *
import settings
import random


class PopulationTests(unittest.TestCase):

    def setUp(self):
        self.population = Population()

    def tearDown(self):
        del self.population

    def test_population_init(self):
        self.assertIsInstance(self.population, object)

    def test_population_genomes(self):
        self.assertEqual(settings.POPULATION_SIZE, len(self.population.genomes))


class GenomeTests(unittest.TestCase):

    def setUp(self):
        self.genome = Genome()

    def test_genome_init(self):
        self.assertIsInstance(self.genome, object)

    def test_seed_genome(self):
        for gene in self.genome.seedGenome(genes=settings.GENES):
            self.assertIn(gene, settings.GENES)

    def test_genome_length(self):
        self.assertEqual(len(self.genome.genes), settings.GENOME_LENGTH)

    def test_translate_codon(self):
        for codon in self.genome.genes:
            self.assertEqual(self.genome.translateCodon(codon), settings.GENES[codon])

    def test_base_edit_zero_divisor(self):
        given = [y for x in range(settings.GENOME_LENGTH) for y in ['/', 0]]
        desiderata = [y for x in range(settings.GENOME_LENGTH) for y in ['*', 0]]
        rationalized_rna = self.genome.baseEditZeroDivisorFragments(normalized_rna=given)

        self.assertEqual(rationalized_rna, desiderata)

    def test_format_sequence_order(self):
        all_integers = [x for x in range(settings.GENOME_LENGTH)]
        all_operators = [random.choice(['/', '*', '+', '-']) for x in range(settings.GENOME_LENGTH)]

        # Assert that both lists, one of nothing but integers and the other nothing but operators, will be empty and therefore equal (an empty list plus an empty list is...an empty list)

        self.assertEqual([], self.genome.formatSequenceOrder(all_operators) + self.genome.formatSequenceOrder(all_integers))


if __name__ == '__main__':
    unittest.main()