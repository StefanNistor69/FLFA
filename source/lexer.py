import re


class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_patterns = [
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('COMMA', r','),
            ('ASSIGN', r'='),
            ('ADD', r'add\b'),
            ('SEMICOLON', r';'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('GREATER', r'>'),
            ('GREATER_EQUAL', r'>='),
            ('EQUAL', r'=='),
            ('LESS', r'<'),
            ('LESS_EQUAL', r'<='),
            ('NOT_EQUAL', r'!='),
            ('IF', r'if\b'),
            ('ELSE', r'else\b'),
            ('FOR', r'for\b'),
            ('WHILE', r'while\b'),
            ('IN', r'in\b'),
            ('RETURN', r'return\b'),
            ('BREAK', r'break\b'),
            ('CONTINUE', r'continue\b'),
            ('VAR', r'var\b'),
            ('FUNC', r'func\b'),
            ('ID', r'[a-zA-Z_]\w*'),
            ('NUMBER', r'\d+(\.\d+)?'),
            ('STRING', r'"[^"]*"'),
            ('WHITESPACE', r'\s+'),
            ('COMMENT', r'//.*'),
            ('INVALID', r'.')
        ]

    def tokenize(self, input_string):
        while len(input_string) > 0:
            matched = False
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(input_string)
                if match:
                    matched = True
                    if token_type not in ['WHITESPACE', 'COMMENT']:
                        token = (token_type, match.group(0))
                        self.tokens.append(token)
                    input_string = input_string[len(match.group(0)):]
                    break
            if not matched:
                raise ValueError(f"Invalid token: {input_string}")
        return self.tokens
