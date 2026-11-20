# Lattice bounds in dimensions 13 and 14

| Dimension | Lattice density upper bound | What the proof establishes |
|---|---:|---|
| 13 | **0.042023513562578** | Mordell's inequality applied to the sharp rank-12 input. The separate five-percent target **0.041382759430854** still has **15 open families**. |
| 14 | **0.03399687961750058** | A bound for every lattice, combining the rank-12 input, length constraints within each parity class, and differences across classes. |

Both bounds use the rank-12 result of Géraud-Stewart and Naccache with the classification and finite checks specified in their preprint. The finer dimension-13 exclusions also use their rank-10 and rank-11 results. The original rank-nine classification is an external input. [Hermite constants in dimensions 10–12](https://eprint.iacr.org/2026/2825) · [Rank-eleven paper](https://eprint.iacr.org/2026/2826)

The latest dimension-14 refinement bounds the number of pairs with each fixed short difference by a matching. [Proof](n14/MATCHING.md) · [Exact certificate](n14/tightmatching14-final-packing-proof.json)

## Reproduce

The full rank-14 replay also runs the final matching check. To check just the refinement against the archived Fourier budgets, run `python -B sections/n14/check_matching.py` from the repository root.

Run from the repository root with Python 3.11 or later and assertions enabled. The release was tested with Python 3.14.6. The verifiers use temporary working directories and leave the archived evidence intact.

```sh
python -m pip install -r sections/requirements.txt
python -B sections/replay13.py
python -B sections/replay14.py
```

The first command after installation computes the Mordell upper, the 5% target, and the determinant thresholds. To reproduce all dimension-13 marking exclusions, download `hermite11_rank9_reproduction.zip` from the authors' archive and extract `hermite11_rank9_reproduction/project/certificate_database/k11_certificates_v3.sqlite`. The full replay reads 4,487,813 selected rows. It checks the database SHA-256 `982eaf73232af64ccf3ad2123d5e1f3eef169976cb1a90b2f45eaae4389c59e8` before evaluating them. The compressed archive is approximately 1.44 GB and the extracted database approximately 1.92 GB. [Public certificate database](https://doi.org/10.5281/zenodo.23979316)

```sh
python -B sections/replay13.py --database /path/to/k11_certificates_v3.sqlite
```

The dimension-14 replay uses only the bundled files and Python dependencies. It checks both determinant ranges, the geometry for 12, 13 and 15 pairs, the Fourier signs, both directions of the 577-case integer calculation, and two exact continuum checks of the final angular inequality. The class calculation and angular calculation are separate stages. The final check covers 194 angle intervals. [Dimension-14 proof](n14/FOURTEEN.md) · [Rational certificate](n14/angle-price-v1-exact.json) · [Sturm verification](n14/angle-price-v1-sturm-audit.json)

## Previously established bounds

Values below are packing densities. The comparison uses the November 19 snapshot of `alexlegeartis/SpherePackings` at `9a98518`. The source table credits the constructions in its lower-bound column to the sources in Cohn's tables. [General-packing table](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/RESULTS.md) · [Lattice table](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/LATTICE_RESULTS.md)

| Dimension | Previously established general-packing lower | Best known lattice lower | Previously established upper | Lattice upper here | Remaining lattice gap |
|---|---:|---:|---:|---:|---:|
| 13 | ≈0.032014 | ≈0.029208430928108 | 0.059905026 (all packings) | 0.042023513562578 | ≈0.012815082634470 |
| 14 | ≈0.021624 | ≈0.021624096082447 | 0.0347128 | 0.03399687961750058 | ≈0.012372783535054 |

The pinned lattice table starts at dimension 14. Its companion general-packing table gives the dimension-13 upper 0.059905026, valid also for lattices. The general-packing lower comes from a periodic packing with 72 spheres per unit cell. The lattice comparison and five-percent target use the density of K₁₃. In dimension 14, Λ₁₄ supplies the lower in both tables. Relative to the previously established lattice upper, the new upper closes approximately **5.47%** of the gap to Λ₁₄. The matching refinement lowered the preceding upper of 0.033997010427326 to 0.03399687961750058. [Cohn's packing table](https://cohn.mit.edu/sphere-packing/) · [Nebe–Sloane lattice catalogue](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/density.html)

## The open dimension-13 target

Let Δ be the supremum of the lattice packing densities. The target would establish Δ ≤ 0.041382759430854, closing 5% of the gap from the Mordell upper to K₁₃. A minimum-four Gram determinant floor of 242111/500 would suffice. At this target the reduction starts with 1,746,860 rank-nine markings. The certificates exclude **1,746,845**. A marking labels a possible continuous family of section metrics and extensions. [Descent and both dual orientations](n13/SECTION-TRANSFER.md) · [Cofactor inequality](n13/COFACTOR.md)

| After applying | Open markings |
|---|---:|
| Rank-nine determinant filter | 1,746,860 |
| Trace witnesses clearing the stronger rank-ten threshold | 704,615 |
| Both orientations of the two successive sections | 14,955 |
| Linked reciprocal vectors and the full marking cone | 7,741 |
| Primal-minimum cofactor inequalities and matrix tests | 75 |
| Interval cover for the rank-ten dual minimum | 36 |
| Reciprocal plane areas and upper bounds on individual contact weights | 32 |
| Joint contact weights and common-circle lift constraints | **15** |

A joint test of contact weights, section lengths and circle lifts reduces the 32 to **15**. The open list consists of **ten exceptional markings and five tree markings**. [Exact certificates and proof](n13/CONTACT-PRICES.md) · [Current list](n13/OPEN-AFTER-CONTACT-PRICES.txt)

The previous 32 comprised 15 tree marks, three glue marks, three domain marks, one reverse-orientation trace mark and the ten exceptional marks in the rank-eleven paper. For 19 of them a further check excludes an explicit one-sided neighborhood of the reference metric. [Identifiers at the preceding stage](n13/FINAL-OPEN-MARKS.txt) · [Final interval and plane argument](n13/INTERVALS.md) · [Neighborhood witnesses](n13/reference-neighborhoods.json)
