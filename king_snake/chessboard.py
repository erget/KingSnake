"""A chess board and fields."""

from king_snake.errors import FieldOccupiedError


class Field(object):

    """A field on a chessboard."""

    def __repr__(self):
        return "Field({letter}, {number}, {board})".format(
                                                       letter=chr(self.letter),
                                                       number=self.number,
                                                       board=self.chessboard)

    def __str__(self):
        return "{}{}".format(chr(self.letter), self.number)

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
            if self in figure.legal_moves:
                return True


class Chessboard(object):

    """A chessboard."""

    def __init__(self):
        self.players = dict()

        self.fields = dict()
        self.current_player = None
        for letter in "ABCDEFGH":
            for number in range(1, 9):
                self.fields[letter + str(number)] = Field(letter, number, self)

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
