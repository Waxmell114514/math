# Lean formalization: The Exponential Time Hypothesis is False

This is a slimmed copy of the upstream `lean/` library that keeps only the
`OAI.Algorithms.SubexponentialSAT` development (the import closure of
`OAI/Algorithms/SubexponentialSAT/Main.lean`, 3,091 files) and its Comparator challenge.
It depends on nothing but Mathlib, pinned to the same revision as upstream
(`d13f23b723b8a846827a245b89c10fc7d3f11612`, Lean `v4.34.1`).

- Trusted statement: [`ComparatorChallenges/SubexponentialSAT.lean`](ComparatorChallenges/SubexponentialSAT.lean)
- Main theorem: `OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat` in
  [`OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean`](OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean)
- Scope: [`docs/378.md`](docs/378.md)

```sh
lake update          # fetches Mathlib and downloads its prebuilt cache
lake build OAI ComparatorChallenges
../verify/check_lean.sh   # statement comparison, axioms, kernel replay, negative controls
```

See the [repository README](../README.md) for the verification results.
