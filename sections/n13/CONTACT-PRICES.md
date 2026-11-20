# Seventeen whole families excluded in dimension 13

At the proposed density upper of **0.041382759430854**, the previous descent left 32 possible rank-nine markings. This check excludes 17 over their entire parameter ranges. **Fifteen remain**, comprising ten exceptional markings and five tree markings. The upper for all dimension-13 lattices is still **0.042023513562578** from Mordell and the rank-12 theorem. [Previous 32 markings](FINAL-OPEN-MARKS.txt) · [Current 15 markings](OPEN-AFTER-CONTACT-PRICES.txt) · [Descent and rank-12 input](SECTION-TRANSFER.md)

Let $Q$ be the actual Gram matrix of the rank-nine section, $T=Q^{-1}$, and $u$ the squared minimum of the balanced rank-ten dual. On an interval of $u$, the descent gives a rational ceiling $e_0$ for $\det Q$. The marking theorem writes $T=\sum_x w_x xx^t$ over the integral minimum pairs of the reference form. Each $w_x$ lies in $[0,1/4]$, and $\sum w_x\le9/4$. The individual bound follows from $T\succeq w_xxx^t$ and $x^tQx\ge4$. The verifier enumerates all minimum pairs of the reference form exactly. [Marking and interval inequalities](INTERVALS.md)

**One test serves all 17 markings.** Collect lower bounds $\mathrm{tr}(A_jT)\ge b_j$ valid for the same metric and lifts. Choose nonnegative rational weights $\lambda_j$, set $A=\sum_j\lambda_j A_j$, and $b=\sum_j\lambda_j b_j$. Then

$$
4b\le 4\mathrm{tr}(AT)=\sum_x 4w_x\,x^tAx
\le \text{sum of the nine largest positive parts of }x^tAx.
$$

The last step uses $4w_x\le1$ and $\sum_x4w_x\le9$. A certificate makes the last quantity strictly smaller than $4b$. This excludes every choice of section metric and gluing in that interval.

**Where the lower bounds come from.** Reciprocal integer directions give individual length bounds. Signed triples give a joint bound, and pairs spanning a plane give area bounds. For rational positive definite $S$ and nonzero integral $x$, put $V=S-Sxx^tS/(x^tSx)$. The eight nonzero eigenvalues of $T^{1/2}VT^{1/2}$ have product $\det S\,\det T\,(x^tQx)/(x^tSx)$. Their arithmetic mean gives $\mathrm{tr}(VT)\ge8(4\det S/(e_0 x^tSx))^{1/8}$. The verifier checks each proposed rational lower bound by raising it to the eighth power. [Cofactor proof](COFACTOR.md)

**Why common gluing helps.** Every reciprocal direction $z$ has a circle phase $\chi(z)$ from its lift to the rank-ten dual, and $T[z]\ge u(1-\lVert\chi(z)\rVert^2)$, where the norm denotes distance to the nearest integer. After orienting a signed triple so $z_1+z_2+z_3=0$, its phases are differences between three points on a circle of circumference one. At least one circular gap is at most $1/3$, so one of these directions has $T[z_i]\ge8u/9$. The verifier checks all three choices wherever it uses this split. Two of the 17 saved family proofs use the split. The other certificates close with the weighted inequalities alone.

The public file contains 60 rational weighted contradictions and 39 intervals already empty by scalar inequalities. The verifier also replays the earlier cell and plane proofs covering the initial part of each family's range. The balancing inequality $768u^5\le1024$ controls the remaining tail. The floating-point search supplied candidate rational weights. Every inequality, strict separation and interval endpoint in the published proof is checked using integer or rational arithmetic. [Certificate data](contact-prices.jsonl) · [Exact verifier](audit_contact_prices.py)

From the repository root, run the following with the extracted rank-eleven certificate database. Omit `--contact-prices-only` to replay the earlier descent as well. [Database source](https://doi.org/10.5281/zenodo.23979316)

```sh
python -B sections/replay13.py --database /path/to/k11_certificates_v3.sqlite --contact-prices-only
```
