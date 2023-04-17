from typing import List, Dict

class CNFConverter:
    def __init__(self, grammar: Dict[str, List[str]]):
        self.grammar = grammar
        self.cnf_grammar = self._convert_to_cnf()

    def _remove_unit_productions(self):
        new_grammar = {}
        for symbol in self.grammar:
            new_productions = []
            for production in self.grammar[symbol]:
                if len(production) == 1 and production[0] in self.grammar:
                    new_productions.extend(self.grammar[production[0]])
                else:
                    new_productions.append(production)
            new_grammar[symbol] = new_productions
        self.grammar = new_grammar

    def _eliminate_long_productions(self):
        for symbol in list(self.grammar):
            for production in self.grammar[symbol]:
                if len(production) > 2:
                    self.grammar[symbol].remove(production)
                    new_symbols = []
                    for character in production:
                        if character not in self.grammar:
                            new_symbol = 'X' + str(len(self.grammar))
                            self.grammar[new_symbol] = [character]
                            new_symbols.append(new_symbol)
                        else:
                            new_symbols.append(character)
                    self.grammar[symbol].append(''.join(new_symbols))

    def _remove_epsilon_productions(self):
        new_grammar = {}
        epsilon_symbols = set()
        for symbol in self.grammar:
            if "" in self.grammar[symbol]:
                epsilon_symbols.add(symbol)
        while epsilon_symbols:
            symbol = epsilon_symbols.pop()
            new_productions = []
            for production in self.grammar[symbol]:
                if production == "":
                    continue
                if symbol in production:
                    # generate new productions for each possible removal of the symbol
                    new_productions.extend(
                        [production.replace(symbol, "", 1)] + [production.replace(symbol, "", i) for i in
                                                               range(1, len(production))])
                else:
                    new_productions.append(production)
            new_productions = list(set(new_productions))
            new_grammar[symbol] = new_productions
            for s in new_grammar:
                if symbol in new_grammar[s]:
                    if all(x in new_grammar[s] for x in new_grammar[symbol]):
                        # if all the productions of the symbol are in the productions of s, add s to epsilon_symbols
                        epsilon_symbols.add(s)
            self.grammar = new_grammar

    def _convert_to_cnf(self):
        self._remove_unit_productions()
        self._eliminate_long_productions()
        new_grammar = {}
        for symbol in self.grammar:
            new_productions = []
            for production in self.grammar[symbol]:
                if len(production) == 2 and not any(c.islower() for c in production):
                    new_productions.append(production)
                elif len(production) == 1 and production.islower():
                    new_productions.append(production)
                elif len(production) == 1 and production.isupper():
                    pass
                else:
                    new_symbol = f'X{len(new_grammar)}'
                    new_grammar[new_symbol] = [production[-1]]
                    new_productions.append(production[:-1] + new_symbol)
            new_grammar[symbol] = new_productions
        return new_grammar



