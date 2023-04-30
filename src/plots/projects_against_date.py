import matplotlib.pyplot as plt
import numpy as np
from numpy.core._multiarray_umath import arange
from peewee import *
from scipy.optimize import curve_fit

from src.models.models import pg_db_schema
from src.utils import configurator


def objective(x1, a1, b1):
    return a1 * x1 + b1


sql1 = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
       "FROM {sch}.tempdifftextanalysis " \
       "GROUP BY txn_month order by txn_month ".format(sch=pg_db_schema)

sql2 = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
       "FROM {sch}.tempdifftextanalysis where primitives = '' " \
       "GROUP BY txn_month order by txn_month ; ".format(sch=pg_db_schema)

sql3 = "SELECT date_trunc('month', commitdatumtijd) AS txn_month, count(*) as monthly_sum " \
       "FROM {sch}.tempdifftextanalysis where primitives != '' " \
       "GROUP BY txn_month order by txn_month ; ".format(sch=pg_db_schema)

if __name__ == '__main__':
    params_for_db = configurator.get_database_configuration()
    connection = PostgresqlDatabase('multicore', user=params_for_db.get('user'), password=params_for_db.get('password'),
                                    host='localhost', port=params_for_db.get('port'))

    cursor = connection.execute_sql(sql1)
    line_data_1 = []
    for (date, counter) in cursor.fetchall():
        year = date.strftime("%Y")
        month = date.strftime("%m")
        line_data_1.append((year + '-' + month, counter / 10))

    line_data_1 = dict(line_data_1)

    cursor = connection.execute_sql(sql3)
    line_data_2 = []
    for (date, counter) in cursor.fetchall():
        year = date.strftime("%Y")
        month = date.strftime("%m")
        line_data_2.append((year + '-' + month, counter))

    line_data_2 = dict(line_data_2)
    x_ax_labels = []
    x_ax_numbers = []
    line1 = []
    line2 = []
    line3 = []
    i = 0
    for year in [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023]:
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            date = str(year) + '-' + month
            l1data = line_data_1.get(date)
            l2data = line_data_2.get(date)
            x_ax_labels.append(date)
            x_ax_numbers.append(i)
            i += 1
            line1.append(l1data)
            line2.append(l2data)
            line3.append(100 * l2data / l1data if (l1data is not None and l1data != 0) and l1data is not None else None)

    fig, ax1 = plt.subplots(layout='constrained')

    ax1.scatter(x_ax_labels, line1, color='r')
    ax1.set_xticks(np.arange(0, len(x_ax_labels), 12))
    ax1.set_xticklabels(x_ax_labels[::12], rotation=45)
    ax1.set_xlabel('Months')

    ax1.set_ylabel('Nr of diff Lines', color='r')
    ax2 = ax1.twinx()
    ax2.scatter(x_ax_labels, line3, color='b')
    ax2.set_ylabel('Percentage of lines with mc primitives', color='b')

    l = len(x_ax_labels)

    x, y = x_ax_numbers[6:l - 8], line3[6:l - 8]
    popt = curve_fit(f=objective, xdata=x, ydata=y)
    a, b = popt[0]
    print('y = %.5f * x + %.5f' % (a, b))
    x_line = arange(min(x), max(x), 1)
    # calculate the output for the range
    y_line = objective(x_line, a, b)
    # create a line plot for the mapping function
    plt.plot(x_line, y_line, '--', color='b')

    plt.show()
