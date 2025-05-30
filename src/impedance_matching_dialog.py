import tkinter as tk
from tkinter import ttk, messagebox

class ImpedanceMatchingDialog:
    def __init__(self, parent, line_info, available_options, message_type="no_match"):
        self.result = None
        self.line_info = line_info
        self.available_options = available_options
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Impedance Matching")
        self.dialog.geometry("800x500")
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
        
        # Title based on message type
        if message_type == "no_match":
            title_text = "No Impedance Match Found"
            message_text = "No impedance records found for the following line:"
        else:
            title_text = "Multiple Impedance Matches Found"
            message_text = "Multiple impedance records found for the following line:"
        
        title_label = ttk.Label(main_frame, text=title_text, font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Message
        message_label = ttk.Label(main_frame, text=message_text)
        message_label.pack(pady=(0, 10))
        
        # Line info frame
        info_frame = ttk.LabelFrame(main_frame, text="Line Information", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Display line info in grid
        info_text = f"Type: {line_info.get('Type', 'N/A')}\n"
        info_text += f"Conductor Size: {line_info.get('Conductor Size', 'N/A')}\n"
        info_text += f"Conductor Type: {line_info.get('Conductor Type', 'N/A')}\n"
        info_text += f"Length: {line_info.get('Length', 'N/A')}\n"
        info_text += f"Voltage Level: {line_info.get('Voltage_Level', 'N/A')} kV"
        
        ttk.Label(info_frame, text=info_text, font=('Consolas', 10)).pack()
        
        # Instructions
        if len(available_options) > 0:
            if message_type == "no_match":
                instructions = "However, there are other options with the same Type and Voltage Level. Please select one:"
            else:
                instructions = "Please select one of the available choices:"
        else:
            instructions = "No alternative options available."
        
        ttk.Label(main_frame, text=instructions, wraplength=750).pack(pady=(0, 10))
        
        if len(available_options) > 0:
            # Create treeview for options
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # Create treeview with scrollbars
            tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
            tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
            
            self.tree = ttk.Treeview(tree_frame, 
                                    yscrollcommand=tree_scroll_y.set,
                                    xscrollcommand=tree_scroll_x.set,
                                    height=10)
            
            tree_scroll_y.config(command=self.tree.yview)
            tree_scroll_x.config(command=self.tree.xview)
            
            # Define columns
            columns = ('conductor_size', 'conductor_type', 'pole_type', 'ground', 'impedance')
            self.tree['columns'] = columns
            self.tree['show'] = 'tree headings'
            
            # Format columns
            self.tree.column('#0', width=50, minwidth=50)
            self.tree.column('conductor_size', width=120, minwidth=100)
            self.tree.column('conductor_type', width=120, minwidth=100)
            self.tree.column('pole_type', width=120, minwidth=100)
            self.tree.column('ground', width=100, minwidth=80)
            self.tree.column('impedance', width=200, minwidth=150)
            
            # Create headings
            self.tree.heading('#0', text='#')
            self.tree.heading('conductor_size', text='Conductor Size')
            self.tree.heading('conductor_type', text='Conductor Type')
            self.tree.heading('pole_type', text='Pole Type')
            self.tree.heading('ground', text='Ground?')
            self.tree.heading('impedance', text='% Z+ @ 100 MVA')
            
            # Add options to tree
            for idx, option in enumerate(available_options.iterrows()):
                i, row = option
                values = (
                    str(row.get('Conductor Size', 'N/A')),
                    str(row.get('Conductor Type', 'N/A')),
                    str(row.get('Pole Type', 'N/A')),
                    str(row.get('Ground?', 'N/A')),
                    str(row.get('% Z+ @ 100 MVA', 'N/A'))
                )
                self.tree.insert('', 'end', text=str(idx + 1), values=values)
            
            # Pack treeview and scrollbars
            self.tree.grid(row=0, column=0, sticky='nsew')
            tree_scroll_y.grid(row=0, column=1, sticky='ns')
            tree_scroll_x.grid(row=1, column=0, sticky='ew')
            
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            # Select first item
            first_item = self.tree.get_children()[0]
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            
            # Bind double-click
            self.tree.bind('<Double-Button-1>', lambda e: self.on_ok())
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        if len(available_options) > 0:
            ttk.Button(button_frame, text="Select", command=self.on_ok, width=15).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel, width=15).pack(side=tk.RIGHT)
        
        # Bind Enter and Escape keys
        self.dialog.bind('<Return>', lambda e: self.on_ok() if len(available_options) > 0 else None)
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        """Handle OK/Select button"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select an option.")
            return
        
        # Get selected index
        item = self.tree.item(selection[0])
        idx = int(item['text']) - 1
        
        # Get the selected row from available_options
        self.result = self.available_options.iloc[idx]
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button"""
        self.result = None
        self.dialog.destroy()
    
    def get_result(self):
        """Get the dialog result"""
        self.dialog.wait_window()
        return self.result