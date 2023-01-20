import pandas as pd

def read_2_array():
    file = pd.read_csv("data/progress/progress_file.csv")
    arr = []
    for i in file:
       arr.append(file[i].values[0])

    return arr

def update_progress(level:str, flag:bool):
    file = pd.read_csv("data/progress/progress_file.csv")
    file.loc[0,level] = flag
    file.to_csv('data/progress/progress_file.csv', index=False)