import numpy
import matplotlib.pyplot as pyplot
import sqlite3 as db

# Get info from db
with db.connect('results.db') as conn:
    conn.row_factory = db.Row
    c = conn.cursor()

    generation_averages = c.execute('SELECT given_number, avg(generations) from genalgo_results WHERE roulette_method = "stochastic_acceptance_roulette" group by given_number').fetchall()
    generations = c.execute('SELECT given_number, generations from genalgo_results WHERE roulette_method = "stochastic_acceptance_roulette"').fetchall()


gens_collection = {}
for r in generations:
    desideratum = r[0]
    try:
        gens_collection[desideratum].append(r[1])
    except KeyError:
        gens_collection[desideratum] = [r[1]]

variance = [numpy.var(gens_collection[desideratum]) for desideratum in gens_collection]

ind = numpy.arange(len(generation_averages))
width = 0.8

fig, ax = pyplot.subplots()
rects = ax.bar(ind, [result[1] for result in generation_averages], width=width, yerr=variance, color='cornflowerblue')

# add some text for labels, title and axes ticks
ax.set_xlabel('Desideratum')
ax.set_ylabel('Average # of generation')
ax.set_title('Average # of generations till desideratum')
ax.set_xticks(ind + (width / 2))
ax.set_xticklabels((result['given_number'] for result in generation_averages), horizontalalignment='center')
ax.set_xlim(-width)

fig.savefig('figures/generations_till_desideratum.png')