# A lattice Fourier bound with common parity and angular populations

Let \(L\subset\mathbb R^n\) have squared minimum one. Write \(V_n=\pi^{n/2}/\Gamma(1+n/2)\), and let \(\Delta=V_n/(2^n\operatorname{covol}L)\). A “line” in the sums below is an opposite pair of lattice vectors. Below squared length four every such vector is primitive. A separate choice of orientation of each pair leaves every count and every even polynomial unchanged.

## Fourier normalization

Choose rational \(d_j\), \(\tau>0\), and write \(\ell_j(x)=L_j^{n/2-1}(x)/L_j^{n/2-1}(0)\). Let \(P=\sum d_j\ell_j\), \(Q=\sum(-1)^j d_j\ell_j\). Under the Fourier convention \(e^{-2\pi i\langle x,y\rangle}\), the transform of \(f(x)=P(\tau|x|^2)e^{-\tau|x|^2/2}\) is \((2\pi/\tau)^{n/2}Q(4\pi^2|y|^2/\tau)e^{-2\pi^2|y|^2/\tau}\). Thus if \(Q\ge0\) on the nonnegative axis, \(Q(0)>0\), and
\(\sum_{v\in L} f(v)\le P(0)+B\), Poisson summation gives
\[
 \Delta\le\frac{(\tau/8)^{n/2}}{\Gamma(1+n/2)}
             \frac{P(0)+B}{Q(0)}.
\]
All new middle-dimensional results with a successful global Fourier-sign check use this from zero. A gap available only under a determinant hypothesis would require a separate complementary branch.

Choose a rational cutoff \(R<\sqrt8\). Beyond it the certificate checks \(P(\tau a)\le0\). Below it partition squared lengths into bins \([l,r)\) with an edge at two. Closed-interval analytic enclosures also bound these half-open bins. Write \(N=2^n-1\), \(U\) for the integer rounding scale, and \(W_i\) for an upper integer bound on \(2NU f(v)\) in bin \(i\). The factor two counts both signs, and dividing a total over classes by \(N\) restores the original sum.

## What each parity class can contain

If \(v,w\) are different lines in the same class of \(L/2L\), then both \((v+w)/2\) and \((v-w)/2\) are nonzero in \(L\). For their squared lengths \(a,b\) this gives \(a+b\ge4\) and \(|\langle v,w\rangle|\le(a+b-4)/2\). The zero class contributes nothing below \(R\). Each of the other \(N\) classes has either no vector below two or exactly one such opposite pair, the short anchor. A class containing an anchor in a bin with right endpoint \(A\) cannot have an additional vector below \(S\) when \(A+S\le4\).

For \(S\ge2\), all pairs in a class with squared lengths below \(S\) have normalized absolute inner products at most \(z=1-2/S\). Apply the trace inequality \(\operatorname{tr}(H^2)\ge(\operatorname{tr}H)^2/n\) to the sum \(H\) of their unit rank-one projectors. If \(nz^2<1\), this bounds the class size by \(\lfloor n(1-z^2)/(1-nz^2)\rfloor\). For a short anchor its angle with every other member has squared cosine at most \(u=(A+S-4)^2/(4AS)\), where the class is nonempty. Monotonicity follows by differentiation on the admissible range. Orthogonal projection off the anchor gives the analogous cap in dimension \(n-1\) at cosine \((z+u)/(1-u)\) whenever the relative bound applies.

There is also a weighted cap. If \(k\) long lines are present, add \(t k\) times the anchor projector to their projector sum. Expanding the same trace inequality gives
\[
 k[1/n-z^2+2t(1/n-u)-t^2(1-1/n)]\le1-z^2.
\]
Choose \(t=(1/n-u)_+/(1-1/n)\) and use the bound whenever the bracket is positive. The verifier takes the minimum of valid caps, including the ordinary relative bound with the anchor counted.

For the fixed-total test define \(g(a)=(1-2/a)_+^2\). Two long lengths satisfy
\[
 \frac{(a+b-4)^2}{4ab}\le\frac{g(a)+g(b)}{2}.
\]
After clearing denominators the nonnegative difference has the factor \((a-b)^2(8-ab)\). For a short anchor the left side increases as its length approaches two on the admissible range, and the inequality follows at \(a=2,\ b<4\). Thus a class of \(k>n\) vectors contributes \(\sum g(a)\ge k(k-n)/(n(k-1))\) by the same trace inequality. All these statements apply to the actual common class, without assuming that its long lengths coincide.

## Constraints shared among classes

A projective polynomial with nonnegative even Gegenbauer coefficients, positive constant coefficient \(f_0\) and \(f(t)\le0\) for \(|t|\le z\) bounds the number of lines of such a code by \(\lfloor f(1)/f_0\rfloor\), by the spherical addition theorem. Through squared length \(s<2\) the lattice gives \(z=1-1/(2s)\) using both signs and length separation. A rational witness has the form \(t^{2j}(t^2-z^2)p(t^2)^2\). The independent verifier tests the harmonic signs by Rodrigues' formula; each derivative integral is a rational linear combination of the sphere moments \(\mathbb E(t^{2d})=(2d-1)!!/[n(n+2)\cdots(n+2d-2)]\). This proves a global prefix cap independent of the classwise moment calculation.

For an angular source window \([A,B)\subset[1,2)\), \(B-A<1\), let \(m\) count its lines and \(F\) have nonnegative even harmonic coefficients with \(F_0=1\). A bound \(F(t)\le\epsilon<1\) for \(0\le t\le1-1/B\) leaves an exceptional pair only when one signed difference \(w\) has squared length below two. It is unique up to sign, since the sum of the two candidate squared lengths is at least four. If \(w\) has length squared in \([l,r)\), the actual cosine lies between \(\max(0,1-r/(2A))\) and \(1-l/(2B)\). These bounds follow by minimizing or maximizing \((a+b-|w|^2)/(2\sqrt{ab})\) over the individual source lengths. Let \(p_j\) bound \((F-\epsilon)_+\) in that range. Fixing \(w\) gives a matching on the \(m\) lines. Indeed the two possible partners of a fixed \(x\) would be \(x+w,x-w\), whose squared lengths average at least two. Hence there are at most \(m/2\) unordered pairs for each \(w\).

Alternatively, the centered vectors \((x+y)/2\) for decompositions \(w=x-y\), up to signs, have squared length at most \(B-l/4\). Distinct centers are separated, including after sign changes, by a nonzero lattice vector. Their directions make squared cosine at most \((B-A)^2/[l(4A-l)]\) with \(w\). Projective code bounds in \(n\) or in \(w^\perp\) give an upper bound \(D_j\) for the number of decompositions per \(w\). Write \(m_j\) for the number of all short lines in bin \(j\). Applying the addition theorem to \(F-\epsilon\) now gives either
\[
 (1-\epsilon)m-\sum_j p_jm_j\le F(1)-\epsilon
\]
(the zero-mass case holds directly), or
\[
 (1-\epsilon)m^2\le (F(1)-\epsilon)m+2\sum_j D_jp_jm_j.
\]
For integer \(m,k\), \(m^2\ge(2k+1)m-k(k+1)\). This gives rational linear count constraints at the chosen tangents. The pinned input's original prefix-window cuts use its real square tangent and its recorded projected degree bounds; the independent implementation verifies their complete angular intervals and every projected degree by the same addition theorem.

## From these certificates to a single density

Every shared inequality has the form \(N^{-1}\sum_{\rm classes}\sum_i h_i m_{c,i}\le b\). Give it a nonnegative rational multiplier \(\alpha\). Add \(\alpha b\) to the global allowance, then subtract \(\lfloor U\sum\alpha h_i\rfloor\) from each integer height \(W_i\). This operation combines constraints on the same population. Different class patterns do not receive different copies of the global allowance.

Fix the anchor bin and the total number of long lines. For any nonnegative price \(\lambda\), add \(\lceil\lambda g(r)\rceil\) to each long-bin score and subtract the floor of \(\lambda\) times the required class moment. At that fixed total, the \(j\)-th ordered long member can occur only after the corresponding cumulative class cap reaches \(j\). The suffix maximum of the adjusted heights therefore bounds its score. Summing those maxima, then maximizing over all allowed integer totals (including zero), bounds the class. The anchor contributes its own adjusted height and zero moment. Each supplied price is tested on the occupancy where it is used; no optimality of the numerical prices is needed.

Finally integrate the class bounds by their superlevel counts. At each level above the unanchored bound, every qualifying class contains a unique short line in a bin ending no later than the rightmost qualifying endpoint. Its population is at most the smallest applicable spherical prefix cap, and at most \(N\). This yields \(B\), including the global allowances, in the Fourier inequality above. The final verifier uses exact integer or rational arithmetic except for directed enclosures of exponentials and roots. It cross-checks the density factor by factorials and, in odd dimensions, a rational lower bound for \(\pi\).
