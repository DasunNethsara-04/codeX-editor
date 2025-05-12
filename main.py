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
    CTkToplevel, CTkRadioButton, CTkEntry
)
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer

from utils.keymap import *
from utils.config import *
from utils import file_types, check_file_type, create_project_files, CHANGELOG, SYNTAX_COLORS, get_lexer_for_language

# Add a global variable to track the current file path
current_file_path: str | None = None


def clear_code_area() -> None:
    code_area.delete("0.0", "end")


def create_new_file(event=None) -> None:
    global current_file_path
    current_file_path = None
    language_var.set('Text File')
    clear_code_area()
    status_var.set("Ready!")
    update_line_numbers()


def center_window(win, width=600, height=400) -> None:
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")


def create_new_project(event=None) -> None:
    new_project_window: CTkToplevel = CTkToplevel()
    new_project_window.title("New Project")
    new_project_window.iconbitmap("./logo.ico")
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
    global current_file_path
    node_id = tree.focus()
    path = tree_paths.get(node_id)
    if os.path.isfile(path):
        current_file_path = path
        with open(path, "r") as f:
            content = f.read()
        code_area.delete("0.0", "end")
        code_area.insert("0.0", content)
        language_var.set(check_file_type(path))
        status_var.set(f"Opened: {os.path.basename(path)}")
        highlight_syntax(language_var.get())
        update_line_numbers()


def open_project(path: str) -> None:
    tree.delete(*tree.get_children(""))
    root_node = tree.insert("", "end", text=os.path.basename(path), open=True)
    tree_paths[root_node] = path
    load_directory(root_node, path)


# -------------------- File Functions --------------------
def open_file_content(event=None) -> None:
    global current_file_path
    filename: str = filedialog.askopenfilename()
    if filename:
        current_file_path = filename
        language_var.set(check_file_type(filename))
        with open(filename, "r") as file:
            code_area.delete("0.0", "end")
            code_area.insert("0.0", file.read())
        status_var.set(f"Opened: {os.path.basename(filename)}")
        update_line_numbers()


def open_folder_as_project(event=None) -> None:
    folder_path = filedialog.askdirectory()
    if folder_path:
        open_project(folder_path)
        status_var.set(f"Project opened: {os.path.basename(folder_path)}")


def get_code_area_content() -> str:
    return code_area.get("0.0", "end")


def save_file(event=None) -> None:
    global current_file_path
    content: str = get_code_area_content()

    if current_file_path:
        # Save to existing file path
        with open(current_file_path, "w", encoding="utf-8") as file:
            file.write(content)
        status_var.set(f"Saved: {os.path.basename(current_file_path)}")

        # Refresh syntax highlighting
        highlight_syntax(check_file_type(current_file_path))
    else:
        # No path exists, call save_file_as
        save_file_as()


def save_file_as(event=None) -> None:
    global current_file_path
    content: str = get_code_area_content()
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)

    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        current_file_path = filepath
        language_var.set(check_file_type(filepath))
        status_var.set(f"Saved: {os.path.basename(filepath)}")

        # Apply syntax highlighting for the newly saved file
        highlight_syntax(check_file_type(filepath))


def change_appearance_mode(mode: str = "Dark") -> None:
    customtkinter.set_appearance_mode(mode)

    # Re-apply syntax highlighting if we're viewing a code file
    if language_var.get() != "Text File":
        highlight_syntax(language_var.get())


def about_codeX(event=None) -> None:
    CTkMessagebox(title=f"About {APP_NAME}",
                  message=f"{APP_NAME}: {APP_EDITION} Edition\nVersion: {APP_VERSION}\nDeveloped by: Dasun Nethsara")


def whats_new_dialog(event=None) -> None:
    changelog_window = CTkToplevel()
    changelog_window.title(f"{APP_NAME} - What's New")
    changelog_window.iconbitmap("./logo.ico")
    center_window(changelog_window, 600, 500)
    changelog_window.resizable(True, True)

    # Main title
    header_frame = CTkFrame(changelog_window)
    header_frame.pack(fill=X, padx=20, pady=20)

    CTkLabel(
        header_frame,
        text=f"{APP_NAME} Change Log",
        font=("Arial", 24, "bold")
    ).pack(side=LEFT)

    CTkLabel(
        header_frame,
        text=f"Current Version: {APP_VERSION}",
        font=("Arial", 14)
    ).pack(side=RIGHT, padx=10)

    scrollable_frame = customtkinter.CTkScrollableFrame(
        changelog_window,
        width=560,
        height=380
    )
    scrollable_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

    # Add version history
    for version, changes in CHANGELOG:
        # Version header
        version_frame = CTkFrame(scrollable_frame)
        version_frame.pack(fill=X, pady=(15, 5))

        CTkLabel(
            version_frame,
            text=f"Version {version}",
            font=("Arial", 16, "bold"),
            anchor="w"
        ).pack(fill=X, padx=10, pady=5)

        changes_frame = CTkFrame(scrollable_frame)
        changes_frame.pack(fill=X, padx=20, pady=5)

        for i, change in enumerate(changes):
            change_item = CTkFrame(changes_frame)
            change_item.pack(fill=X, pady=2)

            bullet = CTkLabel(change_item, text="•", width=20, anchor="e")
            bullet.pack(side=LEFT, padx=(5, 0))

            CTkLabel(
                change_item,
                text=change,
                anchor="w",
                wraplength=480
            ).pack(side=LEFT, fill=X, expand=True, padx=5)

    CTkButton(
        changelog_window,
        text="Close",
        command=changelog_window.destroy,
        width=120,
        height=32
    ).pack(pady=(0, 20))

    def _on_mousewheel(event) -> None:
        scrollable_frame._parent_canvas.yview_scroll(-int(event.delta / 2), "units")

    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    # Focus the window
    changelog_window.focus()


def keymap(event=None) -> None:
    keymap_window = CTkToplevel()
    keymap_window.title("CodeX Keyboard Shortcuts")
    keymap_window.iconbitmap("./logo.ico")
    center_window(keymap_window, 550, 450)
    keymap_window.resizable(False, False)

    # Main title
    CTkLabel(keymap_window, text="Keyboard Shortcuts", font=("Arial", 20, "bold")).pack(pady=(20, 10))

    # Create a proper scrollable frame using customtkinter's scrollable frame
    scrollable_frame = customtkinter.CTkScrollableFrame(keymap_window, width=500, height=350)
    scrollable_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

    # File Operations
    file_frame = CTkFrame(scrollable_frame)
    file_frame.pack(fill=X, pady=10)
    CTkLabel(file_frame, text="File Operations", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

    for action, shortcut in file_shortcuts:
        shortcut_frame = CTkFrame(file_frame)
        shortcut_frame.pack(fill=X, padx=10, pady=2)
        CTkLabel(shortcut_frame, text=action, width=150, anchor="w").pack(side=LEFT)
        CTkLabel(shortcut_frame, text=shortcut, width=100, anchor="w").pack(side=LEFT)

    # Editing Operations
    edit_frame = CTkFrame(scrollable_frame)
    edit_frame.pack(fill=X, pady=10)
    CTkLabel(edit_frame, text="Editing", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

    for action, shortcut in edit_shortcuts:
        shortcut_frame = CTkFrame(edit_frame)
        shortcut_frame.pack(fill=X, padx=10, pady=2)
        CTkLabel(shortcut_frame, text=action, width=150, anchor="w").pack(side=LEFT)
        CTkLabel(shortcut_frame, text=shortcut, width=100, anchor="w").pack(side=LEFT)

    # View Operations
    view_frame = CTkFrame(scrollable_frame)
    view_frame.pack(fill=X, pady=10)
    CTkLabel(view_frame, text="View", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

    for action, shortcut in view_shortcuts:
        shortcut_frame = CTkFrame(view_frame)
        shortcut_frame.pack(fill=X, padx=10, pady=2)
        CTkLabel(shortcut_frame, text=action, width=150, anchor="w").pack(side=LEFT)
        CTkLabel(shortcut_frame, text=shortcut, width=100, anchor="w").pack(side=LEFT)

    # Help Operations
    help_frame = CTkFrame(scrollable_frame)
    help_frame.pack(fill=X, pady=10)
    CTkLabel(help_frame, text="Help", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

    for action, shortcut in help_shortcuts:
        shortcut_frame = CTkFrame(help_frame)
        shortcut_frame.pack(fill=X, padx=10, pady=2)
        CTkLabel(shortcut_frame, text=action, width=150, anchor="w").pack(side=LEFT)
        CTkLabel(shortcut_frame, text=shortcut, width=100, anchor="w").pack(side=LEFT)

    # Close button
    CTkButton(keymap_window, text="Close", command=keymap_window.destroy, width=100).pack(pady=(0, 20))

    # Add mouse wheel scrolling support
    def _on_mousewheel(event) -> None:
        scrollable_frame._parent_canvas.yview_scroll(-int(event.delta / 2), "units")

    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    # Focus the window
    keymap_window.focus()


def zoom_in_text(event=None) -> None:
    global font_size
    font_size += 2
    code_area.configure(font=("Consolas", font_size))


def zoom_out_text(event=None) -> None:
    global font_size
    font_size = max(8, font_size - 2)  # Prevent font from becoming too small
    code_area.configure(font=("Consolas", font_size))

    # Reapply syntax highlighting after zoom
    if language_var.get() != "Text File":
        highlight_syntax(language_var.get())


def reset_zoom_text(event=None) -> None:
    global font_size
    font_size = 13
    code_area.configure(font=("Consolas", font_size))

    # Reapply syntax highlighting after zoom
    if language_var.get() != "Text File":
        highlight_syntax(language_var.get())


# -------------------- Syntax Highlighting Functions --------------------
def highlight_syntax(language: str) -> None:
    """Apply syntax highlighting to the code area based on the language"""
    # Clear existing tags
    for tag in code_area._textbox.tag_names():
        code_area._textbox.tag_delete(tag)

    if language == "Text File":
        return  # No highlighting for plain text files

    # Get appropriate lexer for the language
    lexer = get_lexer_for_language(language)
    if not lexer:
        # Try to guess lexer if specific language mapping not found
        try:
            content = code_area.get("0.0", "end-1c")
            if content.strip():
                lexer = guess_lexer(content)
            else:
                return  # Empty content, nothing to highlight
        except:
            return  # Cannot guess lexer, no highlighting

    # Get current content
    content = code_area.get("0.0", "end-1c")

    # Create tags for token types
    for token_type, color in SYNTAX_COLORS.items():
        code_area._textbox.tag_configure(str(token_type), foreground=color)

    # Apply syntax highlighting
    tokens = list(lex(content, lexer))

    # Processing each token
    pos = 0
    for token, text in tokens:
        # Find token positions in the text
        token_end = pos + len(text)

        # Convert character positions to line.column format
        start_line = content[:pos].count('\n') + 1
        start_col = pos - content[:pos].rfind('\n') - 1 if '\n' in content[:pos] else pos

        end_line = content[:token_end].count('\n') + 1
        end_col = token_end - content[:token_end].rfind('\n') - 1 if '\n' in content[:token_end] else token_end

        start_index = f"{start_line}.{start_col}"
        end_index = f"{end_line}.{end_col}"

        # Apply color based on token type
        for token_type, color in SYNTAX_COLORS.items():
            if token is token_type or token in token_type:
                code_area._textbox.tag_add(str(token_type), start_index, end_index)
                break

        pos = token_end


def on_key_release(event=None) -> None:
    """Re-apply syntax highlighting after typing"""
    if language_var.get() != "Text File":
        # Only highlight if we're editing a code file
        # Use a timer to avoid excessive re-highlighting
        if hasattr(on_key_release, "timer_id"):
            window.after_cancel(on_key_release.timer_id)
        on_key_release.timer_id = window.after(500, lambda: highlight_syntax(language_var.get()))


def update_line_numbers(event=None):
    """Update line numbers dynamically with improved reliability"""
    try:
        # Get the total number of lines in the code area
        # Use get('1.0', 'end-1c') to ensure we capture the entire content
        code_lines = code_area.get('1.0', 'end-1c').split('\n')

        # Ensure we always have at least one line (even if empty)
        number_lines = max(1, len(code_lines))

        # Generate line numbers with consistent width for better alignment
        number_text = '\n'.join(f"{i + 1:4}" for i in range(number_lines))

        # Update the line number widget
        line_numbers.configure(state="normal")
        line_numbers.delete('1.0', 'end')
        line_numbers.insert('1.0', number_text)
        line_numbers.configure(state="disabled")
    except Exception as e:
        print(f"Error updating line numbers: {e}")


# Modify scroll synchronization
def sync_scroll(*args) -> None:
    """Synchronize scrolling between line numbers and code area"""
    try:
        # Ensure arguments are passed correctly
        if len(args) >= 2:
            first, last = args[0], args[1]
            line_numbers.configure(state="normal")
            line_numbers._textbox.yview_moveto(first)
            line_numbers.configure(state="disabled")
    except Exception as e:
        print(f"Scroll sync error: {e}")


def on_content_change(event=None) -> None:
    """Handle content changes and update line numbers more robustly"""
    # Use after method to prevent multiple rapid updates
    if hasattr(on_content_change, "timer_id"):
        try:
            window.after_cancel(on_content_change.timer_id)
        except:
            pass

    # Slightly increased delay to ensure full content update
    on_content_change.timer_id = window.after(100, update_line_numbers)


def toggle_sidebar(event=None) -> None:
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.pack_forget()
    else:
        # Re-pack the sidebar on the left side of the content frame
        sidebar_frame.pack(side=LEFT, fill=Y, before=main_content)
    sidebar_visible = not sidebar_visible


# -------------------- UI Setup --------------------
window: CTk = CTk()
window.title(f"{APP_NAME} : v{APP_VERSION}")
window.geometry("1200x720")
window.resizable(width=True, height=True)
window.iconbitmap("logo.ico")
status_var: StringVar = StringVar(value="Ready!")
language_var: StringVar = StringVar(value="Text File")

# Add the menu bar at the top
menu = CTkMenuBar(master=window)
file_menu: CTkButton = menu.add_cascade("File")
view_menu: CTkButton = menu.add_cascade("View")
help_menu: CTkButton = menu.add_cascade("Help")

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
appearance_submenu.add_option("Light", command=lambda: change_appearance_mode("Light"))
appearance_submenu.add_option("Dark", command=lambda: change_appearance_mode("Dark"))
appearance_submenu.add_option("System Theme", command=lambda: change_appearance_mode("System"))

help_dropdown: CustomDropdownMenu = CustomDropdownMenu(widget=help_menu)
help_dropdown.add_option(option="What's New?", command=whats_new_dialog)
help_dropdown.add_option(option="Keymap", command=keymap)
help_dropdown.add_option(option="About CodeX", command=about_codeX)

# Set up sidebar visibility control
sidebar_visible = True

view_dropdown.add_option(option="Toggle Sidebar", command=toggle_sidebar)

sidebar_frame = CTkFrame(content_frame, width=250)
sidebar_frame.pack(side=LEFT, fill=Y)

main_content = CTkFrame(content_frame)
main_content.pack(side=RIGHT, fill=BOTH, expand=True)

# Add tree to sidebar
tree = ttk.Treeview(sidebar_frame, show="tree")
tree.pack(fill=BOTH, expand=True)

tree.bind("<<TreeviewOpen>>", on_tree_expand)
tree.bind("<Double-1>", on_tree_double_click)

line_numbers = customtkinter.CTkTextbox(main_content, width=50)
line_numbers.configure(state="disabled")  # Prevent editing
line_numbers.configure(yscrollcommand=lambda *args: None)  # 🔥 Hides scrollbar
line_numbers.pack(side=LEFT, fill=Y)

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

# Modify existing bindings
code_area.bind("<KeyRelease>", on_content_change)
code_area.bind("<Return>", on_content_change)
code_area.bind("<BackSpace>", on_content_change)
code_area.bind("<Delete>", on_content_change)

# Reconfigure scrollbar to use our sync_scroll function
code_area.configure(yscrollcommand=lambda *args: (sync_scroll(*args),
                                                  line_numbers.configure(yscrollcommand=lambda *args: None)))

# Keyboard shortcuts
window.bind("<Control-plus>", zoom_in_text)
window.bind("<Control-minus>", zoom_out_text)
window.bind("<Control-0>", reset_zoom_text)
window.bind("<Control-b>", toggle_sidebar)
window.bind("<Control-s>", save_file)
window.bind("<Control-Shift-S>", save_file_as)
window.bind("<Control-n>", create_new_file)
window.bind("<Control-o>", open_file_content)
window.bind("<Control-Shift-N>", create_new_project)
window.bind("<Control-Shift-O>", open_folder_as_project)
window.bind("<Control-k>", keymap)

window.bind("<F1>", about_codeX)
window.bind("<F2>", whats_new_dialog)

window.mainloop()
