<!-- {"stage": "sec-09-additional-consequences-of-refuting-eth", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 359, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 76652, "estimated_cost_usd": 1.5601, "message_id": "msg_011CgS4M9MPXxnJDgeMpPCH1", "finished_at": "2026-10-27T03:59:42+00:00"} -->

## What this part proves

Appendix `app:consequences` derives three corollaries from Theorem `thm:main`:

1. **Corollary `cor:consequence-circuits`.** $\mathrm E^{\mathrm{NP}}\not\subseteq\mathrm{SIZE}(O(n))$, where the circuits use bounded-fan-in AND/OR/NOT gates. The proof is a one-line appeal to [Wil13, Thm 6.1], "ETH false ⇒ $\mathrm E^{\mathrm{NP}}$ lacks linear-size circuits."
2. **Proof of Corollary `cor:quantitative-circuits`** (stated in §1). There are $L\in\mathrm E^{\mathrm{NP}}$ and $c>0$ with $C_L(n)>c\,n\sqrt{\log n}$ for infinitely many $n$. Here $C_L$ counts the noninput gates of a circuit over arbitrary fan-in-≤2 gates, and $\log$ is natural. The proof combines:
   - Williams' witness-circuit argument,
   - the Jahanjou–Miles–Viola (JMV) local reduction with $r=2$,
   - Žák's hierarchy, and
   - the **fixed-density** bound of Theorem `thm:main`.
3. **Corollary `cor:consequence-local-inversion`.** For a $d$-local map $G:\{0,1\}^n\to\{0,1\}^m$ with $d$ fixed, the following run in deterministic time $(n+m)^{O_d(1)}2^{O_d(\rho(n))}$ and polynomial space:
   - exact computation of $|G^{-1}(\vec b)|$, and
   - finding a preimage when one exists.

It also contains remarks on exact uniform sampling via [JVV86] and on Goldreich-type local functions.

## Dependencies on other parts

**Internal**

- **(I1) `thm:main`, general bound.** For fixed $k\ge2$ and $n\ge20$, it computes $\#F$ exactly, deterministically, in time $(n+m)^{O_k(1)}2^{O_k(n\log\log n/\sqrt{\log n})}$ and space $(n+m)^{O_k(1)}$. It is used:
  - with $k=3$, only as "ETH is false", in `cor:consequence-circuits`;
  - with $k=\max\{2,d\}$, $n$ declared variables and $\le 2^dm+n$ clauses (including self-reduction unit clauses), in `cor:consequence-local-inversion`.
- **(I2) `thm:main`, fixed-density bound.** With $k=3$ and $D=5$: deterministic time $(n+m)^{O(1)}2^{O(n/\sqrt{\log n})}$ and space $(n+m)^{O(1)}$ on 3-CNFs with $m\le5n$. This bound is load-bearing for the $\sqrt{\log n}$ factor in `cor:quantitative-circuits`. It rests on `subsec:sharp-fixed-density` and Theorem `thm:tensor-contraction` (`app:tensor`).
  - If only Proposition `prop:interpolation-bound` (exponent $\rho(n)$) survives, the same argument gives only $C_W(N)>cN\sqrt{\log N}/(\log\log N)^2$ infinitely often.
  - In that case use $s_n=\eta n\sqrt{\log n}/(\log\log n)^2$, so that $\rho(3s_n)=\Theta(\eta n)$.
- **(I3) Definition of $\rho(n)$ and Proposition `prop:interpolation-bound`.** This proposition is sufficient by itself for `cor:consequence-circuits` (via the argument in D below with $s_n=cn$) and for `cor:consequence-local-inversion`.
- **(I4) Input conventions of §1.**
  - Clauses may have width $<k$.
  - Declared but unused variables are allowed.
  - Empty clauses and empty formulas are handled.

**External**

- **(E1) [Wil13, Thm 6.1].** ETH false ⇒ $\mathrm E^{\mathrm{NP}}\not\subseteq \mathrm{SIZE}(O(n))$.
- **(E2) [Žák83] in unary form ([Wil13, Thm 2.1]).** There is a unary $H\in\mathrm{NTIME}(2^n)\setminus\mathrm{NTIME}(2^{n/2})$ on multitape TMs. Žák's condition holds: $2^{(n+1)/2}=o(2^n)$.
- **(E3) [JMV13, Thm 1].** For $T\ge n$ and $r\le n$, a decoder $D:\{0,1\}^\ell\to\{0,1\}^{3v+3}$ is constructible in $\mathrm{poly}(n,\log T)$ time, with:
  - $\ell=\max(\log T,n/r)+O(\log n)+O(\log\log T)$;
  - $v=O(\ell)$;
  - every output bit a decision tree of depth $O(\log r)$;
  - $\varphi_x$ satisfiable iff $\exists y\,M(x,y)=1$.
- **(E4) [JVV86].** Exact counts give exact uniform sampling in expected polynomial overhead.
- **(E5) Standard simulation.** A RAM algorithm using $S$ bits of space is simulated on a multitape TM with $\mathrm{poly}(S)$ overhead per step.

**Provided to other parts**

- The proofs of `cor:quantitative-circuits` and `cor:consequence-local-inversion` promised in §1 ("Appendix `subsec:circuit-lower-bounds` proves the corollary"; "Appendix `subsec:local-inversion` gives algorithms…").
- Corollary `cor:consequence-circuits`.
- Nothing in the proof of `thm:main` or in any other appendix uses this part.

## Detailed verification

**A. Preamble.** The claims are consistent with what follows. Both circuit arguments use only the positivity of the count.

**B. `cor:consequence-circuits`.**
- "ETH false" requires, for each $\varepsilon>0$, a 3-SAT algorithm running in $\mathrm{poly}(n+m)2^{\varepsilon n}$; deterministic is more than needed.
- (I1) gives $2^{O(n\log\log n/\sqrt{\log n})}\le2^{\varepsilon n}$ for $n\ge n_0(\varepsilon)$. So the hypothesis is met if (E1) is stated in terms of 3-SAT.
- If (E1) is phrased for Circuit-SAT on $O(n)$-size circuits, the following paragraph supplies the Tseitin step.
- The exact hypothesis of (E1) cannot be checked here (Issue 1). The corollary also follows from the argument in D, run with $s_n=cn$:
  - $W$ does not depend on $c$;
  - the test circuit then has $O(n)$ gates, so any $2^{o(N)}$ algorithm for 3-CNFs with $N$ variables and $O(N)$ clauses suffices;
  - Proposition `prop:interpolation-bound` is enough.
- So this corollary is robust.

**C. Tseitin paragraph.**
- A circuit with $n$ inputs and $s$ fan-in-2 gates gives $n+s$ variables.
- Each gate needs at most 4 clauses of width at most 3, plus one unit clause for the output, so at most $4s+1$ clauses.
- For $s=O(n)$ the running time is $2^{O(N/\sqrt{\log N})}=2^{o(n)}$. This is correct; for the fan-in caveat see Issue 4.

**D. Proof of `cor:quantitative-circuits`.**

1. *Hierarchy.* Žák's condition holds, as noted in (E2). The lazy-diagonalization proof yields a unary language.
2. *Local reduction, index length.* Take $T=2^n n^{O(1)}$, so $\log T=n+O(\log n)$. With $r=2$, $\ell=\max(n+O(\log n),n/2)+O(\log n)=n+O(\log n)=q$. ✓
3. *Local reduction, decoder size.*
   - The decoder has $3v+3=O(n)$ output bits, each a decision tree of depth $O(1)$.
   - Each output therefore depends on at most $w=2^{O(1)}$ index bits.
   - It is computable with $O(2^w)$ fan-in-2 gates, so the decoder has $O(n)$ gates. ✓
4. *Support recovery.* Let $S_f$ be the set of relevant variables of an output bit $f$, so $|S_f|\le w$.
   - Then $j\in S_f$ iff some $z$ has $f(z)\ne f(z\oplus e_j)$.
   - Zeroing $z$ outside $S_f$ preserves both values, so a witness pair of weight $\le w$ exists.
   - Conversely, any such pair, of any weight, certifies relevance.
   - Hence evaluation on the $O(q^w)$ strings of weight $\le w$ identifies $S_f$ exactly, and also yields the truth table on $S_f$. This takes polynomial time. ✓
5. *$W\in\mathrm E^{\mathrm{NP}}$.* Let $N=dn$; $n$ is determined from $|i|$.
   - Writing out $\varphi_n$ costs $2^{q}\mathrm{poly}(n)$.
   - At most $2^{dn}$ prefix-extension queries are made, each of length $2^{O(n)}$.
   - The total time is $2^{O(N)}$.
   - Lex-first gives 0 on unused labels, consistent with $W$. ✓
6. *Solver.*
   - From (I2) with $k=3$, $D=5$, the solver runs in time $(6V)^{O(1)}2^{A'V/\sqrt{\ln V}}=V^b2^{AV/a(V)}$ with $A=A'/\sqrt{\ln2}$.
   - The multitape overhead is $\mathrm{poly}(V)$ by (E5).
   - $s_n=\lfloor\eta n\lfloor a(n)\rfloor\rfloor$, using $\lfloor\sqrt{x}\rfloor=\lfloor\sqrt{\lfloor x\rfloor}\rfloor$; it is computable in $\mathrm{poly}(\log n)$. ✓
7. *Simulation.*
   - If $1^n\in H$, the circuit for $W_{dn}$, which has at most $s_n$ gates by assumption, makes the test circuit unsatisfiable, so the machine accepts.
   - If $1^n\notin H$, every assignment violates some clause of $\varphi_n$, so every guess is rejected. ✓
8. *Sizes.*
   - Gates: at most $3s_n+O(n)$, covering the decoder, the three copies, the violation test and the padding constants.
   - Variables: $q+\#\text{gates}\le U_n:=3s_n+Bn$.
   - Clauses: at most $4\#\text{gates}+1\le4U_n+1\le5U_n$. ✓
9. *Asymptotics.*
   - $s_n=(\eta+o(1))n\,a(n)$ and $U_n=(3\eta+o(1))n\,a(n)$.
   - $\log_2U_n=\log_2n+O(\log\log n)$, so $a(U_n)=(1+o(1))a(n)$.
   - The exponent is $AU_n/a(U_n)=(3A\eta+o(1))n<(1/4+o(1))n$.
   - Total nondeterministic time is $2^{(1/4+o(1))n}\le2^{n/2}$ for large $n$, a contradiction. Hence $C_W(dn)>s_n$ for infinitely many $n$. ✓
10. *Constant.* With $N=dn$, $s_n\sim\frac{\eta}{d\sqrt{\ln2}}N\sqrt{\ln N}$. So any $c<\eta/(d\sqrt{\log2})$, natural log, works. $W$ is fixed before $\eta$ is chosen, so a single language serves. ✓

**E. `cor:consequence-local-inversion`.**
- *Encoding.* The clause $\bigvee_{j}\ell_{j,\alpha_j}$ is false iff $x|_{S_i}=\alpha$. ✓
  - Width is at most $d$.
  - There are $\sum_i|\{\alpha:g_i(\alpha)\ne b_i\}|\le2^dm$ clauses.
  - Satisfying assignments are exactly $G^{-1}(\vec b)$.
  - If $S_i=\emptyset$ and $g_i\ne b_i$, the answer is 0, or equivalently the formula contains an empty clause.
- *Time.* $(n+2^dm)^{O_k(1)}2^{O_k(n\log\log n/\sqrt{\log n})}\le(n+m)^{O_d(1)}2^{O_d(\rho(n))}$. ✓
- *Finding a preimage.* Self-reduction makes $n$ queries, each adding unit clauses. The formula keeps $n$ declared variables and at most $2^dm+n$ clauses, so time and space are unchanged up to polynomial factors. ✓

**F. Remarks.**
- With exact counts, a uniform preimage is obtained from one uniform integer in $[1,N]$, which needs expected $O(1)$ rejection trials. ✓
- With $m=\mathrm{poly}(n)$ the time is $2^{o(n)}$. This rules out only $2^{\Omega(n)}$ hardness, as stated. ✓

## Issues

1. **MINOR — `cor:consequence-circuits` is proved by citation only.**
   - The exact form of (E1) cannot be verified from the manuscript: which variant of "ETH false" it assumes, and whether linear-size decoders are needed.
   - A one-line remark would make the corollary independent of the citation and of `app:quantitative`: the proof of `cor:quantitative-circuits` with $s_n=cn$ yields it from Proposition `prop:interpolation-bound` alone.

2. **MINOR — The JMV dependency is under-specified in D.**
   - The sentence "a time allowance $T=2^nn^{O(1)}$ includes the polylogarithmic overhead…" is vague.
   - The proof needs four precise facts, which should be stated with the exact theorem form:
     - index length $\max(\log T,n/r)+O(\log n)+O(\log\log T)$;
     - decision-tree depth $O(\log r)$;
     - label length $v=O(\ell)$, needed for "pad to $dn$ bits for fixed $d$";
     - the machine model.

3. **MINOR — Citation numbering and form need checking.**
   - [Wil13, "Theorem 2.1/6.1 in the full version"] should be checked against the full version.
   - Žák's original statement is not phrased for unary languages; the unary form comes from the lazy-diagonalization proof.

4. **MINOR — Fan-in caveat in the Tseitin paragraph after `cor:consequence-circuits`.**
   - "3-CNF" requires fan-in 2.
   - $\mathrm{SIZE}(O(n))$ is defined with *bounded* fan-in, so a constant-factor reduction of fan-in to 2 should be mentioned.

5. **MINOR — Citation choice in `cor:consequence-local-inversion`.**
   - The corollary invokes `thm:main` but states the weaker $\rho(n)$ bound.
   - It should either cite `prop:interpolation-bound`, which is the minimal dependency and is independent of `app:quantitative`, or state the stronger bound.

6. **MINOR — Notation clashes with the main text.** The following symbols are reused with different meanings:
   - $r$ (2 here, vs number of groups);
   - $q$ (index bits vs Taylor order);
   - $T$, $H$, $W$, $V$, $B$, $D$;
   - $d$ (padding factor here, locality in `subsec:local-inversion`);
   - $G$ (map vs formula/graph).

7. **MINOR — Wording.**
   - "guess a circuit on $dn$ index bits" should say *label* bits; the clause-index bits are the $q$ inputs.
   - "bit $i$" means the value of the variable labelled $i$.

## Verdict

Every step of this part checks out: all bounds were recomputed (D1–D10, E). The circuit lower bounds and the local-inversion algorithm follow correctly from the stated dependencies. The quantitative constant $c<\eta/(d\sqrt{\ln2})$ and the exponent $3A\eta<1/4$ are right.

The soundness is conditional on `thm:main`:
- the $c\,n\sqrt{\log n}$ bound depends specifically on the fixed-density bound (I2) from `app:quantitative`/`thm:tensor-contraction`;
- the other two corollaries need only Proposition `prop:interpolation-bound`.

Only presentation and citation issues remain.

VERDICT: SOUND-WITH-MINOR-ISSUES
