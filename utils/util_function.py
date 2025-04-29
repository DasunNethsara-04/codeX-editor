def get_file_extension(filename: str) -> str|None:
    if filename:
        extension: str = filename.split('.')[-1]
        return extension
    return None

def check_file_type(filename: str) -> str:
    extension:str = get_file_extension(filename)
    type: str|None = None
    if extension == 'txt':
        type = 'Text File'
    elif extension == 'py':
        type = 'Python File'
    elif extension == 'html':
        type = 'HTML File'
    elif extension == 'css':
        type = 'CSS File'
    elif extension == 'js':
        type = 'JavaScript File'
    return type
