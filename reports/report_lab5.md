# Parser & Building an Abstract Syntax Tree

## Course: Formal Languages & Finite Automata  
## Author: Nistor Stefan




## Theory

The process of gathering syntactical meaning or doing a syntactical analysis over some text can also be called parsing. It usually results in a parse tree which can also contain semantic information that could be used in subsequent stages of compilation, for example.

    Similarly to a parse tree, in order to represent the structure of an input text one could create an Abstract Syntax Tree (AST). This is a data structure that is organized hierarchically in abstraction layers that represent the constructs or entities that form up the initial text. These can come in handy also in the analysis of programs or some processes involved in compilation.
## Objectives

1. Get familiar with parsing, what it is and how it can be programmed [^1].
2. Get familiar with the concept of AST [^2].
3. In addition to what has been done in the 3rd lab work, do the following:
    1. In case you didn't have a type that denotes the possible types of tokens, you need to:
        1. Have a type TokenType (like an enum) that can be used in the lexical analysis to categorize the tokens.
        2. Please use regular expressions to identify the type of the token.
    2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
    3. Implement a simple parser program that could extract the syntactic information from the input text.


## Implementation description

### Constructor

The constructor takes a `lexer` as a parameter, which is responsible for breaking down the input into tokens.
```python
       def __init__(self, lexer):
    self.lexer = lexer
    self.tokens = []
    self.current_token_index = 0
```


### 'parse' method
The parse method takes an input_string as a parameter, tokenizes it using the lexer, and then constructs an AST from the tokens.

```python
       def parse(self, input_string):
    self.tokens = self.lexer.tokenize(input_string)
    self.current_token_index = 0
    return self.parse_program()

        
```
### 'consume_token' method

The consume_token method increments the current_token_index by 1, effectively moving the parser's focus to the next token in the sequence.
```python
  def consume_token(self):
    self.current_token_index += 1

```

### 'current_token' method

The current_token method returns the current token that the parser is looking at.
```python
       def current_token(self):
    return self.tokens[self.current_token_index]

```

### 'parse_program' method
The parse_program method initializes a new 'Program' node and then repeatedly calls parse_statement until all tokens have been consumed. Each statement is added to the 'Program' node's 'body'.
```python
        def parse_program(self):
    program = {
        'type': 'Program',
        'body': []
    }
    while self.current_token_index < len(self.tokens):
        statement = self.parse_statement()
        program['body'].append(statement)
    return program
```


### 'parse_statement' method
The parse_statement method switches on the type of the current token to decide which specific parsing method to call. For example, if the current token is a 'VAR', it calls parse_variable_declaration.
```python
     def parse_statement(self):
    token_type, _ = self.current_token()
    if token_type == 'VAR':
        return self.parse_variable_declaration()
    # Add other statement types here...
    else:
        raise ValueError(f"Unexpected token: {token_type}")

```


### 'parse_variable_declaration', 'parse_identifier', and 'parse_expression' methods
These methods are responsible for parsing specific parts of the input, such as variable declarations, identifiers, and expressions. They each construct and return an AST node corresponding to the part they're parsing.
```python
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


```
# Input:
```
var x = 5;
```
# Results:
```
{'type': 'Program', 'body': [{'type': 'VariableDeclaration', 'identifier': {'type': 'Identifier', 'name': 'x'}, 'expression': {'type': 'NumericLiteral', 'value': 5.0}}]}
```

# Conclusion

Parsing and the use of Abstract Syntax Trees (ASTs) are fundamental concepts in the field of compilers and interpreters, and they play a significant role in many areas of software development.

Parsing is the process of analyzing a string of symbols, either in natural language, computer languages or data structures, conforming to the rules of a formal grammar. In the context of computer languages, this involves the conversion of code into an intermediate representation that is easier for a computer to work with, such as tokens.

ASTs represent the syntactic structure of source code in a tree format, where each node of the tree denotes a construct occurring in the source code. The use of ASTs simplifies the process of manipulation and translation of source code, as it provides a high-level representation of the program structure, abstracting away from the textual details.

While the implementation and complexity of parsers and ASTs can vary greatly depending on the specific requirements of the language and the project, the core principles remain the same. Understanding these principles is crucial for anyone wishing to work in areas that involve code interpretation, such as developing new programming languages, building compilers or interpreters, or working on code analysis and refactoring tools.

In this era of growing reliance on technology and software, the importance of these concepts and their application in real-world situations continues to grow. Therefore, a thorough understanding of parsing and ASTs will continue to be an important asset for software developers and computer scientists.



