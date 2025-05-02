# CodeX - A Lightweight Python-Based Code Editor

## 🧩 Introduction

**CodeX** is a simple and modern text/code editor built with Python using the [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) library. It is designed to provide a minimal yet effective development environment with features like file navigation,  project management, and custom keybindings — all without the bulk of traditional IDEs.

---

## ⚙️ Specifications

- ✅ Built with **Python 3** and **CustomTkinter**
- 🗂️ Sidebar with a project/file tree viewer
- 💾 Create, open, save, and manage files or projects
- 🔍 Zoom in/out/reset code area
- 🎨 Theme customization (Light/Dark mode)
- 🖍️ Syntax highlighting for **HTML, CSS, JavaScript, Python** using Pygments (coming soon)
- 🔧 Toggle sidebar visibility for distraction-free writing

---

## ⌨️ Shortcut Keys

| Shortcut              | Action                            |
|-----------------------|-----------------------------------|
| `Ctrl + O`            | Open a file                       |
| `Ctrl + S`            | Save current file                 |
| `Ctrl + N`            | Create a new file                 |
| `Ctrl + M`            | Create a new project              |
| `Ctrl + B`            | Open a folder as a project        |
| `Ctrl + +`            | Zoom in the code area             |
| `Ctrl + -`            | Zoom out the code area            |
| `Ctrl + 0`            | Reset zoom in the code area       |

> 📝 Note: On macOS, use `Command` instead of `Control`.

---

## 🛠️ Development Setup

To set up CodeX locally for development:

### 1. Clone the Repository

```bash
git clone https://github.com/DasunNethsara-04/codeX-editor.git
cd codeX-editor
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Editor

```bash
python main.py
```

> 💡 Make sure you are using **Python 3.10+**

---

## 📌 Contributions

Pull requests, bug reports, and feature suggestions are welcome! If you find a problem or want to contribute, feel free to open an issue or fork the project.

---

## 📄 License

This project is open-source under the [Apache License](LICENSE).
