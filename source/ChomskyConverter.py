class CNFConverter:
    def __init__(self, grammar):
        self.grammar = grammar
        self.non_terminals = set(grammar.keys())
        self.terminals = self.get_terminals(grammar)

    def get_terminals(self, grammar):
        terminals = set()
        for rules in grammar.values():
            for rule in rules:
                for symbol in rule:
                    if symbol not in self.non_terminals:
                        terminals.add(symbol)
        return terminals

    def remove_null_productions(self):
        for key, rules in self.grammar.items():
            new_rules = [rule for rule in rules if rule != '']
            self.grammar[key] = new_rules

    def remove_unit_productions(self):
        for key, rules in self.grammar.items():
            new_rules = []
            for rule in rules:
                if len(rule) == 1 and rule in self.non_terminals:
                    new_rules.extend(self.grammar[rule])
                else:
                    new_rules.append(rule)
            self.grammar[key] = new_rules

    def replace_terminals_with_non_terminals(self):
        for key in list(self.grammar.keys()):  # Iterate over a copy of the keys
            rules = self.grammar[key]
            new_rules = []
            for rule in rules:
                new_rule = []
                for symbol in rule:
                    if symbol in self.terminals:
                        new_non_terminal = f'{symbol.upper()}0'
                        if new_non_terminal not in self.non_terminals:
                            self.non_terminals.add(new_non_terminal)
                            self.grammar[new_non_terminal] = [symbol]
                        new_rule.append(new_non_terminal)
                    else:
                        new_rule.append(symbol)
                new_rules.append(''.join(new_rule))
            self.grammar[key] = new_rules

    def split_long_productions(self):
        new_rules_to_add = {}

        for key in list(self.grammar.keys()):
            rules = self.grammar[key]
            new_rules = []

            for rule in rules:
                if len(rule) > 2:
                    new_non_terminals = [f'X{key}{i}' for i in range(len(rule) - 2)]
                    for new_non_terminal in new_non_terminals:
                        self.non_terminals.add(new_non_terminal)

                    new_rule = rule[0] + new_non_terminals[0]
                    new_rules_to_add[new_non_terminals[0]] = [rule[0:2]]

                    for i in range(1, len(new_non_terminals)):
                        new_rules_to_add[new_non_terminals[i]] = [new_non_terminals[i - 1] + rule[i + 1]]

                    new_rules.append(new_non_terminals[-1] + rule[-1])
                else:
                    new_rules.append(rule)

            self.grammar[key] = new_rules

        self.grammar.update(new_rules_to_add)

    def convert_to_cnf(self):
        self.remove_null_productions()
        self.remove_unit_productions()
        self.replace_terminals_with_non_terminals()
        self.split_long_productions()
        return self.grammar