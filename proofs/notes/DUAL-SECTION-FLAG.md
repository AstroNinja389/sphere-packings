# A two-dimensional reciprocal section contributes to the Poisson denominator

Let the primal lattice have minimum squared length one and density between a trial value \(t\) and a proved upper bound \(U\). Put \(s=4\pi^2/\tau\). Scale the dual lattice by \(\sqrt{s}\) and call its covolume \(B\). If \(V_j\) denotes the volume of the unit ball in dimension \(j\), then \(B=s^{n/2}2^n\Delta/V_n\). A primitive \(k\)-dimensional sublattice of the dual corresponds to a perpendicular section in the primal. The covolume of the perpendicular section is the product of the primal covolume and the covolume of the unscaled dual sublattice. Its minimum squared length is at least one. Consequently the Gram determinant in the scaled dual is at least
\[
 g_k=s^k (2^k V_{n-k}t/(V_n U_{n-k}))^2 .
\]
The inequality also holds for nonprimitive independent tuples because their index multiplies the covolume.

Choose a shortest dual vector \(x\), of squared length \(a\), and project the scaled dual along it. Choose a shortest nonzero vector of the projected lattice, of squared length \(b\), and lift it to \(y\), with \(x\cdot y/a=u\in[0,1/2]\) after subtracting a multiple of \(x\) and choosing its sign. Both vectors exist in the same lattice. Write \(\gamma_j=4(U_j/V_j)^{2/j}\) for an upper bound on the Hermite constant. With \(B_{\max}=s^{n/2}2^nU/V_n\), the parameters satisfy
\[
 g_1\le a\le\gamma_n B_{\max}^{2/n},\qquad
 ab\ge g_2,\qquad a\le b+a u^2,\qquad
 b\le\gamma_{n-1}(B_{\max}/\sqrt a)^{2/(n-1)} .
\]
The last inequality follows because the projected covolume is \(B/\sqrt a\). The projected shortest vector is primitive and any chosen preimage is a valid lift. Every integer pair \((i,j)\) gives an actual vector of squared length \(a(i+ju)^2+j^2 b\). Taking \(j>0\) or \(j=0,i>0\) counts one representative per opposite pair.

If the reciprocal Gaussian-polynomial function is nonnegative above the dual gap, a certified lower bound \(\eta\) for twice the sum of its values on a fixed finite list of these pairs increases the Poisson denominator from \(Q(0)\) to \(Q(0)+\eta\). The old spatial budget may include lattice-specific signed terms, parity, perfection and eutaxy. Each active conditional premise must still cover contenders above \(t\). A previous denominator already using reciprocal mass requires a joint accounting of the same vectors. The resulting unconditional upper bound is the larger of \(t\) and the new conditional density. The same construction can also permit a signed inner reciprocal shell when a separate rank or population bound pays every negative term.
