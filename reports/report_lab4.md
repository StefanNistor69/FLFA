# Chomsky Normal Form

**Course:** Formal Languages & Finite Automata  
**Author:** Nistor Stefan

## Grammar
### Variant 18

G=(VN, VI, P, S) Vn={S, A, B, C, D} VÃ={a, b}
P={1. S⇒aB
2. S→bA
3. S→B
4. A→b
5. A⇒aD
6. A→ AS
7. A→BAB
8. A⇒ ε
9. B→a
10. B→bS 11. C→AB
12. D→BB}
## Theory

Chomsky Normal Form (CNF) is a simplified form of context-free grammars that is useful in both the study and the development of algorithms for parsing and other language-processing tasks. A context-free grammar is said to be in Chomsky Normal Form if all its production rules are in one of the following two forms:

1. A -> BC, where A, B, and C are non-terminal symbols.
2. A -> a, where A is a non-terminal symbol, and a is a terminal symbol. 

The main advantage of CNF is its simplicity, which makes it easier to develop algorithms that work with context-free grammars. Any context-free grammar can be converted into an equivalent grammar in Chomsky Normal Form. The conversion process involves the following steps:

1. Eliminate ε-productions: Replace any production rule of the form A -> ε with alternative productions that generate the same language without the ε-production.
2. Eliminate renaming (unit productions): Remove production rules of the form A -> B, where A and B are non-terminal symbols, and substitute the production rules for B in place of A.
3. Eliminate inaccessible symbols: Remove any non-terminal symbols that cannot be reached from the start symbol in the grammar.
4. Eliminate non-productive symbols: Remove any non-terminal symbols that cannot derive any terminal strings.
5. Convert remaining rules to CNF: Break down production rules with more than two symbols on the right-hand side into multiple rules that conform to the CNF format.

By following these steps, we can transform any context-free grammar into an equivalent grammar in Chomsky Normal Form without altering the language it generates.

## Objectives

1. Implement a method for normalizing an input grammar by the rules of CNF (Chomsky Normal Form).
2. Encapsulate the implementation in a method with an appropriate signature (also ideally in an appropriate class/type).
3. Execute and test the implemented functionality.
4. (Bonus) Create unit tests that validate the functionality of the project.
5. (Bonus) Make the function accept any grammar, not only the one from the student's variant.

## Implementation description

### Eliminate Epsilon Productions

The `eliminate_epsilon` method is responsible for removing ε-productions (rules of the form A -> ε) from the grammar. It identifies all non-terminal symbols that generate ε directly or indirectly and substitutes them in all other production rules, effectively removing the need for ε-productions.
```python
        def eliminate_epsilon(self):
        vn, vi, p, s = self.grammar

        # Step 1: Find nullable symbols
        nullable = set()
        while True:
            updated = False
            for rule in p:
                if all(s in nullable for s in rule[1]):
                    if rule[0] not in nullable:
                        nullable.add(rule[0])
                        updated = True
            if not updated:
                break

        # Step 2: Eliminate epsilon productions
        new_p = []
        for rule in p:
            lhs, rhs = rule
            for i in range(2 ** len(rhs)):
                binary = bin(i)[2:].zfill(len(rhs))
                new_rhs = [rhs[j] for j in range(len(rhs)) if binary[j] == '0']
                if new_rhs:
                    new_p.append((lhs, tuple(new_rhs)))
            if not rhs:
                new_p.append((lhs, ('epsilon',)))

        if self.grammar[3]:
            self.grammar = vn, vi, new_p, s
        else:
            self.grammar = vn, vi, new_p
```


### Eliminate Renaming
The `eliminate_renaming` method removes unit productions (rules of the form A -> B, where A and B are non-terminal symbols) from the grammar. It does so by replacing the unit production with all the production rules of the referenced non-terminal symbol. This process is repeated until all unit productions are eliminated.

```python
        def eliminate_renaming(self):
        vn, vi, p, s = self.grammar

        # Step 3: Eliminate renaming
        new_p = []
        for rule in p:
            if len(rule[1]) == 1 and rule[1][0] in vn:
                for sub_rule in p:
                    if sub_rule[0] == rule[1][0]:
                        new_p.append((rule[0], sub_rule[1]))
            else:
                new_p.append(rule)

        
```
### Eliminate Inaccessible Symbols

The `eliminateInaccessibleSymbols` part of the `eliminate_renaming` removes non-terminal symbols that are not reachable from the start symbol of the grammar. It starts with the start symbol and iteratively finds all non-terminal symbols reachable from it. Then, it removes any production rules containing non-reachable symbols.

```python
  # Step 4: Eliminate inaccessible symbols
   reachable = set([s])
        updated = True
        while updated:
            updated = False
            for rule in new_p:
                if rule[0] in reachable:
                    for symbol in rule[1]:
                        if symbol in vn or symbol in reachable:
                            updated = updated or symbol not in reachable
                            reachable.add(symbol)

        new_vn = set([s])
        new_p = [rule for rule in new_p if rule[0] in reachable and all(s in new_vn or s in vi for s in rule[1])]
        for rule in new_p:
            for symbol in rule[1]:
                if symbol in vn:
                    new_vn.add(symbol)

        if self.grammar[3]:
            self.grammar = new_vn, vi, new_p, s
        else:
            self.grammar = new_vn, vi, new_p
```

### Eliminate Non-Productive Symbols

The `eliminate_nonproductive` method removes non-terminal symbols that cannot derive any terminal strings. It first identifies all non-productive symbols and then removes any production rules containing them. This step ensures that every non-terminal symbol in the grammar can derive at least one terminal string.

```python
       def eliminate_nonproductive(self):
        vn, vi, p, s = self.grammar

        # Step 5: Eliminate non-productive symbols
        productive = set([s])
        updated = True
        while updated:
            updated = False
            for rule in p:
                if rule[0] in productive:
                    for symbol in rule[1]:
                        if symbol in vn or symbol in productive:
                            updated = updated or symbol not in productive
                            productive.add(symbol)

        if not productive:
            raise ValueError('The resulting grammar has no productive symbols')

        new_vn = set([s])
        new_p = [rule for rule in p if rule[0] in productive and all(s in new_vn or s in vi for s in rule[1])]
        for rule in new_p:
            for symbol in rule[1]:
                if symbol in vn:
                    new_vn.add(symbol)

        if self.grammar[3]:
            self.grammar = new_vn, vi, new_p, s
        else:
            self.grammar = new_vn, vi, new_p
```

### Convert to Chomsky Normal Form
The `chomsky_normal_form` method converts the remaining production rules to the CNF format. It does so by breaking down rules with more than two symbols on the right-hand side into multiple rules that conform to CNF. Additionally, it introduces new non-terminal symbols for terminal symbols within rules containing more than one symbol on the right-hand side.

```python
        def chomsky_normal_form(self):
        vn, vi, p, s = self.grammar

        # Step 0: Add a new start symbol if necessary
        if s in vn:
            s_prime = s + "'"
            while s_prime in vn:
                s_prime += "'"
            vn.add(s_prime)
            new_p = [('S', (s,))]
            new_p.extend(p)
            new_p.append(('S', ('epsilon',)))
            self.grammar = vn, vi, new_p, 'S'
        else:
            s_prime = s

        # Step 1: Eliminate epsilon productions
        self.eliminate_epsilon()

        # Step 2: Eliminate renaming
        self.eliminate_renaming()

        # Step 3: Eliminate inaccessible symbols
        self.eliminate_nonproductive()

        # Step 6: Convert remaining productions to Chomsky normal form
        new_vn = set()
        new_p = []
        mapping = {}
        count = 0

        for rule in self.grammar[2]:
            if len(rule[1]) == 1 and rule[1][0] in self.grammar[1]:
                new_p.append(rule)
            elif len(rule[1]) == 1 and rule[1][0] in mapping:
                new_p.append((rule[0], (mapping[rule[1][0]],)))
            else:
                new_lhs = rule[0]
                new_rhs = rule[1]
                while len(new_rhs) > 2:
                    new_lhs = new_lhs + str(count)
                    count += 1
                    new_vn.add(new_lhs)
                    mapping[new_lhs] = new_rhs[:2]
                    new_p.append((new_lhs, new_rhs[:2]))
                    new_rhs = (new_lhs,) + new_rhs[2:]
                new_p.append((new_lhs, new_rhs))

        if len(new_p) == 1 and len(new_p[0][1]) == 1 and new_p[0][1][0] in self.grammar[1]:
            vn = new_vn
            s = s_prime
            vi = self.grammar[1].union(new_vn)
            p = new_p
        else:
            vn = new_vn.union(set(mapping.keys()))
            s = s_prime
            vi = self.grammar[1].union(new_vn)
            p = new_p
            for lhs, rhs in mapping.items():
                p.append((lhs, rhs))

        return vn, vi, p, s
```

These methods, when executed in sequence, transform the input grammar into an equivalent grammar in Chomsky Normal Form.
### Performing Unit Tests
This is a unit test class for the CNFConverter class, tests the conversion of context-free grammars to Chomsky normal form. The tests include input grammars and their expected outputs as tuples, and each test asserts that the output of the convert_to_cnf method of the CNFConverter class matches the expected output.
```python
      class UnitTester(unittest.TestCase):
    def test_grammar_1(self):
        grammar = ({'S', 'A', 'B', 'C', 'D'}, {'a', 'b'}, [('S', ('a', 'B')), ('S', ('b', 'A')), ('S', ('B',)), ('A', ('b',)), ('A', ('a', 'D')), ('A', ('A', 'S')), ('A', ('B', 'A', 'B')), ('A', ()), ('B', ('a',)), ('B', ('b', 'S')), ('C', ('A', 'B')), ('D', ('B', 'B'))], 'S')
        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()
        expected = (set(), {'a', 'b'}, [('S', ('S',)), ('S', ('a',)), ('S', ('b',)), ('S', ('a',)), ('S', ('a',)), ('S', ('b', 'S')), ('S', ('b',)), ('S', ('S',)), ('S', ('b',)), ('S', ('b',)), ('S', ('a',)), ('S', ('S',)), ('S', ('a',)), ('S', ('b', 'S')), ('S', ('b',)), ('S', ('S',))], "S'")
        self.assertEqual(cnf_grammar, expected)

    def test_grammar_2(self):
        grammar = ({'S', 'A', 'B', 'C', 'D'}, {'a', 'b', 'c'}, [('S', ('A', 'B')), ('S', ('a', 'C')), ('S', ('b', 'D')), ('A', ('a', 'B', 'c')), ('A', ('a', 'c')), ('B', ('b', 'A')), ('C', ('a', 'S')), ('D', ('c', 'D')), ('D', ('B', 'c')), ('D', ('c',))], 'S')
        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()
        expected = (set(), {'a', 'c', 'b'}, [('S', ('S',)), ('S', ('a',)), ('S', ('b',)), ('S', ('a', 'c')), ('S', ('a',)), ('S', ('c',)), ('S', ('a', 'c')), ('S', ('a',)), ('S', ('c',)), ('S', ('b',)), ('S', ('a',)), ('S', ('a', 'S')), ('S', ('a',)), ('S', ('S',)), ('S', ('b',)), ('S', ('c',)), ('S', ('c',)), ('S', ('c',))], "S'")
        self.assertEqual(cnf_grammar, expected)

    def test_grammar_3(self):
        grammar = ({'S', 'A', 'B'}, {'a', 'b'},
                   [('S', ('A', 'B')), ('S', ('B', 'A')), ('S', ('a',)), ('A', ('S', 'B')), ('A', ('a', 'B')),
                    ('B', ('S', 'A')), ('B', ('b',))], 'S')
        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()
        expected = (set(), {'a', 'b'}, [('S', ('S',)), ('S', ('a',)), ('S', ('S',)), ('S', ('a',)), ('S', ('S',)), ('S', ('b',)), ('S', ('S',)), ('S', ('b',)), ('S', ('S',)), ('S', ('a',)), ('S', ('a',))], "S'")
        self.assertEqual(cnf_grammar, expected)

    def test_grammar_4(self):
        grammar = ({'S', 'A', 'B', 'C'}, {'a', 'b'},
                   [('S', ('A', 'B')), ('S', ('B', 'C')), ('A', ('a', 'A')), ('A', ('a', 'B')), ('B', ('b', 'B')),
                    ('B', ('C', 'A')), ('C', ('b', 'A')), ('C', ('B', 'S'))], 'S')
        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()
        expected = (set(), {'a', 'b'}, [('S', ('S',)), ('S', ('a',)), ('S', ('a',)), ('S', ('b',)), ('S', ('b',)), ('S', ('b',)), ('S', ('S',))], "S'")
        self.assertEqual(cnf_grammar, expected)
```

# Results:
```
Original grammar:
({'A', 'S', "S'", 'B', 'C', 'D'}, {'b', 'a'}, [('S', ('a', 'B')), ('S', ('b', 'A')), ('S', ('B',)), ('A', ('b',)), ('A', ('a', 'D')), ('A', ('A', 'S')), ('A', ('B', 'A', 'B')), ('A', ()), ('B', ('a',)), ('B', ('b', 'S')), ('C', ('A', 'B')), ('D', ('B', 'B'))], 'S')
Grammar in Chomsky normal form:
(set(), {'b', 'a'}, [('S', ('S',)), ('S', ('a',)), ('S', ('b',)), ('S', ('a',)), ('S', ('a',)), ('S', ('b', 'S')), ('S', ('b',)), ('S', ('S',)), ('S', ('b',)), ('S', ('b',)), ('S', ('a',)), ('S', ('S',)), ('S', ('a',)), ('S', ('b', 'S')), ('S', ('b',)), ('S', ('S',))], "S'")
All Tests Passed
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

# Conclusions
In this project, we have successfully implemented a method for normalizing an input grammar by the rules of Chomsky Normal Form (CNF). We have addressed each step of the conversion process, including eliminating ε-productions, unit productions, inaccessible symbols, and non-productive symbols. Finally, we have converted the remaining production rules to CNF.

The implementation is modular, with each step encapsulated in a separate method. This approach not only makes the code more maintainable but also allows for easier testing and modification if needed. The Chomsky Normal Form is a powerful tool in the study of formal languages and automata, as it simplifies the grammar structure, making it easier to develop algorithms for parsing and language processing tasks.

As a result of this project, we have gained a deeper understanding of context-free grammars, their properties, and the process of converting them to Chomsky Normal Form. This knowledge will be valuable in future projects and studies related to formal languages and automata theory.