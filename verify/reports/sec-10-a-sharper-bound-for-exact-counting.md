<!-- {"stage": "sec-10-a-sharper-bound-for-exact-counting", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 375, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 29613, "estimated_cost_usd": 0.6194, "message_id": "msg_011CgS5t9r8aHygshakmj677", "finished_at": "2026-10-27T04:12:59+00:00"} -->

# Referee report: Appendix "A sharper bound for exact counting" (`app:quantitative`)

This is a compressed but complete pass. I recomputed every quantitative claim I could check. I found no fatal error in this part. Its conclusions depend on lemmas proved elsewhere, and those must be verified independently.

## What this part proves

- **Thm `thm:tensor-contraction`.** Bipartite Boolean tensor networks with at most $Cs$ edges, maximum degree at most $\lceil s^{9/10}\rceil$, polynomially many vertices, and entries in $(\mathbb Z/2^{P_0})[V]/(V^\ell)$ with $P_0,\ell\le Cs$ can be contracted deterministically in $(s+\mathcal L)^{O(1)}2^{O(s/\sqrt{\log s})}$ time and polynomial space.
- **Fixed-density bound of Thm `thm:main`.** It follows from the theorem above via a clause/equality network with $s=n+m$.
- **Lemma `lem:tensor-sparse-query`.** Sparse $\mathbb F_2$ systems can be counted in $2^{O(n\log\log n/\sqrt{\log n})}$ time, via an incidence-monomial network with $s=n\nu$ wires.
- **Arbitrary-density bound of Thm `thm:main`.** This also yields the "single algorithm" combining both bounds.
- **Provides to other parts:** both bounds of Thm `thm:main`. Corollaries `cor:graph-counting`, `cor:quantitative-circuits` (which uses the fixed-density bound) and `cor:consequence-local-inversion` rely on these.

## Dependencies on other parts

1. **`lem:sparsify`.** Used with $\sigma=1/\lceil\sqrt\lambda\rceil$. Needed: a disjoint tree with $\mathrm{poly}_k(n,\sigma^{-1})2^{\sigma n}$ nodes, leaf occurrence bound $B=O_k((\sigma^{-1}\log(2/\sigma))^{k-1})$, and polynomial work per node.
2. **`lem:sparse-checks`.** Needed: at most $3n$ rows, row support at most $D_0=320000B^2\mu^3$, and every nonzero kernel word has weight at least $m/P$. Construction cost is $\exp(\mathrm{poly}(B,\log m))$.
3. **`lem:greedy-hashes`.** Needed: $3n$ appended rows of length $P$, at most $3n(2m)^P$ counts, at most $6n$ equations, at most $2^k\max(D_0,P)$ monomials per equation, and $N(A)=\#F$ at the end.
4. **`lem:rational-idempotent`.** Needed: integer $e_j$ with $\deg e_j\le1$, $p_\ell=\sum e_jh^j\equiv\mathbb 1_{2\mid y}\pmod{2^\ell}$, and $\mathrm{poly}(\ell)$ construction.
5. **`lem:total-order`.** Needed: the truncated product, followed by $\mathcal S_\ell$, gives the parity-product congruence mod $2^\ell$ at integer arguments.
6. **Bar23 / standard facts.** Only via the corollaries; not used here.

## Detailed verification

**Ring setup (`subsec:tensor-arithmetic`).**
- $f$ irreducible mod 2 with degree $e=4\lambda$. Hence $\mathcal O/2=\mathbb F_{2^e}$, $v_2$ is multiplicative, and non-zero-mod-2 elements are units. All correct.
- $2^e\ge s^4$ binary lifts have pairwise unit differences, so Lagrange interpolation over $\mathcal A_p$ is valid.
- The canonical-lift bookkeeping is consistent:
  - A child computes the contraction of fixed lifts mod $2^{p_t}$, with $p_t>p$.
  - The parent's $F$ is defined with those same lifts.
  - Reduction mod $2^{p_t}$ commutes with the polynomial evaluation.

**Parameters.**
- From $H<M\le Cs8^{-d}$ we get $8^d<C\sqrt\lambda+O(1)$, so $d\le\frac{\log_2\lambda}6+O(1)$. Then $u_d\ge\varepsilon\lambda/(C'\lambda^{1/6})-1\ge\lambda^{4/5}$ once $\lambda^{1/30}\gtrsim2^{17}C'$.
- $a_d\le4\varepsilon\lambda$, which gives $L\le2^{4\lambda/2^{17}}$ and $D_{\rm arr}=2^{12a}\le s^{1/1000}$.
- (`eq:tensor-packing-conditions`): $2D_{\rm arr}^2\Delta=O(s^{0.902})=o(H)$. Checked.

**Lemma `lem:tensor-packets`.**
- Pairs of edges with disjoint endpoints have agreement probability exactly $1/D_{\rm arr}$. The pairs that share an endpoint number at most $2M\Delta$, giving $\mathbb E\Phi\le2M\Delta$.
- The load is at most $M/D_{\rm arr}+\sqrt{2M\Delta}$, so $H_{\rm pad}\le3M/D_{\rm arr}$ by (`eq:tensor-packing-conditions`).
- Packets have $2^{a'}\cdot2^{a-a'}=L$ slots, which is possible since $L\mid H_{\rm pad}$. There are at most $3M/L$ packets.
- Item 3: a given symbol occupies a $1/r$ fraction of pair labels, giving at most $3M/r$ ports. Checked.

**Lemma `lem:tensor-integrality`.**
- $S$ is $2^{a+1}$ consecutive integers. Hence $v_2(t-q)\le a$, and the valuation profile of $\mathcal C'(t)$ is independent of $t$.
- Each factor $(t-q+\alpha z)$ carries $2^{v_2(t-q)}$, so $\mathcal C(t+\alpha z)/\mathcal C'(0)\in2^{a+1}\mathcal O[z]$.
- Removing the factor indexed by $y-x$ costs at most $2^a$ (or exactly $\alpha z$ when $y-x=t$). Correct.

**Lemma `lem:tapered-hermite`.**
- $\sum q_t\ge Lhu\ge3ML>M(2L-1)$, and $h\le4M/u$ uses $M\ge u$.
- Valuation counts: there are $D/2^j$ points with $v_2(q)=i+j$, and $D/2^j$ with $v_2(t-q)=i+j$. These sum to $D-1$, using the block of $2^{a+1}$ consecutive integers containing $0$.
- Identity (`eq:tensor-hermite-loss`) verified, and $\sum j^2/2^j=6$, so the loss from $E_t(0)$ is at least $-6hD$.
- The factors $1+\alpha z/(t-q)$ are integral with valuation of $\alpha/(t-q)$ at least $1$, so the division is lossless.
- Evaluation at $-t/\alpha$ loses at most $(q_t-1)(a+1)\le4M(a+1)$.
- The total is within $8hD+8M(a+1)$. The Hermite formula itself is the standard CRT construction. Correct.

**Precision (`eq:tensor-precision-bound`).**
- Increments are $O(Cs2^{a_d}/u)$ per depth, which gives $p\le s\lambda^{O(1)}2^{a_{d-1}}$.
- $q_t>0$ implies $D_t\ge2^{a_{d-1}+u}$. Since $M>s/\sqrt\lambda$ and $2^u\ge2^{\lambda^{4/5}}$, inherited precision and $8M(a+1)$ are $O(MD_t/u)$. Checked.

**Modes (`subsec:tensor-modes`).**
- $W(t)$ is local: $y-x=t$ flips bit $i$, which makes the symbols agree.
- Crossing implies $v_2(t-y_0+x)\le i$; verified using $t\equiv2^i\pmod{2^{i+1}}$.
- In the geometric expansion, the first factor has valuation $\ge a+1-i\ge1$ and the ratio has valuation $\ge1$. So the coefficient of $Z$ is divisible by $2^{w_Z}$, and that of $Z^\beta$ by $2^{\sum w\beta}$.
- Multiplicity per weight: $(3M/L)2^{i+1}=6M/D$.
- Partition bound: $e^{\theta p_t+(6M/D)\pi^2/(6\theta)}$ with $\theta=\sqrt{M/(Dp_t)}$ gives $\exp(O(\sqrt{Mp_t/D}))=\exp(O(M/\sqrt u))$. Checked.

**Children.**
- The coefficient of $Z^\beta$ factors over target groups, since a row only meets modes targeted at its own group. Each $L_Z$ reads only bits of its source group. So (`eq:tensor-recursion-identity`) holds.
- Edge count: at most $6M/r=3M/32<M/8$.
- Packet-vertex degree is at most $2L\le\Delta$. Packet entry cost is $e^{O(L\log s)}$.

**Cost.**
- Per-depth exponent: $O\bigl(\frac{s}{\sqrt\lambda}(\sqrt2/8)^d\bigr)$, which is geometric.
- Polynomial factors over $O(\log\lambda)$ levels give $2^{O(\lambda\log\lambda)}$.
- Leaves cost $2^{H+O(s^{9/10})}$. The space accounting is correct.

**Fixed density.** Equality trees, subdivision to make the network bipartite, degree at most $\max(k,3)$, $P_0=n+1\le Cs$, and a factor $2^u$ for unused variables. Correct.

**Lemma `lem:tensor-sparse-query`.**
- Branching on high-incidence variables: at most $N_0/D_*\le n/\sqrt\lambda$ variables. The multilinear representative is valid because incidence variables are disjoint across tests.
- Degree bound: $K=k(a+2(\ell-1))$.
- Wire count: $\sum\lceil\log C_{gh}\rceil\le J^2+\log\binom{N}{\le K}\le J^2+K\log(e(N+K)/K)=O(n\nu)$.
- Degrees are at most $n^{3/4}\lambda^{O(1)}\le s^{9/10}$.
- Entries are correct: the variable side is $2^{\#\{b_v=0\}}$, and the test side uses Möbius inversion with $2^{|S_i|}\le2^{k\lambda^c}$ terms.
- The array count $2^{O(\sqrt n\log n)}$ is absorbed.

**Arbitrary density.**
- Candidates: $3n(2m_G)^P=2^{\lambda^{O_k(1)}}$, which is absorbed.
- Hypotheses of `lem:tensor-sparse-query`: $a\le6n$ and monomials $\le\lambda^{c(k)}$ hold. Checked.

## Issues

1. **MINOR — astronomical thresholds.** "Sufficiently large" in `subsec:tensor-packing` requires $\lambda^{1/30}\gtrsim2^{17}C'$, i.e. roughly $s>2^{2^{510}}$. This is valid asymptotically, but it should be stated explicitly.
2. **MINOR — notation clashes.**
   - $J$ denotes both the number of groups (`lem:tensor-sparse-query`) and the Taylor order elsewhere.
   - $D$ denotes clause density, $L/2^i$, and $D_{\rm arr}$-related quantities.
   - $h$ and $H$ are overloaded, as is $T$ (subset vs. variable).
   - "$\log$ base two" in `app:tensor` conflicts with the global natural-log convention.
3. **MINOR — misleading "$\le\Delta$" claim.** In `lem:tensor-sparse-query`, "the degree of each vertex is at most its number of incidences" is fine, but the "$\le\Delta$" claim should cite $s=n\nu$ explicitly.
4. **MINOR — unstated argument for tile coefficients.** `subsec:tensor-modes` asserts the tile-coefficient computation "using only unit inverses" without spelling out the cancellation. It is the same argument as in `lem:tensor-integrality` and should be cross-referenced.
5. **GAP (presentation only, repairable).** `subsec:tensor-cost` merges the per-call node, value and group counts into "polynomial in $s$" without bounding them explicitly. The bounds are at most $2L$ nodes, $M(2L-1)+1$ values, and $r$ groups. These are trivially polynomial, but they should be stated.

## Verdict

The contraction recursion, the tapered Hermite precision analysis, the mode counting, and both encodings check out line by line. Correctness of Thm `thm:main` additionally rests on `lem:sparsify`, `lem:sparse-checks`, `lem:greedy-hashes`, `lem:rational-idempotent` and `lem:total-order`, which must be verified in their own parts.

VERDICT: SOUND-WITH-MINOR-ISSUES
