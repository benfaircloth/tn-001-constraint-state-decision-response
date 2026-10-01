def evidence_is_sufficient(
    score: float,
    threshold: float = 0.72,
) -> bool:
    return score >= threshold
