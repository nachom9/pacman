"""Score, lives and cheats of a whole game, shared by all its levels."""


class GameStats:
    """Score, remaining lives and cheat settings of the current game.

    One GameStats is created when a game starts and is passed to every
    level, so these values are kept from one level to the next.
    """

    def __init__(self, lives: int) -> None:
        """Start a new game.

        Args:
            lives: Number of lives the player starts with.
        """
        self.score: int = 0
        self.lives: int = lives
        self.cheat_mode: bool = False
        self.ghosts_frozen: bool = False
