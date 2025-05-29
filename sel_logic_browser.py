import os
import re
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from collections import defaultdict, OrderedDict

class SELLogicDecoder:
    def __init__(self):
        self.logic_bits = {}  # Dictionary to store logic bit definitions
        self.settings = {}  # Dictionary to store other settings (non-logic)
        
    def parse_settings_file(self, file_path):
        """Parse an SEL settings file and extract logic bits and other settings."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Find the section identifier (e.g., [1], [2], [L1], [L2], etc.)
            section_match = re.search(r'\[([A-Z0-9]+)\]', content)
            if section_match:
                section = section_match.group(1)
                print(f"Processing section {section} from {file_path}")
                
                # Extract all settings with pattern "SETTING_NAME,"VALUE""
                settings_pattern = re.finditer(r'([A-Z0-9_]+),"([^"]*)"', content)
                
                for match in settings_pattern:
                    setting_name = match.group(1)
                    value = match.group(2).strip()
                    
                    # Skip empty settings
                    if value == "NA" or value == "0" or not value:
                        continue
                    
                    # Determine if it's a logic equation or regular setting
                    if any(op in value for op in [" AND ", " OR ", " NOT ", "("]) or "TRIG" in value:
                        # It looks like a logic equation
                        self.logic_bits[setting_name] = value
                    else:
                        # It's probably a regular setting
                        self.settings[setting_name] = value
                
                # Special handling for SET/RST logic bits which define LT bits
                set_patterns = re.finditer(r'SET(\d+),"([^"]*)"', content)
                rst_patterns = re.finditer(r'RST(\d+),"([^"]*)"', content)
                
                # Store SET logic
                for match in set_patterns:
                    bit_num = match.group(1)
                    logic = match.group(2).strip()
                    if logic != "NA" and logic != "0":
                        bit_name = f"LT{bit_num}"
                        self.logic_bits[bit_name] = f"SET: {logic}"
                
                # Store RST logic
                for match in rst_patterns:
                    bit_num = match.group(1)
                    logic = match.group(2).strip()
                    if logic != "NA" and logic != "0":
                        # If LT already exists, append the RST logic
                        bit_name = f"LT{bit_num}"
                        if bit_name in self.logic_bits:
                            self.logic_bits[bit_name] += f"\nRST: {logic}"
                        else:
                            self.logic_bits[bit_name] = f"RST: {logic}"
                
                return True
            else:
                print(f"No section found in {file_path}")
                return False
                
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return False
    
    def parse_directory(self, directory):
        """Parse all .txt files in a directory that might contain SEL settings."""
        success = False
        for filename in os.listdir(directory):
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(directory, filename)
                if self.parse_settings_file(file_path):
                    success = True
        return success
    
    def simple_expand_logic(self, expression):
        """
        Simply replace word bits with their definitions without recursive expansion.
        This shows one level of expansion for better readability.
        """
        if not expression or expression == "0" or expression == "NA":
            return expression
        
        # If it's a SET/RST definition, handle separately
        if expression.startswith("SET:") or expression.startswith("RST:"):
            parts = expression.split("\n")
            expanded_parts = []
            for part in parts:
                prefix = part.split(":")[0] + ":"
                logic = ":".join(part.split(":")[1:]).strip()
                expanded_logic = self.simple_expand_logic(logic)
                expanded_parts.append(f"{prefix} {expanded_logic}")
            return "\n".join(expanded_parts)
            
        # Find all word bits (like LT01, SV02, etc.) in the expression
        word_bits = re.findall(r'\b([A-Z0-9_]+)(?!\s*=|\s*:)', expression)
        
        # Prepare expanded explanation
        bit_definitions = []
        for bit in word_bits:
            # Skip if it's a common operator or number
            if bit in ["AND", "OR", "NOT", "XOR", "R_TRIG", "F_TRIG"] or bit.isdigit():
                continue
            
            # Get the definition if available
            if bit in self.logic_bits:
                bit_definitions.append(f"{bit} = {self.logic_bits[bit]}")
        
        # Return original expression followed by bit definitions
        if bit_definitions:
            return expression + "\n\nWhere:\n" + "\n".join(bit_definitions)
        else:
            return expression
    
    def decode_equation(self, equation_name):
        """Decode a specific logic equation by name."""
        if equation_name in self.logic_bits:
            original = self.logic_bits[equation_name]
            expanded = self.simple_expand_logic(original)
            return {
                "equation": equation_name,
                "original": original,
                "expanded": expanded
            }
        elif equation_name in self.settings:
            # Return non-logic settings too
            return {
                "equation": equation_name,
                "original": self.settings[equation_name],
                "expanded": self.settings[equation_name]
            }
        else:
            return {
                "equation": equation_name,
                "error": "Setting not found"
            }
    
    def get_all_settings(self):
        """Get all settings (logic and non-logic) as a sorted dictionary."""
        all_settings = {}
        all_settings.update(self.logic_bits)
        all_settings.update(self.settings)
        return dict(sorted(all_settings.items()))

    def get_all_logic_bits(self):
        """Get all logic bits as a sorted dictionary."""
        return dict(sorted(self.logic_bits.items()))
    
    def search_settings(self, search_term):
        """Search for settings containing the search term."""
        results = {}
        search_term = search_term.upper()
        
        # Search in setting names
        for name, value in self.get_all_settings().items():
            if search_term in name:
                results[name] = value
        
        # Search in setting values
        for name, value in self.get_all_settings().items():
            if name not in results and search_term in str(value).upper():
                results[name] = value
                
        return results


class SELLogicBrowserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SEL Relay Logic Browser")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        self.decoder = SELLogicDecoder()
        self.current_dir = ""
        self.current_equation = ""
        
        self._create_ui()
        
    def _create_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top frame for controls
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Directory selection
        ttk.Label(top_frame, text="Settings Directory:").pack(side=tk.LEFT, padx=(0, 5))
        self.dir_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.dir_var, width=50).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(top_frame, text="Browse...", command=self._browse_directory).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(top_frame, text="Load Settings", command=self._load_settings).pack(side=tk.LEFT, padx=(0, 5))
        
        # Search
        ttk.Label(top_frame, text="Search:").pack(side=tk.LEFT, padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        ttk.Entry(top_frame, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(top_frame, text="Clear", command=self._clear_search).pack(side=tk.LEFT)
        
        # Create paned window
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left frame - Settings list
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # Settings list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.settings_list = ttk.Treeview(list_frame, columns=("Type",), show="headings")
        self.settings_list.heading("Type", text="Type")
        self.settings_list.column("Type", width=80, anchor="center")
        self.settings_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.settings_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.settings_list.configure(yscrollcommand=scrollbar.set)
        
        self.settings_list.bind("<<TreeviewSelect>>", self._on_setting_selected)
        
        # Filter buttons
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.filter_var = tk.StringVar(value="All")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="All", 
                       command=self._apply_filter).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(filter_frame, text="Logic", variable=self.filter_var, value="Logic", 
                       command=self._apply_filter).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(filter_frame, text="Settings", variable=self.filter_var, value="Settings", 
                       command=self._apply_filter).pack(side=tk.LEFT, padx=(0, 10))
        
        # Category filter dropdown
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=(10, 5))
        self.category_var = tk.StringVar(value="All")
        self.category_dropdown = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly")
        self.category_dropdown.pack(side=tk.LEFT, padx=(0, 5))
        self.category_dropdown.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())
        
        # Right frame - Details
        self.right_frame = ttk.Frame(paned_window)
        paned_window.add(self.right_frame, weight=2)
        
        # Current setting name
        self.setting_name_var = tk.StringVar()
        ttk.Label(self.right_frame, textvariable=self.setting_name_var, font=("TkDefaultFont", 12, "bold")).pack(fill=tk.X, pady=(0, 5))
        
        # Original value
        ttk.Label(self.right_frame, text="Original Value:").pack(anchor=tk.W)
        self.original_text = scrolledtext.ScrolledText(self.right_frame, height=6, wrap=tk.WORD)
        self.original_text.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # Expanded value
        ttk.Label(self.right_frame, text="Expanded Logic:").pack(anchor=tk.W)
        self.expanded_text = scrolledtext.ScrolledText(self.right_frame, height=15, wrap=tk.WORD)
        self.expanded_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # References
        ttk.Label(self.right_frame, text="Referenced By:").pack(anchor=tk.W)
        self.references_text = scrolledtext.ScrolledText(self.right_frame, height=6, wrap=tk.WORD)
        self.references_text.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Status bar
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(5, 0))
        
    def _browse_directory(self):
        directory = filedialog.askdirectory(title="Select SEL Settings Directory")
        if directory:
            self.dir_var.set(directory)
    
    def _load_settings(self):
        directory = self.dir_var.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        self.status_var.set("Loading settings files...")
        self.root.update_idletasks()
        
        self.decoder = SELLogicDecoder()
        if self.decoder.parse_directory(directory):
            self.current_dir = directory
            self._populate_settings_list()
            self._populate_categories()
            self.status_var.set(f"Loaded settings from {directory}")
        else:
            self.status_var.set(f"No valid settings files found in {directory}")
            messagebox.showwarning("Warning", "No valid SEL settings files found in the selected directory")
    
    def _populate_settings_list(self):
        self.settings_list.delete(*self.settings_list.get_children())
        
        all_settings = self.decoder.get_all_settings()
        for name, value in all_settings.items():
            # Determine type
            if name in self.decoder.logic_bits:
                setting_type = "Logic"
            else:
                setting_type = "Setting"
                
            # Add prefix based on common naming patterns
            if name.startswith("LT"):
                prefix = "LT"
            elif name.startswith("SV"):
                prefix = "SV"
            elif name.startswith("OUT"):
                prefix = "OUT"
            elif name.startswith("TR"):
                prefix = "TR"
            elif name.startswith("CL"):
                prefix = "CL"
            elif name.startswith("RB"):
                prefix = "RB"
            elif name.startswith("E"):
                prefix = "E"
            elif name.startswith("SET"):
                prefix = "SET"
            elif name.startswith("RST"):
                prefix = "RST"
            else:
                prefix = name[:2] if len(name) > 2 else ""
                
            self.settings_list.insert("", tk.END, iid=name, text=name, values=(setting_type,), tags=(prefix,))
        
        self.status_var.set(f"Loaded {len(all_settings)} settings")
    
    def _populate_categories(self):
        """Populate the category dropdown with prefixes found in settings names."""
        prefixes = set()
        for name in self.decoder.get_all_settings().keys():
            # Extract prefix (usually first 2-3 chars)
            if name.startswith("LT") or name.startswith("SV") or name.startswith("OUT") or name.startswith("TR"):
                prefix = name[:2]
            else:
                prefix = name[:2] if len(name) > 2 else name
            prefixes.add(prefix)
        
        categories = ["All"] + sorted(list(prefixes))
        self.category_dropdown['values'] = categories
    
    def _on_setting_selected(self, event):
        selected_items = self.settings_list.selection()
        if not selected_items:
            return
        
        self.current_equation = selected_items[0]
        self._show_equation_details(self.current_equation)
    
    def _show_equation_details(self, equation_name):
        result = self.decoder.decode_equation(equation_name)
        
        if 'error' in result:
            self.setting_name_var.set(f"{equation_name} - {result['error']}")
            self.original_text.delete(1.0, tk.END)
            self.expanded_text.delete(1.0, tk.END)
            return
        
        self.setting_name_var.set(equation_name)
        
        # Show original value
        self.original_text.delete(1.0, tk.END)
        self.original_text.insert(tk.END, result['original'])
        
        # Show expanded value
        self.expanded_text.delete(1.0, tk.END)
        self.expanded_text.insert(tk.END, result['expanded'])
        
        # Find references (other settings that reference this one)
        self._show_references(equation_name)
    
    def _show_references(self, equation_name):
        """Find and display settings that reference the current equation."""
        references = []
        for name, value in self.decoder.get_all_settings().items():
            if equation_name in str(value):
                references.append(name)
        
        self.references_text.delete(1.0, tk.END)
        if references:
            self.references_text.insert(tk.END, ", ".join(references))
        else:
            self.references_text.insert(tk.END, "No references found")
    
    def _apply_filter(self):
        filter_type = self.filter_var.get()
        category = self.category_var.get()
        
        # Show all items first
        for item in self.settings_list.get_children():
            self.settings_list.item(item, open=True)
            self.settings_list.detach(item)
        
        # Apply type filter
        all_items = []
        for name, value in self.decoder.get_all_settings().items():
            if filter_type == "All":
                all_items.append(name)
            elif filter_type == "Logic" and name in self.decoder.logic_bits:
                all_items.append(name)
            elif filter_type == "Settings" and name not in self.decoder.logic_bits:
                all_items.append(name)
        
        # Apply category filter
        for item in all_items:
            if category == "All":
                self.settings_list.reattach(item, "", tk.END)
            elif item.startswith(category):
                self.settings_list.reattach(item, "", tk.END)
        
        self.status_var.set(f"Filter applied: {filter_type}, Category: {category}")
    
    def _on_search(self, *args):
        search_term = self.search_var.get().strip().upper()
        if not search_term:
            self._apply_filter()  # Reset to current filter
            return
        
        # Hide all items
        for item in self.settings_list.get_children():
            self.settings_list.detach(item)
        
        # Search in both names and values
        results = self.decoder.search_settings(search_term)
        
        # Show matching items
        for name in results:
            self.settings_list.reattach(name, "", tk.END)
        
        self.status_var.set(f"Search results for '{search_term}': {len(results)} matches")
    
    def _clear_search(self):
        self.search_var.set("")
        self._apply_filter()  # Reset to current filter

if __name__ == "__main__":
    root = tk.Tk()
    app = SELLogicBrowserGUI(root)
    root.mainloop()