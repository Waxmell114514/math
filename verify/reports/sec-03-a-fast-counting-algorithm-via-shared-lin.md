<!-- {"stage": "sec-03-a-fast-counting-algorithm-via-shared-lin", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 363, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 89833, "estimated_cost_usd": 1.8238, "message_id": "msg_011CgS33fLa9yvEUHg8wJaKW", "finished_at": "2026-10-27T03:43:45+00:00"} -->

# Referee report on Section 3, "A fast counting algorithm via shared linear summaries" (`sec:counting`)

## What this part proves

Section 3 is a conditional, essentially self-contained reduction (the "common counting routine"). It makes no bit-complexity claims; those are explicitly deferred to §5.4 and Appendix B. Its inputs are:

- **Factors.** Polynomial factors $\Phi_f$ with scopes $I_f\subseteq[n]$ and coefficients in a commutative $\mathbb Q$-algebra $\mathcal A$.
- **Degree hypothesis** \eqref{eq:general-product-degree}. The product $\prod_f\Phi_f$, taken in incidence indeterminates $Y_{f,v}$ and computed in $\mathcal A[Y]$, has total degree $\le d$.
- **A design** (Definition `def:layout`):
  - partitions $S_{t,g}$ with $|S_{t,g}|\le 2n/r$;
  - assignments $\sigma_f\in[r]^Q$;
  - integer matrices $C_{t,g}$ with every row's $\ell_1$-norm $\le D$ and $\sum_g c_{t,g}\le 2\tau n$;
  - rows $\vec P_{f,v}(T)$ with $\vec P_{f,v}(0)=\delta_v$, degree $\le R$, satisfying the kernel condition;
  - a coefficient-size condition (item 5), which is not used inside §3.

From these it proves the following.

- **Lemma `lem:measurement-separation`.** Fixing integer measurement tuples factorizes a sum of products over groups. The restricted sum $Z_E$ costs $2(2D+1)^c\sum_g 2^{|S_g|}$ examined Boolean vectors.
- **Exact Taylor recovery.**
  - Hermite recovery of $H$ from $[z^j]H(t+z)$, for $t\in[Q]$ and $j<J=\lfloor dR/Q\rfloor+1$.
  - The bound $\deg_{\vec X}[z^j]\mathcal G_x\le j$.
  - Lemma `lem:boolean-differences`, which replaces the substitution $\vec X=x$ by the Boolean substitutions $\vec X=\mathbf 1_U$ together with the restrictions $x_E=1$.
- **Proposition `prop:general-count`.** $Z$ is computed by examining at most $2QrC_q(2D+1)^{2\tau n}2^{2n/r}$ Boolean vectors. Here $C_q=\sum_{s\le\min(q,n)}2^s\binom ns$.
- **Equation \eqref{eq:three-costs}.** When $d=O(n)$, the exponent is $O\big(n[\tfrac RQ\log\tfrac{2Q}R+\tau\log(2D+1)+\tfrac1r]\big)$.

## Dependencies on other parts

**D1. Lemma `lem:incidence-parameters`, eq. \eqref{eq:balanced-cost} (§4.7).**
- *Where used:* only in the closing remark of §3.5.
- *Statement used:* fix $\beta\ge1$ and let $n$ be sufficiently large, with $\lambda=\lceil\log_2 n\rceil$ and $\nu=\lceil\log_2\lambda\rceil$. Assume $b,w\le\lambda^\beta$ and $n\le M\le bn$. Then the choices $r=\lfloor\sqrt\lambda/\nu^2\rfloor$, $Q=\lfloor\lambda/(128\nu)\rfloor$, $R=(\beta+3)\lceil\sqrt\lambda\rceil$, $\tau=1/(r\lambda)$, $D=r^{2Q}$ satisfy:
  - $r\ge2$, $6R\le Q$ (so $1\le R<Q$), and $0<\tau\le 1/2$;
  - $\frac RQ\log\frac{2Q}R+\tau\log(2D+1)+\frac1r=O_\beta(\nu^2/\sqrt\lambda)$.
- *Recomputed:*
  - $R/Q\sim128(\beta+3)\nu/\sqrt\lambda$ and $\log(2Q/R)=O(\nu)$.
  - Since $\log_2 r\le\frac12\log_2\lambda\le\nu/2$, we get $\ln(2D+1)\le\ln3+\frac{\lambda\ln 2}{128}$. Hence $\tau\ln(2D+1)\le\frac{\ln 3}{r\lambda}+\frac{\ln2}{128 r}=O(1/r)$.
  - $1/r=O(\nu^2/\sqrt\lambda)$.

**D2. Lemma `lem:layout` and Lemma `lem:row-coefficients` (§4).**
- These discharge the hypothesis "a design is supplied"; they are not used inside any §3 proof.
- Interface to be cross-checked in the review of §4: they must deliver
  - items 1–4 of `def:layout` with $D=r^{2Q}$, degree $\le R-1\le R$, and $\sum_g c_{t,g}=rhc_{\mathcal B}\le 2\tau n$ (every $C_{t,g}$ keeps all $hc_{\mathcal B}$ rows);
  - item 5 with denominator $(R-1)!Q!$ and $2^{O(Q\log Q)}$ coefficient norm.
- I spot-checked Lemmas `lem:swaps-matrix`, `lem:swaps-support`, `lem:swaps-forms` and the transfer in §4.5. I found no mismatch with `def:layout`.

**D3. Lemma `lem:total-order` (§5) and Proposition `prop:count`.**
- Not used by §3 itself.
- The cost remark "$d=O(n)$" is only realized through $d=k(m_{\rm test}+2(\ell-1))$. That bound is the degree *over $\mathcal A_\ell$*, after $V$-truncation, which is exactly the form \eqref{eq:general-product-degree} requires.

**D4. §5.4 and Appendix B (§§B.2–B.3).**
- All bit-complexity claims are deferred there.
- \eqref{eq:three-costs} is stated conditionally ("if factor evaluation and coefficient arithmetic have polynomial bit cost").

**D5. Overview §§2.2, 2.4, 2.5.**
- These are motivational only.
- The one non-trivial fact asserted but not proved in §3, invertibility of the Hermite matrix, is argued only in §2.5.

## What this part provides to other parts

- **`def:layout`:** the construction target of Lemma `lem:layout`, a hypothesis of Prop. `prop:count`, and the source of $B_P=O(Q\log Q+\log D)$ in App. B.2.
- **Prop. `prop:general-count`:** used by Prop. `prop:count` with $\mathcal A=\mathcal A_\ell$.
- **\eqref{eq:three-costs}:** used in the proof of Thm `thm:overview-sparse-polynomials`, in dimension $n'$.
- **Equations used in App. B.2:** \eqref{eq:hasse-order}, \eqref{eq:jet-substitution}, \eqref{eq:group-sum}, \eqref{eq:group-polynomial}, \eqref{eq:full-taylor-sum} and \eqref{eq:pair-count}, including $M_*\le 3^n(2D+1)^c$.
- **Hermite invertibility statement:** cited in App. B.3.
- **Lemmas `lem:measurement-separation` and `lem:boolean-differences`:** cited in overview §§2.4–2.5.

## Detailed verification

### §3.1: the target and $H$

**$H(0)=Z$.** At $T=0$, $\langle\vec P_{f,v}(0),x\rangle=\langle\delta_v,x\rangle=x_v$. Correct.

**$\deg_T H\le dR$.** Correct, by the following argument.
- Fix $x$. Let $G(Y)=\prod_f\Phi_f(Y_f)\in\mathcal A[Y]$, with the product formed in $\mathcal A[Y]$. Any cancellation caused by zero divisors of $\mathcal A$ is therefore included, and $\deg G\le d$.
- The specialization $\epsilon_x:Y_{f,v}\mapsto\langle\vec P_{f,v}(T),x\rangle\in\mathbb Q[T]$ is an $\mathcal A$-algebra homomorphism $\mathcal A[Y]\to\mathcal A[T]$.
- So the $x$-summand of $H$ equals $\epsilon_x(G)$, and a monomial of degree $j\le d$ maps to $T$-degree $\le jR$.

This homomorphism argument is load-bearing for §5. There, the factor-by-factor degrees sum to $\Theta(km_{\rm test}\ell)=\Theta(n^2)$, and only the degree of the product over $\mathcal A_\ell$ is $O(n)$. The text's one-line justification is correct but terse (Issue 1).

### §3.2: Definition `def:layout`

**Interpretation paragraph.** If $x,x'$ agree outside $S_{t,h}$, with $h\ne\sigma_f(t)$, and have equal $C_{t,h}$-measurements, then $x'_h-x_h\in\ker C_{t,h}$. Item 4 and linearity then give equal values of $\langle\vec P_{f,v}(t),\cdot\rangle$. Iterating over the groups $h\ne g$ shows the inputs of $f$ are determined by $x_g$ and $(C_{t,h}x_h)_{h\ne g}$. Correct.

**Measurement range.** Integrality and row $\ell_1$-norm $\le D$ give Boolean measurements in $[-D,D]\cap\mathbb Z$. Correct.

**Remark on rank versus row sum.** The row $(1,2,\dots,2^{n-1})$ separates all of $\{0,1\}^n$. Correct and apt.

**Item 5.** Not used anywhere in §3 (Issue 4).

### §3.3: Lemma `lem:measurement-separation`

**Identity.** Fix $\vec y$, with representatives $\bar x_h\in\mathcal X_h(y_h)$.
- For $x_h\in\mathcal X_h(y_h)$ we have $x_h-\bar x_h\in\ker C_h$.
- Replacing the components one group at a time uses invariance at points of $\mathbb Q^n$. In fact all intermediate points are Boolean, so the hypothesis is used only on $\{0,1\}^n$.
- This gives $A_g(\sum_h x_h)=A_g(x_g+\sum_{h\ne g}\bar x_h)$.
- The fibre of $\vec y$ under the restriction $x_E=1$ is $\prod_g\mathcal X_{g,E}(y_g)$. Distributivity yields $\prod_g\Sigma_g(\vec y)$.
- Each Boolean $x$ has exactly one tuple in $\mathcal Y$. Hence $Z_E=\sum_{\vec y}\prod_g\Sigma_g$. Correct.

**Count of examined vectors.** For each $\vec y$:
- the representative scan examines $\le\sum_g2^{|S_g|}$ vectors;
- the summation scan examines $\le\sum_g2^{|S_g|}$ vectors;
- and $|\mathcal Y|=(2D+1)^c$.

This gives $2(2D+1)^c\sum_g2^{|S_g|}$. Correct.

**Per-vector costs.**
- At most one $A_g$ evaluation per vector.
- Measurement and fixed-bit checks take $O(c_g|S_g|\log(D+2))$ bit operations.
- Ring operations: one addition per vector, plus $r$ multiplications and one addition per tuple. The per-tuple operations amortize because $\sum_g 2^{|S_g|}\ge r$.

**Space.** $\vec y$ uses $O(c\log(D+2))$ bits, the representatives $n$ bits, and three ring elements. Correct.

**Application to $H(t)$.** For $h\ne g$ and $\xi\in\ker C_{t,h}$, every $f$ with $\sigma_f(t)=g$ has unchanged inputs by item 4. So $A_g=\prod_{\sigma_f(t)=g}\Phi_f$ is invariant. Correct.

### §3.4: Taylor coefficients

**Interpolation parameters.**
- $QJ=Q\lfloor d_H/Q\rfloor+Q>d_H$. Correct.
- Hermite: the data map is $\mathsf V\otimes\mathrm{id}_{\mathcal A}$ with $\mathsf V_{(t,j),u}=\binom uj t^{u-j}$.
- $\mathsf V$ is nonsingular over $\mathbb Q$: a nonzero rational polynomial of degree $<QJ$ cannot be divisible by $\prod_{t=1}^Q(T-t)^J$.
- Hence $\mathsf V^{-1}\otimes\mathrm{id}$ recovers $H$ over any $\mathbb Q$-algebra. Correct, but the proof is not in §3 (Issue 2).

**Jet substitution.** $\langle\vec P(t),x\rangle+\langle\vec P(t+z)-\vec P(t),x\rangle=\langle\vec P(t+z),x\rangle$, so $\sum_x\mathcal G_x(x,z)=H(t+z)$. Correct.

**\eqref{eq:degree-cost}.** Correct, via a weight argument.
- Give $z$ weight $1$ and each $X_i$ weight $-1$.
- Every input is a rational constant plus terms $z^aX_i$ with $a\ge1$, so all of its terms have weight $\ge0$.
- Products and sums over $\mathcal A$ preserve "all weights $\ge0$", and cancellation only removes terms.
- Hence any term $z^jX^\alpha$ satisfies $|\alpha|\le j$. This holds independently of $d$.

**Lemma `lem:boolean-differences`.** Correct over any commutative ring.
- Multilinearization keeps Boolean values and does not raise degree.
- The multilinear representation of a function $\{0,1\}^n\to\mathcal A$ is unique.
- Möbius inversion gives $c_{x,E}=\sum_{U\subseteq E}(-1)^{|E\setminus U|}p_x(\mathbf 1_U)$, and $c_{x,E}=0$ for $|E|>q$.
- Interchanging the sums gives \eqref{eq:boolean-differences}.

**Sanity check.** Take $n=1$, $\Phi=X_1^2$, row $1+T$ (so $R=1$, $d=2$), and $Q=2$, so $q=1$.
- The four restricted sums give $(1+t)^2-(1+t)^2+\big[(1+t)^2+2(1+t)z\big]$.
- This equals $H(t+z)\bmod z^2$. Correct.

**Application of the lemma.**
- For $j\le J-1=q$, $\deg_{\vec X}[z^j]\mathcal G_x\le q$, so one family of pairs $U\subseteq E$ with $|E|\le q$ serves all $j$.
- Extracting $[z^j]$ commutes with Boolean specialization.
- $\mathcal A[z]\to\mathcal A[z]/(z^J)$ is a ring homomorphism.
- $A_{g,U}$ is invariant: the original inputs are invariant by item 4, and the corrections $\langle\Delta\vec P_{f,v}(z),\mathbf 1_U\rangle$ do not depend on $x$.
- \eqref{eq:boolean-enumeration}: from $c\le2\tau n$ and $|S_{t,g}|\le 2n/r$, $2(2D+1)^c\sum_g2^{|S_g|}\le 2r(2D+1)^{2\tau n}2^{2n/r}$. Correct.
- \eqref{eq:full-taylor-sum}. Correct.

### §3.5: three costs

**Pair count.** $C_q$ counts the pairs $U\subseteq E$ with $|E|\le q$. $C_0=1$, and $C_q=3^n$ for $q\ge n$. Correct.

**\eqref{eq:finite-difference-cost}.** $\eta^qC_q\le\sum_{s\le\min(q,n)}(2\eta)^s\binom ns\le(1+2\eta)^n$ for $0<\eta\le1$. Correct.

**Prop. `prop:general-count`.**
- Total examined vectors: $Q\cdot C_q\cdot 2r(2D+1)^{2\tau n}2^{2n/r}$. Correct.
- Each examined vector requires at most $|\mathcal F|$ factor evaluations in $\mathcal A[z]/(z^J)$.
- A truncated product costs $O(J^2)$ $\mathcal A$-operations.
- Precomputing $\vec P_{f,v}(t)$ and the shifted corrections takes polynomially many rational operations per $(t,U)$.
- The interpolation system is $QJ\times QJ$.
- Storage is the current indices, the accumulators and $QJ$ elements of $\mathcal A$. Correct.

**Cost of $C_q$ when $d=O(n)$.** With $\eta=R/Q<1$:
$$\ln C_q\le q\ln(Q/R)+n\ln(1+2R/Q)\le O\!\big(n\tfrac RQ\ln\tfrac QR\big)+2n\tfrac RQ=O\!\big(n\tfrac RQ\log\tfrac{2Q}R\big).$$
Correct.

**\eqref{eq:three-costs}.** It follows from $\log_2(2D+1)^{2\tau n}=2\tau n\log_2(2D+1)$. Correct.

**Closing remark.** Recomputed under D1. It holds with constant $O_\beta$, given $d=O(n)$.

## Issues

1. **MINOR (§3.1, "multiply the degree by at most $R$").**
   - The bound $\deg_TH\le dR$ is correct only via the specialization-homomorphism argument applied to the already-formed product in $\mathcal A[Y]$.
   - A factor-by-factor reading gives the useless bound $R\sum_f\deg\Phi_f$. In the $\mathcal A_\ell$ application that bound is quadratic in $n$.
   - Since this is exactly where the $V$-truncation trick of §5 pays off, the one-line justification should say so explicitly.

2. **MINOR (§3.4, Hermite step).**
   - "The rational Hermite matrix … is invertible over $\mathbb Q$" is asserted without proof in §3, yet App. B.3 cites "the Hermite interpolation statement in Section `sec:counting`".
   - The proof is the divisibility argument given only in overview §2.5.
   - Add that line (and note $\mathsf V\otimes\mathrm{id}_{\mathcal A}$).

3. **MINOR (\eqref{eq:degree-cost}).** "Each occurrence of $\vec X$ carries a factor of $z$" is correct, but it should be stated as the weight argument above. That argument also shows the bound is independent of cancellations in $\mathcal A$.

4. **MINOR (Definition `def:layout`, item 5, and the opening of §3).**
   - Item 5 hard-wires the denominator $(R-1)!Q!$ of the §4 construction into a generic interface whose item 4 only demands degree $\le R$.
   - Item 5 is never used in §3. Its $\log D$ slack exceeds what Lemma `lem:row-coefficients` needs.
   - The hypothesis $\tau\le1/2$ is likewise unused.
   - The opening sentence "Here the factors can be any rational polynomials" contradicts the later, needed generality of $\mathcal A$-coefficients.

5. **MINOR (notation).** Several symbols are overloaded across the paper:
   - $\mathcal A$: coefficient algebra here; the incidence set in eq. \eqref{eq:factor-incidences}; a ring in App. E.
   - $D$: row-sum bound here; clause density in Thm `thm:main`.
   - $J$: Hermite multiplicity here; a subset of $[Q]$ in Lemma `lem:swaps-support`; a group count in Lemma `lem:tensor-sparse-query`.
   - Also $C_q$ versus $C_{t,g}$, $E$ versus $E_{u,y}$, and $T$ versus $T_t$.

6. **MINOR (end of §3.5).**
   - "Makes their sum $O((\log\log n)^2/\sqrt{\log n})$" hides the dependence on $\beta$.
   - It also silently requires $d=O(n)$ for the first term to represent $\log C_q/n$.
   - Prop. `prop:general-count` lists $D$, rather than $\log D$, among the parameters of the per-vector overhead. This is harmless but looser than Lemma `lem:measurement-separation`.

No FATAL or GAP issues were found in this part.

## Verdict

Section 3 is a correct, generic and honestly stated reduction. Every identity, count and estimate was rechecked, including the amortized operation counts, the weight argument for \eqref{eq:degree-cost}, Möbius inversion over arbitrary commutative rings, and the $C_q$ estimate. It introduces no hidden exponential cost.

It carries none of the extraordinary content of the paper. The claimed $2^{o(n)}$ bound rests entirely on the realizability of its hypotheses:
- designs with $R/Q\to0$, $\tau\log D=O(1/r)$ and $r\to\infty$ (§4: `lem:layout`, `lem:incidence-parameters`);
- $d=O(n)$ over $\mathcal A_\ell$ (§5: `lem:total-order`);
- polynomial bit cost (App. B).

These must be validated in the reviews of those parts; my spot-check found the interface between them and `def:layout` consistent.

VERDICT: SOUND-WITH-MINOR-ISSUES
