"""Abstract chess figure classes."""

from king_snake.exceptions import FieldOccupiedError, IllegalMoveError


class Figure(object):

    """
    A chess figure.

    start_position is the starting position for the figure class and should be
    implemented in subclasses. It contains a dictionary of possible positions
    for each color. Each entry in the dictionary is a tuple of the appropriate
    field coordinates.
    """

    start_position = {"white": (None),
                      "black": (None)}

    def __repr__(self):
        return "{type} at {position}".format(type=self.__class__.__name__,
                                             position=self.position)

    def __init__(self, player):
        """
        Initialize figure and position figure on chessboard.

        The start position is determined by the player's color and whether or
        not the position on the board is already taken.
        """
        self.player = player
        if self.player == self.player.chessboard.players["white"]:
            self.color = "white"
        else:
            self.color = "black"
        self.position = None
        self._set_position()

    def _set_position(self):
        """
        Set figure's position.

        Go through all possible positions for object's color. Try to take
        position. If position is blocked, try next position.
        """
        for position in self.start_position[self.color]:
            if not self.position:
                try:
                    self.player.chessboard.fields[
                                              position].receive_figure(self)
                    self.position = self.player.chessboard.fields[position]
                except FieldOccupiedError:
                    pass

    @property
    def legal_moves(self):
        """
        Compute list of legal moves.

        If legal, append field. If piece, stop. Append if other color, else
        don't append.
        """
        raise NotImplementedError

    def move(self, field):
        """
        Move to field.

        If field in self.legal_moves, add self to field, then replace
        self.position with new field. Else raise FieldOccupiedError.
        """
        if field in self.legal_moves:
            field.receive_figure(self)
            self.position = field
        else:
            raise IllegalMoveError("Piece cannot move to given field.")

    def capture(self, field):
        """Capture piece at field.

        @return dict: {"figure": figure, "old_position": old_position}
        """
        if field.figure.color != self.color:
            field.receive_figure(self)
            self.position = field
            return


class RelevantHistoryFigure(Figure):

    """A figure for which the move history is relevant."""

    start_position = {"white": (None),
                      "black": (None)}

    def __init__(self, player):
        super(RelevantHistoryFigure, self).__init__(player)
        self.already_moved = False
