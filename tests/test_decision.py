from csdr.state import AppState
from csdr.decision import Decision, decide


# Tests using default thresholds (calibrated for TF-IDF retrieval)

def test_low_evidence_abstains():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.05,
    )

    assert decide(state) == Decision.ABSTAIN


def test_strong_evidence_answers():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.35,
    )

    assert decide(state) == Decision.ANSWER


def test_marginal_evidence_retrieves_more():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.20,
    )

    assert decide(state) == Decision.RETRIEVE_MORE


def test_exact_threshold_answers():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.25,
    )

    assert decide(state) == Decision.ANSWER


def test_just_below_threshold_retrieves():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.249,
    )

    assert decide(state) == Decision.RETRIEVE_MORE


def test_zero_score_abstains():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.0,
    )

    assert decide(state) == Decision.ABSTAIN


def test_exact_lower_threshold_retrieves():
    state = AppState(
        question="What is the policy?",
        retrieval_score=0.15,
    )

    assert decide(state) == Decision.RETRIEVE_MORE


# Tests with explicit thresholds (illustrative values from TN-001)

def test_custom_thresholds():
    state = AppState(question="test", retrieval_score=0.60)
    assert decide(state, abstain_below=0.50, answer_above=0.72) == Decision.RETRIEVE_MORE

    state = AppState(question="test", retrieval_score=0.80)
    assert decide(state, abstain_below=0.50, answer_above=0.72) == Decision.ANSWER

    state = AppState(question="test", retrieval_score=0.31)
    assert decide(state, abstain_below=0.50, answer_above=0.72) == Decision.ABSTAIN
