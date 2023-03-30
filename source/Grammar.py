import random

class Grammars:
    def __init__(self, productions, start_symbol):
        # Initialize the class with a dictionary of productions and a start symbol
        self.productions = productions
        self.start_symbol = start_symbol

    def generate_string(self):
        # Generate a string from the start symbol using the internal recursive method
        return self._generate_string(self.start_symbol)

    def _generate_string(self, symbol):
        # If the current symbol is a terminal symbol, return it
        if symbol not in self.productions:
            return symbol
        # Otherwise, choose a random production for the current symbol and recursively generate a string from each symbol in the production
        production = random.choice(self.productions[symbol])
        return ''.join(self._generate_string(s) for s in production)


    def to_finite_automaton(self):
        # Initialize the finite automaton with a start state
        start_state = 0
        automatons = {start_state: {}}
        state_count = 1

        # Iterate over each symbol in the productions dictionary
        for symbol in self.productions:
            # Iterate over each production for the current symbol
            for production in self.productions[symbol]:
                current_state = start_state
                # For each symbol in the production, create a new state if necessary and add a transition to the finite automaton
                for s in production:
                    if s not in automatons[current_state]:
                        automatons[current_state][s] = state_count
                        automatons[state_count] = {}
                        state_count += 1
                    current_state = automatons[current_state][s]
                # Add an epsilon transition from the final state of the production to the start state of the finite automaton
                if current_state not in automatons:
                    automatons[current_state] = {}
                automatons[current_state][''] = start_state

        # Return the resulting finite automaton
        return automatons

    def chomsky_classification(self):
        # Check if each production in the grammar is in Chomsky normal form
        for symbol, productions in self.productions.items():
            for production in productions:
                # If the production is a single terminal symbol, it's in CNF
                if len(production) == 1 and production.islower():
                    continue
                # If the production is a pair of nonterminal symbols, it's in CNF
                elif len(production) == 2 and production.isupper():
                    continue
                # If the production is a single nonterminal symbol, it's not in CNF
                elif len(production) == 1 and production.isupper():
                    return "Type 0: Unrestricted Grammar"
                # If the production is not a pair of nonterminal symbols or a single terminal symbol, it's not in CNF
                elif len(production) != 2 or not production.isupper():
                    return "Type 1: Context-Sensitive Grammar"

        # Check if the start symbol has a production that only consists of the empty string
        if self.start_symbol in self.productions and 'ε' in self.productions[self.start_symbol]:
            # If there are any other productions for the start symbol, the grammar is not in CNF
            if len(self.productions[self.start_symbol]) > 1:
                return "Type 2: Context-Free Grammar"
            # If there are no other productions for the start symbol, the grammar is in CNF
            else:
                return "Type 3: Regular Grammar"
        # If the start symbol doesn't have a production that only consists of the empty string, the grammar is not in CNF
        else:
            return "Type 2: Context-Free Grammar"

