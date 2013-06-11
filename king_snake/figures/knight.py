"""A knight chess piece."""

from figure import Figure


class Knight(Figure):

    """A knight chess piece."""

    start_position = {"white": ("B1", "G1"),
                      "black": ("B8", "G8")}
