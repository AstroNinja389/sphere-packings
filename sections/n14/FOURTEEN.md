# Dimension 14. A global difference count over the parity classes

At squared minimum four write $D=\det\operatorname{Gram}(L)$. The density is $\pi^7/(5040\sqrt D)$. The case $D>314$ gives density below 0.033818453867395. For $D\le314$, normalize to squared minimum one and use the existing dimension-14 Fourier polynomial and its parity kernel. All Fourier and spatial signs and all 577 anchor cases were replayed in both directions. The geometric input below uses the published rank-twelve floor 729, including the census assumptions of that theorem. [Géraud-Stewart and Naccache](https://eprint.iacr.org/2026/2825)

## Where the lower-dimensional paper enters

At squared minimum four, every rank-13 primitive section has determinant at least $A=(729/4)^{13/11}$ by Mordell. The previous rank-14 proof used this to bound the norm of every nonzero reciprocal vector and, through the common circle coordinate of a lift, the number of nearly orthogonal vectors in a single parity class. Here the last (largest) length in a 13-point prefix controls the positive mass that the prefix must carry. The sorted diagonal perturbations, with or without one negative entry, lie in a simplex cut by a linear mass budget. Clipping the simplex at the allowed largest entry preserves a finite list of vertices. A Schur complement bounds individual and pair inverse quadratic forms throughout the cell; integer character group and circle capacities then rule out the cell. For example, if all thirteen squared lengths are at most $9/4$, the excess $\sum_i\max(0,\lVert x_i\rVert^2-2)$ exceeds $0.958$ at $D\le314$. The previous thirteen-point rule gave $0.7$. The exact calculation checks ten length cutoffs and re-enumerates the vertices independently. The twelve- and fifteen-point inputs of the preceding proof were retained. [Earlier geometric argument](geometry/PROOF.md) · [Length-dependent certificate](rank14-adaptive-314.json)

## Why more than one parity class is needed

The largest class budget for the previous Fourier polynomial occurs at an anchor of squared length near $5/4$. Such an anchor cannot even occur with a second vector in the same class through our cutoff $21/8$, since the two squared lengths would sum to less than four. A second large class budget occurs near $1.486$. Strengthening the 13-point rule alone leaves the worst single-class budget unchanged in the matched exact replay.

Let $N=2^{14}-1$. Each of these $N$ parity classes contains at most one opposite pair shorter than squared length two. Give a class the bin of that pair, or a final unanchored bin. Write $n_j$ for the numbers of classes in these bins. Existing exact prefix spherical-code bounds control $\sum_{j\le k}n_j$. For example, at most 8,585 anchor pairs have squared length at most $5/4$. We re-expanded every even polynomial into the dimension-14 normalized Gegenbauer basis over the rationals. Its nonnegative harmonic coefficients and its nonpositive off-diagonal values give the stated count by the addition formula. For unequal squared lengths $a,b\in[1,T]$, the minimum-length constraint implies $|\cos\theta|\le(a+b-1)/(2\sqrt{ab})\le1-1/(2T)$ when $T<2$.

The next constraint uses differences between *distinct* parity classes. Fix squared-length interval $(A,B]\subset[1,2)$. Its $m$ opposite pairs determine $m$ unit lines. Let $F(t)=\sum b_k G_{2k}^{(14)}(t)$, where $b_k\ge0$, $G_j^{(14)}(1)=1$. The addition formula gives $\sum_{i,j}F(\langle x_i,x_j\rangle)\ge b_0m^2$ for unit representatives. For distinct lines of actual squared lengths $a,b$, choose the sign of the difference $z$ that minimizes $c=\lVert z\rVert^2$. For $t=|\cos\theta|$,
$$
 t=(a+b-c)/(2\sqrt{ab}).
$$
When $c\ge2$, $0\le t\le1-1/B$, by bounding with $c=2$. When $c\in[l,r]\subset[1,2]$, $t$ lies between $\max(0,1-r/(2A))$ and $1-l/(2B)$. This follows by monotonicity in $a,b$ at $c=l,r$. Choose $\epsilon\ge0$ above $F$ on the first interval and $p_j\ge0$ above $F-\epsilon$ on the second.

If $c<2$, the actual opposite pair $\{\pm z\}$ is the short anchor of one parity class. For a fixed $x_i$ and a fixed $\{\pm z\}$, at most two choices of the line $x_j$ give that difference, since $x_j$ is represented by $x_i+z$ or $x_i-z$. Thus for $m>0$
$$
 (b_0-\epsilon)m\le F(1)-\epsilon+2\sum_j p_j n_j .
$$
The right side is nonnegative for $m=0$. This is valid for every lattice and requires neither integrality of the Gram matrix nor an assumed angular distribution. Dividing by the same $N$, add these inequalities for the two intervals $(59/48,61/48]$ and $(47/32,145/96]$ to the Fourier density inequality. The certificate includes the prices and physical units (a factor of 1,000 in the search).

After addition let $s_j$ be the resulting density score for bin $j$ and $C_j$ the independently verified cumulative integer capacity, with $C_{\mathrm{last}}=N$. Every admissible population has average score bounded by
$$
 \frac1N\sum_j(C_j-C_{j-1})\max_{k\ge j}s_k .
$$
This follows by sorting classes by anchor bin: a slot of index greater than $C_{j-1}$ lies at bin $j$ or later. The checkers compute the same value by sorting scores and by summing ordered slots.

## Verification

The first verifier isolates all derivative roots and encloses the polynomial on every continuum interval over the rationals. The second uses independent square-free factorization and Sturm variations for the signed threshold polynomials and checks the alternative population calculation. Both use the same published lower-dimensional input and the replayed parity/Fourier certificate. The second check covers 194 angle intervals. The global density, rounded upward, is **0.033997010427326**. The previous upper was **0.033997149607843**. The new length-dependent geometry was verified and included; its fixed-polynomial ablation leaves the previous worst class unchanged. The measured improvement comes from coupling populations and charging differences. [Exact certificate](angle-price-v1-exact.json) · [Sturm cross-check](angle-price-v1-sturm-audit.json) · [Forward density replay](rank14-joint-sharp-ref-314-384-front-result.json) · [Backward density replay](rank14-joint-sharp-ref-314-384-back-result.json)
