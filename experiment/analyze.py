"""Analyze experiment results from run_experiment.py.

Usage:
    python -m experiment.analyze [--input results.csv]
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Analyze CSDR experiment results")
    parser.add_argument("--input", type=str, default="results.csv", help="Input CSV path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"No results file at {input_path}. Run the experiment first:")
        print("  python -m experiment.run_experiment")
        return

    with input_path.open() as f:
        rows = list(csv.DictReader(f))

    by_arch = defaultdict(list)
    for row in rows:
        by_arch[row["architecture"]].append(row)

    print("=" * 70)
    print("CSDR Experiment Summary")
    print("=" * 70)

    for arch_name in sorted(by_arch):
        arch_rows = by_arch[arch_name]
        decisions = defaultdict(int)
        for row in arch_rows:
            decisions[row["decision"]] += 1

        total = len(arch_rows)
        print(f"\n{arch_name}")
        print(f"  Total runs: {total}")
        for decision, count in sorted(decisions.items()):
            print(f"  {decision}: {count} ({count/total*100:.0f}%)")

    print("\n" + "-" * 70)
    print("Per-question decision consistency (arch_2 and arch_3)")
    print("-" * 70)

    by_question = defaultdict(lambda: defaultdict(list))
    for row in rows:
        if row["architecture"] in ("arch_2_app_decides", "arch_3_app_decides_with_evidence"):
            by_question[row["question_id"]][row["architecture"]].append(row["decision"])

    for q_id in sorted(by_question):
        for arch, decisions in sorted(by_question[q_id].items()):
            unique = set(decisions)
            consistent = "consistent" if len(unique) == 1 else "VARIABLE"
            score = decisions[0] if decisions else "?"
            q_rows = [r for r in rows if r["question_id"] == q_id]
            ret_score = q_rows[0]["retrieval_score"] if q_rows else "?"
            print(f"  {q_id} | {arch:40s} | score={ret_score} | {list(unique)} | {consistent}")


if __name__ == "__main__":
    main()
