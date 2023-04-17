import matplotlib.pyplot as plt
import networkx as nx
import unittest
from lexer import Lexer
from Automaton import Automaton
from FiniteAutomaton import FiniteAutomaton
from Grammar import Grammars
from ChomskyConverter import CNFConverter
from UnitTester import UnitTester
class Main:
    # Initialize the Main class by setting up a grammar,
    # converting it to a finite automaton, and setting up a FiniteAutomaton object
    def __init__(self):
        self.productions = {
            'S': ['aA', 'aB'],
            'A': ['bS'],
            'B': ['aC'],
            'C': ['a', 'bS'],
        }
        self.start_symbol = 'S'
        self.grammar = Grammars(self.productions, self.start_symbol)
        self.finite_automaton = self.grammar.to_finite_automaton()
        self.automaton = FiniteAutomaton

    # Generates strings from the grammar
    def generate_strings(self, num_strings):
        for i in range(num_strings):
            string = self.grammar.generate_string()
            print(string)

if __name__ == '__main__':
    # Create a Main object
    main = Main()

    # Generate and print 5 strings from the grammar
    main.generate_strings(5)

    # Convert the grammar to a finite automaton
    automatons = main.grammar.to_finite_automaton()

    # Define a finite automaton manually
    automaton = {
        'states': {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'},
        'alphabet': {'a', 'b'},
        'transition': {
            'q0': {'a': 'q1'},
            'q1': {'b': 'q2', 'a': 'q3'},
            'q2': {'a': 'q4'},
            'q3': {'a': 'q1', 'b': 'q5'},
            'q4': {'a': 'q5', 'b': 'q5'},
            'q5': {'a': 'q5', 'b': 'q5'}
        },
        'start_state': 'q0',
        'final_states': {'q5'}
    }

    # Create a FiniteAutomaton object for the manually-defined automaton
    checker = FiniteAutomaton(automaton)

    # Check whether a list of strings are accepted by the finite automaton
    checker.check_strings(['aaa', 'abaaa', 'ababaa', 'aa', 'abababa'])

    # Print the finite automaton
    print(automatons)

automation = Automaton()

automation.states = ['q0', 'q1', 'q2', 'q3']
automation.alphabet = ['a', 'b', 'c']
automation.transitions = {('q0', 'a'): ['q0', 'q1'],
                   ('q1', 'b'): ['q2'],
                   ('q2', 'a'): ['q2'],
                   ('q3', 'a'): ['q3'],
                   ('q2', 'b'): ['q3']}
automation.start_state = 'q0'
automation.accept_states = ['q3']
print('')
print('')
print('')
print('-------------------------------------------------------------------LAB2-------------------------------------------------------------------------')
# Check if automaton is deterministic
is_deterministic = automation.is_deterministic()
print(f"Is automaton deterministic? {is_deterministic}")

# Convert NDFA to DFA
dfa = automation.to_dfa()
print(f"DFA states: {dfa.states}")
print(f"DFA transition function: {dfa.transitions}")
print(f"DFA initial state: {dfa.start_state}")
print(f"DFA final states: {dfa.accept_states}")

# Convert automaton to regular grammar
grammar = automation.to_grammar()
print(f"Regular grammar productions: {grammar}")
print(main.grammar.chomsky_classification())
automation.render()
print('')
print('')
print('')
print('-------------------------------------------------------------------LAB3-------------------------------------------------------------------------')
lexer = Lexer()
tokens = lexer.tokenize("2 + 3 * (4 - 1)")
print(tokens)
print('input valid')
print('')
print('')
print('')
print('-------------------------------------------------------------------LAB4-------------------------------------------------------------------------')
VN = {'S', 'A', 'B', 'C', 'D'}
VI = {'a', 'b'}
P = [
    ('S', ('a', 'B')),
    ('S', ('b', 'A')),
    ('S', ('B',)),
    ('A', ('b',)),
    ('A', ('a', 'D')),
    ('A', ('A', 'S')),
    ('A', ('B', 'A', 'B')),
    ('A', ()),
    ('B', ('a',)),
    ('B', ('b', 'S')),
    ('C', ('A', 'B')),
    ('D', ('B', 'B'))
]
S = 'S'
grammar = (VN, VI, P, S)

# Convert the grammar to Chomsky normal form
cnf_converter = CNFConverter(grammar)
cnf_grammar = cnf_converter.convert_to_cnf()

# Print the resulting grammar
print('Original grammar:')
print(grammar)
print('Grammar in Chomsky normal form:')
print(cnf_grammar)

print("All Tests Passed")
unittest.main()



