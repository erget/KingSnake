"""Errors for chess game"""


class IllegalMoveError(Exception):
    """Proposed move is illegal."""


class IllegalCaptureError(Exception):
    """Proposed capture is illegal."""


class TurnError(Exception):
    """Player tried to play out of order."""


class FieldOccupiedError(Exception):
    """Goal field is occupied."""


class FieldMustBeCastledError(Exception):
    """King is being moved and the field is only available for castling."""
