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
    ax.bar(jaren, mc_commits, label="Multi-core")
    ax.bar(jaren, all_commits, bottom=mc_commits, label="Other")
    ax.set_ylabel("Number of commits")
    ax.legend(loc='upper left', ncols=2)

    # second axis with a line
    ax2 = ax.twinx()
    ax2.plot(jaren, averages)
    ax2.set_ylabel('percentage multi-core of all commits')
    ax2.set_ylim(0, 50)
    ax2.legend(['percentage multi-core'], loc="upper right")

    plt.title("Multi-core usage throughout the years")
    plt.xlabel("years")

    plt.show()


if __name__ == '__main__':
    create_diagram_usage_by_year()
