# Dimension 13 at the five-percent target

All determinants here are Gram determinants. Scale each lattice to squared minimum four. In rank 13 the density is $V_{13}/\sqrt D$, where $V_{13}=128\pi^6/135135$. The working contradiction hypothesis is $D<242111/500$. Ruling it out would close slightly more than 5% of the gap between the Mordell upper bound and the density of $K_{13}$.

## The general upper bound

Let the original squared minimum be four. Between the lattice and its dual rescaled to squared minimum four, choose the representative with the smaller Gram determinant $D$. If its dual has squared minimum $v$, the other representative has determinant $(4/v)^{13}/D$. Thus $v\le4D^{-2/13}$. The section perpendicular to a shortest dual vector has determinant $vD$ and squared minimum at least four. The external rank-12 theorem gives $729\le vD\le4D^{11/13}$. The original determinant is at least $D$, so its density is at most $V_{13}(729/4)^{-13/22}<0.042023513562578$. This argument establishes the general bound without the later marking exclusions. [Numerical enclosure with directed rounding](../replay13.py)

## What comes from the other paper

Géraud-Stewart and Naccache give determinant floors 768, 972 and 729 in ranks 10, 11 and 12, under their stated rank-nine classification and computational inputs. Their Proposition 7 gives a marking of a section metric $Q$ by a minimum-four perfect form $P$ with $\operatorname{tr}(P Q^{-1})\le9$. In fact $Q^{-1}=\sum w_x xx^t$ over the minimum pairs of $P$, with $w_x\ge0$ and $\sum w_x\le9/4$. Their rank-eleven database proves a rank-ten floor $d_0=4\,972^{9/11}$ at every listed mark except ten named exceptions. We use their proof of this floor for nontrace, nonexceptional marks. We recompute the trace-format bounds directly. The full underlying 2,237,251,040-row raw classification is an external input. [Main paper](https://eprint.iacr.org/2026/2825) · [Rank-eleven paper](https://eprint.iacr.org/2026/2826) · [Certificate database](https://doi.org/10.5281/zenodo.23979316)

## The descent and the orientation issue

In rank $n$, choose the smaller determinant between the minimum-four lattice and its minimum-four normalized dual. For this representative of determinant $D$, its dual minimum satisfies $v\le 4D^{-2/n}$. Cut perpendicular to a shortest dual vector. Before rescaling, the section has determinant $vD$ and squared minimum at least four. Rescaling and a possible dual switch can only lower the determinant. Repeating gives the rank-$k$ ceiling $4^{k(n-k)/(n-1)}D^{k(k-1)/(n(n-1))}$. The rational ceilings used here are 993.31 at rank eleven, 1133 at rank ten and 1110.28 at rank nine. The latter lies inside the coverage of the public rank-eleven selection. The per-row determinant filter uses the least diagonal entry as an upper bound on the raw minimum, so retaining extra rows is safe.

Let $E$ be the balanced rank-eleven determinant, $v$ its dual minimum, and $4s$ the minimum of the resulting raw rank-ten section, so $s\ge1$. The normalized rank-ten section $F$ has determinant $d_o=vE/s^{10}\le1133$. Let $d\le d_o$ denote the balanced rank-ten determinant, $u$ its dual minimum, and $Q$ the Gram of its actual rank-nine section before any further rescaling. Write $e=\det Q=ud,\ T=Q^{-1},\ t=\min T$. The same ceiling $e<1110.28$ holds before this last rescaling. The projection of a lattice along a shortest vector has minimum at least three quarters of the original squared minimum, by lifting with a coefficient of absolute value at most $1/2$. Thus $t\ge3u/4$.

* In the direct orientation the first three squared Gram–Schmidt lengths of an HKZ basis of the rank-eleven dual are $v,u/s,t/s$. The three-dimensional KZ constant is $3/2$, so $t\ge 2sv/3\ge2d/(3E)$. The two-dimensional inequality gives $u\ge3d/(4E)$. The first three HKZ vectors span a rank-three lattice to which the KZ bound applies. [KZ constant, equation (1.3)](https://pure.tue.nl/ws/files/2066021/Metis197411.pdf)
* In the reverse orientation the balanced rank-ten lattice is the scaled dual of $F$. Since $\min F=4$, its own dual minimum is also $u=\min F^*$. Hence $u^{10}d_o d=4^{10}$ and $u>9799/10000$. The two orientations can tie; either proof applies in that event.

## Transferring an entire published trace witness

Let $P'\preceq P$ be the marking matrix divided by the published safe scale, in the certified unimodular basis. The trace witness has $P'=R+\sum_i w_i z_i z_i^t$, with $R$ positive definite, $z_i$ nonzero integral and $W=\sum_iw_i>0$. Then
$$
 9\ge9(\det R/e)^{1/9}+Wt,\qquad
 e/t\ge J=(10/9)^{10}W\det R.
$$
The second inequality follows by maximizing $t(1-Wt/9)^9$. Therefore $d\ge3J/4$. The independent scan checks $3J/4\ge d_0$ for every retained trace record, including positive definiteness, the normalization and the unimodular transform.

In the direct orientation, $ud=e\ge Jt\ge 2Jd/(3E)$. This implies $u\ge8d_0/(9E)>4d_0^{-1/5}$, whereas balancing gives $u\le4d^{-1/5}\le4d_0^{-1/5}$. The strict comparison is $E<(2/9)d_0^{6/5}$, verified in integers for $E\le993.31$. This excludes **every trace-format mark in the direct orientation** with the same argument.

In the reverse orientation insert $t\ge3(9799/10000)/4$ directly into the first trace inequality. A nonpositive trace remainder is impossible. Otherwise $e\ge\det R/(1-(9799/10000)W/12)^9$. At 689,660 additional marks this contradicts $e<1110.28$, beyond the 1,042,245 marks already excluded by $3J/4\ge1133$ alone. The exact raw-row auditor constructs the positive characteristic coefficients of each symmetric residual and checks the determinant inequalities in integers.

## Additional vectors and the full normal cone

For an integral rank-nine reciprocal direction $z$ let $\chi(z)$ be the circle coordinate of a lift back to the rank-ten dual. This is one homomorphism for the whole lattice. Then $T[z]\ge u(1-\|\chi(z)\|^2)$. For three signed directions with $z_1+z_2+z_3=0$, the sum of their three squared circle distances is at most $1/2$. To check this, split the square of the first two coordinates at the lines where the nearest integer for their sum changes. On each polygon the sum is convex, and its values at all vertices are at most $1/2$. It follows that the three reciprocal lengths sum to at least $5u/2$. This bound uses their joint geometry.

For each single-vector or triple matrix $V_j$ with certified $\operatorname{tr}(V_jT)\ge h_j$, choose nonnegative rational prices $\lambda_j$. The matrix
$$
 K=(1+\textstyle\sum_j\lambda_jh_j/9)P'-\sum_j\lambda_j V_j
$$
satisfies $\operatorname{tr}(KT)\le9$. When $K\succ0$, AM–GM implies $e\ge\det K$. More generally any rational $K\succ0$ suffices if every true minimum vector $x$ of the normalized mark satisfies
$$
 x^t(K+\textstyle\sum_j\lambda_jV_j)x\le4+(4/9)\sum_j\lambda_jh_j .
$$
Multiply by the same nonnegative marking weights and sum. The independent checker enumerates all minimum vectors by rational square completion, checks the contact inequalities and subtracts an exactly computed multiple of $P$ to pay any rounding error. An improved lower bound on $e$ feeds back through $e=ud\le4d^{4/5}$, with the same lattice throughout.

## Coverage before the cofactor and interval certificates

The later certificates reduce the open list to 32 markings. [Combined results](../README.md)

The disjoint ledger and the list of keys still open are in [the audit at this stage](dimension13-final-audit.json) and [the residual list](dimension13-open-keys.txt). The audit rules out 1,739,119 of 1,746,860 potential marks at the target. It leaves 7,214 reverse-orientation trace marks, 385 domain marks, 62 glue marks, 70 tree marks and ten exceptional marks. A surviving mark represents possible section metrics and extensions. It furnishes no packing witness. The general dimension-13 upper bound at the displayed precision remains 0.042023513562578.
