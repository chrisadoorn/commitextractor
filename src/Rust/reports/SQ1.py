#SQ.1 How is the usage of multi-core programming primitives distributed among programmers?

#number of authors and file changes
"""select count(distinct(ci.author_id)), count(b.id)
from test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id"""

#number of MC-file changes
"""select count(id)
from test.bestandswijziging_zoekterm
where falsepositive = 'False'"""

#number of MC-authors and file changes
"""select count(distinct(ci.author_id)), count(b.id)
from test.bestandswijziging_zoekterm bz,
     test.bestandswijziging b,
	 test.commitinfo ci
where b.idcommit = ci.id
	  and bz.id = b.id
	  and bz.falsepositive = 'False'"""


# a histogram that visualizes how many programmers fall within each MC-frequency count range

import matplotlib.pyplot as plt
import numpy as np
from peewee import *
from src.models.selection_models import pg_db_schema
from src.utils import configurator

params_for_db = configurator.get_database_configuration()
connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                host=params_for_db.get('host'), port=params_for_db.get('port'))

#auteurs en hun count van zoektermen
sql = " select ci.author_id, count(bz.id) " \
      " from test.bestandswijziging_zoekterm bz, " \
      " test.bestandswijziging_zoekterm b, " \
	  " test.commitinfo ci " \
      " where bz.idbestandswijziging = b.id " \
      " and b.id = ci.id " \
      " group by author_id".format(sch=pg_db_schema)


cursor = connection.execute_sql(sql)

frequency_counts = []

for (auteur, frequencyCount) in cursor.fetchall():
    frequency_counts.append(frequencyCount)

# Define the bins/ranges for the histogram
bins = [0, 10, 20, 30, 40, 50, 100]

# Create the histogram
plt.hist(frequency_counts, bins=bins, edgecolor='black', alpha=0.7)

# Add labels and title
plt.xlabel('Frequency Count')
plt.ylabel('Number of Programmers')
plt.title('Distribution of Programmers by Multicore Code Usage Frequency')

# Show the plot
plt.show()
