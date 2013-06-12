"""A knight chess piece."""

from figure import Figure


class Knight(Figure):

    """A knight chess piece."""

    start_position = {"white": ("B1", "G1"),
                      "black": ("B8", "G8")}

    @property
    def legal_moves(self):
        """Return legal moves from current position."""
        moves = []
        for first_step in ("above", "below"):
            for second_step in ("above_left", "above_right"):
                first_pos = getattr(self.position, first_step)()
                if first_pos:
                    second_pos = getattr(first_pos, second_step)()
                    if second_pos:
                        moves.append(second_pos)
        return moves
