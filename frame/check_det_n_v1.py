"""DETERMINANT LEMMA IN DIMENSION n: machine check of the last step (2026-11-18, v1).  mpmath intervals, 40 digits.

Setting. delta in R^n, delta_i <= 1/8, delta_i + delta_j >= 0 (so at most one entry is negative), D+ := sum of the
positive entries <= DELTA0; Q = I + diag(delta) + E, E symmetric with zero diagonal, |E_ij| <= (delta_i + delta_j)/2.
Claim: det Q >= 1.
Proof steps 1 and 2 are those of ../n16-fifteen-frame-theorem-20261112/DETERMINANT-LEMMA-v1.txt with 15 replaced by n:
 Step 1 (comparison with E = -cap) needs the row margins (1 + delta_i) - sum_{j != i} cap_ij
        = 1 - Delta/2 - ((n-4)/2) delta_i > 0,  Delta = sum delta_i;
        for delta_i <= 1/8 and Delta <= DELTA0 this is >= 1 - DELTA0/2 - (n-4)/16   (CHECK 1; for a negative
        delta_i the margin is larger).
 Step 2 gives det Q >= Phi_n(delta) = prod (1 + 2 delta_i) * [ (1 - Delta/2)^2 - gamma ((n-8)/4 + Delta/2) ],
        gamma = sum delta_i^2/(1 + 2 delta_i)   (the rank-two determinant identity with beta' = n - 2 alpha).
 Step 3 (checked here). Write nu >= 0 for minus the negative entry (nu = 0 if none); then every other entry is >= nu,
        so (n-1) nu <= D+, and Delta = D+ - nu.  With ln(1+t) >= t - (27/50) t^2/(1+t) on [-3/52, 1/4]  (CHECK D2 of
        the lemma file; needs nu <= 3/104, CHECK 2):   ln prod(1 + 2 delta_i) >= 2 Delta - (54/25) gamma.
        gamma <= D+/10 + nu^2/(1 - 2 nu)   (delta^2/(1+2 delta) <= delta/10 on [0, 1/8]).
        Bracket: B = 1 - x,  x := Delta - Delta^2/4 + gamma ((n-8)/4 + Delta/2);  if 0 <= x <= 1/2 then
        ln(1 - x) >= -x - x^2.  Hence  ln det Q >= 2 Delta - (54/25) g - x - x^2  with g the upper bound of gamma,
        which is decreasing in gamma, so g may replace gamma (x increases with gamma; needs (n-8)/4 + Delta/2 >= 0).
        Put nu = r D+ with 0 <= r <= 1/(n-1). Everything is D+ times a polynomial-like expression in (D+, r):
           L(D+, r) := 2 (1 - r) - (54/25) G - X - D+ X^2,   G := 1/10 + r^2 D+/(1 - 2 r D+),
           X := (1 - r) - D+ (1 - r)^2/4 + G ((n-8)/4 + D+ (1 - r)/2)          (x = D+ X, g = D+ G).
        CHECK 3: L >= 0 and 0 <= D+ X <= 1/2 on a grid of cells covering [0, DELTA0] x [0, 1/(n-1)].
Usage: check_det_n_v1.py N DELTA0
"""
import sys
from fractions import Fraction as F
from mpmath import iv, mp
iv.dps = 40; mp.dps = 50
n = int(sys.argv[1]); D0 = F(sys.argv[2]); assert 9 <= n <= 24 and 0 < D0 <= F(1, 2)
def I(fr): fr = F(fr); return iv.mpf(fr.numerator)/iv.mpf(fr.denominator)
def cell(a, b): return I(a) + (I(b) - I(a))*iv.mpf([0, 1])
def lo(x): return mp.mpf(x.a)
def hi(x): return mp.mpf(x.b)
m1 = 1 - D0/2 - F(n-4, 16); assert m1 > 0, 'CHECK 1 fails'
assert D0/(n-1) <= F(3, 104), 'CHECK 2 fails'
assert F(n-8, 4) >= 0
ND, NR = 200, 40; worst = None; xmax = None
for i in range(ND):
    Dp = cell(D0*i/ND, D0*(i+1)/ND)
    for j in range(NR):
        r = cell(F(j, NR)/(n-1), F(j+1, NR)/(n-1))
        G = I(F(1, 10)) + r*r*Dp/(1 - 2*r*Dp)
        X = (1 - r) - Dp*(1 - r)**2/4 + G*(I(F(n-8, 4)) + Dp*(1 - r)/2)
        L = 2*(1 - r) - I(F(54, 25))*G - X - Dp*X*X
        assert lo(X) >= 0 and hi(Dp*X) <= mp.mpf(1)/2, ('x out of range', i, j)
        assert lo(L) > 0, ('CHECK 3 fails', i, j, L)
        worst = lo(L) if worst is None else min(worst, lo(L)); xmax = hi(Dp*X) if xmax is None else max(xmax, hi(Dp*X))
print('DETERMINANT LEMMA n = %d, sum of positive excess <= %s: PASS. row margin >= %s; nu <= %s <= 3/104; least L >= %s (ln det Q >= D+ L); largest x <= %s; %d cells'
      % (n, D0, m1, D0/(n-1), mp.nstr(worst, 6), mp.nstr(xmax, 6), ND*NR))
