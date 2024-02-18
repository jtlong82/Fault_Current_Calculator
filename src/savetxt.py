import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

def savetxt(buffer):
    # Initialize Tkinter root
    root = tk.Tk()
    root.withdraw()  # Hides the small Tkinter window

    # Ask user if they want to save the output using a Tkinter dialog
    save_file = simpledialog.askstring("Save File", "Do you want to save the output to a .txt file? (y/n):")
    if save_file and save_file.strip().lower() == 'y':
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Choose filename"
        )

        # Check if a file path was provided
        if file_path:
            # Write the buffer to the file with UTF-8 encoding
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("".join(buffer))
        else:
            print("File save cancelled.")

    # Destroy the Tkinter root (clean up)
    root.destroy()
