# -*- coding: utf-8 -*-
"""A bishop chess piece."""

from .figure import Figure


class Bishop(Figure):

    """A bishop chess piece."""

    start_position = {"white": ("C1", "F1"),
                      "black": ("C8", "F8")}

    def __str__(self):
        if self.color == "white":
            string = "♗"
        else:
            string = "♝"
        return string

    @property
    def legal_moves(self):
        """Return legal moves from current position."""
        return self._fields_in_directions(("above_right", "below_right",
                                           "above_left", "below_left"))
