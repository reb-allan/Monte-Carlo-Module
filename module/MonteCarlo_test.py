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

    def test_change_weight(self):
        '''
        Test changing the weight of a face, invalid face change, and invalid weight type
        '''
        self.die.change_weight(1, 2.0)
        self.assertEqual(self.die.df.loc[1, 'weights'], 2.0)

        with self.assertRaises(IndexError):
            self.die.change_weight(7, 2.0)

        with self.assertRaises(TypeError):
            self.die.change_weight(1, "string")

    def test_roll(self):
        '''
        Test that roll produces the expected output.
        '''
        result = self.die.roll(times=3)
        self.assertEqual(len(result), 3)
        
    def test_show_state_returns_copy(self):
        """
        Test that the show_state method returns a dataframe.
        """
        die_state = self.die.show_state()
        self.assertIsInstance(die_state, pd.DataFrame)


class TestGame(unittest.TestCase):
    def setUp(self):
        die1 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        self.game = Game(dice=[die1, die2])

    def test_initialization_game(self):
        '''
        Test that the game initializes with correct dice
        '''
        self.assertEqual(len(self.game.dice), 2)

    def test_play(self):
        '''
        Test the play method to verify the results are a DataFrame, and checks that the DataFrame is the size we would expect.
        '''
        self.game.play(rolls=5)
        self.assertIsInstance(self.game.results, pd.DataFrame)
        self.assertEqual(self.game.results.shape[0], 5)
        self.assertEqual(self.game.results.shape[1], 2)  

    def test_show_results(self):
        '''
        Test that show_results returns the DataFrame in wide and narrow formats, and checks the index for both.
        '''
        self.game.play(rolls=5)
        results_wide = self.game.show_results(form="wide")
        self.assertIsInstance(results_wide, pd.DataFrame)
        self.assertEqual(results_wide.index.name, 'Roll')

        self.game.play(rolls=5)
        results_narrow = self.game.show_results(form="narrow")
        self.assertIsInstance(results_narrow, pd.DataFrame)
        self.assertEqual(results_narrow.index.names, ['Roll', 'Die'])           
            

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        die1 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(faces=np.array([1, 2, 3, 4, 5, 6]))
        self.game = Game(dice=[die1, die2])
        self.game.play(rolls=5)
        self.analyzer = Analyzer(game=self.game)

    def test_initialization_analyser(self):
        '''
        Test that the analyzer is initialized correctly with a Game object and raises an error when initialized with a non-Game object.
        '''
        self.assertEqual(self.analyzer.game, self.game)
        
        with self.assertRaises(ValueError):
            invalid_analyzer = Analyzer([])
        
        with self.assertRaises(ValueError):
            invalid_analyzer = Analyzer(None)
        
    def test_jackpot(self):
        '''
        Test jackpot count.
        '''
        self.assertIsInstance(self.analyzer.jackpot(), int)

    def test_face_counts_per_roll(self):
        '''
        Test that face counts are calculated correctly, checking that it returns a dataframe, the index name is correct, and all counts determined are the faces of our dice.
        '''
        face_counts = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(face_counts, pd.DataFrame)
        self.assertEqual(face_counts.index.name, 'Roll')
        self.assertTrue(np.all(face_counts.columns.isin([1, 2, 3, 4, 5, 6])))

    def test_combo_counts(self):
        '''
        Test the combinations of rolled faces, checking that it returns data frame and the column was named correctly.
        '''
        combo_counts = self.analyzer.combo_counts()
        self.assertIsInstance(combo_counts, pd.DataFrame)
        self.assertIn('Count', combo_counts.columns)

    def test_permute_counts(self):
        '''
        Test the permutations of rolled faces, checking that it returns data frame and the column was named correctly.
        '''
        perm_counts = self.analyzer.permute_counts()
        self.assertIsInstance(perm_counts, pd.DataFrame)
        self.assertIn('Count', perm_counts.columns)


if __name__ == '__main__':
    unittest.main()
    
