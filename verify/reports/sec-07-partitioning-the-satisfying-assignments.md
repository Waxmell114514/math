<!-- {"stage": "sec-07-partitioning-the-satisfying-assignments", "requested_model": "claude-opus-5-5", "served_by": ["claude-opus-5-5"], "fallback_used": false, "effort": "max", "stop_reason": "end_turn", "input_tokens": 356, "cache_read_input_tokens": 128260, "cache_creation_input_tokens": 0, "output_tokens": 65277, "estimated_cost_usd": 1.3326, "message_id": "msg_011CgS3z3DiDApth3PHRrdBM", "finished_at": "2026-10-27T03:52:53+00:00"} -->

## What this part proves

Appendix A proves Lemma `lem:sparsify` (stated in §5.4, `subsec:general-reduction`). With explicit constants, it shows the following.

- **Normalization.** The input is normalized into an antichain of nontautological clauses. Unit clauses are not propagated, and all $n$ declared variables are kept.
- **Branching.** A deterministic binary branching rule is applied with threshold base $M$ and thresholds $\theta_j=M^j$:
  - choose the smallest width $c$ with a violated threshold, then the largest heart $H$;
  - $F_A=G\wedge H$;
  - $F_B=G\wedge\bigwedge_a P_a\wedge\bigwedge_{\ell\in H}\{\neg\ell\}$.
- **Partition.** At every node the two children partition the parent's satisfying assignments.
- **Depth and $B$-choices.** Along any path prefix, $T_j\le 4(3M)^{j-1}n$. Hence the depth is at most $Cn$, with $C=4\sum_{j=0}^{k-2}(3M)^j$. The number of $B$-choices on a path is at most $\Gamma n/M$, with $\Gamma=2(3^{k-1}-1)$.
- **Choice of $M$.** $M$ is the first power of two $\ge\Gamma$ with $\Gamma\lceil\log_2(4CM)\rceil\le\sigma M$. Then $M=O_k(\sigma^{-1}\log(2/\sigma))$.
- **Tree size.** The tree has at most $(Cn+1)^2 2^{\sigma n}=\poly_k(n,\sigma^{-1})2^{\sigma n}$ nodes.
- **Leaf sparsity.** Leaves satisfy the occurrence bound $B=2\sum_{j=0}^{k-1}M^j\le 4M^{k-1}=O_k([\sigma^{-1}\log(2/\sigma)]^{k-1})$.
- **Costs.**
  - Per-node cost is $\poly_k(n,\log M)$.
  - Parameter construction costs $\poly_k(L_\sigma)$.
  - Input normalization costs $\poly_k(n,m)$.

## Dependencies on other parts

**Internal dependencies.** No internal lemma is invoked. The part uses only:

- the statement of Lemma `lem:sparsify` (§5.4), which it proves;
- conventions from §1.2: $\poly_k$, natural $\log$, signed binary integers;
- the input format from §1, where repeated literals model short clauses.

**External citations.** [CIP, §6] and [DHMTW, App. A] are cited only for provenance; the argument is self-contained. The main text's citation of [Calabro thesis, Lemma 5.14, eq. (5.4)] for "quantitative bounds" is likewise not used here. The only external fact needed is the elementary bound $\binom{N}{a}\le(eN/a)^a$.

**What this part provides** (each consumer should cross-check these):

1. **§2.10 (overview).**
   - Uses: $\sigma\asymp(\log n)^{-1/(2k)}$, rational.
   - Requires: leaf count $\poly_k(n,\sigma^{-1})2^{\sigma n}$; $B=O_k((\sigma^{-1}\log(2/\sigma))^{k-1})$; leaves have at most $Bn$ clauses.
   - Provided.
2. **Prop. `prop:interpolation-bound`.**
   - Uses: $\sigma=1/s$ with $s=\lfloor\sqrt{\lambda_n}/\nu_n^2\rfloor\ge 2$.
   - Requires:
     - node count $2^{n/s}\poly_k(n,s)$;
     - depth $\poly_k(n,s)$ for depth-first-search (DFS) space;
     - $B=O_k((s\log s)^{k-1})$ (valid since $\log(2s)\le 2\log s$);
     - leaves on the same $n$ variables, with at most $Bn$ nonempty clauses;
     - disjointness, so leaf counts add.
   - Provided.
3. **Appendix "Arbitrary clause density."**
   - Uses: $\sigma=1/\lceil\sqrt\lambda\rceil$.
   - Requires: node count $n^{O_k(1)}2^{n/\sqrt\lambda}$, polynomial depth, $B=\lambda^{O_k(1)}$.
   - Provided.
4. **§6 and Lemma `lem:sparse-checks`.** These need a positive integer $B$ with $m_G\le Bn$ for each leaf $G$.
   - Provided, because every leaf clause is nonempty: no branch ever inserts an empty clause.

## Detailed verification

**Normalization and branching rule.**

- Deleting tautologies, duplicate clauses and subsumed clauses preserves the solution set.
- A violation needs $\emptyset\ne H\subsetneq C$ with $|C|=c$. So $c\ge2$ and $j=c-|H|\in[1,c-1]\subseteq[1,k-1]$, and only $\theta_1,\dots,\theta_{k-1}$ are used.
- The search starts at $M\ge\Gamma=2(3^{k-1}-1)\ge4$, so the requirement $M\ge2$ holds.

**Partition.**

- *Child $A$.* If some literal of $H$ is true, every selected clause $H\cup P_a$ is satisfied. So $F$ restricted to this case equals $G\wedge H$.
- *Child $B$.* If all literals of $H$ are false, the selected clauses reduce to $P_a$, and the units $\{\neg\ell\}$ encode the case.
- The two cases are complementary, so the children partition the parent's solutions. Normalization does not change solution sets.
- Induction over the tree gives the lemma's exactness and disjointness claims, which justify adding leaf counts.

**Lemma `lem:spar-branch`.**

- *Widths.* $|H|\le c-1$, $|P_a|=j\le c-1$, and units have width $1<2\le c$. ✓
- *Petals are distinct and new.* Distinct selected clauses give distinct $P_a=(H\cup P_a)\setminus H$, so $z=\deg_c(H)\ge\theta_j$.
  - No old clause is contained in $H$ or $P_a$. Since $H\ne\emptyset$ and $P_a\ne\emptyset$ (as $j\ge1$), such a clause would be strictly inside $H\cup P_a$, contradicting the antichain. ✓
- *Survival.* $P_a$ contains no variable of $H$, because $P_a\cap H=\emptyset$ and the parent clause is nontautological.
  - So no new unit $\{\neg\ell\}$ is contained in any $P_a$, and no $P_a$ equals a unit.
  - Equal-width distinct $P_a$ are incomparable.
  - An old clause contained in $\{\neg\ell\}$ must equal $\{\neg\ell\}$; that case is "already present" and not counted.
  - An old unit $\{\ell\}$ with $\ell\in H$ cannot exist, since it would be strictly inside $H\cup P_a$. ✓
- *Removed clauses.* Selected clauses contain $H$ (child $A$) or $P_a$ (child $B$) strictly.
  - Any other removal is caused by a clause not present before, since a pre-existing unit cannot subsume anything in an antichain.
  - Strictness holds because new clauses are not present in the parent. ✓

**Lemma `lem:spar-marked-degree`** ($1\le i<j<k$, $|S|=i$).

- A branch inserting width-$j$ clauses has $c>j$. By the smallest-width priority, $\deg_j(S)<\theta_{j-i}$ in the parent.
- *Child $A$* adds one clause, so the count is at most $\theta_{j-i}<2\theta_{j-i}$.
- *Child $B$.* Units have width $1<j$, so they are irrelevant here.
  - If $S\subseteq P_a$ for some $a$, then $S\cap H=\emptyset$, and $\#\{a:S\subseteq P_a\}=\deg_c(H\cup S)$.
  - $H\cup S$ is a nonempty proper subset of a selected clause, because $|H\cup S|=|H|+i<c$, and it is larger than $H$.
  - By the largest-$|H|$ priority, $\deg_c(H\cup S)<\theta_{c-|H|-i}=\theta_{j-i}$.
  - The total is at most $2\theta_{j-i}-2$.
- Branches that insert no width-$j$ clause, and deletions, cannot raise the marked count. The induction is valid. ✓

**Lemma `lem:spar-insertion-bound`.**

- *$T_1\le 2n$.* No branch inserts the empty clause, so units are never deleted. A unit is inserted only if absent, so each of the $2n$ literal units is inserted at most once. ✓
- *$L_j$.* Summing the previous lemma over the $2n$ literals gives $jL_j<4n\theta_{j-1}$, hence $L_j\le4n\theta_{j-1}$. ✓
- *$D_j$.* Each deletion of a marked width-$j$ clause occurs at a branch where it contains a strict subset $N$ inserted at that same branch.
  - By the previous lemma at the parent node, $N$ (of width $i<j<k$) lies in fewer than $2\theta_{j-i}$ marked width-$j$ clauses.
  - So $D_j\le 2\sum_{i<j}\theta_{j-i}T_i$. ✓
- *Recurrence.* $T_j/(nM^{j-1})\le 4+\sum_{i=1}^{j-1}8\cdot3^{i-1}=4+4(3^{j-1}-1)=4\cdot3^{j-1}$. ✓

**Tree size.**

- *Depth.* Every branch inserts at least one clause, so depth $\le\sum_{j=1}^{k-1}T_j\le4n\sum_{j=0}^{k-2}(3M)^j=Cn$. ✓
- *$B$-choices.* A $B$-choice with petal width $j$ uses at least $M^j$ of the $T_j$ insertions. Summing $4\cdot3^{j-1}n/M$ over $j$ gives $\Gamma n/M$, and $4\sum_{j=0}^{k-2}3^j=2(3^{k-1}-1)$. ✓
- *Node encoding.* The rule is deterministic, so a node is determined by its depth and its set of $B$-positions. This gives at most $(Cn+1)\sum_{a\le\lfloor\Gamma n/M\rfloor}\binom{Cn}{a}$ nodes.
- *Binomial estimate.* $a\mapsto(4Cn/a)^a$ increases on $(0,4Cn/e]$. Also $\Gamma n/M\le n\le Cn/4$, using $M\ge\Gamma$ and $C\ge4$.
  - Each summand is at most $(4CM/\Gamma)^{\Gamma n/M}\le(4CM)^{\Gamma n/M}$.
  - There are at most $Cn+1$ summands. ✓
- *Choice of $M$.* For $M\ge2$, $C\le 4.8(3M)^{k-2}$, so $h\le(k-1)\log_2M+O_k(1)$.
  - $\sigma M-\Gamma((k-1)\log_2M+O_k(1))$ is eventually increasing and becomes nonnegative at some $M^*=O_k(\sigma^{-1}\log(2/\sigma))$.
  - The first power of two that succeeds is at most $2\max(M^*,\Gamma)$, so $M=O_k(\sigma^{-1}\log(2/\sigma))$.
  - The exponent satisfies $(\Gamma n/M)\log_2(4CM)\le\Gamma nh/M\le\sigma n$. ✓
- *Final bound.* The tree has at most $(Cn+1)^22^{\sigma n}$ nodes, and $C=O_k(M^{k-2})=\poly_k(\sigma^{-1})$. ✓

**Leaf occurrence bound.**

- At a leaf, every literal lies in fewer than $M^{c-1}$ width-$c$ clauses for each $c\ge2$, and in at most one unit.
- Summing over $c$ and the two literals of a variable gives at most $2\sum_{j=0}^{k-1}M^j$ occurrences.
- For $M\ge2$, $(M^k-1)/(M-1)<2M^{k-1}$, so $B\le4M^{k-1}$. ✓
- Every clause is nonempty, so a leaf has at most $Bn$ clauses. ✓

**Costs.**

- A normalized node has $O_k(n^k)$ clauses. The counters indexed by $(c,H)$, the threshold comparisons on $O_k(\log M)$ bits, and subsumption removal cost $\poly_k(n,\log M)$, independent of $m$ after the one-time $\poly_k(n,m)$ normalization. ✓
- *Parameter search.* $\log_2M\le O_k(1)+2L_\sigma$, so $O_k(L_\sigma)$ candidates are tried. Each test compares $\Gamma hq\le pM$, for $\sigma=p/q$, using $O_k(L_\sigma)$-bit integers. ✓

## Issues

1. **MINOR (notation overload).** Symbols in Appendix A clash with other sections:
   - $M$ (threshold base) vs. $M$ (incidence count in §§2–4, wire count in the tensor appendix);
   - $\Gamma$ vs. $\Gamma=\Delta^{2\ell-1}$ (§4.4, App. B);
   - $h$, $H$, $G$, $C$, $T_j$, $D_j$, $L_j$ vs. $h(Y)$, $H(T)$, leaf formula $G$, etc.

   This does not affect correctness but invites misreading when cross-checking Prop. `prop:interpolation-bound`, which uses $G$ and $B$ in the leaf sense.
2. **MINOR (implicit facts).**
   - "Units are never deleted" relies on the unstated fact that no branch inserts the empty clause.
   - The accounting relies on deletions being attributed to clauses inserted at the same step.

   Both follow from Lemma `lem:spar-branch` and should be stated. The sentence "Clauses present in the input are excluded from this count" should read "$T_j$ counts insertion events."
3. **MINOR (wording in the tree bound).**
   - "For a positive integer $a$" is then applied at the possibly non-integer point $a=\Gamma n/M$. This is harmless, since monotonicity holds for real $a\le 4Cn/e$.
   - Only the second inequality in that display needs $M\ge\Gamma$.
4. **MINOR (statement wording).** Lemma `lem:sparsify` says the algorithm "constructs a tree." What is proved and used downstream is a depth-first traversal with depth $\le Cn$ and $\poly_k(n,\log M)$ cost per node. Explicitly building the tree would take exponential space. Rephrase.
5. **MINOR (provenance).**
   - The main text attributes quantitative bounds to [CIP §6] and [Calabro, Lemma 5.14, eq. (5.4)], but the appendix's self-contained proof does not use them.
   - The claim that the selection rule "follows CIP §6" is not load-bearing.

## Verdict

Appendix A is a correct, self-contained proof of the disjoint sparsification lemma with the stated parameter dependence. All its outputs match what §2.10, Prop. `prop:interpolation-bound` and the arbitrary-density proof consume: partition, node count, depth, the occurrence bound $B$, the $Bn$ clause bound, and the cost bounds. Only presentation issues were found.

VERDICT: SOUND-WITH-MINOR-ISSUES
