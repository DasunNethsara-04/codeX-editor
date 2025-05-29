# Language-specific keywords and functions
keywords:  dict[str, list[str]] = {
    'python': [
        'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
        'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
        'while', 'with', 'yield', 'True', 'False', 'None',

        '__init__', '__name__', '__repr__', '__str__', '__dir__', '__class__', '__trunc__'
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
