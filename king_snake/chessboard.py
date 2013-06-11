"""A chess board and fields."""

from king_snake.exceptions import FieldOccupiedError


class Field(object):

    """A field on a chessboard."""

    def __repr__(self):
        return "Field({letter}, {number})".format(letter=chr(self.letter),
                                                  number=self.number)

    def __str__(self):
        return "{}{}".format(chr(self.letter), self.number)

    def __init__(self, letter, number):
        """
        Store position on chessboard.

        Letter is given as a capital character and converted internally into an
        integer.
        """
        self.letter = ord(letter)
        self.number = number
        self.figure = None

    def receive_figure(self, figure):
        """Place a figure on field."""
        if not self.figure:
            self.figure = figure
        else:
            raise FieldOccupiedError("The goal field is occupied.")


class Chessboard(object):

    """A chessboard."""

    def __init__(self):
        self.players = dict()

        self.fields = dict()
        self.current_player = None
        for letter in "ABCDEFGH":
            for number in range(1, 9):
                self.fields[letter + str(number)] = Field(letter, number)

    def add_players(self, white, black):
        """Add players to the game"""
        for color, player in (("white", white), ("black", black)):
            self.players[color] = player
            player.set_up_board(self)
            self.current_player = self.players["white"]

    def end_turn(self):
        """End turn for current player."""
        if self.current_player == self.players["white"]:
            self.current_player = self.players["black"]
        else:
            self.current_player = self.players["white"]
