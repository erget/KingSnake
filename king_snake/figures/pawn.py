"""Pawn chess piece."""

from figure import Figure


class Pawn(Figure):

    """Pawn chess piece."""

    start_position = {"white": list(letter + "2" for letter in "ABCDEFGH"),
                      "black": list(letter + "7" for letter in "ABCDEFGH")}

    def __init__(self, player):
        super(Pawn, self).__init__(player)
        self.already_captured = False

    def become_queen(self):
        """Become a queen."""
