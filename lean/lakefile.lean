import Lake

open System Lake DSL

-- Slimmed from the upstream openai/math `lean/lakefile.lean`: only the
-- `SubexponentialSAT` formalization (ETH disproof) is kept, and it depends on
-- nothing beyond Mathlib, so all other `require`s and dependency patches are gone.
package OAI where
  version := v!"0.1.0"
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

@[default_target] lean_lib OAI

lean_lib ComparatorChallenges where globs := #[`ComparatorChallenges.+]
