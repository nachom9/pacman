import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

KNOWN_KEYS = (
    "highscore_filename",
    "lives",
    "points_per_pacgum",
    "points_per_super_pacgum",
    "points_per_ghost",
    "seed",
    "level_max_time",
    "levels",
)

MIN_LEVELS = 10
MIN_MAZE_SIZE = 5
MAX_MAZE_SIZE = 20
DEFAULT_WIDTH = 15
DEFAULT_HEIGHT = 15


class ConfigError(Exception):
    """Raised when the configuration file cannot be used at all."""


@dataclass
class LevelConfig:
    """Maze size of a single level."""

    width: int
    height: int


def _default_levels() -> list[LevelConfig]:
    """Return the default list of levels."""
    return [
        LevelConfig(DEFAULT_WIDTH, DEFAULT_HEIGHT) for _ in range(MIN_LEVELS)
    ]


class ConfigLoader:
    """Load the configuration file and keep its validated values."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.highscore_filename: str = "highscores.json"
        self.lives: int = 3
        self.points_per_pacgum: int = 10
        self.points_per_super_pacgum: int = 50
        self.points_per_ghost: int = 200
        self.seed: int = 42
        self.level_max_time: int = 90
        self.levels: list[LevelConfig] = _default_levels()

    def load_config(self) -> None:
        text = self._read_text()
        raw = self._parse_json(text)
        self._build_config(raw)

    def _read_text(self) -> str:
        """Return the content of the file or raise ConfigError."""
        path = self.file_path
        if Path(path).suffix != ".json":
            raise ConfigError(f"'{path}' is not a .json file")
        try:
            with open(path, encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise ConfigError(f"'{path}' does not exist") from None
        except IsADirectoryError:
            raise ConfigError(f"'{path}' is a directory") from None
        except PermissionError:
            raise ConfigError(f"no permission to read '{path}'") from None
        except UnicodeDecodeError:
            raise ConfigError(f"'{path}' is not a text file") from None
        except OSError as error:
            raise ConfigError(
                f"cannot read '{path}': {error.strerror}"
            ) from None

    def _strip_comments(self, text: str) -> str:
        """Blank out comment lines, keeping line numbers unchanged."""
        kept = []
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                kept.append("")
            else:
                kept.append(line)
        return "\n".join(kept)

    def _parse_json(self, text: str) -> dict[str, Any]:
        """Parse the text as JSON and check that it is an object."""
        path = self.file_path
        try:
            data = json.loads(self._strip_comments(text))
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"invalid JSON in '{path}' at line {error.lineno}: "
                f"{error.msg}"
            ) from None
        if not isinstance(data, dict):
            raise ConfigError(f"'{path}' must contain a JSON object {{...}}")
        return data

    def is_string(self, value: Any, key: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            print(
                f"[config] Warning: '{key}' must be a "
                f"non-empty string, using {getattr(self, key)!r}",
                file=sys.stderr,
            )
            return False
        return True

    def is_number(self, value: Any, key: str) -> bool:
        if not isinstance(value, int) or isinstance(value, bool):
            print(
                f"[config] Warning: '{key}' must be an integer, "
                f"using {getattr(self, key)!r}",
                file=sys.stderr,
            )
            return False
        return True

    def _check_levels(self, value: Any) -> None:
        if not isinstance(value, list):
            print(
                "[config] Warning: 'levels' must be a list, "
                f"using {MIN_LEVELS} default levels "
                f"({DEFAULT_WIDTH}x{DEFAULT_HEIGHT})",
                file=sys.stderr,
            )
            return

        levels: list[LevelConfig] = []
        for index, item in enumerate(value):
            name = f"levels[{index}]"
            if not isinstance(item, dict):
                print(
                    f"[config] Warning: '{name}' must be an object "
                    '{"width": ..., "height": ...}, level skipped',
                    file=sys.stderr,
                )
                continue
            width = self._check_size(item, "width", DEFAULT_WIDTH, name)
            height = self._check_size(item, "height", DEFAULT_HEIGHT, name)
            levels.append(LevelConfig(width, height))

        if len(levels) < MIN_LEVELS:
            missing = MIN_LEVELS - len(levels)
            print(
                f"[config] Warning: only {len(levels)} valid levels, "
                f"adding {missing} default levels "
                f"({DEFAULT_WIDTH}x{DEFAULT_HEIGHT})",
                file=sys.stderr,
            )
            for _ in range(missing):
                levels.append(LevelConfig(DEFAULT_WIDTH, DEFAULT_HEIGHT))

        self.levels = levels

    def _check_size(
        self, level: dict[str, Any], key: str, default: int, name: str
    ) -> int:
        if key not in level:
            print(
                f"[config] Warning: '{name}.{key}' is missing, "
                f"using {default}",
                file=sys.stderr,
            )
            return default
        size = level[key]
        if not isinstance(size, int) or isinstance(size, bool):
            print(
                f"[config] Warning: '{name}.{key}' must be an integer, "
                f"using {default}",
                file=sys.stderr,
            )
            return default
        if size < MIN_MAZE_SIZE:
            print(
                f"[config] Warning: '{name}.{key}' is below "
                f"{MIN_MAZE_SIZE}, using {MIN_MAZE_SIZE}",
                file=sys.stderr,
            )
            return MIN_MAZE_SIZE
        if size > MAX_MAZE_SIZE:
            print(
                f"[config] Warning: '{name}.{key}' is above "
                f"{MAX_MAZE_SIZE}, using {MAX_MAZE_SIZE}",
                file=sys.stderr,
            )
            return MAX_MAZE_SIZE
        return size
            

    def _build_config(self, raw: dict[str, Any]) -> None:
        """Replace the default values with the valid ones from raw."""
        for key in raw:
            if key not in KNOWN_KEYS:
                print(
                    f"[config] Warning: unknown key '{key}' ignored",
                    file=sys.stderr,
                )

        for key in KNOWN_KEYS:
            if key == "levels":
                if "levels" not in raw:
                    print(
                        "[config] Warning: 'levels' is missing, "
                        f"using {MIN_LEVELS} default levels "
                        f"({DEFAULT_WIDTH}x{DEFAULT_HEIGHT})",
                        file=sys.stderr,
                    )
                else:
                    self._check_levels(raw[key])
                continue
            if key not in raw:
                print(
                     f"[config] Warning: '{key}' is missing, "
                     f"using '{getattr(self, key)}'",
                     file=sys.stderr,
                )
            else:
                value = raw[key]
                if key == "highscore_filename":
                    if self.is_string(value, key):
                        self.highscore_filename = value
                elif key in ["lives",
                             "points_per_pacgum",
                             "points_per_super_pacgum",
                             "points_per_ghost",
                             "seed",
                             "level_max_time"]:
                    if self.is_number(value, key):
                        minimum = 0
                        if key in ("lives", "level_max_time"):
                            minimum = 1
                        if value < minimum:
                            print(
                                f"[config] Warning: '{key}' is below "
                                f"{minimum}, using {minimum}",
                                file=sys.stderr,
                            )
                            value = minimum
                        setattr(self, key, value)
