from pylab import plt
import numpy as np
import matplotlib.gridspec as gridspec

import operator
import itertools
import argparse

from behavior import backup


def plot(data):

    gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1.5])
    plt.figure(figsize=(9, 4))

    # -------------------------- Nationalities hist ---------------------------------- #
    ax = plt.subplot(gs[:, 0])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(length=0)
    plt.title("Nationality")

    # data
    dic_nationality = {}
    for n in np.unique(data.nationality):
        dic_nationality[n] = np.sum(data.nationality == n)
    nationalities = sorted(dic_nationality.items(), key=operator.itemgetter(1))
    labels = [i[0].capitalize() for i in nationalities]
    labels_pos = np.arange(len(labels))
    values = [round((i[1] / len(data.age)) * 100, 2) for i in nationalities]

    # text
    ax.set_yticks(labels_pos)
    ax.set_yticklabels(labels)
    ax.set_xticks([])
    for i, v in enumerate(values):
        ax.text(v + 1, i - 0.05, "{:.2f}%".format(v))

    # create
    ax.barh(labels_pos, values, edgecolor="white", align="center", alpha=0.5)

    # -------------------------- Gender pie ---------------------------------- #

    ax = plt.subplot(gs[0, 1])
    ax.axis('equal')
    plt.title("Gender")

    # get data
    genders = np.unique(data.gender)
    labels = [i.capitalize() for i in genders]
    values = [np.sum(data.gender == i) for i in genders]

    # create
    ax.pie(values,
           labels=labels, explode=(0.01, 0.05), autopct='%1.1f%%',
           startangle=90, shadow=False)
    # -------------------------- Age hist ---------------------------------- #
    ax = plt.subplot(gs[1, 1])
    plt.title("Age", y=1.05)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(length=0)

    # get data
    n_ages = len(data.age)
    ages = [list(i[1]) for i in itertools.groupby(sorted(data.age), lambda x: x // 10)]
    decades = ["{}0-{}9".format(int(i[0] / 10), int(i[0] / 10)) if i[0] >= 20 else "18-19" for i in ages]
    decades_pos = np.arange(len(decades))
    values = np.array([round((len(i) / n_ages) * 100) for i in ages])

    # text
    ax.set_xticks(decades_pos)
    ax.set_xticklabels(decades)
    ax.set_yticks([])
    for i, v in enumerate(values):
        ax.text(i - 0.1, v + 1, "{}%".format(v))
    ax.text(3.5, 20, "Mean: {:.2f} $\pm$ {:.2f} (SD)".format(np.mean(data.age), np.std(data.age)))

    # create
    ax.bar(decades_pos, values, edgecolor="white", align="center", alpha=0.5)

    plt.tight_layout()

    plt.savefig("fig/demographics.pdf")
    plt.show()


def run(force):

    data = backup.get_user_data(force)

    print("\nThere is a total of {} users.".format(len(data.age)))

    print("******* Age ********")
    print("Average age: {:.2f} ".format(np.mean(data.age)))
    print("Std age: {:.2f}".format(np.std(data.age)))
    print("Min age: {}".format(np.min(data.age)))
    print("Max age: {}".format(np.max(data.age)))
    print("******* Nationalities ********")
    for n in np.unique(data.nationality):
        print(n, np.sum(data.nationality == n))
    print("******* Gender ********")
    for g in np.unique(data.gender):
        print("{}: {}".format(g, np.sum(data.gender == g)))

    plot(data)
