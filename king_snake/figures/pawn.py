# -*- coding: utf-8 -*-
"""Pawn chess piece."""

from .figure import Figure, IllegalCaptureError, PawnMustCaptureError
from .queen import Queen


class Pawn(Figure):

    """Pawn chess piece."""

    start_position = {"white": list(letter + "2" for letter in "ABCDEFGH"),
                      "black": list(letter + "7" for letter in "ABCDEFGH")}

    def __str__(self):
        if self.color == "white":
            string = "♙"
        else:
            string = "♟"
        return string

    def __init__(self, player):
        """Initialize Pawn, set direction and change thresholds by color."""
        super(Pawn, self).__init__(player)
        self.en_passant_ready = False
        self.can_be_taken_en_passant = True
        if self.color == "white":
            self.move_direction = "above"
            self.last_row = 8
            self.en_passant_row = 5
            self.first_jump_row = 4
        else:
            self.move_direction = "below"
            self.last_row = 1
            self.en_passant_row = 4
            self.first_jump_row = 5

    def _finish_turn(self):
        """
        Monitor pawn state changes.

        If Pawn reaches last row, it is exchanged for a Queen. If Pawn is in
        its en passant row, it is ready to perform en passant. If Pawn moves
        two squares on its first move, it can be taken by en passant.
        """

        if self.position.number == self.last_row:
            # Remove self from field and place queen there
            self.position.figure = None
            queen = Queen(self.player, self.position)
            self.position.figure = queen
            # Replace self in player's list with queen
            self.player.figures[self.player.figures.index(self)] = queen

        elif self.position.number == self.en_passant_row:
            self.en_passant_ready = True

        elif (self.position.number == self.first_jump_row and not
              self.already_moved):
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
            movement_direction = "above"
            capture_directions = "above_left", "above_right"
        else:
            movement_direction = "below"
            capture_directions = "below_left", "below_right"

        if self.already_moved:
            move_range = 1
        else:
            move_range = 2
        moves = self._fields_in_directions([movement_direction], move_range)
        for field in self._fields_in_directions(capture_directions, 1):
            if field and self.en_passant_ready or field.figure:
                moves.append(field)
        return moves

    def move(self, field):
        """
        Move to given field.

        can_be_taken_en_passant is always set to False in order to override
        previous settings to true. Otherwise that state would be carried over
        even when it was no longer true.
        """

        self.can_be_taken_en_passant = False
        if (field in self.legal_moves and
                field in self._fields_in_directions([self.move_direction], 2)):
            super(Pawn, self).move(field)
            self._finish_turn()
        else:
            raise PawnMustCaptureError("Pawn can move diagonally only when "
                                       "capturing.")

    def capture(self, field):
        """Capture piece if legal, diagonally adjacent or en passant."""
        if self.color == "white":
            capture_directions = ("above_left", "above_right")
            en_passant_direction = "below"
        else:
            capture_directions = ("below_left", "below_right")
            en_passant_direction = "above"

        if field not in self._fields_in_directions(capture_directions, 1):
            raise IllegalCaptureError("Pawns can only capture forward "
                                      "diagonally.")

        # En passant
        if not field.figure and self.en_passant_ready:
            field.receive_figure(self)
            capture_position = self._fields_in_directions(
                                                 [en_passant_direction], 1)[0]
            capture_figure = capture_position.figure
            if (isinstance(capture_figure, Pawn) and
                capture_figure.can_be_taken_en_passant and
                capture_figure.last_moved == (
                                  self.position.chessboard.current_move - 1)):
                capture_dict = super(Pawn, self).capture(capture_position)
                field.receive_figure(self)
        # Normal capture
        else:
            capture_dict = super(Pawn, self).capture(field)
        self._finish_turn()
        return capture_dict
