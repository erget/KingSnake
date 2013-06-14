#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from king_snake.player import Player
from king_snake.chessboard import Chessboard
from king_snake.errors import ChessError

"""The GUI for playing chess using KingSnake!"""


class ChessGame(object):

    """
    A chess game manager

    What it should be able to do:
    Read a game from the command line
    Provide a user interface for moving pieces
    Prompt user to move pieces around
    """

    def __init__(self):
        player1, player2 = Player(), Player()
        self.white, self.black = player1, player2
        self.chessboard = Chessboard()
        self.chessboard.add_players(player1, player2)
        self.greet()

    def greet(self):
        """Greet the players and begin game."""
        print("Welcome to KingSnake.\n"
              "Enter moves directly or press Enter to enter the menu.")
        self.get_move()

    def get_move(self):
        """Show board and prompt for current move, then execute it."""
        valid_move = False
        while not valid_move:
            self.show()
            move = raw_input("Please enter your move (e.g. E2 E4) or enter to "
                             "access the menu: ")
            if not move:
                self.menu()
            else:
                try:
                    start_position, end_position = move.split()
                    self.chessboard.current_player.move(start_position.upper(),
                                                        end_position.upper())
                    valid_move = True
                except ValueError:
                    print("Please enter your move in the following form:\n"
                          "{start position} {end position}\n"
                          "Positions are notaded using their letter followed"
                          "by their number.\n"
                          "Example valid move request to move from A1 to A2: "
                          "'A1 A2'")
                except KeyError:
                    print("Only valid fields are allowed.")
                except ChessError as error:
                    print(error)
        self.get_move()

    def menu(self):
        """Allow user to do something other than move pieces"""

        def quit_game():
            """Quit game."""
            sys.exit()

        def resign():
            """Resign."""
            print("{} resigns. {} is the winner!".format(
                 self.chessboard.current_player.color.capitalize(),
                 self.chessboard.current_player.opponent.color.capitalize()))
            time.sleep(10)
            quit_game()

        def restart():
            """Start new game."""
            self.__init__()

        def save_game():
            """Save game to file."""
            raise NotImplementedError

        def load_game():
            """Load game from file."""
            raise NotImplementedError

        def undo_turn():
            """Undo turn."""
            raise NotImplementedError

        def return_to_game():
            """Resume play."""
            self.get_move()
        menu_choices = []
        for function in (quit_game, resign, restart, save_game, load_game,
                         undo_turn, return_to_game):
            menu_choices.append((function, function.__doc__))
        valid_choice = False
        while not valid_choice:
            for number, choice in enumerate(menu_choices):
                print("{}. {}".format(number + 1, choice[1]))
            try:
                decision = int(raw_input("What would you like to do?: ")) - 1
                try:
                    valid_choice = True
                    menu_choices[decision][0]()
                except IndexError:
                    valid_choice = False
                    print("Please enter a valid menu number.")
            except (ValueError, IndexError):
                print("Please enter a valid menu number.")

    def show(self):
        """Show chessboard and print current player."""
        print(self.chessboard)
        print("It's {}'s turn.\n".format(self.chessboard.current_player.color))

game = ChessGame()
