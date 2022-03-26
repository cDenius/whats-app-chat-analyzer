import numpy as np
import datetime
from plotting import plot_histogram

WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def weekday_analaysis(authors, masks, times, plot=False):
    print("\nOn which weekday are they writing")
    for i, author in enumerate(authors):
        a_times = times[masks[i]]
        days = np.zeros(7, dtype=int)
        for t in a_times:
            # zero = Monday
            days[datetime.datetime(2000+t[2], t[1], t[0]).weekday()] += 1
        print(author, list(zip(WEEKDAYS, days)))


def time_histogram(authors, masks, times, messages, m_length=False, plot=True):
    if m_length:
        print("\nCharacters Histogram")
    else:
        print("\nMessage Histogram")

    first_m, first_y = times[0, 1], times[0, 2]
    last_m, last_y = times[-1, 1], times[-1, 2]

    months = {(last_y * 13 + last_m): 0}

    while first_m != last_m or first_y != last_y:
        months[(first_y * 13 + first_m)] = 0
        if first_m == 12:
            first_y += 1
        first_m = first_m + 1 if first_m < 12 else 1

    for time in times:
        months[(time[2] * 13 + time[1])] += 1

    for key in sorted(months):
        print(f"{key % 13}.{key // 13} - {months[key]}")

    if plot:
        plot_histogram(months)
