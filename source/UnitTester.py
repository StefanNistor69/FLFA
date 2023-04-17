import unittest
from ChomskyConverter import CNFConverter


class TestCNFConverter(unittest.TestCase):
    def test_conversion(self):
        grammar = {
            'S': ['aA', 'aB'],
            'A': ['bS'],
            'B': ['aC'],
            'C': ['a', 'bS']
        }
        converter = CNFConverter(grammar)
        expected_cnf_grammar = {
            'S': ['X0A', 'X1B'],
            'A': ['bS', 'aAa', 'aBa', 'aCa'],
            'B': ['aC', 'aBa', 'aBb', 'aCb'],
            'C': ['a', 'bS', 'aCa', 'aCb', 'bSa', 'bSb']
        }
        self.assertEqual(converter.cnf_grammar, expected_cnf_grammar)

    def test_unit_productions(self):
        grammar = {
            'S': ['aA'],
            'A': ['bB'],
            'B': ['cC'],
            'C': ['d']
        }
        converter = CNFConverter(grammar)
        expected_cnf_grammar = {
             'S': ['aX0'],
             'A': ['bX1'],
             'B': ['cX2'],
             'C': ['d'],
             'X0': ['A'],
             'X1': ['B']
        }
        self.assertEqual(converter.cnf_grammar, expected_cnf_grammar)

    def test_long_productions(self):
        grammar = {
            'S': ['aBCDE'],
            'A': ['a'],
            'B': ['b'],
            'C': ['c'],
            'D': ['d'],
            'E': ['e']
        }
        converter = CNFConverter(grammar)
        expected_cnf_grammar = {
            'S': ['aX0'],
            'A': ['a'],
            'B': ['b'],
            'C': ['c'],
            'D': ['d'],
            'E': ['e'],
            'X0': ['X1E'],
            'X1': ['X2D'],
            'X2': ['X3C'],
            'X3': ['aB']
        }
        self.assertEqual(converter.cnf_grammar, expected_cnf_grammar)

    def test_empty_grammar(self):
        grammar = {}
        converter = CNFConverter(grammar)
        expected_cnf_grammar = {}
        self.assertEqual(converter.cnf_grammar, expected_cnf_grammar)
