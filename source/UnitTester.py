import unittest
from ChomskyConverter import CNFConverter

class UnitTester(unittest.TestCase):
    def test_cnf_conversion_grammar1(self):
        grammar = {
            'S': ['aA', 'aB'],
            'A': ['bS'],
            'B': ['aC'],
            'C': ['a', 'bS']
        }

        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()

        expected_cnf_grammar = {
            'S': ['XS0A', 'XS0B'],
            'A': ['XA0S'],
            'B': ['XB0C'],
            'C': ['A0', 'XC0S'],
            'A0': ['a'],
            'B0': ['b'],
            'XS0': ['A0'],
            'XA0': ['B0'],
            'XB0': ['A0'],
            'XC0': ['B0']
        }

        self.assertEqual(cnf_grammar, expected_cnf_grammar)

    def test_cnf_conversion_grammar2(self):
        grammar = {
            'S': ['aAB', 'bBA'],
            'A': ['a', 'aA'],
            'B': ['b', 'bB']
        }

        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()

        expected_cnf_grammar = {
            'S': ['XS1B', 'XS1A'],
            'A': ['A0', 'XA0A'],
            'B': ['B0', 'XB0B'],
            'A0': ['a'],
            'B0': ['b'],
            'XS0': ['B0'],
            'XS1': ['XS0B'],
            'XA0': ['A0'],
            'XB0': ['B0']
        }

        # Sort the productions for each non-terminal in both grammars
        for nt in cnf_grammar:
            cnf_grammar[nt].sort()
        for nt in expected_cnf_grammar:
            expected_cnf_grammar[nt].sort()

        self.assertEqual(cnf_grammar, expected_cnf_grammar)

    def test_cnf_conversion_grammar3(self):
        grammar = {
            'S': ['AB'],
            'A': ['aAA', 'a'],
            'B': ['b', 'bB']
        }

        cnf_converter = CNFConverter(grammar)
        cnf_grammar = cnf_converter.convert_to_cnf()

        expected_cnf_grammar = {
            'S': ['AB'],
            'A': ['XA1A', 'A0'],
            'B': ['B0', 'XB0B'],
            'A0': ['a'],
            'B0': ['b'],
            'XA0': ['A0'],
            'XA1': ['XA0A'],
            'XB0': ['B0']
        }

        self.assertEqual(cnf_grammar, expected_cnf_grammar)