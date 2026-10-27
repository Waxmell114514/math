# [Comparator](https://github.com/leanprover/comparator) challenge

With `comparator`, `landrun`, and `lean4export` on `PATH`, from `lean/`:

```sh
lake update
lake env comparator ComparatorChallenges/SubexponentialSAT.json
```

Without them, [`../../verify/check_lean.sh`](../../verify/check_lean.sh) performs the same
statement comparison and axiom check with a small self-contained checker
([`../../verify/CompareDecls.lean`](../../verify/CompareDecls.lean)) and re-checks the proof
with the kernel via `leanchecker`.
