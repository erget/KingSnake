"""A chess player."""

from king_snake.exceptions import (FieldOccupiedError,
                                   IllegalMoveError,
                                   TurnError)
from king_snake.figures import Pawn, Rook, Knight, Bishop, Queen, King


class Player(object):

    """A chess player."""

    def __repr__(self):
        return "Player()"

    def __str__(self):
        if self.chessboard:
            if self == self.chessboard.players["white"]:
                color = "White"
            else:
                color = "Black"
            return_string = ("{color} Player on "
                             "{chessboard}\n"
                             "Figures: "
                             "{figures}".format(color=color,
                                                chessboard=self.chessboard,
                                                figures=self.figures))
        else:
            return_string = self.__repr__()
        return return_string

    def __init__(self):
        """
        Gather figures and set up player's side of chessboard.
        """
        self.chessboard = None
        self.figures = None
        self.king = None

    def set_up_board(self, chessboard):
        """Set up pieces on given chessboard."""
        self.chessboard = chessboard
        # Create figures
        self.figures = [Pawn(self) for pawns in range(8)]
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
        If yes, roll back the move.

        @param start_field - String used to look up field object (e.g. "E2")
        @param goal_field - Like start_field
        """
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
        except FieldOccupiedError:
            captured_piece = figure.capture(goal_field)
        moved_piece = {"figure": figure, "old_position": start_field}

        if self.king.in_check:
            self.rollback(moved_piece, captured_piece)
            raise IllegalMoveError("Move would put player's king in check.")

        figure.already_moved = True
        self.chessboard.end_turn()

    def rollback(self, moved_piece, captured_piece=None):
        """
        Reverse a turn.

        @param moved_piece - Tuple of piece moved during the move with its old
                             position
        @param captured_piece - Tuple for captured piece, formated as above
        """
        rollback_pieces = [moved_piece]
        if captured_piece:
            rollback_pieces.append(captured_piece)

        for piece in rollback_pieces:
            piece["old_position"].receive_figure(piece["figure"])
            piece["figure"].position = piece["old_position"]
