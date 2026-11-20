# A compact plane inequality with independent origins and radial cutoffs

Normalize the squared minimum of the lattice to one. Index short directions by opposite pairs and use one representative per pair. Write \(a=|v|^2\), \(R=19/13\), \(H(a)=(h^6,h^9,h^{12})^t\), \(h=(19-13a)_+/6\). A source certificate in dimension \(d\) supplies positive semidefinite matrices \(B_j\), nonnegative \(c_j\) with \(c_0=1\), and \(q=\sum_jc_j\). Its kernel on two lines is
\[
 K(v,w)=q^{-2}\sum_j c_j\,H(a)^tB_jH(b)\,G_{2j}^{(d)}(\cos\angle(v,w)),
\]
where the zonal polynomial is normalized to one at one. The source's two geometric sign checks apply to the off-diagonal pairs in each real lattice plane. The two-line check bounds a single interaction when the absolute cosine is at most \(1/2\). The three-line check bounds the *sum* of all three interactions on the full reduced-plane domain. All upstream geometric package replays used in the comparison completed, including the interval proof of the latter sign. The source snapshot is pinned to commit 9a9851887da20ca75825342bfb09e8ab031f4153.

## Why a smaller cutoff works

The lattice in the span of any independent pair is a saturated two-dimensional lattice. It has three nonzero parity classes. Each contains at most one opposite pair of squared length below two, since two distinct lines in one class have squared lengths adding to at least four. The zero class has no such vector. Thus the entire source support in a plane consists of at most three lines. Every off-diagonal pair occurs in a unique plane.

Choose \(s\ge1\). Evaluating the source on \(\sqrt{s}L\) preserves the minimum-length lower bound. Optionally truncate further at squared length \(T\) in the original lattice, where \(1<T\le R/s\), by setting the features to zero at and beyond \(T\). A retained three-line interaction is precisely the verified original three-line interaction. If just two independent lines remain, orient them acutely, with squared lengths \(a\le b\). Were the cosine greater than \(1/2\), their difference would be a third distinct lattice line with squared length strictly less than \(b\). It too would be retained. Thus the two-line check applies. The same argument works with either consistent convention at the endpoint. A closed-interval analytic check on both sides gives both limiting bounds. This proof permits separate cutoffs for different kernels in one nonnegative sum.

## Restriction to a smaller dimension and the origin

For \(n\le d\), embed the actual lattice span isometrically in \(\mathbb R^d\). Restriction leaves the values on every actual pair unchanged. The spherical addition theorem gives a positive kernel on \(S^{n-1}\). Its degree-zero part has matrix
\[
 M=\sum_j c_j B_j\,\mathbb E_{u\in S^{n-1}}G_{2j}^{(d)}(u_1),
 \qquad W=q^{-1}\sum_jc_jB_j .
\]
The spherical averages are nonnegative and are evaluated by rational even moments. All nonconstant components give a nonnegative quadratic form on the common set of lines. For \(\alpha>0\), an arbitrary real column \(z\), and \(M\) positive definite, completing the square on the constant component costs \(s_0=z^tM^{-1}z/\alpha\). Indeed, with \(b=2\sum_{\rm lines}H(sa)/q\) restricted to the chosen cutoff, \(\alpha b^tMb+2z^tb+s_0\ge0\). The factor two assigns both signs of every lattice line its actual multiplicity.

Adding the other spherical components and discarding the nonpositive off-diagonal plane sums gives
\[
 s_0+2\sum_{\rm lines}g(a)\ge0,\qquad
 g(a)=\frac{2}{q}\{z^tH(sa)+\alpha H(sa)^tWH(sa)\}
\]
on the retained support, with zero outside. The factors follow from four copies of each line diagonal in the signed double sum. This also establishes the sign of the correction when combined with the spatial Fourier function. Different kernels may use different \(z,\alpha,s,T\). Their costs and their corrections add.

## Combining with Fourier and checking the certificate

Let the spatial radial function be \(f(a)=P(\tau a)e^{-\tau a/2}\) and \(Q\) its normalized Laguerre transform as in the [Fourier proof](PROOF-parity-Fourier.md). If \(f(a)+\sum g(a)\le0\) for every \(a\ge1\), the lattice sum of \(f\) is at most \(P(0)+\sum s_0\). The same conclusion with an extra allowance \(B\) applies if the sum of the residual over nonzero signed lattice vectors is bounded by \(B\). This is where length bins and common parity counts can enter.

With \(Q\ge0\) on the entire nonnegative axis and \(Q(0)>0\), Poisson summation now gives
\[
 \Delta(L)\le \frac{(\tau/8)^{n/2}}{\Gamma(1+n/2)}
              \frac{P(0)+\sum s_0+B}{Q(0)} .
\]
For the compact-only comparison rows \(B=0\). The two analytic checkers reconstruct \(W,M,g,P,Q\) independently. One uses a local exponential expansion with an explicit exponential remainder. The other uses degree-four Bernstein bounds with a directed fifth-derivative enclosure, isolating every support breakpoint. Beyond the last cutoff the sign of \(-P\) is checked on a half-line. The independent verifier checks the sign of \(Q\) from zero and uses only \(Q(0)\). Additional reciprocal-vector terms used during numerical discovery are unnecessary for the displayed bounds.
