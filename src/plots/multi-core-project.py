import matplotlib.pyplot as plt
import numpy as np
from peewee import *
import scipy.stats as stats
import math

from src.models.selection_models import pg_db_schema
from src.utils import configurator


def create_diagram_mc_usage_projects():
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host=params_for_db.get('host'), port=params_for_db.get('port'))
    sql = ("select idproject, count_commit,  count_mc_commit, ((avg_commit - avg_mc_commit)  / count_commit) * 100 as percentueel_verschil "
           "from {sch}.compare_project_history where count_commit > 9 and count_mc_commit > 0 order by percentueel_verschil asc").format(sch=pg_db_schema)

    projecten = []
    all_commits = []
    mc_commits = []
    averages = []
    cursor = connection.execute_sql(sql)
    teller = 1
    for (project, count_commit, count_mc_commit, avg_mc_commit) in cursor.fetchall():
        projecten.append(teller)
        all_commits.append(count_commit)
        mc_commits.append(count_mc_commit)
        averages.append(float(avg_mc_commit))
        teller = teller + 1

    # normal distribution
    # mu = 0
    # variance = 1
    # sigma = math.sqrt(variance)
    # x = np.linspace(mu - 3 * sigma, mu + 3 * sigma)
    # plt.plot(averages, stats.norm.pdf(averages, mu, sigma))

    # line
    # xpoints = np.array(projecten)
    # ypoints = np.array(averages)
    #
    # # scatter: toon datapunten
    # # plt.scatter(xpoints, ypoints)
    # plt.plot(ypoints, xpoints)
    #
    # # bereken trendline
    # z = np.polyfit(ypoints, xpoints, 1)
    # p = np.poly1d(z)
    # # toon trendline
    # plt.plot(ypoints, p(ypoints), "r--")
    #
    fig, ax = plt.subplots()
    plt.title("Multi-core usage in Projects")
    plt.xlabel("Median time of usage within the project")
    plt.ylabel("Number of projects")
    # histogram
    frequency_counts = []
    # Define the bins/ranges for the histogram
    bins = [-45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45]

    # Create the histogram
    ax.hist(averages, bins=bins, edgecolor='black', alpha=0.7)

    plt.show()


if __name__ == '__main__':
    create_diagram_mc_usage_projects()
