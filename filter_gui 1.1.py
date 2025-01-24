import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import subprocess
import sys

def process_data(csv_path, output_directory):
    try:
        data = pd.read_csv(csv_path)
        data_with_nickname = data.dropna(subset=['Nickname'])

        filters = {
            'silver_nicknames.txt': 'Silver tier',
            'copper_nicknames.txt': 'Copper tier',
            'lead_nicknames.txt': 'Lead tier',
            'past_benefactors_nicknames.txt': 'Past-Benefactor 💰',
            'verified_18_plus_nicknames.txt': '18+ verified'
        }

        for file_name, column in filters.items():
            filtered_data = data_with_nickname.dropna(subset=[column])['Nickname']
            full_path = f"{output_directory}/{file_name}"
            filtered_data.to_csv(full_path, index=False, header=False)

        messagebox.showinfo("Success", "Files have been successfully processed and saved.")
        open_folder(output_directory)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_folder(path):
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin':  # macOS
        subprocess.Popen(['open', path])
    else:  # linux
        subprocess.Popen(['xdg-open', path])

def main():
    root = tk.Tk()
    root.title("mellish's Whitelist Generator")

    def select_csv_file():
        file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
        if file_path:
            file_path_var.set(file_path)

    def select_output_directory():
        directory_path = filedialog.askdirectory(title="Select Output Directory")
        if directory_path:
            directory_path_var.set(directory_path)

    def on_process_clicked():
        csv_path = file_path_var.get()
        output_directory = directory_path_var.get()
        if csv_path and output_directory:
            process_data(csv_path, output_directory)
        else:
            messagebox.showwarning("Warning", "Please select both a CSV file and an output directory.")

    file_path_var = tk.StringVar()
    directory_path_var = tk.StringVar()

    tk.Button(root, text="Select CSV File", command=select_csv_file).pack(pady=5)
    tk.Label(root, textvariable=file_path_var).pack(pady=5)
    tk.Button(root, text="Select Output Directory", command=select_output_directory).pack(pady=5)
    tk.Label(root, textvariable=directory_path_var).pack(pady=5)
    tk.Button(root, text="Process", command=on_process_clicked).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
