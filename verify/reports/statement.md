<!-- {"stage": "statement", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 5483, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 86092, "estimated_cost_usd": 1.7694, "message_id": "msg_011CgS257YpZ7bVLKYfcXAMX", "finished_at": "2026-10-27T03:31:33+00:00"} -->

## Findings

**1. Machine model (`PrimitiveMachine`, `Cfg`, `step`, `init`): OK.**
- **Finite control.** `stateCount` and `tapeCount` are fixed numbers belonging to the existentially chosen machine. `transition` is a function on the finite set `Fin stateCount × Option Bool`, so it is a finite table. No arithmetic, random access or oracle power can be hidden in it.
- **Alphabet and tapes.** The alphabet is `Option Bool`: blank `none` (the `Inhabited (Option _)` default used by `Turing.Tape`), `some false` and `some true`. Tapes are Mathlib's bi-infinite `Turing.Tape`.
- **One step.** The machine reads the head symbol of the single tape `scan q`. It then either halts with a Boolean (`.inl b`, tapes unchanged, after which `step = none`), or enters `q'` and executes one `TM0.Stmt` on that same tape: move one cell, or write one symbol.
- **Relation to standard TMs.** This is a deterministic multitape TM whose steps touch a single tape.
  - A standard multitape TM with stay moves simulates it step for step.
  - A standard t-tape step costs O(t) primitive steps.
  - So step counts equal multitape-TM time up to constant factors, and time bounds are meaningful.
- **Input placement.** `init` puts `input.map some` on `inputTape`, with the head on the first bit and blanks elsewhere. All other tapes are blank. The input tape is read-write, which is standard; it only affects the space accounting (Finding 9).

**2. Run semantics (`Trace`, `locatedStep`, monitor): OK.**
- `Trace step t a c` is exact t-step reachability.
- `locatedStep` applies `machine.step` to the config component. `monitor` recomputes the same transition from the *old* configuration, so the `config` component is exactly the machine's run; `position/lower/upper` are pure bookkeeping.
- `Trace.cons` needs `step a = some b`, and halted configurations have no successor. Since `final.config.state = .inl _`, `time` is exactly the halting time of the unique run.
- `time = 0` is impossible, because the initial state is `.inr start`.
- The displacements (`right = +1`) agree with `Tape.mk₁` placing the input at positions `0..L−1`.

**3. Formula semantics and `SAT.count`: OK.**
- A literal is true iff `a v = sign`; a clause is ∃ over its literals; a CNF is ∀ over its clauses. Dot notation resolves to `CNF.eval a F` and `Clause.eval a C` with the correct argument placement.
- The empty clause is false, the empty CNF is true, and tautological clauses are allowed and evaluated correctly.
- `count F` counts all 2^n maps `Fin n → Bool`, including unused declared variables. This is exactly #F of (1.1).
- `WidthAtMost k` counts distinct literals, which is the right notion after deduplication.

**4. Encoding (`encodeCNF`, `formulaBitLength`): OK.**
- **Format.** n is written in unary. Literal code 2v+[positive] is written in unary. Clauses are sorted code lists; the CNF is the sorted (lexicographic `List ℕ` order) list of clause lists. Nesting is self-delimiting via `frame`/`encodeList`.
- **Injectivity.** `literalCode` is injective on `Literal (Fin n)`. Hence `clauseNumbers` and `cnfNumbers` are injective, and the encoding loses no information.
- **No leakage.** The encoding is a fixed polynomial-time canonical form of F, so it reveals nothing about satisfiability.
- **Exact length.** Using |encodeNat c| = c+1, |frame w| = 2|w|+1 and |encodeList| = 1+Σ(2|enc aᵢ|+2):
  L = n + 2 + Σ_{C∈F}(4 + Σ_{ℓ∈C}(4·code(ℓ)+8)).
  Hence n+2+4m ≤ L ≤ n+2+m(4+k(8n+4)).
- **Finsets bound the size.** Because formulas and clauses are `Finset`s, m ≤ Σ_{j≤k} C(2n,j) ≤ (2n+1)^k, so L = n^{O(k)}.
- **Unary codes.** They cost at most a factor O(n) over a binary encoding, which is polynomial.

**5. Output conditions and vacuity: OK.**
- The count tape must equal `Tape.mk₁ ((countWord c).map some)`. This fixes the head position (first bit) and every cell.
- `ListBlank` only identifies trailing blanks, and the word contains no blank, so the tape determines the word. `countWord` (little-endian `Nat.bits`, `[false]` for 0) is injective, so c is pinned down.
- The answer tape and the halting state both carry `decide (0 < c)`.
- `countTape = answerTape` would force `countWord c = [decide (0<c)]`, which is false once c ≥ 2 (e.g. the empty CNF on one variable). So the two outputs cannot collapse.
- All hypotheses are satisfiable (`2 ≤ k`, `WidthAtMost k F`, and the space clause along the run). Nothing is vacuous.

**6. Redundant conjuncts: MINOR.**
`toNat (countWord c) = c` and `(countWord c).length ≤ n+1` do not mention the machine. They are true facts about `Nat.bits` and c ≤ 2^n. They are harmless and document the decoding, but they are not part of the computational claim.

**7. Quantifiers and uniformity: OK.**
`∃ machine countTape answerTape C A S d e` precedes `∀ n F`. There is one machine and one set of constants per k, independent of n and F; the machine reads n from its input.

**8. Time bound: OK (load-bearing).**
- **Form.** `runtimeBound C A d L n = C·(L+1)^d·2^{A·n(ln ln(n+16))²/√ln(n+16)}`, with the arguments in the correct order.
- **Real-number edge cases.** n+16 ≥ 16 gives ln ≥ 2.77, ln ln ≥ 1.02 and √ > 0. Lean's conventions for log of non-positive arguments, x/0 = 0 and √ of negatives therefore never apply. `runtimeScale 0 = 0`, and the bound is always positive.
- **Width ≤ 3.**
  - m ≤ (4n³+5n+3)/3 ≤ 2(n+1)³.
  - Each clause contributes at most 24n+16 to L.
  - Hence L+1 ≤ n+3+48(n+1)⁴ ≤ 51(n+1)⁴.
- **Resulting bound.**
  time ≤ C·51^d·(n+1)^{4d}·2^{A n (ln ln(n+16))²/√ln(n+16)},
  so log₂ time ≤ O(1) + 4d·log₂(n+1) + A·n(ln ln(n+16))²/√ln(n+16) = o(n).
- **Why this is the right shape.** The exponent is in n (number of variables), not in L or m, and the polynomial factor is poly(n). That is what ETH requires.
- **Remark.** The bound is purely asymptotic: even with A = 1, the exponential factor drops below 2^n for large n only when ln n ≳ 5.5·10³. This is irrelevant to ETH.

**9. Space condition: OK.**
- **What it says.** For every prefix j ≤ time, Σ_tapes (upper − lower + 1) ≤ S(L+1)^e. Here [lower, upper] is the hull of 0, every head position so far, and (on the input tape) the input cells [0, L−1].
- **Why it is a genuine space bound.** With unit moves, this hull is exactly the set of cells that held input or were under a head. All other cells keep their initial blank. So it is a genuine space bound that includes the input.
- **Redundancy.** The quantity is monotone, so the ∀-prefix form is equivalent to the bound at `final`.
- **Matches the claim.** Since n+m ≤ L ≤ O(knm+n), this is poly(n,m) space, as claimed in `thm:main`. It is not needed for ETH.

**10. The Lean exponent is ρ(n), not `thm:main`: MINOR for ETH, substantive for the paper.**
- **What is certified.** The Lean exponent n(ln ln n)²/√ln n is the paper's ρ(n) from `prop:interpolation-bound`.
- **What is not.** `thm:main` claims 2^{O_k(n log log n/√log n)} in general and 2^{O_{k,D}(n/√log n)} for m ≤ Dn. Both rest solely on the unformalized Appendix F (`thm:tensor-contraction`, `lem:tensor-sparse-query`); the scope document discloses this.
- **Downstream effect.**
  - `cor:quantitative-circuits` uses the fixed-density case. From the Lean-certified bound, the same argument yields only C_L(n) > c·n√log n/(log log n)².
  - `cor:consequence-circuits`, `cor:max-sat-approximation`, `cor:graph-counting` and `cor:consequence-local-inversion` need only 2^{o(n)} or 2^{O(ρ(n))}.
- **For ETH.** The difference is immaterial: both exponents are o(n).

**11. Other differences from `thm:main` and the scope document: OK.**
- (a) **Polynomial factor.** (L+1)^d versus (n+m)^{O_k(1)} are equivalent, since n+m ≤ L ≤ n+2+m(4+k(8n+4)).
- (b) **Model.** Lean counts TM steps; the paper counts "bit operations". Lean's model is weaker, so its bound is stronger.
- (c) **Input form.** Lean takes deduplicated canonical `Finset` inputs; the paper allows repeated literals and clauses. Normalization is poly-time and count-preserving (the paper does it itself in `prop:interpolation-bound`).
- (d) **Coverage.** Lean covers all n (the paper needs n ≥ 20) and additionally outputs the SAT bit.
- (e) **Scope document.** It matches the Lean statement exactly.

**12. Abstract wording: MINOR.**
"2^{n/(log n)^{1/2+o(1)}}" is correct only if the o(1) term may be negative.
- n log log n/√log n = n/(log n)^{1/2 − lnlnln n/lnln n}.
- ρ(n) has the exponent 1/2 − 2 lnlnln n/lnln n.
- Writing 1/2 − o(1), or the explicit form, would be clearer.

**13. Trust base: OK.**
- All non-Mathlib notions are defined in the trusted file and were checked above.
- The Mathlib pieces (`Turing.Tape`, `TM0.Stmt`, `ListBlank`, `Finset.sort`, `Nat.bits`, `Real.log/sqrt/rpow`) are used with their standard meanings.
- A classical existence proof of a finite transition table suffices, because refuting ETH is an existence claim.

## Implication chain

ETH (IP01; textbook form: "∃δ>0: 3-SAT on n variables and m clauses is not solvable in deterministic time 2^{δn}(n+m)^{O(1)}").

1. **Instantiate.** Apply the theorem with k = 3 to obtain M, `countTape`, `answerTape`, C, A, S, d, e.
2. **Adequacy of the formula model (Finding 3).** Take any 3-CNF φ over x₁..xₙ, possibly with repeated literals or clauses. Let F_φ be its set of literal-sets over `Fin n`. Then F_φ.eval x = φ(x) for every x. Hence `count F_φ` = #φ and `WidthAtMost 3 F_φ` holds.
3. **Encoding robustness.** A deterministic multitape TM E computes `encodeCNF F_φ` from a standard N-bit encoding of φ in time poly(N+n). It does so as follows:
   - compute the codes 2v+s;
   - sort and deduplicate each clause's at most 3 codes;
   - sort and deduplicate the clause lists lexicographically (a poly-time order);
   - write the unary/framed form, leaving the head on the first cell.

   The output length satisfies L+1 ≤ 51(n+1)⁴ (Finding 8).
4. **Determinism (Findings 2 and 5).** M on `encodeCNF F_φ` halts after exactly `time` steps in state `.inl (decide (#φ>0))`.
5. **Arithmetic (Finding 8).** time ≤ C·51^d·(n+1)^{4d}·2^{A·runtimeScale(n)} = 2^{o(n)}.
6. **TM-to-RAM robustness.**
   - The composition E;M is a deterministic multitape TM: one primitive step is one multitape step with stay moves. It runs in poly(N+n) + O(time) steps.
   - A RAM simulates it with O(1) overhead per step (O(log) under log-cost).
   - Polynomial overheads preserve the form 2^{o(n)}·poly(N).
7. **Input size.**
   - For clause-set inputs (the IP01 convention), N = O(n³ log n), so poly(N) = 2^{O(log n)} and the total time is 2^{o(n)}.
   - With repeated clauses, ETH formulations carry a poly(N) or poly(n+m) factor anyway.
8. **Conclusion.**
   - For every δ>0 there is n_δ beyond which the total time is ≤ 2^{δn}·poly(N); smaller n cost O(1)·poly(N). So s₃ = 0 and ETH is false.
   - Randomized ETH also fails, since deterministic algorithms are randomized algorithms.
   - #ETH fails via the count output.
   - The same argument for each fixed k gives c_k·2^{n/2} time, which refutes SETH.

## Verdict

The statement has no loophole:
- standard formula semantics;
- a uniform, deterministic machine equivalent to a multitape TM;
- a uniquely pinned exact output;
- an honest step count;
- an exponent in n with a polynomial factor that is poly(n) for 3-CNF.

If the kernel-checked proof is accepted, ETH (and also SETH and #ETH) is false.

The caveats do not affect ETH:
- It certifies only the weaker ρ(n) bound of `prop:interpolation-bound`. The sharper bounds of `thm:main`, and `cor:quantitative-circuits` as stated, remain uncertified and rest on Appendix F.
- The final step to ETH uses routine, unformalized facts: canonical re-encoding and TM/RAM simulation.
- The theorem applies only to canonical, deduplicated input encodings.

VERDICT: FAITHFUL-WITH-CAVEATS
