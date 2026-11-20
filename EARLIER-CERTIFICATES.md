# Earlier certificates in dimensions 10–23

This page documents the preceding release and its reproduction commands. The [current bounds and comparison](proofs/COMPARISON.md) incorporate the subsequent improvements.

## Results

| n | Upper bound (this repository) | Comparison value | Best known lattice | Check it here |
|---:|---|---|---|---|
| 11 | 0.090771844556272 (conditional) | none (general packings: ≈0.10664) | 0.066238 | `count/n11` |
| 12 | 0.065276234098413 (conditional) | none (general packings: ≈0.079503) | 0.049454 | `count/n12` |
| 13 | **0.042023513562578** (Mordell and cited rank-12 theorem) | none (general packings: ≈0.059905) | 0.029208430928107 (K₁₃) | [Section proof and replay](sections/README.md) |
| 14 | **0.033997010427326** (uses cited rank-12 theorem) | 0.0347128 | 0.0216240 (Λ₁₄) | [Geometry, Fourier and angular certificates](sections/n14/FOURTEEN.md) |
| 15 | 0.025212337452388 (conditional) | 0.0255112 | 0.0168575 | `dim15` |
| 16 | 0.0172314323416 | 0.0186552 | 0.0147081 | not yet, see [dim16](dim16/README.md) |
| 17 | 0.013763319803959 (conditional) | 0.0138325 | 0.00881131 | `frame/n17` |
| 18 | 0.010336520221586 | 0.0103439 | 0.00592836 | `mixed/n18` |
| 19 | 0.0077671805985286 | 0.00780844 | 0.00412080 | `mixed/n19` |
| 20 | 0.0058802043811005 | 0.00595464 | 0.00322586 | `mixed/n20` |
| 21 | 0.0044694365948149 | 0.00455796 | 0.00246588 | `mixed/n21` |
| 22 | 0.0033989364209325 | 0.00348294 | 0.00212766 | `mixed/n22` |
| 23 | 0.002581019409686 | 0.00260841 | 0.00190532 | `mixed/n23` |

"Comparison value" is the lattice-only upper bound listed in
[alexlegeartis/SpherePackings, `LATTICE_RESULTS.md`](https://github.com/alexlegeartis/SpherePackings/blob/main/LATTICE_RESULTS.md)
as read on 18 November 2026 (its release notes are dated 17 November 2026). Those values were not replayed here.
That table starts at dimension 14; for 11–13 the value in brackets is the upper bound for general packings in the same
repository (`RESULTS.md`), which also bounds lattices.
"Best known lattice" is the density of the densest lattice known, rounded down, for orientation only.

**Dimension 13.** The stronger target **0.041382759430854 remains open**. At that target, 1,746,828 of 1,746,860 candidate rank-nine markings are excluded. The **32 remaining families** can each contain continuous choices of section metric and gluing. The competitor's general-packing lower of approximately 0.032014 comes from a periodic packing with 72 spheres per cell. Our lattice comparison uses K₁₃. [Remaining markings](sections/n13/FINAL-OPEN-MARKS.txt) · [Competing general table](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/RESULTS.md) · [Lattice catalogue](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/density.html)

**Dimension 14.** Against the competitor's displayed lattice upper of 0.0347128 and the Λ₁₄ lower of approximately 0.021624096082447, our upper closes **5.47% of their remaining gap**. The final refinement alone lowered our previous upper of 0.033997149607843 by 0.000000139180517. Both dimension-13 and dimension-14 bounds use the sharp rank-12 result with its stated classification and computational inputs. [Competing lattice table](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/LATTICE_RESULTS.md) · [Lower-dimensional theorem](https://eprint.iacr.org/2026/2825) · [Proofs and reproduction commands](sections/README.md)

Weaker bounds that are also in this repository and are checked by other programs:

| n | Upper bound | Check it here | Method |
|---:|---|---|---|
| 10 | 0.13010849917496 | `joint/n10` | certificate plus joint cuts (unconditional; not a best bound for dimension 10, here because the dimension-11 row uses it) |
| 11 | 0.092981475168202 | `frame/n11` | bootstrapped frame floor, three rounds (conditional on the determinant lemma) |
| 11 | 0.094565500874952 | `joint/n11` | certificate plus one joint cut (unconditional) |
| 12 | 0.066670465797823 | `frame/n12` | bootstrapped frame floor with odd-order exclusion (conditional) |
| 12 | 0.06770167234454 | `joint/n12` | certificate plus one joint cut (unconditional) |
| 13 | 0.047947694667495 | `frame/n13` | earlier conditional frame calculation |
| 13 | 0.0486832075907 | `joint/n13` | certificate plus one joint cut (unconditional) |
| 14 | 0.034664418153345 | `frame/n14` | earlier conditional frame calculation |
| 17 | 0.013875579669877 | `joint/n17` | certificate plus one joint cut (unconditional; weaker than the comparison value 0.0138325) |
| 19 | 0.0078055517781953 | `joint/n19` | certificate plus joint cuts |
| 20 | 0.0059269594018778 | `joint/n20` | certificate plus one joint cut |
| 20 | 0.0059274281468171 | `certificates/n020.json` | plain certificate, four verifiers |
| 21 | 0.0045221361589603 | `certificates/n021.json` | plain certificate, three verifiers |
| 22 | 0.0034531371421659 | `certificates/n022.json` | plain certificate, four verifiers |

## How each row is established

**Dimensions 20, 21, 22 (`certificates/`).** Certificates in the format of Theorem 1 of arXiv:2610.35830 (classes
modulo 2L), with a wider length range and a re-optimised function. Each is checked by exact arithmetic in several
independent verifiers taken unchanged from the repository of that paper:

```
python -B verify/run_all.py --gp /path/to/gp
```

`taylor` and `bernstein` need only the Python standard library, `descartes` (even dimensions) needs python-flint,
`pari` needs PARI/GP. A verifier that cannot run is reported as skipped, never as passed. On the author's machine
all applicable verifiers pass for the three files (four for n = 20, 22; three for n = 21).

**Dimensions 10, 11, 12, 13, 17, 19 and 20 (`joint/`).** The same kind of function, plus "joint cuts" that couple the lengths of two
vectors of one class with the lengths of their half-sum and half-difference through positive-definite Gegenbauer
kernels. The statement and proof sketch are in [`joint/THEOREM.txt`](joint/THEOREM.txt). The audit program
re-verifies the Fourier function, audits every kernel exactly, and runs a backward dynamic programme over all
admissible class counts in rational arithmetic:

```
python -B joint/audit_joint_bound.py joint/n19/bundle.json my-n19-audit.json
```

and likewise for `n10`, `n11`, `n12`, `n13`, `n17`, `n20`. The output file must not exist; the reference output of the author's
run is `audit.json` in each folder. A replay agrees with them in every field except the timing and the names and hashes of the
freshly written kernel-audit files. Needs mpmath. Two to ten seconds each.

**Dimensions 18–23 (`mixed/`).** The same kind of function (with one joint cut in dimensions 18 and 19), plus one new inequality for the vectors of a
class modulo 2L (the "mixed relative bound"): if y₁, …, y_K lie in one class, are pairwise different up to sign and
have squared lengths mᵢ between 2 and 2√2 (minimum 1), then Σ (1 − 2/mᵢ)² ≥ K(K − n)/(n(K − 1)). For equal lengths
this is the relative bound for lines, which the class budget of the earlier paper uses through cumulative caps; the
mixed form charges every vector with its own length. The statement, its one-page proof and the way it enters the
class budget are in [`mixed/MIXED-RELATIVE-BOUND.txt`](mixed/MIXED-RELATIVE-BOUND.txt). It needs no assumption on the
lattice, so these rows are not conditional. The audit program is the joint-cut auditor with this one addition:

```
python -B mixed/audit_mixed_bound.py mixed/n20/bundle.json my-n20-audit.json
```

and likewise for `n18`, `n19`, `n21`, `n22`, `n23`. The output file must not exist; the reference outputs are `audit.json`
in each folder; a replay agrees with them in every field except the timing and, for `n18` and `n19`, the names and
hashes of the freshly written kernel-audit files. Needs mpmath. A few seconds each. The gain grows with the dimension: against the earlier entries of this
repository listed above it is 0.49% in dimension 19, 0.79% in 20, 1.17% in 21 and 1.57% in 22.

**Dimension 11 (`frame/`, superseded by `count/n11`), conditional on a determinant lemma.** A class with eleven pairs of squared length about 2
(a "frame") forces the lattice to contain a perturbed copy of D₁₁, so its density is (index) × (density of that copy),
and the index is an integer. If the lattice is denser than 4 times the density of D₁₁, the index is at least 5, and
the bound already known for dimension 11 then forces the Gram determinant of the frame, hence the excess
Σ max(|x|², 2) − 22, to be large. This gives a floor on such classes with no further input; the bound it yields is
used as the known bound of the next round. Three rounds (`frame/n11/r1`, `r2`, `r3`), each with its own premise file
(statement, numbers, six-line proof) and exact audit:

```
python -B frame/check_det_n_v1.py 11 1/4
python -B frame/audit_frame_bound.py frame/n11/r1/bundle.json my-n11-r1.json
```

and likewise `r2`, `r3`. Round 1 starts from the bound of `joint/n11`; rounds 2 and 3 start from the result of the
previous round (the number in its `audit.json`). The general statement is in
[`frame/BOOTSTRAPPED-FRAME-FLOOR.txt`](frame/BOOTSTRAPPED-FRAME-FLOOR.txt). **The condition:** the proof uses det Q ≥ 1
for the Gram matrix of a near-frame. That is the determinant lemma, written out for general dimension in
[`frame/DETERMINANT-LEMMA-GENERAL-N-v1.txt`](frame/DETERMINANT-LEMMA-GENERAL-N-v1.txt); its last step is an interval
computation done by `frame/check_det_n_v1.py` (a few seconds; the stored output is `frame/n11/check-det-n-v1-N11-D1_4.log`).
Each round is also conditional on the bound it starts from and on the audit program. Needs mpmath.

**Dimensions 12 (superseded by `count/n12`) and 13 (`frame/`), conditional on the determinant lemma and an odd-order lemma.** The same integrality
argument, with one more elementary ingredient: the index is the order of a finite group of "glue" classes, and such
a group cannot contain an element of order 3, 5 or 7 in dimension 12 (3 or 5 in dimension 13), because the multiples
of such an element cannot all be as long as the minimum requires. This is a finite computation over residue patterns
([`frame/ODD-ORDER-EXCLUSION-v1.txt`](frame/ODD-ORDER-EXCLUSION-v1.txt), `frame/check_odd_order_v1.py`, exact
rational arithmetic, seconds). In dimension 12 a lattice denser than 4 times D₁₂ with a near-frame would have index 5,
6 or 7, in dimension 13 a lattice denser than 8 times D₁₃ would have index 9 or 10; all are excluded, which gives the
full floor in one round:

```
python -B frame/check_det_n_v1.py 12 1/4
python -B frame/check_odd_order_v1.py 12 1/4 3 5 7
python -B frame/audit_frame_bound.py frame/n12/r1/bundle.json my-n12.json
```

and likewise for 13 (`check_odd_order_v1.py 13 1/4 3 5`). The thinnest place is dimension 13, order 3: 17.92 against 18.

**Dimensions 11 and 12 (`count/`), conditional on a theorem about n − 1 pairs with computer-checked lemmas.** The rows of the
first table for dimensions 11 and 12. The floor is put on n − 1 pairs of one class instead of n: in a lattice of
dimension 11 denser than 0.0905, any ten distinct pairs of one class, each of squared length below 9/4, have
Σ max(|x|², 2) > 20 + 3/4; in a lattice of dimension 12 denser than 0.065, any eleven such pairs have
Σ max(|x|², 2) > 22 + 3/4. Ten such pairs span a perturbed copy of D₁₀ inside a 10-dimensional section of the lattice.
The known bound for dimension 10 (`joint/n10`) and the odd-order lemma leave index 1 or 2 for that copy in the section,
and the density assumption then makes the next layer of the lattice so close that a point q of it has both q and 2q
at least as far from the copy as the minimum allows; two table lemmas in ten coordinates say that this cannot happen.
Dimension 12 is the same one dimension higher, with `joint/n11` as the known bound. The audit program is the frame
auditor with the floor on n − 1 pairs and the density threshold as an explicit complement:

```
python -B count/check_det_n_v2.py 10 3/8
python -B frame/check_odd_order_v1.py 10 3/8 3
python -B count/audit_count_bound.py count/n11/bundle.json my-n11.json
python -B count/check_det_n_v2.py 11 3/8
python -B frame/check_odd_order_v1.py 11 3/8 3 5
python -B count/audit_count_bound.py count/n12/bundle.json my-n12.json
```

The proofs are `count/n11/TEN-PAIRS-PREMISE-n11-v1.txt` and `count/n12/ELEVEN-PAIRS-PREMISE-n12-S3_4-v1.txt`.
**What cannot be replayed here** are the table lemmas (one table of 13,160 cases and one of 118,440 for dimension 11,
two of 118,440 for dimension 12, with 111 cell files): each was produced by one program and re-checked by a second
implementation of the same author. The logs, the bookkeeping files and the programs are in `count/n11`, `count/n12`
and `count/lemma-programs`; the tables and cell files are not. [`count/COUNT-FLOORS-11-12.txt`](count/COUNT-FLOORS-11-12.txt)
says exactly what is here and what each bound depends on. The bounds of `frame/n11` and `frame/n12` below are weaker
and rest on fewer assumptions.

**Dimensions 14 and 17 (`frame/`), conditional on a frame theorem with computer-checked lemmas.** Here the frame floor
is not bootstrapped from a known bound; the index of the perturbed copy of Dₙ is bounded directly. It is the order of a
finite group G of glue classes, and Σ ψ(g) ≥ 0 over G for ψ(g) = Σᵢ cos 2πgᵢ. Elements of order two have ψ ≤ n − 16,
and for every other element a "hybrid lemma" (both g and 2g are at least as long as the minimum) gives ψ < −1 in
dimension 14 and ψ < −9/20 in dimension 17. Hence the index is at most 14 in dimension 14; in dimension 17 it is at
most 64, starting from the cap 79 that the bound of `joint/n17` gives. The resulting floors are 5/8 and 11/25:

```
python -B frame/check_det_n_v1.py 14 5/16
python -B frame/audit_frame_bound.py frame/n14/r1/bundle.json my-n14.json
python -B frame/check_det_n_v1.py 17 1/4
python -B frame/n17/check_apriori_n17_v1.py
python -B frame/audit_frame_bound.py frame/n17/r1/bundle.json my-n17.json
```

The proofs are `frame/n14/r1/FRAME-PREMISE-n14-v2.txt` (with `-v1` for the unchanged steps) and
`frame/n17/r1/FRAME-PREMISE-n17-v1.txt`. **What cannot be replayed here** are the two hybrid lemmas: each is a table
of 13,160 cases plus cell files, produced by one program and re-checked by a second implementation of the same
author. The logs, the bookkeeping files and the programs are in `frame/n14`, `frame/n17` and `frame/lemma-programs`;
the tables and cell files are not. [`frame/FRAME-THEOREMS-14-17.txt`](frame/FRAME-THEOREMS-14-17.txt) says exactly
what is here, what a replay reproduces and what each bound depends on.

**Dimension 15 (`dim15/`), conditional.** A constraint special to this dimension: in a 15-dimensional lattice denser
than the laminated lattice Λ₁₅, any fifteen distinct pairs of one class modulo 2L, each of squared length at most
9/4 (minimum 1), have Σ max(|x|², 2) > 123/4. The statement and its short proof are in
[`dim15/N15-FRAME-FLOOR-THEOREM-v2.txt`](dim15/N15-FRAME-FLOOR-THEOREM-v2.txt); it follows from a determinant lemma,
an index bound and a computer-assisted "two-class lemma", whose statements and proofs are in `dim15/documents/`.
The audit program adds this constraint to the class budget exactly and takes the maximum with the density of Λ₁₅:

```
python -B dim15/audit_frame_floor_bound.py --selftest
python -B dim15/audit_frame_floor_bound.py dim15/bundle.json my-n15-audit.json
```

The audit itself can be replayed here (a few seconds; needs mpmath). **What cannot be replayed here** is the
two-class lemma: its 118,440 certificates and the programs that check them are not in this repository. The bound
is therefore conditional on that lemma and on the two others; see the review note below.

**Dimension 16 (`dim16/`).** The value 0.0172314323416 is the end of a long chain of exact certificates that uses
structure specific to dimension 16. **It cannot be replayed from this repository yet**: the chain's programs and
data (about ten thousand hash-bound files) are not packaged. What is here is the statement, two of the proof
notes, the final audit outputs with their hash lists, and an inventory of what the chain depends on. See
[dim16/README.md](dim16/README.md) before relying on this row.

## What has and has not been reviewed

- The four certificate verifiers share no implementation code and come unchanged from the repository of the
  earlier paper. The three certificates themselves are new and have been checked only by those programs.
- The joint-cut auditor is a single implementation, written separately from the search that produced the cuts.
  The theorem note has not been reviewed outside the project.
- The mixed relative bound (dimensions 18–23) was written and machine-tested inside the project on 18 November 2026.
  Two independent automated reviewers (not humans) re-derived the proof, attacked it numerically (including all
  classes of the Barnes–Wall lattice in dimension 16, where it holds with equality on some classes) and recomputed
  a dimension-20 audit of the project with their own code; they found no error (section 7 of the note). A third
  automated reviewer worked from this repository alone: it replayed the six bundles and recomputed the class budget
  of each with its own program (a different dynamic programme; the joint-cut part of dimensions 18 and 19 was
  reused), in agreement on all 97 rows in every dimension. No human has reviewed any of this.
- The odd-order lemma behind dimensions 12 and 13 was written on 18 November 2026 and checked by an automated
  reviewer (not a human); see section 7 of `frame/BOOTSTRAPPED-FRAME-FLOOR.txt`.
- A further automated checker, working from this repository alone, replayed the five `frame/` bundles and recomputed
  their class budgets, including the frame case, with two programs of its own; all values agree (section 8 of
  `frame/BOOTSTRAPPED-FRAME-FLOOR.txt`).
- The dimension-11 frame floor was written on 18 November 2026. An automated reviewer (not a human) re-derived the
  six steps, the induction over the rounds and the numbers; see the end of `frame/BOOTSTRAPPED-FRAME-FLOOR.txt`.
  The determinant lemma it uses was reviewed with the dimension-15 lemmas (automated review only). No human has
  reviewed either.
- The ten-pair and eleven-pair theorems of dimensions 11 and 12 (`count/`) were written on 18 November 2026. For each,
  an automated referee (not a human) re-derived the proof text and its numbers and found no error; its report is in
  the folder. It did not check the tables, the bookkeeping or the cell scheme. The table lemmas were checked by two
  programs of the same author. The determinant lemma is used in a wider form (v2) whose change against v1 has had
  no separate review, and the level limit SMALL3 used in dimension 12 was checked by the automated referee only.
  The count auditor is the frame auditor with two lines changed and has not been recomputed by an independent
  program. No human has reviewed any of this.
- The frame theorems of dimensions 14 and 17 were written on 18 November 2026. Their hybrid lemmas were checked by
  two programs of the same author (a first program and a re-check in ball arithmetic). Neither the theorems nor the
  lemma programs have had a second-party review, automated or human.
- The dimension-15 constraint rests on three lemmas written and machine-checked inside the project. On
  18 November 2026 five independent automated reviewers (not humans) re-derived them, tested them against brute
  force and searched for counterexamples; they found no error, and three gaps of exposition that are now written
  up. Their findings are in [`dim15/documents/REVIEW-SUMMARY-v1.txt`](dim15/documents/REVIEW-SUMMARY-v1.txt). No
  human has reviewed these lemmas.
- The dimension-16 chain was produced and checked inside the project, largely by computer-assisted sessions; its
  most recent steps have not been reviewed by a second party. Details in `dim16/`.

## Requirements

Tested with Python 3.14.6, python-flint 0.9.0, mpmath 1.3.0 and PARI/GP 2.19.0 on Windows. Do not run with
`python -O`: the programs use assertions.

## Licence

No licence has been chosen yet; none is granted by this checkout.

## Files

- `certificates/` – three certificates (JSON, rational data only).
- `verify/` – the four verifiers, the GP script, and `run_all.py`.
- `joint/` – auditor, kernel auditors, theorem note, and one bundle per dimension.
- `mixed/` – the mixed relative bound (note with proof), its auditor, and one bundle per dimension 18–23.
- `frame/` – the bootstrapped frame floor: note, determinant check, auditor with the frame case, three rounds for dimension 11, one round each for dimensions 12 and 13 (with the odd-order lemma and its check); the frame theorems of dimensions 14 and 17 with their bundles, logs and bookkeeping files, the lemma programs (`lemma-programs/`) and a note on what is replayable.
- `count/` – floors on n − 1 pairs of one class (dimensions 11 and 12): auditor, bundles, premise texts, referee reports, logs and bookkeeping files of the table lemmas, the lemma programs (`lemma-programs/`), determinant lemma v2 with its check, and a note on what is replayable.
- `dim15/` – auditor, bundle, theorem note, the lemma documents and the review summary.
- `dim16/` – statement, documents, final audit outputs (paths inside them are replaced by `<TREE-A>`, `<TREE-B>`).
- `results.json` – the table above in machine-readable form.
- `SHA256SUMS` – hashes of every file in the repository.
- `sections/` – dimension-13 Mordell bound, finite exclusions and 32 open families; dimension-14 global proof with geometry and angular replays.
