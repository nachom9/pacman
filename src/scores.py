

def load_scores():
    pass


def save_score(name: str, score: int):
    scores = load_scores()
    scores[name] = score
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores[:10]

