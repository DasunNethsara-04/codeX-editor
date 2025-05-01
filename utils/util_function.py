import os


def get_file_extension(filename: str) -> str | None:
    if filename:
        extension: str = filename.split('.')[-1]
        return extension
    return None


def check_file_type(filename: str) -> str:
    extension: str = get_file_extension(filename)
    file_type: str | None = None
    if extension == 'txt':
        file_type = 'Text File'
    elif extension == 'py':
        file_type = 'Python File'
    elif extension == 'html':
        file_type = 'HTML File'
    elif extension == 'css':
        file_type = 'CSS File'
    elif extension == 'js':
        file_type = 'JavaScript File'
    return file_type


def create_project_files(project_type: str, full_path: str, project_name: str) -> tuple[bool, Exception] | bool:
    try:
        os.makedirs(full_path, exist_ok=True)
        # create project template folders based on type
        if project_type == "Web":
            os.makedirs(os.path.join(full_path, "styles"), exist_ok=True)
            os.makedirs(os.path.join(full_path, "scripts"), exist_ok=True)
            os.makedirs(os.path.join(full_path, "images"), exist_ok=True)

            # create required files
            # main entry point of the web (index.html)
            with open(os.path.join(full_path, 'index.html'), 'w') as f:
                f.write("<html>\n\t<head>\n\t\t<title>Document</title>\n\t\t<link rel='stylesheet' href='styles/style.css' type='text/css'>\n\t</head>\n\n\t<body>\n\t\t<h1>Hello World</h1>\n\n\t\t<script src='scripts/main.js'></script>\n\t</body>\n</html>")

            # main styling code
            with open(os.path.join(full_path, 'styles\\style.css'), 'w') as f:
                f.write("* {\n\tpadding: 0;\n\tmargin: 0;\n}")

            # main javascript code
            with open(os.path.join(full_path, 'scripts\\main.js'), 'w') as f:
                f.write("// your JavaScript code here")

            # README file
            with open(os.path.join(full_path, 'README.md'), 'w') as f:
                f.write(f"# Project Name: {project_name}")
        elif project_type == "Python":
            # main entry point of the Python application
            with open(os.path.join(full_path, "main.py"), "w") as f:
                f.write("def main() -> None:\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()")

            # requirements.txt file for 3rd party modules or libraries
            with open(os.path.join(full_path, "requirements.txt"), "w") as f:
                f.write('')

            # README file
            with open(os.path.join(full_path, 'README.md'), 'w') as f:
                f.write(f"# Project Name: {project_name}")

        return True
    except Exception as e:
        return False, e
