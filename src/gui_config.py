# GUI Configuration and Styling

# Color scheme
COLORS = {
    'background': '#f0f0f0',
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'text': '#2c3e50',
    'text_light': '#7f8c8d',
    'border': '#bdc3c7',
    'input_bg': '#ffffff',
    'button_hover': '#34495e'
}

# Font configurations
FONTS = {
    'default': ('Arial', 10),
    'heading': ('Arial', 12, 'bold'),
    'subheading': ('Arial', 11, 'bold'),
    'monospace': ('Courier', 10),
    'small': ('Arial', 9),
    'large': ('Arial', 14)
}

# Window settings
WINDOW_SETTINGS = {
    'min_width': 1200,
    'min_height': 700,
    'default_width': 1400,
    'default_height': 900
}

# Plot settings
PLOT_SETTINGS = {
    'figure_dpi': 100,
    'grid': True,
    'grid_alpha': 0.3,
    'line_width': 2,
    'marker_size': 8,
    'annotation_size': 9
}

def apply_theme(style):
    """Apply custom theme to ttk widgets"""
    
    # Configure colors for different widget states
    style.configure('TLabel', 
                   background=COLORS['background'],
                   foreground=COLORS['text'])
    
    style.configure('Title.TLabel',
                   font=FONTS['heading'],
                   foreground=COLORS['primary'])
    
    style.configure('TButton',
                   padding=6,
                   relief='flat',
                   background=COLORS['primary'],
                   foreground='white')
    
    style.map('TButton',
             background=[('active', COLORS['button_hover']),
                        ('pressed', COLORS['secondary'])])
    
    style.configure('Success.TButton',
                   background=COLORS['success'])
    
    style.configure('Warning.TButton',
                   background=COLORS['warning'])
    
    style.configure('Danger.TButton',
                   background=COLORS['danger'])
    
    style.configure('TFrame',
                   background=COLORS['background'],
                   borderwidth=0)
    
    style.configure('Card.TFrame',
                   background='white',
                   relief='raised',
                   borderwidth=1)
    
    style.configure('TLabelframe',
                   background=COLORS['background'],
                   bordercolor=COLORS['border'],
                   relief='groove')
    
    style.configure('TLabelframe.Label',
                   background=COLORS['background'],
                   foreground=COLORS['primary'],
                   font=FONTS['subheading'])
    
    style.configure('TNotebook',
                   background=COLORS['background'],
                   borderwidth=0)
    
    style.configure('TNotebook.Tab',
                   padding=[12, 8],
                   background=COLORS['background'])
    
    style.map('TNotebook.Tab',
             background=[('selected', 'white')],
             expand=[('selected', [1, 1, 1, 0])])
    
    style.configure('TCombobox',
                   fieldbackground=COLORS['input_bg'],
                   borderwidth=1,
                   relief='solid')
    
    style.configure('TEntry',
                   fieldbackground=COLORS['input_bg'],
                   borderwidth=1,
                   relief='solid')
    
    style.configure('TScrollbar',
                   background=COLORS['background'],
                   bordercolor=COLORS['border'],
                   arrowcolor=COLORS['primary'],
                   troughcolor=COLORS['input_bg'])