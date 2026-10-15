import json
import sys

MAX_NAME_LENGTH = 10
MAX_SCORES = 10


def is_valid_entry(entry) -> bool:
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


def load_scores(file_name: str):
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

def save_score(name: str, score: int, file_name: str):
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
