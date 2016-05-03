from random import randint, choice as randomchoice


class Population(object):

    POPULATION_SIZE = 100

    def __init__(self):
        self.genomes = [Genome() for genome in range(Population.POPULATION_SIZE)]
        self.phenomes = [Phenome(genome=genome) for genome in self.genomes]


class Genome(object):

    GENOME_LENGTH = 20

    genes = {
        '0000': 0,
        '0001': 1,
        '0010': 2,
        '0011': 3,
        '0100': 4,
        '0101': 5,
        '0110': 6,
        '0111': 7,
        '1000': 8,
        '1001': 9,
        '1010': '+',
        '1011': '-',
        '1100': '*',
        '1101': '/'
    }

    def __init__(self):
        self.genes = self.seedGenome()
        self.sequence = ''.join(self.genes)
        self.mRNA = self.translateGenome()
        self.normalized_rna = self.editRNA()
        self.fitness = 0.0

    def seedGenome(self):
        '''Returns a genome as an (inherently) ordered list of genes of length given by static GENOME_LENGTH variable'''
        genome = [randomchoice(Genome.genes.keys()) for x in range(Genome.GENOME_LENGTH)]

        return genome

    def translateGenome(self):

        mRNA = [Genome.genes[x] for x in self.genes]

        return mRNA

    def editRNA(self):
        normalized_rna = []
        need_operator = True

        for codon in self.mRNA:
            # Looking for an operator
            if need_operator:
                if not isinstance(codon, int):
                    need_operator = False
                    normalized_rna.append(codon)

            # Looking for a number
            else:
                if isinstance(codon, int):
                    need_operator = True
                    normalized_rna.append(codon)

        for index, codon in enumerate(normalized_rna):
            if codon is '/' and next(enumerate(normalized_rna)) is 0:
                normalized_rna[index] = '*'

        return normalized_rna


class Phenome(object):

    def __init__(self, genome=Genome()):
        self.genome = genome
        self.expression = self.expressGenome()
        self.fitness = 0.0

    def expressGenome(self):
        expression = 0.0

        for index, trait in enumerate(self.genome.normalized_rna):

            if trait == '+':
                try:
                    expression += self.genome.normalized_rna[index + 1]
                except:
                    pass

            if trait == '-':
                try:
                    expression -= self.genome.normalized_rna[index + 1]
                except:
                    pass

            if trait == '*':
                try:
                    expression *= self.normalized_rna[index + 1]
                except:
                    pass

            if trait == '\/':
                try:
                    expression /= self.normalized_rna[index + 1]
                except:
                    pass

        return expression