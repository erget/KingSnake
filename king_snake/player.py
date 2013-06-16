"""A chess player."""

from king_snake.errors import (FieldMustBeCastledError,
                               FieldOccupiedError,
                               IllegalMoveError,
                               PawnMustCaptureError,
                               TurnError)
from king_snake.figures import Pawn, Rook, Knight, Bishop, Queen, King


class Player(object):

    """A chess player."""

    def __repr__(self):
        return "Player()"

    def __str__(self):
        if self.chessboard:
            return_string = ("{color} Player on "
                             "{chessboard}\n"
                             "Figures: "
                             "{figures}".format(color=self.color,
                                                chessboard=self.chessboard,
                                                figures=self.figures))
        else:
            return_string = self.__repr__()
        return return_string

    def __init__(self):
        self.chessboard = None
        self.figures = None
        self.king = None
        self.color = None

    @property
    def opponent(self):
        """Return other player in chess game"""
        if self.color == "white":
            return self.chessboard.players["black"]
        else:
            return self.chessboard.players["white"]

    def set_up_board(self, chessboard):
        """Set up pieces on given chessboard and find other player."""
        self.chessboard = chessboard
        if self == self.chessboard.players["white"]:
            self.color = "white"
        else:
            self.color = "black"
        self.figures = list(Pawn(self) for pawns in range(8))
        for doubled_piece in (Rook, Knight, Bishop) * 2:
            self.figures.append(doubled_piece(self))
        self.figures.append(Queen(self))
        self.king = King(self)
        self.figures.append(self.king)

    def move(self, start_field, goal_field):
        """
        Move a piece to a new field.

        First verify if self is the chessboard's current player. Then check if
        a moveable figure is located at the start field. If the piece can be
        moved, move to the goal field, capturing a figure at the goal field if
        necessary. Finally, check if the move would put the own king in check.
        If yes, roll back the move. Otherwise, record the current turn on all
        moved pieces and end the turn.

        @param start_field - String used to look up field object (e.g. "E2")
        @param goal_field - Like start_field
        """
        self.chessboard.start_move(start_field, goal_field)
        if self != self.chessboard.current_player:
            raise TurnError("Move attempted out of turn.")

        start_field = self.chessboard.fields[start_field]
        goal_field = self.chessboard.fields[goal_field]

        figure = start_field.figure
        if not figure in self.figures:
            raise IllegalMoveError("Player does not own a piece at given "
                                   "position.")

        try:
            figure.move(goal_field)
            captured_piece = None
        except (FieldOccupiedError, PawnMustCaptureError):
            captured_piece = figure.capture(goal_field)
        except FieldMustBeCastledError:
            captured_piece = figure.castle(goal_field)

        if self.king.in_check:
            self.chessboard.rollback()
            raise IllegalMoveError("Move would put player's king in check.")

        figure.already_moved = True
        figure.last_moved = self.chessboard.current_move
        if captured_piece:
            captured_piece.last_moved = self.chessboard.current_move
        self.chessboard.end_turn()
