import sys
import re
import numpy as np
import datetime


WEEKDAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def load_chat(file):
    with open(file) as f:
        lines = f.readlines()

    # skip end-to-end message
    lines = lines[1:]

    regexp = re.compile(r'[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]'
                        + r'\,[0-9][0-9]\:[0-9][0-9]\-')

    data = []

    for line in lines:
        if "Sicherheitsnummer" in line or len(line) == 1:
            continue
        if regexp.search(line[:17].replace(" ", "")):
            time, rest = line.split('-', 1)
            author, message = rest.split(': ', 1)

        else:
            data[-1][-1] += line

        date, clock = time.replace(" ", "").split(",")
        d, m, y = date.split(".")
        hr, mn, = clock.split(":")

        data.append([int(d),
                     int(m),
                     int(y),
                     int(hr),
                     int(mn),
                     author[1:],
                     message]
                    )

        # print(time, author, message)

    data = np.array(data)
    times = np.array(data[:, :5], dtype=int)
    authors = np.array(data[:, 5], dtype=str)
    messages = np.array(data[:, 6], dtype=str)

    for m in messages:
        print(m)

    unique_authors, counts = np.unique(authors, return_counts=True)
    print("\nNumber of messages")
    print(dict(zip(unique_authors, counts)))

    masks = []
    for author in unique_authors:
        mask = (authors == author)
        masks.append(mask)

    print("\nAverage message length (in char)")
    for i, author in enumerate(unique_authors):
        print(author, sum(map(len, messages[masks[i]]))
              / len(messages[masks[i]]))

    print("\nOn which weekday are they writing")
    for i, author in enumerate(unique_authors):
        a_times = times[masks[i]]
        days = np.zeros(7, dtype=int)
        for t in a_times:
            # zero = Monday
            days[datetime.datetime(2000+t[2], t[1], t[0]).weekday()] += 1
        print(author, list(zip(WEEKDAYS, days)))


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        raise ValueError("You need to provide exactly one .txt as an argument")

    load_chat(sys.argv[1])
