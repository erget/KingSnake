"""Pawn chess piece."""

from figure import Figure


class Pawn(Figure):

    """Pawn chess piece."""

    start_position = {"white": list(letter + "2" for letter in "ABCDEFGH"),
                      "black": list(letter + "7" for letter in "ABCDEFGH")}

    def __init__(self, player):
        super(Pawn, self).__init__(player)
        self.already_captured = False

    # TODO: Implement exceptional movement
    def legal_moves(self):
        """Return legal moves from current position."""
        return self._fields_in_directions(["above"], 1)

    def become_queen(self):
        """Become a queen."""
