<!-- {"stage": "sec-05-counting-common-zeros-of-sparse-polynomi", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 363, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 116059, "estimated_cost_usd": 2.3483, "message_id": "msg_011CgS33fMZDCUZtcxd1CLeD", "finished_at": "2026-10-27T03:47:15+00:00"} -->

## What this part proves

Section 5 (label `sec:setup`) proves **Theorem `thm:overview-sparse-polynomials`**: for fixed $k\ge2$ and $c\ge1$, take $m_{\rm test}\le cn$ polynomials over $\mathbb F_2$ on $n\ge20$ variables, each a list of at most $(\log n)^c$ monomials of degree at most $k$. Their number of common zeros is computed deterministically in $2^{O_{k,c}(n(\log\log n)^2/\sqrt{\log n})}$ bit operations and $n^{O_{k,c}(1)}$ space.

The intermediate results are:

- **Lemma `lem:rational-idempotent`.**
  - $p_\ell=1-F_\ell=(1-Y)^\ell\sum_{j<\ell}\binom{\ell+j-1}{j}Y^j$ satisfies $p_\ell(y)\equiv\mathbb 1_{2\mid y}\pmod{2^\ell}$.
  - $p_\ell=\sum_{j<\ell}e_jh^j$ with $h=Y(Y-1)$, $e_j\in\mathbb Z[Y]$ and $\deg e_j\le1$.
- **Lemma `lem:total-order`.**
  - Truncating the product of the $V$-graded lifts modulo $V^\ell$ and then applying $\mathcal S_\ell$ gives the product of parity indicators modulo $2^\ell$.
  - Each retained coefficient has input degree at most $d_*(m+2(\ell-1))$.
- **§5.3.** The factors $\mathcal B_i$ over $\mathcal A_\ell=\mathbb Q[V]/(V^\ell)$ satisfy (`eq:general-product-degree`) with $d=k(m_{\rm test}+2(\ell-1))$, which gives (`eq:origin-residue`).
- **Proposition `prop:count`.** Given a design satisfying Definition `def:layout`, $N(\mathcal P)$ is computed in $\poly(\cdot)\,C_q(2D+1)^{2\tau n}2^{2n/r}$ bit operations and polynomial space.
- **Proof of the theorem.**
  - Branch on variables with more than $b_0$ incidences.
  - Apply Lemma `lem:incidence-parameters` and Lemma `lem:layout` on each branch, then Proposition `prop:count`.
  - Use an exhaustive-search fallback for finitely many $n$.

## Dependencies on other parts

- **D1. Definition `def:layout` (§3.2).**
  - Parameter range: $r\ge2$, $D\ge1$, $1\le R<Q$, $0<\tau\le\frac12$.
  - (1) $|S_{t,g}|\le 2n/r$.
  - (3) $C_{t,g}$ are integer matrices with absolute row sums at most $D$, and $\sum_g c_{t,g}\le2\tau n$.
  - (4) $\vec P_{f,v}(0)=\delta_v$, $\deg\le R$, and the kernel condition for $g\ne\sigma_f(t)$.
  - (5) $d_{\rm den}=(R-1)!Q!$ clears denominators, and coefficients have $O(Q\log Q+\log D)$ bits.
- **D2. §3.1, over an arbitrary commutative $\mathbb Q$-algebra $\mathcal A$.**
  - Hypothesis: the product in independent incidence indeterminates has degree at most $d$ over $\mathcal A$, and the rows have degree at most $R$ with $\vec P(0)=\delta_v$.
  - Conclusion: $H(0)=Z$ and $\deg_TH\le dR$.
- **D3. Proposition `prop:general-count` (§3.5), used with $\mathcal A=\mathcal A_\ell$.**
  - It returns $H(0)\in\mathcal A_\ell$ after examining at most $2QrC_q(2D+1)^{2\tau n}2^{2n/r}$ Boolean vectors.
  - It performs at most $|\mathcal F|$ factor evaluations in $\mathcal A[z]/(z^J)$ per vector, with polynomial overhead and polynomial storage.
  - Internally it uses Lemma `lem:measurement-separation`, Lemma `lem:boolean-differences`, (`eq:degree-cost`), and Hermite interpolation with $QJ>d_H$.
- **D4.** (`eq:hasse-order`), (`eq:pair-count`), (`eq:finite-difference-cost`), the derived bound $\log C_q\le q\log(Q/R)+n\log(1+2R/Q)$, and (`eq:three-costs`) when $d=O(n)$.
- **D5. Lemma `lem:layout`.**
  - Hypotheses: scopes of size at most $w$; incidence at most $b$; $n\le M\le bn$; $r\ge2$; $1\le R<Q$; $0<\tau\le\frac12$; $D=r^{2Q}$.
  - Further hypotheses: $2(b+w)D^2\le M$, $2Qr^2\le n$, and an interval $\mathcal I$ with $\Pr[W\notin\mathcal I]\le\tau/(rb)$.
  - Conclusion: all data of Definition `def:layout`, rows of degree at most $R-1$, constructed in $\poly(n,M,|\mathcal F|,D,Q,r,b,w)$ time.
- **D6. Lemma `lem:incidence-parameters`.**
  - Hypotheses: fixed $\beta\ge1$, $b,w\le\lambda^\beta$, $n\le M\le bn$.
  - Conclusions, eventually and uniformly in $(b,w,M)$: the hypotheses of D5 hold, $R\ge32$, $6R\le Q$, $D\le2^{\lambda/128}$, and (`eq:balanced-cost`).
  - The checks are exact in $\poly_\beta(\log n)$ time.
  - Used here with $(n',M',b,w,\beta)$.
- **D7. Lemma `lem:row-coefficients`**, used through D1(5).
- **D8. Lemma `lem:rational-lift-height` (App. B).** Coefficients of the $e_j$ are integers of size at most $2^{C\ell^2}$, constructed in $\poly(\ell)$ time.
- **D9. App. B §§B.2–B.3.**
  - (`eq:sum-bit-bound`) over the fixed denominators $\Gamma^{m_{{\rm test},g}}$ and $\Omega$.
  - Exact Hermite read-out (Cramer/Bareiss) and the final residue.

**Provides to other parts:**

- Theorem `thm:overview-sparse-polynomials` goes to §6 (Lemma `lem:greedy-hashes`, §`subsec:count-sparse`) and to Proposition `prop:interpolation-bound`. It needs only the number, degree and sparsity of the equations, so it applies to discarded candidates too.
- Lemma `lem:rational-idempotent` goes to App. B and to Lemma `lem:tensor-sparse-query`.
- Lemma `lem:total-order` goes to App. D, via (`eq:sharp-incidence-degree`) and (`eq:sharp-branch-residue`), where it is transferred to $\mathbb Z/2^p$ by the reduction homomorphism.
- (`eq:origin-residue`) and the denominators $\Delta,\Gamma,\Omega$ go to App. B.

## Detailed verification

**§5.1.**
- $L_i(x)\equiv P_i(x)\pmod 2$ on Boolean $x$; this holds even without combining duplicate monomials.
- $\deg L_i\le k$.
- $\ell=n+1$ suffices because $N\le2^n<2^\ell$.
- Correct.

**Lemma `lem:rational-idempotent`.**
- The coefficient of $Y^j$ in $(1-Y)^{-\ell}$ is $\binom{\ell+j-1}{j}$ (weak compositions). Correct.
- $p_\ell-1\in\mathbb Z[Y]$ vanishes below degree $\ell$, so $p_\ell=1+Y^\ell g$ with $g\in\mathbb Z[Y]$. The cofactor of $(1-Y)^\ell$ is integral. Both congruences are therefore correct.
- $\deg p_\ell=2\ell-1$, so the $h$-adic digits stop at $j=\ell-1$, and monic division keeps integrality.
- Independent checks:
  - $p_2=1-3Y^2+2Y^3=(1-Y)+(2Y-1)h$.
  - By division, $p_3=1-10Y^3+15Y^4-6Y^5=(1-Y)+(2Y-1)h+(3-6Y)h^2$, with $p_3(2)=-31\equiv1$ and $p_3(3)=-512\equiv0\pmod 8$.
- In general $p_\ell$ is the idempotent $(1,0)$ of $\mathbb Q[Y]/(h^\ell)$. Using $Y^2=Y+h$ this gives a closed form:
  - $e_0=1-Y$;
  - $e_j=\tfrac{(-1)^j}{2}\binom{2j}{j}(1-2Y)$ for $j\ge1$.
- Hence $|a_j|,|b_j|<4^j$. The $\poly(\ell)$ claim holds with room to spare; App. B's $2^{O(\ell^2)}$ bound is valid but crude.

**Lemma `lem:total-order`.**
- A term with $\sum j_i=s$ is divisible by $2^s$ at integers, so dropping $s\ge\ell$ changes the sum by a multiple of $2^\ell$.
- The untruncated sum is $\prod_i p_\ell(y_i)$.
- The degree of a retained term is $\sum_i d_*(1+2j_i)\le d_*(m+2(\ell-1))$; the sharper bound $d_*(m+2s)$ holds for the $V^s$ coefficient.
- The $\ell=2$ example was rechecked modulo 4 at $(y_1,y_2)\in\{(0,0),(1,0),(2,0),(2,2),(3,0),(3,3),(2,1)\}$. All correct.

**§5.3.**
- The coefficient of $V^s$ in $\prod_i\mathcal B_i$ is $\sum_{\sum j_i=s}\prod_i e_{j_i}(L_i)h(L_i)^{j_i}$, of degree at most $k(m_{\rm test}+2s)$. So (`eq:general-product-degree`) holds over $\mathcal A_\ell$ with $d=k(m_{\rm test}+2(\ell-1))$.
- Neutral factors have degree $0$.
- Substitution $Y_{f,v}\mapsto\langle\vec P_{f,v}(T),x\rangle$ is a ring homomorphism $\mathcal A_\ell[Y]\to\mathcal A_\ell[T]$, so $\deg_TH\le dR$.
- $H(0)$ has integer $V$-coefficients.
- Linearity of $\mathcal S_\ell$ together with Lemma `lem:total-order` gives $\mathcal S_\ell(H(0))\equiv N\pmod{2^\ell}$.
- Hermite interpolation acts coordinatewise in $V$, and $\mathcal S_\ell$ commutes with it.
- Correct.

**Proposition `prop:count`.**
- Denominators: a substituted input has denominator dividing $d_{\rm den}$ (because $t$ is an integer). A monomial of degree $u\le k$ has denominator dividing $d_{\rm den}^u\mid\Delta$. The term $e_j(L)h(L)^j$ has denominator dividing $\Delta^{2j+1}\mid\Gamma$, and the full product has denominator dividing $\Omega$. Correct.
- Per-factor cost is $O(k|\mathcal M_i|J^2+\ell J^2)$ operations in $\mathbb Q[z]/(z^J)$, and no enumeration over the scope is performed. Correct.
- Bit sizes, with $\ell=n+1$ and $m_{\rm test}\le cn$:
  - $\log_2\Omega=k(2\ell-1)m_{\rm test}\log_2((R-1)!Q!)=O(kn^2Q\log Q)$.
  - Numerators have $O(\log M_*+n+m_{\rm test}\log B_1)$ bits, which is $O(n^3+\dots)$ with App. B's $E_\ell$ bound.
- The Hermite system has size $QJ=O(nR)$.
- All of this is polynomial; the claim is correct given D3 and D9.

**Proof of the theorem.**
- **Incidences:** $M\le n+ckn(\ln n)^c$.
- **Branching:** $|S|(b_0+1)\le M$ gives $|S|<n/\sqrt\lambda$. At $n=20$, $n'\ge(1-5^{-1/2})n>0.55n$.
- **Restricted parameters:**
  - Restriction only lowers incidences, so $b\le b_0\le(2+ck(\ln n)^c)(\sqrt\lambda+1)$ and $w\le k(\ln n)^c$.
  - Since $\ln n<\lambda\le\lambda'+1$, eventually $b,w\le(\lambda')^{c+1}$, so $\beta\le c+1$ uniformly.
  - $n'\le M'\le bn'$ holds because the neutral factors remain.
- **Tail chain:**
  - $R^2/(8Q)\ge16(\beta+3)^2\nu'$, which gives $2e^{-16(\beta+3)^2\nu'}\le2^{-(\beta+2)\nu'}\le(\lambda')^{-(\beta+2)}\le1/(br^2\lambda')=\epsilon=\tau/(rb)$.
  - $\mathcal I$ contains every integer within $R/4$ of $\mu$ once $R\ge6$.
  - The interval lies in $[0,Q]$ by $Q/4\le\mu\le Q/2$ and $R\le Q/6$.
  - Correct.
- **Cost per branch:**
  - $d_H\le kR(c+2)n\le2k(c+2)n'R$, so $q\le2k(c+2)n'R/Q$.
  - Taking $\eta=R/Q$: $\ln C_q\le q\ln(Q/R)+2n'R/Q=O_{k,c}(n'\nu'^2/\sqrt{\lambda'})$.
  - Measurements: $2\tau n'\log_2(2D+1)\le n'/(64r)+4n'/(r\lambda')$.
  - Groups: $2n'/r$.
  - Total: $O_{k,c}(n'\nu'^2/\sqrt{\lambda'})\le O_{k,c}(n\nu^2/\sqrt\lambda)$.
- **Branching cost:** the branches add $n/\sqrt\lambda=O(n\nu^2/\sqrt\lambda)$ to the exponent.
- **Fallback and space:** the fallback is uniform because $\beta$ is bounded. Space is polynomial, with an $(n+1)$-bit accumulator.
- Correct.

## Issues

1. **MINOR — notation collisions.**
   - $S$ is the length bound in Proposition `prop:count` and also the high-incidence set in the proof.
   - $b$ is a branch assignment $b\in\{0,1\}^S$ and also the incidence bound.
   - $M$ is the incidence count and also a monomial $M\in\mathcal M_i$.
   - $\mathcal B_i$ (factor) collides with $\mathcal B$ (labels, §4) and with $B$ (App. B).
   - $\mathcal A$ is the algebra in §3 and the incidence set in §4.
   - $c$ is the input constant and also the number of measurement rows.

2. **MINOR — misattribution in §5.3.** "By the same lemma, summing their values gives $\deg_TH\le d_H$": the degree bound is D2 ($\deg_TH\le dR$). Only the congruence uses Lemma `lem:total-order`.

3. **MINOR — the statement of Proposition `prop:count` is underspecified.**
   - It should state that the factor family consists of the lifts $\mathcal B_i$ of the *normalized, nonconstant* equations plus the neutral factors, with their scopes.
   - It should state that $m_{\rm test}$ in $d_H$ counts those equations.
   - "Any $\ell$ with $2^\ell>2^n$" is simply $\ell\ge n+1$.

4. **MINOR — preprocessing order.**
   - Constants can only be detected after normalization (multilinearize, combine monomials mod 2), both before and after branching.
   - The case in which every equation becomes $0=0$ should be stated: it gives $2^{n'}$, or equivalently only neutral factors remain.

5. **MINOR — fallback and uniformity.**
   - $b,w,M',\beta,R$ and some checks are branch-dependent, but the text describes one global check ("abandons the branched computation").
   - The "finitely many $n$" claim needs two facts made explicit:
     - the uniform bound $\beta\le c+1$ for large $n$;
     - the fact that the threshold in Lemma `lem:incidence-parameters` is uniform in $(b,w,M)$ for fixed $\beta$.
   - Both hold.

6. **MINOR — scope after branching.** The scope used is $I_f\setminus S$, while the re-normalized branch polynomial may read fewer variables. This is harmless but should be said.

7. **MINOR — coefficient bound for the $e_j$.** The closed form $e_j=\frac{(-1)^j}{2}\binom{2j}{j}(1-2Y)$ ($j\ge1$) gives $O(\ell)$-bit coefficients. This would simplify Lemma `lem:rational-lift-height` and shrink $B_{\rm sum}$ by a factor of order $\ell$. Optional.

8. **MINOR — unverifiable citation.** The pointer "[BT94, Section 2.3]" cannot be checked here. The proof is self-contained, so this is harmless.

9. **MINOR — purely asymptotic thresholds.**
   - $6R\le Q$ alone requires $\sqrt{\lambda'}\gtrsim768(\beta+3)\nu'$, i.e. $\lambda'\gtrsim10^{10}$ even for $\beta=1$.
   - For $q<n'$ one needs $\sqrt{\lambda'}/\nu'\gtrsim256k(c+2)(\beta+3)$.
   - The result is correct as an $O(\cdot)$ statement, but every feasible input size uses the exhaustive fallback. This deserves a remark.

## Verdict

Every lemma, identity and bound in this part checks out. The parity lift and the truncation across all equations are correct, the degree bound $d=k(m_{\rm test}+2(\ell-1))$ is right, and the exponent recomputes to $O_{k,c}(n\nu^2/\sqrt\lambda)$.

The subexponential claim rests on D3 (Proposition `prop:general-count`) and D5/D6 (Lemmas `lem:layout` and `lem:incidence-parameters`). I re-derived their interfaces as used here and found them consistent:
- the separation identity;
- the Boolean-difference identity;
- the kernel condition via $(I-M_0)=KC^{\mathcal B}$ and the vanishing of $\varphi$;
- the measurement count $rhc_{\mathcal B}\le2\tau n$.

Their full verification belongs to the review of §§3–4. No FATAL issues or GAPs were found in this part.

VERDICT: SOUND-WITH-MINOR-ISSUES
