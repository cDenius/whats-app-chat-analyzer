import sys
import re
import numpy as np


def load_chat(file):
    with open(file) as f:
        lines = f.readlines()
    
    # skip end-to-end message
    lines = lines[1:]

    regexp = re.compile(r'[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]\,[0-9][0-9]\:[0-9][0-9]\-')

    data = []
    
    for l in lines:
        if "Sicherheitsnummer" in l or len(l) == 1:
            continue
        if regexp.search(l[:17].replace(" ", "")):
            time, rest = l.split('-', 1)
            author, message = rest.split(':', 1)
        else:
            message = l
        
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
  
    unique_authors, counts = np.unique(authors, return_counts=True)
    print("\nNumber of messages")
    print(dict(zip(unique_authors, counts)))

    masks = [] 
    for author in unique_authors:
        mask = (authors == author)
        masks.append(mask)

    print("\nAverage message length")
    for i, author in enumerate(unique_authors):
        print(author, sum(map(len, messages[masks[i]])) 
                      / len(messages[masks[i]]))



if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        raise ValueError("You need to provide exactly one .txt as an argument")
        
    load_chat(sys.argv[1])