from pygments.lexers import get_lexer_by_name

def get_lexer_for_language(language: str):
    """Get the appropriate lexer for a given language"""
    language_map = {
        "Python": "python",
        "HTML": "html",
        "CSS": "css",
        "JavaScript": "javascript",
        "JSON": "json",
        "XML": "xml",
        "C": "c",
        "C++": "cpp",
        "Java": "java",
        "PHP": "php",
        "Ruby": "ruby",
        "SQL": "sql",
        "YAML": "yaml",
        "Markdown": "markdown",
    }

    lexer_name = language_map.get(language)
    if lexer_name:
        try:
            return get_lexer_by_name(lexer_name)
        except:
            pass

    # Default to no highlighting for unsupported languages
    return None