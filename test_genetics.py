import unittest
from genetics import *
from evolution import *
import random


class PopulationTests(unittest.TestCase):

    def setUp(self):
        self.population = Population()

    def tearDown(self):
        del self.population

    def test_population_init(self):
        self.assertIsInstance(self.population, object)

    def test_population_genomes(self):
        self.assertEqual(self.population.POPULATION_SIZE, len(self.population.genomes))

    def test_population_phenomes(self):
        self.assertEqual(self.population.POPULATION_SIZE, len(self.population.phenomes))


class GenomeTests(unittest.TestCase):

    def setUp(self):
        self.genome = Genome()

    def test_genome_init(self):
        self.assertIsInstance(self.genome, object)

    def test_seed_genome(self):
        for gene in self.genome.seedGenome(genes=self.genome.GENES):
            self.assertIn(gene, self.genome.GENES)

    def test_genome_length(self):
        self.assertEqual(len(self.genome.genes), self.genome.GENOME_LENGTH)

    def test_translate_codon(self):
        for codon in self.genome.genes:
            self.assertEqual(self.genome.translateCodon(codon), self.genome.GENES[codon])

    def test_base_edit_zero_divisor(self):
        given = [y for x in range(self.genome.GENOME_LENGTH) for y in ['/', 0]]
        desiderata = [y for x in range(self.genome.GENOME_LENGTH) for y in ['*', 0]]
        rationalized_rna = self.genome.baseEditZeroDivisorFragments(normalized_rna=given)

        self.assertEqual(rationalized_rna, desiderata)

    def test_format_sequence_order(self):
        all_integers = [x for x in range(self.genome.GENOME_LENGTH)]
        all_operators = [random.choice(['/', '*', '+', '-']) for x in range(self.genome.GENOME_LENGTH)]

        self.assertEqual(self.genome.formatSequenceOrder(all_operators), self.genome.formatSequenceOrder(all_integers))


if __name__ == '__main__':
    unittest.main()