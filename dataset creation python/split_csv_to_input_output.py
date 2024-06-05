# -*- coding: utf-8 -*-
"""
Created on Sun May 26 22:51:29 2024

@author: ronbinyamin
"""
import csv

def split_csv(output_file_path, loads_number, buses_number):
    # Calculate the number of columns for each CSV
    input_columns = 2 * loads_number + 1
    output_columns = 2 * buses_number
    
    # Read the original CSV file
    with open(output_file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    # Split the data into input and output CSVs
    input_data = [row[:input_columns] for row in data]
    output_data = [row[input_columns:input_columns + output_columns] for row in data]

    # Write the input data to input_only.csv
    with open('input_only.csv', 'w', newline='') as input_file:
        writer = csv.writer(input_file)
        writer.writerows(input_data)

    # Write the output data to output_only.csv
    with open('output_only.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output_data)

split_csv(r"C:\Program Files\thesis\dss and data\output.csv",15,41)

