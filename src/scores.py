import json

def load_scores(file_name: str):
    try:
        with open(file_name, encoding="utf-8") as f:
            scores = json.load(f)
    except (OSError, ValueError):
        return []
    if not isinstance(scores, list):
        return []
    scores = [
        score for score in scores
        if isinstance(score, dict)
        and isinstance(score.get("name"), str)
        and isinstance(score.get("score"), int)
        ]
    return scores

def save_score(name: str, score: int, file_name: str):
    scores = load_scores(file_name)

    score_data = {"name": name, "score": score}

    scores.append(score_data)
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError as e:
        print(f"[scores] Warning: cannot save scores: {error.strerror}",
              file=sys.stderr)
