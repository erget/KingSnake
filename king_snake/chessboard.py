# -*- coding: utf-8 -*-
"""A chess board and fields."""

from king_snake.errors import FieldOccupiedError


class Field(object):

    """A field on a chessboard."""

    def __repr__(self):
        return "Field({letter}, {number}, {board})".format(
                                           letter=chr(self.letter),
                                           number=self.number,
                                           board=self.chessboard.__repr__())

    def __str__(self):
        """
        Return unicode representation of the field and its figure, if present.

        If no figure is present, "..." is returned.
        """
        figure = self.figure
        if not figure:
            figure = "…"
        return str(figure)

    def __init__(self, letter, number, chessboard):
        """
        Store position on chessboard.

        Letter is given as a capital character and converted internally into an
        integer.
        """
        self.letter = ord(letter)
        self.number = number
        self.chessboard = chessboard
        self.figure = None

    def receive_figure(self, figure):
        """
        Place a figure on field.

        If figure was already on chessboard, remove figure from former field.
        Set figure's position to self.
        If self is occupied, raise error.
        """
        if not self.figure:
            self.figure = figure
            if figure.position:
                figure.position.figure = None
            figure.position = self
        else:
            raise FieldOccupiedError("The goal field is occupied.")

    def to_right(self):
        """Return field to right of self or None if there is none."""
        position = chr(self.letter + 1) + str(self.number)
        return self.chessboard.fields.get(position)

    def to_left(self):
        """Return field to left of self or None if there is none."""
        position = chr(self.letter - 1) + str(self.number)
        return self.chessboard.fields.get(position)

    def above(self):
        """Return field above self or None if there is none."""
        position = chr(self.letter) + str(self.number + 1)
        return self.chessboard.fields.get(position)

    def below(self):
        """Return field below self or None if there is none."""
        position = chr(self.letter) + str(self.number - 1)
        return self.chessboard.fields.get(position)

    def above_right(self):
        """Return field above self and to right or None if there is none."""
        above = self.above()
        if above:
            return above.to_right()

    def above_left(self):
        """Return field above self and to left or None if there is none."""
        above = self.above()
        if above:
            return above.to_left()

    def below_right(self):
        """Return field below self and to right or None if there is none."""
        below = self.below()
        if below:
            return below.to_right()

    def below_left(self):
        """Return field below self and to left or None if there is none."""
        below = self.below()
        if below:
            return below.to_left()

    def threatened_by(self, player):
        """Field is in legal moves of given player."""
        for figure in player.figures:
            if figure.position and self in figure.legal_moves:
                return True


class Chessboard(object):

    """A chessboard."""

    def __str__(self):
        """Print border with coordinates and all fields in order."""
        string = ""
        column_string = ""
        if self.current_player.color == "white":
            row_range = (8, 0, -1)
            column_range = (ord("A"), ord("H") + 1)
        else:
            row_range = (1, 9)
            column_range = (ord("H"), ord("A") - 1, -1)
        for row in range(*row_range):
            string += "{}|".format(row)
            for column in range(*column_range):
                position = "{}{}".format(chr(column), row)
                string += str(self.fields[position])
                if len(column_string) < 8:
                    column_string += chr(column)
            string += "\n"
        string += " " + "=" * 9 + "\n"
        string += "  {}".format(column_string)
        return string

    def __init__(self, players=None, move_history=[]):
        """
        Initialize fields and set current move to 1.

        Players do not have to be supplied. If they are, they should be
        provided as a dictionary: {"white": Player, "black": Player}

        If a move history is supplied, apply that move history.
        """
        self.fields = dict()
        for letter in "ABCDEFGH":
            for number in range(1, 9):
                self.fields[letter + str(number)] = Field(letter, number, self)

        if players:
            self.add_players(players["white"], players["black"])
        else:
            self.players = dict()
            self.current_player = None

        self.move_history = []
        self.current_move = 1
        if self.current_player:
            for start_field, goal_field in move_history:
                self.current_player.move(start_field, goal_field)

    def start_move(self, start_field, goal_field):
        """
        Pickle self and store it on object.

        The move history is used for rollback capabilities
        """
        self.current_move += 1
        self.move_history.append((start_field, goal_field))

    def rollback(self):
        """Rollback to previous state"""
        self.__init__(self.players, self.move_history[:-1])

    def add_players(self, white, black):
        """Add players to the game, assign colors and set up board."""
        for color, player in (("white", white), ("black", black)):
            self.players[color] = player
            self.players[color].color = color
            player.set_up_board(self)
            self.current_player = self.players["white"]

    def end_turn(self):
        """End turn for current player and increment current_move."""
        if self.current_player == self.players["white"]:
            self.current_player = self.players["black"]
        else:
            self.current_player = self.players["white"]
