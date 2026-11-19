"""Write TEN-PAIRS-PREMISE-n11-v1.txt (2026-11-18): the ten-pair floor of excess 3/4 in dimension 11. The file is written only
if every computational input is complete: determinant lemma log (v2 program), odd-order log, two-class bookkeeping
(COMPLETE), one-class bookkeeping (COMPLETE), and the numerical conditions (checked here with mpmath intervals).
Adapted from ../n12-eleven-pairs-20261118/mk_premise_e12_v3.py (same proof scheme, ten coordinates, range 3/8, index <= 3)."""
import json, sys, hashlib
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
from mpmath import iv
iv.dps = 50; mp.mp.dps = 50
H = Path(__file__).resolve().parent; NL = chr(10)
B10 = '0.13010849917496'; C = F(181, 2000); S0 = F(3, 4); D0 = F(3, 8); A1 = F(53, 1000); B1 = F(53, 250); A2 = F(53, 250)
T2NAME = 'FU2-BOOKKEEPING-N10-D3_8-A53_1000-B53_250-T-21_2.json'; U1NAME = 'FU1-BOOKKEEPING-N10-D3_8-A53_250-T-2.json'
assert 'DETERMINANT LEMMA n = 10, sum of positive excess <= 3/8: PASS' in (H/'check-det-n-v2-N10-D3_8.log').read_text()
assert 'RESULT PASS n 10 D 3/8 primes [3]' in (H/'check-odd-order-v1-N10-D3_8.log').read_text()
t2 = json.loads((H/T2NAME).read_text()); assert t2['result'] == 'COMPLETE' and F(t2['claim']) == F(-21, 2) and t2['rows'] == 118440, t2
assert t2['n'] == 10 and F(t2['delta0']) == D0 and F(t2['A']) == A1 and F(t2['B']) == B1 and t2['rows_left_to_cells'] == 0 and not t2['problems'], t2
u1 = json.loads((H/U1NAME).read_text()); assert u1['result'] == 'COMPLETE' and F(u1['target']) == -2 and not u1['pairs_not_covered'], u1
assert u1['n'] == 10 and F(u1['delta0']) == D0 and F(u1['A']) == A2 and not u1['problems'], u1
assert u1['cells_confirmed'] == u1['pairs_needing_cells'] and (u1['pairs_needing_cells'] == 0 or u1['largest_rechecked_cells'] < -2), u1
assert u1['largest_rechecked_table'] < -2.2 and t2['largest_rechecked'] < -10.5 and u1['pairs'] == 13160
assert C == F(181, 2000) and S0 == 2*D0 and A2 == 4*A1 == B1
def sha(f): return hashlib.sha256((H/f).read_bytes()).hexdigest()
INPUTS = ['check-det-n-v2-N10-D3_8.log', 'check-odd-order-v1-N10-D3_8.log', T2NAME, U1NAME, 'DETERMINANT-LEMMA-GENERAL-N-v2.txt', 'ODD-ORDER-EXCLUSION-v1.txt']
hashes = NL.join('      %s  %s' % (sha(f), f) for f in INPUTS)
pi = iv.pi
d10 = pi**5/iv.mpf(120)/iv.mpf(2)**6                                      # V_10 = pi^5/120
d11 = iv.mpf(2)**6*pi**5/iv.mpf(10395)/iv.mpf(2)**(iv.mpf(13)/2)        # V_11 = 2^6 pi^5/11!!, 11!! = 10395
x10 = (iv.mpf(F(B10).numerator)/iv.mpf(F(B10).denominator))/d10; top = x10*iv.exp(iv.mpf(3)/16); assert 3 < top.a and top.b < 4
hh = (d11/(iv.mpf(181)/2000))**2; assert hh.b < mp.mpf(53)/1000 and 4*hh.b < mp.mpf(53)/250
def _dec(x, k, up):
    x = mp.mpf(x); assert x > 0; e = int(mp.floor(mp.log10(x))); m = x*mp.mpf(10)**(k - 1 - e)
    n_ = int(mp.ceil(m)) if up else int(mp.floor(m)); s_ = str(n_).rjust(k, '0'); p_ = e + 1
    return (s_[:p_] + '.' + s_[p_:]) if p_ > 0 else ('0.' + '0'*(-p_) + s_)
def lo(z, k): return _dec(z.a, k, False)
def hi(z, k): return _dec(z.b, k, True)
cells_txt = ('no pair needed cell mode' if u1['pairs_needing_cells'] == 0 else
             '%d pairs certified in cell mode at -2.05 (subdivision of the cell; %d confirmed, largest re-checked value %.4f)' % (
                 u1['pairs_needing_cells'], u1['cells_confirmed'], u1['largest_rechecked_cells']))
txt = f"""TEN PAIRS OF ONE CLASS IN DIMENSION 11, EXCESS 3/4 (premise of a floor on ten pairs)                 v1, 2026-11-18
=====================================================================================================================
Status: written by one author (Claude) in one session. The proof (steps 1-8) is the proof of
../n12-eleven-pairs-20261118/ELEVEN-PAIRS-PREMISE-n12-v1.txt with ten coordinates, range 3/8 and index at most 3 (that
proof was re-derived by an automated referee, folder review-E1 there). An automated referee (not a human; folder review-T1)
re-derived steps 1-8 of THIS text, the numbers, the change in the determinant lemma and the odd-order instance, and found
no error; it did not check the tables. NOT reviewed by a human. It uses five inputs listed below: the determinant lemma in the form v2 (wider range; the change against
the reviewed v1 is not reviewed), an earlier computer-assisted density bound for dimension 10, the odd-order lemma
(exact finite check), and two computer-checked lemmas in ten coordinates (a two-class table and a one-class table of the
cell scheme, each re-checked by the second implementation). By itself it changes no density bound.

STATEMENT.  Let L be a lattice of dimension 11 and minimum squared length 1 with density(L) > 181/2000 = 0.0905.
Then any ten distinct pairs +-x_1, ..., +-x_10 of one class modulo 2L, each of squared length < 9/4, satisfy
      sum_i max(|x_i|^2, 2) > 20 + 3/4.

INPUTS.
 (I1) Determinant lemma in ten coordinates, range 3/8 (DETERMINANT-LEMMA-GENERAL-N-v2.txt; check_det_n_v2.py 10 3/8,
      log check-det-n-v2-N10-D3_8.log).
 (I2) B_10 := {B10}: an upper bound for the density of lattices in dimension 10 that needs no frame premise (certificate
      plus joint cuts; audited value of the 4 November sweep, SWEEP-SUMMARY-v3.json, n = 10).
 (I3) Lemma O(10, 3/8, 3) (ODD-ORDER-EXCLUSION-v1.txt; check-odd-order-v1-N10-D3_8.log: 55/36).
 (I4) LEMMA T2(10; 3/8; 53/1000, 53/250).  For Q' = I + diag(delta) + E on R^10, delta_i in [0, 1/8], sum delta_i <= 3/8,
      |E_ij| <= (delta_i + delta_j)/2:   N(q) >= 2 - 53/1000 and N(2q) >= 2 - 53/250 imply psi(q) < -21/2,
      where N(q) := min of Q' over q + D10 and psi(q) := sum_i cos 2 pi q_i. As psi >= -10 always, the two hypotheses
      cannot hold together.
      Computer check (two-class cell scheme of GLUE-INDEX-REDUCTION-v2.txt sections 4, 7 with the bounds (F), (G), (M); program
      frame_u2_scheme_n10_v1.py with FRAME_N = 10, arguments 3/8 53/1000 53/250 -10.5, two parts): 118,440 rows =
      {t2['certified_rows_confirmed']} certified below -21/2 (largest stored value {t2['largest_stored_certified']:.4f}) + {t2['empty_rows_confirmed']} empty + 0 left to cells;
      re-check frame_u2_recheck_n10_v1.py (second implementation, ball arithmetic), two halves: every certified row
      confirmed (largest re-checked value {t2['largest_rechecked']:.4f}), every empty row confirmed empty;
      bookkeeping_fu2_full_v2.py: RESULT COMPLETE ({T2NAME}).
 (I5) LEMMA U(10; 3/8; 53/250).  For Q' as in (I4):   N(q) >= 2 - 53/250 implies psi(q) < -2.
      Computer check (one-class scheme, frame_u_scheme_n10_v1.py 10 3/8 53/250 -2.2): 13,160 pairs = {u1['certified_rows_confirmed']} table rows certified
      below -2.2 and confirmed by the second implementation frame_u_recheck_n10_v1.py (largest re-checked value {u1['largest_rechecked_table']:.4f}) + {u1['empty_rows_confirmed']}
      empty rows confirmed; {cells_txt};
      bookkeeping_fu_v2.py at -2: RESULT COMPLETE ({U1NAME}).
 The programs for ten coordinates are the programs for N coordinates with the grids for Y = sum t_i ending 9/2, 19/4, 5 and,
      for 2q, 4, 9/2, 5 (for N = 10 the last two points of the standard grids coincide; the grids are data of the scheme;
      generators ../n10-frame-floor-20261118/make_n10_variants_v1.py and
      ../n11-ten-pairs-PREPARED-20261118/make_n10_u2_variants_v1.py). The level limit of the scheme, (SMALL') for N = 10 and
      range 3/8, is 1 + (3/8)(4/5)(13/5) = 1.78 < 2 - 53/250 = 1.788.
 Numbers (interval arithmetic in mk_premise_t11_v2.py): d_n := V_n 2^(-n/2-1); B_10/d_10 in [{lo(x10, 12)}, {hi(x10, 12)}];
      (B_10/d_10) exp(3/16) in [{lo(top, 12)}, {hi(top, 12)}], so below 4;   (d_11/(181/2000))^2 <= {hi(hh, 12)} < 53/1000.
      Thin places: 0.05291 against 0.053 (the complement 181/2000 fixes the levels); 3.939 against 4 (index bound);
      1.78 against 1.788 (level limit of the scheme).
 Input files (sha256):
{hashes}

PROOF.  Suppose ten such pairs have sum_i max(|x_i|^2, 2) <= 20 + 3/4.
 1. d_i := |x_i|^2 - 2 (< 1/4). For i != j the vectors x_i +- x_j are non-zero elements of 2L, so |x_i +- x_j|^2 >= 4:
    d_i + d_j >= 0 and |x_i . x_j| <= (d_i + d_j)/2; at most one d_i is negative. Lambda := sqrt 2 L (minimum 2),
    f_i := x_i/sqrt 2 (i = 1..10); f_i +- f_j is in Lambda, so Gamma := {{sum c_i f_i : c in D10}} is a sublattice of Lambda
    (D10 := the vectors of Z^10 with even coordinate sum). Gram matrix Q = diag(1 + delta_i) + E of the f_i:
    delta_i = d_i/2 <= 1/8, delta_i + delta_j >= 0, |E_ij| <= (delta_i + delta_j)/2, sum_i max(delta_i, 0) <= 3/8.
 2. det Q >= 1 by (I1). So the f_i are independent; V := their span (dimension 10); covol(Gamma) = 2 sqrt(det Q).
    Hadamard: det Q <= prod (1 + delta_i) <= exp(sum max(delta_i, 0)) <= exp(3/8).
 3. M := Lambda n V is a lattice of rank 10 containing Gamma; j := [M : Gamma]. M is a 10-dimensional lattice whose
    minimum is >= 2, so its density is at least V_10 2^(-5)/covol(M) = j d_10/sqrt(det Q), and at most B_10 (I2). Hence
          j <= (B_10/d_10) sqrt(det Q) <= (B_10/d_10) exp(3/16) < 4:      j in {{1, 2, 3}}.
 4. G := M/Gamma, written in the coordinates of the f_i, is a subgroup of R^10/D10 of order j; each non-zero class
    consists of non-zero vectors of Lambda, so its least Q-norm is >= 2. If delta_1 = -nu < 0 put Q' := Q + nu e_1 e_1^t,
    otherwise Q' := Q: Q' >= Q, diagonal excesses max(delta_i, 0) in [0, 1/8] with sum <= 3/8, |E_1j| <= (delta_j - nu)/2
    <= delta_j/2, the cap of Q'; least Q'-norms are >= least Q-norms. Write N for the least Q'-norm of a class modulo D10,
    and from here on delta_i for the diagonal excess of Q', i.e. max(delta_i, 0).
    (a) j is not 3: a group of order 3 has an element of order 3, against (I3). So j is 1 or 2.
    (b) If j = 2: G = {{0, g0}} with 2 g0 in D10. g0 is not integral (its class would contain a unit vector e_i, of Q'-norm
        1 + delta_i < 2). So g0 = c/2 modulo Z^10 for a non-zero 0/1 word c, of even weight w (the coordinate sum of 2 g0
        is even). The vectors with entries +-1/2 on the support of c, 0 elsewhere, and a fixed parity of the number of
        minus signs lie in the class; for w >= 4 their signs are pairwise uncorrelated under the uniform distribution, so
        the shortest has Q'-norm <= sum_(supp c) (1 + delta_i)/4 <= (w + 3/8)/4 < 2 for w <= 6; for w = 2 any of them has
        Q'-norm <= (2 + delta_a + delta_b)/4 + (delta_a + delta_b)/4 <= 5/8 < 2. Hence w is 8 or 10.
 5. Lambda/M is infinite cyclic (M = Lambda n V). Let w0 = p^ + h u0 generate it, u0 the unit normal of V, h > 0, p^ in V
    with coordinate vector p in R^10. covol(Lambda) = covol(M) h = 2 sqrt(det Q) h/j, so
          density(L) = V_11 2^(-11/2)/covol(Lambda) = j d_11/(h sqrt(det Q)).
    density(L) > 181/2000 and det Q >= 1 give h < j d_11/(181/2000), i.e. h^2 < j^2 * 53/1000.
 6. For k in {{1, 2}} and every m in M the vector k w0 + m is a non-zero vector of Lambda (its component along u0 is k h),
    so Q(k p + m) + k^2 h^2 >= 2. Hence for every class g of G:  N(k p + g) >= 2 - k^2 h^2  (least Q-norm, a fortiori
    least Q'-norm, over k p + g + D10).
 7. j = 1.  q := p has N(q) >= 2 - h^2 > 2 - 53/1000 and N(2q) >= 2 - 4 h^2 > 2 - 53/250 (step 6 with k = 1, 2 and the
    zero class). By (I4) psi(q) < -21/2 < -10 <= psi(q).
    Contradiction.
 8. j = 2.  z := 10 - w <= 2 coordinates lie outside the support of c (step 4(b)). For q1 := p and q2 := p + g0:
          psi(q1) + psi(q2) = sum_i [cos 2 pi p_i + cos 2 pi (p_i + c_i/2)] = 2 sum_(i outside supp c) cos 2 pi p_i >= -2z >= -4,
    so some q in {{q1, q2}} has psi(q) >= -2. By step 6, N(q) >= 2 - h^2 > 2 - 4 * 53/1000 = 2 - 53/250. By (I5) psi(q) < -2.
    Contradiction.                                                                                              QED

USE.  Floor on COUNT = 10 pairs in the class budget of dimension 11 (audit_count_bound_v1.py: count 10, S0 = 3/4,
T = 9/4, complement 0.0905). The audited density is a bound for lattices denser than 0.0905; the final bound is the maximum.
A class with eleven such pairs contains ten, so the frame case is included.
WHAT THE RESULT IS CONDITIONAL ON: (I1) in the form v2, (I4), (I5) (computer-checked, project programs, not reviewed),
(I3) (elementary, exact finite check, automated review of the lemma), (I2) (exact audit of 4 November), and the
soundness of the audit program.
"""
out = H/'TEN-PAIRS-PREMISE-n11-v1.txt'; assert not out.exists(); out.write_text(txt, encoding='utf-8', newline=NL); print('written', out.name)
