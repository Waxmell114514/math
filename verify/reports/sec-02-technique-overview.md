<!-- {"stage": "sec-02-technique-overview", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 396, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 120097, "estimated_cost_usd": 2.4292, "message_id": "msg_011CgS33fLp1R78xLJUzYAZt", "finished_at": "2026-10-27T03:48:37+00:00"} -->

# Referee report on Section 2 ("Technique overview", `sec:technical-overview`)

## What this part proves

Section 2 is expository. Formally it contains only:

- `def:overview-measurement-structure`, the "$(r,\tau,D)$-design". It is the informal analogue of `def:layout`, minus condition 5.
- The statement of `thm:overview-sparse-polynomials`. Its proof is deferred to §5.5.

It also gives informal arguments for three claims:

1. **Bounded-occurrence counting (§§2.1–2.7).** For a 3-CNF in which every variable lies in at most 3 clauses, $\#F$ can be computed in $n^{O(1)}2^{O(n(\log\log n)^2/\sqrt{\log n})}$ bit operations and polynomial space (`eq:overview-bounded-time`). The ingredients are:
   - the deformed polynomial $H(T)$ of `eq:simple-counting-polynomial`;
   - a design at each $t\in[Q]$;
   - Taylor data at each $t$ via Boolean differences;
   - Hermite interpolation;
   - the swap-matrix construction of the replacement forms (Steps 1–5).
2. **General $\#k$-SAT (§2.8).** For fixed $k\ge2$, combining claim 1 with `lem:sparsify`, an OR-gate encoding and Tovey copying gives $(n+m)^{O_k(1)}2^{O_k(n(\log\log n)^{k+1}/(\log n)^{1/(2k)})}=2^{o(n)}$. With $k=3$ this alone would contradict ETH.
3. **Route to the $O_k(\rho(n))$ exponent (§2.9).** This covers:
   - a self-contained randomized parity-test reduction;
   - the Beigel–Tarui lift, truncated in the total power of $h$ across all tests;
   - branching on frequent variables;
   - `thm:overview-sparse-polynomials`.

**What this part provides to others.**

- `thm:overview-sparse-polynomials` (statement only). It is used by §6.3 (`eq:sparse-formula-cost`) and by the proof of `prop:interpolation-bound`.
- `def:overview-measurement-structure`. §3.2 cites it ("same design as in Section 2.4"), but `def:layout` is self-contained.
- `eq:overview-bounded-time`. It is used only within §2.8.
- App. B.4 refers back to §2.4 (the $\vec\lambda$-coefficients).

## Dependencies on other parts

| Label | Statement used here | Parameter range |
|---|---|---|
| `lem:measurement-separation` | For a partition $\sqcup S_g$, integer $C_g$ with row $\ell_1$-norms $\le D$, and $A_g$ invariant under $\ker C_h$ ($h\ne g$): $Z_E$ is obtained by examining $\le 2(2D+1)^c\sum_g2^{\lvert S_g\rvert}$ vectors, in poly space. | any commutative ring; $E$ arbitrary |
| `lem:boolean-differences` | $\sum_x p_x(x)=\sum_{\lvert E\rvert\le q}\sum_{U\subseteq E}(-1)^{\lvert E\rvert-\lvert U\rvert}\sum_{x_E=1}p_x(\mathbf 1_U)$ | $\deg p_x\le q$ |
| `prop:general-count`, `eq:finite-difference-cost`, `eq:three-costs` | $Z$ is computed by examining $\le 2QrC_q(2D+1)^{2\tau n}2^{2n/r}$ vectors. | coefficients in a commutative $\mathbb Q$-algebra; `def:layout` holds |
| `def:layout` | Formal design (1)–(5). | $r\ge2$, $1\le R<Q$, $0<\tau\le\frac12$ |
| `lem:swaps-matrix`, `lem:swaps-support`, `lem:swaps-forms` | $c_{\mathcal B}\le D\Pr[W\notin\mathcal I]$ with $W\sim\Bin(Q,\frac{r-1}{2r})$, and $M_0$ fixes $\ker C^{\mathcal B}$. $M_0[u,y]\ne0\Rightarrow\lvert E_{u,y}\rvert\le R-1$. $\vec P_u$ has degree $\le R-1$, $\vec P_u(0)=\delta_u$, and satisfies the kernel implication. | any interval $\mathcal I$ of length $R$ in $\{0..Q\}$ |
| `lem:incidence-labels` | If $2(b+w)D^2\le M$ and $2Qr^2\le n$, labels can be found deterministically in poly time with multiplicity $\le 2M/D$ and $\lvert S_{t,g}\rvert\le 2n/r$. | used with $b=w=3$, i.e. $12D^2\le M$ |
| §4.5, `eq:incidence-measurement-count` | $\sum_g c_{t,g}\le 2r\epsilon M$ | $\epsilon=\tau/(rb)$, $b=3$ |
| `lem:row-coefficients` | Common denominator $(R-1)!Q!$; coefficient sums $2^{O(Q\log Q)}$; construction in $\mathrm{poly}(D,Q,r)$. | — |
| `lem:layout`, `lem:incidence-parameters` | Parameter feasibility and the balanced cost $O_\beta(\nu^2/\sqrt\lambda)$. | $\beta=1$, so $R=4\lceil\sqrt\lambda\rceil$ |
| App. B.4 | Bit complexity and space of the bounded-occurrence algorithm. | — |
| `lem:sparsify` (App. A) | Disjoint tree with $\mathrm{poly}_k(n,\sigma^{-1})2^{\sigma n}$ nodes; leaf occurrence bound $O_k((\sigma^{-1}\log(2/\sigma))^{k-1})$. | rational $0<\sigma\le1$ |
| `lem:rational-idempotent`, `lem:total-order`, `eq:origin-residue`, `prop:count`, §5.5 | Lift, truncation degree $d_*(m_{\rm test}+2(\ell-1))$, residue readout, proof of `thm:overview-sparse-polynomials`. | $\ell=n+1$ |
| `lem:sparse-checks`, `lem:greedy-hashes`, §6.3, `prop:interpolation-bound` | $\le3n$ initial rows, kernel weight $\ge m/P$; $3n$ greedy rows; $\le 3n(2m)^P+1$ counter calls; $\sigma=1/\lfloor\sqrt{\lambda_n}/\nu_n^2\rfloor$. | $m\le Bn$, $B=\mathrm{polylog}$ |

**External results used:**

- Hoeffding's inequality.
- Tovey's cycle construction [Tov84] / [Gol08, Prop. 4.7].
- The OR-gate (Tseitin-style) encoding.
- The Beigel–Tarui polynomial [BT94].
- Hermite interpolation.

## Detailed verification

**§2.1–2.2.**
- Normalization preserves the bound of $\le3$ occurrences.
- Dummy factors are added only for unused variables. Hence $b=3$, and $n\le M\le 3n$ (`eq:overview-incidences`).
- $\Phi_e$ is correct, including the example: for $\neg x_b$ we get $1-L=X_b$.
- $\deg\prod\Phi_e\le M$.
- The hypothetical-partition count $\prod N_g$ and $\sum2^{\lvert S_g\rvert}\le r2^{2n/r}$ are correct.

**§2.3.**
- $H(0)=\#F$.
- $\deg_TH\le M\max\deg\vec P\le M(R-1)\le 3nR$. Correct.

**§2.4.**
- Condition 4 is equivalent to $\vec P_{e,v}(t)|_{S_h}\in\mathrm{row}(C_h)$, i.e. to the annihilator form in `def:layout`(4). Correct.
- The factorization `eq:outline-separated-sum` is correct; it is exactly `lem:measurement-separation`.
- The overview evaluates $A_{t,g}$ through $\vec\lambda$, even for unattainable $y_h$. This is harmless, because then $B_{t,h}=0$.
- The cost $(2D+1)^{2\tau n}\,r2^{2n/r}$ is correct.

**§2.5.**
- Uniqueness of Hermite interpolation holds since $QJ>3nR$.
- $\Delta\vec P$ is divisible by $z$; in fact the constant $(I-M_0)$ part cancels. Hence $\deg_{\vec X}[z^j]\mathcal G_x\le j$.
- The inclusion–exclusion identity `eq:outline-taylor-recovery` is correct. I also checked it on a toy case: $n=1$, $\mathcal G_x=\alpha_x+\beta_xzX$.
- Fixing $\vec X=\mathbf1_U$ leaves $x$-dependence only through $\langle\vec P(t),x\rangle$, so the design applies. The constraints $x_E=1$ are group-local.

**§2.6.**
- $q\le n/2$ follows from $6R\le Q$ (Step 5).
- $(2en/j)^j$ increases for $j<2n$, so $C_q\le(q+1)(2en/q)^q$.
- With $R/Q=(512+o(1))\nu/\sqrt\lambda$, the three costs are:
  - Taylor: $q\log_2(2en/q)\approx768\,n\nu^2/\sqrt\lambda$;
  - measurements: $2\tau n\log_2(2D+1)\le\frac{2n}{r\lambda}(\frac{\lambda}{128}+2)=O(n/r)$;
  - groups: $2n/r=O(n\nu^2/\sqrt\lambda)$.
- All three agree with `eq:three-costs` and `eq:balanced-cost`.

**§2.7, Steps 1–3.** I re-derived the following.
- The $\Pi_s$ commute and are involutions.
- $V_0[u,w]\ne0$ implies $E_{u,w}=\varnothing$.
- Expanding $f(W_0)$ gives `eq:overview-partial-swaps`, and the summand $\prod_{s\notin S}\Pi_s$ has $E_{u,w}\subseteq S$.
- The tensor eigenbasis is orthogonal with entries in $\{0,\pm1\}$, and $M_0\psi=(-1)^jf(j)\psi$.
- $\ker C$ equals the span of the fixed $\psi$, by orthogonality.
- $j\sim\Bin(Q,\frac{r-1}{2r})$.
- $P(T)=(I-M_0)+M_0\circ[\varphi_{u,w}(T)]$ satisfies $P(0)=I$, has degree $\le R-1$, and at each $t$ equals (rank $\le c$) + (entries only where $a_w(t)=d_u(t)$).
- As a sanity check, I independently recomputed the $Q=R=2$ example in the Remark of §4.3. I obtained $\zeta_0-\frac T2\zeta_1-T\zeta_2$, as stated.

**Step 4.**
- Kernel condition after transfer: $\pi_c\iota\tilde\xi$ is supported on $S^{\mathcal B}_{t,h}$ and lies in $\ker C^{\mathcal B}$. Hence $\langle\vec P_u(t),\cdot\rangle=0$. Correct.
- Row count: $rhc\le r\cdot\frac{2M}{D}\cdot\frac{D\tau}{3r}=\frac{2M\tau}{3}\le2\tau n$.
- Row sums: these are $\le2^Q\le D$, since each $\psi$ has $\le2^Q$ nonzeros.

**Step 5.**
- $\log_2D\le2\frac{\lambda}{128\nu}\frac\nu2=\frac\lambda{128}$.
- $12D^2\le 12\cdot2^{\lambda/64}<2^{\lambda-1}<n$.
- $2Qr^2\le\lambda^2/(64\nu^5)\le n$.
- $R^2/(8Q)\ge16\lambda\cdot128\nu/(8\lambda)=256\nu$.
- $2e^{-256\nu}\le1/(3\lambda^2)\le\tau/(3r)$, using $\lambda\le2^\nu$ and $r^2\le\lambda$.
- The interval contains $[Qp-\frac{R-1}2,\,Qp+\frac{R-1}2-1]$. This contains all integers within $R/4$ of $Qp$ when $R\ge6$.
- The interval lies in $\{0,\dots,Q\}$: $A_0\ge Q/6-\frac12$ and $A_0+R-1\le 7Q/12$.
- Hoeffding with deviation $R/4$ gives $2e^{-R^2/(8Q)}$.
- All of this matches `lem:incidence-parameters` at $\beta=1$: there $R=(\beta+3)\lceil\sqrt\lambda\rceil$ and $16(\beta+3)^2\nu=256\nu$.

**§2.8.**
- Each OR gate uses 3 clauses that force $z=u\vee v$, so the encoding is parsimonious.
- The Tovey cycle forces all copies to agree, and each copy has exactly 3 occurrences.
- $N=O_k(Bn)$ and $N\ge n$.
- With $\sigma\asymp(\log n)^{-1/(2k)}$, we get $B\rho(n)/n\asymp(\log\log n)^{k+1}(\log n)^{-1/(2k)}$, as claimed.
- Replacing $N$ by $n$ in $(\log\log N)^2/\sqrt{\log N}$ is valid, since $\log N=\Theta(\log n)$.

**§2.9, randomized reduction.**
- $p_w=\frac12(1-(1-w/m_G)^L)$.
- For $u\le1$: $p_w\ge u/4$. Since $2nL/m_G\ge2L/B=4\lceil\log_2(2m_G)\rceil$, we get $m_G^we^{-2nLw/m_G}\le 2^{-5.7w}<16^{-w}$.
- For $u>1$: $p_w\ge(1-e^{-1})/2>1/4$, and $2^n(3/4)^{8n}=(0.2002)^n<1/4$.
- Total failure probability $\le\frac1{15}+\frac14<\frac13$.

**§2.9, lift and truncation.**
- $p_\ell=(1-Y)^\ell S(Y)$ with $p_\ell\equiv1\pmod{Y^\ell}$. Hence $p_\ell\equiv1\pmod{2^\ell}$ at even integers and $\equiv0$ at odd integers.
- Retained terms have degree $\le k(m_{\rm test}+2(\ell-1))=O(n)$.

**§2.9, branching and the theorem.**
- $\lvert S\rvert\le M/b_0\le n/\sqrt\lambda$.
- The statement of `thm:overview-sparse-polynomials` matches what §5.5 proves: branch count $2^{n/\sqrt\lambda}$, $n'\ge n/2$, bounded $\beta$, and exhaustive fallback.
- Its hypotheses concern only size, so it also applies to discarded greedy candidates.
- The number of counter calls, $3n(2m)^P+1=2^{(\log n)^{O_k(1)}}$, and the choice $\sigma\asymp(\log\log n)^2/\sqrt{\log n}$ match §6.

I also spot-checked `lem:sparse-checks`, `lem:greedy-hashes` and `lem:incidence-labels`, on which this section relies. I found:
- $\varepsilon^2d_G/2=4\mu$;
- local code: $2^{d_G/(25B)}<2^{c_G}$;
- $\delta(\delta-\varepsilon)=1/(20000B^2\mu^2)$;
- $\mathbb E\Phi\le M(b+w)$ and $\mathbb E\Xi=Qn(1-1/r)$.

All are consistent.

## Issues

1. **MINOR — notation overload.** Several symbols carry more than one meaning:
   - $D$ is the design row-sum bound in `def:overview-measurement-structure`, $\lvert\mathcal B\rvert=r^{2Q}$ in Step 1, and the density constant in `thm:main`.
   - $B$ is the occurrence bound, the coordinate set $\mathcal B$, and the group sums $B_{t,g}$.
   - $h$ is the number of copies and also $h(Y)=Y(Y-1)$.
   - $u$ and $w$ are labels in §2.7 but "expected hits" and "set size" in §2.9.
   - $\ell(\vec X)$ is a measurement in Step 4, while $\ell$ is the precision in §2.9.

   The identification "row-sum bound $=\lvert\mathcal B\rvert$" is intended. The actual row sums are $\le2^Q$; stating this would clarify.

2. **MINOR — degree $R$ vs. $R-1$.** §2.3 requires $\deg\vec P_{e,v}\le R$, while Step 3 delivers $R-1$. This is harmless and consistent with `lem:layout`.

3. **MINOR — first-moment heuristic in Step 4.** The heuristic in Step 4 ("expected multiplicity $M/D$ … conditional expectations ensure multiplicity $\le2M/D$") does not by itself give a maximum bound. The second-moment potentials in `lem:incidence-labels` are what produce the hypothesis $12D^2\le M$. The formal lemma is correct.

4. **MINOR — §2.8 is never formalized.** Neither §2.8 nor `eq:overview-bounded-time` is stated or proved in the formal sections, yet the §2 intro asserts that "Taking $k=3$ already refutes ETH" via this route.
   - Repair: $\widehat G$ is a 3-CNF on $N$ variables with $\le3N$ clauses. The equations $v_e=0$ have $\le8$ monomials each, so `thm:overview-sparse-polynomials` (with $k=3$, $c=3$, dimension $N$) applies directly.
   - The formal ETH refutation in any case goes through `prop:interpolation-bound`.

5. **MINOR — App. B.4 is only a sketch.** It is cited at the end of §2.6 for bit complexity. It refers to $\vec\lambda$-coefficients that the formal routine does not use, and it does not treat the $z$-coefficients explicitly. A common denominator $d_{\rm den}^{M}$ and polynomial bit length follow as in App. B.2.

6. **MINOR — two different integer lifts.** §2.9 lifts a test as $L_i=\sum_{e\in S_i}v_e$, whereas §5.1 lifts it as the number of surviving $\mathbb F_2$-monomials. Both have the correct parity and degree $\le k$. The formal proof uses the second; the text should say which lift is used.

7. **MINOR — sign of the $o(1)$.** In $\rho(n)=n/(\log n)^{1/2+o(1)}$ (Section 1, relied on in the §2 intro and §2.9), and likewise in the abstract, the $o(1)$ is negative: $-\Theta(\log\log\log n/\log\log n)$. Writing $1/2-o(1)$, or the explicit form, would avoid misreading.

8. **MINOR — "sufficiently large n" hides astronomical thresholds.**
   - $r\ge2$ needs $\lambda\ge4\nu^4$, i.e. $\lambda\gtrsim2^{19}$.
   - $6R\le Q$ needs $\sqrt\lambda\gtrsim3072\nu$, i.e. $\lambda\gtrsim2^{33.5}$, so $n\gtrsim2^{2^{33.5}}$.

   Below these sizes the algorithm is exhaustive search. This is not an error, but it should be said.

9. **MINOR — forward references.** "$q\le n/2$ since $R/Q\to0$" in §2.6, and the tail estimate in Step 2, both depend on Step 5 (on $6R\le Q$ and on the specific interval). These forward references should be made explicit.

10. **MINOR — missing derivation.** The inequality $m_G^we^{-2nLw/m_G}\le16^{-w}$ in §2.9 is stated without derivation. One line (as in the verification above) suffices.

## Verdict

I re-derived every quantitative step and every exact identity in this part:
- the swap-matrix eigenstructure and support;
- the transfer of the kernel condition;
- the separation and Boolean-difference identities;
- Hermite uniqueness;
- all parameter inequalities and the three cost exponents;
- the randomized-reduction constants.

I found no error. The overview is also consistent with the formal sections in parameters, exponents and the object counted. Every idea it describes is formally covered, either directly or (for §2.8) via `thm:overview-sparse-polynomials`.

Note that §§2.1–2.7, together with standard reductions, would by themselves refute ETH. The extraordinary claim therefore rests on §§3–4 (which formalize this mechanism) and on App. A, and reviewers of those parts should concentrate there. My verdict covers only Section 2.

VERDICT: SOUND-WITH-MINOR-ISSUES
