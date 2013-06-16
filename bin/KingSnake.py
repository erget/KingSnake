#!/bin/env python
# -*- coding: utf-8 -*-

"""The GUI for playing chess using KingSnake!"""

import pickle
import sys
import time

from king_snake.player import Player
from king_snake.chessboard import Chessboard
from king_snake.errors import ChessError


class ChessGame(object):

    """A chess game manager"""

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

    def get_move(self, message=""):
        """Show board and prompt for current move, then execute it."""
        valid_move = False
        while not valid_move:
            self.show(message)
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
                    message = ("Please enter your move in the following form:"
                               "\n{start position} {end position}\n"
                              "Positions are notated using their letter "
                              "followed by their number.\n"
                              "Example valid move request to move from A1 to "
                              "A2: 'A1 A2'")
                except KeyError:
                    message = "Only valid fields are allowed."
                except ChessError as error:
                    message = error
        self.get_move(message)

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
            file_name = raw_input("What file would you like to save to?: ")
            try:
                with open(file_name, "w") as saved_game:
                    pickle.dump(self.chessboard, saved_game)
            except IOError:
                self.get_move("The file you have chosen is invalid. "
                              "Please enter a valid filename.")

        def load_game():
            """Load game from file."""
            file_name = raw_input("What file would you like to load from?: ")
            try:
                with open(file_name) as saved_game:
                    self.chessboard = pickle.load(saved_game)
                    self.white = self.chessboard.players["white"]
                    self.black = self.chessboard.players["black"]
            except IOError:
                self.get_move("The file you have chosen is invalid. "
                              "Please enter a valid filename.")

        def undo_turn():
            """Undo turn."""
            try:
                self.chessboard = self.chessboard.previous_move
                self.white = self.chessboard.players["white"]
                self.black = self.chessboard.players["black"]
                self.get_move("Move restored.")
            except AttributeError:
                self.get_move("You are already at the first move.")

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

    def show(self, message=""):
        """Show chessboard and print current player."""
        print(self.chessboard)
        print("{}\n"
              "It's {}'s turn.".format(message,
                                       self.chessboard.current_player.color))

game = ChessGame()
