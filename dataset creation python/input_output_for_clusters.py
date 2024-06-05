# -*- coding: utf-8 -*-
"""
Created on Sun May 19 13:08:33 2024

@author: ronbinyamin
"""
import sys
import os
import pandas as pd
import dss 
import numpy as np
import re

def extract_arrays_from_csv(csv_file, loads_number, bus_number):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract the first column and save it in v_in array
    v_in = df.iloc[:, 0].to_numpy()

    # Extract the next 2*loads_number columns and save them in x array
    start_idx = 1
    end_idx = start_idx + 2 * loads_number
    x = df.iloc[:, start_idx:end_idx].to_numpy()

    # Extract the next bus_number columns to v_mag array
    start_idx = end_idx
    end_idx = start_idx + bus_number
    v_mag = df.iloc[:, start_idx:end_idx].to_numpy()

    # Extract the next bus_number columns to v_ang array
    start_idx = end_idx
    end_idx = start_idx + bus_number
    v_ang = df.iloc[:, start_idx:end_idx].to_numpy()

    return v_in, x, v_mag, v_ang

def cluster_file_to_array(file_path):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True, header=None)
    
    # Combine the columns into a single 2D array
    array = df.to_numpy()
    
    return array

def convert_decimal_to_letter(value):
    # Define a dictionary to map decimal digits to letters
    decimal_to_letter = {
        1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e',
        6: 'f', 7: 'g', 8: 'h', 9: 'i'
    }
    
    # Remove any letters from the input string
    cleaned_value = re.sub(r'[^\d\.]', '', str(value))
    
    # Separate the integer and decimal parts
    integer_part, decimal_part = cleaned_value.split('.')
    
    # Convert the decimal part to a letter
    letter = decimal_to_letter[int(decimal_part)]
    
    # Combine the integer part with the letter and prepend 's'
    converted_value = f"s{integer_part}{letter}"
    
    return converted_value


def create_empty_array_with_dynamic_name(name,value):
    # Create an empty array with no elements
    array_value = np.array([])
    
    # Dynamically create a variable name
    variable_name = f"{name}_{value}"
    
    # Assign the empty array to the dynamically created variable name in the global scope
    globals()[variable_name] = array_value
    
def add_data_to_dynamic_array(name,value,data):
# Dynamically create the variable name
    variable_name = f"{name}_{value}"
    
 # Check if the variable exists in the global scope
    if variable_name in globals():
        # Access the array using the variable name
        array = globals()[variable_name]
        
        # Convert data to a numpy array if it is not already
        data = np.array(data)
        
        # Reshape data to ensure it is a column vector
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        
        # If the original array is empty, initialize it with the new data
        if array.size == 0:
            array = data
        else:
            # If the dimensions match, add the new data as a new column
            if array.shape[0] == data.shape[0]:
                array = np.hstack((array, data))
            else:
                print(f"Error: The number of rows in the new data ({data.shape[0]}) does not match the existing array ({array.shape[0]}).")
        
        # Update the global variable with the new array
        globals()[variable_name] = array
    else:
        print(f"Variable '{variable_name}' does not exist.")   

def merge_mag_ang(value):
    # Dynamically create the variable names
    mag_variable_name = f"mag_{value}"
    ang_variable_name = f"ang_{value}"
    output_variable_name = f"output_{value}"
    
    # Check if the mag and ang variables exist in the global scope
    if mag_variable_name in globals() and ang_variable_name in globals():
        # Access the mag and ang arrays using the variable names
        mag_array = globals()[mag_variable_name]
        ang_array = globals()[ang_variable_name]
        
        # Check if the number of columns match
        if mag_array.shape[1] != ang_array.shape[1]:
            print(f"Error: The number of columns in {mag_variable_name} and {ang_variable_name} do not match.")
            return
        
        # Interleave the columns of mag_array and ang_array
        merged_array = np.empty((mag_array.shape[0], mag_array.shape[1] + ang_array.shape[1]))
        merged_array[:, ::2] = mag_array
        merged_array[:, 1::2] = ang_array
        
        # Assign the merged array to the dynamically created variable name in the global scope
        globals()[output_variable_name] = merged_array
    else:
        print(f"One or both variables '{mag_variable_name}' and '{ang_variable_name}' do not exist.")
        
def save_dynamic_array_to_csv(name,value):
    # Dynamically create the variable name
    variable_name = f"{name}_{value}"
    
    # Check if the variable exists in the global scope
    if variable_name in globals():
        # Access the array using the variable name
        array = globals()[variable_name]
        
        # Convert the array to a DataFrame
        df = pd.DataFrame(array)
        
        # Define the CSV filename
        csv_filename = f"{variable_name}.csv"
        
        # Save the DataFrame to a CSV file
        df.to_csv(csv_filename, index=False, header=False)
        print(f"Array saved to {csv_filename}")
    else:
        print(f"Variable '{variable_name}' does not exist.")
        
def split_csv_to_clusters(cluster_path, bus_list, loads_list,output_path):
    # Initialize dictionaries to store arrays for each cluster
    v_in,x,v_mag,v_ang = extract_arrays_from_csv(output_path,len(loads_list),len(bus_list))
    cluster_array = cluster_file_to_array(cluster_path)
    cluster_values = []
    temp_input = []
    temp_v_mag = []
    temp_v_ang= []
    k = -1
    for bus_index in cluster_array[:, 0]:
        k+=1
        bus_value = bus_list[bus_index]
        load_value = convert_decimal_to_letter(bus_value)
        
        # Find the load index if it exists
        load_index = next((idx for idx, load in enumerate(loads_list) if load == load_value), None)
        
        # Determine the cluster value
        cluster_value = cluster_array[k, 1]
        
        # Append v_mag and v_ang to the corresponding cluster arrays
        if cluster_value not in cluster_values:
            cluster_values.append(cluster_value)
            create_empty_array_with_dynamic_name("inp",cluster_value)
            create_empty_array_with_dynamic_name("mag",cluster_value)
            create_empty_array_with_dynamic_name("ang",cluster_value)
        add_data_to_dynamic_array("mag",cluster_value,v_mag[:, bus_index])
        add_data_to_dynamic_array("ang",cluster_value,v_ang[:, bus_index])
        
        # If load_index is found, append input_array to the corresponding cluster array
        if load_index is not None:
            add_data_to_dynamic_array("inp",cluster_value,x[:, 2*load_index])
            add_data_to_dynamic_array("inp",cluster_value,x[:, 2*load_index+1])
            
    for h in cluster_values:
        merge_mag_ang(h)
            
    for j in cluster_values:
        save_dynamic_array_to_csv("inp",j)
        save_dynamic_array_to_csv("output",j)
