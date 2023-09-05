import locale
import matplotlib.pyplot as plt
from peewee import *

from src.models.selection_models import pg_db_schema
from src.utils import configurator


def create_diagram_usage_by_year():
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host=params_for_db.get('host'), port=params_for_db.get('port'))
    sql = ("select jaar, count_all_commit, count_mc_commit, avg_mc_commit from {sch}.compare_jaar order by jaar asc").format(sch=pg_db_schema)

    jaren = []
    all_commits = []
    mc_commits = []
    averages = []
    cursor = connection.execute_sql(sql)
    for (jaar, count_all_commit, count_mc_commit, avg_mc_commit) in cursor.fetchall():
        jaren.append(jaar)
        all_commits.append(count_all_commit - count_mc_commit)
        mc_commits.append(count_mc_commit)
        averages.append(avg_mc_commit)

    # naast elkaar
    # x = np.arange(len(jaren))
    # width = 0.25
    # multiplier = 0
    #
    # means = {'all_commits': tuple(all_commits), 'mc_commits': tuple(mc_commits)}
    # fig, ax = plt.subplots(layout='constrained')
    #
    # for attribute, measurement in means.items():
    #     offset = width * multiplier
    #     rects = ax.bar(x + offset, measurement, width, label=attribute)
    #     ax.bar_label(rects, padding=3)
    #     multiplier += 1

    # enkele bar
    # xpoints = np.array(jaren)
    # ypoints = np.array(all_commits)
    # plt.bar(xpoints, ypoints, color='red')

    # stacked bars
    fig, ax = plt.subplots()
    ax.bar(jaren, mc_commits, label="Multicore")
    ax.bar(jaren, all_commits, bottom=mc_commits, label="Other")
    ax.set_ylabel("Number of file changes (in thousands)")
    ax.legend(loc='upper left', ncols=2)
    # format numbers to show dots
    current_values = plt.gca().get_yticks()
    locale.setlocale(locale.LC_ALL, '')
    plt.gca().set_yticklabels(["{:n}".format(int(x/1000)) for x in current_values])

    # second axis with a line
    ax2 = ax.twinx()
    ax2.plot(jaren, averages)
    ax2.set_ylabel('percentage multicore of all file changes')
    ax2.set_ylim(0, 100)
    ax2.legend(['percentage multicore'], loc="upper right")

    plt.title("Multicore usage throughout the years")
    plt.xlabel("years")

    plt.show()


if __name__ == '__main__':
    create_diagram_usage_by_year()
