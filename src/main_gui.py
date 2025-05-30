import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Import all your existing modules
from menus import zbusmenu, fault_loc_menu, sel_time_menu, savetxt
from Classes import ZBus, ZLine, ZTrans
from GetExcel import load_impedance_sheets, load_line_trace, load_clean_line_imp
from CleanLineTrace import map_impedances
from Calcs import (primary_line_fault_calculation, locate_primary_line_fault_l_g, 
                   sec_trans_fault_calculation, locate_primary_line_fault_3ph,
                   locate_primary_line_fault_l_l, locate_primary_line_fault_l_l_g)

class PowerSystemFaultCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Power System Fault Calculator")
        self.root.geometry("1400x900")
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Import and apply modern theme
        try:
            from gui_config import apply_theme, COLORS, FONTS
            apply_theme(self.style)
            self.colors = COLORS
            self.fonts = FONTS
        except ImportError:
            # Fallback to basic styling if gui_config not available
            self.colors = {
                'background': '#f8f9fa',
                'primary': '#1a1a2e',
                'secondary': '#0466c8',
                'card_bg': '#ffffff'
            }
            self.fonts = {
                'default': ('Segoe UI', 10),
                'heading': ('Segoe UI', 14, 'bold')
            }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Data storage
        self.bus_dataframes = None
        self.line_dataframes = None
        self.zbus_selection = None
        self.zline_selection = None
        self.ztrans_selection = None
        self.line_trace = None
        self.buffer = []
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
        # Create main content area
        self.create_main_content()
        
        # Load initial data
        self.load_initial_data()
        
    def create_menu_bar(self):
        menubar = tk.Menu(self.root, bg=self.colors['card_bg'], fg=self.colors['text'], 
                         activebackground=self.colors['secondary'], activeforeground='white')
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['card_bg'], fg=self.colors['text'],
                           activebackground=self.colors['secondary'], activeforeground='white')
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Impedance Sheets", command=self.load_impedance_sheets_gui, 
                             accelerator="Ctrl+O")
        file_menu.add_command(label="Load Line Impedances", command=self.load_line_impedances_gui)
        file_menu.add_command(label="Load Line Trace", command=self.load_line_trace_gui, 
                             accelerator="Ctrl+L")
        file_menu.add_separator()
        file_menu.add_command(label="Save Results", command=self.save_results, 
                             accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, 
                             accelerator="Ctrl+Q")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['card_bg'], fg=self.colors['text'],
                           activebackground=self.colors['secondary'], activeforeground='white')
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Clear Results", command=self.clear_results)
        view_menu.add_command(label="Reset All", command=self.reset_all)
        view_menu.add_separator()
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0, bg=self.colors['card_bg'], fg=self.colors['text'])
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        
        self.theme_var = tk.StringVar(value="light")
        theme_menu.add_radiobutton(label="Light Mode", variable=self.theme_var, value="light",
                                  command=lambda: self.change_theme("light"))
        theme_menu.add_radiobutton(label="Dark Mode", variable=self.theme_var, value="dark",
                                  command=lambda: self.change_theme("dark"))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['card_bg'], fg=self.colors['text'],
                           activebackground=self.colors['secondary'], activeforeground='white')
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about, 
                             accelerator="F1")
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        
        # Bind keyboard shortcuts
        self.root.bind_all("<Control-o>", lambda e: self.load_impedance_sheets_gui())
        self.root.bind_all("<Control-l>", lambda e: self.load_line_trace_gui())
        self.root.bind_all("<Control-s>", lambda e: self.save_results())
        self.root.bind_all("<Control-q>", lambda e: self.root.quit())
        self.root.bind_all("<F1>", lambda e: self.show_about())
        
    def create_toolbar(self):
        toolbar_frame = ttk.Frame(self.main_container, style='Card.TFrame')
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
        
        toolbar = ttk.Frame(toolbar_frame)
        toolbar.pack(padx=10, pady=8)
        
        # Create toolbar buttons with better styling
        button_style = {'style': 'TButton', 'width': 15}
        
        ttk.Button(toolbar, text="📁 Load Data", command=self.load_all_data, **button_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="💾 Save Results", command=self.save_results, **button_style).pack(side=tk.LEFT, padx=3)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(toolbar, text="⚡ Bus Fault", command=lambda: self.notebook.select(0), **button_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="🔌 Line Fault", command=lambda: self.notebook.select(1), **button_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="🔄 Trans. Fault", command=lambda: self.notebook.select(2), **button_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="📍 Locate Fault", command=lambda: self.notebook.select(3), **button_style).pack(side=tk.LEFT, padx=3)
        ttk.Button(toolbar, text="⏱️ SEL Curves", command=lambda: self.notebook.select(4), **button_style).pack(side=tk.LEFT, padx=3)
        
    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.root, style='Card.TFrame')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(5, 10))
        
        status_content = ttk.Frame(self.status_bar)
        status_content.pack(fill=tk.X, padx=15, pady=8)
        
        self.status_label = ttk.Label(status_content, text="Ready", font=self.fonts['small'])
        self.status_label.pack(side=tk.LEFT)
        
        self.data_status_label = ttk.Label(status_content, text="No data loaded", 
                                         font=self.fonts['small'], foreground=self.colors['text_light'])
        self.data_status_label.pack(side=tk.RIGHT)
        
    def create_main_content(self):
        # Create content frame with padding
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs with icons
        self.bus_fault_tab = ttk.Frame(self.notebook)
        self.line_fault_tab = ttk.Frame(self.notebook)
        self.trans_fault_tab = ttk.Frame(self.notebook)
        self.fault_location_tab = ttk.Frame(self.notebook)
        self.sel_curves_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook with better labels
        self.notebook.add(self.bus_fault_tab, text="⚡ Bus Fault Current")
        self.notebook.add(self.line_fault_tab, text="🔌 Primary Line Fault")
        self.notebook.add(self.trans_fault_tab, text="🔄 Transformer Secondary")
        self.notebook.add(self.fault_location_tab, text="📍 Fault Location")
        self.notebook.add(self.sel_curves_tab, text="⏱️ SEL U-Curves")
        
        # Create content for each tab
        self.create_bus_fault_tab()
        self.create_line_fault_tab()
        self.create_trans_fault_tab()
        self.create_fault_location_tab()
        self.create_sel_curves_tab()
        
    def create_bus_fault_tab(self):
        # Create main frame with padding
        main_frame = ttk.Frame(self.bus_fault_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create grid layout
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input section - Left side
        input_frame = ttk.LabelFrame(main_frame, text="Bus Selection Parameters", padding=20)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Add some vertical spacing between inputs
        ttk.Label(input_frame, text="Voltage Level:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.bus_voltage_var = tk.StringVar()
        self.bus_voltage_combo = ttk.Combobox(input_frame, textvariable=self.bus_voltage_var, width=25)
        self.bus_voltage_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.bus_voltage_combo.bind('<<ComboboxSelected>>', self.on_voltage_level_change)
        
        ttk.Label(input_frame, text="Station:", style='Subtitle.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.bus_station_var = tk.StringVar()
        self.bus_station_combo = ttk.Combobox(input_frame, textvariable=self.bus_station_var, width=25)
        self.bus_station_combo.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Calculate button with primary style
        calc_btn = ttk.Button(input_frame, text="Calculate Bus Fault", 
                             command=self.calculate_bus_fault, style='Primary.TButton')
        calc_btn.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Quick info panel - Right side
        info_frame = ttk.LabelFrame(main_frame, text="Quick Info", padding=20)
        info_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N), padx=(10, 0))
        
        info_text = """This calculation determines the available fault current at the selected bus.

Key outputs:
• 3-Phase fault current
• Line-to-ground fault
• Line-to-line fault
• Line-to-line-to-ground fault

Results include magnitude and angle for each phase."""
        
        ttk.Label(info_frame, text=info_text, wraplength=300, 
                 foreground=self.colors['text_light']).pack(pady=10)
        
        # Results section - Bottom
        results_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding=15)
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        
        # Configure grid weights
        main_frame.rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Create text widget with modern styling
        self.bus_results_text = tk.Text(results_frame, wrap=tk.WORD, height=15, 
                                       font=self.fonts['monospace'], 
                                       bg=self.colors['input_bg'],
                                       relief=tk.FLAT,
                                       borderwidth=1)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.bus_results_text.yview)
        self.bus_results_text.configure(yscrollcommand=scrollbar.set)
        
        self.bus_results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def create_line_fault_tab(self):
        # Create main frame with padding
        main_frame = ttk.Frame(self.line_fault_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section - Input parameters
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create three columns
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)
        
        # Left column - Bus selection
        bus_frame = ttk.LabelFrame(top_frame, text="Bus Selection", padding=15)
        bus_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(bus_frame, text="Voltage Level:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.line_voltage_var = tk.StringVar()
        self.line_voltage_combo = ttk.Combobox(bus_frame, textvariable=self.line_voltage_var, width=20)
        self.line_voltage_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.line_voltage_combo.bind('<<ComboboxSelected>>', self.on_line_voltage_change)
        
        ttk.Label(bus_frame, text="Station:", style='Subtitle.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.line_station_var = tk.StringVar()
        self.line_station_combo = ttk.Combobox(bus_frame, textvariable=self.line_station_var, width=20)
        self.line_station_combo.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Middle column - Relay settings
        relay_frame = ttk.LabelFrame(top_frame, text="Relay Settings", padding=15)
        relay_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        ttk.Label(relay_frame, text="CT Ratio (CTR:1):", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.ctr_var = tk.StringVar(value="600")
        ctr_entry = ttk.Entry(relay_frame, textvariable=self.ctr_var, width=15)
        ctr_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(relay_frame, text="PT Ratio (PTR:1):", style='Subtitle.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.ptr_var = tk.StringVar(value="100")
        ptr_entry = ttk.Entry(relay_frame, textvariable=self.ptr_var, width=15)
        ptr_entry.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Right column - Line trace
        trace_frame = ttk.LabelFrame(top_frame, text="Line Trace", padding=15)
        trace_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.line_trace_label = ttk.Label(trace_frame, text="No file loaded", 
                                         relief=tk.FLAT, 
                                         background=self.colors['border_light'],
                                         padding=10)
        self.line_trace_label.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(trace_frame, text="Load Line Trace", 
                  command=self.load_line_trace_gui,
                  style='TButton').pack(fill=tk.X)
        
        # Calculate button
        calc_frame = ttk.Frame(main_frame)
        calc_frame.pack(fill=tk.X, pady=(0, 20))
        
        calc_btn = ttk.Button(calc_frame, text="Calculate Line Fault", 
                             command=self.calculate_line_fault, 
                             style='Primary.TButton')
        calc_btn.pack()
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with modern styling
        self.line_results_text = tk.Text(results_frame, wrap=tk.WORD, height=15, 
                                        font=self.fonts['monospace'],
                                        bg=self.colors['input_bg'],
                                        relief=tk.FLAT,
                                        borderwidth=1)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.line_results_text.yview)
        self.line_results_text.configure(yscrollcommand=scrollbar.set)
        
        self.line_results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_trans_fault_tab(self):
        # Create main frame with paned window
        paned = ttk.PanedWindow(self.trans_fault_tab, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for inputs
        top_frame = ttk.Frame(paned)
        paned.add(top_frame, weight=1)
        
        # Input section
        input_frame = ttk.LabelFrame(top_frame, text="Transformer Fault Parameters", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create three columns
        col1 = ttk.Frame(input_frame)
        col1.grid(row=0, column=0, padx=10, sticky=tk.N)
        
        col2 = ttk.Frame(input_frame)
        col2.grid(row=0, column=1, padx=10, sticky=tk.N)
        
        col3 = ttk.Frame(input_frame)
        col3.grid(row=0, column=2, padx=10, sticky=tk.N)
        
        # Column 1 - Bus selection
        ttk.Label(col1, text="Bus Selection", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(col1, text="Voltage Level:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.trans_voltage_var = tk.StringVar()
        self.trans_voltage_combo = ttk.Combobox(col1, textvariable=self.trans_voltage_var, width=20)
        self.trans_voltage_combo.grid(row=1, column=1, padx=5, pady=5)
        self.trans_voltage_combo.bind('<<ComboboxSelected>>', self.on_trans_voltage_change)
        
        ttk.Label(col1, text="Station:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.trans_station_var = tk.StringVar()
        self.trans_station_combo = ttk.Combobox(col1, textvariable=self.trans_station_var, width=25)
        self.trans_station_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Column 2 - Relay settings
        ttk.Label(col2, text="Relay Settings", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(col2, text="CT Ratio:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.trans_ctr_var = tk.StringVar(value="600")
        ttk.Entry(col2, textvariable=self.trans_ctr_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(col2, text="PT Ratio:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.trans_ptr_var = tk.StringVar(value="100")
        ttk.Entry(col2, textvariable=self.trans_ptr_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        # Column 3 - Transformer selection
        ttk.Label(col3, text="Transformer", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        self.trans_type_var = tk.StringVar(value="predefined")
        ttk.Radiobutton(col3, text="Predefined", variable=self.trans_type_var, 
                       value="predefined", command=self.on_trans_type_change).grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(col3, text="Custom", variable=self.trans_type_var, 
                       value="custom", command=self.on_trans_type_change).grid(row=1, column=1, sticky=tk.W)
        
        # Predefined transformer selection
        self.trans_kva_var = tk.StringVar()
        self.trans_kva_combo = ttk.Combobox(col3, textvariable=self.trans_kva_var, width=15)
        self.trans_kva_combo['values'] = ['45', '75', '112.5', '150', '225', '300', '500', '750', '1000', '1500', '2000', '2500']
        self.trans_kva_combo.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Custom transformer inputs (initially hidden)
        self.custom_trans_frame = ttk.Frame(col3)
        
        ttk.Label(self.custom_trans_frame, text="kVA:").grid(row=0, column=0, sticky=tk.W)
        self.custom_kva_var = tk.StringVar()
        ttk.Entry(self.custom_trans_frame, textvariable=self.custom_kva_var, width=10).grid(row=0, column=1)
        
        ttk.Label(self.custom_trans_frame, text="Z%:").grid(row=1, column=0, sticky=tk.W)
        self.custom_z_var = tk.StringVar()
        ttk.Entry(self.custom_trans_frame, textvariable=self.custom_z_var, width=10).grid(row=1, column=1)
        
        ttk.Label(self.custom_trans_frame, text="X/R:").grid(row=2, column=0, sticky=tk.W)
        self.custom_xr_var = tk.StringVar()
        ttk.Entry(self.custom_trans_frame, textvariable=self.custom_xr_var, width=10).grid(row=2, column=1)
        
        # Connection type
        ttk.Label(col3, text="Connection:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.trans_conn_var = tk.StringVar()
        self.trans_conn_combo = ttk.Combobox(col3, textvariable=self.trans_conn_var, width=15)
        self.trans_conn_combo['values'] = ['Δ-Yg', 'Yg-Yg', 'Δ-Δ', 'Y-Y']
        self.trans_conn_combo.grid(row=5, column=1, pady=5)
        
        ttk.Label(col3, text="Sec. Voltage (kV):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.trans_sec_voltage_var = tk.StringVar(value="0.48")
        ttk.Entry(col3, textvariable=self.trans_sec_voltage_var, width=15).grid(row=6, column=1, pady=5)
        
        # Line trace section
        trace_frame = ttk.Frame(input_frame)
        trace_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        ttk.Label(trace_frame, text="Line Trace:").pack(side=tk.LEFT, padx=5)
        self.trans_trace_label = ttk.Label(trace_frame, text="No file loaded", relief=tk.SUNKEN, width=50)
        self.trans_trace_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(trace_frame, text="Load", command=self.load_trans_line_trace).pack(side=tk.LEFT)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate Transformer Fault", 
                  command=self.calculate_trans_fault).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Bottom frame for results
        bottom_frame = ttk.Frame(paned)
        paned.add(bottom_frame, weight=1)
        
        # Results section
        results_frame = ttk.LabelFrame(bottom_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.trans_results_text = tk.Text(results_frame, wrap=tk.WORD, height=15, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.trans_results_text.yview)
        self.trans_results_text.configure(yscrollcommand=scrollbar.set)
        
        self.trans_results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
    def create_fault_location_tab(self):
        # Create main frame with paned window
        paned = ttk.PanedWindow(self.fault_location_tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Input
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        input_frame = ttk.LabelFrame(left_frame, text="Fault Location Parameters", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bus selection
        ttk.Label(input_frame, text="Bus Selection", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(input_frame, text="Voltage Level:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.loc_voltage_var = tk.StringVar()
        self.loc_voltage_combo = ttk.Combobox(input_frame, textvariable=self.loc_voltage_var, width=20)
        self.loc_voltage_combo.grid(row=1, column=1, padx=5, pady=5)
        self.loc_voltage_combo.bind('<<ComboboxSelected>>', self.on_loc_voltage_change)
        
        ttk.Label(input_frame, text="Station:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.loc_station_var = tk.StringVar()
        self.loc_station_combo = ttk.Combobox(input_frame, textvariable=self.loc_station_var, width=30)
        self.loc_station_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Line trace
        ttk.Label(input_frame, text="Line Trace:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=10)
        self.loc_trace_label = ttk.Label(input_frame, text="No file loaded", relief=tk.SUNKEN, width=30)
        self.loc_trace_label.grid(row=3, column=1, padx=5, pady=10)
        ttk.Button(input_frame, text="Load", command=self.load_loc_line_trace).grid(row=3, column=2, padx=5)
        
        # Fault parameters
        ttk.Label(input_frame, text="Fault Type:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.fault_type_var = tk.StringVar()
        self.fault_type_combo = ttk.Combobox(input_frame, textvariable=self.fault_type_var, width=20)
        self.fault_type_combo['values'] = ['3 Phase', 'Line to Ground', 'Line to Line', 'Double Line to Ground']
        self.fault_type_combo.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Fault Magnitude (A):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.fault_mag_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.fault_mag_var, width=20).grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Calculation Type:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.calc_type_var = tk.StringVar(value="Quick")
        ttk.Radiobutton(input_frame, text="Quick", variable=self.calc_type_var, 
                       value="Quick").grid(row=6, column=1, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Accurate", variable=self.calc_type_var, 
                       value="Accurate").grid(row=7, column=1, sticky=tk.W)
        
        # Calculate button
        ttk.Button(input_frame, text="Locate Fault", 
                  command=self.locate_fault).grid(row=8, column=0, columnspan=2, pady=20)
        
        # Right side - Plot
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        plot_frame = ttk.LabelFrame(right_frame, text="Fault Location Plot", padding=10)
        plot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fault_figure = Figure(figsize=(8, 6), dpi=100)
        self.fault_ax = self.fault_figure.add_subplot(111)
        self.fault_canvas = FigureCanvasTkAgg(self.fault_figure, master=plot_frame)
        self.fault_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Results text below plot
        results_frame = ttk.Frame(right_frame)
        results_frame.pack(fill=tk.X, pady=5)
        
        self.fault_result_label = ttk.Label(results_frame, text="", font=('Arial', 12, 'bold'))
        self.fault_result_label.pack()
        
    def create_sel_curves_tab(self):
        # Create main frame
        main_frame = ttk.Frame(self.sel_curves_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="SEL U-Curve Parameters", padding=20)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create grid for inputs
        ttk.Label(input_frame, text="U-Curve Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.sel_curve_var = tk.StringVar()
        self.sel_curve_combo = ttk.Combobox(input_frame, textvariable=self.sel_curve_var, width=15)
        self.sel_curve_combo['values'] = ['U1', 'U2', 'U3', 'U4', 'U5']
        self.sel_curve_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Time Dial Setting:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.time_dial_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.time_dial_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Tap Setting:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.tap_setting_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.tap_setting_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="CT Ratio (CTR:1):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.sel_ctr_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.sel_ctr_var, width=15).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Primary Fault Current (A):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.pri_fault_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.pri_fault_var, width=15).grid(row=4, column=1, padx=5, pady=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate Times", 
                  command=self.calculate_sel_times).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=20)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create result labels
        self.sel_results_frame = ttk.Frame(results_frame)
        self.sel_results_frame.pack()
        
        # Headers
        ttk.Label(self.sel_results_frame, text="Operation Time:", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=20, pady=10)
        ttk.Label(self.sel_results_frame, text="Reset Time:", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=20, pady=10)
        
        # Result values (initially empty)
        self.op_time_label = ttk.Label(self.sel_results_frame, text="", font=('Arial', 14))
        self.op_time_label.grid(row=1, column=0, padx=20, pady=5)
        
        self.rst_time_label = ttk.Label(self.sel_results_frame, text="", font=('Arial', 14))
        self.rst_time_label.grid(row=1, column=1, padx=20, pady=5)
        
        # Additional info
        self.sel_info_label = ttk.Label(results_frame, text="", font=('Arial', 10))
        self.sel_info_label.pack(pady=10)
    
    # Event handlers and calculation methods
    def load_initial_data(self):
        """Try to load initial data files"""
        try:
            self.update_status("Loading initial data...", "info")
            self.bus_dataframes = load_impedance_sheets()
            self.line_dataframes = load_clean_line_imp()
            
            if self.bus_dataframes:
                self.update_voltage_combos()
                self.data_status_label.config(text="Data loaded")
                self.update_status("Ready", "success")
            else:
                self.data_status_label.config(text="No data loaded")
                self.update_status("Please load impedance sheets", "warning")
        except Exception as e:
            self.show_error(f"Error loading initial data: {str(e)}")
            
    def load_all_data(self):
        """Load all required data files"""
        self.load_impedance_sheets_gui()
        if self.bus_dataframes:
            self.load_line_impedances_gui()
            
    def load_impedance_sheets_gui(self):
        """Load impedance sheets with GUI feedback"""
        try:
            self.bus_dataframes = load_impedance_sheets()
            if self.bus_dataframes:
                self.update_voltage_combos()
                messagebox.showinfo("Success", "Impedance sheets loaded successfully!")
                self.data_status_label.config(text="Data loaded")
            else:
                messagebox.showwarning("Warning", "No impedance sheets loaded.")
        except Exception as e:
            self.show_error(f"Error loading impedance sheets: {str(e)}")
            
    def load_line_impedances_gui(self):
        """Load line impedances with GUI feedback"""
        try:
            self.line_dataframes = load_clean_line_imp()
            if self.line_dataframes:
                messagebox.showinfo("Success", "Line impedances loaded successfully!")
            else:
                messagebox.showwarning("Warning", "No line impedances loaded.")
        except Exception as e:
            self.show_error(f"Error loading line impedances: {str(e)}")
            
    def load_line_trace_gui(self):
        """Load line trace for line fault calculations"""
        try:
            self.line_trace = load_line_trace()
            if self.line_trace:
                filename = list(self.line_trace.keys())[0] if self.line_trace else "No file"
                self.line_trace_label.config(text=filename)
                self.trans_trace_label.config(text=filename)
                self.loc_trace_label.config(text=filename)
                messagebox.showinfo("Success", f"Line trace '{filename}' loaded successfully!")
        except Exception as e:
            self.show_error(f"Error loading line trace: {str(e)}")
            
    def load_trans_line_trace(self):
        """Load line trace for transformer calculations"""
        self.load_line_trace_gui()
        
    def load_loc_line_trace(self):
        """Load line trace for fault location"""
        self.load_line_trace_gui()
        
    def update_voltage_combos(self):
        """Update all voltage combo boxes"""
        if self.bus_dataframes:
            # Filter dataframes to only include those with 'Bus' in the sheet name
            bus_dataframes = {k: v for k, v in self.bus_dataframes.items() if 'Bus' in k}
            voltage_levels = sorted(set(sheet_name.split('-')[0] for sheet_name in bus_dataframes))
            
            # Update all voltage combos
            for combo in [self.bus_voltage_combo, self.line_voltage_combo, 
                         self.trans_voltage_combo, self.loc_voltage_combo]:
                combo['values'] = voltage_levels
                
    def on_voltage_level_change(self, event):
        """Update station combo when voltage level changes"""
        self.update_station_combo(self.bus_voltage_var.get(), self.bus_station_combo)
        
    def on_line_voltage_change(self, event):
        """Update station combo for line fault tab"""
        self.update_station_combo(self.line_voltage_var.get(), self.line_station_combo)
        
    def on_trans_voltage_change(self, event):
        """Update station combo for transformer tab"""
        self.update_station_combo(self.trans_voltage_var.get(), self.trans_station_combo)
        
    def on_loc_voltage_change(self, event):
        """Update station combo for fault location tab"""
        self.update_station_combo(self.loc_voltage_var.get(), self.loc_station_combo)
        
    def update_station_combo(self, voltage_level, station_combo):
        """Update station combo box based on voltage level"""
        if self.bus_dataframes and voltage_level:
            voltage_df = self.bus_dataframes.get(voltage_level)
            if voltage_df is not None:
                stations = voltage_df.iloc[:, 0].tolist()
                station_combo['values'] = stations
                
    def on_trans_type_change(self):
        """Handle transformer type change"""
        if self.trans_type_var.get() == "custom":
            self.custom_trans_frame.grid(row=3, column=0, columnspan=2, pady=5)
            self.trans_kva_combo.grid_remove()
        else:
            self.custom_trans_frame.grid_remove()
            self.trans_kva_combo.grid(row=2, column=0, columnspan=2, pady=5)
            
    def calculate_bus_fault(self):
        """Calculate bus fault current"""
        try:
            if not self.bus_dataframes:
                messagebox.showwarning("Warning", "Please load impedance sheets first.")
                return
                
            voltage = self.bus_voltage_var.get()
            station_idx = self.bus_station_combo.current()
            
            if not voltage or station_idx < 0:
                messagebox.showwarning("Warning", "Please select voltage level and station.")
                return
                
            # Get selected record
            voltage_df = self.bus_dataframes[voltage]
            selected_record = voltage_df.iloc[station_idx]
            
            # Create ZBus object
            self.zbus_selection = ZBus(selected_record)
            
            # Calculate and display results
            self.buffer = []
            self.zbus_selection.display_info(self.buffer)
            
            # Display results
            self.bus_results_text.delete(1.0, tk.END)
            self.bus_results_text.insert(tk.END, "".join(self.buffer))
            
            self.update_status("Bus fault calculation completed", "success")
            
        except Exception as e:
            self.show_error(f"Error calculating bus fault: {str(e)}")
            
    def calculate_line_fault(self):
        """Calculate line fault current"""
        try:
            if not self.bus_dataframes:
                messagebox.showwarning("Warning", "Please load impedance sheets first.")
                return
                
            if not self.line_trace:
                messagebox.showwarning("Warning", "Please load line trace.")
                return
                
            # Get bus selection
            voltage = self.line_voltage_var.get()
            station_idx = self.line_station_combo.current()
            
            if not voltage or station_idx < 0:
                messagebox.showwarning("Warning", "Please select voltage level and station.")
                return
                
            # Get CTR and PTR
            try:
                ctr = float(self.ctr_var.get())
                ptr = float(self.ptr_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Please enter valid CTR and PTR values.")
                return
                
            # Get selected record
            voltage_df = self.bus_dataframes[voltage]
            selected_record = voltage_df.iloc[station_idx]
            
            # Create ZBus object
            self.zbus_selection = ZBus(selected_record)
            
            # Process line trace
            if isinstance(self.line_trace, dict):
                first_sheet_name_trace = list(self.line_trace.keys())[0]
                line_trace_df = self.line_trace[first_sheet_name_trace]
            else:
                line_trace_df = self.line_trace
                first_sheet_name_trace = "Line Trace"
                
            # Map impedances
            if isinstance(self.line_dataframes, dict):
                first_sheet_name = list(self.line_dataframes.keys())[0]
                line_dataframes_df = self.line_dataframes[first_sheet_name]
            else:
                line_dataframes_df = self.line_dataframes
                
            line_trace_df = map_impedances(line_trace_df, line_dataframes_df)
            
            # Create ZLine object
            self.zline_selection = ZLine(line_trace_df, first_sheet_name_trace, ctr, ptr)
            self.zline_selection.get_individual_parameters()
            
            # Calculate
            self.buffer = []
            self.zbus_selection.display_info(self.buffer)
            self.buffer.append(f"\nLine trace {first_sheet_name_trace}:\n")
            self.zline_selection.display_info(self.buffer)
            self.buffer.append(f"CT ratio: {ctr}:1   PT Ratio: {ptr}:1\n")
            primary_line_fault_calculation(self.zbus_selection, self.zline_selection, self.buffer)
            
            # Display results
            self.line_results_text.delete(1.0, tk.END)
            self.line_results_text.insert(tk.END, "".join(self.buffer))
            
            self.update_status("Line fault calculation completed", "success")
            
        except Exception as e:
            self.show_error(f"Error calculating line fault: {str(e)}")
            
    def calculate_trans_fault(self):
        """Calculate transformer fault current"""
        try:
            # First calculate line fault
            self.calculate_line_fault()
            
            if not self.zbus_selection or not self.zline_selection:
                return
                
            # Get transformer parameters
            if self.trans_type_var.get() == "predefined":
                kva = self.trans_kva_var.get()
                if not kva:
                    messagebox.showwarning("Warning", "Please select transformer kVA.")
                    return
                    
                # Get predefined values
                percent_z, x_r = ZTrans.predefined_transformers[kva]
                kva = float(kva)
            else:
                # Get custom values
                try:
                    kva = float(self.custom_kva_var.get())
                    percent_z = float(self.custom_z_var.get())
                    x_r = float(self.custom_xr_var.get())
                except ValueError:
                    messagebox.showwarning("Warning", "Please enter valid transformer parameters.")
                    return
                    
            # Get connection and voltage
            conn = self.trans_conn_var.get()
            if not conn:
                messagebox.showwarning("Warning", "Please select connection type.")
                return
                
            try:
                sec_voltage = float(self.trans_sec_voltage_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Please enter valid secondary voltage.")
                return
                
            # Create transformer object
            self.ztrans_selection = ZTrans(conn, sec_voltage, percent_z, kva, x_r)
            
            # Calculate
            self.buffer.append("\n" + "="*80 + "\n")
            self.ztrans_selection.display_info(self.buffer)
            sec_trans_fault_calculation(self.zbus_selection, self.zline_selection, 
                                      self.ztrans_selection, self.buffer)
            
            # Display results
            self.trans_results_text.delete(1.0, tk.END)
            self.trans_results_text.insert(tk.END, "".join(self.buffer))
            
            self.update_status("Transformer fault calculation completed", "success")
            
        except Exception as e:
            self.show_error(f"Error calculating transformer fault: {str(e)}")
            
    def locate_fault(self):
        """Locate fault on line"""
        try:
            if not self.bus_dataframes or not self.line_trace:
                messagebox.showwarning("Warning", "Please load required data first.")
                return
                
            # Get parameters
            voltage = self.loc_voltage_var.get()
            station_idx = self.loc_station_combo.current()
            fault_type = self.fault_type_var.get()
            
            try:
                fault_mag = int(self.fault_mag_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Please enter valid fault magnitude.")
                return
                
            if not all([voltage, station_idx >= 0, fault_type, fault_mag]):
                messagebox.showwarning("Warning", "Please fill all fields.")
                return
                
            # Get bus selection
            voltage_df = self.bus_dataframes[voltage]
            selected_record = voltage_df.iloc[station_idx]
            zbus_obj = ZBus(selected_record)
            
            # Process line trace
            if isinstance(self.line_trace, dict):
                first_sheet_name_trace = list(self.line_trace.keys())[0]
                line_trace_df = self.line_trace[first_sheet_name_trace]
            else:
                line_trace_df = self.line_trace
                first_sheet_name_trace = "Line Trace"
                
            # Map impedances
            if isinstance(self.line_dataframes, dict):
                first_sheet_name = list(self.line_dataframes.keys())[0]
                line_dataframes_df = self.line_dataframes[first_sheet_name]
            else:
                line_dataframes_df = self.line_dataframes
                
            line_trace_df = map_impedances(line_trace_df, line_dataframes_df)
            zline_obj = ZLine(line_trace_df, first_sheet_name_trace, 1, 1)
            zline_obj.get_individual_parameters()
            
            # Clear previous plot
            self.fault_ax.clear()
            
            # Temporarily redirect matplotlib to our canvas
            plt.figure(self.fault_figure.number)
            
            # Calculate based on fault type
            if fault_type == '3 Phase':
                distance, current = locate_primary_line_fault_3ph(zbus_obj, zline_obj, fault_mag)
            elif fault_type == 'Line to Ground':
                distance, current = locate_primary_line_fault_l_g(zbus_obj, zline_obj, fault_mag)
            elif fault_type == 'Line to Line':
                distance, current = locate_primary_line_fault_l_l(zbus_obj, zline_obj, fault_mag)
            elif fault_type == 'Double Line to Ground':
                distance, current = locate_primary_line_fault_l_l_g(zbus_obj, zline_obj, fault_mag)
                
            # The plot is already created by the locate functions
            # Just update our canvas
            self.fault_canvas.draw()
            
            # Display result
            self.fault_result_label.config(
                text=f"Fault Location: {distance:.2f} miles from station\n"
                     f"Calculated Current: {current:.0f} Amps"
            )
            
            self.update_status("Fault location calculated", "success")
            
        except Exception as e:
            self.show_error(f"Error locating fault: {str(e)}")
            
    def calculate_sel_times(self):
        """Calculate SEL curve operate and reset times"""
        try:
            # Get all parameters
            curve_type = self.sel_curve_var.get()
            
            try:
                td = float(self.time_dial_var.get())
                tap = float(self.tap_setting_var.get())
                ctr = float(self.sel_ctr_var.get())
                pri_fault = float(self.pri_fault_var.get())
            except ValueError:
                messagebox.showwarning("Warning", "Please enter valid numeric values.")
                return
                
            if not curve_type:
                messagebox.showwarning("Warning", "Please select curve type.")
                return
                
            # Calculate M
            m = pri_fault / (tap * ctr)
            
            # Calculate times based on curve type
            if curve_type == 'U1':
                op_time = td * (0.0226 + (0.0104 / ((m ** 0.02) - 1)))
                rst_time = td * (1.08 / (1 - (m ** 2)))
            elif curve_type == 'U2':
                op_time = td * (0.180 + (5.95 / ((m ** 2) - 1)))
                rst_time = td * (5.95 / (1 - (m ** 2)))
            elif curve_type == 'U3':
                op_time = td * (0.0963 + (3.88 / ((m ** 2) - 1)))
                rst_time = td * (3.88 / (1 - (m ** 2)))
            elif curve_type == 'U4':
                op_time = td * (0.0352 + (5.67 / ((m ** 2) - 1)))
                rst_time = td * (5.67/ (1 - (m ** 2)))
            elif curve_type == 'U5':
                op_time = td * (0.0262 + (0.00342/ ((m ** 0.02) - 1)))
                rst_time = td * (0.323 / (1 - (m ** 2)))
                
            # Convert to cycles
            op_time_cy = op_time / 0.0166666666666666667
            rst_time_cy = rst_time / 0.0166666666666666667
            
            # Display results
            self.op_time_label.config(text=f"{op_time:.2f} seconds\n{op_time_cy:.1f} cycles")
            self.rst_time_label.config(text=f"{-rst_time:.2f} seconds\n{-rst_time_cy:.1f} cycles")
            
            # Additional info
            self.sel_info_label.config(text=f"M = {m:.3f} (Multiple of pickup)")
            
            self.update_status("SEL times calculated", "success")
            
        except Exception as e:
            self.show_error(f"Error calculating SEL times: {str(e)}")
            
    def save_results(self):
        """Save current results to file"""
        if not self.buffer:
            messagebox.showwarning("Warning", "No results to save.")
            return
            
        savetxt(self.buffer)
        
    def clear_results(self):
        """Clear all result displays"""
        self.bus_results_text.delete(1.0, tk.END)
        self.line_results_text.delete(1.0, tk.END)
        self.trans_results_text.delete(1.0, tk.END)
        self.fault_ax.clear()
        self.fault_canvas.draw()
        self.fault_result_label.config(text="")
        self.op_time_label.config(text="")
        self.rst_time_label.config(text="")
        self.sel_info_label.config(text="")
        self.buffer = []
        self.update_status("Results cleared", "info")
        
    def reset_all(self):
        """Reset all data and results"""
        self.clear_results()
        self.bus_dataframes = None
        self.line_dataframes = None
        self.zbus_selection = None
        self.zline_selection = None
        self.ztrans_selection = None
        self.line_trace = None
        self.data_status_label.config(text="No data loaded")
        self.update_status("All data reset", "warning")
        
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                          "Power System Fault Calculator\n\n"
                          "Version 2.0\n\n"
                          "A comprehensive tool for calculating fault currents\n"
                          "in power distribution systems.\n\n"
                          "© 2024")
        
    def show_user_guide(self):
        """Show user guide"""
        guide_text = """
USER GUIDE

1. GETTING STARTED:
   - Load impedance sheets (Andy Sheets) using File menu
   - Load line impedances if available
   - Load line traces for specific calculations

2. BUS FAULT CALCULATIONS:
   - Select voltage level and station
   - Click 'Calculate Bus Fault' to see results

3. LINE FAULT CALCULATIONS:
   - Select bus parameters
   - Enter CT and PT ratios
   - Load line trace file
   - Calculate to see fault currents

4. TRANSFORMER FAULTS:
   - Complete line fault calculation first
   - Select transformer (predefined or custom)
   - Enter connection type and secondary voltage
   - Calculate for secondary fault currents

5. FAULT LOCATION:
   - Select bus and load line trace
   - Choose fault type and enter magnitude
   - Results show distance and plot

6. SEL CURVES:
   - Enter all relay parameters
   - Calculate for operate/reset times

TIPS:
- Save results using File > Save Results
- Use toolbar buttons for quick navigation
- Check status bar for operation feedback
"""
        
        # Create a new window for the guide
        guide_window = tk.Toplevel(self.root)
        guide_window.title("User Guide")
        guide_window.geometry("600x500")
        
        text_widget = tk.Text(guide_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, guide_text)
        text_widget.config(state=tk.DISABLED)
        
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.update_status("Error occurred", "error")
    
    def change_theme(self, theme_name):
        """Change the application theme"""
        try:
            from gui_config import apply_theme, THEMES
            # Update colors
            self.colors = THEMES[theme_name]
            # Reapply theme
            apply_theme(self.style, theme_name)
            # Update root window background
            self.root.configure(bg=self.colors['background'])
            # Show confirmation
            self.update_status(f"Theme changed to {theme_name} mode", "success")
        except Exception as e:
            self.show_error(f"Error changing theme: {str(e)}")
    
    def update_status(self, message, status_type="info"):
        """Update status bar with better visual feedback"""
        # Update message
        self.status_label.config(text=message)
        
        # Briefly highlight status bar for important messages
        if status_type == "success":
            self.status_label.config(foreground=self.colors['success'])
            self.root.after(2000, lambda: self.status_label.config(foreground=self.colors['text']))
        elif status_type == "error":
            self.status_label.config(foreground=self.colors['danger'])
        elif status_type == "warning":
            self.status_label.config(foreground=self.colors['warning'])

def main():
    root = tk.Tk()
    
    # Splash screen disabled for now - uncomment below to enable when splash_screen.py is available
    # try:
    #     from splash_screen import show_splash
    #     show_splash(root, duration=2.5)
    # except (ImportError, Exception) as e:
    #     print(f"Splash screen not available: {e}")
    #     pass
    
    app = PowerSystemFaultCalculatorGUI(root)
    root.mainloop()

if __name__ == '__main__':
    # Run without splash screen if there are any import issues
    try:
        main()
    except Exception as e:
        print(f"Error in main: {e}")
        # Fallback - run without splash screen
        import tkinter as tk
        root = tk.Tk()
        app = PowerSystemFaultCalculatorGUI(root)
        root.mainloop()