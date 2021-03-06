import numpy as np
import datetime
from plotting import plot_bars, plot_stacked_bars

WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def weekday_analysis(unique_authors, times, authors, plot=False):
    print("\nOn which weekday are they writing")
    days = np.zeros((7, len(unique_authors)), dtype=int)
    for t, a in zip(times, authors):
        a_index = unique_authors.tolist().index(a)
        d = datetime.datetime(2000+t[2], t[1], t[0]).weekday()
        days[d, a_index] += 1

    for i, author in enumerate(unique_authors):
        print(author)
        for j, wd in enumerate(WEEKDAYS):
            print(wd, days[j, i])
        if plot:
            plot_bars(days[:, i],
                      WEEKDAYS,
                      f"When does {author} writes messages")


def time_histogram(unique_authors, times, authors, messages, plot=True):
    first_m, first_y = times[0, 1], times[0, 2]
    last_m, last_y = times[-1, 1], times[-1, 2]

    # create empty histograms
    hist_mess = {(last_y * 13 + last_m): [0]*len(unique_authors)}
    hist_char = {(last_y * 13 + last_m): [0]*len(unique_authors)}

    while first_m != last_m or first_y != last_y:
        hist_mess[(first_y * 13 + first_m)] = [0]*len(unique_authors)
        hist_char[(first_y * 13 + first_m)] = [0]*len(unique_authors)
        if first_m == 12:
            first_y += 1
        first_m = first_m + 1 if first_m < 12 else 1

    # fill histograms
    for t, a, m in zip(times, authors, messages):
        a_index = unique_authors.tolist().index(a)
        hist_mess[(t[2] * 13 + t[1])][a_index] += 1
        hist_char[(t[2] * 13 + t[1])][a_index] += len(m)

    grid_mess = np.zeros((len(hist_mess), len(unique_authors)))
    print("\nMessage Histogram")
    for index, key in enumerate(sorted(hist_mess)):
        print(f"{key % 13}.{key // 13} - {hist_mess[key]}")
        grid_mess[index] = hist_mess[key]

    grid_char = np.zeros((len(hist_char), len(unique_authors)))
    print("\nCharacters Histogram")
    for index, key in enumerate(sorted(hist_char)):
        print(f"{key % 13}.{key // 13} - {hist_char[key]}")
        grid_char[index] = hist_char[key]

    if plot:
        plot_stacked_bars(grid_mess,
                          sorted(hist_mess),
                          unique_authors,
                          "Number of Messages send")
        plot_stacked_bars(grid_char,
                          sorted(hist_char),
                          unique_authors,
                          "Number of Characters send")
