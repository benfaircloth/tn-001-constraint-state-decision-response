from dataclasses import dataclass, field


@dataclass
class AppState:
    question: str
    retrieved_docs: list[str] = field(default_factory=list)
    retrieval_score: float = 0.0
    user_role: str = "user"
    decision: str | None = None
