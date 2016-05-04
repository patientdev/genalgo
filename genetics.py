from random import randint, choice as randomchoice
import settings


class Population(object):

    def __init__(self):
        self.genomes = [Genome() for genome in range(settings.POPULATION_SIZE)]
        self.phenomes = [Phenome(genome=genome) for genome in self.genomes]


class Genome(object):

    def __init__(self):
        self.genes = self.seedGenome()
        self.sequence = ''.join(self.genes)
        self.mRNA = map(self.translateCodon, self.genes)
        self.normalized_rna = self.editRNA()
        self.fitness = 0.0

    def seedGenome(self, genes={}):
        '''Returns a genome as an (inherently) ordered list of genes of length given by static GENOME_LENGTH variable'''
        genome = [randomchoice(settings.GENES.keys()) for x in range(settings.GENOME_LENGTH)]

        return genome

    def translateCodon(self, codon=''):

        gene = settings.GENES[codon]

        return gene

    def editRNA(self, mRNA=[]):
        '''
        We need the sequence to be operator -> number -> operator -> ...
        because the phenome will begin its expression at 0.0

        And we can't allow division by zero, so the sequence `/ -> 0` will be
        replaced by `* -> 0`
        '''

        if not mRNA:
            mRNA = self.mRNA

        normalized_rna = self.formatSequenceOrder(mRNA)
        rationalized_rna = self.baseEditZeroDivisorFragments(normalized_rna)

        return rationalized_rna

    def formatSequenceOrder(self, mRNA=[]):
        normalized_rna = []
        need_operator = True

        for codon in mRNA:
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

        try:
            if not isinstance(normalized_rna[-1], int):
                del normalized_rna[-1]
        except IndexError:
            pass

        return normalized_rna

    def baseEditZeroDivisorFragments(self, normalized_rna=[]):
        for i in range(len(normalized_rna) - 1):
            if normalized_rna[i] is '/' and normalized_rna[i + 1] == 0:
                normalized_rna[i] = '*'

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