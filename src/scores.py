"""Load and save the highscores (top 10) in a JSON file."""

import json
import sys
from typing import Any

MAX_NAME_LENGTH = 10
MAX_SCORES = 10


def is_valid_entry(entry: object) -> bool:
    """Return True if a highscore entry read from the file can be used.

    The name must have 1 to 10 characters, only letters, digits and
    spaces. The score must be a non-negative integer (bool is rejected,
    because in Python True and False are also ints).
    """
    if not isinstance(entry, dict):
        return False
    name = entry.get("name")
    score = entry.get("score")
    if not isinstance(name, str) or not 1 <= len(name) <= MAX_NAME_LENGTH:
        return False
    if not all(char.isalnum() or char == " " for char in name):
        return False
    if isinstance(score, bool) or not isinstance(score, int):
        return False
    return score >= 0


def load_scores(file_name: str) -> list[dict[str, Any]]:
    """Read the highscores file.

    Any problem (missing file, invalid JSON, wrong format) gives an empty
    list instead of an error. Invalid entries are skipped.

    Args:
        file_name: Path of the highscores JSON file.

    Returns:
        The valid entries, best score first, at most MAX_SCORES.
    """
    scores: list[dict[str, Any]]
    try:
        with open(file_name, encoding="utf-8") as f:
            scores = json.load(f)
    except (OSError, ValueError, RecursionError):
        return []
    if not isinstance(scores, list):
        return []
    scores = [entry for entry in scores if is_valid_entry(entry)]
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:MAX_SCORES]


def save_score(name: str, score: int, file_name: str) -> None:
    """Add a score to the file, keeping only the best MAX_SCORES.

    If the file cannot be written, a warning is printed and the game goes
    on.

    Args:
        name: Player name.
        score: Final score of the game.
        file_name: Path of the highscores JSON file.
    """
    scores = load_scores(file_name)

    score_data = {"name": name, "score": score}

    scores.append(score_data)
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:MAX_SCORES]
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError as error:
        print(f"[scores] Warning: cannot save scores: {error.strerror}",
              file=sys.stderr)
