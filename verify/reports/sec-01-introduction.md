<!-- {"stage": "sec-01-introduction", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 445, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 12154, "estimated_cost_usd": 0.2705, "message_id": "msg_011CgS4UvNG6enbQxZdA35M8", "finished_at": "2026-10-27T03:52:14+00:00"} -->

## What this part proves

The Introduction states Theorem `thm:main` (deterministic exact #k-SAT in $(n+m)^{O_k(1)}2^{O_k(n\log\log n/\sqrt{\log n})}$ time and polynomial space, improving to $2^{O_{k,D}(n/\sqrt{\log n})}$ when $m\le Dn$) and defines $\rho(n)$. It then proves three corollaries:

- `cor:max-sat-approximation`: Max-$k$-SAT within additive $\varepsilon m$ of OPT.
- `cor:graph-counting`: counting independent sets, $q$-colorings and perfect matchings.
- `cor:quantitative-circuits`: stated here, proved in the appendix.

It also asserts consequences for ETH, SETH, Gap-ETH, NSETH, #ETH and the randomized variants.

## Dependencies on other parts

- **Theorem `thm:main`.** Both bounds are proved in Appendix `app:quantitative`, via `thm:tensor-contraction`, `lem:tensor-sparse-query` and §`subsec:sharp-fixed-density`. Every corollary here relies on it for all $n\ge20$, fixed $k\ge2$ and arbitrary $m$, and on the fixed-density bound with $D=5$, $k=3$. Nothing in this part verifies it.
- **Proposition `prop:interpolation-bound`.** Its exponent $O_k(\rho(n))$ is quoted only as a weaker remark.
- **Corollary `cor:quantitative-circuits`.** Its proof is in Appendix `subsec:circuit-lower-bounds` and needs the fixed-density solver in time $V^b2^{AV/\sqrt{\log_2V}}$ for $3$-CNFs with at most $5V$ clauses.
- **External results:**
  - [Bar23, Lemmas 15.9–15.10], the parsimonious circuit-to-3CNF reduction (Tseitin).
  - [JVV86, Thm 3.3(1)].
  - [Wil13, Thm 6.1].
  - [CDL16, Obs. 3.6].
  - [OpenAIUGC26], cited but not used in any proof.

## Detailed verification

**Theorem `thm:main` (statement).**
- The quantifiers are consistent with the appendix proofs.
- The polynomial factor $(n+m)^{O_k(1)}$ is harmless, since after normalization $m\le(2n)^k$.
- For 3-SAT, $2^{o(n)}$ for every $\delta>0$ refutes ETH as stated in the abstract.
- The phrase "$n/(\log n)^{1/2+o(1)}$" (abstract and the definition of $\rho$) is only formally correct. Since $(\log\log n)^2=(\log n)^{o(1)}$, the honest exponent is $1/2-o(1)$; see Issue 1.

**Sampling remark.** With exact counts, bitwise conditional sampling is exactly uniform, so the citation of JVV86 is fine.

**Corollary `cor:max-sat-approximation`.** All steps check out.
- *Sample size and union bound.* Take $s=Cn/\varepsilon^2$. Hoeffding gives failure probability at most $2e^{-s\varepsilon^2/2}=2e^{-Cn/2}$ for each $x$. The union bound over $2^n$ assignments is $2^{-\Omega(n)}$ for large $C$.
- *Approximation chain.* $f(\hat x)\ge\hat f(\hat x)-\varepsilon/2\ge\hat f(x^*)-\varepsilon/2\ge f(x^*)-\varepsilon$. This is correct.
- *Circuit size.* Evaluating the clauses takes $O(ks)$ gates and counting $s$ bits against a threshold takes $O(s)$ gates, for $O_{k,\varepsilon}(n)$ in total.
- *Reduction.* The Tseitin reduction gives $N=O_{k,\varepsilon}(n)$ variables at constant density. Theorem `thm:main` then yields $2^{O(N/\sqrt{\log N})}\le2^{O_{k,\varepsilon}(\rho(n))}$.
- *Search.* Binary search costs $O(\log s)$ calls. Self-reduction on the 3-CNF yields $\hat x$ by restriction to the original variables.
- *Rejection sampling.* Truncating after $n+\log s$ trials adds failure probability at most $s\cdot2^{-(n+\log s)}=2^{-n}$.

**Corollary `cor:graph-counting`.**
- *Independent sets.* The 2-CNF has $v$ variables and $e\le v^2$ clauses, so the polynomial factor is $\mathrm{poly}(v)$ and the time is $2^{o(v)}$.
- *$q$-colorings.* The encoding uses one width-$q$ clause per vertex, $O(q^2v)$ pairwise exclusions and $qe$ edge clauses, with $k=q$. This gives $2^{o(qv)}=2^{o(v)}$ for fixed $q$. The encoding is parsimonious.
- *Perfect matchings.* The exactly-one circuits have total size $O(\sum\deg)=O(v+e)$. The gate values are determined by the edge bits, so the encoding is parsimonious and the time is $2^{o(v+e)}$, as stated.
- *Small inputs.* The case $n<20$ is handled by brute force.

**Corollary `cor:quantitative-circuits`.** Checked against its appendix proof as far as the parameters go.
- *Size of the test formula.* $U_n=3s_n+Bn=(3\eta+o(1))n\sqrt{\log_2n}$.
- *Running time.* The time is $2^{AU_n/a(U_n)}=2^{(3A\eta+o(1))n}$. With $\eta<1/(12A)$ this is below $2^{n/4}$, so the machine runs in $\mathrm{NTIME}(2^{n/2})$ and contradicts Žák's hierarchy.
- *Conversion to the stated form.* At $N=dn$, $s_n\sim\eta(N/d)\sqrt{\ln N/\ln2}$, which gives $c<\eta/(d\sqrt{\ln 2})$. This matches the proof.
- *Clause encoding.* Four clauses per arbitrary fan-in-2 gate suffice.
- *Witness language.* $W\in\mathrm E^{\mathrm{NP}}$ via prefix search.

The corollary follows, conditional on the fixed-density part of `thm:main`.

**Hypotheses refuted.**
- A deterministic $2^{o(n)}$ decision procedure for each fixed $k$ refutes ETH, SETH, the randomized variants and #ETH. For #ETH the 3-CNF count needs $m\le O(n^3)$, which holds.
- Deterministic unsatisfiability testing in $2^{o(n)}$ is in particular nondeterministic $2^{(1-\varepsilon)n}$, so NSETH falls.
- Deciding satisfiability solves the Gap-ETH promise problem.
- The non-transfer remark about $2^{n^{o(1)}}$ reductions is correct.
- The Set-Splitting reduction is correct.

**Factual check of prior work.** The cited bounds are consistent with the literature: Schöning $(2-2/k)^n$, Hertli $1.308^n$, Liu $1.32793^n$, Wahlström $1.2377^n$, Curticapean's #ETH result, and Williams' MA-SETH protocol at $2^{n/2}$.

## Issues

1. **MINOR. Abstract and the definition of $\rho(n)$: "$2^{n/(\log n)^{1/2+o(1)}}$".** Both $n(\log\log n)^2/\sqrt{\log n}$ and $n\log\log n/\sqrt{\log n}$ equal $n/(\log n)^{1/2-o(1)}$. Writing "$+o(1)$" is formally true only with a negative $o(1)$ and is misleading. It should be stated as $1/2-o(1)$, or the explicit form should be used.

2. **MINOR. Paragraph before `cor:graph-counting`: "subexponential time algorithms for … perfect matchings".** The result is $2^{o(v+e)}$, which is subexponential in $v$ only when $e=O(v)$. For dense graphs it is worse than the classical $O^*(2^{v/2})$ algorithm. The statement of the corollary itself is correct.

3. **MINOR. Paragraph before `cor:max-sat-approximation`: the "Unique Games Theorem" [OpenAIUGC26].**
   - The Unique Games Conjecture is open, and calling it a theorem on the strength of a single unrefereed preprint is factually unsupported.
   - It is not used in any proof, so correctness is unaffected. It should be rephrased as conditional on UGC, or removed.

4. **MINOR. `cor:max-sat-approximation`: weaker exponent than needed.** The constant-density 3-CNF actually allows $2^{O_{k,\varepsilon}(n/\sqrt{\log n})}$. The stated $\rho(n)$ bound is correct but needlessly weak.

## Verdict

Every corollary and claimed consequence in the Introduction follows correctly from Theorem `thm:main` with the stated parameters. The parameter recomputations (Hoeffding/union bound, circuit sizes, $\eta<1/(12A)$, the constant $c$) all check out. Correctness of this part is therefore conditional on the appendix proof of `thm:main`, which must be verified separately. The issues found here are presentational.

VERDICT: SOUND-WITH-MINOR-ISSUES
