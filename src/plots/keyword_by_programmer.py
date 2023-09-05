import locale

import matplotlib.pyplot as plt
import numpy as np
from peewee import *

from src.models.selection_models import pg_db_schema
from src.utils import configurator


def create_diagram_keyword_by_programmer():
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host=params_for_db.get('host'), port=params_for_db.get('port'))
    sql = ("select zoekterm, count(zoekterm) as aantal_gebruik, count(distinct auteur) as aantal_programmers "
           "from  {sch}.wijziging_lineage where falsepositive = false and uitgesloten = false "
           "group by zoekterm order by aantal_programmers desc").format(sch=pg_db_schema)

    zoektermen = []
    aantal_zoekterm = []
    aantal_programmeurs = []
    cursor = connection.execute_sql(sql)
    for (zoekterm, count_zoekterm, count_programmer) in cursor.fetchall():
        zoektermen.append(zoekterm)
        aantal_zoekterm.append(count_zoekterm)
        aantal_programmeurs.append(count_programmer)

    fig, ax = plt.subplots()
    plt.title("Usage of keywords")
    plt.xlabel("Used by programmers")
    plt.ylabel("Keyword usages")

    ax.scatter(aantal_programmeurs, aantal_zoekterm)

    # format numbers to show dots
    locale.setlocale(locale.LC_ALL, '')
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:n}".format(int(x)) for x in current_values])
    current_values = plt.gca().get_xticks()
    plt.gca().set_xticklabels(["{:n}".format(int(x)) for x in current_values])

    z = np.polyfit(aantal_programmeurs, aantal_zoekterm, 1)
    p = np.poly1d(z)
    plt.plot(aantal_programmeurs, p(aantal_programmeurs), color='red')

    plt.show()


if __name__ == '__main__':
    create_diagram_keyword_by_programmer()
