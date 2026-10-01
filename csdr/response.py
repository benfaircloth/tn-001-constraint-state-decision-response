from csdr.state import AppState
from csdr.decision import Decision, decide
from csdr.retrieval import retrieve


def generate_answer(question: str, documents: list[str]) -> str:
    context = "\n\n".join(documents)
    return (
        f"Based on the available evidence:\n\n"
        f"{context}\n\n"
        f"Answer: This is a placeholder response to '{question}'. "
        f"Replace generate_answer() with an LLM call for real generation."
    )


def respond(state: AppState) -> str:
    if state.decision == Decision.ABSTAIN:
        return "I don't have enough evidence to answer that reliably."

    if state.decision == Decision.RETRIEVE_MORE:
        return "I need additional evidence before answering."

    return generate_answer(
        question=state.question,
        documents=state.retrieved_docs,
    )


def run(question: str) -> str:
    state = AppState(question=question)

    docs, score = retrieve(question)

    state.retrieved_docs = docs
    state.retrieval_score = score

    state.decision = decide(state)

    return respond(state)
