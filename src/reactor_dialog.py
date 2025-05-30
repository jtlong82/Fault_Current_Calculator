import tkinter as tk
from tkinter import ttk
import pandas as pd

class ReactorSelectionDialog:
    def __init__(self, parent, reactor_df):
        self.result = None
        self.reactor_df = reactor_df
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Reactor Selection")
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - self.dialog.winfo_width()) // 2
        y = (self.dialog.winfo_screenheight() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Create main frame
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Reactor Selection for 11.5kV System", 
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                               text="Please select one of the available reactor choices, enter a custom reactor, or select 'No Reactor':",
                               wraplength=550)
        instructions.pack(pady=(0, 20))
        
        # Create listbox frame
        listbox_frame = ttk.Frame(main_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create listbox with scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, 
                                 height=8, font=('Consolas', 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Add reactor options
        self.reactor_options = []
        for idx, (i, row) in enumerate(reactor_df.iterrows()):
            display_text = f"{row['Type']:<15} {row['Wire Type']:<25} {row['% Z+ @ 100 MVA']}"
            self.listbox.insert(tk.END, display_text)
            self.reactor_options.append(row)
        
        # Add custom option
        self.listbox.insert(tk.END, "─" * 60)
        self.listbox.insert(tk.END, "Custom Reactor")
        
        # Add no reactor option
        self.listbox.insert(tk.END, "No Reactor")
        
        # Select first item by default
        self.listbox.selection_set(0)
        
        # Bind double-click
        self.listbox.bind('<Double-Button-1>', lambda e: self.on_ok())
        
        # Custom reactor frame (initially hidden)
        self.custom_frame = ttk.LabelFrame(main_frame, text="Custom Reactor Parameters", padding=10)
        
        ttk.Label(self.custom_frame, text="Reactor Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.custom_name_var = tk.StringVar()
        ttk.Entry(self.custom_frame, textvariable=self.custom_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.custom_frame, text="% Z+ @ 100 MVA:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.custom_impedance_var = tk.StringVar()
        ttk.Entry(self.custom_frame, textvariable=self.custom_impedance_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="OK", command=self.on_ok, width=15).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel, width=15).pack(side=tk.RIGHT)
        
        # Bind selection change
        self.listbox.bind('<<ListboxSelect>>', self.on_selection_change)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_selection_change(self, event):
        """Handle selection change"""
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            # Check if custom reactor is selected
            if idx == len(self.reactor_options) + 1:  # Custom option
                self.custom_frame.pack(fill=tk.X, pady=(20, 0), before=self.listbox.master.master.winfo_children()[-1])
            else:
                self.custom_frame.pack_forget()
    
    def on_ok(self):
        """Handle OK button"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        
        if idx < len(self.reactor_options):
            # Predefined reactor selected
            self.result = {
                'type': 'predefined',
                'data': self.reactor_options[idx]
            }
        elif idx == len(self.reactor_options) + 1:  # Custom
            # Validate custom inputs
            name = self.custom_name_var.get().strip()
            impedance = self.custom_impedance_var.get().strip()
            
            if not name or not impedance:
                tk.messagebox.showwarning("Input Error", "Please enter both reactor name and impedance.")
                return
            
            try:
                impedance_complex = complex(impedance)
            except ValueError:
                tk.messagebox.showwarning("Input Error", "Please enter a valid complex number for impedance (e.g., 1.5+2.3j).")
                return
            
            self.result = {
                'type': 'custom',
                'name': name,
                'impedance': impedance_complex
            }
        elif idx == len(self.reactor_options) + 2:  # No Reactor
            self.result = {
                'type': 'none'
            }
        
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button"""
        self.result = None
        self.dialog.destroy()
    
    def get_result(self):
        """Get the dialog result"""
        self.dialog.wait_window()
        return self.result