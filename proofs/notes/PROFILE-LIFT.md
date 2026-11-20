# Reusing a certified profile as a linear count constraint

Scale the lattice to squared minimum one, and let \(N=2^n-1\). Suppose a proof puts the squared lengths below \(R<4\) in bins, including an edge at two. Write \(m_i\) for the total number of opposite pairs in bin \(i\). Let \(j(c)\) be the short anchor bin in nonzero parity class \(c\), with index zero if there is no short anchor. Each class has at most one short anchor.

Examine a previous certificate *before* it maximizes over the anchor or takes its final packing bound. It has one radial score \(H_i\) per bin, one exact class budget \(V_j\) per anchor type, and possibly inequalities whose slack has a nonnegative sum over the lattice. Global constants are included in every \(V_j\) in normalized units. The integer maximization and the summed geometric inequalities give
\[
 N^{-1}\sum_i H_i m_i \le N^{-1}\sum_{c\ne0} V_{j(c)}.
\]
This holds for the common actual population under all determinant or geometric premises of the source. It also holds if any \(H_i\) is decreased. If a source only exposes certified upper envelopes for a radial function, evaluating that function at a rational point of each bin and rounding down gives safe replacement scores, because its envelope bounds every point in the bin.

Exactly \(m_j\) classes have short anchor in bin \(j\). Therefore the preceding inequality is the single linear row
\[
 N^{-1}\sum_i\bigl(H_i-\mathbf 1_{i\ {\rm short}}(V_i-V_0)\bigr)m_i\le V_0.
\]
The bound \(V_0\) may include the original Fourier-independent geometric allowances. The old Fourier origin and its Poisson denominator do not appear in this row. Retain the entire integer budget vector and the original class hypotheses. A published scalar density alone gives no such row.

A new Fourier function, a new compact-plane inequality, prefix capacities or other verified rows may all be priced against this same population. Nonnegative multipliers preserve the proof. When a mesh refines the source partition, transport each row by the containing source bin. The final proof rechecks the new Fourier signs, all physical interval bounds, the shared class counts, and the largest complementary density of any active case-specific input. It can combine several different certified profile shapes without assuming their individually maximizing class distributions coexist.
