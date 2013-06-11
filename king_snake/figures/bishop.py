"""A bishop chess piece."""

from figure import Figure


class Bishop(Figure):

    """A bishop chess piece."""

    start_position = {"white": ("C1", "F1"),
                      "black": ("C8", "F8")}
