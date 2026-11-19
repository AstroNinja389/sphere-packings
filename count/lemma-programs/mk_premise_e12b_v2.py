"""Write ELEVEN-PAIRS-PREMISE-n12-S3_4-v1.txt (2026-11-18): the eleven-pair floor of excess 3/4 in dimension 12. Written only
if every computational input is complete: determinant lemma log (v2 program), odd-order log, the bookkeeping of the two
two-class tables (COMPLETE), and the numerical conditions (checked here with mpmath intervals).
Proof scheme of ../n12-eleven-pairs-20261118/mk_premise_e12_v3.py (excess 1/2) with range 3/8; the case of index 2 uses a
two-class table with the character sum instead of the one-class table."""
import json, hashlib
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp
from mpmath import iv
iv.dps = 50; mp.mp.dps = 50
H = Path(__file__).resolve().parent; NL = chr(10)
B11 = '0.094565500874952'; C = F(13, 200); S0 = F(3, 4); D0 = F(3, 8); A1 = F(129, 5000); B1 = F(129, 1250); A2 = F(129, 1250); B2 = F(258, 625)
assert S0 == 2*D0 and B1 == 4*A1 and A2 == 4*A1 and B2 == 16*A1
TA = 'FU2-BOOKKEEPING-N11-D3_8-A129_5000-B129_1250-T-111_10.json'; TB = 'FU2-BOOKKEEPING-N11-D3_8-A129_1250-B258_625-T-3.json'
assert 'DETERMINANT LEMMA n = 11, sum of positive excess <= 3/8: PASS' in (H/'check-det-n-v2-N11-D3_8.log').read_text()
assert 'RESULT PASS n 11 D 3/8 primes [3, 5]' in (H/'check-odd-order-v1-N11-D3_8.log').read_text()
def load(name, a, b, claim):
    t = json.loads((H/name).read_text())
    assert t['result'] == 'COMPLETE' and not t['problems'] and t['n_rows_not_covered'] == 0 and t['rows'] == 118440, t
    assert t['n'] == 11 and F(t['delta0']) == D0 and F(t['A']) == a and F(t['B']) == b and F(t['claim']) == claim, t
    assert t['certified_rows_confirmed'] + t['empty_rows_confirmed'] + t['rows_needing_cells'] == 118440 and t['largest_rechecked'] is not None and t['cells_confirmed'] == t['rows_needing_cells'], t
    assert t['largest_rechecked'] is None or F(str(t['largest_rechecked'])) < claim
    assert t['largest_rechecked_cells'] is None or F(str(t['largest_rechecked_cells'])) < claim
    return t
ta = load(TA, A1, B1, F(-111, 10)); tb = load(TB, A2, B2, F(-3))
def sha(f): return hashlib.sha256((H/f).read_bytes()).hexdigest()
INPUTS = ['check-det-n-v2-N11-D3_8.log', 'check-odd-order-v1-N11-D3_8.log', TA, TB, 'DETERMINANT-LEMMA-GENERAL-N-v2.txt', 'ODD-ORDER-EXCLUSION-v1.txt', 'SMALL3-BOUND-v1.txt',
          'frame_u2_scheme_s3_v1.py', 'frame_u2_recheck_s3_v1.py']
hashes = NL.join('      %s  %s' % (sha(f), f) for f in INPUTS)
pi = iv.pi
d11 = iv.mpf(2)**6*pi**5/iv.mpf(10395)/iv.mpf(2)**(iv.mpf(13)/2)        # V_11 = 2^6 pi^5/11!!, 11!! = 10395
d12 = pi**6/iv.mpf(720)/iv.mpf(2)**7
x11 = (iv.mpf(F(B11).numerator)/iv.mpf(F(B11).denominator))/d11; top = x11*iv.exp(iv.mpf(3)/16); assert 5 < top.a and top.b < 6
hh = (d12/(iv.mpf(13)/200))**2; assert hh.b < mp.mpf(129)/5000
s3 = F(89, 64); assert 2 - B2 > s3 and 2 - B1 > s3 and 2 - A1 > s3
def _dec(x, k, up):
    x = mp.mpf(x); assert x > 0; e = int(mp.floor(mp.log10(x))); m = x*mp.mpf(10)**(k - 1 - e)
    n_ = int(mp.ceil(m)) if up else int(mp.floor(m)); s_ = str(n_).rjust(k, '0'); p_ = e + 1
    return (s_[:p_] + '.' + s_[p_:]) if p_ > 0 else ('0.' + '0'*(-p_) + s_)
def lo(z, k): return _dec(z.a, k, False)
def hi(z, k): return _dec(z.b, k, True)
def stats(t, tt, ct):
    c = ('no row needed cell mode' if t['rows_needing_cells'] == 0 else
         '%d rows certified in cell mode at %s (subdivision of the cell; all confirmed by the cells re-check, largest re-checked value %.4f)' % (
             t['rows_needing_cells'], ct, t['largest_rechecked_cells']))
    return ('118,440 rows = %d certified below %s in the table and confirmed by the re-check (largest re-checked value %.4f) + %d empty rows confirmed;' % (
                t['certified_rows_confirmed'], tt, t['largest_rechecked'], t['empty_rows_confirmed']) + NL + '      ' + c)
txt = f"""ELEVEN PAIRS OF ONE CLASS IN DIMENSION 12, EXCESS 3/4 (premise of a floor on eleven pairs)          v1, 2026-11-18
=====================================================================================================================
Status: written by one author (Claude) in one session. An automated referee (not a human; folder review-S1) re-derived steps
1-8, the numbers and the proof of (SMALL3), tried to break (SMALL3) numerically, and found no error; it did not check the
tables, the bookkeeping or the cell scheme itself. NOT reviewed by a human. The proof (steps 1-8)
follows ../n12-eleven-pairs-20261118/ELEVEN-PAIRS-PREMISE-n12-v1.txt (excess 1/2; that proof was re-derived by an automated
referee) with range 3/8; step 8 (index 2) is different: it uses a two-class table together with the character sum.
Inputs: the determinant lemma in the form v2, an earlier computer-assisted density bound for dimension 11, the odd-order
lemma (exact finite check), two computer-checked two-class lemmas in eleven coordinates (each re-checked by the second
implementation), and the level limit (SMALL3) of the table programs. By itself it changes no density bound.

STATEMENT.  Let L be a lattice of dimension 12 and minimum squared length 1 with density(L) > 13/200 = 0.065.
Then any eleven distinct pairs +-x_1, ..., +-x_11 of one class modulo 2L, each of squared length < 9/4, satisfy
      sum_i max(|x_i|^2, 2) > 22 + 3/4.

INPUTS.
 (I1) Determinant lemma in eleven coordinates, range 3/8 (DETERMINANT-LEMMA-GENERAL-N-v2.txt; check_det_n_v2.py 11 3/8,
      log check-det-n-v2-N11-D3_8.log).
 (I2) B_11 := {B11}: an upper bound for the density of lattices in dimension 11 that needs no frame premise (certificate
      plus one joint cut; audited value of the 4 November sweep; public repository joint/n11).
 (I3) Lemma O(11, 3/8, p) for p = 3, 5 (ODD-ORDER-EXCLUSION-v1.txt; check-odd-order-v1-N11-D3_8.log: 178/99 and 216/125).
 Setting of (I4), (I5): Q' = I + diag(delta) + E on R^11, delta_i in [0, 1/8], sum delta_i <= 3/8, |E_ij| <= (delta_i + delta_j)/2;
      N(q) := min of Q' over q + D11; psi(q) := sum_i cos 2 pi q_i.
 (I4) LEMMA T2(11; 3/8; 129/5000, 129/1250; -111/10).  N(q) >= 2 - 129/5000 and N(2q) >= 2 - 129/1250 imply psi(q) < -111/10.
      As psi >= -11 always, the two hypotheses cannot hold together.
      Computer check (program frame_u2_scheme_s3_v1.py, FRAME_N = 11, arguments 3/8 129/5000 129/1250 -11.5, two parts;
      re-check frame_u2_recheck_s3_v1.py, two halves; cell mode at -11.2 with its re-check):
      {stats(ta, '-11.5', '-11.2')};
      bookkeeping_fu2_cells_v1.py at -111/10: RESULT COMPLETE ({TA}).
 (I5) LEMMA T2(11; 3/8; 129/1250, 258/625; -3).  N(q) >= 2 - 129/1250 and N(2q) >= 2 - 258/625 imply psi(q) < -3.
      Computer check (same programs, arguments 3/8 129/1250 258/625 -3.2; cell mode at -3.05):
      {stats(tb, '-3.2', '-3.05')};
      bookkeeping_fu2_cells_v1.py at -3: RESULT COMPLETE ({TB}).
 (I6) Level limit of the programs: cells with sum t_i <= 2 are excluded because 2 - level > S3(3/8) = 89/64 = 1.390625
      (SMALL3-BOUND-v1.txt; the least level used here is 2 - 258/625 = 1.5872, which is below the old limit 1.8089 of the
      programs: (I5) is admissible only through (SMALL3); the levels of (I4) pass the old limit too). The programs are the two-class programs of
      the cell scheme (GLUE-INDEX-REDUCTION-v2.txt sections 4, 7 with the bounds (F), (G), (M)) with that one line changed
      (../small3-variants-20261118/make_s3_variants_v1.py).
 Numbers (interval arithmetic in mk_premise_e12b_v2.py): d_n := V_n 2^(-n/2-1); B_11/d_11 in [{lo(x11, 12)}, {hi(x11, 12)}];
      (B_11/d_11) exp(3/16) in [{lo(top, 12)}, {hi(top, 12)}], so below 6;   (d_12/(13/200))^2 <= {hi(hh, 12)} < 129/5000.
 Input files (sha256):
{hashes}

PROOF.  Suppose eleven such pairs have sum_i max(|x_i|^2, 2) <= 22 + 3/4.
 1. d_i := |x_i|^2 - 2 (< 1/4). For i != j the vectors x_i +- x_j are non-zero elements of 2L, so |x_i +- x_j|^2 >= 4:
    d_i + d_j >= 0 and |x_i . x_j| <= (d_i + d_j)/2; at most one d_i is negative. Lambda := sqrt 2 L (minimum 2),
    f_i := x_i/sqrt 2 (i = 1..11); f_i +- f_j is in Lambda, so Gamma := {{sum c_i f_i : c in D11}} is a sublattice of Lambda
    (D11 := the vectors of Z^11 with even coordinate sum). Gram matrix Q = diag(1 + delta_i) + E of the f_i:
    delta_i = d_i/2 <= 1/8, delta_i + delta_j >= 0, |E_ij| <= (delta_i + delta_j)/2, sum_i max(delta_i, 0) <= 3/8.
 2. det Q >= 1 by (I1). So the f_i are independent; V := their span (dimension 11); covol(Gamma) = 2 sqrt(det Q).
    Hadamard: det Q <= prod (1 + delta_i) <= exp(sum max(delta_i, 0)) <= exp(3/8).
 3. M := Lambda n V is a lattice of rank 11 containing Gamma; j := [M : Gamma]. M is an 11-dimensional lattice whose
    minimum is >= 2, so its density is at least V_11 2^(-11/2)/covol(M) = j d_11/sqrt(det Q), and at most B_11 (I2). Hence
          j <= (B_11/d_11) sqrt(det Q) <= (B_11/d_11) exp(3/16) < 6:      j in {{1, 2, 3, 4, 5}}.
 4. G := M/Gamma, written in the coordinates of the f_i, is a subgroup of R^11/D11 of order j; each non-zero class
    consists of non-zero vectors of Lambda, so its least Q-norm is >= 2. If delta_1 = -nu < 0 put Q' := Q + nu e_1 e_1^t,
    otherwise Q' := Q: Q' >= Q, diagonal excesses max(delta_i, 0) in [0, 1/8] with sum <= 3/8, |E_1j| <= (delta_j - nu)/2
    <= delta_j/2, the cap of Q'; least Q'-norms are >= least Q-norms. Write N for the least Q'-norm of a class modulo D11,
    and from here on delta_i for the diagonal excess of Q', i.e. max(delta_i, 0).
    (a) j is not 3 and not 5: by Cauchy's theorem G would have an element of order 3 or 5, against (I3).
    (b) j is not 4. A group of order 4 is Z/2 x Z/2 or Z/4.
        Elements of order 2: g with 2g in D11. g is not integral (its class would contain a unit vector e_i, of Q'-norm
        1 + delta_i < 2). So g = c/2 modulo Z^11 for a non-zero 0/1 word c, of even weight w (the coordinate sum of 2g is
        even). The vectors with entries +-1/2 on the support of c, 0 elsewhere, and a fixed parity of the number of minus
        signs lie in the class; for w >= 4 their signs are pairwise uncorrelated under the uniform distribution, so the
        shortest has Q'-norm <= sum_(supp c) (1 + delta_i)/4 <= (w + 3/8)/4 < 2 for w <= 6; for w = 2 any of them has
        Q'-norm <= (2 + delta_a + delta_b)/4 + (delta_a + delta_b)/4 <= 5/8 < 2. Hence w is 8 or 10.
        Z/2 x Z/2: words c, c' and c + c' (modulo 2), all of weight >= 8 in length 11: |c n c'| >= 8 + 8 - 11 = 5, so
        the weight of c + c' is |c u c'| - |c n c'| <= 11 - 5 = 6. Impossible (also if c = c': then the third element is
        integral and non-zero, which was excluded above).
        Z/4: g of order 4, 2g = c/2 modulo Z^11 with c of weight w in {{8, 10}}. So g has entries +-1/4 (modulo 1) on the
        support of c and 0 or 1/2 (modulo 1) elsewhere; b := number of entries 1/2, b <= 11 - w.
        For every real vector u:  Q'(u) <= |u|^2 + |u|_1 sum_a delta_a |u_a| <= |u|^2 + (3/8) |u|_1 |u|_inf      (X)
        ((X) of ODD-ORDER-EXCLUSION-v1.txt). If b >= 1, the class contains a vector u with entries +-1/4 on supp c,
        +-1/2 on the b places and 0 elsewhere (the sign of one entry 1/2 adjusts the parity of the integer part):
        |u|^2 = w/16 + b/4 <= 5/4, |u|_1 = w/4 + b/2 <= 7/2, |u|_inf = 1/2, so N(g) <= 5/4 + 21/32 = 61/32 < 2.
        If b = 0, the class contains a vector with entries +-1/4 on supp c except possibly one entry +-3/4, 0 elsewhere:
        |u|^2 <= w/16 + 1/2 <= 9/8, |u|_1 <= w/4 + 1/2 <= 3, |u|_inf <= 3/4, so N(g) <= 9/8 + 27/32 = 63/32 < 2. Impossible.
    So j is 1 or 2.
 5. Lambda/M is infinite cyclic (M = Lambda n V). Let w0 = p^ + h u0 generate it, u0 the unit normal of V, h > 0, p^ in V
    with coordinate vector p in R^11. covol(Lambda) = covol(M) h = 2 sqrt(det Q) h/j, so
          density(L) = V_12 2^(-6)/covol(Lambda) = j d_12/(h sqrt(det Q)).
    density(L) > 13/200 and det Q >= 1 give h < j d_12/(13/200), i.e. h^2 < j^2 * 129/5000.
 6. For k in {{1, 2}} and every m in M the vector k w0 + m is a non-zero vector of Lambda (its component along u0 is k h),
    so Q(k p + m) + k^2 h^2 >= 2. Hence for every class g of G:  N(k p + g) >= 2 - k^2 h^2  (least Q-norm, a fortiori
    least Q'-norm, over k p + g + D11).
 7. j = 1.  q := p has N(q) >= 2 - h^2 > 2 - 129/5000 and N(2q) >= 2 - 4 h^2 > 2 - 129/1250 (step 6 with k = 1, 2 and the
    zero class). By (I4) psi(q) < -111/10 < -11 <= psi(q). Contradiction.
 8. j = 2.  G = {{0, g0}}, g0 = c/2 modulo Z^11 with c of weight w in {{8, 10}} (step 4(b)); z := 11 - w <= 3 coordinates lie
    outside the support. Here h^2 < 4 * 129/5000 = 129/1250. For q1 := p and q2 := p + g0:
          psi(q1) + psi(q2) = sum_i [cos 2 pi p_i + cos 2 pi (p_i + c_i/2)] = 2 sum_(i outside supp c) cos 2 pi p_i >= -2z >= -6,
    so some q in {{q1, q2}} has psi(q) >= -3. By step 6 with k = 1 (classes 0 and g0), N(q) >= 2 - h^2 > 2 - 129/1250.
    Moreover 2 q2 = 2p + 2 g0 with 2 g0 in D11, so 2q = 2p modulo D11 for both, and by step 6 with k = 2 and the zero class
    N(2q) = N(2p) >= 2 - 4 h^2 > 2 - 16 * 129/5000 = 2 - 258/625. By (I5) psi(q) < -3. Contradiction.          QED

USE.  Floor on COUNT = 11 pairs in the class budget of dimension 12 (audit_count_bound_v1.py: count 11, S0 = 3/4,
T = 9/4, complement 0.065). The audited density is a bound for lattices denser than 0.065; the final bound is the maximum.
A class with twelve such pairs contains eleven, so the frame case is included.
Thin places: (d_12/(13/200))^2 = 0.02576 against 129/5000 = 0.0258; 63/32 against 2 in step 4(b).
WHAT THE RESULT IS CONDITIONAL ON: (I1) in the form v2, (I4), (I5), (I6) (computer-checked, project programs and notes, not
reviewed), (I3) (elementary, exact finite check), (I2) (exact audit of 4 November), and the soundness of the audit program.
"""
out = H/'ELEVEN-PAIRS-PREMISE-n12-S3_4-v1.txt'; assert not out.exists(); out.write_text(txt, encoding='utf-8', newline=NL); print('written', out.name)
