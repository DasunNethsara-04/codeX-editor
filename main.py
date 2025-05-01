import os
import tkinter.ttk as ttk
from tkinter import filedialog, Y

import customtkinter
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu
from CTkMessagebox import CTkMessagebox
from customtkinter import (
    CTk,
    CTkTextbox,
    CTkLabel,
    CTkFrame,
    CTkButton,
    StringVar,
    BOTH,
    BOTTOM,
    X,
    RIGHT,
    LEFT,
    TOP,
    CTkToplevel, CTkRadioButton, CTkEntry
)

from utils import file_types, check_file_type, create_project_files

def clear_code_area() -> None:
    code_area.delete("0.0", "end")


def create_new_file(event=None) -> None:
    language_var.set('Text File')
    clear_code_area()


def center_window(win, width=600, height=400):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")


def create_new_project(event=None) -> None:
    new_project_window: CTkToplevel = CTkToplevel()
    new_project_window.title("New Project")
    center_window(new_project_window, 600, 400)
    new_project_window.resizable(False, False)

    CTkLabel(new_project_window, text="Create New Project", font=("Arial", 20, "bold")).pack(pady=20)

    name_frame = CTkFrame(new_project_window)
    name_frame.pack(padx=20, pady=10, fill=X)
    CTkLabel(name_frame, text="Project Name:", width=120, anchor="w").pack(side=LEFT)
    project_name_var = StringVar()
    CTkEntry(name_frame, textvariable=project_name_var).pack(side=LEFT, fill=X, expand=True, padx=10)

    path_frame = CTkFrame(new_project_window)
    path_frame.pack(padx=20, pady=10, fill=X)
    CTkLabel(path_frame, text="Save Location:", width=120, anchor="w").pack(side=LEFT)
    project_path_var = StringVar()
    path_entry = CTkEntry(path_frame, textvariable=project_path_var)
    path_entry.pack(side=LEFT, fill=X, expand=True, padx=10)

    def browse_folder() -> None:
        path = filedialog.askdirectory()
        if path:
            project_path_var.set(path)
        new_project_window.focus()

    CTkButton(path_frame, text="Browse", command=browse_folder, width=80).pack(side=LEFT)

    CTkLabel(new_project_window, text="Project Type:", anchor="w").pack(padx=20, anchor="w")
    type_frame = CTkFrame(new_project_window)
    type_frame.pack(padx=20, pady=10, anchor="w")
    project_type_var = StringVar(value="Python")
    CTkRadioButton(type_frame, text="Python", variable=project_type_var, value="Python").pack(side=LEFT, padx=10)
    CTkRadioButton(type_frame, text="Web (HTML/CSS/JS)", variable=project_type_var, value="Web").pack(side=LEFT,
                                                                                                      padx=10)

    def create_project() -> None:
        name = project_name_var.get()
        path = project_path_var.get()
        ptype = project_type_var.get()

        if not name or not path:
            CTkMessagebox(title="Error", message="Please enter a name and path.", icon="cancel")
            return

        full_path = os.path.join(path, name)
        status: bool = create_project_files(project_type=ptype, project_name=name, full_path=full_path)
        if status:
            CTkMessagebox(title="Success", message=f"Project '{name}' created!", icon="check")
            new_project_window.destroy()
            open_project(full_path)
        else:
            CTkMessagebox(title="Error", message="Unknown Error", icon="cancel")

    CTkButton(new_project_window, text="Create Project", command=create_project, width=200).pack(pady=20)
    new_project_window.focus()


# -------------------- Directory Tree Functions --------------------
tree_paths = {}


def load_directory(parent, path) -> None:
    tree.delete(*tree.get_children(parent))
    try:
        items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        for item in items:
            item_path = os.path.join(path, item)
            node_id = tree.insert(parent, "end", text=item, open=False)
            tree_paths[node_id] = item_path
            if os.path.isdir(item_path):
                tree.insert(node_id, "end")
    except PermissionError:
        pass


def on_tree_expand(event) -> None:
    node_id = tree.focus()
    path = tree_paths.get(node_id)
    if os.path.isdir(path):
        load_directory(node_id, path)


def on_tree_double_click(event) -> None:
    node_id = tree.focus()
    path = tree_paths.get(node_id)
    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
        code_area.delete("0.0", "end")
        code_area.insert("0.0", content)
        language_var.set(check_file_type(path))
        status_var.set(f"Opened: {os.path.basename(path)}")


def open_project(path: str) -> None:
    tree.delete(*tree.get_children(""))
    root_node = tree.insert("", "end", text=os.path.basename(path), open=True)
    tree_paths[root_node] = path
    load_directory(root_node, path)


# -------------------- File Functions --------------------
def open_file_content(event=None) -> None:
    filename: str = filedialog.askopenfilename()
    if filename:  # Add check if file was selected
        language_var.set(check_file_type(filename))
        with open(filename, "r") as file:
            code_area.delete("0.0", "end")
            code_area.insert("0.0", file.read())
        status_var.set(f"Opened: {os.path.basename(filename)}")


def open_folder_as_project(event=None) -> None:
    folder_path = filedialog.askdirectory()
    if folder_path:
        open_project(folder_path)
        status_var.set(f"Project opened: {os.path.basename(folder_path)}")


def get_code_area_content() -> str:
    return code_area.get("0.0", "end")


def save_file(event=None) -> None:
    content: str = get_code_area_content()
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)
    if filepath:
        with open(filepath, "w") as file:
            file.write(content)
        status_var.set(f"Saved: {os.path.basename(filepath)}")


def save_file_as() -> None:
    save_file()  # Reuse the save_file function since it always asks for location


def change_appearance_mode(mode: str = "Dark") -> None:
    customtkinter.set_appearance_mode(mode)


def zoom_in_text(event=None) -> None:
    global font_size
    font_size += 2
    code_area.configure(font=("Consolas", font_size))


def zoom_out_text(event=None) -> None:
    global font_size
    font_size = max(8, font_size - 2)  # Prevent font from becoming too small
    code_area.configure(font=("Consolas", font_size))


def reset_zoom_text(event=None) -> None:
    global font_size
    font_size = 13
    code_area.configure(font=("Consolas", font_size))


# -------------------- UI Setup --------------------
window: CTk = CTk()
window.title("Text Editor")
window.geometry("1200x720")
window.resizable(width=True, height=True)

status_var: StringVar = StringVar(value="Ready!")
language_var: StringVar = StringVar(value="Text File")
font_size = 13

# Add the menu bar at the top
menu = CTkMenuBar(master=window)
file_menu: CTkButton = menu.add_cascade("File")
view_menu: CTkButton = menu.add_cascade("View")
about_menu: CTkButton = menu.add_cascade("About")

# Create the main container frame
content_frame = CTkFrame(window)
content_frame.pack(fill=BOTH, expand=True)

file_dropdown: CustomDropdownMenu = CustomDropdownMenu(widget=file_menu)
file_dropdown.add_option(option="New File", command=create_new_file)
file_dropdown.add_option(option="New Project", command=create_new_project)
file_dropdown.add_separator()
file_dropdown.add_option(option="Open File", command=open_file_content)
file_dropdown.add_option(option="Open Folder as Project", command=open_folder_as_project)
file_dropdown.add_separator()
file_dropdown.add_option(option="Save File", command=save_file)
file_dropdown.add_option(option="Save File As...", command=save_file_as)
file_dropdown.add_separator()
file_dropdown.add_option(option="Exit", command=lambda: window.destroy())

view_dropdown: CustomDropdownMenu = CustomDropdownMenu(widget=view_menu)
appearance_submenu: CustomDropdownMenu = view_dropdown.add_submenu("Appearance Mode")
appearance_submenu.add_option("LIGHT", command=lambda: change_appearance_mode("Light"))
appearance_submenu.add_option("DARK", command=lambda: change_appearance_mode("Dark"))
appearance_submenu.add_option("SYSTEM", command=lambda: change_appearance_mode("System"))

# Set up sidebar visibility control
sidebar_visible = True

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.pack_forget()
    else:
        # Re-pack the sidebar on the left side of the content frame
        sidebar_frame.pack(side=LEFT, fill=Y, before=main_content)
    sidebar_visible = not sidebar_visible

view_dropdown.add_option(option="Toggle Sidebar", command=toggle_sidebar)

# Create the sidebar frame
sidebar_frame = CTkFrame(content_frame, width=250)
sidebar_frame.pack(side=LEFT, fill=Y)

# Create the main content area (will contain code area)
main_content = CTkFrame(content_frame)
main_content.pack(side=RIGHT, fill=BOTH, expand=True)

# Add tree to sidebar
tree = ttk.Treeview(sidebar_frame, show="tree")  # Only show the tree, not the headings
tree.pack(fill=BOTH, expand=True)

# tree_scroll = ttk.Scrollbar(sidebar_frame, orient="vertical", command=tree.yview)
# tree.configure(yscrollcommand=tree_scroll.set)
# tree_scroll.pack(side=RIGHT, fill=Y)

tree.bind("<<TreeviewOpen>>", on_tree_expand)
tree.bind("<Double-1>", on_tree_double_click)

# Add code area to main content
code_area: CTkTextbox = CTkTextbox(main_content, font=("Consolas", font_size))
code_area.pack(fill=BOTH, expand=True)

# Add status bar at the bottom of the window
status_bar: CTkFrame = CTkFrame(window, height=25)
status_bar.pack(side=BOTTOM, fill=X)

status_label: CTkLabel = CTkLabel(status_bar, textvariable=status_var, anchor="w")
status_label.pack(side=LEFT, padx=10)

status_file_label: CTkLabel = CTkLabel(status_bar, textvariable=language_var, anchor="w")
status_file_label.pack(side=RIGHT, padx=10)

# Keyboard shortcuts
window.bind("<Control-plus>", zoom_in_text)
window.bind("<Control-minus>", zoom_out_text)
window.bind("<Control-0>", reset_zoom_text)
window.bind("<Control-s>", save_file)
window.bind("<Control-n>", create_new_file)
window.bind("<Control-o>", open_file_content)

window.mainloop()