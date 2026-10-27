<!-- {"stage": "synthesis", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 73463, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 56970, "estimated_cost_usd": 1.4589, "message_id": "msg_011CgS6Cuxz8t3gcD9rA9Lsn", "finished_at": "2026-10-27T04:21:18+00:00"} -->

## Cross-part consistency

I checked each report's "Dependencies" against what the cited part proves, using both the reports and the manuscript. I found no parameter or statement mismatch that breaks any implication. The details follow.

**Interfaces that match**

- **`def:layout` (§3) ↔ §4.**
  - §4 provides degree ≤ R−1 (≤ R is required).
  - The row-sum bound D = r^{2Q} is met; actual row sums are ≤ 2^Q.
  - Σ_g c_{t,g} = rhc_B ≤ 2r·ε·M ≤ 2τn with ε = τ/(rb).
  - The kernel condition holds via `lem:swaps-forms` and §4.5.
  - Item 5 is satisfied with O(Q log Q) bits, which is stronger than the required O(Q log Q + log D).
- **§2 overview ↔ §4.**
  - The overview's b = w = 3 gives the hypothesis 12D² ≤ M of `lem:incidence-labels` and ε = τ/(3r).
  - R = 4⌈√λ⌉ is the case β = 1 of `lem:incidence-parameters`, since 16(β+3)²ν = 256ν.
- **`lem:incidence-parameters` ↔ §5.5.**
  - The threshold depends only on β, uniformly in (b, w, M).
  - For large n, β ≤ c+1, so the "finitely many failures" claim holds.
  - M′ ≥ n′ is guaranteed by the neutral factors.
- **`lem:total-order` and `eq:origin-residue` ↔ §3.1 and App. B.**
  - d = k(m_test + 2(ℓ−1)) bounds the degree *over 𝒜_ℓ*, which is what `eq:general-product-degree` requires.
  - App. B's d_H, Δ, Γ and Ω agree with §5.
- **`lem:sparse-checks` and `lem:greedy-hashes` ↔ counters.**
  - These produce ≤ 6n equations with ≤ 2^k·max(D_0, P) = λ^{O_k(1)} monomials each.
  - That fits `thm:overview-sparse-polynomials` (natural-log bound (log n)^c, with c(k) ≥ 6).
  - It also fits `lem:tensor-sparse-query` (bound ⌈log₂n⌉^c).
  - Constant equations, such as rows containing the units {x} and {¬x} (possible because App. A does no unit propagation), are handled by both counters.
- **`lem:sparsify` (statement) ↔ App. A (proof).**
  - App. A gives at most (Cn+1)²·2^{σn} nodes, depth ≤ Cn, B ≤ 4M^{k−1}, and every leaf clause nonempty, so m_G ≤ Bn.
  - This matches every use: §2.8, `prop:interpolation-bound` with σ = 1/s, and App. E with σ = 1/⌈√λ⌉.
- **App. E's use of `lem:total-order` over ℤ/2^p.** This is valid because reduction mod 2^p is a ring homomorphism and the lemma's conclusion is an integer congruence.

**Mismatches to flag (none load-bearing for the ETH refutation)**

1. **Which result proves what.**
   - `thm:main`'s stated exponents (n log log n/√log n in general, n/√log n at fixed density) are proved *only* in App. E.
   - The main-text path (§§3–6, App. A, B) proves only O_k(ρ(n)) (`prop:interpolation-bound`).
   - `cor:quantitative-circuits` depends specifically on App. E's fixed-density bound. From ρ(n) alone one gets only C_L(N) > cN√log N/(log log N)².
   - The other corollaries need only `prop:interpolation-bound`.
   - The Lean statement certifies only the ρ(n) form.
   - The intro, statement, §9 and §10 reports agree on all of this.
2. **§2 introduction overstatement.** It says "taking k=3 already refutes ETH" via §2.8, but §2.8 and `eq:overview-bounded-time` are never formalized. The repair is easy: apply `thm:overview-sparse-polynomials` to Ĝ.
3. **Citation gap for Hermite invertibility.** App. B.3 cites it "in Section 3", but the proof (a divisibility argument) appears only in §2.5.
4. **Two different integer lifts of a parity test.** §2.9 uses Σ v_e; §5.1 uses a count of surviving monomials. Both have the right parity and degree ≤ k. The formal proof uses the second.
5. **Lean proof status.** The statement report presupposes a kernel-checked proof, but no report verifies that the proof builds or which axioms it uses.

## Re-examined issues

**FATAL issues.** No report rated any issue FATAL.

**The sole "GAP" (sec-10, `subsec:tensor-cost`, per-call counts not bounded explicitly): refuted as a GAP; it is MINOR.**
- Nodes of positive multiplicity are at most |S| = 2L ≤ 2s^{1/1000}.
- Interpolation values number M(2L−1)+1, and the paper itself states this is < s⁴ via `eq:tensor-parameter-bounds`.
- Groups number r = 64.
- All three follow directly from the definitions, so no argument is missing.

**Independent re-derivations of the load-bearing steps.** Because of the claim's magnitude, I re-derived the following myself. All are confirmed.

- **Swap construction.**
  - I recomputed the Q = R = 2 example in full. M₀ = Π₁ + Π₂ − Π₁Π₂ has eigenvalues (1, 1, 1, −3) on the characters, so I − M₀ = χ₁₂χ₁₂ᵀ, and the row is ζ₀ − (T/2)ζ₁ − Tζ₂, as stated.
  - `lem:swaps-support`: the summand ∏_{s∉J}Π_s maps u to y with E_{u,y} = {s∈J : a_u(s) ≠ d_u(s)} ⊆ J.
  - (I − M₀) = K·C^𝓑, and φ_{u,y} vanishes exactly on E_{u,y}.
- **Transfer and measurement count.**
  - π_c ι ξ̃ is supported on S^𝓑_{t,g} and lies in ker C^𝓑.
  - rhc_B ≤ 2τn.
  - The measurement exponent is ≈ n/(64r).
- **Counting identities.**
  - Separation identity.
  - deg_X [z^j]𝒢_x ≤ j, by a weight argument independent of cancellation.
  - Möbius / Boolean-difference identity.
  - Uniqueness of Hermite recovery from QJ > d_H.
  - deg_T H ≤ dR via the specialization homomorphism applied to the product formed in 𝒜_ℓ[Y].
- **Parameters.**
  - R²/(8Q) ≥ 16(β+3)²ν.
  - Pr[W ∉ 𝓘] ≤ 1/(br²λ).
  - log₂D ≤ λ/128.
  - q = O(nν/√λ), giving total exponent O(nν²/√λ).
- **`lem:incidence-labels`.** E[Φ] ≤ M(b+w), E[Ξ] = Qn(1−1/r), and the potential stays ≤ 2.
- **Expander code.**
  - Hoeffding exponent 4μ.
  - Local-code count < 2^{d_G/(25B)} ≤ 2^{c_G}.
  - δ(δ−ε) = 1/P.
  - Mixing-lemma distance argument.
- **Greedy step.** Rejection probability ≥ (1−e^{−1})/2 > 1/4, and (27/32)^n < 1.
- **App. A.** The recurrence T_j ≤ 4n·θ_{j−1} + 2Σθ_{j−i}T_i solves to 4·3^{j−1}nM^{j−1}. Units are never deleted because no empty clause is ever inserted.
- **App. E.**
  - Locality of W(t).
  - Crossing implies v₂(t − y₀ + x) ≤ i, so mode coefficients are divisible by 2^{w_Z}.
  - Exactly 6M/D modes per weight.
  - Valuation identity in `eq:tensor-hermite-loss`, with residue counts D/2^j and the bound ≥ −6hD.
  - Child edge count ≤ 3M/32.
  - Geometric summation of exponents (√2/8)^d.

**MINOR issues deserving editorial action.** Correctness is unaffected; classifications unchanged.
- The introduction calls the UGC a "theorem" on the strength of an unrefereed preprint. It is unused in any proof and should be rephrased or removed.
- "(log n)^{1/2+o(1)}" in the abstract and in ρ(n) requires a negative o(1); write 1/2 − o(1).
- "Subexponential perfect matchings" holds only for e = O(v).
- B.4 is only a sketch, but it covers the overview algorithm, not the main path.
- "Sufficiently large n" hides thresholds near n ≳ 2^{2^{33}}. Every feasible input therefore takes the brute-force fallback. The result is purely asymptotic, which suffices for ETH but should be stated.
- There is pervasive notation overloading (D, B, h, 𝒜, J, M, Γ, …).

## Overall assessment

**(a) The paper's proof.**
- No report found a FATAL error. The one GAP is presentational, and my own re-derivation of every load-bearing step found nothing wrong.
- The main path is coherent and complete at the level checked:
  - design construction (§4);
  - shared-measurement separation with Taylor/Boolean-difference recovery and Hermite interpolation (§3);
  - Beigel–Tarui lift truncated in total h-power (§5);
  - Tanner/expander checks plus greedy parity tests (§6);
  - disjoint sparsification (App. A);
  - exact arithmetic (App. B).
- Together these prove `prop:interpolation-bound`, a deterministic 2^{O_k(ρ(n))}·poly algorithm. That alone refutes ETH, SETH, #ETH, NSETH and Gap-ETH as claimed.
- The sharper exponents in `thm:main`, and the n√log n circuit bound, additionally rest on App. E. It appears correct, but it received only a compressed review and is unformalized.

**(b) The Lean statement.**
- It appears faithful: standard CNF semantics, a uniform deterministic multitape-equivalent machine, an exactly pinned output, an honest step count, and an exponent in n with a poly(n) factor for 3-CNF.
- It captures a refutation of ETH (in the ρ(n) form), modulo routine unformalized facts: polynomial-time canonical re-encoding and TM/RAM robustness.
- If the accompanying proof kernel-checks, the ETH refutation is settled regardless of prose gaps. No report verified that it does.

**(c)** See below.

## What humans should check

1. **Lean verification.** This is decisive for the ETH claim. Build the project from a clean checkout with pinned Lean and Mathlib versions. Confirm:
   - no `sorry` or `admit`;
   - `#print axioms` on the main theorem shows only `propext`, `Classical.choice` and `Quot.sound`;
   - no `native_decide` or `Lean.ofReduceBool`, and no `implemented_by` or `extern` in the proof path;
   - no custom axioms or `opaque` tricks;
   - the trusted statement file is byte-identical to the one reviewed.
2. **If the Lean proof is not confirmed: independent expert verification of the main path.** Priorities:
   - `lem:swaps-matrix`, `lem:swaps-support`, `lem:swaps-forms` and the §4.5 transfer (the novel core);
   - `prop:general-count` together with `lem:boolean-differences`;
   - `lem:total-order` and its use as the degree hypothesis over 𝒜_ℓ;
   - `lem:sparse-checks` and `lem:greedy-hashes`;
   - App. A.

   An end-to-end implementation test on small artificial parameters would be valuable. The paper's parameters cannot be tested this way, since they apply only astronomically late, but the identities can be checked independently of them.
3. **App. E (unformalized, compressed review).** Check the tapered-Hermite precision accounting (`eq:tensor-precision-bound`), the canonical-lift consistency across recursion levels, the mode factorization (`eq:tensor-recursion-identity`), and the global call count. This is required for `thm:main` as stated and for `cor:quantitative-circuits`.
4. **External citations used in proofs.**
   - [Wil13, Thm 6.1]: its exact hypothesis.
   - [JMV13, Thm 1]: index length, decision-tree depth and label length.
   - Žák's hierarchy in unary form.
   - [BT94]: provenance only.
5. **Editorial corrections.** Remove or rephrase the UGC claim; fix the o(1) sign; state where the thresholds and fallback apply; make the choice of c(k) explicit in §6.3; make the §2.8 claim formal or soften it.

VERDICT: PROOF-APPEARS-CORRECT
