import unittest
import numpy as np
import pandas as pd
from MonteCarlo import Die, Game, Analyzer 

class TestDie(unittest.TestCase):
    def setUp(self):
        self.die = Die(faces=np.array([1, 2, 3, 4, 5, 6]))

    def test_initialization(self):
        '''
        Test that the die is initialized with correct faces and weights
        '''
        self.assertEqual(list(self.die.faces), [1, 2, 3, 4, 5, 6])
        self.assertTrue(np.array_equal(self.die.weights, np.ones(6)))
        self.assertIsInstance(self.die.df, pd.DataFrame)

    def test_change_weight(self):
        '''
        Test changing the weight of a face
        '''
        self.die.change_weight(1, 2.0)
        self.assertEqual(self.die.df.loc[1, 'weights'], 2.0)

    def test_invalid_face_for_weight_change(self):
        '''
        Test invalid face change (should raise IndexError)
        '''
        with self.assertRaises(IndexError):
            self.die.change_weight(7, 2.0)

    def test_invalid_weight_type(self):
        '''
        Test invalid weight type (should raise TypeError)
        '''
        with self.assertRaises(TypeError):
            self.die.change_weight(1, "string")

    def test_roll(self):
        '''
        Test that roll produces the expected output (a face from the die)
        '''
        result = self.die.roll(times=3)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(face in self.die.faces for face in result))


class TestGame(unittest.TestCase):
    def setUp(self):
        '''
        
        '''
        die1 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        self.game = Game(dice=[die1, die2])

    def test_initialization(self):
        '''
        Test that the game initializes with correct dice
        '''
        self.assertEqual(len(self.game.dice), 2)
        self.assertIsInstance(self.game.dice[0], Die)

    def test_play(self):
        '''
        Test the play method to verify the results DataFrame
        '''
        self.game.play(rolls=5)
        self.assertIsInstance(self.game.results, pd.DataFrame)
        self.assertEqual(self.game.results.shape[0], 5)
        self.assertEqual(self.game.results.shape[1], 2)  # Since 2 dice are being rolled

    def test_show_results_wide(self):
        '''
        Test that show_results returns the DataFrame in wide format
        '''
        self.game.play(rolls=5)
        results_wide = self.game.show_results(form="wide")
        self.assertIsInstance(results_wide, pd.DataFrame)
        self.assertEqual(results_wide.index.name, 'Roll')

    def test_show_results_narrow(self):
        '''
        Test that show_results returns the DataFrame in narrow format
        '''
        self.game.play(rolls=5)
        results_narrow = self.game.show_results(form="narrow")
        self.assertIsInstance(results_narrow, pd.DataFrame)
        self.assertEqual(results_narrow.index.names, ['Roll', 'Die'])

    def test_show_results_invalid_form(self):
        '''
        Test invalid form argument
        '''
        with self.assertRaises(ValueError):
            self.game.show_results(form="invalid")


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        '''
        
        '''
        die1 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        self.game = Game(dice=[die1, die2])
        self.game.play(rolls=5)
        self.analyzer = Analyzer(game=self.game)

    def test_jackpot(self):
        '''
        Test jackpot count (all dice rolled the same face)
        '''
        self.assertIsInstance(self.analyzer.jackpot(), int)

    def test_face_counts_per_roll(self):
        '''
        Test that face counts are calculated correctly
        '''
        face_counts = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(face_counts, pd.DataFrame)
        self.assertEqual(face_counts.index.name, 'Roll')
        self.assertTrue(np.all(face_counts.columns.isin([1, 2, 3, 4, 5, 6])))

    def test_combo_counts(self):
        '''
        Test that combinations of rolled faces are counted correctly
        '''
        combo_counts = self.analyzer.combo_counts()
        self.assertIsInstance(combo_counts, pd.DataFrame)
        self.assertIn('Count', combo_counts.columns)

    def test_permute_counts(self):
        '''
        Test that permutations of rolled faces are counted correctly
        '''
        perm_counts = self.analyzer.permute_counts()
        self.assertIsInstance(perm_counts, pd.DataFrame)
        self.assertIn('Count', perm_counts.columns)


if __name__ == '__main__':
    unittest.main()
    