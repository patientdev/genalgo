import numpy
import matplotlib.pyplot as pyplot
import sqlite3 as db

# Get info from db
conn = db.connect('results.db')
conn.row_factory = db.Row
c = conn.cursor()

averages = c.execute('SELECT given_number, avg(duration) from genalgo_results WHERE roulette_method = "stochastic_acceptance_roulette" group by given_number').fetchall()

ind = numpy.arange(len(averages))
width = 0.1

fig, ax = pyplot.subplots()
rects = ax.bar(ind, [r[1] for r in averages], width, color='cornflowerblue')

# add some text for labels, title and axes ticks
ax.set_xlabel('Desideratum')
ax.set_ylabel('Average duration')
ax.set_title('Average time till desideratum')
ax.set_xticks(ind + (width/2))
ax.set_xticklabels((result['given_number'] for result in averages), horizontalalignment='right')
ax.set_xlim(-width)

fig.savefig('figures/avg.png')