# A convex consequence of the actual primal minimum

Let $T=Q^{-1}$ in dimension $r$, in integer lattice coordinates, with $Q[x]\ge m$ for all nonzero integral $x$. Consider the hypothesis $\det Q\le U$. For any positive definite rational comparison matrix $S$ and any one of those actual integer vectors, define
$$
 V=S-\frac{Sxx^tS}{x^t Sx}.
$$
Then
$$
 \operatorname{tr}(VT)\ \ge\ (r-1)
 \left(\frac{m\det S}{U\,x^t Sx}\right)^{1/(r-1)} .
$$

To see this, use an orthonormal basis ending in $x/\lVert x\rVert$. In its first $r-1$ coordinates, $V$ is the Schur complement of the last scalar block of $S$. It is positive definite on that subspace, with determinant $\lVert x\rVert^2\det S/S[x]$. The upper principal block of $T$ has determinant $\det T\;Q[x]/\lVert x\rVert^2$ by the cofactor identity. The product of these determinants is at least $m\det S/(U S[x])$. AM–GM on their positive product gives the trace inequality. Each comparison matrix and vector gives a linear condition on the *same actual inverse*. The positivity and determinant hypothesis are essential.

For dimension 13 we took $r=9,\ m=4,\ U=27757/25$ at the bottom of the section chain. The helper first tries $S$ near the perfect marking and may use a different rational $S$ from the first matrix optimization. To certify a quoted lower value $b$, the separate verifier proves $(b/8)^8 U S[x]\le4\det S$ in rational arithmetic. It then combines these rows with actual lifted single directions and signed triples. On the full-mark tests all primal contact inequalities are checked on a complete enumeration of the marking's exact minima. All the positive matrices, integer vectors and rational prices used for accepted cases are recorded in the witness streams.

An exclusion here contradicts the rank-nine determinant ceiling for an entire marked class. It does not establish a global density by itself. [Independent auditor](audit_cofactor.py) · [Section proof and initial coverage](SECTION-TRANSFER.md)
