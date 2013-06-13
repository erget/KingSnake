"""Pawn chess piece."""

from figure import Figure
from .queen import Queen


class Pawn(Figure):

    """Pawn chess piece."""

    start_position = {"white": list(letter + "2" for letter in "ABCDEFGH"),
                      "black": list(letter + "7" for letter in "ABCDEFGH")}

    def __init__(self, player):
        super(Pawn, self).__init__(player)
        self.en_passant_ready = False
        self.can_be_taken_en_passant = True

    @property
    def legal_moves(self):
        """
        Return legal moves from current position.

        If pawn has already moved, it has a range of one square. Otherwise it
        has a range of two squares. Also, if the adjacent squares in the pawn's
        capture directions contain players, those fields are added to the legal
        moves.
        """
        if self.color == "white":
            capture_directions = "above_left", "above_right"
        else:
            capture_directions = "below_left", "below_right"

        if self.already_moved:
            move_range = 1
        else:
            move_range = 2
        moves = self._fields_in_directions(["above"], move_range)
        for field in self._fields_in_directions(capture_directions, 1):
            if field and field.figure:
                moves.append(field)
        return moves

    def move(self, field):
        """Move to field, become queen if possible and track en passant."""
        if self.color == "white":
            last_row = 8
            en_passant_row = 5
            first_jump_row = 4
        else:
            last_row = 1
            en_passant_row = 4
            first_jump_row = 5

        super(Pawn, self).move(field)
        # Become Queen if Pawn has reached last_row
        if self.position.number == last_row:
            self = Queen(self.player, self.position)
        # Be ready to en passant if in piece's fifth rank
        elif self.position.number == en_passant_row:
            self.en_passant_ready = True
        # Be ready to be en passant'd if conditions match
        elif self.position.number == first_jump_row and not self.already_moved:
            self.can_be_taken_en_passant = True
