import sys
import re
import pandas as pd


def load_chat(file):
    with open(file) as f:
        lines = f.readlines()
    
    # skip end-to-end message
    lines = lines[1:]

    regexp = re.compile(r'[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]\,[0-9][0-9]\:[0-9][0-9]\-')
    df = pd.DataFrame(columns=["time", "author", "message"])
    
    
    for l in lines:
        if "Sicherheitsnummer" in l or len(l) == 1:
            continue
        if regexp.search(l[:17].replace(" ", "")):
            time, rest = l.split('-', 1)
            author, message = rest.split(':', 1)
        else:
            message = l
        
        df = df.append({"time":time, 
                        "author": author, 
                        "message": message}, 
                       ignore_index=True
                       )
        print(time, author, message)

    print(df.author.value_counts())


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".txt"):
        raise ValueError("You need to provide exactly one .txt as an argument")
        
    load_chat(sys.argv[1])