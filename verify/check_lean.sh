#!/usr/bin/env bash
# Mechanical (non-LLM) checks of the Lean formalization of "The Exponential Time Hypothesis
# is False". Run from anywhere; needs `lake`/`lean`/`leanchecker` (Lean 4.34.1) on PATH.
#
#   1. build the solution (OAI) and the trusted challenge statement
#   2. compare the solution against the challenge statement and check its axioms
#      (verify/CompareDecls.lean, driven by the repository's Comparator config)
#   3. replay every SubexponentialSAT declaration through the Lean kernel (leanchecker)
#   4. negative controls: two mutated challenges that step 2 must reject
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
cd "$here/../lean"
config=ComparatorChallenges/SubexponentialSAT.json
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

step() { printf '\n== %s\n' "$*"; }

step "1. lake build OAI ComparatorChallenges"
lake build OAI ComparatorChallenges 2>&1 | tee "$work/build.log" | grep -E "^(error|✖)|Build completed" || true
if grep -qE "^(error|✖)" "$work/build.log"; then
  echo "build failed"; exit 1
fi
echo "sorry warnings outside the challenge file: $(grep "declaration uses 'sorry'" "$work/build.log" | grep -vc ComparatorChallenges || true)"
# Lake leaves a ~6 MB `.setup.json` per module in .lake/build/ir (about 18 GB for this
# project). They are only inputs for compiling a module and are rewritten on a rebuild.
find .lake/build/ir -name '*.setup.json' -delete

step "2. statement comparison and axioms ($config)"
lake env lean --run "$here/CompareDecls.lean" "$config"

step "3. kernel replay: leanchecker OAI.Algorithms.SubexponentialSAT"
time lake env leanchecker OAI.Algorithms.SubexponentialSAT
echo "leanchecker: all SubexponentialSAT modules replayed without error"

step "4. negative controls (each must be rejected)"
mkdir -p "$work/neg/ComparatorChallenges"
mutate() {  # name, sed expression
  local src="$work/neg/ComparatorChallenges/$1.lean"
  sed "$2" ComparatorChallenges/SubexponentialSAT.lean > "$src"
  if cmp -s "$src" ComparatorChallenges/SubexponentialSAT.lean; then
    echo "mutation $1 did not change the file"; exit 1
  fi
  lake env lean -o "$work/neg/ComparatorChallenges/$1.olean" "$src" > /dev/null 2>&1
  sed "s/ComparatorChallenges.SubexponentialSAT\"/ComparatorChallenges.$1\"/" "$config" > "$work/$1.json"
  if lake env bash -c "LEAN_PATH=\"$work/neg:\$LEAN_PATH\" lean --run \"$here/CompareDecls.lean\" \"$work/$1.json\"" > "$work/$1.out" 2>&1; then
    echo "NEGATIVE CONTROL $1 WAS ACCEPTED"; cat "$work/$1.out"; exit 1
  fi
  echo "rejected as expected: $1 -> $(grep -m1 FAIL "$work/$1.out")"
}
# A supporting definition changes (clause width bound k -> k + 1).
mutate MutatedDefinition 's/def WidthAtMost (k : ℕ) (F : CNF V) : Prop := ∀ C ∈ F, C.card ≤ k$/def WidthAtMost (k : ℕ) (F : CNF V) : Prop := ∀ C ∈ F, C.card ≤ k + 1/'
# The theorem statement changes (count-word length bound n + 1 -> n + 2).
mutate MutatedStatement 's/(countWord (SAT.count F)).length ≤ n + 1 ∧/(countWord (SAT.count F)).length ≤ n + 2 ∧/'

step "ALL CHECKS PASSED"
