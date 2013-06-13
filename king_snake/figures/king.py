"""King chess piece."""

from king_snake.errors import FieldMustBeCastledError, IllegalMoveError
from figure import Figure


class King(Figure):

    """King chess piece."""

    start_position = {"white": ["E1"],
                      "black": ["E8"]}

    def __init__(self, player):
        """Initialize king and set castle positions."""
        super(King, self).__init__(player)
        self.castle_positions = {"left": self.position.to_left().to_left(),
                                 "right": self.position.to_right().to_right()}

    @property
    def legal_moves(self):
        """Return legal moves from current position."""
        moves = []
        # Castling positions
        if not self.already_moved:
            moves.extend(self.castle_positions.values())
        # Normal positions
        moves.extend(self._fields_in_directions(("to_left", "to_right",
                                                 "above", "below",
                                                 "above_right", "below_right",
                                                 "above_left", "below_left"),
                                                1))
        return moves

    def move(self, field):
        """
        Move to field.

        If given field is a castling field and castling is legal, use try
        castling. Otherwise call superclass method.
        """
        if field in self.legal_moves and field in self.castle_positions:
            raise FieldMustBeCastledError("Goal field is for castling.")
        else:
            super(King, self).move(field)

    @property
    def in_check(self):
        """Test if king is in check."""
        return self.position.threatened_by(self.player.opponent)

    def castle(self, field):
        """
        Castle king.

        First, check if corresponding rook is there and has not moved yet. Then
        check if any of the positions between and including the king and rook
        are occupied or threatened. If this is not the case, castle the king.
        If not, raise error.

        @return: Dictionary as if rook had been captured.
        """
        involved_fields = []
        rook, rook_position = None, None
        position = old_position = self.position
        involved_fields.append(position)

        if field == self.castle_positions["left"]:
            rook_position = self.player.chessboard.fields[
                                                      "A{}".format(
                                                      self.position.number)]
            while position != self.castle_positions["left"]:
                position = position.to_left()
                involved_fields.append(position)
        # Rook is on right
        elif field == self.castle_positions["right"]:
            rook_position = self.player.chessboard.fields[
                                                      "H{}".format(
                                                      self.position.number)]
            while position != self.castle_positions["right"]:
                position = position.to_right()
                involved_fields.append(position)

        if rook_position:
            rook = rook_position.figure
        if rook and not rook.already_moved:
            involved_fields_free = True
            for position in involved_fields:
                if position.threatened_by(self.player.opponent):
                    involved_fields_free = False
                elif position.figure and not (position == self.position or
                                              position == rook_position):
                    involved_fields_free = False
            if involved_fields_free:
                field.receive_figure(self)
                if field == self.castle_positions["left"]:
                    field.to_right().receive_figure(rook)
                else:
                    field.to_left().receive_figure(rook)

        # If King could be castled, return capture dictionary with rook.
        if self.position == field:
            return {"figure": rook, "old_position": old_position}
        else:
            raise IllegalMoveError("King cannot castle here.")
