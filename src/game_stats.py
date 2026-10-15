"""Score and lives of a whole game, shared by all its levels."""


class GameStats:
    """Score and remaining lives of the current game.

    One GameStats is created when a game starts and is passed to every
    level, so the score and the lives are kept from one level to the next.
    """

    def __init__(self, lives: int) -> None:
        """Start a new game.

        Args:
            lives: Number of lives the player starts with.
        """
        self.score: int = 0
        self.lives: int = lives
