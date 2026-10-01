from enum import Enum

from csdr.state import AppState


class Decision(str, Enum):
    ANSWER = "answer"
    RETRIEVE_MORE = "retrieve_more"
    ABSTAIN = "abstain"


DEFAULT_ABSTAIN_THRESHOLD = 0.15
DEFAULT_ANSWER_THRESHOLD = 0.25


def decide(
    state: AppState,
    abstain_below: float = DEFAULT_ABSTAIN_THRESHOLD,
    answer_above: float = DEFAULT_ANSWER_THRESHOLD,
) -> Decision:
    if state.retrieval_score < abstain_below:
        return Decision.ABSTAIN

    if state.retrieval_score < answer_above:
        return Decision.RETRIEVE_MORE

    return Decision.ANSWER
