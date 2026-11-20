# Paying a two-vector angular inequality with the spatial Fourier tail

Normalize the squared lattice minimum to one. Let \(I=[A,B)\subset[1,2)\) be a source window and \(m\) its number of opposite pairs. Let \(R\) be the upper end of the primal class budget. Assume \(2+2A-B\ge R\) and \(f(x)\le0\) for \(|x|^2\ge R\). For each ordered pair of distinct source lines \(v,w\), use the two output lines \(2v+w,\ 2v-w\). The unordered pair of outputs is independent of orientations.

**Multiplicity and primitivity.** Each output has the unique short parity label of \(w\). A fixed output line \(x\) has at most two decompositions across all ordered input pairs: \(w\) is specified by this label, after which \(v\) is one of the lines \((x+w)/2,(x-w)/2\). With \(a=|v|^2,b=|w|^2\), the two actual squared output lengths are \(4a+b\pm4\langle v,w\rangle\). Their minimum is at least \(2+2a-b\), by applying the lattice minimum to both \(v+w\) and \(v-w\). In particular both lie in the spatial tail. Each output is primitive. It has nonzero parity and squared length \(<18\). If it were an odd multiple of a lattice vector, the only possible multiplier would be three. The shorter vector would have squared length below two and the same parity as \(w\), hence it would equal \(w\) up to sign, contrary to independence. A nonprimitive integer multiple of any existing short primitive line is therefore disjoint from these outputs. Windows with disjoint source labels for \(w\) cannot spend the same tail line.

Write \(N=2^n-1\). Suppose an even polynomial \(F\) with nonnegative Gegenbauer coefficients and constant harmonic \(c_0\) satisfies
\[
 N^2\{f(2v+w)+f(2v-w)\}+F(u)\le0,\qquad
 u=|\langle v,w\rangle|/\sqrt{ab}
\]
for all admissible lengths and angles. Multiplicity at most two permits the entire ordered input sum on the left inside an upper bound on the **signed** lattice tail, since each unoriented output contributes two signed copies of a nonpositive value. The addition theorem gives the following deduction from the original spatial budget:
\[
 \sum_{\rm output\ lines} 2f(x)
 \ \le\ [mF(1)-c_0m^2]/N^2 .
\]
For any fixed \(x_0\ge0\), an affine upper bound is \(c_0 x_0^2+(F(1)/N-2c_0x_0)m/N\). Multiple disjoint source windows may be added. For overlapping source windows, a sufficient accounting is that the total nonnegative allocation per short label \(w\) is at most one. Unrestricted multipliers on separate copies of the same tail would invalidate the conclusion. This proof uses the common parity map, both actual output lengths and the negative spatial tail beyond the class cutoff. It can be combined with nonprimitive multiple summation. It does not alter positivity on the Fourier-transform side.
