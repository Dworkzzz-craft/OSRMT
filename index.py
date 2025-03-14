import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
import pandas as pd
from datetime import datetime
from collections import deque
import mysql.connector
import re
import tempfile
import xlsxwriter
import openpyxl
import os
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300")
        self.root.config(bg="#FFFFFF")

        # Set the window icon using PNG
        self.set_app_icon("logo.png")  # Ensure "logo.png" is in the same directory
        
        font_style = ("Arial", 14)  # Increased font size

        self.username_label = tk.Label(self.root, text="Username:", font=font_style)
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=font_style, width=25)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:", font=font_style)
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=font_style, width=25)
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", font=font_style, command=self.login, padx=10)
        self.login_button.pack(pady=20)

    def set_app_icon(self, image_path):
        """Sets a PNG image as the application icon."""
        try:
            img = Image.open(image_path)
            img = img.resize((32, 32))  # Resize if necessary
            self.icon_img = ImageTk.PhotoImage(img)

            # Set the icon in the window title bar
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_img)

        except Exception as e:
            print(f"Error loading icon: {e}")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='Employee@123', database='user_management')
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            role = user.get("role")
            if  role == "admin":
                self.open_admin_panel(role) # Redirect to admin panel
            else:
                self.open_user_panel(role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_admin_panel(self,role):
        self.root.destroy()
        root = tk.Tk()
        AdminPanel(root,role)
        root.mainloop()

    def open_user_panel(self,role):
        self.root.destroy()
        root = tk.Tk()
        OSRMTApp(root,role)
        root.mainloop()

class AdminPanel:
    def __init__(self, root, role):
        self.root = root
        self.role = role  # Store the role
        self.root.title("Admin Panel")
        self.root.geometry("400x400")
        
        # Set the window icon using PNG
        self.set_app_icon("logo.png")  # Ensure "logo.png" is in the same directory

        font_style = ("Arial", 14)  # Increased font size

        if self.role == "admin":  # Ensure only admin sees this button
            self.register_button = tk.Button(self.root, text="Register New User", font=font_style,  command=self.register_user)
            self.register_button.pack(pady=20)

        self.osrmt_button = tk.Button(self.root, text="Go to OSRMTApp", font=font_style,  command=self.open_osrmt)
        self.osrmt_button.pack(pady=20)

    def set_app_icon(self, image_path):
        """Sets a PNG image as the application icon."""
        try:
            img = Image.open(image_path)
            img = img.resize((32, 32))  # Resize if necessary
            self.icon_img = ImageTk.PhotoImage(img)

            # Set the icon in the window title bar
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_img)

        except Exception as e:
            print(f"Error loading icon: {e}")
    
    def register_user(self):
        RegisterApp(tk.Toplevel(self.root))

    def open_osrmt(self):
        self.root.destroy()
        root = tk.Tk()
        OSRMTApp(root,self.role) # Ensure admin role is passed
        root.mainloop()

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Register User")
        self.root.geometry("400x400")
        
        # Set the window icon using PNG
        self.set_app_icon("logo.png")  # Ensure "logo.png" is in the same directory

        font_style = ("Arial", 14)

        self.username_label = tk.Label(self.root, text="Username:", font=font_style)
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=font_style, width=25)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:", font=font_style)
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=font_style, width=25)
        self.password_entry.pack(pady=5)

        self.role_label = tk.Label(self.root, text="Role:", font=font_style)
        self.role_label.pack(pady=5)

        self.role_label = ttk.Combobox(self.root, values=["user", "admin"], state="readonly")
        self.role_label.pack(pady=5)
        self.role_label.current(0)  # Default selection
        self.role_entry = self.role_label  # Ensure role_entry refers to the combobox

        self.register_button = tk.Button(self.root, text="Register", font=font_style, command=self.register)
        self.register_button.pack(pady=20)

    def set_app_icon(self, image_path):
        """Sets a PNG image as the application icon."""
        try:
            img = Image.open(image_path)
            img = img.resize((32, 32))  # Resize if necessary
            self.icon_img = ImageTk.PhotoImage(img)

            # Set the icon in the window title bar
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_img)

        except Exception as e:
            print(f"Error loading icon: {e}")
            
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        
         # Validate username
        if not re.match(r"^[a-zA-Z0-9_]{5,20}$", username):
            messagebox.showerror("Error", "Please enter username.")
            return
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='Employee@123', database='user_management')
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, hashed_password, role))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()


class OSRMTApp:
    def __init__(self, root, role):
        self.root = root
        self.role = role  # Store user role
        self.root.title("OSRMT")
        self.root.geometry("1920x1080")
        self.font_size = 14  # Base font size for non-table widgets
        
        # Set the window icon using PNG
        self.set_app_icon("logo.png")  # Ensure "logo.png" is in the same directory
        
        # Connect to the database
        self.conn = self.setup_database()
        if not self.conn:
            messagebox.showerror("Error", "Failed to connect to the database.")
            self.root.destroy()
            return
        
        # In-memory data storage for each table
        self.data_tables = {
            "feature": [],
            "requirement": [],
            "design": [],
            "implementation": [],
            "testcase": []
        }

        # Load all tables initially
        self.load_data_from_db()

        self.undo_stack = deque()
        self.redo_stack = deque()

        self.current_view = None  # Name of the currently selected table
        self.current_tableview = None  # Reference to the right-side Treeview

        # Build UI components
        self.create_menu_bar()
        self.create_toolbar()  # Toolbar now does NOT include the Open button
        self.create_main_panes()

        # Configure a custom style for the Treeview to show borders and use smaller font
        self.configure_treeview_style()
     
    def set_app_icon(self, image_path):
        """Sets a PNG image as the application icon."""
        try:
            img = Image.open(image_path)
            img = img.resize((32, 32))  # Resize if necessary
            self.icon_img = ImageTk.PhotoImage(img)

            # Set the icon in the window title bar
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_img)

        except Exception as e:
            print(f"Error loading icon: {e}")
            
    def configure_treeview_style(self):
        style = ttk.Style()
        # Use the default theme so we can adjust elements
        style.theme_use("default")
        # Configure the custom Treeview style
        style.configure("Custom.Treeview",
                        background="white",
                        fieldbackground="white",
                        borderwidth=1,
                        font=("Arial", 10),
                        rowheight=25)
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        borderwidth=1,
                        relief="solid")
        # This layout adds borders for cells (if supported by theme)
        style.layout("Custom.Treeview", [
            ('Custom.Treeview.treearea', {'sticky': 'nswe'})
        ])

    def setup_database(self):
        """Establish MySQL connection."""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',          # Replace with your MySQL username
                password='Employee@123',  # Replace with your MySQL password
                database='user_management'
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return None

    def load_data_from_db(self):
        """Fetch the latest data from ALL tables into self.data_tables."""
        for table_name in ["feature", "requirement", "design", "implementation", "testcase"]:
            self.load_data_for_table(table_name)

    def load_data_for_table(self, table_type):
        """Load only the specified table_type from the DB."""
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM {table_type}")
            self.data_tables[table_type] = cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()

    def save_to_db(self, table_type, data, action="add", old_data=None):
        """Insert, update, or delete in the specified table while preventing duplicate IDs."""
        cursor = self.conn.cursor(dictionary=True)

        try:
            if action == "add":
                # Check if an entry with the same ID already exists
                check_query = f"SELECT id FROM {table_type} WHERE id = %s"
                cursor.execute(check_query, (data["id"],))
                existing_entry = cursor.fetchone()

                if existing_entry:
                    messagebox.showwarning("Duplicate Entry", f"An entry with ID {data['id']} already exists.")
                    return  # Stop execution to prevent duplicate insertion

                # Proceed with inserting a new entry
                columns = ", ".join(data.keys())
                placeholders = ", ".join(["%s"] * len(data))
                query = f"INSERT INTO {table_type} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, list(data.values()))

            elif action == "edit":
                set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
                query = f"UPDATE {table_type} SET {set_clause} WHERE id = %s"
                cursor.execute(query, list(data.values()) + [old_data["id"]])

            elif action == "delete":
                query = f"DELETE FROM {table_type} WHERE id = %s"
                cursor.execute(query, (data["id"],))

            self.conn.commit()
        
            if action == "add":
                messagebox.showinfo("Success", "Entry added successfully!")
    
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()


    def create_menu_bar(self):
        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_product)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Validate", command=lambda: self.dummy_action("Validation Tool"))
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

        admin_menu = tk.Menu(self.menu_bar, tearoff=0)
        admin_menu.add_command(label="Users", command=lambda: self.dummy_action("User Management"))
        admin_menu.add_command(label="Permissions", command=lambda: self.dummy_action("Permission Settings"))
        self.menu_bar.add_cascade(label="Admin", menu=admin_menu)

        system_menu = tk.Menu(self.menu_bar, tearoff=0)
        system_menu.add_command(label="Settings", command=lambda: self.dummy_action("System Settings"))
        self.menu_bar.add_cascade(label="System", menu=system_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=self.menu_bar)

    def create_toolbar(self):
        """Toolbar without the Open button."""
        self.toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.new_button = ttk.Button(self.toolbar, text="New", width=9, command=self.new_item)
        self.new_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Open button removed

        self.save_button = ttk.Button(self.toolbar, text="Save", width=9,
                                      command=lambda: self.export_to_excel(self.current_view))
        self.save_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.print_button = ttk.Button(self.toolbar, text="Print", width=9, command=self.print_table_as_excel)
        self.print_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.import_button = ttk.Button(self.toolbar, text="Import Excel", width=12, command=self.import_from_excel)
        self.import_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.about_button = ttk.Button(self.toolbar, text="About", width=9, command=self.show_about)
        self.about_button.pack(side=tk.LEFT, padx=2, pady=2)

    def create_main_panes(self):
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.left_frame = ttk.Frame(self.paned_window, width=200, relief=tk.SUNKEN)
        self.paned_window.add(self.left_frame, weight=1)

        self.tree = ttk.Treeview(self.left_frame, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.initialize_sidebar()

        self.right_frame = ttk.Frame(self.paned_window, relief=tk.SUNKEN)
        self.paned_window.add(self.right_frame, weight=4)

        self.status_bar = ttk.Label(self.root, text="Please select an artifact", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def initialize_sidebar(self):
        project = self.tree.insert("", "end", text="Project", open=True, tags=("project",))
        self.tree.tag_configure("project", foreground="blue")

        feature_folder = self.tree.insert(project, "end", text="Feature", open=True, tags=("folder",))
        self.tree.insert(feature_folder, "end", text="Project Feature", tags=("feature",))

        req_folder = self.tree.insert(project, "end", text="Requirement", open=True, tags=("folder",))
        self.tree.insert(req_folder, "end", text="Project Requirement", tags=("requirement",))

        design_folder = self.tree.insert(project, "end", text="Design", open=True, tags=("folder",))
        self.tree.insert(design_folder, "end", text="Project Design", tags=("design",))

        impl_folder = self.tree.insert(project, "end", text="Implementation", open=True, tags=("folder",))
        self.tree.insert(impl_folder, "end", text="Project Implementation", tags=("implementation",))

        test_folder = self.tree.insert(project, "end", text="TestCase", open=True, tags=("folder",))
        self.tree.insert(test_folder, "end", text="Project TestCase", tags=("testcase",))

        self.tree.tag_configure("folder", foreground="black")
        self.tree.tag_configure("feature", foreground="black")
        self.tree.tag_configure("requirement", foreground="black")
        self.tree.tag_configure("design", foreground="black")
        self.tree.tag_configure("implementation", foreground="black")
        self.tree.tag_configure("testcase", foreground="black")

    # The open_product method is still available via the File menu.
    def open_product(self):
        filepath = filedialog.askopenfilename()
        if filepath:
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
            for widget in self.right_frame.winfo_children():
                widget.destroy()
            if parent_text in self.data_tables:
                self.current_view = parent_text
                self.display_data_table(parent_text)
            else:
                self.display_message("Select a specific item to view details")

    def get_headers_for_type(self, table_type):
        # Adjust these to match your database columns exactly (all lowercase)
        common = ["id", "name", "description", "created", "modified", "status"]
        if table_type == "feature":
            return common + ["priority", "version"]
        elif table_type == "requirement":
            return common + ["priority", "type", "source", "rationale"]
        elif table_type == "design":
            return common + ["component", "complexity", "dependencies"]
        elif table_type == "implementation":
            return common + ["language", "loc", "complexity", "developer"]
        elif table_type == "testcase":
            return common + ["type", "preconditions", "expectedresult", "actualresult"]
        else:
            return common

    def display_data_table(self, table_type):
        # Clear any previous tableview reference
        self.current_tableview = None

        control_frame = ttk.Frame(self.right_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        add_button = ttk.Button(control_frame, text="Add New",
                                command=lambda: self.show_entry_form(table_type))
        add_button.pack(side=tk.LEFT, padx=5)

        export_button = ttk.Button(control_frame, text="Export to Excel",
                                   command=lambda: self.export_to_excel(table_type))
        export_button.pack(side=tk.LEFT, padx=5)

        fetch_button = ttk.Button(control_frame, text="Fetch",
                                  command=lambda: self.fetch_data(table_type))
        fetch_button.pack(side=tk.LEFT, padx=5)

        # Only show delete button if the user is an admin
        if self.role == "admin":
            delete_button = ttk.Button(control_frame, text="Delete Row",
                                        command=self.delete_selected)
            delete_button.pack(side=tk.LEFT, padx=5)

        # Create a table frame with a visible border.
        table_frame = ttk.Frame(self.right_frame, relief="solid", borderwidth=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        headers = self.get_headers_for_type(table_type)
        columns = [f"col{i}" for i in range(len(headers))]
        treeview = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended", style="Custom.Treeview")
        for i, header in enumerate(headers):
            treeview.heading(f"col{i}", text=header.capitalize())
            treeview.column(f"col{i}", width=120)
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=y_scroll.set)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=treeview.xview)
        treeview.configure(xscrollcommand=x_scroll.set)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate treeview rows
        for row_data in self.data_tables[table_type]:
            values = [row_data.get(h, "") for h in headers]
            treeview.insert("", "end", values=values)

        treeview.bind("<Double-1>", lambda event: self.edit_selected_item(event, treeview, table_type))
        self.current_tableview = treeview

    def fetch_data(self, table_type):
        self.load_data_for_table(table_type)
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.display_data_table(table_type)
        messagebox.showinfo("Fetch", f"Data for '{table_type}' has been refreshed from the database.")

    def show_entry_form(self, table_type):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add New {table_type.capitalize()}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding=5)
        form_frame.pack(fill=tk.BOTH, expand=True)

        headers = self.get_headers_for_type(table_type)
        entry_widgets = {}

        for i, field in enumerate(headers):
            ttk.Label(form_frame, text=field.capitalize() + ":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
        
            if field == "description":
                widget = tk.Text(form_frame, height=4, width=40)
            elif field == "status":
                widget = ttk.Combobox(form_frame, values=["New", "In Progress", "Completed", "On Hold"])
                widget.current(0)
            elif field == "priority":
                widget = ttk.Combobox(form_frame, values=["Low", "Medium", "High", "Critical"])
                widget.current(1)
            elif field in ["created", "modified"]:
                widget = ttk.Entry(form_frame, width=30)
                widget.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
            elif field == "id":
                widget = ttk.Entry(form_frame, width=30)
                widget.insert(0, f"{table_type[:3].upper()}-{len(self.data_tables[table_type]) + 1:03d}")  # Auto-generate an ID
            else:
                widget = ttk.Entry(form_frame, width=30)

            widget.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
            entry_widgets[field] = widget

        def validate_and_save():
            data = {}
            for field, widget in entry_widgets.items():
                if isinstance(widget, tk.Text):
                    data[field] = widget.get("1.0", tk.END).strip()
                else:
                    data[field] = widget.get().strip()

            # Ensure ID is not empty
            if not data.get("id"):
                messagebox.showerror("Error", "ID cannot be empty.")
                return
        
            # Ensure name field is not empty
            if not data.get("name"):
                messagebox.showerror("Error", "Name cannot be empty.")
                return

            # Check if ID already exists in the database
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(f"SELECT id FROM {table_type} WHERE id = %s", (data["id"],))
            existing_entry = cursor.fetchone()
            cursor.close()

            if existing_entry:
                messagebox.showwarning("Duplicate Entry", f"An entry with ID {data['id']} already exists. Please use a different ID.")
                return  # Stop saving process

            # Save to database and update UI
            self.data_tables[table_type].append(data)
            self.save_to_db(table_type, data, "add")
            self.undo_stack.append(("add", table_type, data))
        
            dialog.destroy()
            self.display_data_table(table_type)

        save_button = ttk.Button(form_frame, text="Save", command=validate_and_save)
        save_button.grid(row=len(headers) + 1, column=1, sticky=tk.E, padx=5, pady=10)

        cancel_button = ttk.Button(form_frame, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=len(headers) + 1, column=0, sticky=tk.W, padx=5, pady=10)


    def update_data_table(self, table_type, index, updated_data):
        old_data = self.data_tables[table_type][index].copy()
        self.data_tables[table_type][index] = updated_data
        self.undo_stack.append(("edit", table_type, index, old_data))

    def edit_selected_item(self, event, treeview, table_type):
        selection = treeview.selection()
        if not selection:
            return
        item = selection[0]
        item_values = treeview.item(item, "values")
        headers = self.get_headers_for_type(table_type)
        item_id = item_values[0]
        item_index = None
        for i, record in enumerate(self.data_tables[table_type]):
            if str(record.get("id", "")) == str(item_id):
                item_index = i
                break
        if item_index is None:
            return
        self.show_edit_form(table_type, item_index)

    def show_edit_form(self, table_type, item_index):
        data = self.data_tables[table_type][item_index]
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit {table_type.capitalize()}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)

        headers = self.get_headers_for_type(table_type)
        entry_widgets = {}
        for i, field in enumerate(headers):
            ttk.Label(form_frame, text=field.capitalize() + ":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            current_value = data.get(field, "")
            if field == "description":
                widget = tk.Text(form_frame, height=4, width=40)
                widget.insert("1.0", current_value)
            elif field == "status":
                widget = ttk.Combobox(form_frame, values=["New", "In Progress", "Completed", "On Hold"])
                widget.set(current_value if current_value else "New")
            elif field == "priority":
                widget = ttk.Combobox(form_frame, values=["Low", "Medium", "High", "Critical"])
                widget.set(current_value if current_value else "Medium")
            elif field == "modified":
                widget = ttk.Entry(form_frame, width=30)
                widget.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
            else:
                widget = ttk.Entry(form_frame, width=30)
                widget.insert(0, str(current_value))
            widget.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
            entry_widgets[field] = widget

        def update_entry():
            updated_data = {}
            for field, widget in entry_widgets.items():
                if isinstance(widget, tk.Text):
                    updated_data[field] = widget.get("1.0", tk.END).strip()
                else:
                    updated_data[field] = widget.get()
            self.update_data_table(table_type, item_index, updated_data)
            self.save_to_db(table_type, updated_data, "edit", old_data=data)
            dialog.destroy()
            self.display_data_table(table_type)

        update_button = ttk.Button(form_frame, text="Update", command=update_entry)
        update_button.grid(row=len(headers) + 1, column=1, sticky=tk.E, padx=5, pady=10)
        cancel_button = ttk.Button(form_frame, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=len(headers) + 1, column=0, sticky=tk.W, padx=5, pady=10)

    def import_from_excel(self):
        """Imports data from an Excel file into the corresponding tables while preventing duplicate IDs."""
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            return

        try:
            df_dict = pd.read_excel(file_path, sheet_name=None)  # Read all sheets into a dictionary
            valid_tables = {"feature", "requirement", "design", "implementation", "testcase"}
            imported_count = 0
            skipped_count = 0
            debug_info = []

            for sheet_name, df in df_dict.items():
                table_name = sheet_name.strip().lower()  # Normalize sheet name
                if table_name in valid_tables:
                    headers = self.get_headers_for_type(table_name)
                    df.columns = df.columns.str.strip()  # Remove whitespace from column names
                    debug_info.append(f"Checking sheet: {sheet_name}, Expected Headers: {headers}, Found Headers: {df.columns.tolist()}")

                    if all(col in df.columns for col in headers):
                        data_list = df.to_dict(orient="records")

                        if data_list:  # Ensure data is not empty
                            for data in data_list:
                                entry_id = data.get("id")
                                
                                # Check if ID already exists in the database
                                cursor = self.conn.cursor(dictionary=True)
                                cursor.execute(f"SELECT id FROM {table_name} WHERE id = %s", (entry_id,))
                                existing_entry = cursor.fetchone()
                                cursor.close()

                                if existing_entry:
                                    skipped_count += 1
                                    debug_info.append(f"Skipping duplicate ID: {entry_id}")
                                    continue  # Skip duplicate entry

                                self.data_tables[table_name].append(data)
                                self.save_to_db(table_name, data, "add")
                                imported_count += 1
                        else:
                            messagebox.showwarning("Empty Data", f"Sheet '{sheet_name}' has headers but no data.")
                    else:
                        messagebox.showwarning("Invalid Format", f"Sheet '{sheet_name}' does not match the required format.\nFound headers: {df.columns.tolist()}")

            if imported_count > 0:
                messagebox.showinfo("Import Successful", f"Imported {imported_count} entries successfully.\nSkipped {skipped_count} duplicate entries.")
                if self.current_view:
                    self.display_data_table(self.current_view)
            else:
                messagebox.showwarning("No Data Imported", f"No valid data was found in the selected file.\nSkipped {skipped_count} duplicate entries.\nDebug Info:\n" + "\n".join(debug_info))

        except Exception as e:
            messagebox.showerror("Import Failed", f"Error: {str(e)}")


    def export_to_excel(self, table_type):
        """Exports data from a selected table type to an Excel file."""
        if not table_type:
            messagebox.showinfo("Export", "No table type selected.")
            return
        if not self.data_tables.get(table_type):
            messagebox.showinfo("Export", "No data to export.")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Export to Excel"
            )
            if not file_path:
                return

            # Create DataFrame and align columns
            headers = self.get_headers_for_type(table_type)
            df = pd.DataFrame(self.data_tables[table_type])
            df = df[headers] if not df.empty else pd.DataFrame(columns=headers)

            # Use XlsxWriter engine
            with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name=table_type.capitalize(), index=False)

                # Adjust column width for readability
                worksheet = writer.sheets[table_type.capitalize()]
                col_indices = {header: i for i, header in enumerate(headers)}
                if "created" in col_indices:
                    worksheet.set_column(col_indices["created"], col_indices["created"], 20)
                if "modified" in col_indices:
                    worksheet.set_column(col_indices["modified"], col_indices["modified"], 20)

            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {str(e)}")

    def print_table_as_excel(self):
        """Prints the currently selected table."""
        if not self.current_view:
            messagebox.showinfo("Print", "No table selected for printing.")
            return
        if not self.data_tables.get(self.current_view):
            messagebox.showinfo("Print", "No data available to print.")
            return
        try:
            headers = self.get_headers_for_type(self.current_view)
            df = pd.DataFrame(self.data_tables[self.current_view])
            df = df[headers] if not df.empty else pd.DataFrame(columns=headers)

            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        
            # Use XlsxWriter engine
            with pd.ExcelWriter(tmp.name, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name=self.current_view.capitalize(), index=False)

                # Adjust column width
                worksheet = writer.sheets[self.current_view.capitalize()]
                col_indices = {header: i for i, header in enumerate(headers)}
                if "created" in col_indices:
                    worksheet.set_column(col_indices["created"], col_indices["created"], 20)
                if "modified" in col_indices:
                    worksheet.set_column(col_indices["modified"], col_indices["modified"], 20)

            tmp.close()

            # Attempt to print file on Windows
            if os.name == "nt":
                try:
                    os.startfile(tmp.name, "print")
                    messagebox.showinfo("Print", "Printing initiated. Check your printer.")
                except Exception:
                    messagebox.showinfo("Print", f"Failed to auto-print. File saved at {tmp.name}, open and print manually.")
            else:
                messagebox.showinfo("Print", f"Excel file generated at {tmp.name}. Please open and print manually.")

        except Exception as e:
            messagebox.showerror("Print Failed", f"Error: {str(e)}")


    def new_item(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("New Item", "Please select a category first")
            return
        item = selected_items[0]
        item_text = self.tree.item(item, "text").lower()
        if item_text in self.data_tables:
            self.show_entry_form(item_text)
        else:
            parent_id = self.tree.parent(item)
            if parent_id:
                parent_text = self.tree.item(parent_id, "text").lower()
                if parent_text in self.data_tables:
                    self.show_entry_form(parent_text)

    def delete_selected(self):
        """
        Delete the selected row(s) from the right-side table (self.current_tableview),
        remove them from in-memory data (self.data_tables), and delete from the DB.
        """
        if not self.current_view or not self.current_tableview:
            messagebox.showinfo("Delete", "No table is currently selected.")
            return

        selection = self.current_tableview.selection()
        if not selection:
            messagebox.showinfo("Delete", "Please select one or more rows to delete.")
            return

        # Ask for confirmation once for all selected rows.
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the selected {len(selection)} row(s)?")
        if not confirm:
            return

        for item in selection:
            row_values = self.current_tableview.item(item, "values")
            if not row_values:
                continue
            row_id = str(row_values[0])  # Assuming the first column is 'id'

            # Locate and remove the record from the in-memory data table.
            data_list = self.data_tables[self.current_view]
            index_to_delete = None
            for i, record in enumerate(data_list):
                if str(record.get("id", "")) == row_id:
                    index_to_delete = i
                    break

            if index_to_delete is not None:
                deleted_item = data_list.pop(index_to_delete)
                self.undo_stack.append(("delete", self.current_view, deleted_item))
                # Delete the row from the database.
                self.save_to_db(self.current_view, deleted_item, "delete")

            # Remove the item from the Treeview.
            self.current_tableview.delete(item)

        messagebox.showinfo("Delete", "Selected row(s) have been deleted.")

    def display_message(self, message):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        msg_label = ttk.Label(self.right_frame, text=message, font=("Arial", 14), foreground="blue")
        msg_label.place(relx=0.5, rely=0.5, anchor="center")

    def undo(self):
        if not self.undo_stack:
            messagebox.showinfo("Undo", "No actions to undo.")
            return
        action = self.undo_stack.pop()
        action_type = action[0]
        if action_type == "add":
            table_type = action[1]
            data = action[2]
            self.data_tables[table_type].remove(data)
            self.save_to_db(table_type, data, "delete")
            self.redo_stack.append(action)
        elif action_type == "edit":
            table_type = action[1]
            index = action[2]
            previous_data = action[3]
            current_data = self.data_tables[table_type][index].copy()
            self.data_tables[table_type][index] = previous_data
            self.save_to_db(table_type, previous_data, "edit", old_data=current_data)
            self.redo_stack.append(action)
        elif action_type == "delete":
            table_type = action[1]
            deleted_item = action[2]
            self.data_tables[table_type].append(deleted_item)
            self.save_to_db(table_type, deleted_item, "add")
            self.redo_stack.append(action)
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
            self.data_tables[table_type].append(data)
            self.save_to_db(table_type, data, "add")
            self.undo_stack.append(action)
        elif action_type == "edit":
            table_type = action[1]
            index = action[2]
            old_data = action[3]
            current_data = self.data_tables[table_type][index].copy()
            self.data_tables[table_type][index] = old_data
            self.save_to_db(table_type, old_data, "edit", old_data=current_data)
            self.undo_stack.append(action)
        elif action_type == "delete":
            table_type = action[1]
            deleted_item = action[2]
            self.data_tables[table_type].remove(deleted_item)
            self.save_to_db(table_type, deleted_item, "delete")
            self.undo_stack.append(action)
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
