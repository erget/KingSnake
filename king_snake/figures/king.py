"""King chess piece."""

from figure import Figure


class King(Figure):

    """King chess piece."""

    start_position = {"white": ["E1"],
                      "black": ["E8"]}

    def __init__(self, player):
        super(King, self).__init__(player)

    @property
    def in_check(self):
        """Test if king is in check."""
        for figure in self.player.other_player.figures:
            if self.position in figure.legal_moves():
                return True

    def castle(self):
        """Castle king."""
