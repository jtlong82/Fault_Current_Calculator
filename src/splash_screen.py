import tkinter as tk
from tkinter import ttk
import time
import threading

class SplashScreen:
    def __init__(self, root, duration=3):
        self.root = root
        self.duration = duration
        
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Set splash dimensions
        splash_width = 600
        splash_height = 400
        
        # Center the splash screen
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        
        # Create gradient background
        self.canvas = tk.Canvas(self.splash, width=splash_width, height=splash_height, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient effect
        self.create_gradient()
        
        # Add content
        self.add_content()
        
        # Add progress bar
        self.add_progress_bar()
        
        # Update splash screen
        self.splash.update()
        
    def create_gradient(self):
        """Create a gradient background"""
        width = 600
        height = 400
        
        # Create gradient from dark to light blue
        for i in range(height):
            # Calculate color
            ratio = i / height
            r = int(26 + (4 - 26) * ratio)  # From 26 to 4
            g = int(26 + (102 - 26) * ratio)  # From 26 to 102
            b = int(46 + (200 - 46) * ratio)  # From 46 to 200
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color, width=1)
    
    def add_content(self):
        """Add text and logo to splash screen"""
        # Main title
        self.canvas.create_text(300, 100, text="Power System", font=('Segoe UI', 36, 'bold'), 
                               fill='white', anchor='center')
        self.canvas.create_text(300, 150, text="Fault Calculator", font=('Segoe UI', 36, 'bold'), 
                               fill='white', anchor='center')
        
        # Version
        self.canvas.create_text(300, 200, text="Version 2.0", font=('Segoe UI', 14), 
                               fill='#ffffff80', anchor='center')
        
        # Lightning bolt icon
        self.draw_lightning_bolt()
        
        # Loading text
        self.loading_text = self.canvas.create_text(300, 320, text="Initializing...", 
                                                   font=('Segoe UI', 12), fill='white', anchor='center')
        
    def draw_lightning_bolt(self):
        """Draw a simple lightning bolt icon"""
        points = [280, 230, 300, 250, 290, 250, 310, 280, 295, 260, 320, 260, 280, 230]
        self.canvas.create_polygon(points, fill='#ffb700', outline='#ffa500', width=2)
        
    def add_progress_bar(self):
        """Add a progress bar"""
        # Create progress bar background
        self.canvas.create_rectangle(100, 340, 500, 350, fill='#ffffff20', outline='')
        
        # Create progress bar
        self.progress_rect = self.canvas.create_rectangle(100, 340, 100, 350, fill='#06ffa5', outline='')
        
    def update_progress(self, value, text="Loading..."):
        """Update progress bar and text"""
        # Update progress bar
        self.canvas.coords(self.progress_rect, 100, 340, 100 + (value * 4), 350)
        
        # Update text
        self.canvas.itemconfig(self.loading_text, text=text)
        self.splash.update()
        
    def close(self):
        """Close the splash screen"""
        self.splash.destroy()
        
    def show_with_progress(self):
        """Show splash with animated progress"""
        steps = [
            (20, "Loading modules..."),
            (40, "Initializing interface..."),
            (60, "Loading configurations..."),
            (80, "Preparing calculations..."),
            (100, "Ready!")
        ]
        
        for progress, text in steps:
            self.update_progress(progress, text)
            time.sleep(self.duration / len(steps))
            
        time.sleep(0.5)  # Brief pause at 100%
        self.close()

def show_splash(root, duration=3):
    """Show splash screen before main window"""
    # Hide main window
    root.withdraw()
    
    # Create and show splash
    splash = SplashScreen(root, duration)
    
    # Run splash in separate thread
    def run_splash():
        splash.show_with_progress()
        # Show main window after splash
        root.deiconify()
        
    splash_thread = threading.Thread(target=run_splash)
    splash_thread.daemon = True
    splash_thread.start()
    
    return splash