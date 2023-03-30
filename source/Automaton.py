import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
class Automaton:
    def __init__(self):
        # Initializes the attributes of the automaton object
        self.states = {'q0', 'q1', 'q2', 'q3'}  # Set of states
        self.alphabet = {'a', 'b', 'c'}  # Set of input symbols
        self.start_state = 'q0'  # The start state
        self.accept_states = {'q3'}  # Set of accept states
        self.transitions = {
            ('q0', 'a'): {'q0', 'q1'},
            ('q1', 'b'): {'q2'},
            ('q2', 'a'): {'q2'},
            ('q3', 'a'): {'q3'},
            ('q2', 'b'): {'q3'}
        }  # Dictionary of transition function mappings

    def is_deterministic(self):
        # Checks if the automaton is deterministic
        for state in self.states:
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), set())
                if len(next_states) != 1:
                    return False
        return True

    def to_dfa(self):
        # Converts the automaton to a deterministic finite automaton (DFA)
        if self.is_deterministic():
            return self

        dfa_states = set()
        dfa_accept_states = set()
        dfa_transitions = dict()
        state_queue = [frozenset([self.start_state])]
        while state_queue:
            current_states = state_queue.pop(0)
            dfa_states.add(current_states)
            if any(state in self.accept_states for state in current_states):
                dfa_accept_states.add(current_states)
            for symbol in self.alphabet:
                next_states = set()
                for state in current_states:
                    next_states |= set(self.transitions.get((state, symbol), set()))
                if next_states:
                    next_states = frozenset(next_states)
                    dfa_transitions[(current_states, symbol)] = next_states
                    if next_states not in dfa_states:
                        state_queue.append(next_states)

        dfa = Automaton()
        dfa.states = dfa_states
        dfa.accept_states = dfa_accept_states
        dfa.transitions = dfa_transitions
        return dfa

    def to_grammar(self):
        # Initialize an empty dictionary to hold the productions
        productions = dict()

        # For each state and symbol in the automaton's transitions,
        # create a production for each possible next state.
        for state in self.states:
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), set())
                for next_state in next_states:
                    if next_state in self.accept_states:
                        # If the next state is an accept state, add a production
                        # that generates the symbol for the current state.
                        if state not in productions:
                            productions[state] = set()
                        productions[state].add(symbol)
                    else:
                        # If the next state is not an accept state, add a production
                        # that generates the symbol concatenated with the next state.
                        if next_state not in productions:
                            productions[next_state] = set()
                        productions[next_state].add(symbol + state)

        # Set the start symbol to be the start state of the automaton.
        start_symbol = self.start_state
        if start_symbol in productions:
            # If there is already a production for the start symbol, rename it to "S"
            # and add new productions that use "S" instead of the start symbol.
            productions['S'] = productions[start_symbol]
            del productions[start_symbol]
            for state in self.states:
                for symbol in self.alphabet:
                    next_states = self.transitions.get((state, symbol), set())
                    for next_state in next_states:
                        if state in productions and symbol + state in productions[state]:
                            if next_state not in productions:
                                productions[next_state] = set()
                            productions[next_state].add(symbol + 'S')
        else:
            # If there is no production for the start symbol, create one that generates
            # the empty string and concatenates it with each accept state.
            start_symbol = 'S'
            productions[start_symbol] = set()
            for accept_state in self.accept_states:
                productions[start_symbol].add('eps' + accept_state)

        # Return the start symbol and the productions.
        return start_symbol, productions

    def render(self):
        # Create a directed graph using networkx
        G = nx.DiGraph()

        # Add nodes to the graph
        for state in self.states:
            G.add_node(state, shape='circle')
        G.nodes[self.start_state]['shape'] = 'doublecircle'
        for state in self.accept_states:
            G.nodes[state]['peripheries'] = 2

        # Add edges to the graph
        for (from_state, symbol), to_states in self.transitions.items():
            for to_state in to_states:
                G.add_edge(from_state, to_state, label=symbol)

        # Set up positions for the nodes using networkx spring_layout
        pos = nx.spring_layout(G, seed=42)

        # Draw the graph using matplotlib
        nx.draw_networkx_nodes(G, pos, node_size=1000, alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.8)
        nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif')
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=18, font_family='sans-serif')
        plt.axis('off')
        plt.show()


