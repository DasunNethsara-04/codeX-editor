from pygments.token import Token, _TokenType

SYNTAX_COLORS:  dict[_TokenType, str] = {
    # Keywords - Pink/Purple
    Token.Keyword: "#C586C0",  # Pink/Purple
    Token.Keyword.Constant: "#569CD6",  # Blue
    Token.Keyword.Declaration: "#C586C0",
    Token.Keyword.Namespace: "#C586C0",
    Token.Keyword.Reserved: "#C586C0",
    Token.Keyword.Type: "#569CD6",  # Blue

    # Names - Classes, functions, etc.
    Token.Name.Class: "#4EC9B0",  # Teal
    Token.Name.Function: "#DCDCAA",  # Light yellow/gold
    Token.Name.Builtin: "#4FC1FF",  # Light blue
    Token.Name.Builtin.Pseudo: "#4FC1FF",
    Token.Name.Exception: "#4EC9B0",  # Teal
    Token.Name.Decorator: "#DCDCAA",  # Light yellow/gold

    # Strings - Warm orange
    Token.Literal.String: "#CE9178",  # Warm orange
    Token.Literal.String.Doc: "#6A9955",  # Green for docstrings
    Token.Literal.String.Double: "#CE9178",
    Token.Literal.String.Single: "#CE9178",
    Token.Literal.String.Backtick: "#CE9178",
    Token.Literal.String.Symbol: "#CE9178",

    # Numbers - Light green
    Token.Literal.Number: "#B5CEA8",  # Light green
    Token.Literal.Number.Float: "#B5CEA8",
    Token.Literal.Number.Integer: "#B5CEA8",
    Token.Literal.Number.Hex: "#B5CEA8",

    # Comments - Green
    Token.Comment: "#6A9955",  # Green
    Token.Comment.Single: "#6A9955",
    Token.Comment.Multiline: "#6A9955",

    # Operators and punctuation
    Token.Operator: "#D4D4D4",  # Light grey
    Token.Punctuation: "#D4D4D4",  # Light grey

    # Web-specific
    Token.Name.Tag: "#569CD6",  # Blue for HTML/XML tags
    Token.Name.Attribute: "#9CDCFE",  # Light blue for attributes

    # CSS specific
    Token.Name.Variable: "#9CDCFE",  # Light blue for variables
    Token.Name.Constant: "#4EC9B0",  # Teal for constants

    # Additional highlights for completeness
    Token.Name.Entity: "#DCDCAA",  # Light yellow for entities
    Token.Name.Label: "#C586C0",  # Pink for labels
    Token.Name.Namespace: "#4EC9B0",  # Teal for namespaces
    Token.Name.Property: "#9CDCFE",  # Light blue for properties

    # Literals
    Token.Literal: "#CE9178",  # Orange
    Token.Literal.Date: "#CE9178",  # Orange

    # Language specific highlights
    Token.Name.Variable.Class: "#9CDCFE",  # Light blue
    Token.Name.Variable.Global: "#9CDCFE",  # Light blue
    Token.Name.Variable.Instance: "#9CDCFE",  # Light blue

    # Error highlighting
    Token.Error: "#F14C4C",  # Red
    Token.Generic.Error: "#F14C4C",  # Red
}