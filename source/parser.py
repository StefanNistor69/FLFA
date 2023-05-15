

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token_index = 0

    def parse(self, input_string):
        self.tokens = self.lexer.tokenize(input_string)
        self.current_token_index = 0
        return self.parse_program()

    def consume_token(self):
        self.current_token_index += 1

    def current_token(self):
        return self.tokens[self.current_token_index]

    def parse_program(self):
        program = {
            'type': 'Program',
            'body': []
        }
        while self.current_token_index < len(self.tokens):
            statement = self.parse_statement()
            program['body'].append(statement)
        return program

    def parse_statement(self):
        token_type, _ = self.current_token()
        if token_type == 'VAR':
            return self.parse_variable_declaration()
        # Add other statement types here...
        else:
            raise ValueError(f"Unexpected token: {token_type}")

    def parse_variable_declaration(self):
        self.consume_token()  # Consume 'VAR'
        identifier = self.parse_identifier()
        self.consume_token()  # Consume 'ASSIGN'
        expression = self.parse_expression()
        self.consume_token()  # Consume 'SEMICOLON'

        return {
            'type': 'VariableDeclaration',
            'identifier': identifier,
            'expression': expression
        }

    def parse_identifier(self):
        token_type, token_value = self.current_token()
        if token_type == 'ID':
            self.consume_token()
            return {
                'type': 'Identifier',
                'name': token_value
            }
        else:
            raise ValueError(f"Unexpected token: {token_type}")

    def parse_expression(self):
        token_type, token_value = self.current_token()
        if token_type == 'NUMBER':
            self.consume_token()
            return {
                'type': 'NumericLiteral',
                'value': float(token_value)
            }
        else:
            raise ValueError(f"Unexpected token: {token_type}")