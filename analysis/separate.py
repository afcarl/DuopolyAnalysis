# DuopolyAnalysis
# Copyright (C) 2018  Aurélien Nioche, Basile Garcia & Nicolas Rougier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import SubplotParams
import matplotlib.gridspec as gridspec
import os


def eeg_like(backup, subplots_positions):

    pst = backup.positions
    prc = backup.prices

    t_max = backup.t_max

    t = np.arange(1, t_max)

    position_max = backup.n_positions - 1

    position_A = pst[1:t_max, 0] / position_max
    position_B = pst[1:t_max, 1] / position_max
    price_A = prc[1:t_max, 0]
    price_B = prc[1:t_max, 1]

    color_A = "orange"
    color_B = "blue"

    price_min = backup.p_min
    price_max = backup.p_max

    # Position firm A
    ax = plt.subplot(subplots_positions[0])
    ax.plot(t, position_A, color=color_A, alpha=1, linewidth=1.1)
    ax.plot(t, np.ones(len(t)) * 0.5, color='0.5', linewidth=0.5, linestyle='dashed', zorder=-10)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([0, 1])
    ax.set_ylabel('Pos. A', labelpad=16)
    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    # Add title
    # plt.title("$r={}$".format(backup.parameters.r))

    # Position firm B
    ax = plt.subplot(subplots_positions[1])
    ax.plot(t, position_B, color=color_B, alpha=1, linewidth=1.1)
    ax.plot(t, np.ones(len(t)) * 0.5, color='0.5', linewidth=0.5, linestyle='dashed', zorder=-10)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([0, 1])
    ax.set_ylabel('Pos. B', labelpad=16)
    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    # Price firm A
    ax = plt.subplot(subplots_positions[2])
    ax.plot(t, price_A, color=color_A, alpha=1, linewidth=1.1, clip_on=False)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([price_min, price_max])
    ax.set_ylabel('Price A', labelpad=10)  # , rotation=0)
    ax.set_ylim([price_min, price_max])
    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    # Price firm B
    ax = plt.subplot(subplots_positions[3])
    ax.plot(t, price_B, color=color_B, alpha=1, linewidth=1.1, clip_on=False)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([price_min, price_max])
    ax.set_ylabel('Price B', labelpad=10)  # , rotation=0)
    ax.set_ylim([price_min, price_max])

    ax.set_xlabel("Time", labelpad=10)
    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")


def pos_firmA_over_pos_firmB(backup, subplot_position):

    position_max = backup.n_positions - 1

    pos = backup.positions[-1000:] / position_max

    ax = plt.subplot(subplot_position)

    ax.scatter(pos[:, 0], pos[:, 1], color="black", alpha=0.05, zorder=10)
    ax.axvline(0.5, color="0.5", linewidth=0.5, linestyle="--", zorder=1)
    ax.axhline(0.5, color="0.5", linewidth=0.5, linestyle="--", zorder=1)

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks((0, 0.5, 1))
    plt.yticks((0, 0.5, 1))

    plt.xlabel("Position A")
    plt.ylabel("Position B")

    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    # plt.title("$r={:.2f}$".format(backup.parameters.r))
    ax.set_aspect(1)

    return ax


def plot(backup, fig_name=None, subplot_spec=None):

    n_rows, n_cols = 1, 2

    # Width ratios of the two columns (we expect the right column to be twice larger than the left one)
    width_ratios = [1, 2]

    if not subplot_spec:

        # Create the figure object
        plt.figure(figsize=(6, 3.5))

        # Separate the frame in two columns (1: 1 row, 2: 2 columns)
        gs = gridspec.GridSpec(
            1,
            2,
            width_ratios=width_ratios,
            # wspace=0.4
        )

    else:
        gs = gridspec.GridSpecFromSubplotSpec(
            nrows=n_rows, ncols=n_cols, subplot_spec=subplot_spec,
            width_ratios=width_ratios, wspace=0.4)

    # Plot the sub-figure on left
    ax = pos_firmA_over_pos_firmB(backup, subplot_position=gs[0])

    # Create sub-rows on the right
    n_sub_row = 4
    gs = gridspec.GridSpecFromSubplotSpec(n_sub_row, 1, subplot_spec=gs[1])
    subplots_positions = [gs[j, 0] for j in range(n_sub_row)]

    # Plot the 4 sub-figures on the right
    eeg_like(backup=backup, subplots_positions=subplots_positions)

    if not subplot_spec:
        ax.text(0.5, 1.5, '$r$ = {:.2f}'.format(backup.r), horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes)

        plt.tight_layout()

    if fig_name is not None:

        # Create directories if not already existing
        os.makedirs(os.path.dirname(fig_name), exist_ok=True)

        # Save fig
        plt.savefig(fig_name)
        plt.close()

    else:
        if not subplot_spec:
            plt.show()
            plt.close()
