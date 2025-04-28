from CTkMenuBar import *
from tkinter import filedialog
from customtkinter import CTk, CTkTextbox, CTkLabel, BOTH

# required functions
def open_file_content() -> list[str]:
    filename: str = filedialog.askopenfilename()
    content: list[str] = []
    with open(filename, "r") as file:
        content = [line for line in file.readlines()]
    return content

def set_content() -> None:
    file_content:list[str] = open_file_content()
    for line in file_content:
        code_area.insert("0.0", line)

def save_file() -> None:
    pass

def save_file_as() -> None:
    pass

# main user interface configurations
window: CTk = CTk()
window.title("Text Editor")
window.geometry("1200x720")
window.resizable(width=True, height=True)

# menu bar
menu = CTkMenuBar(master=window)

file_menu = menu.add_cascade("File")
view_menu = menu.add_cascade("View")
about_menu = menu.add_cascade("About")


# file menu option
file_dropdown = CustomDropdownMenu(widget=file_menu)
file_dropdown.add_option(option="New File")
file_dropdown.add_option(option="New Project")
file_dropdown.add_separator()
file_dropdown.add_option(option="Open File", command=set_content)
file_dropdown.add_separator()
file_dropdown.add_option(option="Save File", command=save_file)
file_dropdown.add_option(option="Save File As...", command=save_file_as)
file_dropdown.add_separator()
file_dropdown.add_option(option="Exit", command=lambda : window.destroy())


# user interface widgets
code_area: CTkTextbox = CTkTextbox(window, font=("Consolas", 25))
code_area.pack(fill=BOTH, expand=True)



window.mainloop()
