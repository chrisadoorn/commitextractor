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
    sql = " select author_id, count(bz.zoekterm) " \
          " from test.bestandswijziging_zoekterm bz, " \
          " test.bestandswijziging b, " \
          " test.commitinfo ci " \
          " where bz.idbestandswijziging = b.id " \
          " and b.idcommit = ci.id " \
          " and bz.falsepositive = 'False'"\
          " group by author_id".format(sch=pg_db_schema)


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


if __name__ == '__main__':
    create_histogram()
