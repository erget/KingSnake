"""King chess piece."""

from figure import RelevantHistoryFigure


class King(RelevantHistoryFigure):

    """King chess piece."""

    start_position = {"white": ["E1"],
                      "black": ["E8"]}

    def __init__(self, player):
        super(King, self).__init__(player)

    @property
    def in_check(self):
        """Test if king is in check."""

    def castle(self):
        """Castle king."""
