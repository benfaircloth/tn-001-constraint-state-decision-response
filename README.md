# TN-001: Constraint, State, Decision, Response

Companion code for [Teaching Note 001](https://benfaircloth.com/teaching/tn-001-constraint-state-decision-response/).

A minimal implementation of the CSDR pattern for reasoning about applications built with language models.

## Structure

```
csdr/
  state.py         AppState dataclass
  constraint.py    Evidence sufficiency check
  decision.py      Decision enum and policy
  response.py      Response generation and run() entry point
  retrieval.py     TF-IDF document retrieval

experiment/
  documents/       Synthetic policy documents
  questions.json   Ten questions with varying evidence quality
  run_experiment.py  Three architectures, repeated runs, CSV output
  analyze.py       Summary statistics from experiment results

tests/
  test_decision.py    Decision boundary tests
  test_constraint.py  Constraint enforcement tests
  test_response.py    Response behavior tests
```

## Run the tests

```
pytest
```

## Run the experiment

```
python -m experiment.run_experiment --runs 5 --output results.csv
python -m experiment.analyze --input results.csv
```

The experiment runs three architectures against the same questions:

1. **Model decides everything.** No application-level constraints.
2. **Application decides answerability.** Model generates only after the decision policy permits it.
3. **Application decides with evidence tracking.** Same as 2, but the response must identify supporting evidence.

The default implementation uses placeholder responses. To use a real LLM, replace `generate_answer()` in `csdr/response.py`.

## The point

The value is not the code. The value is making each responsibility visible: what is allowed (constraint), what the system knows (state), what should happen (decision), and what the user receives (response).

If those questions cannot be answered independently, the prompt is carrying responsibilities that belong elsewhere in the system.

## License

MIT

## Author

Ben Faircloth
