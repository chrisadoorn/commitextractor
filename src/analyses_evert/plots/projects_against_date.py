import matplotlib.pyplot as plt
import numpy as np
from peewee import *
from scipy.optimize import curve_fit

from src.models.selection_models import pg_db_schema
from src.utils import configurator


def objective_straight_line(x1, a1, b1):
    return a1 * x1 + b1


def objective_quadratic(x1, a1, b1):
    return a1 * x1 * x1 + b1


def objective_quadratic_2(x1, a1, b1, c1):
    return a1 * x1 * x1 * x1 + b1 * x1 * x1 + c1


sql1 = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
       "FROM {sch}.tempdifftextanalysis " \
       "GROUP BY txn_month order by txn_month ".format(sch=pg_db_schema)

sql2 = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
       "FROM {sch}.tempdifftextanalysis where primitives = '' " \
       "GROUP BY txn_month order by txn_month ; ".format(sch=pg_db_schema)

sql3 = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
       "FROM {sch}.tempdifftextanalysis where primitives != '' " \
       "GROUP BY txn_month order by txn_month ; ".format(sch=pg_db_schema)


def create_diagram2():
    sql = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
          "FROM {sch}.commitinfo " \
          "GROUP BY txn_month order by txn_month ; ".format(sch=pg_db_schema)
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    cursor = connection.execute_sql(sql)

    line_data_1 = []
    for (date, counter) in cursor.fetchall():
        year = date.strftime("%Y")
        month = date.strftime("%m")
        line_data_1.append((year + '-' + month, counter))

    line_data_1 = dict(line_data_1)

    x_ax_labels = []
    line1_y_values = []
    months = create_month_list(2012, 1, 2023, 6)
    for m in months:
        l1data = line_data_1.get(m)
        if l1data is None:
            l1data = 0
        x_ax_labels.append(m)  # alle x as labels
        line1_y_values.append(l1data)

    fig, ax1 = plt.subplots(layout='constrained')
    ax1.scatter(x_ax_labels, line1_y_values, color='r')
    ax1.set_xticks(np.arange(0, len(x_ax_labels), 12))
    ax1.set_xticklabels(x_ax_labels[::12], rotation=45)
    ax1.set_xlabel('Months')

    l = len(months)
    popt = curve_fit(f=objective_quadratic_2, xdata=range(0, l), ydata=line1_y_values)
    a, b, c = popt[0]
    print('y = %.5f * x + %.5f' % (a, b))
    x_line = range(0, l)
    # calculate the output for the range
    y_line = objective_quadratic_2(x_line, a, b, c)
    ax1.set_ylabel('Nr of commits', color='r')
    # create a line plot for the mapping function
    plt.plot(x_line, y_line, '--', color='b')
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
    create_diagram2()
