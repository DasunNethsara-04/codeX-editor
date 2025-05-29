# Language-specific keywords, functions, and methods
keywords: dict[str, list[str]] = {
    'python': [
        'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
        'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
        'while', 'with', 'yield', 'True', 'False', 'None',
    ],
    'javascript': [
        'break', 'case', 'catch', 'continue', 'debugger', 'default',
        'delete', 'do', 'else', 'finally', 'for', 'function', 'if',
        'in', 'instanceof', 'new', 'return', 'switch', 'this',
        'throw', 'try', 'typeof', 'var', 'void', 'while', 'with',
        'let', 'const', 'class', 'extends', 'super', 'async', 'await'
    ],
    'php': [
        'abstract', 'and', 'array', 'as', 'break', 'callable', 'case',
        'catch', 'class', 'clone', 'const', 'continue', 'declare',
        'default', 'die', 'do', 'echo', 'else', 'elseif', 'empty',
        'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch',
        'endwhile', 'eval', 'exit', 'extends', 'final', 'finally',
        'for', 'foreach', 'function', 'global', 'goto', 'if',
        'implements', 'include', 'include_once', 'instanceof',
        'insteadof', 'interface', 'isset', 'list', 'namespace',
        'new', 'or', 'print', 'private', 'protected', 'public',
        'require', 'require_once', 'return', 'static', 'switch',
        'throw', 'trait', 'try', 'unset', 'use', 'var', 'while',
        'xor', 'yield'
    ],
    'sql': [
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE',
        'CREATE', 'DROP', 'ALTER', 'TABLE', 'INDEX', 'VIEW',
        'DATABASE', 'SCHEMA', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES',
        'CONSTRAINT', 'NOT', 'NULL', 'UNIQUE', 'DEFAULT', 'CHECK',
        'AND', 'OR', 'IN', 'LIKE', 'BETWEEN', 'ORDER', 'BY',
        'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'JOIN', 'INNER',
        'LEFT', 'RIGHT', 'FULL', 'OUTER', 'UNION', 'DISTINCT', 'USE'
    ],
    'css': [
        'color', 'background', 'font', 'margin', 'padding', 'border',
        'width', 'height', 'display', 'position', 'top', 'left',
        'right', 'bottom', 'float', 'clear', 'text-align',
        'text-decoration', 'font-size', 'font-weight', 'line-height'
    ],
    'html': [
        'html', 'head', 'body', 'title', 'meta', 'link', 'script',
        'style', 'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5',
        'h6', 'a', 'img', 'ul', 'ol', 'li', 'table', 'tr', 'td',
        'th', 'form', 'input', 'button', 'select', 'option'
    ]
}

# Built-in functions and methods for each language
functions: dict[str, list[str]] = {
    'python': [
        # Built-in functions
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
        'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr',
        'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
        'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
        'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
        'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max',
        'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
        'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round',
        'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum',
        'super', 'tuple', 'type', 'vars', 'zip',
        # Common methods
        'append', 'extend', 'insert', 'remove', 'pop', 'clear', 'index',
        'count', 'sort', 'reverse', 'copy', 'keys', 'values', 'items',
        'get', 'update', 'split', 'join', 'replace', 'strip', 'lower',
        'upper', 'startswith', 'endswith', 'find', 'rfind',

        # dunder methods
        '__init__', '__name__', '__repr__', '__str__', '__dir__', '__class__', '__trunc__'
    ],
    'javascript': [
        # Built-in functions
        'alert', 'confirm', 'prompt', 'console', 'parseInt', 'parseFloat',
        'isNaN', 'isFinite', 'encodeURI', 'decodeURI', 'encodeURIComponent',
        'decodeURIComponent', 'eval', 'setTimeout', 'setInterval',
        'clearTimeout', 'clearInterval',
        # Array methods
        'push', 'pop', 'shift', 'unshift', 'slice', 'splice', 'concat',
        'join', 'reverse', 'sort', 'indexOf', 'lastIndexOf', 'forEach',
        'map', 'filter', 'reduce', 'find', 'findIndex', 'includes',
        'some', 'every',
        # String methods
        'charAt', 'charCodeAt', 'concat', 'indexOf', 'lastIndexOf',
        'slice', 'substring', 'substr', 'toLowerCase', 'toUpperCase',
        'trim', 'split', 'replace', 'match', 'search', 'startsWith',
        'endsWith', 'includes',
        # Object methods
        'hasOwnProperty', 'toString', 'valueOf'
    ],
    'php': [
        # Built-in functions
        'array', 'count', 'sizeof', 'is_array', 'in_array', 'array_key_exists',
        'array_keys', 'array_values', 'array_merge', 'array_push', 'array_pop',
        'array_shift', 'array_unshift', 'array_slice', 'array_splice',
        'implode', 'explode', 'str_replace', 'strlen', 'substr', 'strtolower',
        'strtoupper', 'trim', 'ltrim', 'rtrim', 'strpos', 'strrpos',
        'strcmp', 'strcasecmp', 'strstr', 'stristr', 'preg_match',
        'preg_replace', 'htmlspecialchars', 'htmlentities', 'strip_tags',
        'addslashes', 'stripslashes', 'json_encode', 'json_decode',
        'serialize', 'unserialize', 'md5', 'sha1', 'hash', 'rand',
        'mt_rand', 'date', 'time', 'mktime', 'strtotime', 'file_get_contents',
        'file_put_contents', 'fopen', 'fclose', 'fread', 'fwrite'
    ],
    'sql': [
        # Built-in functions
        'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'ROUND', 'CEIL', 'FLOOR',
        'ABS', 'POWER', 'SQRT', 'MOD', 'CONCAT', 'LENGTH', 'CHAR_LENGTH',
        'SUBSTRING', 'LEFT', 'RIGHT', 'LTRIM', 'RTRIM', 'TRIM', 'UPPER',
        'LOWER', 'REPLACE', 'REVERSE', 'NOW', 'CURDATE', 'CURTIME',
        'DATE', 'TIME', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE',
        'SECOND', 'DATEDIFF', 'DATE_ADD', 'DATE_SUB', 'IFNULL',
        'COALESCE', 'NULLIF', 'CASE', 'IF', 'CAST', 'CONVERT'
    ],
    'css': [
        # CSS functions
        'rgb', 'rgba', 'hsl', 'hsla', 'url', 'calc', 'var', 'linear-gradient',
        'radial-gradient', 'repeating-linear-gradient', 'repeating-radial-gradient',
        'rotate', 'scale', 'translate', 'skew', 'matrix', 'perspective',
        'cubic-bezier', 'steps', 'attr', 'counter', 'counters'
    ],
    'html': [
        # HTML events and attributes (commonly used)
        'onclick', 'onload', 'onmouseover', 'onmouseout', 'onchange',
        'onsubmit', 'onfocus', 'onblur', 'onkeydown', 'onkeyup',
        'class', 'id', 'style', 'src', 'href', 'alt', 'title',
        'width', 'height', 'type', 'name', 'value', 'placeholder'
    ]
}

# Get all suggestions for a language (keywords + functions)
def get_all_suggestions(language: str) -> list[str]:
    lang_keywords = keywords.get(language.lower(), [])
    lang_functions = functions.get(language.lower(), [])
    return lang_keywords + lang_functions

# Get only keywords for a language
def get_keywords(language: str) -> list[str]:
    return keywords.get(language.lower(), [])

# Get only functions for a language
def get_functions(language: str) -> list[str]:
    return functions.get(language.lower(), [])