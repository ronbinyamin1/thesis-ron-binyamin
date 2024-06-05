import numpy as np
import pandas as pd
import random
import math

def normalize(arr, val_min, val_max):
    norm_arr = []
    diff = val_max - val_min
    diff_arr = arr.max() - arr.min()
    for i in arr:
        temp = (((i - arr.min()) * diff) / diff_arr) + val_min
        norm_arr.append(temp)
    return norm_arr

def save_to_csv(concatenated_vector, file_path):
    pd.DataFrame(concatenated_vector).to_csv(file_path, index=False, header=False)

def generate_and_save_profiles(number_of_years, number_of_loads, csv_file_path, csv_save_path_prefix):
    data = pd.read_csv(csv_file_path, header=None)
    samples = data.iloc[:, 0].values
    number_of_sampling = len(samples)
    mu_arr = np.arange(50, 100, 0.25)

    for load_number in range(1, number_of_loads + 1):
        loadprofile = np.zeros((number_of_years, number_of_sampling))
        loadprofile_scale = np.zeros((number_of_years, number_of_sampling))

        for e in range(number_of_years):
            while True:
                index = random.choice(range(len(mu_arr)))
                if not math.isnan(mu_arr[index]):
                    break

            curr_mu = mu_arr[index]
            mu_arr[index] = np.NaN

            for h in range(number_of_sampling):
                loadprofile[e, h] = samples[h] * (1 + curr_mu * abs(samples[h])) / np.log(1 + curr_mu)



            loadprofile_scale = normalize(loadprofile, min(samples), max(samples))

        concatenated_vector = [item for sublist in loadprofile_scale for item in sublist]
        filename = f"{csv_save_path_prefix}{load_number}.csv"
        save_to_csv(concatenated_vector, filename)
        print(f"Data saved to {filename}")
        
    for load_number in range(1, number_of_loads + 1):
        loadprofile = np.zeros((number_of_years, number_of_sampling))
        loadprofile_scale = np.zeros((number_of_years, number_of_sampling))

        for e in range(number_of_years):
            while True:
                index = random.choice(range(len(mu_arr)))
                if not math.isnan(mu_arr[index]):
                    break

            curr_mu = mu_arr[index]
            mu_arr[index] = np.NaN

            for h in range(number_of_sampling):
                loadprofile[e, h] = samples[h] * (1 + curr_mu * abs(samples[h])) / np.log(1 + curr_mu)



            loadprofile_scale = normalize(loadprofile, min(samples), max(samples))

        concatenated_vector = [item for sublist in loadprofile_scale for item in sublist]
        filename = f"{csv_save_path_prefix}_Q{load_number}.csv"
        save_to_csv(concatenated_vector, filename)
        print(f"Data saved to {filename}")
