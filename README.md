# The Exponential Time Hypothesis is False — paper, Lean proof, and verification

This branch is a slimmed copy of [openai/math](https://github.com/openai/math) (forked as
`Waxmell114514/math`) that keeps only what concerns family **378, "Disproof of the Exponential
Time Hypothesis"** — the October 25, 2026 manuscript and its Lean formalization — plus tooling to
check them. Everything else from the upstream collection (the other ~720 manuscripts and Lean
developments) is still on `main`.

> **378. Disproof of the Exponential Time Hypothesis.** For every fixed $k\ge2$, a deterministic
> algorithm counts the satisfying assignments of a $k$-CNF with $n$ variables and $m$ clauses in
> time $(n+m)^{O_k(1)}2^{n/(\log n)^{1/2+o(1)}}$. This yields superlinear circuit lower bounds for
> a language in $\mathsf{E}^{\mathsf{NP}}$ on infinitely many input lengths.

## Layout

| Path | Contents |
| --- | --- |
| [`preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/`](preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/) | The paper (`paper.pdf`) and its LaTeX source (`build/`), unchanged from upstream |
| [`lean/`](lean/) | Lean 4 project with only the `SubexponentialSAT` development (unchanged sources) and a Mathlib-only `lakefile.lean` |
| [`lean/ComparatorChallenges/SubexponentialSAT.lean`](lean/ComparatorChallenges/SubexponentialSAT.lean) | The trusted statement of the main theorem, unchanged from upstream |
| [`verify/`](verify/) | Verification tooling and reports (see below) |

All paper and Lean source files are byte-identical to upstream `main`; only the build
configuration (`lean/lakefile.lean`, `lean/lake-manifest.json`, `lean/OAI.lean`,
`lean/formalization.yaml`) and the READMEs were changed. Check with
`git diff --diff-filter=AMR --stat main -- preprints lean/OAI lean/docs lean/ComparatorChallenges/SubexponentialSAT.*`
(prints nothing).

## Verification

Two independent kinds of checks:

1. **Mechanical Lean checks** — [`verify/check_lean.sh`](verify/check_lean.sh): build the
   formalization against Mathlib, compare the solution with the trusted challenge statement and
   list the axioms it uses ([`verify/CompareDecls.lean`](verify/CompareDecls.lean)), replay every
   declaration through the Lean kernel (`leanchecker`), and run two negative controls that the
   comparison must reject.
2. **Referee review by Claude Opus** — [`verify/opus_review.py`](verify/opus_review.py): one
   review of whether the Lean statement faithfully refutes ETH, a line-by-line proof check of each
   of the paper's ten sections/appendices, and a synthesis. Reports go to
   [`verify/reports/`](verify/reports/).

Results are summarized in [`verify/RESULTS.md`](verify/RESULTS.md).

### Reproducing

```sh
# Lean 4.34.1 toolchain on PATH (lake, lean, leanchecker)
cd lean && lake update && cd ..
verify/check_lean.sh

pip install anthropic
ANTHROPIC_API_KEY=... python3 verify/opus_review.py          # all stages; finished ones are skipped
python3 verify/opus_review.py --list                         # stage names
python3 verify/opus_review.py --only statement --force       # re-run one stage
```

## License and citation

Content is from [openai/math](https://github.com/openai/math) under its [LICENSE](LICENSE); see
the paper's [README](preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/README.md)
for the citation.
