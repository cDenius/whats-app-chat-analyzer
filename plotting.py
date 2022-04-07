import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(values, labels, unique_authors, title=""):
    labels = [f"{x % 13}.{x // 13}" for x in labels]
    for i in range(values.shape[1]):
        lower_end = np.sum(values[:, :i], axis=1)
        plt.bar(labels, values[:, i], bottom=lower_end, edgecolor='white', label=unique_authors[i])
    plt.title(title)
    plt.legend()
    plt.show()
