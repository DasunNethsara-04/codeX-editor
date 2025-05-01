import os
from tkinter import filedialog

import customtkinter
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu
from CTkMessagebox import CTkMessagebox
from customtkinter import (CTk,
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
                           CTkToplevel, CTkRadioButton, CTkEntry
                           )

from utils import file_types, check_file_type, create_project_files


# required functions
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

    # ---------- Title Label ----------
    CTkLabel(new_project_window, text="Create New Project", font=("Arial", 20, "bold")).pack(pady=20)

    # ---------- Project Name ----------
    name_frame = CTkFrame(new_project_window)
    name_frame.pack(padx=20, pady=10, fill=X)

    CTkLabel(name_frame, text="Project Name:", width=120, anchor="w").pack(side=LEFT)
    project_name_var = StringVar()
    CTkEntry(name_frame, textvariable=project_name_var).pack(side=LEFT, fill=X, expand=True, padx=10)

    # ---------- Project Path ----------
    path_frame = CTkFrame(new_project_window)
    path_frame.pack(padx=20, pady=10, fill=X)

    CTkLabel(path_frame, text="Save Location:", width=120, anchor="w").pack(side=LEFT)
    project_path_var = StringVar()
    path_entry = CTkEntry(path_frame, textvariable=project_path_var)
    path_entry.pack(side=LEFT, fill=X, expand=True, padx=10)

    def browse_folder():
        path = filedialog.askdirectory()
        if path:
            project_path_var.set(path)
        new_project_window.focus()

    CTkButton(path_frame, text="Browse", command=browse_folder, width=80).pack(side=LEFT)

    # ---------- Project Type ----------
    CTkLabel(new_project_window, text="Project Type:", anchor="w").pack(padx=20, anchor="w")
    type_frame = CTkFrame(new_project_window)
    type_frame.pack(padx=20, pady=10, anchor="w")

    project_type_var = StringVar(value="Python")

    CTkRadioButton(type_frame, text="Python", variable=project_type_var, value="Python").pack(side=LEFT, padx=10)
    CTkRadioButton(type_frame, text="Web (HTML/CSS/JS)", variable=project_type_var, value="Web").pack(side=LEFT,
                                                                                                      padx=10)

    # ---------- Create Button ----------
    def create_project():
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
        else:
            CTkMessagebox(title="Error", message="Unknown Error", icon="cancel")

    CTkButton(new_project_window, text="Create Project", command=create_project, width=200).pack(pady=20)

    # Center the window
    new_project_window.focus()


def open_project(path: str) -> None:
    pass

def open_file_content(event=None) -> None:
    filename: str = filedialog.askopenfilename()
    language_var.set(check_file_type(filename))
    with open(filename, "r") as file:
        code_area.delete("0.0", "end")
        code_area.insert("0.0", file.read())


def get_code_area_content() -> str:
    return code_area.get("0.0", "end")


def save_file(event=None) -> None:
    content: str = get_code_area_content()
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)
    if filepath:
        with open(filepath, "w") as file:
            file.write(content)


def save_file_as() -> None:
    pass


def change_appearance_mode(mode: str = "Dark") -> None:
    customtkinter.set_appearance_mode(mode)


def zoom_in_text(event=None) -> None:
    global font_size
    font_size += 2
    code_area.configure(font=("Consolas", font_size))


def zoom_out_text(event=None) -> None:
    global font_size
    font_size -= 2
    code_area.configure(font=("Consolas", font_size))


def reset_zoom_text(event=None) -> None:
    global font_size
    font_size = 13
    code_area.configure(font=("Consolas", font_size))


# main user interface configurations
window: CTk = CTk()
window.title("Text Editor")
window.geometry("1200x720")
window.resizable(width=True, height=True)

# special variables
status_var: StringVar = StringVar()
status_var.set("Ready!")

language_var: StringVar = StringVar()
language_var.set("Text File")

font_size = 13

# user interface widgets

# menu bar
menu = CTkMenuBar(master=window)

file_menu: CTkButton = menu.add_cascade("File")
view_menu: CTkButton = menu.add_cascade("View")
about_menu: CTkButton = menu.add_cascade("About")

# file menu option
file_dropdown: CustomDropdownMenu = CustomDropdownMenu(widget=file_menu)
file_dropdown.add_option(option="New File", command=create_new_file)
file_dropdown.add_option(option="New Project", command=create_new_project)
file_dropdown.add_separator()
file_dropdown.add_option(option="Open File", command=open_file_content)
file_dropdown.add_separator()
file_dropdown.add_option(option="Save File", command=save_file)
file_dropdown.add_option(option="Save File As...", command=save_file)
file_dropdown.add_separator()
file_dropdown.add_option(option="Exit", command=lambda: window.destroy())

# view menu option
view_dropdown: CustomDropdownMenu = CustomDropdownMenu(widget=view_menu)
appearance_submenu: CustomDropdownMenu = view_dropdown.add_submenu("Appearance Mode")
appearance_submenu.add_option("LIGHT", command=lambda: change_appearance_mode("Light"))
appearance_submenu.add_option("DARK", command=lambda: change_appearance_mode("Dark"))
appearance_submenu.add_option("SYSTEM", command=lambda: change_appearance_mode("System"))

# text box
code_area: CTkTextbox = CTkTextbox(window, font=("Consolas", font_size))
code_area.pack(fill=BOTH, expand=True)

# Now create the status bar
status_bar: CTkFrame = CTkFrame(window, height=25)
status_bar.pack(side=BOTTOM, fill=X)

# Left side label (Status)
status_label: CTkLabel = CTkLabel(status_bar, textvariable=status_var, anchor="w")
status_label.pack(side=LEFT, padx=10)

# Right side label (Language)
language_label: CTkLabel = CTkLabel(status_bar, textvariable=language_var, anchor="e")
language_label.pack(side=RIGHT, padx=10)

# keyboard shortcuts

# zoom
window.bind("<Control-plus>", zoom_in_text)
window.bind("<Control-minus>", zoom_out_text)
window.bind("<Control-0>", reset_zoom_text)

# save file
window.bind("<Control-s>", save_file)

# open file
window.bind("<Control-o>", open_file_content)

# new file
window.bind("<Control-n>", create_new_file)

# new project
window.bind("<Control-m>", create_new_project)

window.mainloop()
