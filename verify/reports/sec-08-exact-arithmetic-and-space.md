<!-- {"stage": "sec-08-exact-arithmetic-and-space", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 351, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 64470, "estimated_cost_usd": 1.3165, "message_id": "msg_011CgS4F7FUbpddbRonJxDfV", "finished_at": "2026-10-27T03:55:54+00:00"} -->

## What this part proves

Appendix B ("Exact arithmetic and space") supplies the bit-complexity and space accounting that Proposition `prop:count` and Section 2.6 defer to it.

- **B.1, Lemma `lem:rational-lift-height`.**
  - The $h$-adic digits $e_j=a_j+b_jY$ of $p_\ell=\sum_{j<\ell}e_jh^j$, with $h=Y^2-Y$, are integral.
  - They satisfy $|a_j|,|b_j|\le 2^{C\ell^2}$.
  - They are computable in $\poly(\ell)$ time and space.
- **B.2, streaming bounds.** Set $d_{\rm den}=(R-1)!Q!$, $\Delta=d_{\rm den}^k$, $\Gamma=\Delta^{2\ell-1}$ and $\Omega=\Gamma^{m_{\rm test}}$.
  - Every substituted input, lifted factor, group sum, partial product and Taylor accumulator $T_t$ lies in $\mathbb Q[z,V]/(z^J,V^\ell)$.
  - Each has a denominator dividing a fixed power of $\Gamma$.
  - Each has an integer numerator of $\ell_1$-norm at most $M_*2^nB_1^{m_{\rm test}}$.
  - This yields \eqref{eq:sum-bit-bound}.
- **B.3, exact read-out.**
  - For each $s<\ell$, $H_s(0)=N_H/(\Omega D_H)$, by Cramer's rule on the integer Hermite (confluent Vandermonde) matrix.
  - Both determinants are computed by Bareiss elimination in polynomial bit cost.
  - $N(\mathcal P)$ is the least nonnegative residue of $\sum_sH_s(0)$ modulo $2^\ell$.
- **B.4, overview arithmetic.** A sketch that the bounded-occurrence algorithm of §2 has polynomial bit overhead and uses polynomial space.

## Dependencies on other parts

- **D1. Lemma `lem:rational-idempotent` (§5.1).**
  - For every $\ell\ge1$, $p_\ell(Y)=(1-Y)^\ell\sum_{j<\ell}\binom{\ell+j-1}{j}Y^j\in\mathbb Z[Y]$ and $\deg p_\ell=2\ell-1$.
  - The $e_j$ are the successive remainders of division by the monic $h$, with $\deg e_j\le1$.
  - The congruence property is used only via D7.
- **D2. Definition `def:layout`, used with $1\le R<Q$, $0<\tau\le1/2$, $D\ge1$.**
  - Item 1: a partition, so $\sum_g|S_{t,g}|=n$.
  - Item 3: integer $C_{t,g}$ with absolute row sums at most $D$, and $\sum_gc_{t,g}\le2\tau n\le n$.
  - Item 4: $\deg\vec P_{f,v}\le R$.
  - Item 5: $d_{\rm den}\vec P_{f,v}$ is integral with $O(Q\log Q+\log D)$-bit coefficients.
- **D3. Lemma `lem:row-coefficients`.**
  - $d_{\rm den}\vec P_{f,v}(T)$ is integral with total coefficient $\ell_1$-norm $2^{O(Q\log Q)}$, under the hypothesis $R<Q$.
  - It is the source of D2 item 5 in the application, and is used directly in B.4.
- **D4. Lemma `lem:measurement-separation` and its algorithm.**
  - Only attainable tuples are processed, at most $(2D+1)^c$ of them.
  - Factors are evaluated at the Boolean vector $u+\sum_{h\neq g}\bar x_h$.
  - Each group sum runs over at most $2^{|S_g|}$ vectors.
- **D5. Correctness inputs.**
  - Eq. \eqref{eq:full-taylor-sum} together with Lemma `lem:boolean-differences` and Proposition `prop:general-count`.
  - Used here: the signed sum over pairs $U\subseteq E$ with $|E|\le J-1$ equals $\mathcal H_t(z)$ in $\mathcal A_\ell[z]/(z^J)$.
- **D6. Hermite invertibility.**
  - Eq. \eqref{eq:hasse-order}: $J=\lfloor d_H/Q\rfloor+1$, so $QJ>d_H$.
  - The confluent Vandermonde matrix at the nodes $1,\dots,Q$ with multiplicity $J$ is invertible. This is asserted in §3.4 and proved by the divisibility argument of §2.5.
- **D7. Eq. \eqref{eq:origin-residue}, via Lemma `lem:total-order`.**
  - $\deg_T[V^s]H\le d_H=kR(m_{\rm test}+2(\ell-1))$.
  - $H_s(0)\in\mathbb Z$.
  - $\mathcal S_\ell(H(0))\equiv N(\mathcal P)\pmod{2^\ell}$.
- **D8. Form of the factors.**
  - Eq. \eqref{eq:lifted-factor} and §5.1: $L_i$ is a sum of at most $S$ normalized monomials of degree at most $k$.
  - One replacement row is used per (equation, variable) pair.
  - The neutral factors are constant one.
  - This is a hypothesis of Proposition `prop:count`, with $2^\ell>2^n$.
- **D9. For B.4.**
  - The §2.4 algorithm, with design condition 4 guaranteeing that the $\vec\lambda_{e,v,h}$ exist.
  - $M\le3n$ and $J=\lfloor3nR/Q\rfloor+1$.
  - The §2.8 construction, which coincides with §4 for $b=w=3$.
- **D10. External.** Bareiss (1968): fraction-free elimination whose retained entries are minors, with $O(M^3)$ operations and exact divisions. This is correctly cited.

**Provided to other parts.**
- Lemma `lem:rational-lift-height` supports Lemma `lem:rational-idempotent`'s size, time and space claims. Appendix E's Lemma `lem:tensor-sparse-query` relies on these $e_j$ being constructible in polynomial time.
- \eqref{eq:sum-bit-bound}, the interpolation cost and the space bound support Proposition `prop:count`. Through it they support Theorem `thm:overview-sparse-polynomials`, §6.3 and Proposition `prop:interpolation-bound`.
- B.4 supports the bit and space claims behind \eqref{eq:overview-bounded-time} in §2.6 and §2.9.
- The final proof of Theorem `thm:main` (Appendix E) uses only B.1 from this part.

## Detailed verification

### Lemma `lem:rational-lift-height`

**Initial norm.**
- $\|(1-Y)^\ell\|_1=2^\ell$.
- By the hockey-stick identity, $\sum_{j=0}^{\ell-1}\binom{\ell-1+j}{j}=\binom{2\ell-1}{\ell-1}\le2^{2\ell-1}$.
- Hence $\|p_\ell\|_1\le2^{3\ell-1}$. ✓

**Integrality.** $h$ is monic in $\mathbb Z[Y]$, so all quotients and remainders are integral. ✓

**One elimination step.** At degree $d$ with leading coefficient $c$:
- The dividend becomes $g-cY^d+cY^{d-1}$, so its norm does not increase.
- The quotient gains $cY^{d-2}$, with $|c|\le\|g\|_1$.
- So the potential (quotient norm plus remainder norm) at most doubles. The paper's "factor three" is valid.

**Number of eliminations.** $\sum_{i=1}^{\ell-1}2i=\ell(\ell-1)$. ✓

**Conclusion.**
- $|a_j|,|b_j|\le2^{3\ell}3^{\ell^2}\le2^{5\ell^2}$, so $C=5$ works for all $\ell\ge1$.
- There are $O(\ell^2)$ operations on $O(\ell^2)$-bit integers.
- Forming $p_\ell$ itself is also cheap. ✓

**Sharper bound (not needed).**
- Within one division the dividend norm never increases, so $\|q_{j+1}\|_1\le2\ell\|q_j\|_1$.
- This gives $\|e_j\|_1\le(2\ell)^j2^{3\ell}=2^{O(\ell\log\ell)}$.

### B.2 (claim by claim)

**$B_0$.** Each of the three evaluations in $\theta$ is bounded after clearing $d_{\rm den}$:
- $\langle\vec P(t),x\rangle$ is bounded by $n(R+1)2^{B_P}Q^R$.
- $\langle\vec P(t+z),\mathbf1_U\rangle$ is bounded by $n(R+1)2^{B_P}(Q+1)^R$, since $\|(t+z)^\rho\|_1=(t+1)^\rho$.
- $\langle\vec P(t),\mathbf1_U\rangle$ is bounded by the same quantity.

The extra summand $d_{\rm den}$ only secures $d_{\rm den}\le B_0$. The argument $u+\sum_{h\ne g}\bar x_h$ is Boolean (D4), so the bound applies. ✓

**Monomials and $L_i$.**
- $\Delta\prod_{v\in M}\theta=d_{\rm den}^{k-|M|}\prod(d_{\rm den}\theta)$, with norm at most $B_0^k$. This includes the constant monomial.
- Hence $\|\Delta L_i\|_1\le SB_0^k\le B$. ✓

**Logarithms.**
- $\log d_{\rm den}\le2Q\log Q$.
- $\log B_0=O(Q\log(Q+2)+\log(nD+2))$, using $R<Q$.
- $\log B=O(k\log B_0+\log(S+2))$. ✓

**Lifted factor.**
- Term $j$ of $\Gamma\mathcal B_i$ equals $\Delta^{2(\ell-1-j)}\cdot(a_j\Delta+b_jA_i)\cdot(A_i(A_i-\Delta))^j$.
- Its norm is at most $E_\ell(B+\Delta)^{2\ell-1}$.
- Summing over $j<\ell$ gives at most $B_1$, and truncation only lowers norms.
- $\log B_1=O(\ell^2+\ell\log(B+\Delta+2))$, using $\log E_\ell=O(\ell^2)$ from B.1. ✓

**Group products, sums and partial products.** Using $\|fg\|_1\le\|f\|_1\|g\|_1$, $\sum_g|S_g|=n$ and $B_1\ge1$:
- the group product $A_{g,U}$ is bounded by $B_1^{m_{{\rm test},g}}$ over $\Gamma^{m_{{\rm test},g}}$;
- the group sum $\Sigma_g$ is bounded by $2^{|S_g|}B_1^{m_{{\rm test},g}}$;
- the partial product $\Pi_g$ is bounded by $2^nB_1^{m_{\rm test}}$ over a divisor of $\Omega$. ✓

**Accumulator.**
- The number of updates is $M_*\le C_q(2D+1)^c\le3^n(2D+1)^c$.
- Every partial sum satisfies $\|\Omega T_t\|_1\le M_*2^nB_1^{m_{\rm test}}$.
- $\log\Omega=k(2\ell-1)m_{\rm test}\log d_{\rm den}$. ✓

**Resulting bit length.** Using $c\le2\tau n\le n$, the bit length is
$$O\big(n\log(D+2)+m_{\rm test}\ell^2+m_{\rm test}\ell(kQ\log(Q+2)+k\log(nD+2)+\log(S+2))\big).$$
- This is polynomial in the parameters of \eqref{eq:sum-bit-bound}.
- In the application ($\ell=n+1$, $m_{\rm test}=O(n)$, $Q=O(\log n)$) it is $O(n^3)$ bits per coefficient.
- Each stored element has at most $J\ell$ coefficients. ✓

**Space.**
- The working state is: the current indices, the representatives, one group sum, one partial product, $T_t$, and $QJ\ell$ Taylor coefficients.
- This is polynomial. ✓

### B.3 Interpolation

**The matrix.**
- $[z^j](t+z)^u=\binom uj t^{u-j}$, so $\mathsf V$ is the correct square $QJ\times QJ$ Hermite matrix.
- Entries are at most $2^{M_H}Q^{M_H}$, i.e. $O(M_H\log(Q+2))$ bits. ✓
- It is nonsingular by D6.
- $\mathsf V\mathbf h=\mathbf y$ uses $\deg H_s\le d_H<M_H$ (D7). ✓

**Cramer's rule.**
- $\mathbf b=\Omega\mathbf y$ is integral by B.2.
- Cramer's rule applied to $\mathsf V(\Omega\mathbf h)=\mathbf b$ gives $h_0=N_H/(\Omega D_H)$. ✓

**Bareiss elimination.**
- Retained entries are (signed) minors, also under row pivoting.
- A minor is a sum of at most $M_H!$ products of at most $M_H$ entries, which gives the stated bound (loosely).
- The cost is $\poly(M_H,B_{\rm data})$ bit operations and space. ✓
- $\mathsf V^{(0)}$ can be singular when $H_s(0)=0$; pivoting handles this. ✓

**Read-out.**
- $H_s(0)\in\mathbb Z$ (D7), so the division is exact.
- $u\equiv N(\mathcal P)\pmod{2^\ell}$ and $0\le N(\mathcal P)\le2^n<2^\ell$, so the least residue equals the count.
- On branches the count is at most $2^{n'}\le2^n$. ✓
- Repeating the interpolation $\ell$ times reuses the same workspace. ✓

### B.4 Overview arithmetic

- Row coefficients have $O(Q\log Q)$ bits (D3; the overview has $6R\le Q$).
- Basic solutions $\vec\lambda$ of the poly-size systems have polynomial bit length.
- $\delta$, the product of poly-many poly-bit denominators, has poly bits.
- Each linear input (local part, plus $\sum\langle\vec\lambda,y_h\rangle$ with $|y_h|_\infty\le D$, plus the shift correction) has denominator dividing $\delta$.
- $\Phi_e$ is multilinear in its at most 3 inputs, so the full product has denominator dividing $\delta^{M}\mid\delta^{3n}$.
- Sums of $2^{O(n)}$ such terms keep polynomial length.
- The B.3 read-out applies with $\Omega$ replaced by $\delta^{3n}$, and $H(0)=\#F\in\mathbb Z$. ✓ (sketch)

## Issues

1. **MINOR (B.2, definition of $\theta$).** The input is defined as $\theta_{f,v}(z;x)$ and in the next sentence used as $\theta_{i,v}$. The factor index $f$ silently becomes the equation index $i$.

2. **MINOR (notation overloads inside the part).** None of these causes a mathematical error.
   - $B$ (norm bound) clashes with the sparsification occurrence bound $B$ (§6, Lemma `lem:sparsify`).
   - $\Pi_g$ (partial products) clashes with the permutation matrices $\Pi_s$ (§4).
   - $u$ is used three ways: monomial degree, column index of $\mathsf V$, and $u=\sum_sH_s(0)$.
   - $\Delta=d_{\rm den}^k$ clashes with the shift $\Delta\vec P$ of §3.4.
   - $T_t$ clashes with the variable $T$.
   - $\delta$ clashes with $\delta_v$.
   - $h(Y)$ clashes with $\mathbf h$ and $h_0$.
   - $D_H, M_H$ clash with $D, M$.
   - The absolute constant $C$ clashes with $C_{t,g}$.
   - $S$ (total length) clashes with $S_g$.

3. **MINOR (B.1, proof of Lemma `lem:rational-lift-height`).**
   - "Increases ... by at most a factor of three" is correct but loose; the factor is two.
   - The whole $2^{O(\ell^2)}$ bound can be sharpened to $2^{O(\ell\log\ell)}$, since the dividend norm never increases.
   - This would shrink the dominant $m_{\rm test}\ell^2$ term in B.2. No effect on correctness.

4. **MINOR (B.2).** Two parts of the setup are unexplained or unused, but harmless.
   - The additive term $d_{\rm den}$ in $B_0$ is unexplained; it exists only to ensure $d_{\rm den}^{k-u}B_0^u\le B_0^k$.
   - The stated inequality $B_1\ge\Gamma$ is never used.

5. **MINOR (B.2).** "Precision $\ell$ such that $2^\ell>2^n$" just means $\ell\ge n+1$. It would help to say explicitly that on a branch with $n'$ free variables the bound $2^{n'}<2^\ell$ is what is needed.

6. **MINOR (B.3).**
   - The minor bound charges $B_{\rm data}$ $M_H$ times, although any minor uses at most one entry from the column $\mathbf b$.
   - The reference "Hermite interpolation statement in Section 3" points to an assertion whose proof is in §2.5. Cite §2.5 or the divisibility argument directly.

7. **MINOR (B.4, presentation).** B.4 is only a sketch and leaves three routine points implicit. The stated conclusion holds in each case.
   - **(a)** The systems for $\vec\lambda_{e,v,h}$ are typically rank-deficient. A basic solution (Gaussian elimination or Cramer on a nonsingular subsystem) must be chosen to guarantee polynomial bit length.
   - **(b)** Unlike Lemma `lem:measurement-separation`, the §2.4 algorithm evaluates $B_{t,g}(\vec y)$ also for unattainable $\vec y$. There the linear inputs are not of the form $\langle\vec P_{e,v}(t),x\rangle$ with Boolean $x$. The bound still holds because $|y_h|_\infty\le D$ and denominators divide $\delta$.
   - **(c)** The Taylor-shift coefficients of $\vec P_{e,v}(t+z)$ must also be covered by $\delta$. They are, because their denominators divide those of the row coefficients.

No FATAL or GAP issues were found in this part. All displayed bounds were recomputed and hold, mostly with room to spare. Correctness of the identities feeding the accumulator (D5) and of $\deg_T H\le d_H$ (D7) is assumed from other parts and should be cross-checked there.

## Verdict

The appendix does what it claims. Every intermediate rational has a fixed, polynomially bounded denominator and a numerator whose bit length grows only logarithmically in the number of summands. The integer Hermite read-out via Cramer's rule and Bareiss elimination is correct and polynomial. The only defects are notational and presentational, plus the sketchiness of B.4, which concerns the overview algorithm and not the main proof path.

VERDICT: SOUND-WITH-MINOR-ISSUES
