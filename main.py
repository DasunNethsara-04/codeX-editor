import customtkinter
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu
from tkinter import filedialog
from utils import file_types, check_file_type
from customtkinter import CTk, CTkTextbox, CTkLabel, CTkFrame, CTkButton, StringVar, BOTH, BOTTOM, X, RIGHT, LEFT

# required functions
def clear_code_area() -> None:
    code_area.delete("0.0", "end")

def create_new_file(event=None) -> None:
    language_var.set('Text File')
    clear_code_area()

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

def change_appearance_mode(mode:str="Dark") -> None:
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
status_var:StringVar = StringVar()
status_var.set("Ready!")

language_var:StringVar = StringVar()
language_var.set("Text File")

font_size = 13

# user interface widgets

# menu bar
menu = CTkMenuBar(master=window)

file_menu:CTkButton = menu.add_cascade("File")
view_menu:CTkButton = menu.add_cascade("View")
about_menu:CTkButton = menu.add_cascade("About")


# file menu option
file_dropdown:CustomDropdownMenu = CustomDropdownMenu(widget=file_menu)
file_dropdown.add_option(option="New File", command=create_new_file)
file_dropdown.add_option(option="New Project")
file_dropdown.add_separator()
file_dropdown.add_option(option="Open File", command=open_file_content)
file_dropdown.add_separator()
file_dropdown.add_option(option="Save File", command=save_file)
file_dropdown.add_option(option="Save File As...", command=save_file)
file_dropdown.add_separator()
file_dropdown.add_option(option="Exit", command=lambda : window.destroy())

# view menu option
view_dropdown:CustomDropdownMenu = CustomDropdownMenu(widget=view_menu)
appearance_submenu:CustomDropdownMenu = view_dropdown.add_submenu("Appearance Mode")
appearance_submenu.add_option("LIGHT", command=lambda:change_appearance_mode("Light"))
appearance_submenu.add_option("DARK", command=lambda:change_appearance_mode("Dark"))
appearance_submenu.add_option("SYSTEM", command=lambda:change_appearance_mode("System"))

# text box
code_area: CTkTextbox = CTkTextbox(window, font=("Consolas", font_size))
code_area.pack(fill=BOTH, expand=True)

# Now create the status bar
status_bar:CTkFrame = CTkFrame(window, height=25)
status_bar.pack(side=BOTTOM, fill=X)

# Left side label (Status)
status_label:CTkLabel = CTkLabel(status_bar, textvariable=status_var, anchor="w")
status_label.pack(side=LEFT, padx=10)

# Right side label (Language)
language_label:CTkLabel = CTkLabel(status_bar, textvariable=language_var, anchor="e")
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

window.mainloop()
