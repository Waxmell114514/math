<!-- {"stage": "sec-06-reducing-k-sat-to-counting-common-zeros", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 402, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 93115, "estimated_cost_usd": 1.8896, "message_id": "msg_011CgS3yd2B1A5AWQtGUwkg6", "finished_at": "2026-10-27T03:56:28+00:00"} -->

# Referee report on Section 6: "Reducing #k-SAT to counting common zeros" (`sec:hashes`, through the end of the proof of `prop:interpolation-bound`)

## What this part proves

This section is the reduction layer between disjoint sparsification and the common-zero counter. Its contents are as follows.

1. **Preamble.** For a $k$-CNF $F$ with $m$ indexed clauses, it defines the violation polynomials $v_e\in\mathbb F_2[x]$, with $\deg v_e\le k$ and at most $2^k$ monomials after normalization.
   - For a binary $A$ with $m$ columns it defines the system $\mathcal P_A$ by `eq:hash-query`.
   - It states the identity $N(A)=\#F+D(A)$.
2. **`lem:sparse-checks`.** Fix positive integers $n,m,B$ with $m\le Bn$, and put $\mu=\lfloor\log_2 m\rfloor+1$, $P=20000B^2\mu^2$, $D_0=320000B^2\mu^3$.
   - It constructs a deterministic binary $A^{(0)}$ with $m$ columns, at most $3n$ rows, and row weight at most $D_0$.
   - Every nonzero kernel vector has weight at least $m/P$.
   - Cost: $\exp(\mathrm{poly}(B,\log(m+2)))$ time and $\mathrm{poly}(n,m,B)$ space.
3. **`lem:greedy-hashes`.** Given an exact common-zero counter, $3n$ greedy rounds over $(2m)^P$ candidate rows yield $A$ with $N(A)=\#F$.
   - The procedure uses at most $3n(2m)^P$ counts.
   - Every queried system has at most $6n$ equations, each with at most $2^k\max(D_0,P)$ monomials of degree at most $k$.
4. **§`subsec:count-sparse`, eq. `eq:sparse-formula-cost`.** For $n\ge20$, $1\le m\le Bn$ and $B\le(\log n)^{O_k(1)}$, it computes $\#F$.
   - Time: $(n+m)^{O_k(1)}2^{O_k(\rho(n))}$. Space: polynomial.
   - It makes at most $3n(2m)^P+1$ calls to `thm:overview-sparse-polynomials`.
5. **`lem:sparsify`.** Statement only; the proof is in App. A.
6. **`prop:interpolation-bound`.** It counts any $k$-CNF in $(n+m)^{O_k(1)}2^{O_k(\rho(n))}$ time and $(n+m)^{O_k(1)}$ space.

Logically the part establishes: `thm:overview-sparse-polynomials` + `lem:sparsify` ⇒ `prop:interpolation-bound`. All queried systems live on the original $n$ variables, and the reduction adds only quasi-polynomial ($2^{(\log n)^{O_k(1)}}$) overhead. **The subexponential saving does not originate here.** The extraordinary claim rests entirely on dependency D1 below (and, for Thm. `thm:main`, on App. `app:quantitative`).

## Dependencies on other parts

**D1. `thm:overview-sparse-polynomials`** (stated in §2.9, proved in §§3–5 and App. B).
- Statement used: fix integers $k\ge2$ and $c\ge1$. Given $m_{\rm test}\le cn$ polynomials over $\mathbb F_2$ on $n\ge20$ variables, each a list of at most $(\ln n)^c$ monomials of degree at most $k$:
  - it computes the **exact** number of common zeros in $\{0,1\}^n$, deterministically;
  - it uses $2^{O_{k,c}(n(\log\log n)^2/\sqrt{\log n})}$ bit operations and $n^{O_{k,c}(1)}$ space.
- Parameters used here:
  - $n$ is the declared-variable count of the leaf (unchanged);
  - $m_{\rm test}\le 6n$, so $c\ge6$;
  - the monomial bound is $2^k\max(D_0,P)=(\log n)^{O_k(1)}$;
  - $c=c(k)$ is fixed.
- Requirements for the cross-check:
  - The theorem must hold for **arbitrary** such systems: candidates that accept nonsatisfying assignments, unbounded variable incidence, and constant equations.
  - Constant equations do arise. Every all-zero list gives $0=0$. A row containing two unit clauses $\{x\},\{\neg x\}$ gives $v_1+v_2=1$, i.e. $1=0$; App. A does no unit propagation, so such leaves exist.
  - The proof in §`sec:setup` handles both constant cases.

**D2. `lem:sparsify`** (statement in this part, proof in App. A, not refereed here).
- Used with $\sigma=1/s$, where $s=\lfloor\sqrt{\lambda_n}/\nu_n^2\rfloor$ is an integer with $2\le s\le\sqrt{\lambda_n}$. The properties used are:
  - (i) the satisfying sets of the leaves partition those of the input;
  - (ii) there are at most $\mathrm{poly}_k(n,s)2^{n/s}$ nodes;
  - (iii) the depth is $\mathrm{poly}_k(n,s)$;
  - (iv) every leaf is a normalized $k$-CNF (no tautologies or repeated literals, so $\deg v_e\le k$) on the same $n$ variables, with each variable occurring at most $B=O_k((s\ln 2s)^{k-1})$ times, $B$ an explicit integer;
  - (v) per-node cost $\mathrm{poly}_k(n,\log s)$, normalization cost $\mathrm{poly}_k(n,m)$, parameter construction cost $\mathrm{poly}_k(\log s)$.
- Consistency check against App. A:
  - App. A gives at most $(Cn+1)^2 2^{\sigma n}$ nodes, with depth at most $Cn$ and $C=O_k(M^{k-2})$;
  - it gives $M=O_k(\sigma^{-1}\log(2/\sigma))$ and $B=2\sum_{j<k}M^j\le 4M^{k-1}$.
  - These match the statement.

**D3. Conventions.** $\rho(n)=n(\log\log n)^2/\sqrt{\log n}$ (§1), with natural logarithms.

**D4. Standard facts.** Hoeffding's inequality for sums of independent $\pm1$ variables; union bounds; character diagonalization of Cayley (multi)graphs on $\mathbb F_2^{\ell}$. All are re-derived or checked in place. The citations [Tan81, SS96, NN93, Rag88] are attributional only, since the proofs are self-contained.

**What this part provides to other parts.**
- **App. `app:quantitative`, arbitrary-density proof of Thm. `thm:main`.** It uses:
  - `lem:sparse-checks`;
  - `lem:greedy-hashes`, which is counter-agnostic: it needs only exact counts, at most $3n(2m_G)^P+1$ of them, on systems with at most $6n$ equations and at most $2^k\max(D_0,P)$ monomials each. It is paired there with `lem:tensor-sparse-query`, whose $\lceil\log_2 n\rceil^c$ monomial bound is compatible;
  - `lem:sparsify` with $\sigma=1/\lceil\sqrt\lambda\rceil$.
- **§2.8.** `lem:sparsify` with $\sigma\asymp(\log n)^{-1/(2k)}$.
- **§1 and §2.9.** `prop:interpolation-bound`, i.e. the $O_k(\rho(n))$ exponent.

## Detailed verification (lemma by lemma)

**Preamble (`eq:hash-query`).**
- $v_e=\prod_{\text{pos } x_v}(1+x_v)\prod_{\text{neg } x_v}x_v$ is correct.
- For normalized clauses there are at most $k$ factors and at most $2^{\#\mathrm{pos}}\le 2^k$ monomials.
- $N(A)=\#F+D(A)$ holds because $v(x)=0$ for every satisfying $x$.
- Since $\#F$ does not depend on the candidate, $\arg\min N=\arg\min D$. Correct.

**`lem:sparse-checks`.** Recomputed step by step.

- **(a) Edge count.** We need $m\le q_Gd_G<2m$.
  - If $q_G=1$, then $d_G\ge m$, and since $d_G\le m$ we get $d_G=m$.
  - If $q_G\ge2$, minimality gives $(q_G/2)d_G<m$.
  - Moreover $q_G>1\Rightarrow d_G<m\Rightarrow d_G=D_0$. Both claims are correct.
- **(b) Regularity.** Each vertex has exactly one incident edge per port. A right vertex $v$ meets edge $(v\oplus s_j,j)$ at port $j$, so the graph is $d_G$-regular, with parallel edges distinct. Correct.
- **(c) Small bias.**
  - Hoeffding gives $\Pr\big[|\sum_j(-1)^{b\cdot s_j}|\ge\varepsilon d_G\big]\le2e^{-\varepsilon^2d_G/2}$.
  - The exponent is $\varepsilon^2D_0/2=\frac{320000B^2\mu^3}{2\cdot40000B^2\mu^2}=4\mu$.
  - Since $q_G<2m<2^{\mu+1}$, the union bound gives $2q_Ge^{-4\mu}<4(2e^{-4})^\mu\le 8e^{-4}<1$.
  - Exhaustive search costs $\le 2^{(\mu+1)D_0}\cdot\mathrm{poly}(m)=2^{O(B^2\mu^4)}$. Correct.
- **(d) Mixing.**
  - $(\mathsf A_G\chi_b)(u)=\chi_b(u)\sum_j(-1)^{b\cdot s_j}$ is correct, and $\mathsf A_G$ is symmetric.
  - Write $\mathbf 1_U=\tfrac{|U|}{q_G}\mathbf 1+f$ and $\mathbf 1_V=\tfrac{|V|}{q_G}\mathbf 1+g$ with $f,g\perp\mathbf 1$.
  - Then $e_G(U,V)=d_G|U||V|/q_G+f^\top\mathsf A_Gg$, and $|f^\top\mathsf A_G g|\le\varepsilon d_G\sqrt{|U||V|}$.
  - This is `eq:hash-mixing`. Correct.
- **(e) Local code.**
  - A fixed nonzero word lies in the kernel of a uniform $c_G\times d_G$ matrix with probability $2^{-c_G}$.
  - Put $h=\lceil\delta d_G\rceil-1$, the largest integer below $\delta d_G$. Then $\sum_{j\le h}\binom{d_G}{j}\le(2d_G)^{2h}$.
  - Using $h<\delta d_G$ and $\log_2(2d_G)<\mu+1\le2\mu$, this is $<2^{4\delta\mu d_G}=2^{d_G/(25B)}$.
  - Since $c_G\ge d_G/(8B)$, the expected number of bad kernel words is $<2^{-d_G(1/8-1/25)/B}\le1$.
  - Search cost: $c_Gd_G\le D_0^2/(8B)+D_0=O(B^3\mu^6)$, so $2^{O(B^3\mu^6)}$ in total. Correct.
- **(f) Distance.**
  - Every vertex touched by the nonzero word has at least $\delta d_G$ nonzero incident edges, so $h'\ge\delta d_G\max(|U|,|V|)\ge\delta d_G\sqrt{|U||V|}$.
  - Every nonzero edge joins $U$ to $V$, so $h'\le e_G(U,V)$.
  - Dividing by $d_G\sqrt{|U||V|}$ gives $\sqrt{|U||V|}\ge(\delta-\varepsilon)q_G$, where $\delta-\varepsilon=\frac1{200B\mu}$.
  - Hence $h'\ge\delta(\delta-\varepsilon)q_Gd_G=q_Gd_G/(20000B^2\mu^2)\ge m/P$.
  - The degenerate case $q_G=1$ (one vertex per side, $m$ parallel edges, vacuous bias condition) also works. Correct.
- **(g) Shortening.** Zero-extension maps accepted words to accepted edge words, so the distance is preserved. Correct.
- **(h) Row count.**
  - If $q_G=1$: $2c_G\le m/(4B)+2\le n/4+2\le3n$.
  - If $q_G>1$: $D_0\ge8B$ gives $2q_G\le q_Gd_G/(4B)$, hence $2q_Gc_G\le q_Gd_G/(2B)<m/B\le n$.
  - Row support is at most $d_G\le D_0$. Correct.
- **(i) Space.** The current shift tuple, local matrix and output use $\mathrm{poly}(n,m,B)$ bits. The output has $O(m)$ rows, so its size is $\mathrm{poly}(m,B)$, inside the time bound. Correct.

**`lem:greedy-hashes`.**
- **Large support.** If $x$ is nonsatisfying and accepted by $A\supseteq A^{(0)}$, then $A^{(0)}v(x)=0$ with $v(x)\ne0$, so $|\mathrm{supp}\,v(x)|\ge m/P$.
  - Each draw hits the support with probability at least $1/P$; this also holds when $P>m$, since then the hit probability is $\ge 1/m>1/P$.
  - So $\Pr[\text{no hit}]\le(1-1/P)^P\le e^{-1}$.
- **Uniform parity.** $h_\gamma\cdot v(x)=\sum_j c_jv_{e_j}(x)\bmod 2$, which is linear in the $c_j$ and valid with repeated indices.
  - Condition on the whole index tuple. If some $v_{e_j}(x)=1$, the independent bit $c_j$ makes the parity uniform.
  - So the rejection probability is $\ge(1-e^{-1})/2\approx0.316>1/4$.
- **Averaging.** The minimum over $\mathcal C$ is at most the mean, which is at most $\tfrac34D(A)$. Since $N=\#F+D$, the argmin of $N$ is the argmin of $D$.
- **Termination.** After $3n$ rounds, $D\le(3/4)^{3n}2^n=(27/32)^n<1$, so $D=0$.
- **Sizes.** There are $3n\cdot(2m)^P$ counts. Systems have at most $3n+3n$ equations. An initial row contributes $\le 2^kD_0$ monomials and an appended row $\le 2^kP$, all of degree at most $k$.
- All correct.

**§`subsec:count-sparse`.**
- **Sizes.** $\mu\le\log_2(Bn)+1$, so $P=O(B^2\log^2(Bn))$ and $D_0=O(B^2\log^3(Bn))$. Both are $(\log n)^{O_k(1)}$.
- **Number of calls.** $\log(3n(2m)^P+1)=O(P\log(2Bn))=(\log n)^{O_k(1)}=o(\rho(n))$.
- **Construction cost.** `lem:sparse-checks` costs $2^{O(B^3\mu^6)}=2^{(\log n)^{O_k(1)}}$.
- **Choice of $c$** (left implicit in the text). If $B\le(\ln n)^{c_1}$, then for $n\ge20$ (where $\ln n\ge2.99$) one has $\mu\le C_1\ln n$. Hence:
  - $2^k\max(D_0,P)\le 2^k\cdot 320000\,C_1^3(\ln n)^{2c_1+3}$;
  - $c=\max\{6,\ 2c_1+3+\log_3(2^k\cdot320000\,C_1^3)\}$ works uniformly in $n$.
- **Conclusion.** The total is `eq:sparse-formula-cost`, given D1. Space is polynomial because candidates are processed sequentially. Correct.

**`lem:sparsify` (statement).** It is consistent with App. A, as recorded in D2, and with all uses in this part and in App. `app:quantitative`.

**`prop:interpolation-bound`.**
- **Normalization.** Subsumption and duplicate removal preserve the satisfying set. Correct.
- **Computing $s$.** $s$ is the largest integer with $s^2\nu_n^4\le\lambda_n$, i.e. $s=\lfloor\sqrt{\lambda_n}/\nu_n^2\rfloor$.
- **Finitely many exceptions.** $s\ge2$ iff $\lambda_n\ge4\nu_n^4$. This fails only finitely often, but not monotonically: it holds at $\lambda=2^{19}$ and fails for $2^{19}<\lambda<640000$.
- **Leaf count.** For $y\ge2$, $\lfloor y\rfloor\ge y/2$, so $n/s\le2n\nu_n^2/\sqrt{\lambda_n}$. With $\nu_n=O(\log\log n)$ and $\lambda_n\ge\ln n$, this is $O(\rho(n))$.
- **Occurrence bound.** $B=O_k((s\ln 2s)^{k-1})=(\log n)^{O_k(1)}$, so the hypotheses of §`subsec:count-sparse` hold for every leaf.
- **Time.** Number of nodes × per-leaf cost $=(n+m)^{O_k(1)}2^{O_k(\rho(n))}$.
- **Space.** Depth-first search over a path of $\mathrm{poly}_k(n,s)$ nodes, with $\mathrm{poly}_k(n)$-bit normalized formulas and an $(n+1)$-bit accumulator, uses $\mathrm{poly}_k(n,m)$ bits.
- Correct, conditional on D1 and D2.

## Issues

1. **MINOR — implicit choice of $c=c(k)$** (§`subsec:count-sparse`, "with a single fixed $c=c(k)$").
   - The invocation of D1 needs $c\ge6$ and $(\ln n)^c\ge 2^k\max(D_0,P)$, with natural log in D1's statement, for all $n$ at which it is called.
   - This holds uniformly for $n\ge20$ by the computation above, but the text does not say so.
   - Add one sentence fixing $c$ in terms of the exponent $c_1$ with $B\le(\ln n)^{c_1}$.
2. **MINOR — notation collisions.**
   - $D(A)$ clashes with $D=r^{2Q}$, $D_0$ and $D_H$.
   - The integer $P$ clashes with the polynomials $P_i$ and the rows $\vec P$.
   - $h$ has four meanings: $\lceil\delta d_G\rceil-1$ in the proof of `lem:sparse-checks`, $h(Y)$, the number of copies, and $h_\gamma$.
   - $B$ also denotes a different quantity in App. B; $m$ denotes both the input and the leaf clause count; $\mu$ is also a mean in `lem:incidence-parameters`; $\ell_G$ clashes with $\ell$; $c$ is used for coefficient bits, a constant, $c_G$ and $c(f,v)$.
   - None causes an error, but renaming would help cross-checking.
3. **MINOR — effective thresholds.**
   - "Finitely many" exceptional sizes means $s\ge2$ only once $\lambda_n\gtrsim6.4\times10^5$, i.e. $n>2^{6\times10^5}$.
   - D1's own requirements ($6R\le Q$, $q<n$) push the threshold far higher.
   - The asymptotic statement is mathematically valid, but this should be stated explicitly.
4. **MINOR — `lem:greedy-hashes` proof.**
   - "Choose one hit position $j$" should name a deterministic rule (e.g., the first hit) and condition on the full index tuple; the $c_j$'s are independent of the indices.
   - The extra "+1" final count in §`subsec:count-sparse` is unnecessary, since the last round's minimum is $N(A)$.
   - Distinct lists representing the same row are recounted, which is harmless.
5. **MINOR — preamble.** "A tautological clause has $v_e=0$" holds as a function on $\{0,1\}^n$, or after multilinearization, but not for the literal product $x_v(1+x_v)$. This is irrelevant here because the leaves are normalized.
6. **MINOR — loose constant.** The row bound "at most $3n$" in `lem:sparse-checks` is loose; the proof gives at most $\max\{n,\ n/4+2\}$.

No FATAL or GAP-level problem was found within this part.

## Verdict

Within its scope the section is correct.
- The expander/Tanner construction, its constants ($4\mu$ exponent, $2^{d_G/(25B)}$ word count, $\delta(\delta-\varepsilon)=1/P$, row counts) and the greedy halving argument all check line by line.
- The resulting system sizes satisfy the counter's hypotheses with a fixed $c(k)$.
- The sparsification parameters give $O_k(\rho(n))$ for both the leaf count and the per-leaf cost.

`prop:interpolation-bound` is, however, only as strong as D1 (`thm:overview-sparse-polynomials`) and D2 (`lem:sparsify`). This part supplies no subexponential saving of its own, so the paper's ETH-refuting claim must be adjudicated in the reviews of §§3–5/App. B (and App. `app:quantitative` for Thm. `thm:main`). The present verdict does not certify it.

VERDICT: SOUND-WITH-MINOR-ISSUES
