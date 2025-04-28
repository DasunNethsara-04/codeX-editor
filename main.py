from CTkMenuBar import *
from tkinter import filedialog
from utils import file_types
from customtkinter import CTk, CTkTextbox, CTkLabel, BOTH

# required functions
def clear_code_area() -> None:
    code_area.delete("0.0", "end")

def create_new_file() -> None:
    clear_code_area()

def open_file_content() -> list[str]:
    filename: str = filedialog.askopenfilename()
    content: list[str] = []
    with open(filename, "r") as file:
        content = [line for line in file.readlines()]
    return content

def set_content() -> None:
    file_content:list[str] = open_file_content()
    clear_code_area()
    for line in file_content:
        code_area.insert("0.0", line)

def get_code_area_content() -> str:
    return code_area.get("0.0", "end")

def save_file() -> None:
    content: str = get_code_area_content()
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)
    if filepath:
        with open(filepath, "w") as file:
            file.write(content)

def save_file_as() -> None:
    pass

# main user interface configurations
window: CTk = CTk()
window.title("Text Editor")
window.geometry("1200x720")
window.resizable(width=True, height=True)

# user interface widgets

# menu bar
menu = CTkMenuBar(master=window)

file_menu = menu.add_cascade("File")
view_menu = menu.add_cascade("View")
about_menu = menu.add_cascade("About")


# file menu option
file_dropdown = CustomDropdownMenu(widget=file_menu)
file_dropdown.add_option(option="New File", command=create_new_file)
file_dropdown.add_option(option="New Project")
file_dropdown.add_separator()
file_dropdown.add_option(option="Open File", command=set_content)
file_dropdown.add_separator()
file_dropdown.add_option(option="Save File", command=save_file)
file_dropdown.add_option(option="Save File As...", command=save_file)
file_dropdown.add_separator()
file_dropdown.add_option(option="Exit", command=lambda : window.destroy())

code_area: CTkTextbox = CTkTextbox(window, font=("Consolas", 25))
code_area.pack(fill=BOTH, expand=True)



window.mainloop()
