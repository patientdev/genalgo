POPULATION_SIZE = 100
GENOME_LENGTH = 20
GENES = {
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

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001
ROULETTE_METHOD = 'stochastic_acceptance_roulette'