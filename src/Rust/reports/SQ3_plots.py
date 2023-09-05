import locale
import matplotlib.pyplot as plt
from peewee import *

from src.models.selection_models import pg_db_schema
from src.utils import configurator


def create_diagram_usage_by_year():
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host=params_for_db.get('host'), port=params_for_db.get('port'))

    sql = ("SELECT jaar, count_all_file_changes, count_mc_file_changes, avg_mc_commit "
           "FROM {sch}.compare_jaar WHERE jaar >= 2014 ORDER BY jaar ASC").format(sch=pg_db_schema)

    jaren = []
    all_file_changes = []
    mc_file_changes = []
    averages = []
    cursor = connection.execute_sql(sql)
    for (jaar, count_all_file_changes, count_mc_file_changes, avg_mc_commit) in cursor.fetchall():
        jaren.append(jaar)
        all_file_changes.append(count_all_file_changes - count_mc_file_changes)
        mc_file_changes.append(count_mc_file_changes)
        averages.append(avg_mc_commit)

    # stacked bars
    fig, ax = plt.subplots()
    ax.bar(jaren, mc_file_changes, label="Multi-core")
    ax.bar(jaren, all_file_changes, bottom=mc_file_changes, label="Other")
    ax.set_ylabel("Number of file changes")
    ax.legend(loc='upper left', ncols=2)
    # format numbers to show dots
    current_values = plt.gca().get_yticks()
    locale.setlocale(locale.LC_ALL, '')
    plt.gca().set_yticklabels(["{:n}".format(int(x)) for x in current_values])

    # second axis with a line
    ax2 = ax.twinx()
    ax2.plot(jaren, averages)
    ax2.set_ylabel('percentage multi-core of all file changes')
    ax2.set_ylim(0, 100)
    ax2.legend(['percentage multi-core'], loc="upper right")

    plt.title("Multi-core usage throughout the years")
    plt.xlabel("years")

    plt.show()

def create_plot():
    years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    values = [28, 128, 291, 1185, 1551, 1693, 2533, 7128, 8904, 13092, 12443]

    plt.plot(years, values, marker='o')
    plt.title("Multicore usage over Years")
    plt.xlabel("Years")
    plt.ylabel("Number of file changes containing multicore primitives")
    plt.grid(True)
    plt.show()
if __name__ == '__main__':
    #create_diagram_usage_by_year()
    create_plot()