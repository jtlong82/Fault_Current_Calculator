# GUI Configuration and Styling

# Color schemes
THEMES = {
    'light': {
        'background': '#f8f9fa',          # Light gray background
        'primary': '#1a1a2e',             # Deep navy blue
        'secondary': '#0466c8',           # Bright blue
        'accent': '#0353a4',              # Medium blue
        'success': '#06ffa5',             # Bright green
        'warning': '#ffb700',             # Amber
        'danger': '#dc2f2f',              # Red
        'text': '#212529',                # Almost black
        'text_light': '#6c757d',          # Gray
        'text_white': '#ffffff',          # White
        'border': '#dee2e6',              # Light gray border
        'border_light': '#e9ecef',        # Very light border
        'input_bg': '#ffffff',            # White
        'input_border': '#ced4da',        # Gray border
        'button_hover': '#0353a4',        # Darker blue
        'card_bg': '#ffffff',             # White cards
        'shadow': '#00000010',            # Subtle shadow
    },
    'dark': {
        'background': '#1a1a2e',          # Dark navy background
        'primary': '#0466c8',             # Bright blue
        'secondary': '#06ffa5',           # Bright green
        'accent': '#0353a4',              # Medium blue
        'success': '#06ffa5',             # Bright green
        'warning': '#ffb700',             # Amber
        'danger': '#ff4545',              # Bright red
        'text': '#ffffff',                # White
        'text_light': '#b8b8b8',          # Light gray
        'text_white': '#ffffff',          # White
        'border': '#2d2d44',              # Dark border
        'border_light': '#3d3d5c',        # Slightly lighter border
        'input_bg': '#2d2d44',            # Dark input
        'input_border': '#3d3d5c',        # Dark border
        'button_hover': '#06ffa5',        # Green hover
        'card_bg': '#232342',             # Dark card
        'shadow': '#00000040',            # Darker shadow
    }
}

# Default theme
COLORS = THEMES['light']

# Font configurations
FONTS = {
    'default': ('Segoe UI', 10),
    'heading': ('Segoe UI', 14, 'bold'),
    'subheading': ('Segoe UI', 12, 'bold'),
    'monospace': ('Consolas', 10),
    'small': ('Segoe UI', 9),
    'large': ('Segoe UI', 16),
    'button': ('Segoe UI Semibold', 10),
    'label': ('Segoe UI', 10)
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

def apply_theme(style, theme_name='light'):
    """Apply custom theme to ttk widgets"""
    
    # Set the color scheme
    global COLORS
    COLORS = THEMES.get(theme_name, THEMES['light'])
    
    # Configure general style
    style.configure('.',
                   background=COLORS['background'],
                   foreground=COLORS['text'],
                   font=FONTS['default'])
    
    # Labels
    style.configure('TLabel', 
                   background=COLORS['background'],
                   foreground=COLORS['text'],
                   font=FONTS['label'])
    
    style.configure('Title.TLabel',
                   font=FONTS['heading'],
                   foreground=COLORS['primary'])
    
    style.configure('Subtitle.TLabel',
                   font=FONTS['subheading'],
                   foreground=COLORS['accent'])
    
    # Modern button styling
    style.configure('TButton',
                   padding=(15, 8),
                   relief='flat',
                   background=COLORS['secondary'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   focuscolor='none',
                   font=FONTS['button'])
    
    style.map('TButton',
             background=[('active', COLORS['accent']),
                        ('pressed', COLORS['primary'])])
    
    # Primary button style
    style.configure('Primary.TButton',
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'])
    
    style.map('Primary.TButton',
             background=[('active', COLORS['accent'])])
    
    # Success button style
    style.configure('Success.TButton',
                   background=COLORS['success'],
                   foreground=COLORS['primary'])
    
    # Warning button style
    style.configure('Warning.TButton',
                   background=COLORS['warning'],
                   foreground=COLORS['primary'])
    
    # Danger button style
    style.configure('Danger.TButton',
                   background=COLORS['danger'],
                   foreground=COLORS['text_white'])
    
    # Modern frame styling
    style.configure('TFrame',
                   background=COLORS['background'],
                   borderwidth=0)
    
    style.configure('Card.TFrame',
                   background=COLORS['card_bg'],
                   relief='flat',
                   borderwidth=1)
    
    # Modern LabelFrame with rounded corners effect
    style.configure('TLabelframe',
                   background=COLORS['card_bg'],
                   bordercolor=COLORS['border_light'],
                   relief='flat',
                   borderwidth=1,
                   padding=15)
    
    style.configure('TLabelframe.Label',
                   background=COLORS['card_bg'],
                   foreground=COLORS['primary'],
                   font=FONTS['subheading'])
    
    # Modern Notebook styling
    style.configure('TNotebook',
                   background=COLORS['background'],
                   borderwidth=0,
                   tabmargins=[10, 10, 10, 0])
    
    style.configure('TNotebook.Tab',
                   padding=[25, 12],
                   background=COLORS['background'],
                   foreground=COLORS['text_light'],
                   borderwidth=0,
                   font=FONTS['button'])
    
    style.map('TNotebook.Tab',
             background=[('selected', COLORS['card_bg'])],
             foreground=[('selected', COLORS['primary'])],
             expand=[('selected', [1, 1, 1, 0])])
    
    # Modern input styling
    style.configure('TCombobox',
                   fieldbackground=COLORS['input_bg'],
                   background=COLORS['input_bg'],
                   bordercolor=COLORS['input_border'],
                   borderwidth=1,
                   relief='flat',
                   padding=5)
    
    style.map('TCombobox',
             fieldbackground=[('focus', COLORS['input_bg'])],
             bordercolor=[('focus', COLORS['secondary'])])
    
    style.configure('TEntry',
                   fieldbackground=COLORS['input_bg'],
                   bordercolor=COLORS['input_border'],
                   borderwidth=1,
                   relief='flat',
                   padding=5)
    
    style.map('TEntry',
             fieldbackground=[('focus', COLORS['input_bg'])],
             bordercolor=[('focus', COLORS['secondary'])])
    
    # Modern scrollbar
    style.configure('TScrollbar',
                   background=COLORS['background'],
                   bordercolor=COLORS['border'],
                   arrowcolor=COLORS['primary'],
                   troughcolor=COLORS['border_light'],
                   borderwidth=0,
                   width=12)
    
    style.map('TScrollbar',
             background=[('active', COLORS['secondary'])])
    
    # Radio buttons
    style.configure('TRadiobutton',
                   background=COLORS['card_bg'],
                   foreground=COLORS['text'],
                   focuscolor='none')
    
    # Separator
    style.configure('TSeparator',
                   background=COLORS['border_light'])
    
    # Progressbar
    style.configure('TProgressbar',
                   background=COLORS['secondary'],
                   troughcolor=COLORS['border_light'],
                   borderwidth=0,
                   lightcolor=COLORS['secondary'],
                   darkcolor=COLORS['secondary'])