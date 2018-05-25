import pandas as pd
pd.options.mode.chained_assignment = None
import logging
import csv
import numpy as np
import os
import sys

def open_file(file):
    logging.debug("Entering open file")
    raw_table = pd.read_csv(file, sep=';', encoding='utf-8')
    return raw_table

def save_file(file, name, save_folder):
    logging.debug("Entering writing pandas to file")
    try:
        filepath = "./save/" + save_folder + "/"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        file.to_csv(filepath + name + ".csv", encoding='utf-8', sep=";", quoting=csv.QUOTE_NONNUMERIC)
        print("Wrote %s%s.csv" % (filepath, name))
    except IOError as exception:
        print("Couldn't save the file. Encountered an error: %s" % exception)
    logging.debug("Finished writing: " + name)

def create_random_sample(file):
    """Creates a random sample that is 10 per cent from the original dataframe."""
    percent_selection = np.random.choice([False, True], len(file), p=[0.90, 0.10])
    df_sample = file[percent_selection]
    df_rest = file.drop(df_sample.index)
    return df_sample, df_rest

def combine_individual_samples(sample_folder, name, save_folder_name):
    filelist = read_folder_contents(sample_folder)
    merged_csvs = []
    for f in filelist:
        df = open_file(sample_folder + "/" + f)
        merged_csvs.append(df)
    final_csv = pd.concat(merged_csvs)
    save_file(final_csv, name, save_folder_name)

def read_arguments(arguments):
    if len(arguments) == 2:
        return arguments[1]
    else:
        return None

def read_folder_contents(path_to_files):
    filelist = os.listdir(path_to_files)
    return filelist

def main(folder_to_read):
    if folder_to_read:
        files = read_folder_contents(folder_to_read)
        x = 0
        for f in files:
            x += 1
            df = open_file(folder_to_read + "/" + f)
            df_sample10, df_rest90 = create_random_sample(df)
            print("Sample length: %s" % len(df_sample10))
            print("Rest length: %s" % len(df_rest90))
            sample__name = "Sample10_" + str(x)
            rest_name = "Rest90_" + str(x)
            save_file(df_sample10, sample__name, "sample10")
            save_file(df_rest90, rest_name, "rest90")
        combine_individual_samples("./save/sample10/", "merged10", "merged10")
        combine_individual_samples("./save/rest90/", "merged90", "merged90")
    else:
        print("You didn't give a folder containing the data.")


if __name__ == "__main__":
    folder_to_read = read_arguments(sys.argv)
    main(folder_to_read)