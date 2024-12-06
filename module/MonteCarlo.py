import numpy as np
import pandas as pd
import random

class Die:
    """
    A class representing a die with distinct faces and weights.
    
    Attributes:
        faces (numpy array): Array of distinct faces (can be strings or numbers).
        weights (numpy array): Array of weights corresponding to the faces (default 1.0 for each).
    """
    
    def __init__(self, faces):
        """
        Initializes the Die object with faces and default weights set to 1.0.
        
        Parameters:
            faces (numpy array): A numpy array of distinct faces (strings or numbers).
        
        Raises:
            TypeError: If faces is not a numpy array.
            ValueError: If faces are not distinct.
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a numpy array.")
        
        if any(faces.count(face) > 1 for face in faces):
            raise ValueError("Faces must be distinct.")
        
        self.faces = faces
        self.weights = np.ones(len(faces))  # default weights are 1.0 for each face
        self.df = pd.DataFrame({'faces': faces, 'weights': self.weights}).set_index('faces')

    def change_weight(self, face, new_weight):
        """
        Changes the weight of a specific face on the die.
        
        Parameters:
            face (str or int): The face to modify.
            new_weight (float or int): The new weight for the face.
        
        Raises:
            IndexError: If the face is not a valid face on the die.
            TypeError: If new_weight is not a numeric type.
        """
        if face not in self.faces:
            raise IndexError(f"Face '{face}' not found in die.")
        
        if not isinstance(new_weight, (int, float)):
            raise TypeError("Weight must be a numeric value.")
        
        self.df.loc[face, 'weights'] = new_weight

    def roll(self, times=1):
        """
        Rolls the die a given number of times, applying weights to determine the outcome.
        
        Parameters:
            times (int): The number of times the die should be rolled. Defaults to 1.
        
        Returns:
            list: A list of rolled faces.
        """
        return random.choices(self.faces, weights=self.df['weights'], k=times)

    def show_state(self):
        """
        Returns a copy of the die's current state (faces and weights).
        """
        return self.df.copy()

    
    
class Game:
    """
    A class representing a game consisting of one or more dice rolls.
    
    Attributes:
        dice (list): A list of Die objects with similar faces.
    """
    
    def __init__(self, dice):
        """
        Initializes the Game object with a list of Die objects.
        
        Parameters:
            dice (list): A list of Die objects with the same faces.
        
        """
        if not all(isinstance(die, Die) for die in dice):
            raise ValueError("All elements must be instances of the Die class.")
        
        self.dice = dice
        self.results = None

    def play(self, rolls):
        """
        Rolls all the dice a specified number of times.
        
        Parameters:
            rolls (int): The number of times each die should be rolled.
        
        Saves the results as a DataFrame in wide format.
        """
        results = []
        for roll in range(rolls):
            roll_results = []
            for i, die in enumerate(self.dice):
                outcome=die.roll(1)[0]
                roll_results.append(outcome)
            results.append(roll_results)
        
        # Convert results to DataFrame with roll number as index and die number as columns
        self.results = pd.DataFrame(results, columns=[f"Die {i}" for i in range(len(self.dice))])
        self.results.index = range(1, len(self.results) + 1)
        self.results.index.name = 'Roll'
    
    def show_results(self, form="wide"):
        """
        Returns the results of the most recent play in the specified format.
        
        Parameters:
            form (str): 'wide' or 'narrow'. Defaults to 'wide'. Narrow format is a MultiIndex.
        
        Returns:
            pandas.DataFrame: The results DataFrame in the requested format.
        
        Raises:
            ValueError: If the form is not 'wide' or 'narrow'.
        """
        if self.results is None:
            raise ValueError("No results available. Please play the game first.")
        
        if form == "wide":
            return self.results.copy()
        
        elif form == "narrow":
            narrow_results = self.wide_results.melt(ignore_index=False, var_name='Die', value_name='Outcome')
            narrow_results.reset_index(inplace=True)
            narrow_results.set_index(['Roll', 'Die'], inplace=True)
            return narrow_results
        
        else:
            raise ValueError("Invalid form. Choose 'wide' or 'narrow'.")

            
            
class Analyzer:
    """
    A class to analyze the results of a game.
    
    Attributes:
        game (Game): The Game object whose results will be analyzed.
    """
    
    def __init__(self, game):
        """
        Initializes the Analyzer object with a Game object.
        
        Parameters:
            game (Game): The game object to analyze.
        
        Raises:
            ValueError: If the input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        
        self.game = game
        
        if self.game.results is None:
            raise ValueError("No game results available. Please play the game first.")
        

    def jackpot(self):
        """
        Computes how many times all dice rolled the same face (a jackpot).
        
        Returns:
            int: The number of jackpots in the results.
        """
        
        jackpot = self.game.results.nunique(axis=1) == 1
        jackpot_count = sum(jackpot)
        return jackpot_count

    def face_counts_per_roll(self):
        """
        Computes how many times each face was rolled in each event.
        
        Returns:
            pandas.DataFrame: A DataFrame with roll number as index and face counts as columns.
        """
        all_faces = self.game.results.stack().unique()
        face_counts = self.game.results.apply(lambda row: row.value_counts(), axis=1).fillna(0)
        face_counts_df = pd.DataFrame(face_counts)
        face_counts_df = face_counts_df.reindex(columns=all_faces, fill_value=0)
        face_counts_df.index.name = 'Roll'
        return face_counts_df

    def combo_counts(self):
        """
        Computes distinct combinations of faces rolled and their counts.
        
        Returns:
            pandas.DataFrame: A DataFrame with distinct combinations and their counts.
        """
        
        combos = self.game.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combos.value_counts()
        combo_counts_df = pd.DataFrame({'Count': combo_counts})
        return combo_counts_df

    def permute_counts(self):
        """
        Computes distinct permutations of faces rolled and their counts.
        
        Returns:
            pandas.DataFrame: A DataFrame with distinct permutations and their counts.
        """
        perms = self.game.results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts()
        perm_counts_df = pd.DataFrame({'Count': perm_counts}).set_index(perm_counts.index)
        return perm_counts_df
