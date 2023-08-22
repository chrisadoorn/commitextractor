#SQ.2 What is the correlation between multi-core programming primitives and the percentage of programmers using them?


import matplotlib.pyplot as plt
import numpy as np
from peewee import *
from src.models.selection_models import pg_db_schema
from src.utils import configurator

def create_histogram():
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host=params_for_db.get('host'), port=params_for_db.get('port'))

    #zoektermen en count van auteurs
    sql = " select bz.zoekterm, count(author_id) " \
          " from test.bestandswijziging_zoekterm bz, " \
          " test.bestandswijziging_zoekterm b, " \
          " test.commitinfo ci " \
          " where bz.idbestandswijziging = b.id " \
          " and b.id = ci.id " \
          " and bz.falsepositive = 'False'"\
          " group by bz.zoekterm".format(sch=pg_db_schema)


    cursor = connection.execute_sql(sql)

    frequency_counts = []

    for (zoekterm, frequencyCount) in cursor.fetchall():
        frequency_counts.append(frequencyCount)

    # Define the bins/ranges for the histogram
    bins = [0, 10, 20, 30, 40, 50, 100]

    # Create the histogram
    plt.hist(frequency_counts, bins=bins, edgecolor='black', alpha=0.7)

    # Add labels and title
    plt.xlabel('Frequency Count')
    plt.ylabel('Number of Programmers')
    plt.title('Distribution of Programmers by Multicore Code Primitive')

    # Show the plot
    plt.show()


#generating a scatter plot with a trendline  representing the relationship between the number of unique authors in a project
#and the percentage of multi-core authors in the same project
#Set y-axis limits to prevent the trendline from going negative
def create_scatter_plot():
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host=params_for_db.get('host'), port=params_for_db.get('port'))
    sql = "select unieke_auteurs, comparatio " \
          "from {sch}.sq1_compare " \
          "where projectid > 0 and unieke_auteurs > 0 order by unieke_auteurs ASC".format(sch=pg_db_schema)

    auteurs = []
    comparatios = []
    cursor = connection.execute_sql(sql)
    for(auteur, comparatio) in cursor.fetchall():
        auteurs.append(auteur)
        comparatios.append(comparatio)

    # x-axis: unieke auteurs
    # y-axis: percentage multicore

    xpoints = np.array(auteurs)
    ypoints = np.array(comparatios)

    plt.title("Distibution of multi-core programmers by Project")
    plt.xlabel("Authors in Project")
    plt.ylabel("Percentage Multi-core Authors in Project")
    plt.xscale('log')

    # Set y-axis limits to prevent the trendline from going negative
    plt.ylim(0, max(ypoints) + 5)  # You can adjust the upper limit as needed

    # scatter: toon datapunten
    plt.scatter(xpoints, ypoints)
    # bereken trendline
    z = np.polyfit(xpoints, ypoints, 1)
    p = np.poly1d(z)
    # toon trendline
    plt.plot(xpoints, p(xpoints), "r--")

    # toon figuur
    plt.show()

if __name__ == '__main__':
    create_histogram()
    create_scatter_plot()