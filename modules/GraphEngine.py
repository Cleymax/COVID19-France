#!/usr/bin/env python
# coding: utf-8

# Twitter: @xrths
# www.xrths.fr

# Importation des librairies.
import matplotlib

from modules.ConfigEngine import get_config

matplotlib.matplotlib_fname()
'/etc/matplotlibrc'
matplotlib.use('Agg')
import csv
import matplotlib.pyplot as plt
import datetime

directory = get_config('System', 'directory')


def make_graph():
    days = []
    total_cases = []
    hospitalization_cases = []
    severe_cases = []
    dead_cases = []
    recovered_cases = []
    sick_cases = []

    with open(directory + 'data/graphData.txt', 'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=',')
        for row in plots:
            days.append(int(row[0]))
            total_cases.append(int(row[1]))
            hospitalization_cases.append(int(row[2]))
            severe_cases.append(int(row[3]))
            dead_cases.append(int(row[4]))
            recovered_cases.append(int(row[5]))
            sick_cases.append(int(row[1]) - (int(row[4]) + int(row[5])))

    plt.style.use('seaborn-talk')

    # plt.plot(totalCases, label=u'Cas totaux confirmés', marker='o',color = 'darkorange', linewidth = 4)

    plt.plot(sick_cases, label=u'Population activement malade', marker='o', color='darkorange', linewidth=4)

    plt.plot(hospitalization_cases, label=u'Population activement hospitalisée', marker='o', color='indianred',
             linewidth=4)

    plt.plot(severe_cases, label=u"Population en réanimation", marker='o', color='maroon', linewidth=4)

    plt.plot(recovered_cases, label=u'Population guérie', marker='o', color='yellowgreen', linewidth=4)

    plt.plot(dead_cases, label=u"Population décédée", marker='o', color='dimgray', linewidth=4)

    now = datetime.now()
    # plt.ylabel(u'Graphique généré le ' + currentDT.strftime("%d-%m-%Y %H:%M:%S") + ' Par @COVID_France', fontsize = 7)
    plt.xlabel(u'Jours à partir du Mardi 17 Mars 2020 - [Confinement]')
    plt.title(u'AVANCÉE DU COVID-19 EN FRANCE\n' + now.strftime("%d") + u' Avril 2020', fontweight='bold')
    plt.legend(prop={'size': 11}, labelspacing=1.1)
    plt.grid(color='black', linestyle='dashed', linewidth=1)

    plt.savefig(directory + 'data/graphIMG.png', format='png', dpi=200)


def save_graph_data(total_cases, sick_cases, severe_cases, dead_cases, recovered_cases):
    graph_data = open(directory + 'data/graphData.txt', 'a')
    graph_data.write(
        "0," + str(total_cases) + "," + str(sick_cases) + "," + str(severe_cases) + "," + str(dead_cases) + "," + str(
            recovered_cases) + "\n")
    graph_data.close()
