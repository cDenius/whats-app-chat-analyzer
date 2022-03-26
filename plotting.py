import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(months):
    labels = []
    heights = []
    for key in sorted(months):
        labels.append(f"{key % 13}.{key // 13}")
        heights.append(months[key])

    y_pos = np.arange(len(heights))

    plt.bar(y_pos, heights)
    plt.xticks(y_pos, labels)
    plt.show()
