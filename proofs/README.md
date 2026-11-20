# Verifying the lattice density bounds

The [full comparison](COMPARISON.md) covers dimensions 13–48. The two certificate archives can be checked offline with Python assertions enabled. The archive sizes and SHA-256 digests are recorded in [archives.json](archives.json). Dimension 13 uses the previously established general-packing upper and the K₁₃ lattice lower. The other percentages use the lattice comparisons from one [pinned SpherePackings revision](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/LATTICE_RESULTS.json).

Run `python -B proofs/check_tables.py` from the repository root to check all 36 displayed bounds, the comparison arithmetic, the open-family count and the archive digests. This quick check uses only the Python standard library. The publication replay records which arithmetic and geometric checks were run from the public files. [Publication replay](audits/PUBLICATION-REPLAY.json)

The catalogue names each cited theorem or geometric lemma under `proof_inputs`. Replay notes say which files are available and which checks were performed. A length or determinant range identifies one case of a proof. The final bound covers every range when the proof also establishes the complementary case. An **open target** still lacks a proof for some of its cases. [Earlier proofs and their inputs](../EARLIER-CERTIFICATES.md)

## Dimensions 13 and 14

Both deductions use the sharp rank-12 Gram determinant floor **729 at minimum squared length four**, including the classification and finite computations of Géraud-Stewart and Naccache. Mordell's inequality gives the published dimension-13 upper **0.042023513562578**. The proposed **0.041382759430854** still has **15 open families**. Each family can contain a continuum of metrics and gluing choices. The dimension-14 proof uses the same rank-12 floor to control primitive sections and combines both determinant ranges to give **0.03399687961750058**. [External rank-12 theorem](https://eprint.iacr.org/2026/2825) · [Section proof and dimension-13 replay](../sections/README.md) · [17 additional whole-family exclusions](../sections/n13/CONTACT-PRICES.md) · [Exact replay and negative controls](audits/N13-CONTACT-PRICES.json) · [Dimension-14 matching argument](../sections/n14/MATCHING.md)

From the repository root, run the full dimension-14 verifier with the dependencies listed in [sections/requirements.txt](../sections/requirements.txt).

```sh
python -B sections/replay14.py
```

## Dimensions 15 and 17–23

Start in a clone of this repository. The checker extracts the [certificate archive](native-proofs.zip) into a temporary directory and uses the earlier verifier modules in the clone. The full replay uses Python 3.11 or later, python-flint, NumPy, SciPy, SymPy and mpmath. The default command recomputes the two original integer budgets, compares every anchor maximum, and checks the selected final Fourier and population bound. For the three repriced dimensions it also verifies the per-anchor coefficient data. The temporary directory is discarded on exit.

```sh
python -B proofs/replay_native.py
python -B proofs/replay_native.py 19
python -B proofs/replay_native.py --final-only 15 22 23
```

The last command uses the saved original census receipts. In both replay modes, the earlier geometric classifications enter as inputs. The archive supplies their proof notes and finite witnesses. Dimension 15 uses the earlier frame-based upper **0.034607876755962** in dimension 14. That proof uses a finite residue calculation for a full frame. Dimension 17 uses a separate rank-16 Fourier estimate. Dimension 19 requires a complementary determinant case even though the final Fourier transform is nonnegative everywhere. [Population argument](notes/PROFILE-LIFT.md) · [Original census audit](audits/NATIVE-ALL-BRANCHES-REVIEW.json) · [Final certificate audit](audits/NATIVE-FINAL-AUDIT.json)

## Dimensions 16 and 24

Dimension 16 carries forward **0.0172314323416**. The existing proof depends on certificate files outside this repository. Dimension 24 records the exact classical density **π¹²/12!** of the Leech lattice. [Dimension-16 proof status](../dim16/README.md) · [Dimension-24 theorem](https://arxiv.org/abs/1603.06518)

## Dimensions 25–48

Download and extract the [offline proof archive](n25-48-proofs-r9.zip) into a short path. From the extracted directory, run either command with Python 3.11 or later, NumPy and python-flint.

```sh
python -B verify.py
python -B verify.py 32 48
```

The verifier checks its input manifest, the spatial and Fourier signs, the parity-class counts, and the refinements selected for each dimension. It works with rational coefficients and uses directed enclosures for transcendental quantities. The final archive incorporates a complete ordinary replay and supplemental checks on the final improvements. The standalone command recomputes the prerequisites from the packaged inputs. [Exact bounds by dimension](bounds-25-48.json) · [Final audit](audits/FINAL-OFFLINE-AUDIT.json) · [Extracted-archive check](audits/ZIP-CLEAN-REPLAY.json)

The complete ordinary run and the supplemental run each have a preserved transcript. A separate check doubled three claimed improvements and confirmed that the verifier rejects them. [Ordinary run](audits/VERIFIED-RELEASE-FULL-REPLAY.log) · [Supplemental run](audits/r9-incremental-full-domain.log) · [Negative controls](audits/NEGATIVE-CONTROL-AUDIT.json)

Short vectors spanning a lattice plane provide one of the strongest constraints. With minimum squared length one, at most three opposite pairs in a plane can have squared length strictly below two. When three pairs occur, their individual lengths determine their angles. This supplies an inequality on the same vector population used by the Fourier bound. A kernel constructed in dimension 28 also works in dimensions 26 and 27. [Plane argument](notes/PLANE-SUPPORT-TWO.md) · [Length-dependent kernels](notes/EXTENDED-RADIAL-FEATURES.md) · [Parity and Fourier proof](notes/PROOF-parity-Fourier.md)

The archive contains numerical certificate inputs from the pinned SpherePackings repository, with their pinned hashes and provenance. The offline checkers verify the inequalities used from those inputs. [Upstream lattice certificates](https://github.com/alexlegeartis/SpherePackings/tree/9a9851887da20ca75825342bfb09e8ab031f4153/verifications/lattice)
