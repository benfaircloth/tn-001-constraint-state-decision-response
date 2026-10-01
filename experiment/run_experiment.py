"""Run the three-architecture experiment from TN-001.

Architecture 1: Model decides everything (retrieval + decision + response).
Architecture 2: Application decides answerability, model generates.
Architecture 3: Same as 2, but response must identify supporting evidence.

Usage:
    python -m experiment.run_experiment [--runs 5] [--output results.csv]
"""

import argparse
import csv
import json
import sys
from pathlib import Path

from csdr.state import AppState
from csdr.decision import Decision, decide
from csdr.retrieval import retrieve


def architecture_1(question: str, docs: list[str], score: float) -> dict:
    """Model decides everything. No application-level constraints."""
    context = "\n\n".join(docs)
    response = (
        f"[Arch 1] Given the context, here is my answer to: {question}\n"
        f"The retrieved documents suggest the following. "
        f"(In a real system, an LLM would generate this response.)"
    )
    return {
        "decision": "model_decided",
        "response": response,
        "supported_claims": "unknown",
        "unsupported_claims": "unknown",
    }


def architecture_2(question: str, docs: list[str], score: float) -> dict:
    """Application decides answerability. Model generates only after ANSWER."""
    state = AppState(
        question=question,
        retrieved_docs=docs,
        retrieval_score=score,
    )
    decision = decide(state)

    if decision == Decision.ABSTAIN:
        response = "I don't have enough evidence to answer that reliably."
    elif decision == Decision.RETRIEVE_MORE:
        response = "I need additional evidence before answering."
    else:
        context = "\n\n".join(docs)
        response = (
            f"[Arch 2] Based on retrieved evidence: {question}\n"
            f"(In a real system, an LLM would generate this response "
            f"using the retrieved documents.)"
        )

    return {
        "decision": decision.value,
        "response": response,
        "supported_claims": "not_tracked",
        "unsupported_claims": "not_tracked",
    }


def architecture_3(question: str, docs: list[str], score: float) -> dict:
    """Application decides. Response must cite evidence."""
    state = AppState(
        question=question,
        retrieved_docs=docs,
        retrieval_score=score,
    )
    decision = decide(state)

    if decision == Decision.ABSTAIN:
        response = "I don't have enough evidence to answer that reliably."
        supported = 0
        unsupported = 0
    elif decision == Decision.RETRIEVE_MORE:
        response = "I need additional evidence before answering."
        supported = 0
        unsupported = 0
    else:
        response = (
            f"[Arch 3] Based on retrieved evidence: {question}\n"
            f"Evidence: {docs[0][:80]}...\n"
            f"(In a real system, an LLM would generate this response "
            f"and explicitly cite the supporting documents.)"
        )
        supported = 1
        unsupported = 0

    return {
        "decision": decision.value,
        "response": response,
        "supported_claims": str(supported),
        "unsupported_claims": str(unsupported),
    }


ARCHITECTURES = {
    "arch_1_model_decides": architecture_1,
    "arch_2_app_decides": architecture_2,
    "arch_3_app_decides_with_evidence": architecture_3,
}


def main():
    parser = argparse.ArgumentParser(description="Run the CSDR experiment")
    parser.add_argument("--runs", type=int, default=5, help="Runs per question per architecture")
    parser.add_argument("--output", type=str, default="results.csv", help="Output CSV path")
    args = parser.parse_args()

    questions_path = Path(__file__).parent / "questions.json"
    questions = json.loads(questions_path.read_text())

    rows = []
    for q in questions:
        docs, score = retrieve(q["question"])
        for arch_name, arch_fn in ARCHITECTURES.items():
            for run_num in range(1, args.runs + 1):
                result = arch_fn(q["question"], docs, score)
                rows.append({
                    "question_id": q["id"],
                    "question": q["question"],
                    "architecture": arch_name,
                    "run": run_num,
                    "retrieval_score": f"{score:.4f}",
                    "decision": result["decision"],
                    "supported_claims": result["supported_claims"],
                    "unsupported_claims": result["unsupported_claims"],
                })

    fieldnames = [
        "question_id", "question", "architecture", "run",
        "retrieval_score", "decision", "supported_claims", "unsupported_claims",
    ]
    output_path = Path(args.output)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")
    print(f"  Questions: {len(questions)}")
    print(f"  Architectures: {len(ARCHITECTURES)}")
    print(f"  Runs per combination: {args.runs}")


if __name__ == "__main__":
    main()
