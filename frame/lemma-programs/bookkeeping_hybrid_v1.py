"""Bookkeeping for the HYBRID lemma (2026-11-18, v1). It only matches lists.
Statement to be covered: for every (case, cell) pair of q (40 x 329 pairs), either
  (1) the one-class certificate holds:  N_Q(q) >= 2 implies psi(q) < CLAIM   (pair covered in the one-class bookkeeping), or
  (2) all nine (2q-case, 2q-cell) combinations (p, d) in {(0,0)} u {1,2} x {1,2,3,4} have a two-class certificate
      (N_Q(q) >= 2 and N_Q(2q) >= 2 imply psi(q) < CLAIM) confirmed by the two-class re-check with covering.
Together: N_Q(q) >= 2 and N_Q(2q) >= 2 imply psi(q) < CLAIM for all q.
Usage: bookkeeping_hybrid_v1.py N DELTA0 CLAIM ONECLASS-BOOKKEEPING.json TWOCLASS-RECHECK-CELLS.json [...]
"""
import sys, json
from fractions import Fraction as F
from pathlib import Path
n = int(sys.argv[1]); D0 = F(sys.argv[2]); T = F(sys.argv[3]); B1 = json.load(open(sys.argv[4])); RC = [json.load(open(f)) for f in sys.argv[5:]]
problems = []
if not (B1['n'] == n and F(B1['delta0']) == D0 and F(B1['A']) == 0 and F(B1['target']) <= T and not B1['problems'] and B1['pairs'] == 40*329): problems.append('one-class bookkeeping does not fit')
hard = [tuple(x) for x in B1['pairs_not_covered']]
combos = {(0, 0)} | {(p, d) for p in (1, 2) for d in (1, 2, 3, 4)}; got = {}
for S in RC:
    if not (S['n'] == n and F(S['delta0']) == D0 and F(S['A']) == 0 and F(S['B']) == 0 and F(S['target']) <= T): problems.append('a two-class re-check has other parameters'); continue
    for gi, pi_, ci, d, npieces, nfail, cov, worst in S['cells']:
        if nfail == 0 and cov and worst is not None and F(str(worst)) < T: got.setdefault((gi, ci), set()).add((pi_, d))
missing = [list(p) for p in hard if got.get(p, set()) != combos]
worst2 = max([S['largest_rechecked'] for S in RC if S['largest_rechecked'] is not None], default=None)
res = dict(n=n, delta0=str(D0), claim=str(T), pairs=40*329, pairs_by_one_class=40*329-len(hard), pairs_by_two_class=len(hard)-len(missing), pairs_not_covered=missing,
           two_class_pieces_files=len(RC), largest_rechecked_two_class=worst2, one_class_bookkeeping=sys.argv[4], problems=problems,
           result='COMPLETE' if not missing and not problems else 'INCOMPLETE')
out = Path(sys.argv[4]).with_name('HYBRID-BOOKKEEPING-N%d-D%s-T%s.json' % (n, str(D0).replace('/', '_'), sys.argv[3].replace('/', '_')))
assert not out.exists(); json.dump(res, open(out, 'w'), indent=1)
print('RESULT %s: n=%d claim %s: %d pairs by the one-class lemma, %d by the two-class lemma, %d not covered; problems %s; largest two-class value re-checked %s' % (
    res['result'], n, T, res['pairs_by_one_class'], res['pairs_by_two_class'], len(missing), problems, worst2))
