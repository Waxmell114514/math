<!-- {"stage": "sec-04-constructing-low-degree-replacement-form", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 355, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 90051, "estimated_cost_usd": 1.8281, "message_id": "msg_011CgS33fMp7mdBCwA9rjxYP", "finished_at": "2026-10-27T03:43:51+00:00"} -->

# Referee report on Section 4, "Constructing low-degree replacement forms" (`sec:construction`)

## What this part proves

From the factor scopes $(I_f)$ alone, Section 4 constructs the data required by Definition `def:layout`: partitions $S_{t,g}$, assignments $\sigma_f$, integer measurement matrices $C_{t,g}$, and replacement rows $\vec P_{f,v}(T)$. It also fixes explicit parameters. The results are:

- **`lem:swaps-matrix`.** Set $M_0=V_0f_{\mathcal I}(W_0)$ as in `eq:swap-matrix-definition`.
  - There is a $\{0,\pm1\}$ matrix $C^{\mathcal B}$ with $c_{\mathcal B}=D\Pr[W\notin\mathcal I]$ rows, where $W\sim\mathrm{Bin}(Q,\frac{r-1}{2r})$.
  - $M_0$ fixes $\ker C^{\mathcal B}$.
- **`lem:swaps-support`.** $M_0[u,y]\neq0\Rightarrow|E_{u,y}|\le R-1$.
- **`lem:swaps-forms`.** The rows in `eq:swaps-row`:
  - have degree $\le R-1$ and satisfy $\vec P_u(0)=\delta_u$;
  - satisfy, at every $t\in[Q]$, the kernel implication with respect to $C^{\mathcal B}_{t,g}$ for every $g\ne d_u(t)$.
- **`lem:incidence-labels`.** Assume $2(b+w)D^2\le M$ and $2Qr^2\le n$. Then there are deterministic labels $a_v,d_f\in[r]^Q$ such that:
  - every label occurs at most $2M/D$ times;
  - $|\{v:a_v(t)=g\}|\le 2n/r$.
- **§4.5, the transfer.** The constructions `eq:actual-rows`, `eq:actual-measurements` and the bound `eq:incidence-measurement-count` give:
  - $\vec P_{f,v}(0)=\delta_v$;
  - absolute row sums $\le D$;
  - $\sum_g c_{t,g}\le 2r\epsilon bn$;
  - the kernel condition of `def:layout`(4).
- **`lem:row-coefficients`.**
  - $(R-1)!\,Q!\,\vec P_u$ and $(R-1)!\,Q!\,\vec P_{f,v}$ are integral, with coefficient $\ell_1$-norm $2^{O(Q\log Q)}$.
  - The construction takes $\mathrm{poly}(D,Q,r)$ time.
- **`lem:layout`.** Assembly of the above into all five items of `def:layout`, in $\mathrm{poly}(n,M,|\mathcal F|,D,Q,r,b,w)$ time.
- **`lem:incidence-parameters`.** For $b,w\le\lambda^\beta$, the explicit parameters `eq:parameter-QR` satisfy every hypothesis of `lem:layout` for large $n$. They also give `eq:balanced-cost`, $=O_\beta(\nu^2/\sqrt\lambda)$.

## Dependencies on other parts

**Used by this part (to be cross-checked against the review of Section 3).**

1. **Definition `def:layout`** is the target interface. It requires integers $r\ge2$, $D\ge1$, $1\le R<Q$, a real $0<\tau\le\frac12$, and:
   - (1) partitions of $[n]$ with $|S_{t,g}|\le2n/r$;
   - (2) sequences $\sigma_f\in[r]^Q$;
   - (3) integer $C_{t,g}$ with absolute row sums $\le D$ and $\sum_g c_{t,g}\le2\tau n$;
   - (4) rows with $\vec P_{f,v}(0)=\delta_v$, $\deg\le R$, and the implication $C_{t,g}\xi=0\Rightarrow\langle\vec P_{f,v}(t),\tilde\xi\rangle=0$ for $g\ne\sigma_f(t)$;
   - (5) $d_{\rm den}=(R-1)!Q!$ clears denominators, with coefficients of $O(Q\log Q+\log D)$ bits.

   Section 4 also uses $D$ in the role of (3), with $D=r^{2Q}=|\mathcal B|$.
2. **External facts.**
   - Hoeffding's inequality for $\mathrm{Bin}(Q,p)$: $\Pr[|W-Qp|\ge s]\le2e^{-2s^2/Q}$, used with $s=R/4$.
   - The method of conditional expectations.
   - Elementary linear algebra over $\mathbb Q$: for an orthogonal basis, the annihilator of a subset equals the span of the complement.
3. **No other internal lemma is used.** Section 4 does not verify the degree hypothesis `eq:general-product-degree`; that is Section 5's job (`lem:total-order`).

**Provided to other parts.**

- **§2 overview (`subsec:preview-auxiliary`, Steps 2–5).**
  - Step 4 uses `lem:incidence-labels` with $b=w=3$, so the hypothesis $2(b+w)D^2\le M$ becomes the overview's $12D^2\le M$. Checked consistent.
  - The measurement bound $c\le D\tau/(3r)$ is $\epsilon=\tau/(rb)$ with $b=3$. Consistent.
  - The overview's choice $R=4\lceil\sqrt\lambda\rceil$ is the case $\beta=1$. The tail bound $2e^{-256\nu}$ matches $16(\beta+3)^2\nu$ at $\beta=1$.
- **§3 (after `eq:three-costs`).** Uses `eq:balanced-cost`.
- **§5, proof of `thm:overview-sparse-polynomials`.** Applies `lem:layout` and `lem:incidence-parameters` on each branch, with data $(n',M',b,w,\beta)$. This needs:
  - $M'\ge n'$ (neutral factors);
  - $b,w\le(\lambda')^\beta$ with $\beta=O_{k,c}(1)$;
  - $n'$ "sufficiently large", which holds since $n'\ge n/2$.

  It uses $D\le(2n')^{1/128}$ and $R=O(\sqrt{\log n'})$, both consistent with what is proved here.
- **App. B (`subsec:rational-streaming-height`).** Uses $d_{\rm den}$ and $B_P=O(Q\log Q+\log D)$. `lem:row-coefficients` supplies even $B_P=O(Q\log Q)$.
- **Appendix E does not use this part.** Section 4 is load-bearing for `prop:interpolation-bound` and `thm:overview-sparse-polynomials`, but not for the proof of Theorem `thm:main` given in Appendix E.

## Detailed verification

**§4.1 (setup).**
- $|S^{\mathcal B}_{t,g}|=r^{2Q-1}=D/r$. Correct.
- Adjoining neutral factors raises $b$ by at most one and gives $M\ge n$. Correct.
- $M\le bn$ is automatic.
- $M\ge n$ is used only in `lem:incidence-parameters`.

**§4.2, the matrices.**
- The $\Pi_s$ act on disjoint coordinate pairs, so they commute and are involutions.
- $V_0[u,y]\ne0\iff y=(d_u,a_u)$, hence $a_y=d_u$. Correct.
- On a common eigenvector with signs $\epsilon_s$: $W_0\psi=\tfrac12\sum_s(1-\epsilon_s)\psi=j\psi$ and $V_0\psi=(-1)^j\psi$. Correct.
- For $0\le q\le R-1$, using $\binom qj=0$ for $j>q$:
  $$f_{\mathcal I}(A_0+q)=(-1)^{A_0}\sum_{j\le q}\binom qj(-2)^j=(-1)^{A_0+q}.$$
  Correct.

**`lem:swaps-matrix`.**
- The one-position spectrum has $r+\binom r2=\frac{r(r+1)}2$ symmetric vectors and $\binom r2$ antisymmetric ones, for $r^2$ in total.
- Tensor products are orthogonal, nonzero, have entries in $\{0,\pm1\}$, and satisfy $\Pi_s\psi=\pm\psi$ according to the parity type of $\psi_s$. Correct.
- The fraction with $j$ antisymmetric positions is $\binom Qj p^j(1-p)^{Q-j}$, with $p=\frac{r(r-1)/2}{r^2}=\frac{r-1}{2r}$. Correct.
- For $j\in\mathcal I$: $M_0\psi=(-1)^jf(j)\psi=\psi$.
- $\ker C^{\mathcal B}$ is spanned by the retained vectors, by orthogonality over $\mathbb Q$.
- $c_{\mathcal B}=D\Pr[W\notin\mathcal I]$ holds with equality. Correct.

**`lem:swaps-support`.**
- $f_{\mathcal I}(W_0)$ is a polynomial of degree $\le R-1$ in commuting involutions. Its multilinear reduction is $\sum_{|J|\le R-1}\gamma_J\prod_{J}\Pi_s$.
- $V_0\prod_J\Pi_s=\prod_{s\notin J}\Pi_s$.
- A nonzero $(u,y)$ entry forces $y=\vartheta_{[Q]\setminus J}(u)$. In fact $E_{u,y}=\{s\in J:a_u(s)\ne d_u(s)\}\subseteq J$. Correct.

**§4.3 and `lem:swaps-forms`.**
- $\varphi_{u,y}$ has degree $|E_{u,y}|\le R-1$, satisfies $\varphi(0)=1$, and its zeros in $[Q]$ are exactly $E_{u,y}$.
- At $T=0$ the row is $\delta_u(I-M_0)+\delta_uM_0=\delta_u$.
- For $\tilde\xi$ supported on $S^{\mathcal B}_{t,g}$ with $g\ne d_u(t)$:
  - $C^{\mathcal B}\tilde\xi=C^{\mathcal B}_{t,g}\xi=0$, so $(I-M_0)\tilde\xi=0$;
  - the surviving summands have $y\in S^{\mathcal B}_{t,d_u(t)}$, which is disjoint from the support of $\tilde\xi$.
- Correct.

**Remark (worked example).** I recomputed it on the orbit indexed by applied swaps $S\subseteq\{1,2\}$.
- The characters $\chi_T$ give eigenvalues of $M_0$ equal to $(-1)^{|T|}(1-2|T|)\in\{1,1,1,-3\}$.
- Hence $I-M_0=\chi_{12}\chi_{12}^{\mathsf T}$ with $\chi_{12}=(1,-1,-1,1)$. This produces the stated $c(\zeta)$.
- $M_0=\Pi_1+\Pi_2-\Pi_1\Pi_2$ gives row $(0,1,1,-1)$.
- The mismatch sets are $E=\{2\},\{1\},\varnothing$.
- Hence $\langle\vec P_u(T),\zeta\rangle=\zeta_0-\frac T2\zeta_1-T\zeta_2$.
- The displayed values at $T=1,2$ and the group memberships are all correct.

**`lem:incidence-labels`.**
- The expansions $\Phi=\sum_u c_u^2-M^2/D$ and $\Xi=\sum_t\sum_{v,v'}\mathbb 1-Qn^2/r$ are correct.
- Pairs with $f\ne f'$ and $v\ne v'$ involve four independent uniform choices, with equality probability $K^{-2}=1/D$.
- At most $|I_f|+\deg v-1\le b+w-1$ pairs are dependent per incidence. Hence $\mathbb E\Phi\le M(b+w)$.
- $\mathbb E\Xi=Q\big[(n^2-n)/r+n-n^2/r\big]=Qn(1-1/r)$.
- The potential starts at $\le2$ and is non-increasing, so $\Phi\le2M(b+w)$ and $\Xi\le2Qn$. This gives:
  - $c_u\le M/D+\sqrt{2M(b+w)}\le 2M/D$, which is equivalent to $2(b+w)D^2\le M$;
  - $n_{t,g}\le n/r+\sqrt{2Qn}\le 2n/r$, which is equivalent to $2Qr^2\le n$.
- The exact conditional-expectation computation is polynomial. Correct.

**§4.5, the transfer.**
- $\vec P_{f,v}(0)=\delta_{u}\pi_c\iota=\delta_v$.
- Each row of $\widetilde C$ has $\le D$ entries in $\{\pm1\}$, and composing with $\iota$ and restricting cannot increase the $\ell_1$ norm.
- $c_{t,g}=hc_{\mathcal B}$ for every $g$, so $\sum_g c_{t,g}=rhc_{\mathcal B}\le r(2M/D)\epsilon D\le2r\epsilon bn=2\tau n$.
- Kernel condition: $C_{t,g}\xi=0$ gives $C^{\mathcal B}\pi_c\iota\tilde\xi=0$ for all $c$. The support of $\pi_c\iota\tilde\xi$ lies in $S^{\mathcal B}_{t,g}$, because a position $(c,y)$ holds $x_{v'}$ with $a_y=a_{v'}$. Applying `lem:swaps-forms` with $d_{u_{f,v}}(t)=\sigma_f(t)\ne g$ finishes the argument. Correct.

**`lem:row-coefficients`.**
- Summand $j$ equals $\frac{(-1)^{A_0+j}}{j!}\prod_{a<j}(2W_0-2(A_0+a)I)$, where $2W_0=QI-\sum_s\Pi_s$ is integral. Hence $(R-1)!M_0$ is integral.
- The denominators of $\varphi$ divide $\prod_{s\in E}s\mid Q!$.
- Norm bounds:
  - $\|2W_0-2(A_0+a)I\|_\infty\le4Q$ (in fact $\le2Q$);
  - $\|M_0\|_\infty\le\sum_{j<R}(4Q)^j/j!\le R(4Q)^{R-1}$;
  - $\|\varphi\|_1\le2^Q$.
- The total is $d_{\rm den}(1+(1+2^Q)R(4Q)^{R-1})$, which is $2^{O(Q\log Q)}$ for $Q\ge2$. Correct.

**`lem:layout`.** The assembly is correct, and every item of `def:layout` is met.

**`lem:incidence-parameters`.**
- $\log_2r\le\frac12\log_2\lambda\le\nu/2$, so $\log_2D\le2\cdot\frac{\lambda}{128\nu}\cdot\frac\nu2=\lambda/128$.
- $2(b+w)D^2\le4\lambda^\beta2^{\lambda/64}<2^{\lambda-1}<n\le M$, and $2Qr^2\le\lambda^2<n$, both for large $n$.
- Interval:
  - $\mu=Q\frac{r-1}{2r}\in[Q/4,Q/2]$;
  - with $Q\ge6R$, $A_0\ge\lfloor R+\frac12\rfloor\ge0$ and $A_0+R-1\le\mu+\frac{R-1}2\le Q$;
  - the interval contains every integer within $R/4$ of $\mu$ as soon as $R\ge6$.
- Hoeffding gives $2e^{-R^2/(8Q)}$.
- $R^2/(8Q)\ge(\beta+3)^2\lambda\cdot16\nu/\lambda=16(\beta+3)^2\nu$.
- Then $2e^{-16(\beta+3)^2\nu}\le2^{-(\beta+2)\nu}\le\lambda^{-(\beta+2)}\le1/(br^2\lambda)=\tau/(rb)$. Correct.
- Cost: $\frac RQ=O_\beta(\nu/\sqrt\lambda)$, $\log\frac{2Q}R=O(\nu)$, $\tau\log(2D+1)=O(1/r)$, and $1/r=O(\nu^2/\sqrt\lambda)$. Correct.
- Exact checks are polynomial in $\log n$; the tail probability has denominator $(2r)^Q$. Correct.

## Issues

1. **MINOR — notation overload.**
   - $\mathcal A$ denotes the incidence set (`eq:factor-incidences`), but the coefficient algebra in §3 and §5 ($\mathcal A$, $\mathcal A_\ell$). The two meet exactly where this section is used.
   - $\Phi$ is the potential in `lem:incidence-labels`, but also the factor polynomials $\Phi_f$.
   - $J$ is a subset in `lem:swaps-support`, but also the truncation order $J=q+1$.
   - $q$ is the shift in the binomial-theorem check, but also the Taylor order.
   - $h$ is the number of copies, but also $h(Y)=Y(Y-1)$ in §5 and a group index in `lem:measurement-separation`.
   - $c$ is overloaded ($c(f,v)$, $c_u$, $c_{\mathcal B}$, $c_{t,g}$), as is $f$ (factor index versus $f_{\mathcal I}$), and $\epsilon$ is used alongside $\varepsilon$.
   - $D$ simultaneously denotes $|\mathcal B|$ and the row-sum bound of `def:layout`(3).
2. **MINOR — misplaced conditional.** "If `eq:incidence-tail` holds, each $C_{t,g}$ has $c_{t,g}=hc_{\mathcal B}$ rows" (§4.5). The row count holds unconditionally; the tail condition only gives $c_{\mathcal B}\le\epsilon D$.
3. **MINOR — loose constant.** `lem:incidence-labels` says "at most $b+w$ incidences sharing $f$ or $v$"; the true bound is $b+w-1$. This is harmless.
4. **MINOR — degenerate case and loose norm.**
   - "$O(Q\log Q)$" in `lem:row-coefficients` degenerates at $Q=1$; it is fine because $R<Q$ forces $Q\ge2$, but $O(Q\log(Q+1))$ would be cleaner.
   - The factor bound $4Q$ can be improved to $2Q$.
5. **MINOR — size of the "sufficiently large $n$" thresholds.**
   - In `lem:incidence-parameters`, $r\ge2$ needs $\sqrt\lambda\ge2\nu^2$, i.e. $\lambda\gtrsim6.4\times10^5$.
   - $6R\le Q$ needs roughly $\sqrt\lambda\ge768(\beta+3)\nu$. For $\beta=1$ that is $\lambda\gtrsim1.1\times10^{10}$, i.e. $n\gtrsim2^{2^{33}}$, and it is larger for the $\beta=O_{k,c}(1)$ used in §5.
   - The asymptotic statements are correct, but the paper should say explicitly that the brute-force fallback covers all such $n$.
6. **MINOR — loose row-sum bound (remark, not an error).**
   - Every basis vector $\psi$ has support $\le2^Q$, so every row of $C_{t,g}$ has $\ell_1$-norm $\le2^Q\ll D=r^{2Q}$.
   - Using $2^Q$ would remove a $\log r$ factor from the measurement cost $\tau\log(2D+1)$.
7. **MINOR — unused hypotheses.** The hypothesis $n\le M\le bn$ in `lem:incidence-labels` and `lem:layout` is not used in their proofs: $M\le bn$ is automatic, and $M\ge n$ is needed only in `lem:incidence-parameters`. Stating where each hypothesis is used would aid cross-checking.

## Verdict

I recomputed every construction, bound and parameter inequality in Section 4, including the worked example. All are correct.
- The section is self-contained linear algebra, plus Hoeffding's inequality and a standard derandomization.
- It delivers exactly the five properties demanded by Definition `def:layout`, with the parameter ranges used in §2, §3, §5 and Appendix B.
- No FATAL issues or GAPs were found; only presentational issues.

The extraordinary overall claim therefore does not fail in this part. Its validity rests on the parts that consume `def:layout` and on the other reductions:
- §3: the Taylor/Hermite recovery and its cost accounting;
- §5: the degree truncation;
- §6: the greedy parity tests;
- Appendix A: sparsification;
- Appendix E: the route actually used for Theorem `thm:main`'s stated bounds.

These must be checked in their own reviews.

VERDICT: SOUND-WITH-MINOR-ISSUES
