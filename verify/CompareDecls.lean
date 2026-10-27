import Lean

/-!
# Challenge/solution declaration comparison

A self-contained stand-in for the core of `leanprover/comparator`, for use when that tool
(and its `landrun` sandbox) is unavailable.  Given a Comparator JSON config it:

1. imports the challenge module and the solution module into two *separate* environments;
2. walks every constant reachable from the listed theorems' statements in the challenge
   environment (through statements, definition bodies, inductive constructors and recursor
   rules — Mathlib and core included) and checks that the solution environment contains a
   declaration of the same name, kind, universe parameters and statement, with the same body
   for definitions (proofs of theorems are irrelevant and are not compared);
3. collects every axiom the solution's theorems depend on (through proofs too) and checks
   them against `permitted_axioms`.

Kernel re-checking of the solution's declarations is done separately with `leanchecker`.

Usage (from `lean/`): `lake env lean --run ../verify/CompareDecls.lean <config.json>`
-/

open Lean

structure Config where
  challenge_module : String
  solution_module : String
  theorem_names : Array String
  permitted_axioms : Array String
  deriving FromJson

/-- Constants that pin down the meaning of `ci`: everything in its statement, plus the body of a
definition, the constructors of an inductive type, and the rules of a recursor. -/
def meaningDeps (ci : ConstantInfo) : Array Name :=
  let used (e : Expr) := e.getUsedConstants
  match ci with
  | .defnInfo v => used v.type ++ used v.value
  | .opaqueInfo v => used v.type ++ used v.value
  | .inductInfo v => used v.type ++ v.all.toArray ++ v.ctors.toArray
  | .ctorInfo v => (used v.type).push v.induct
  | .recInfo v =>
    v.rules.foldl (fun acc r => (acc.push r.ctor) ++ used r.rhs) (used v.type ++ v.all.toArray)
  | _ => used ci.type

/-- Every constant used anywhere in `ci`, proofs included (for axiom collection). -/
def allDeps (ci : ConstantInfo) : Array Name :=
  match ci with
  | .thmInfo v => v.type.getUsedConstants ++ v.value.getUsedConstants
  | _ => meaningDeps ci

def kindName : ConstantInfo → String
  | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque" | .quotInfo _ => "quot" | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor" | .recInfo _ => "recursor"

/-- `none` when `b` (solution) means the same as `a` (challenge); `Expr` equality is
alpha-equivalence. Reducibility hints are ignored; they do not affect what is proved. -/
def compareInfo (a b : ConstantInfo) : Option String :=
  if kindName a != kindName b then
    some s!"kind differs: {kindName a} vs {kindName b}"
  else if a.levelParams != b.levelParams then
    some "universe parameters differ"
  else if !(a.type == b.type) then
    some "statement/type differs"
  else
    match a, b with
    | .defnInfo x, .defnInfo y =>
      if x.value == y.value && x.safety == y.safety then none else some "definition body differs"
    | .opaqueInfo x, .opaqueInfo y =>
      if x.value == y.value && x.isUnsafe == y.isUnsafe then none else some "opaque body differs"
    | .axiomInfo x, .axiomInfo y => if x.isUnsafe == y.isUnsafe then none else some "safety differs"
    | .inductInfo x, .inductInfo y =>
      if x.numParams == y.numParams && x.numIndices == y.numIndices && x.all == y.all &&
          x.ctors == y.ctors && x.numNested == y.numNested && x.isRec == y.isRec &&
          x.isUnsafe == y.isUnsafe && x.isReflexive == y.isReflexive then none
      else some "inductive header differs"
    | .ctorInfo x, .ctorInfo y =>
      if x.induct == y.induct && x.cidx == y.cidx && x.numParams == y.numParams &&
          x.numFields == y.numFields && x.isUnsafe == y.isUnsafe then none
      else some "constructor data differs"
    | .recInfo x, .recInfo y =>
      let sameRules := x.rules.length == y.rules.length &&
        (x.rules.zip y.rules).all fun (r, s) =>
          r.ctor == s.ctor && r.nfields == s.nfields && r.rhs == s.rhs
      if x.all == y.all && x.numParams == y.numParams && x.numIndices == y.numIndices &&
          x.numMotives == y.numMotives && x.numMinors == y.numMinors && x.k == y.k &&
          x.isUnsafe == y.isUnsafe && sameRules then none
      else some "recursor data differs"
    | _, _ => none

def main (args : List String) : IO UInt32 := do
  let [configPath] := args | do
    IO.eprintln "usage: CompareDecls <comparator-config.json>"; return 2
  let cfg ← IO.ofExcept <| (Json.parse (← IO.FS.readFile configPath)) >>= fromJson? (α := Config)
  initSearchPath (← findSysroot)
  let challengeEnv ← importModules #[{ module := cfg.challenge_module.toName }] {}
  let solutionEnv ← importModules #[{ module := cfg.solution_module.toName }] {}
  let challengeIdx := challengeEnv.getModuleIdx? cfg.challenge_module.toName
  let targets := cfg.theorem_names.map String.toName
  let mut failures : Array String := #[]

  -- 1. Same meaning for everything the theorem statements depend on.
  let mut seen : NameSet := {}
  let mut stack := targets
  let mut compared := 0
  let mut fromChallenge := 0
  while h : stack.size > 0 do
    let n := stack.back
    stack := stack.pop
    if seen.contains n then continue
    seen := seen.insert n
    let some a := challengeEnv.find? n | failures := failures.push s!"{n}: missing from challenge"; continue
    if challengeEnv.getModuleIdxFor? n == challengeIdx then fromChallenge := fromChallenge + 1
    match solutionEnv.find? n with
    | none => failures := failures.push s!"{n}: missing from solution"
    | some b =>
      compared := compared + 1
      if let some why := compareInfo a b then failures := failures.push s!"{n}: {why}"
    for d in meaningDeps a do
      unless seen.contains d do stack := stack.push d
  IO.println s!"compared {compared} constants reachable from the challenge statements \
    ({fromChallenge} declared in {cfg.challenge_module}, the rest from Lean/Mathlib)"

  -- 2. The solution actually proves the theorems: they are theorems, not axioms or sorries.
  for t in targets do
    match solutionEnv.find? t with
    | some (.thmInfo _) => pure ()
    | some ci => failures := failures.push s!"{t}: is a {kindName ci} in the solution, not a theorem"
    | none => failures := failures.push s!"{t}: missing from solution"

  -- 3. Axioms used by the solution's proofs.
  let permitted := cfg.permitted_axioms.map String.toName
  let mut axSeen : NameSet := {}
  let mut axioms : Array Name := #[]
  let mut work := targets
  while h : work.size > 0 do
    let n := work.back
    work := work.pop
    if axSeen.contains n then continue
    axSeen := axSeen.insert n
    let some ci := solutionEnv.find? n | continue
    if ci matches .axiomInfo _ then axioms := axioms.push n
    for d in allDeps ci do
      unless axSeen.contains d do work := work.push d
  let used := axioms.qsort Name.lt
  IO.println s!"axioms used by {targets}: {used}"
  for ax in used do
    unless permitted.contains ax do failures := failures.push s!"non-permitted axiom: {ax}"

  if failures.isEmpty then
    IO.println "OK: solution matches the challenge statement and uses only permitted axioms"
    return 0
  else
    for f in failures do IO.eprintln s!"FAIL {f}"
    return 1
