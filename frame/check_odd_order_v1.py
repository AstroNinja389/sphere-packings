"""NO ELEMENTS OF SMALL ODD PRIME ORDER IN THE GLUE GROUP OF A NEAR-FRAME: exact check (2026-11-18, v1).

Setting (ODD-ORDER-EXCLUSION-v1.txt). Q' = I + diag(delta) + E on R^n, delta_a in [0, 1/8], sum delta_a <= D,
|E_ab| <= (delta_a + delta_b)/2. G a finite subgroup of R^n/D_n in which every non-zero class c has
N(c) := min{Q'(w) : w in c} >= 2. CLAIM for the given (n, D, p), p an odd prime: G has no element of order p.

Method. Let g have order p, u := p g~ in D_n for a representative g~, r_k := signed residues of k u modulo p
(entries in (-p/2, p/2)), v_k := r_k/p, k = 1, ..., (p-1)/2. Not all r_1 are 0. v_k is a representative of k g if
sum_i r_(k,i) is even ("even type"); otherwise v_k - s e_i is one, for every coordinate i and sign s ("odd type").
Bounds used (proved in the note):
 (X)  for every real vector w:  Q'(w) <= |w|^2 + |w|_1 * sum_a delta_a |w_a|.
 even type:  N(k g) <= |v_k|^2 + |v_k|_1 * D * mu,   mu := max |v_(k,a)|.
 odd type:   flip a coordinate i with |v_(k,i)| = mu (c such coordinates; choose the one with least delta, so
             delta_i <= D/c):  w = v_k - sign(v_(k,i)) e_i,  |w_i| = 1 - mu,
             N(k g) <= |v_k|^2 + (1 - 2 mu) + (|v_k|_1 + 1 - 2 mu) * D * [mu' + (1 - mu - mu')/c],
             mu' := the largest |v_(k,a)| over a != i  (mu if c >= 2, else the next value, 0 if none).
 p = 3 only (average over the flipped coordinate; m = number of non-zero coordinates, type odd iff m odd):
             odd m:  9 N(g) <= (m+3) + D (1 + 3/m) + (m-1) D |1 - 6/m|;     even m:  9 N(g) <= m (1 + D).
The element is impossible if for EVERY pattern of residues some k has its bound < 2. A pattern is the vector of
counts (c_1, ..., c_h), h = (p-1)/2, c_t = number of coordinates with |r_(1,i)| = t, 1 <= sum c_t <= n.
For p = 3 the better of the two available bounds is used. Exact rational arithmetic.
Usage: check_odd_order_v1.py N D P [P ...]
"""
import sys, itertools
from fractions import Fraction as F
n = int(sys.argv[1]); D = F(sys.argv[2]); primes = [int(x) for x in sys.argv[3:]]
assert 0 <= D and all(p % 2 == 1 and p >= 3 and all(p % q for q in range(2, p)) for p in primes)

def sres(x, p):
    x %= p
    return x if 2*x < p else x - p

def bound_generic(counts_abs, p):
    """counts_abs: dict abs residue t (1..h) -> number of coordinates, for one multiple k. Returns the bound for N(k g)."""
    m = sum(counts_abs.values()); assert m >= 1
    sq = sum(F(t*t, p*p)*c for t, c in counts_abs.items()); l1 = sum(F(t, p)*c for t, c in counts_abs.items())
    tmax = max(t for t, c in counts_abs.items() if c); mu = F(tmax, p); c = counts_abs[tmax]
    odd = sum(t*cnt for t, cnt in counts_abs.items()) % 2 == 1
    if not odd: return sq + l1*D*mu, 'even'
    others = [t for t, cnt in counts_abs.items() if cnt and t != tmax]
    mu2 = mu if c >= 2 else (F(max(others), p) if others else F(0))
    assert 1 - mu >= mu2
    return sq + (1 - 2*mu) + (l1 + 1 - 2*mu)*D*(mu2 + (1 - mu - mu2)/c), 'odd'

def bound_p3(m):
    if m % 2 == 0: return F(m)*(1 + D)/9, 'even'
    return (F(m + 3) + D*(1 + F(3, m)) + (m - 1)*D*abs(1 - F(6, m)))/9, 'odd, averaged'

ok_all = True
for p in primes:
    h = (p - 1)//2; worst = None; npat = 0
    for counts in itertools.product(range(n + 1), repeat=h):
        m = sum(counts)
        if not 1 <= m <= n: continue
        npat += 1; best = None
        for k in range(1, h + 1):
            ca = {}
            for t in range(1, h + 1):
                if counts[t-1]: a = abs(sres(k*t, p)); ca[a] = ca.get(a, 0) + counts[t-1]
            b, typ = bound_generic(ca, p)
            if p == 3: b3, typ3 = bound_p3(m); b, typ = (b3, typ3) if b3 < b else (b, typ)
            if best is None or b < best[0]: best = (b, k, typ)
        if worst is None or best[0] > worst[0]: worst = (best[0], counts, best[1], best[2])
    passed = worst[0] < 2; ok_all &= passed
    print('n = %d, D = %s, p = %d: %d patterns; largest (over patterns) of the least bound (over k): %s = %.6f at counts %s (k = %d, %s): %s' % (
        n, D, p, npat, worst[0], float(worst[0]), worst[1], worst[2], worst[3], 'PASS (< 2: no element of order %d)' % p if passed else 'FAIL'))
print('RESULT', 'PASS' if ok_all else 'FAIL', 'n', n, 'D', D, 'primes', primes)
