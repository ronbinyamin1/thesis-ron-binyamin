# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:01:15 2024

@author: ronbinyamin
"""
import sys
import os
import pandas as pd
import dss 
import numpy as np
import re
import csv
#from ckt5_update_loadshape_file import update_loadshape_ckt5_file

def find_number_of_loads(file_path):
    dss_engine = dss.DSS
    DSSText = dss_engine.Text
    DSSText.Command = f"compile [{file_path}]"
    DSSCircuit = dss_engine.ActiveCircuit
    loads = DSSCircuit.Loads
    print(f"Number of loads: {loads.Count}")
    loads_list = []
    for load_name in DSSCircuit.Loads.AllNames:
        loads_list.append(load_name)
    buses_list = DSSCircuit.AllNodeNames
    return loads.Count,loads_list,buses_list





def run(profile, examination_period, selected_include_caps,file_path):
    dss_engine = dss.DSS
    # dss.AllowForms = True
    DSSText = dss_engine.Text  # Used for all text interfacing from matlab to opendss
    DSSCircuit = dss_engine.ActiveCircuit  # active circuit
    DSSSolution = DSSCircuit.Solution



# Check if the file exists
#if os.path.exists(file_path):
    # Compile the DSS file using the text interface
    DSSText.Command = f"compile [{file_path}]"
    print("File compiled successfully.")
    
    # Access the active circuit
    #DSSCircuit = dss_engine.ActiveCircuit

    # Retrieve and print the number of loads
    loads = DSSCircuit.Loads
    print(f"Number of loads: {loads.Count}")
#else:
    #print("File does not exist. Please check the path.")
        
    nodeNames = DSSCircuit.YNodeOrder
    lineNames = DSSCircuit.Lines.AllNames
    transformerNames = DSSCircuit.Transformers.AllNames
    voltageNames = DSSCircuit.AllNodeNames
    print(len(voltageNames))
    #loads = DSSCircuit.Loads
    number_of_loads = loads.Count

    Cindex = DSSCircuit.Capacitors.First
    while Cindex != 0:
        if selected_include_caps == 0:
            DSSText.Command = DSSCircuit.ActiveElement.Name + '.kVar=0'
        Cindex = DSSCircuit.Capacitors.Next
    ####################################################################################################################

    ####################################################################################################################

    nt = examination_period

    # solve first a 24-hr period to get the regulator and capacitor controls synchronized.
    DSSText.Command = 'set mode=daily stepsize=1h number=24'  # we want 1 day-24 hour period
    DSSText.Command = 'Solve'
    DSSText.Command = 'set mode=yearly stepsize=1h number=1'  # number - Number of solutions or time steps to perform for each Solve command
    DSSText.Command = 'set hour=1'  # Start at second 0 of hour 5

    DSSParallel = DSSCircuit.Parallel  # Habdler for Parallel processing functions
    CPUs = DSSParallel.NumCPUs - 1  # Gets how many CPUs this PC has


    dss_engine.AllowForms = False  # true
    totc = 0
    atime = 0
    columns = np.size(DSSCircuit.AllBusVmagPu)

    v_mag = np.zeros((nt, columns))
    v_ang_matrix = np.zeros((nt, columns))

    num_buses = np.size(DSSCircuit.AllNodeNames)
    x = np.zeros((nt, number_of_loads*2))
    
    #calculate Vsource
    v_source = np.zeros(nt)
    voltage_kv = DSSCircuit.Vsources.BasekV
    #angle_source = np.angle(voltage_kv)



    #################################start of "for i in range(nt)" loop#################################################
    for i in range(nt):
        # start = time.time()
        voltage_kv = DSSCircuit.Vsources.BasekV
        v_source[i] = voltage_kv
        totc = totc + 1
        DSSText.Command = "get hour"
        hour = DSSText.Result

        DSSText.Command = 'Solve'
        DSSText.Command = 'get steptime'
        atime = atime + float(DSSText.Result)

        is_converged = DSSSolution.Converged
        if is_converged:
            pass
        else:
            print("Solution has not converged.")
            continue

        # Retrieve voltage magnitude and angle for each bus
        v = DSSCircuit.AllBusVolts
        comp_v = []
        for r in range(0, len(v) - 1, 2):
            comp_v.append(complex(v[r], v[r + 1]))
        ang_new_v = []
        for m in range(len(comp_v)):
            ang_new_v.append(np.angle(comp_v[m]))
        all_vbus_pu = DSSCircuit.AllBusVmagPu
        for j in range(len(all_vbus_pu)):
            v_mag[i][j] = all_vbus_pu[j]
        for j in range(len(ang_new_v)):
            v_ang_matrix[i][j] = ang_new_v[j]


        if i%500 == 0:
            print("ok")
        power_index = 0
        for load_name in DSSCircuit.Loads.AllNames:
            DSSCircuit.SetActiveElement(f"Load.{load_name}")
            active_power = list(DSSCircuit.ActiveElement.TotalPowers)[0] #tuple pf PQ [0] for active power
            reactive_power = list(DSSCircuit.ActiveElement.TotalPowers)[1]  # you can use this to get the reactive power
            bus_name = list(DSSCircuit.ActiveElement.BusNames)[0]
            bus_index = [idx for idx, bus in enumerate(DSSCircuit.AllNodeNames, 0) if bus == bus_name]
            x[i, power_index] = active_power
            x[i, power_index+1] = reactive_power
            power_index += 2

    y = pd.concat([pd.DataFrame(v_mag), pd.DataFrame(v_ang_matrix)], axis=1)
    x_df = pd.DataFrame(x)
    v_source_df = pd.DataFrame(v_source)

    combined_df = pd.concat([v_source_df,x_df, y], axis=1)

    # Save to CSV
    combined_df.to_csv(r"C:\Program Files\thesis\dss and data\output.csv", index=False)
    #cluster_array = cluster_file_to_array(r"C:\Program Files\thesis\cluster\clusters-networks.ieee_test_cases.123Bus.Run_IEEE123Bus.DSS.log.txt")
    #split_csv_to_clusters(cluster_array,voltageNames,loads,x,v_mag,v_ang_matrix,v_source)

#find_number_of_loads(r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\Run_IEEE123Bus.DSS")
#if __name__ == '__main__':
 #   run("ieee123",1752,1)#,'1','1',{'Vminpu_model1': '0.8', 'Vmaxpu': '1.2', 'Vlowpu': '0.5', 'Vminpu_model2': '0.95', 'Pvfactor': '0.1', 'CVRwatts': '0.8', 'CVRvars': '2.0', 'Vminpu_model8': '0.8', 'ZIPV': '(0.5, 0, 0.5, 1, 0, 0, 0.93)'})
#array = cluster_file_to_array(r"C:\Program Files\thesis\cluster\clusters-networks.ieee_test_cases.123Bus.Run_IEEE123Bus.DSS.log.txt")