import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
import pandas as pd
from datetime import datetime
from collections import deque
import json
import re

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x400")
        self.root.config(bg="#FFFFFF")

        # Create a main frame
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.pack(fill="both", expand=True)

        # Create a logo label
        self.logo_label = tk.Label(self.main_frame, text="Login", font=("Open Sans", 24, "bold"), bg="#FFFFFF", fg="#000000")
        self.logo_label.pack(pady=20)

        # Create a username entry field
        self.username_label = tk.Label(self.main_frame, text="Username/Gmail:", font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.main_frame, font=("Open Sans", 16), width=20, bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.username_entry.pack()

        # Create a password entry field
        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.password_label.pack()
        self.password_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.password_frame.pack()
        self.password_entry = tk.Entry(self.password_frame, font=("Open Sans", 16), width=18, show="*", bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.password_entry.pack(side=tk.LEFT)
        self.eye_button = tk.Button(self.password_frame, text="", command=self.show_password, font=("Open Sans", 16), bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.eye_button.config(text=u"\U0001F441")
        self.eye_button.pack(side=tk.LEFT)

        # Create a login button
        self.login_button = tk.Button(self.main_frame, text="Login", command=self.login, font=("Open Sans", 16, "bold"), bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.login_button.pack(pady=20)

        # Create a register button
        self.register_button = tk.Button(self.main_frame, text="Register", command=self.register, font=("Open Sans", 16, "bold"), bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.register_button.pack()

        self.show_password_status = False

    def show_password(self):
        if not self.show_password_status:
            self.password_entry.config(show="")
            self.show_password_status = True
        else:
            self.password_entry.config(show="*")
            self.show_password_status = False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            with open("users.json", "r") as file:
                try:
                    users = json.load(file)
                except json.JSONDecodeError:
                    users = {}
        except FileNotFoundError:
            users = {}

        if not isinstance(users, dict):
            users = {}

        if username in users:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == users[username]["password"]:
                self.root.destroy()
                # Create a new window after login
                main_root = tk.Tk()
                app = OSRMTApp(main_root)
                main_root.mainloop()
                return
        elif username in [user["gmail"] for user in users.values()]:
            for stored_username, stored_user in users.items():
                if username == stored_user["gmail"]:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if hashed_password == stored_user["password"]:
                        self.root.destroy()
                        # Create a new window after login
                        main_root = tk.Tk()
                        app = OSRMTApp(main_root)
                        main_root.mainloop()
                        return
        messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        self.root.destroy()
        self.register_root = tk.Tk()
        self.register_app = RegisterApp(self.register_root)
        self.register_root.mainloop()

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Register Page")
        self.root.geometry("500x530")
        self.root.config(bg="#FFFFFF")

        # Create a main frame
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.pack(fill="both", expand=True)

        # Create a logo label
        self.logo_label = tk.Label(self.main_frame, text="Register", font=("Open Sans", 24, "bold"), bg="#FFFFFF", fg="#000000")
        self.logo_label.pack(pady=20)

        # Create a username entry field
        self.username_label = tk.Label(self.main_frame, text="Username:", font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.main_frame, font=("Open Sans", 16), width=20, bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.username_entry.pack()

        # Create a Gmail entry field
        self.gmail_label = tk.Label(self.main_frame, text="Gmail:", font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.gmail_label.pack()
        self.gmail_entry = tk.Entry(self.main_frame, font=("Open Sans", 16), width=20, bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.gmail_entry.pack()

        # Create a password entry field
        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.password_label.pack()
        self.password_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.password_frame.pack()
        self.password_entry = tk.Entry(self.password_frame, font=("Open Sans", 16), width=18, show="*", bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.password_entry.pack(side=tk.LEFT)
        self.eye_button = tk.Button(self.password_frame, text="", command=self.show_password, font=("Open Sans", 16), bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.eye_button.config(text=u"\U0001F441")
        self.eye_button.pack(side=tk.LEFT)

        # Create a confirm password entry field
        self.confirm_password_label = tk.Label(self.main_frame, text="Confirm Password:", font=("Open Sans", 16), bg="#FFFFFF", fg="#000000")
        self.confirm_password_label.pack()
        self.confirm_password_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        self.confirm_password_frame.pack()
        self.confirm_password_entry = tk.Entry(self.confirm_password_frame, font=("Open Sans", 16), width=18, show="*", bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.confirm_password_entry.pack(side=tk.LEFT)
        self.confirm_eye_button = tk.Button(self.confirm_password_frame, text="", command=self.show_confirm_password, font=("Open Sans", 16), bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.confirm_eye_button.config(text=u"\U0001F441")
        self.confirm_eye_button.pack(side=tk.LEFT)

        # Create a register button
        self.register_button = tk.Button(self.main_frame, text="Register", command=self.check_password, font=("Open Sans", 16, "bold"), bg="#FFFFFF", fg="#000000", highlightbackground="#000000", highlightthickness=1)
        self.register_button.pack(pady=20)

        self.show_password_status = False
        self.show_confirm_password_status = False

    def show_password(self):
        if not self.show_password_status:
            self.password_entry.config(show="")
            self.show_password_status = True
        else:
            self.password_entry.config(show="*")
            self.show_password_status = False

    def show_confirm_password(self):
        if not self.show_confirm_password_status:
            self.confirm_password_entry.config(show="")
            self.show_confirm_password_status = True
        else:
            self.confirm_password_entry.config(show="*")
            self.show_confirm_password_status = False

    def check_password(self):
        username = self.username_entry.get()
        gmail = self.gmail_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        registered = False

        # Check if Gmail is valid
        if not self.is_valid_gmail(gmail):
            messagebox.showerror("Error", "Invalid Gmail")
        # Check if password starts with a capital letter
        elif not password[0].isupper():
            messagebox.showerror("Error", "Password should start with a capital letter")
        # Check if password has a minimum of 8 characters
        elif len(password) < 8:
            messagebox.showerror("Error", "Password should have a minimum of 8 characters")
        # Check if password has at least one special character
        elif not any(not char.isalnum() for char in password):
            messagebox.showerror("Error", "Password should have at least one special character")
        # Check if password has at least one digit
        elif not any(char.isdigit() for char in password):
            messagebox.showerror("Error", "Password should have at least one digit")
        # Check if password has at least one alphabet
        elif not any(char.isalpha() for char in password):
            messagebox.showerror("Error", "Password should have at least one alphabet")
        # Check if password and confirm password match
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        # Check if the username already exists
        else:
            try:
                with open("users.json", "r") as file:
                    try:
                        users = json.load(file)
                    except json.JSONDecodeError:
                        users = {}
            except FileNotFoundError:
                users = {}

            if not isinstance(users, dict):
                users = {}

            if username in users:
                messagebox.showerror("Error", "Username already exists")
            elif gmail in [user["gmail"] for user in users.values()]:
                messagebox.showerror("Error", "Gmail already exists")
            else:
                registered = True

            if registered:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                users[username] = {
                    "username": username,
                    "gmail": gmail,
                    "password": hashed_password
                }
                with open("users.json", "w") as file:
                    json.dump(users, file)

                self.root.destroy()
                root = tk.Tk()
                app = LoginApp(root)
                root.mainloop()

    def is_valid_gmail(self, gmail):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, gmail):
            return True
        return False

class OSRMTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OSRMT")  # Updated window title
        self.root.geometry("1920x1080")

        # Add font scaling variable
        self.font_size = 14  # Default font size
        self.default_font = Font(family="Arial", size=self.font_size)

        # Create menu bar
        self.menu_bar = tk.Menu(root)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_product)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Validate", command=lambda: self.dummy_action("Validation Tool"))
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

        # Admin menu
        admin_menu = tk.Menu(self.menu_bar, tearoff=0)
        admin_menu.add_command(label="Users", command=lambda: self.dummy_action("User Management"))
        admin_menu.add_command(label="Permissions", command=lambda: self.dummy_action("Permission Settings"))
        self.menu_bar.add_cascade(label="Admin", menu=admin_menu)

        # System menu
        system_menu = tk.Menu(self.menu_bar, tearoff=0)
        system_menu.add_command(label="Settings", command=lambda: self.dummy_action("System Settings"))
        self.menu_bar.add_cascade(label="System", menu=system_menu)

        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=self.menu_bar)

        # Create toolbar
        self.toolbar = ttk.Frame(root, relief=tk.RAISED, borderwidth=1)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Toolbar buttons
        self.new_button = ttk.Button(self.toolbar, text="New", width=9, command=self.new_item)
        self.new_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.open_button = ttk.Button(self.toolbar, text="Open", width=9, command=self.open_product)
        self.open_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_button = ttk.Button(self.toolbar, text="Save", width=9, command=lambda: self.export_to_excel(self.current_view))
        self.save_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.print_button = ttk.Button(self.toolbar, text="Print", width=9, command=lambda: self.dummy_action("Print"))
        self.print_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.delete_button = ttk.Button(self.toolbar, text="Delete", width=9, command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.zoom_in_button = ttk.Button(self.toolbar, text="Zoom In", width=9, command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.zoom_out_button = ttk.Button(self.toolbar, text="Zoom Out", width=11, command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.about_button = ttk.Button(self.toolbar, text="About", width=9, command=self.show_about)
        self.about_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Main content area with split pane
        self.paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel (sidebar tree)
        self.left_frame = ttk.Frame(self.paned_window, width=200, relief=tk.SUNKEN)
        self.paned_window.add(self.left_frame, weight=1)

        # Create treeview for left sidebar
        self.tree = ttk.Treeview(self.left_frame, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Right panel (content display area)
        self.right_frame = ttk.Frame(self.paned_window, relief=tk.SUNKEN)
        self.paned_window.add(self.right_frame, weight=4)

        # Status bar
        self.status_bar = ttk.Label(root, text="Please select an artifact", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize data structures
        self.current_view = None
        self.data_tables = {
            "feature": [],
            "requirement": [],
            "design": [],
            "implementation": [],
            "testcase": []
        }

        self.undo_stack = deque()
        self.redo_stack = deque()

        # Bind tree selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Initialize the sidebar
        self.initialize_sidebar()

    def initialize_sidebar(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Project root
        project = self.tree.insert("", "end", text="Project", open=True, tags=("project",))
        self.tree.tag_configure("project", foreground="blue")

        # Feature
        feature_folder = self.tree.insert(project, "end", text="Feature", open=True, tags=("folder",))
        self.tree.insert(feature_folder, "end", text="Project Feature", tags=("feature",))

        # Requirement
        req_folder = self.tree.insert(project, "end", text="Requirement", open=True, tags=("folder",))
        self.tree.insert(req_folder, "end", text="Project Requirement", tags=("requirement",))

        # Design
        design_folder = self.tree.insert(project, "end", text="Design", open=True, tags=("folder",))
        self.tree.insert(design_folder, "end", text="Project Design", tags=("design",))

        # Implementation
        impl_folder = self.tree.insert(project, "end", text="Implementation", open=True, tags=("folder",))
        self.tree.insert(impl_folder , "end", text="Project Implementation", tags=("implementation",))

        # TestCase
        test_folder = self.tree.insert(project, "end", text="TestCase", open=True, tags=("folder",))
        self.tree.insert(test_folder, "end", text="Project TestCase", tags=("testcase",))

        # Configure tags
        self.tree.tag_configure("folder", foreground="black")
        self.tree.tag_configure("feature", foreground="black")
        self.tree.tag_configure("requirement", foreground="black")
        self.tree.tag_configure("design", foreground="black")
        self.tree.tag_configure("implementation", foreground="black")
        self.tree.tag_configure("testcase", foreground="black")

    def zoom_in(self):
        if self.font_size < 16:  # Set a reasonable upper limit
            self.font_size += 1
            self.update_fonts()

    def zoom_out(self):
        if self.font_size > 6:  # Set a reasonable lower limit
            self.font_size -= 1
            self.update_fonts()

    def update_fonts(self):
        # Update application fonts
        default_font = Font(family="Arial", size=self.font_size)
        
        # Update tree font
        self.tree.configure(style="Custom.Treeview")
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", self.font_size))

        # Update status bar font
        self.status_bar.configure(font=("Arial", self.font_size))

        # If there's an active table in the right frame, update its font too
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                style.configure("Treeview", font=("Arial", self.font_size))
                style.configure("Treeview.Heading", font=("Arial", self.font_size, "bold"))
            elif isinstance(widget, ttk.Label) or isinstance(widget, ttk.Button):
                widget.configure(font=("Arial", self.font_size))

    def open_product(self):
        # Simulate opening a product
        filepath = filedialog.askopenfilename()
        messagebox.showinfo("Open Product", "Product loaded successfully")
        self.initialize_sidebar()
        self.status_bar.config(text="Product loaded. Select an item from the tree.")

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        item_text = self.tree.item(item, "text")
        parent_id = self.tree.parent(item)

        if parent_id:
            parent_text = self.tree.item(parent_id, "text").lower()
            self.status_bar.config(text=f"Selected: {parent_text} - {item_text}")

            # Clear right frame
            for widget in self.right_frame.winfo_children():
                widget.destroy()

            if parent_text in self.data_tables:
                self.current_view = parent_text
                self.display_data_table(parent_text)
            else:
                self.display_message("Select a specific item to view details")

    def display_data_table(self, table_type):
        # Create frame for controls
        control_frame = ttk.Frame(self.right_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Add new item button
        add_button = ttk.Button(control_frame, text="Add New",
                                command=lambda: self.show_entry_form(table_type))
        add_button.pack(side=tk.LEFT, padx=5)

        # Edit button
        #edit_button = ttk.Button(control_frame, text="Edit", command=lambda: self.edit_selected_item(None, self.right_frame.winfo_children()[0], table_type))
        #edit_button.pack(side=tk.LEFT, padx=5)

        # Export button
        export_button = ttk.Button(control_frame, text="Export to Excel", command=lambda: self.export_to_excel(table_type))
        export_button.pack(side=tk.LEFT, padx=5)

        # Create table frame
        table_frame = ttk.Frame(self.right_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create table headers based on type
        headers = self.get_headers_for_type(table_type)

        # Create the treeview for data display
        columns = [f"col{i}" for i in range(len(headers))]
        table = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Configure the headers
        for i, header in enumerate(headers):
            table.heading(f"col{i}", text=header)
            table.column(f"col{i}", width=100)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=y_scroll.set)

        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
        table.configure(xscrollcommand=x_scroll.set)

        # Pack the scrollbars and table
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate with existing data
        for row_data in self.data_tables[table_type]:
            values = [row_data.get(h, "") for h in headers]
            table.insert("", "end", values=values)

        # Double-click to edit
        table.bind("<Double-1>", lambda event: self.edit_selected_item(event, table, table_type))

    def get_headers_for_type(self, table_type):
        # Return appropriate headers for each type
        common = ["ID", "Name", "Description", "Created", "Modified", "Status"]

        if table_type == "feature":
            return common + ["Priority", "Version"]
        elif table_type == "requirement":
            return common + ["Priority", "Type", "Source", "Rationale"]
        elif table_type == "design":
            return common + ["Component", "Complexity", "Dependencies"]
        elif table_type == "implementation":
            return common + ["Language", "LOC", "Complexity", "Developer"]
        elif table_type == "testcase":
            return common + ["Type", "Preconditions", "Expected Result", "Actual Result"]
        else:
            return common

    def show_entry_form(self, table_type):
        # Create a dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add New {table_type.capitalize()}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create a frame for the form
        form_frame = ttk.Frame(dialog, padding=5)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Get fields for this type
        headers = self.get_headers_for_type(table_type)
        entry_widgets = {}

        # Create entry fields
        for i, field in enumerate(headers):
            ttk.Label(form_frame, text=field + ":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)

            if field == "Description":
                # Multiline text for description
                text_widget = tk.Text(form_frame, height=4, width=40)
                text_widget.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = text_widget
            elif field == "Status":
                # Dropdown for status
                status_combo = ttk.Combobox(form_frame, values=["New", "In Progress", "Completed", "On Hold"])
                status_combo.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                status_combo.current(0)
                entry_widgets[field] = status_combo
            elif field == "Priority":
                # Dropdown for priority
                priority_combo = ttk.Combobox(form_frame, values=["Low", "Medium", "High", "Critical"])
                priority_combo.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                priority_combo.current(1)
                entry_widgets[field] = priority_combo
            elif field in ["Created", "Modified"]:
                # Date fields - pre-filled
                date_entry = ttk.Entry(form_frame, width=30)
                date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
                date_entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = date_entry
            elif field == "ID":
                # ID - auto generated
                id_entry = ttk.Entry(form_frame, width=30)
                id_entry.insert(0, f"{table_type[:3].upper()}-{len(self.data_tables[table_type]) + 1:03d}")
                id_entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = id_entry
            else:
                # Standard text entry for other fields
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = entry

        # Save button
        def save_entry():
            # Collect data from form
            data = {}
            for field, widget in entry_widgets.items():
                if isinstance(widget, tk.Text):
                    data[field] = widget.get("1.0", tk.END).strip()
                else:
                    data[field] = widget.get()

            # Add to data table
            self.data_tables[table_type].append(data)

            # Record the undo action
            self.undo_stack.append(("add", table_type, data))

            # Update tree view if needed
            if table_type == "feature":
                feature_folder = None
                for item in self.tree.get_children():
                    for child in self.tree.get_children(item):
                        if self.tree.item(child, "text") == "Feature":
                            feature_folder = item
                            break

                if feature_folder:
                    self.tree.insert(feature_folder, "end", text=data["Name"], tags=(table_type,))

            # Close dialog
            dialog.destroy()

            # Refresh the display
            self.display_data_table(table_type)

        save_button = ttk.Button(form_frame, text="Save", command=save_entry)
        save_button.grid(row=len(headers) + 1, column=1, sticky=tk.E, padx=5, pady=10)

        # Cancel button
        cancel_button = ttk.Button(form_frame, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=len(headers) + 1, column=0, sticky=tk.W, padx=5, pady=10)

    # New method to update item on the data table; used for edit functionality
    def update_data_table(self, table_type, index, updated_data):
        old_data = self.data_tables[table_type][index].copy()  # Keep a copy for undo purposes
        self.data_tables[table_type][index] = updated_data
        self.undo_stack.append(("edit", table_type, index, old_data))  # Record the edit action

    def edit_selected_item(self, event, table, table_type):
        # Get selected item
        selection = table.selection()
        if not selection:
            return

        # Get the item data
        item = selection[0]
        item_values = table.item(item, "values")

        # Get headers
        headers = self.get_headers_for_type(table_type)

        # Find the corresponding data entry
        item_id = item_values[0]  # Assuming ID is first column
        item_index = None
        for i, entry in enumerate(self.data_tables[table_type]):
            if entry["ID"] == item_id:
                item_index = i
                break

        if item_index is None:
            return

        # Create edit dialog
        self.show_edit_form(table_type, item_index)

    def show_edit_form(self, table_type, item_index):
        # Get the data to edit
        data = self.data_tables[table_type][item_index]

        # Create a dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit {table_type.capitalize()}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create a frame for the form
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Get fields for this type
        headers = self.get_headers_for_type(table_type)
        entry_widgets = {}

        # Create entry fields with existing data
        for i, field in enumerate(headers):
            ttk.Label(form_frame, text=field + ":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)

            current_value = data.get(field, "")

            if field == "Description":
                # Multiline text for description
                text_widget = tk.Text(form_frame, height=4, width=40)
                text_widget.insert("1.0", current_value)
                text_widget.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = text_widget
            elif field == "Status":
                # Dropdown for status
                status_combo = ttk.Combobox(form_frame, values=["New", "In Progress", "Completed", "On Hold"])
                status_combo.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if current_value in ["New", "In Progress", "Completed", "On Hold"]:
                    status_combo.set(current_value)
                else:
                    status_combo.current(0)
                entry_widgets[field] = status_combo
            elif field == "Priority":
                # Dropdown for priority
                priority_combo = ttk.Combobox(form_frame, values=["Low", "Medium", "High", "Critical"])
                priority_combo.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if current_value in ["Low", "Medium", "High", "Critical"]:
                    priority_combo.set(current_value)
                else:
                    priority_combo.current(1)
                entry_widgets[field] = priority_combo
            elif field == "Modified":
                # Modified date - updated to current
                date_entry = ttk.Entry(form_frame, width=30)
                date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
                date_entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = date_entry
            else:
                # Standard text entry for other fields
                entry = ttk.Entry(form_frame, width=30)
                entry.insert(0, current_value)
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                entry_widgets[field] = entry

        # Update button
        def update_entry():
            # Collect data from form
            updated_data = {}
            for field, widget in entry_widgets.items():
                if isinstance(widget, tk.Text):
                    updated_data[field] = widget.get("1.0", tk.END).strip()
                else:
                    updated_data[field] = widget.get()

            # Update data table
            self.update_data_table(table_type, item_index, updated_data)

            # Close dialog
            dialog.destroy()

            # Refresh the display
            self.display_data_table(table_type)

        update_button = ttk.Button(form_frame, text="Update", command=update_entry)
        update_button.grid(row=len(headers) + 1, column=1, sticky=tk.E, padx=5, pady=10)

        # Cancel button
        cancel_button = ttk.Button(form_frame, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=len(headers) + 1, column=0, sticky=tk.W, padx=5, pady=10)

    def export_to_excel(self, table_type):
        # Check if there's data to export
        if not self.data_tables[table_type]:
            messagebox.showinfo("Export", "No data to export")
            return

        try:
            # Ask for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Export to Excel"
            )

            if not file_path:
                return  # User cancelled

            # Convert to DataFrame
            df = pd.DataFrame(self.data_tables[table_type])

            # Export to Excel
            df.to_excel(file_path, index=False)

            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {str(e)}")

    def new_item(self):
        # Determine what type of item to create based on selection
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showinfo("New Item", "Please select a category first")
            return

        item = selected_items[0]
        item_text = self.tree.item(item, "text").lower()

        # Check if it's a folder or parent
        if item_text in self.data_tables:
            self.show_entry_form(item_text)
        else:
            parent_id = self.tree.parent(item)
            if parent_id:
                parent_text = self.tree.item(parent_id, "text").lower()
                if parent_text in self.data_tables:
                    self.show_entry_form(parent_text)

    def delete_selected(self):
        # Get selected item
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        item_text = self.tree.item(item, "text")

        # Don't allow deleting root or main folders
        parent_id = self.tree.parent(item)
        if not parent_id or self.tree.item(parent_id, "text") == "Project":
            messagebox.showinfo("Delete", "Cannot delete root or main category folders")
            return

        # Get the type of the item to delete
        item_type = self.tree.tag_has("feature", item) and "feature" or \
                    self.tree.tag_has("requirement", item) and "requirement" or \
                    self.tree.tag_has("design", item) and "design" or \
                    self.tree.tag_has("implementation", item) and "implementation" or \
                    self.tree.tag_has("testcase", item) and "testcase"

        if not item_type:
            messagebox.showerror("Error", "Cannot determine item type for deletion.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_text}'?")
        if not confirm:
            return

        # Record the undo action
        deleted_item = self.data_tables[item_type].pop(self.get_item_index_in_data(item_type, item_text))
        self.undo_stack.append(("delete", item_type, deleted_item))

        # Delete from tree
        self.tree.delete(item)

        # If in current view, refresh
        if self.current_view:
            self.display_data_table(self.current_view)

    def get_item_index_in_data(self, item_type, item_name):
        for i, item in enumerate(self.data_tables[item_type]):
            if item["Name"] == item_name:
                return i
        return -1

    def display_message(self, message):
        # Display a message in the right panel
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        message_label = ttk.Label(
            self.right_frame,
            text=message,
            font=("Arial", 14),
            foreground="blue"
        )
        message_label.place(relx=0.5, rely=0.5, anchor="center")

    def undo(self):
        if not self.undo_stack:
            messagebox.showinfo("Undo", "No actions to undo.")
            return

        action = self.undo_stack.pop()
        
        action_type = action[0]
        if action_type == "add":
            table_type = action[1]
            data = action[2]
            self.data_tables[table_type].remove(data)  # Remove the last added instance from the table
            self.redo_stack.append(action)  # Push action to redo stack

        elif action_type == "edit":
            table_type = action[1]
            index = action[2]
            previous_data = action[3]
            self.data_tables[table_type][index] = previous_data  # Revert to previous data
            self.redo_stack.append(action)  # Push action to redo stack

        elif action_type == "delete":
            table_type = action[1]
            deleted_item = action[2]
            self.data_tables[table_type].append(deleted_item)  # Re-add the deleted item
            self.redo_stack.append(action)  # Push action to redo stack

        # Refresh display after undo
        if self.current_view:
            self.display_data_table(self.current_view)

    def redo(self):
        if not self.redo_stack:
            messagebox.showinfo("Redo", "No actions to redo.")
            return

        action = self.redo_stack.pop()

        action_type = action[0]
        if action_type == "add":
            table_type = action[1]
            data = action[2]
            self.data_tables[table_type].append(data)  # Re-add the previously undone instance
            self.undo_stack.append(action)  # Push action back to undo stack

        elif action_type == "edit":
            table_type = action[1]
            index = action[2]
            current_data = self.data_tables[table_type][index]
            self.data_tables[table_type][index] = action[3]  # Re-apply the edit
            self.undo_stack.append(action)  # Push action back to undo stack

        elif action_type == "delete":
            table_type = action[1]
            deleted_item = action[2]
            self.data_tables[table_type].remove(deleted_item)  # Remove the re-added item
            self.undo_stack.append(action)  # Push action back to undo stack

        # Refresh display after redo
        if self.current_view:
            self.display_data_table(self.current_view)

    def dummy_action(self, action_name):
        messagebox.showinfo("Action", f"{action_name} clicked - Feature not implemented yet")

    def show_about(self):
        about_text = "OSRMT \nVersion 1.0\nOpen Source Requirements Management Tool"
        messagebox.showinfo("About", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

