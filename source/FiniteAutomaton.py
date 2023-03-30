class FiniteAutomaton:
    # Initializes the FiniteAutomaton class with an automaton dictionary as input.
    def __init__(self, automaton):
        # Assigns the set of values to the specified key in the automaton dictionary.
        self.states = automaton['states']

        self.alphabet = automaton['alphabet']

        self.transition = automaton['transition']

        self.start_state = automaton['start_state']

        self.final_states = automaton['final_states']

    # Checks if the given string is accepted by the finite automaton.
    def check_string(self, string):
        # Sets the current state to the start state of the automaton.
        current_state = self.start_state

        # Iterates over each symbol in the input string.
        for symbol in string:
            try:
                # Uses the transition function to determine the next state of the automaton.
                current_state = self.transition[current_state][symbol]
            except KeyError:
                # If there is no valid transition for the current state and input symbol, the string is rejected.
                return False

        # If the final state is in the set of final states, the string is accepted.
        return current_state in self.final_states

    # Checks a list of strings for acceptance by the finite automaton.
    def check_strings(self, strings):
        # Iterates over each string in the input list.
        for string in strings:
            if self.check_string(string):
                # If the string is accepted, prints a message indicating so.
                print(f'String "{string}" is accepted by the automaton.')
            else:
                # If the string is rejected, prints a message indicating so.
                print(f'String "{string}" is rejected by the automaton.')