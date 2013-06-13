"""Abstract chess figure classes."""

from king_snake.errors import (FieldMustBeCastledError, FieldOccupiedError,
                               IllegalCaptureError, IllegalMoveError,
                               PawnMustCaptureError)


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

    def __init__(self, player, position=None):
        """
        Initialize figure and position figure on chessboard.

        If no initialization position is given, the start position is
        determined by the player's color and whether or not the position on the
        board is already taken.

        A Player set's a figure's already_moved field to True when moving. The
        last_moved field is set to the current move number whenever a move is
        successfully completed. A captured move is also set to have been moved
        when being captured, as is a castled rook.
        """
        self.player = player
        if self.player == self.player.chessboard.players["white"]:
            self.color = "white"
        else:
            self.color = "black"

        self.position = position
        if not position:
            self._set_start_position()

        self.already_moved = False
        self.last_moved = None

    def _set_start_position(self):
        """
        Set figure's starting position.

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

    def _fields_in_directions(self, directions, perimeter=8):
        """
        Find fields within a perimeter in a given direction.

        Returns a list of fields in the given directions within the movement
        perimeter. Terminates after appending a field with a piece on it.

        The directions are the string names of directional methods on the Field
        class which return neighboring Fields in the given direction. See Field
        for the possible directions.

        The perimeter is set to 8 by default, because chess pieces operate on
        an 8x8 board.
        """
        fields = []
        for direction in directions:
            found_figure = None
            next_position = getattr(self.position, direction)()
            distance = 1
            while distance <= perimeter and next_position and not found_figure:
                fields.append(next_position)
                if next_position.figure:
                    found_figure = next_position.figure
                next_position = getattr(next_position, direction)()
                distance += 1
        return fields

    @property
    def legal_moves(self):
        """
        Compute list of legal moves.

        If legal, append field. If piece, append field and stop.
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
        else:
            raise IllegalMoveError("Piece cannot move to given field.")

    def capture(self, field):
        """Capture piece at field.

        Check if piece to capture is of different color. If not, raise error.
        If it is, unlink the figure and field, then place self on field.

        @return dict: {"figure": figure, "old_position": old_position}
        """
        if field.figure.color != self.color:
            captured_figure = field.figure
            captured_figure.position = None
            field.figure = None
            field.receive_figure(self)
            return {"figure": captured_figure, "old_position": field}
        else:
            raise IllegalCaptureError("Cannot capture piece of same color.")
