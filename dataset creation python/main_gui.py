import tkinter as tk
from tkinter import filedialog, messagebox
import dss_profile_solver_ron
import profile_with_different_mu_ron
import edit_loadshape
import input_output_for_clusters
    

def calculate_parameters():
    global number_of_loads
    global number_of_years
    global circuit_path
    global loads_list
    global buses_list
    global npts
    global profile_path
    global save_profile_path
    profile_path = entry_profile_path.get()
    circuit_path = entry_circuit_path.get()
    number_of_years = int(entry_number_of_years.get())
    save_profile_path = entry_save_profile_path.get()
    
    with open(profile_path, 'r') as file:
        npts = sum(1 for _ in file)        
    # Run the simulation and get the number of loads
    number_of_loads,loads_list,buses_list = dss_profile_solver_ron.find_number_of_loads(circuit_path)
    messagebox.showinfo("Success", f"Number of loads: {number_of_loads}")
    
def run():
    try:    
        # Generate profiles
        profile_with_different_mu_ron.generate_and_save_profiles(number_of_years, number_of_loads, profile_path, save_profile_path)
        messagebox.showinfo("Success", "Profiles generated and saved successfully.")
        
        create_loadshape_gui(number_of_loads)
        #root.destroy()  # Close the current GUI window
        
        #run_solver_gui(circuit_path)  # Open the new GUI for running the solver

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def find_loads_and_buses(circuit_path):
    global loads_list
    global buses_list
    global number_of_loads
    number_of_loads,loads_list,buses_list = dss_profile_solver_ron.find_number_of_loads(circuit_path)
    
    
def browse_file(entry):
    filepath = filedialog.askopenfilename(filetypes=(("DSS files", "*.dss;*.DSS"), ("All files", "*.*")))
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

def save_file(entry):
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if filepath:
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

def create_loadshape_gui(number_of_loads):
    loadshape_root = tk.Tk()
    loadshape_root.title("LoadShape Configuration")

    # Entry for LOADS file path
    tk.Label(loadshape_root, text="LOADS File Path:").grid(row=0, column=0)
    entry_loads_path = tk.Entry(loadshape_root, width=50)
    entry_loads_path.grid(row=0, column=1)
    tk.Button(loadshape_root, text="Browse", command=lambda: browse_file(entry_loads_path)).grid(row=0, column=2)

    # Entry for LoadShape file save path
    tk.Label(loadshape_root, text="Save LoadShape File Path:").grid(row=1, column=0)
    entry_save_loadshape_path = tk.Entry(loadshape_root, width=50)
    entry_save_loadshape_path.grid(row=1, column=1)
    tk.Button(loadshape_root, text="Browse", command=lambda: save_file(entry_save_loadshape_path)).grid(row=1, column=2)

    # Button to run the edit loadshape function
    tk.Button(loadshape_root, text="Run LoadShape Edit", command=lambda: edit_loadshape.update_loadshape(number_of_loads, entry_loads_path.get(), entry_save_loadshape_path.get(),8760)).grid(row=2, column=0, columnspan=3)

    loadshape_root.mainloop()
 
def create_cluster_gui():
   
    loadshape_root = tk.Tk()
    loadshape_root.title("Clusters Data Divider")

   
    # Cluster File Path
    tk.Label(loadshape_root, text="Cluster File Path:").grid(row=1, column=0)
    entry_loads_path_cluster = tk.Entry(loadshape_root, width=50)
    entry_loads_path_cluster.grid(row=1, column=1)
    tk.Button(loadshape_root, text="Browse", command=lambda: browse_file(entry_loads_path_cluster)).grid(row=1, column=2)
    
    # Input-Output File Path
    tk.Label(loadshape_root, text="Input-Output File Path:").grid(row=2, column=0)
    entry_loads_path_input_output = tk.Entry(loadshape_root, width=50)
    entry_loads_path_input_output.grid(row=2, column=1)
    tk.Button(loadshape_root, text="Browse", command=lambda: browse_file(entry_loads_path_input_output)).grid(row=2, column=2)

    # Buttons
    
    tk.Button(loadshape_root, text="Divide to Clusters", command=lambda: input_output_for_clusters.split_csv_to_clusters(entry_loads_path_cluster.get(), buses_list, loads_list, entry_loads_path_input_output.get())).grid(row=4, column=0, columnspan=3)

    loadshape_root.mainloop()
def run_solver_gui(circuit_path):
    solver_root = tk.Tk()
    solver_root.title("Run Solver")
    tk.Button(solver_root, text="Run solver for the circuit", command=lambda: dss_profile_solver_ron.run("ieee123", 1752, 1, circuit_path)).pack()
    solver_root.mainloop()

def create_gui():
    global root, entry_circuit_path, entry_number_of_years, entry_profile_path, entry_save_profile_path
    root = tk.Tk()
    root.title("Power System Simulation and Profile Generation")

    # Circuit file path
    tk.Label(root, text="Circuit File Path:").grid(row=0, column=0)
    entry_circuit_path = tk.Entry(root, width=50)
    entry_circuit_path.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_file(entry_circuit_path)).grid(row=0, column=2)

    # Number of years
    tk.Label(root, text="Number of Years:").grid(row=1, column=0)
    entry_number_of_years = tk.Entry(root)
    entry_number_of_years.grid(row=1, column=1)

    # Profile path
    tk.Label(root, text="Profile CSV Path:").grid(row=2, column=0)
    entry_profile_path = tk.Entry(root, width=50)
    entry_profile_path.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_file(entry_profile_path)).grid(row=2, column=2)

    # Save profile path
    tk.Label(root, text="Save Profile Path:").grid(row=3, column=0)
    entry_save_profile_path = tk.Entry(root, width=50)
    entry_save_profile_path.grid(row=3, column=1)
    tk.Button(root, text="Save As", command=lambda: save_file(entry_save_profile_path)).grid(row=3, column=2)

    # Run button
    tk.Button(root, text="Calculate Parameters", command=calculate_parameters).grid(row=4, column=0, columnspan=3)
    
    tk.Button(root, text="Run Simulation and Generate Profiles", command=run).grid(row=5, column=0, columnspan=3)

    # Button to open LoadShape configuration GUI
    tk.Button(root, text="Edit LoadShape", command=lambda: create_loadshape_gui(91)).grid(row=23, column=0, columnspan=3)  
    
    tk.Button(root, text="create data for each cluster", command=lambda: create_cluster_gui()).grid(row=24, column=0, columnspan=3)
    
    tk.Button(root, text="Generate input-output file", command=lambda: dss_profile_solver_ron.run("ieee123", 8760*number_of_years, 1, circuit_path)).grid(row=25, column=0, columnspan=3) 
    root.mainloop()

if __name__ == "__main__":
    create_gui()
