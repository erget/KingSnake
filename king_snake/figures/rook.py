"""Rook chess piece."""

from figure import Figure


class Rook(Figure):

    """Rook chess piece."""

    start_position = {"white": ["A1", "H1"],
                      "black": ["A8", "H8"]}

    def __init__(self, player):
        super(Rook, self).__init__(player)
