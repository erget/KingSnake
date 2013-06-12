"""A queen chess piece."""

from figure import Figure


class Queen(Figure):

    """A queen chess piece."""

    start_position = {"white": ["D1"],
                      "black": ["D8"]}

    @property
    def legal_moves(self):
        """Return legal moves from current position."""
        return self._fields_in_directions(("to_left", "to_right", "above",
                                           "below", "above_right",
                                           "below_right", "above_left",
                                           "below_left"))
