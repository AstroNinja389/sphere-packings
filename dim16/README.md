# Dimension 16

**Statement.** Every lattice sphere packing in dimension 16 has density at most **0.0172314323416**
(equivalently γ₁₆ ≤ 2.88496372280). The Barnes–Wall lattice has density 0.0147081…, so the bound is about 1.172
times the best known lattice.

**Status: the last stage can be re-run with the check kit.** The bound was obtained on 11 November 2026 as the output
of a chain of exact certificates whose files live in two working trees outside this repository. The check kit is
published as the release [`dim16-check-kit-v6`](https://github.com/AstroNinja389/sphere-packings/releases/tag/dim16-check-kit-v6):
one zip file of 676 MB, holding 12,191 files (2.6 GB unpacked). They are the 10,005 files the final audit bound and
2,186 further files that the last stage reads. One command (`python n16kit.py all C:\n16check`; Windows, Python 3 with
mpmath, numpy, scipy, sympy and python-flint, and PARI/GP) checks every hash, writes a runnable copy, re-runs the last
stage (both branches and the final audit, about an hour on one core) and compares every output with the stored one.
The kit's README says what this does not re-compute: about 36 hours of earlier audits that are only hash-checked, the
60 theorem notes, and results from outside. Two automated checkers that had nothing but the kit ran earlier versions
of it (the same files, with an older tool) from a fresh copy and got the same bound; the published version fixes what
they found.

In the kit the machine paths of the original files are replaced by neutral ones, and the hashes the files record of
each other are recomputed accordingly. The hash lists in `outputs/` here are those of the original files: for 7,460 of
the 10,005 bound files they differ from the kit's. The kit's `verify` confirms 3,006 of the published hashes (2,545
files are unchanged, and 461 give their published hash when the published hashes are put back in place of the
recomputed ones); the other 6,999 files contain a machine path and cannot be compared without the original files.
`SHA256SUMS-CHECK-KIT-v6.txt` gives the SHA-256 of the archive and of the files at the top of the kit.

## What is here

- `documents/RESULT-20261111-GROUPFLOOR-v1.txt` – the result note written when the chain passed: branches, what
  changed in the last step, checks passed, caveats. Copied verbatim.
- `documents/GROUPED-FLOOR-THEOREM-v1.txt` – the lemma behind the last step. Copied verbatim.
- `outputs/union-summary.json` – the headline fields of the final union audit.
- `outputs/union-integrity.json.gz`, `low-integrity.json.gz`, `high-integrity.json.gz` – the final audit outputs of
  the union and of the two branches, including the full list of bound files and hashes. The only change from the
  originals is that the two working-tree prefixes are replaced by `<TREE-A>` and `<TREE-B>`; `PROVENANCE.json`
  gives the SHA-256 of each original and of each scrubbed text.
- `SHA256SUMS-CHECK-KIT-v6.txt` – the SHA-256 of the check-kit archive `n16-check-kit-v6.zip` and of the files at
  the top of the kit (the kit's README says how to use them).
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
