# Recovering part of the compact-plane allowance from actual contacts

Normalize the squared minimum to one. Let the compact part of an existing Fourier certificate use an even positive kernel \(K\) with signed lattice-vector convention and nonnegative coefficient \(\alpha\). After completing the square in its constant spherical harmonic, the signed double sum is nonnegative. Group its off-diagonal terms by the actual two-dimensional lattice plane. Each unordered pair of distinct opposite pairs contributes \(8\alpha K(v,w)\). The parent proof establishes that each entire plane sum is nonpositive. Any lower bound on the negative of these sums can therefore be subtracted from the parent’s spatial numerator.

A densest lattice exists, and its minimum-vector projectors span the symmetric matrices. Choose any \(M=n(n+1)/2\) distinct opposite pairs of **exact** minimum vectors. For two chosen lines write \(u=|v\cdot w|\); then \(0\le u\le 1/2\). Orient them acutely. They form a basis of their saturated plane. Indeed, rounding both coordinates in that basis places any point within squared distance \((2+2u)/4\le3/4\) of their span over the integers. A proper overlattice would contain a nonzero vector shorter than the minimum. Among the other integer combinations only \(v-w\) can have squared length strictly below two: \(v+w\) has length squared at least two, and any combination with a coefficient of absolute value two or more has squared length at least three. Its squared length is \(c=2-2u\). Its squared cosines with the two minimum lines both equal \((1-u)/2\).

For each eligible parent kernel, evaluate its two-minimum plane sum at these lengths, applying its actual dilation and cutoff to the third line. Multiply by \(-8\alpha\) and sum across eligible kernels to obtain \(b(u)\). A kernel with squared support at two vanishes there. Both sides of a hard cutoff are checked. A plane with \(u<1/2\) contains just this one pair of minimum lines. At \(u=1/2\) it can contain three pairs of chosen lines, and the charge per pair is \(b(1/2)/3\). All skipped parent kernels still satisfy their original plane bounds.

Choose coefficients \(c_j\) with \(c_j\ge0\) for \(j>0\), and put \(F(u)=\sum c_jG_{2j}^{(n)}(u)\), where \(G_{2j}(1)=1\). Verify \(F(u)\le b(u)\) on the whole interval, and \(F(1/2)\le b(1/2)/3\). The spherical addition formula gives the following lower bound on the total available slack from the chosen lines:
\[
\sum_{i<j} F(|v_i\cdot v_j|)
 \ \ge\ \tfrac12\left(M^2c_0-M\sum_jc_j\right).
\]
It applies to the same \(M\) lines throughout. No isotropy of their unweighted distribution is needed. All other planes retain their proved sign. In a reciprocal certificate the divisor includes the existing denominator gain and the original complementary density is retained.

The two checkers reconstruct each angular branch by different formulas. One expands the individual radial and angular polynomials symbolically. The other evaluates the actual pair lengths using the normalized Gegenbauer recurrence, reconstructs by rational interpolation at more than its required degree where needed, and checks each interval by a positive-coefficient substitution and dyadic subdivision. The finite extreme-lattice argument makes the resulting upper bound valid for every lattice. These deductions generally improve only later decimal places. The much larger gains from four radial coordinates are reported separately.

`minimum_plane_fit.py` · `verify_contact_payment.py` · [Parent plane proof](PROOF-compact.md)
