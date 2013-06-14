"""Errors for chess game"""


class ChessError(Exception):
    """An error related to chess."""


class IllegalMoveError(ChessError):
    """Proposed move is illegal."""


class IllegalCaptureError(ChessError):
    """Proposed capture is illegal."""


class TurnError(ChessError):
    """Player tried to play out of order."""


class FieldOccupiedError(ChessError):
    """Goal field is occupied."""


class FieldMustBeCastledError(ChessError):
    """King is being moved and the field is only available for castling."""


class PawnMustCaptureError(ChessError):
    """A Pawn has to capture when moving diagonally."""
