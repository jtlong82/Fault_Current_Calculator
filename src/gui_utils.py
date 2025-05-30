import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import pandas as pd
import os
from datetime import datetime

class ToolTip:
    """Create tooltips for widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        background="lightyellow", 
                        relief="solid", 
                        borderwidth=1,
                        font=("Arial", 9))
        label.pack()
        
    def on_leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ScrollableFrame(ttk.Frame):
    """A scrollable frame widget"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class ResultsFormatter:
    """Format calculation results for display"""
    
    @staticmethod
    def format_complex_number(z, precision=2):
        """Format complex number for display"""
        if z.imag >= 0:
            return f"{z.real:.{precision}f}+{z.imag:.{precision}f}j"
        else:
            return f"{z.real:.{precision}f}{z.imag:.{precision}f}j"
    
    @staticmethod
    def format_polar(magnitude, angle, precision=2):
        """Format polar notation"""
        return f"{magnitude:.{precision}f}∠{angle:.{precision}f}°"
    
    @staticmethod
    def format_table(headers, rows, column_widths=None):
        """Format data as an aligned table"""
        if column_widths is None:
            column_widths = [15] * len(headers)
            
        # Create format string
        format_str = " ".join([f"{{:<{w}}}" for w in column_widths])
        
        # Format header
        result = format_str.format(*headers) + "\n"
        result += "-" * sum(column_widths) + "\n"
        
        # Format rows
        for row in rows:
            result += format_str.format(*row) + "\n"
            
        return result
    
    @staticmethod
    def highlight_text(text_widget, pattern, tag_name, **tag_config):
        """Highlight pattern in text widget"""
        start = 1.0
        while True:
            pos = text_widget.search(pattern, start, tk.END)
            if not pos:
                break
            end = f"{pos}+{len(pattern)}c"
            text_widget.tag_add(tag_name, pos, end)
            text_widget.tag_config(tag_name, **tag_config)
            start = end

class PlotManager:
    """Manage matplotlib plots in tkinter"""
    
    def __init__(self, parent_frame, figure_size=(8, 6), dpi=100):
        self.figure = plt.Figure(figsize=figure_size, dpi=dpi)
        self.ax = self.figure.add_subplot(111)
        
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, parent_frame)
        self.toolbar.update()
        
    def clear_plot(self):
        """Clear the current plot"""
        self.ax.clear()
        self.canvas.draw()
        
    def update_plot(self):
        """Update the canvas"""
        self.canvas.draw()
        
    def save_plot(self, filename=None):
        """Save the current plot"""
        if filename is None:
            filename = f"plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.figure.savefig(filename, dpi=300, bbox_inches='tight')
        return filename

class DataValidator:
    """Validate user inputs"""
    
    @staticmethod
    def validate_float(value, min_val=None, max_val=None):
        """Validate float input"""
        try:
            val = float(value)
            if min_val is not None and val < min_val:
                return False, f"Value must be >= {min_val}"
            if max_val is not None and val > max_val:
                return False, f"Value must be <= {max_val}"
            return True, val
        except ValueError:
            return False, "Invalid number format"
    
    @staticmethod
    def validate_int(value, min_val=None, max_val=None):
        """Validate integer input"""
        try:
            val = int(value)
            if min_val is not None and val < min_val:
                return False, f"Value must be >= {min_val}"
            if max_val is not None and val > max_val:
                return False, f"Value must be <= {max_val}"
            return True, val
        except ValueError:
            return False, "Invalid integer format"
    
    @staticmethod
    def validate_complex(value):
        """Validate complex number input"""
        try:
            val = complex(value)
            return True, val
        except ValueError:
            return False, "Invalid complex number format"

class FileManager:
    """Manage file operations"""
    
    @staticmethod
    def get_recent_files(file_type='xlsx', max_files=5):
        """Get list of recently used files"""
        # This would typically read from a config file
        # For now, return empty list
        return []
    
    @staticmethod
    def save_recent_file(filepath):
        """Save filepath to recent files list"""
        # This would typically write to a config file
        pass
    
    @staticmethod
    def export_results_to_excel(results_dict, filename=None):
        """Export results to Excel file"""
        if filename is None:
            filename = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, data in results_dict.items():
                if isinstance(data, pd.DataFrame):
                    data.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    # Convert text data to DataFrame
                    df = pd.DataFrame([data.split('\n')])
                    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
                    
        return filename

class ProgressDialog:
    """Show progress dialog for long operations"""
    
    def __init__(self, parent, title="Processing...", message="Please wait..."):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x100")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - self.dialog.winfo_width()) // 2
        y = (self.dialog.winfo_screenheight() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Add message
        tk.Label(self.dialog, text=message, pady=10).pack()
        
        # Add progress bar
        self.progress = ttk.Progressbar(self.dialog, mode='indeterminate', length=250)
        self.progress.pack(pady=10)
        self.progress.start(10)
        
    def close(self):
        """Close the progress dialog"""
        self.progress.stop()
        self.dialog.destroy()

def create_icon_button(parent, text, icon_char, command, **kwargs):
    """Create a button with an icon character"""
    btn = ttk.Button(parent, text=f"{icon_char} {text}", command=command, **kwargs)
    return btn

def center_window(window):
    """Center a window on the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Validation functions for Entry widgets
def validate_numeric_input(char):
    """Validate that input is numeric"""
    return char.isdigit() or char in ['.', '-', '+', '']

def validate_positive_numeric(char):
    """Validate that input is positive numeric"""
    return char.isdigit() or char in ['.', '']