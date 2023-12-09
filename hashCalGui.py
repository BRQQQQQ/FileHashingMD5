import tkinter as tk
from tkinter import filedialog
import hashlib, os

class FileHashingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MD5 Hash Calculator GUI")

        # Label and entry for file path
        self.file_path_label = tk.Label(master, text="File Path:")
        self.file_path_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)

        self.file_path_entry = tk.Entry(master, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        # Button for browsing files
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file, cursor="hand2")
        self.browse_button.grid(row=0, column=3, padx=10, pady=10)

        # Checkboxes for save and compare options
        self.save_checkbox_var = tk.IntVar()
        self.save_checkbox = tk.Checkbutton(master, text="Save to File", variable=self.save_checkbox_var)
        self.save_checkbox.grid(row=1, column=0, columnspan=2, pady=5)
        self.compare_checkbox_var = tk.IntVar()
        self.compare_checkbox = tk.Checkbutton(master, text="Compare Hash", variable=self.compare_checkbox_var)
        self.compare_checkbox.grid(row=1, column=2, columnspan=2, pady=5, padx=3)

        # Button to calculate hashing
        self.execute_button = tk.Button(master, text="Execute", command=self.execute_hashing)
        self.execute_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Text widget for displaying output
        self.output_text = tk.Text(master, height=10, width=50, state=tk.DISABLED)
        self.output_text.grid(row=3, column=0, columnspan=4, pady=5)

    # Open a file dialog for browsing files
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(tk.END, file_path)

    # Calculate the hash value of the selected file
    def calculate_hash(self, file_path, algorithm='md5'):
        hash_object = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_object.update(chunk)
        return hash_object.hexdigest()

    # Save the hash value to a file, storing multiple versions
    def save_hash_to_file(self, file_path, hash_value, output_file='hashes.txt'):
        with open(output_file, 'a') as file:
            file.write(f"{file_path}: {hash_value}\n")

     # Compare the hash value of the selected file with stored versions
    def compare_hashes(self, file_path, stored_hash, algorithm='md5'):
        current_hash = self.calculate_hash(file_path, algorithm)
        return current_hash == stored_hash

    def execute_hashing(self):
        file_path = self.file_path_entry.get() # Get the file path from the entry

        # Check if the file exists
        if not os.path.exists(file_path):
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Error: The specified file does not exist.")
            self.output_text.config(state=tk.DISABLED)
            return

        # Calculate & Display the hash value
        hash_value = self.calculate_hash(file_path)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Hash Value: {hash_value}\n")

        # Run the save_hash function if the checkbox is selected
        if self.save_checkbox_var.get():
            self.save_hash(file_path, hash_value)

        # Run the compare_hashes_and_display function if the checkbox is selected
        if self.compare_checkbox_var.get():
            self.compare_hashes_and_display(file_path, hash_value)

        self.output_text.config(state=tk.DISABLED)

    # Save the hash value if the checkbox is selected
    def save_hash(self, file_path, hash_value):
        output_file = 'hashes.txt'

        if not os.path.exists(output_file):
            with open(output_file, 'w'):
                pass

        with open(output_file, 'r') as file:
            existing_hashes = file.read()

        if f"{file_path}: {hash_value}" not in existing_hashes:
            self.save_hash_to_file(file_path, hash_value)
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Hash saved successfully.\n")
            self.output_text.config(state=tk.DISABLED)
        else:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Duplicate hash. This hash already exists in the file.\n")
            self.output_text.config(state=tk.DISABLED)

    # Compare hashes and display the result if the checkbox is selected
    def compare_hashes_and_display(self, file_path, hash_value):
        output_file = 'hashes.txt'

        with open(output_file, 'r') as file:
            existing_hashes = file.readlines()

        for line in existing_hashes:
            parts = line.strip().split(': ', 1)
            if len(parts) == 2:
                stored_file, stored_hash = parts
                if stored_file == file_path:
                    if hash_value == stored_hash:
                        self.output_text.insert(tk.END, "Hashes match. The file has not been modified.\n")
                    else:
                        self.output_text.insert(tk.END, "Hashes didn't match. The file may have been modified.\n")
                    break

if __name__ == "__main__":
    root = tk.Tk() # Create the main Tkinter window
    app = FileHashingGUI(root) # Create the FileHashingGUI instance
    root.mainloop() # Run the Tkinter event loop