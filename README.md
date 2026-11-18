# Lattice sphere-packing density: upper bounds in dimensions 11–13, 15, 16 and 18–23

Upper bounds for the density of **lattice** sphere packings, with the exact data needed to check them.
Nothing here is a claim of optimality, of priority, or about non-lattice packings.

## Results

| n | Upper bound (this repository) | Comparison value | Best known lattice | Check it here |
|---:|---|---|---|---|
| 11 | 0.094565500874952 | none (general packings: ≈0.10664) | 0.066238 | `joint/n11` |
| 12 | 0.06770167234454 | none (general packings: ≈0.079503) | 0.049454 | `joint/n12` |
| 13 | 0.0486832075907 | none (general packings: ≈0.059905) | 0.032014 | `joint/n13` |
| 15 | 0.025212337452388 (conditional) | 0.0255112 | 0.0168575 | `dim15` |
| 16 | 0.0172314323416 | 0.0186552 | 0.0147081 | not yet, see [dim16](dim16/README.md) |
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
Weaker bounds for dimensions 19–22 that are also in this repository and are checked by other programs:

| n | Upper bound | Check it here | Method |
|---:|---|---|---|
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

**Dimensions 11, 12, 13, 19 and 20 (`joint/`).** The same kind of function, plus "joint cuts" that couple the lengths of two
vectors of one class with the lengths of their half-sum and half-difference through positive-definite Gegenbauer
kernels. The statement and proof sketch are in [`joint/THEOREM.txt`](joint/THEOREM.txt). The audit program
re-verifies the Fourier function, audits every kernel exactly, and runs a backward dynamic programme over all
admissible class counts in rational arithmetic:

```
python -B joint/audit_joint_bound.py joint/n19/bundle.json my-n19-audit.json
```

and likewise for `n11`, `n12`, `n13`, `n20`. The output file must not exist; the reference output of the author's
run is `audit.json` in each folder. A replay agrees with them in every field except the timing and the names and hashes of the
freshly written kernel-audit files. Needs mpmath. Two to ten seconds each.

**Dimensions 18–23 (`mixed/`).** The same kind of function and joint cuts, plus one new inequality for the vectors of a
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
in each folder. Needs mpmath. A few seconds each. The gain from the new inequality grows with the dimension: against
the same method without it, 0.2% in dimension 18 and 1.9% in dimension 23.

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
  the dimension-20 audit with their own code; they found no error. Their findings are summarised in section 7 of
  the note. No human has reviewed it. The auditor is a single implementation.
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
- `dim15/` – auditor, bundle, theorem note, the lemma documents and the review summary.
- `dim16/` – statement, documents, final audit outputs (paths inside them are replaced by `<TREE-A>`, `<TREE-B>`).
- `results.json` – the table above in machine-readable form.
- `SHA256SUMS` – hashes of every file in the repository.
