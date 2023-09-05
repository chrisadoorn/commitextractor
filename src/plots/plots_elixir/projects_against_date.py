import matplotlib.pyplot as plt
import numpy as np
from peewee import *
from scipy.optimize import curve_fit
from scipy.special import expit

from src.models.selection_models import pg_db_schema
from src.utils import configurator


def objective_straight_line(x1, a1, b1):
    return a1 * x1 + b1


def objective_quadratic(x1, a1, b1, c1):
    return a1 * x1 * x1 + b1 * x1 + c1


def objective_straight_line_expit(x1, a1, b1):
    z = objective_straight_line(x1, a1, b1)
    return 100 * expit(z)


def with_expit(x):
    return 100 * expit((x / 10) - 5)


def objective_quadratic_2(x1, a1, b1, c1, d1):
    return a1 * x1 * x1 * x1 + b1 * x1 * x1 + c1 * x1 + d1


def create_diagram2():
    sql = """
        SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*), count(*) filter(where count = 0)
        ,count(*) filter(where count > 0), count(*) filter(where count > 0)/count(*)::float*100 as perc
        FROM {sch}."Result_20_commits_date"
        GROUP BY txn_month order by txn_month ;
        """.format(sch=pg_db_schema)

    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    cursor = connection.execute_sql(sql)

    line_data_1 = []
    line_data_2 = []
    for (date, counter, no_mc, mc, perc) in cursor.fetchall():
        year = date.strftime("%Y")
        month = date.strftime("%m")
        line_data_1.append((year + '-' + month, counter))
        line_data_2.append((year + '-' + month, perc))

    line_data_1 = dict(line_data_1)
    line_data_2 = dict(line_data_2)
    x_ax_labels = []
    line1_y_values = []
    line2_y_values = []
    months = create_month_list(2012, 1, 2023, 6)
    zipped = []
    i = 0
    for m in months:
        l1data = line_data_1.get(m)
        l2data = line_data_2.get(m)
        x_ax_labels.append(m)  # alle x as labels
        line1_y_values.append(l1data)
        line2_y_values.append(l2data)
        zipped.append((i, l2data))
        i += 1

    fig, ax1 = plt.subplots(layout='constrained')
    ax1.scatter(x_ax_labels, line1_y_values, color='r')
    ax1.set_xticks(np.arange(0, len(x_ax_labels), 12))
    ax1.set_xticklabels(x_ax_labels[::12], rotation=45)
    ax1.set_xlabel('Months')
    ax1.set_ylabel('Nr of commits', color='r')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('percentage having mc added', color=color)  # we already handled the x-label with ax1
    ax2.scatter(x_ax_labels, line2_y_values, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    chunks_list = chunks(x_ax_labels, 12)
    i = 0
    for chunk in chunks_list:
        y_line = []
        v = 0
        counted = 0
        for (x, y) in zipped:
            if x >= i and x < i + 12 and y > 0:
                v += y
                counted += 1
            if counted > 0:
                average = (v / counted)
            else:
                average = 0
        for x in chunk:
            if average > 0:
                y_line.append(average)
        if average > 0:
            plt.plot(chunk, y_line, '--', color='r', linewidth=1)
            i += 12

    plt.show()


def create_diagram_projects_commits_authors():
    sql = "SELECT id, aantal_commits, naam, total_p, nr_no_mc, nr_mc, perc_mc " \
          "FROM {sch}.projects_commits_authors " \
          "order by aantal_commits ; ".format(sch=pg_db_schema)
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))
    cursor = connection.execute_sql(sql)

    xs = []
    ys = []
    zipped = []
    for (pr_id, aantal_commits, naam, total_p, nr_no_mc, nr_mc, perc_mc) in cursor.fetchall():
        xs += [aantal_commits]
        ys += [round(perc_mc, 2)]
        zipped.append((aantal_commits, round(perc_mc, 2)))

    x_ax_labels = list(range(0, 13000))

    fig, ax1 = plt.subplots(layout='constrained')
    ax1.scatter(xs, ys, color='b')
    ax1.set_xticks(np.arange(0, len(x_ax_labels), 1000))
    ax1.set_xticklabels(x_ax_labels[::1000], rotation=45)
    ax1.set_xlabel('number of commits per project')
    ax1.set_ylabel('percentage authors adding mc')

    chunks_list = chunks(x_ax_labels, 1000)
    i = 0
    for chunk in chunks_list:
        y_line = []
        v = 0
        counted = 0
        for (x, y) in zipped:
            if x >= i and x < i + 1000 and y > 0:
                v += y
                counted += 1
        if counted > 0:
            average = (v / counted)
        else:
            average = 0
        for x in chunk:
            if average > 0:
                y_line.append(average)
        if average > 0:
            plt.plot(chunk, y_line, '--', color='r')
        i += 1000

    plt.show()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def create_diagram_projects_nr_authors():
    sql = "SELECT id, aantal_commits, naam, total_p, nr_no_mc, nr_mc, perc_mc " \
          "FROM {sch}.projects_commits_authors " \
          "order by total_p ; ".format(sch=pg_db_schema)
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))
    cursor = connection.execute_sql(sql)

    xs = []
    ys = []
    zipped = []
    for (pr_id, aantal_commits, naam, total_p, nr_no_mc, nr_mc, perc_mc) in cursor.fetchall():
        xs.append(total_p)
        ys.append(round(perc_mc, 2))
        zipped.append((total_p, round(perc_mc, 2)))
    x_ax_labels = list(range(0, 1200))

    fig, ax1 = plt.subplots(layout='constrained')
    ax1.scatter(xs, ys, color='b')
    ax1.set_xticks(np.arange(0, len(x_ax_labels), 100))
    ax1.set_xticklabels(x_ax_labels[::100], rotation=45)
    ax1.set_xlabel('number of authors per project')
    ax1.set_ylabel('percentage authors adding mc')

    chunks_list = chunks(x_ax_labels, 100)
    i = 0
    for chunk in chunks_list:
        y_line = []
        v = 0
        counted = 0
        for (x, y) in zipped:
            if i <= x < (i + 100) and y > 0:
                v += y
                counted += 1
        if counted > 0:
            average = (v / counted)
        else:
            average = 0
        for x in chunk:
            if average > 0:
                y_line.append(average)
        if average > 0:
            plt.plot(chunk, y_line, '--', color='r')
        i += 100
    plt.show()


def create_month_list(start_year, start_month, end_year, end_month):
    month_list = []
    for year in range(start_year, end_year + 1):
        if year == start_year:
            for month in range(start_month, 13):
                month_list.append(str(year) + '-' + ('0' if month < 10 else '') + str(month))
        elif year == end_year:
            for month in range(1, end_month + 1):
                month_list.append(str(year) + '-' + ('0' if month < 10 else '') + str(month))
        else:
            for month in range(1, 13):
                month_list.append(str(year) + '-' + ('0' if month < 10 else '') + str(month))
    return month_list


if __name__ == '__main__':
    create_diagram_projects_commits_authors()
    create_diagram_projects_nr_authors()
    create_diagram2()
