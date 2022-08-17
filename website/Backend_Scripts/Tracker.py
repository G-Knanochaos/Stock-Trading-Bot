from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import csv


# ---[CSV INTERACTION]---


def init_csv(user):
    with open(f'AC data/{user}_data.csv', 'w', newline='') as user_csv:
        writer = csv.writer(user_csv)
        writer.writerows([['Date', 'Hours', 'Temperature', 'Cost']])


def write_csv(user, hours, temp, cost, inpdate=None):
    with open(f'AC data/{user}_data.csv', 'a', newline='') as user_csv:
        writer = csv.writer(user_csv)
        if inpdate:
            writer.writerow([pd.to_datetime(inpdate, format='%Y-%m-%d'), hours, temp, cost])
        else:
            writer.writerow([datetime.today().strftime('%Y-%m-%d'), hours, temp, cost])


# ---[GRAPHING]---

def plot_graph(dates, y_vals, y_names, colors, graph_name):
    for y, name, date, color in zip(y_vals, y_names, dates, colors):
        plt.xlabel("Date")
        plt.ylabel(name)
        plt.title(graph_name)
        plt.plot(date, y, label=name, marker='o', linewidth='3', color=color)
        plt.fill_between(date, y, alpha=0.5, color=color)
        plt.legend()
    return plt


def pie_chart(ac_costs, fan_costs, graph_name):
    plt.title(graph_name)
    plt.pie(labels=['AC', 'Fan'], x=[sum(ac_costs), sum(fan_costs)], colors=['b', 'g'], explode=[0, 0.2],
            wedgeprops={'edgecolor': 'black'}, shadow=True, autopct='%1.1f%%')
    return plt


def scatter(hours, temps):
    plt.title('Hours/Temperature AC Scatterplot')
    x, y = np.array(hours), np.array(temps)
    plt.scatter(x, y, alpha=0.75, cmap='BuGn')
    plt.xlabel('Hours')
    plt.ylabel('Temperature')
    return plt


# ---[MAIN]---

def main():
    plot_graph(dates=[['2019-08-03', '2020-08-03', '2021-08-03'], ['2019-08-03', '2020-08-03', '2022-08-03']],
               y_vals=[['8', '7', '5'], ['65', '66', '67']], y_names=['Hours', 'Temperature'],
               colors=['#00A36C', '#088F8F'],
               graph_name='AC Hours and Temperature').show()
    pie_chart([8, 8, 9, 8, 9, 9, 8, 9], [1, 1, 2, 3, 1, 2, 1, 1], 'AC vs Fan Costs').show()
    scatter([2, 4, 7, 5, 8, 4], [65, 54, 76, 65, 67, 63]).show()


if __name__ == '__main__':
    main()
