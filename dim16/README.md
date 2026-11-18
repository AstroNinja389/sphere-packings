# Dimension 16

**Statement.** Every lattice sphere packing in dimension 16 has density at most **0.0172314323416**
(equivalently γ₁₆ ≤ 2.88496372280). The Barnes–Wall lattice has density 0.0147081…, so the bound is about 1.172
times the best known lattice.

**Status: not replayable from this repository.** The bound was obtained on 11 November 2026 as the output of a
chain of exact certificates. The final audit re-checked the SHA-256 of 10,005 files (programs, certificates,
intermediate audits) that live in two working trees outside this repository; several of the programs refer to
those trees by absolute path. Packaging that chain so that a third party can run it is still to be done. Until
then this folder documents the claim; it does not let you verify it.

## What is here

- `documents/RESULT-20261111-GROUPFLOOR-v1.txt` – the result note written when the chain passed: branches, what
  changed in the last step, checks passed, caveats. Copied verbatim.
- `documents/GROUPED-FLOOR-THEOREM-v1.txt` – the lemma behind the last step. Copied verbatim.
- `outputs/union-summary.json` – the headline fields of the final union audit.
- `outputs/union-integrity.json.gz`, `low-integrity.json.gz`, `high-integrity.json.gz` – the final audit outputs of
  the union and of the two branches, including the full list of bound files and hashes. The only change from the
  originals is that the two working-tree prefixes are replaced by `<TREE-A>` and `<TREE-B>`; `PROVENANCE.json`
  gives the SHA-256 of each original and of each scrubbed text.
- `DEPENDENCIES.md` – how many bound files sit in which folder, and the names of the theorem and proof notes among
  them (59 notes).

## Shape of the argument

A linear-programming bound of Cohn–Elkies type with constraints on the vectors of each class modulo 2L, as in
arXiv:2610.35830, strengthened by facts special to dimension 16:

- lower bounds for the total squared length of a class with sixteen to nineteen short pairs (33, 575/16, 779/20,
  42 at minimum 1), the first of them valid for lattices denser than Barnes–Wall;
- a cap on the number of short vectors and a split of the argument by that number into a low branch (0 to 3700
  pairs) and a high branch (3651 to 4528), combined count by count;
- a separate bound for the branch in which one class contains a frame of sixteen short pairs.

Each branch has a forward computation, an independent backward computation that must agree exactly, and an
integrity audit; the union audit combines them and takes the maximum with the Barnes–Wall density, below which
the first length bound is not available.

## Review

The chain was built over several weeks inside the project, largely in computer-assisted sessions that the notes
refer to by name. Earlier links carry independent re-audits recorded inside the project; the last step (grouped
multipliers) was written and checked in a single session and has not been reviewed by a second party, as the
result note says. No one outside the project has checked any of it.
