# Lexer & Scanner
## Course: Formal Languages & Finite Automata
## Author: Nistor Stefan FAF-211





## Theory
    The term lexer comes from lexical analysis which, in turn, represents the process of extracting lexical tokens from a string of characters. There are several alternative names for the mechanism called lexer, for example tokenizer or scanner. The lexical analysis is one of the first stages used in a compiler/interpreter when dealing with programming, markup or other types of languages.     The tokens are identified based on some rules of the language and the products that the lexer gives are called lexemes. So basically the lexer is a stream of lexemes. Now in case it is not clear what's the difference between lexemes and tokens, there is a big one. The lexeme is just the byproduct of splitting based on delimiters, for example spaces, but the tokens give names or categories to each lexeme. So the tokens don't retain necessarily the actual value of the lexeme, but rather the type of it and maybe some metadata.

## Objectives:
- Understand what lexical analysis [1] is.

- Get familiar with the inner workings of a lexer/scanner/tokenizer.

- Implement a sample lexer and show how it works.
  

## Implementation description
### Lexer class
This code defines a lexer class that takes a set of production rules as input and extracts the terminal symbols from them. It provides a tokenize method that takes an input string and produces a list of tokens, where each token is a tuple consisting of a type ('TERMINAL' for lowercase letters and 'NON_TERMINAL' for uppercase letters) and the actual symbol. The tokenize method loops over the input string, identifies each character as a terminal or non-terminal symbol based on whether it is a lowercase or uppercase letter, respectively, and adds it to the list of tokens. If the character is neither a lowercase nor an uppercase letter, the input is invalid and an exception is raised.

```python
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
                    token = (token_type, match.group(0))
                    self.tokens.append(token)
                    input_string = input_string[len(token[1]):]
                    break
            if not matched:
                raise ValueError(f"Invalid token: {input_string}")
        return self.tokens

```
### Tokenize method
The tokenize method starts with an empty list of tokens, then repeatedly attempts to match the input string with either the terminal or non-terminal token patterns.
If a match with the terminal token pattern is found, a token tuple is created with the label "TERMINAL" and the matched value as its second element, and then the token is appended to the list of tokens. The input string is then truncated by the length of the matched string to remove the token that has been processed.
If a match with the non-terminal token pattern is found, a token tuple is created with the label "NON-TERMINAL" and the matched value as its second element, and then the token is appended to the list of tokens. The input string is truncated by the length of the matched string to remove the non-terminal symbol that has been processed.
If neither pattern matches, the method raises a ValueError with a message indicating that the input string contains an invalid token.
The method continues this process until the input string is fully consumed, at which point it returns the list of tokens.
```python
     def tokenize(self, input_string):
        while len(input_string) > 0:
            matched = False
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(input_string)
                if match:
                    matched = True
                    token = (token_type, match.group(0))
                    self.tokens.append(token)
                    input_string = input_string[len(token[1]):]
                    break
            if not matched:
                raise ValueError(f"Invalid token: {input_string}")
        return self.tokens
```
### Main
The Main class imports the Lexer class from the lexer module and creates an instance of the Lexer class by calling its constructor with no arguments. It then calls the tokenize method of the lexer instance with the input string "2 + 3 * (4 - 1)". This method breaks the input string down into a list of tokens and returns it. Finally, the resulting list of tokens is printed to the console using the print function. The output shows that the input string has been correctly tokenized into individual tokens, including numbers, operators, and parentheses. The message "input valid" is also printed to the console, indicating that the input string was successfully tokenized without any errors.
```python
from lexer import Lexer
class Main:
    lexer = Lexer()
    tokens = lexer.tokenize("2 + 3 * (4 - 1)")
    print(tokens)
    print('input valid')
```



## Results
[('NUMBER', '2'), ('WHITESPACE', ' '), ('PLUS', '+'), ('WHITESPACE', ' '), ('NUMBER', '3'), ('WHITESPACE', ' '), ('MULTIPLY', '*'), ('WHITESPACE', ' '), ('LPAREN', '('), ('NUMBER', '4'), ('WHITESPACE', ' '), ('MINUS', '-'), ('WHITESPACE', ' '), ('NUMBER', '1'), ('RPAREN', ')')]

input valid
## Conclusions
In this project, we implemented a lexer  using regular expressions in Python. The lexer is responsible for tokenizing an input string and identifying the terminal and non-terminal symbols present in it based on a set of production rules.  The  lexer is an important tool in programming language processing and it can be used for tasks such as syntax highlighting, code completion, and program analysis. Overall, this project provides a good foundation for understanding and implementing lexers and scanners in Python.