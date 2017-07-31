import matplotlib.pyplot as plt
import numpy as np


def stackedbar(df, index, columns, xlabel, ylabel):
    """ Create stacked bar plot """
    f, ax1 = plt.subplots(1, figsize=(12, 6))
    bar_width = 0.75
    colors = "bgrcmykw"  # List of different colors
    color_index = 0
    bar_l = [i + 1 for i in range(len(df[columns[0]]))]
    tick_pos = [i + (bar_width / 2) for i in bar_l]
    total = np.zeros(len(df[columns[0]]))

    # Loop through list of columns and add plots
    for c in columns:
        ax1.bar(bar_l, df[c], width=bar_width, bottom=total, label=c, alpha=0.5, color=colors[color_index])
        color_index += 1  # Increment the color
        total = total + df[c]  # Add data to total so next column is correct

    # Add final stuff
    plt.xticks(tick_pos, index)
    ax1.set_ylabel(ylabel)
    ax1.set_xlabel(xlabel)
    plt.legend(loc='upper left')
    plt.xlim([min(tick_pos) - bar_width, max(tick_pos) + bar_width])