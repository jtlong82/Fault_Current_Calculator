#!/usr/bin/env python3
"""
Power System Fault Calculator - GUI Launcher
Launch script for the graphical user interface version
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    required_modules = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'matplotlib': 'matplotlib',
        'openpyxl': 'openpyxl'
    }
    
    for module_name, pip_name in required_modules.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_deps.append(pip_name)
    
    if missing_deps:
        root = tk.Tk()
        root.withdraw()
        
        msg = f"Missing required dependencies:\n{', '.join(missing_deps)}\n\n"
        msg += "Please install them using:\n"
        msg += f"pip install {' '.join(missing_deps)}"
        
        messagebox.showerror("Missing Dependencies", msg)
        return False
    
    return True

def check_files():
    """Check if all required files are present"""
    # Get the directory where this launcher script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_files = [
        'main_gui.py',
        'menus.py',
        'Classes.py',
        'GetExcel.py',
        'CleanLineTrace.py',
        'Calcs.py',
        'CleanDataframe.py',
        'ExcelToDataframe.py'
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(script_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        root = tk.Tk()
        root.withdraw()
        
        msg = f"Missing required files:\n{', '.join(missing_files)}\n\n"
        msg += "Please ensure all files are in the same directory."
        
        messagebox.showerror("Missing Files", msg)
        return False
    
    return True

def setup_environment():
    """Setup the environment for the application"""
    # Get the directory where this launcher script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Add current directory to Python path
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # Set matplotlib backend
    try:
        import matplotlib
        matplotlib.use('TkAgg')
    except:
        pass

def launch_application():
    """Launch the main GUI application"""
    try:
        # Import and run the main GUI
        from main_gui import main
        main()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        
        msg = f"Error launching application:\n{str(e)}\n\n"
        msg += "Please check the error log for details."
        
        messagebox.showerror("Launch Error", msg)
        
        # Write error to log file
        with open('error_log.txt', 'w') as f:
            import traceback
            f.write(f"Error launching application:\n")
            f.write(traceback.format_exc())

def main():
    """Main entry point"""
    print("Power System Fault Calculator - GUI Version")
    
    # Debug info
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    
    print("\nChecking dependencies...")
    
    if not check_dependencies():
        sys.exit(1)
    
    print("Checking required files...")
    if not check_files():
        sys.exit(1)
    
    print("Setting up environment...")
    setup_environment()
    
    print("Launching application...")
    launch_application()

if __name__ == '__main__':
    main()