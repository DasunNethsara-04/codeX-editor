import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

from keywords import keywords

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, language=""):
        super().__init__(parent)
        self.language = language.lower()
        self.highlighting_rules = []
        self.setup_highlighting_rules()
        self.setup_function_highlighting(language)

    def setup_highlighting_rules(self):
        # Define formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(86, 156, 214))
        keyword_format.setFontWeight(QFont.Bold)

        string_format = QTextCharFormat()
        string_format.setForeground(QColor(206, 145, 120))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(106, 153, 85))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(220, 220, 170))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor(181, 206, 168))

        # Add keyword rules
        if self.language in keywords:
            for word in keywords[self.language]:
                pattern = r'\b' + word + r'\b'
                self.highlighting_rules.append((re.compile(pattern, re.IGNORECASE), keyword_format))

        # Add string rules
        if self.language in ['python', 'javascript', 'php']:
            self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
            self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))

        # Add comment rules
        if self.language == 'python':
            self.highlighting_rules.append((re.compile(r'#.*'), comment_format))
        elif self.language in ['javascript', 'php', 'css']:
            self.highlighting_rules.append((re.compile(r'//.*'), comment_format))
            self.highlighting_rules.append((re.compile(r'/\*.*?\*/'), comment_format))
        elif self.language == 'html':
            self.highlighting_rules.append((re.compile(r'<!--.*?-->'), comment_format))
        elif self.language == 'sql':
            self.highlighting_rules.append((re.compile(r'--.*'), comment_format))

        # Add number rules
        self.highlighting_rules.append((re.compile(r'\b\d+\.?\d*\b'), number_format))

        # Add function rules
        if self.language in ['python', 'javascript', 'php']:
            self.highlighting_rules.append((re.compile(r'\b\w+(?=\()'), function_format))

    def setup_function_highlighting(self, language):
        """Setup function highlighting with different color"""
        from keywords import get_functions
        functions_list = get_functions(language)

        # Create function highlighting format (e.g., blue color)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(0, 100, 200))  # Blue color
        function_format.setFontWeight(QFont.Weight.Bold)

        # Add function patterns
        for function in functions_list:
            pattern = rf'\b{re.escape(function)}\b'
            self.highlighting_rules.append((re.compile(pattern), function_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)
