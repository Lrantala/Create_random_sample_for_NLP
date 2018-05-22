import pandas as pd
pd.options.mode.chained_assignment = None
import logging
import csv
import numpy as np
import os

def open_file(file):
    logging.debug("Entering open file")
    raw_table = pd.read_csv(file, sep=';', encoding='utf-8')
    return raw_table

def save_file(file, name):
    logging.debug("Entering writing pandas to file")
    try:
        filepath = "./save/"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        file.to_csv(filepath + name + ".csv", encoding='utf-8', sep=";", quoting=csv.QUOTE_NONNUMERIC)
    except IOError as exception:
        print("Couldn't save the file. Encountered an error: %s" % exception)
    logging.debug("Finished writing: " + name)

def create_random_sample(file):
    """Creates a random sample that is SAMPLE_SIZE per cent from the original dataframe."""
    percent_selection = np.random.choice([False, True], len(file), p=[0.90, 0.10])
    # percent_selection = np.random.rand(len(file)) < 0.1
    print(percent_selection[1:10])
    df_sample = file[percent_selection]
    df_rest = file.drop(df_sample.index)
    return df_sample, df_rest

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug("Entering main")
    df = open_file("1.csv")
    df_mini = df[1:100]
    df_sample10, df_rest90 = create_random_sample(df)
    #print(df_sample10[1:10])
    #print(df_rest90[1:10])
    print(len(df_sample10))
    print(len(df_rest90))
    save_file(df_sample10, "Sample10")
    save_file(df_rest90, "Rest90")


if __name__ == "__main__":
    main()