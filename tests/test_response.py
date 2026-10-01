from csdr.state import AppState
from csdr.decision import Decision
from csdr.response import respond


def test_abstain_response():
    state = AppState(question="test", decision=Decision.ABSTAIN)
    result = respond(state)
    assert "don't have enough evidence" in result


def test_retrieve_more_response():
    state = AppState(question="test", decision=Decision.RETRIEVE_MORE)
    result = respond(state)
    assert "additional evidence" in result


def test_answer_response():
    state = AppState(
        question="What is the policy?",
        retrieved_docs=["Policy: employees may work remotely."],
        decision=Decision.ANSWER,
    )
    result = respond(state)
    assert "employees may work remotely" in result
