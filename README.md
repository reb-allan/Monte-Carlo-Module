# Monte Carlo Simulator (Dice Game)

A Monte Carlo simulator, in the form of a dice game, where dice are rolled multiple times and the outcomes are analyzed. The game involves multiple dice, each with a set of faces and associated weights, which affect the outcome of each roll.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Synopsis](#synopsis)
4. [API](#api)
5. [Metadata](#metadata)

## Overview

This project simulates the rolling of dice in a Monte Carlo fashion. You can play the game, roll multiple dice with custom weights, and analyze the results. The game tracks the number of times each die rolled the same face (jackpots), counts how often each face appears, and computes distinct combinations or permutations of rolled faces.

The main classes include:
- `Die`: Represents a single die with distinct faces and optional custom weights.
- `Game`: Manages the dice, rolls them, and stores results.
- `Analyzer`: Provides analytical tools for the results of the game, such as jackpot counts, face counts, and combinations of rolls.

## Features

In this repo you will find:
- MonteCarlo.py file that contains the code for the module.
- MonteCarlo_test.py file that contains the information necessary to preform a Unittest.
- Setup.py and __init__.py file that are necessary for importing the model

## Synopsis

This section will show how each the module is imported and how each class is called.

### Importing the Classes

To use the dice simulator, you will need to import the `Die`, `Game`, and `Analyzer` classes:

```
from MonteCarlo import Die, Game, Analyzer
```

### Die Class

The Die class represents a single die with faces and weights. You can specify the faces (as a numpy array) and change the weight of each face.
```
faces = np.array([1, 2, 3, 4, 5, 6])
dice = Die(faces)

```
### Game Class

```
game = Game(dice)   # Create the game
game.play(rolls=5)  # Play the game (roll each die 5 times)
```
### Analyzer Class

```
analyzer = Analyzer(game)
```

## API

This section will detail all methods for each class.

### Die Class:

The methods in the Die Class are:
- change_weight(self, face, new_weight): Changes the weight of a specific face on the die.
- roll(self, times=1): Rolls the die a given number of times, applying weights to determine the outcome. Defaults to 1 roll.
- show_state(self): Returns a copy of the die's current state (faces and weights).


### Game Class:

The methods in the Game Class are:
- play(self, rolls): Rolls all the dice a specified number of times.
- show_results(self, form="wide"): Returns the results of the most recent play with the option for a wide or narrow data frame, defaulting. to wide.


### Analyzer Class:

The methods in the Analyzer Class are:
- jackpot(self): Computes how many times all dice rolled the same face (a jackpot).
- face_counts_per_roll(self): Computes how many times each face was rolled in each event.
- combo_counts(self): Computes distinct combinations of faces rolled and their counts.
- permute_counts(self): Computes distinct permutations of faces rolled and their counts.


## Metadata

- **Name**: Monte Carlo Dice Simulator
- **Version**: 0.1
- **Description**: A Monte Carlo simulator for creating dice, simulating dice rolls, and analyzing results.
- **Author**: Rebekah Allan
- **Email**: tkz5ry@virginia.edu
- **License**: MIT
- **Dependencies**:
    - numpy
    - pandas
- **Project URL**: [GitHub Repository](https://github.com/reb-allan/Monte-Carlo-Module)







