"""Bookkeeping for the one-class Lemma U certificates (2026-11-18, v2: a claim written as a fraction no longer breaks the output name). It only matches lists; it proves nothing itself.
Every one of the 40 x 329 = 13,160 (case, cell) pairs must be exactly one of
  (a) a certified table row confirmed by the re-check (frame_u_recheck_v1.py, mode table all:0:1),
  (b) a row recorded as empty and confirmed empty by the re-check,
  (c) covered by a cell file all of whose pieces were confirmed by the re-check and whose pieces cover the cell.
A table row the re-check did not confirm is acceptable only if (c) holds for its pair. Every re-check output must
carry the same n, DELTA0, A and a target <= the claimed TARGET.
Usage: bookkeeping_fu_v2.py N DELTA0 A TARGET TABLE.npy RECHECK-TABLE.json [RECHECK-CELLS.json ...]
"""
import sys, json
import numpy as np
from fractions import Fraction as F
from pathlib import Path
n = int(sys.argv[1]); D0 = F(sys.argv[2]); A = F(sys.argv[3]); T = F(sys.argv[4]); rows = np.load(sys.argv[5]); RT = json.load(open(sys.argv[6])); RC = [json.load(open(f)) for f in sys.argv[7:]]
NG, NC = 40, 329; problems = []
keys = [(int(round(r[0])), int(round(r[2]))) for r in rows]
assert len(rows) == NG*NC and len(set(keys)) == NG*NC and all(0 <= g < NG and 0 <= c < NC for g, c in keys), 'the table does not list every pair once'
assert all(int(round(r[1])) == 0 and int(round(r[3])) == 0 for r in rows)
st = rows[:, 5].astype(int); cert = np.flatnonzero(st == 0); emp = np.flatnonzero(st == 3); left = np.flatnonzero((st == 1) | (st == 2))
def same(S): return S['n'] == n and F(S['delta0']) == D0 and F(S['A']) == A and F(S['target']) <= T
if not same(RT): problems.append('table re-check has other parameters')
if not (RT['rows_total'] == len(rows) and RT['rechecked'] == len(cert) and RT['empty_checked'] == len(emp)): problems.append('table re-check did not cover all rows')
if RT['empty_not_confirmed']: problems.append('empty rows not confirmed: %s' % RT['empty_not_confirmed'][:5])
if RT['nfail'] != len(RT['failed_rows']): problems.append('failed-row list truncated')
failed = set(RT['failed_rows']); need = {keys[i] for i in left} | {keys[i] for i in failed}
confirmed = set()
for S in RC:
    if not same(S): problems.append('a cell re-check has other parameters'); continue
    for gi, pi_, ci, d, npieces, nfail, cov, worst in S['cells']:
        if nfail == 0 and cov and pi_ == 0 and d == 0 and (worst is None or F(str(worst)) < T): confirmed.add((gi, ci))
missing = sorted(need - confirmed)
vals = [float(r[4]) for i, r in enumerate(rows) if st[i] == 0 and i not in failed]
res = dict(n=n, delta0=str(D0), A=str(A), target=str(T), pairs=len(rows), certified_rows_confirmed=len(cert)-len(failed), empty_rows_confirmed=len(emp),
           pairs_needing_cells=len(need), cells_confirmed=len(confirmed & need), pairs_not_covered=missing, problems=problems,
           largest_stored_value_of_confirmed_rows=max(vals) if vals else None, largest_rechecked_table=RT['largest_rechecked'],
           largest_rechecked_cells=max([S['largest_rechecked'] for S in RC if S['largest_rechecked'] is not None], default=None),
           result='COMPLETE' if not missing and not problems else 'INCOMPLETE')
out = Path(sys.argv[5]).with_name('FU1-BOOKKEEPING-N%d-D%s-A%s-T%s.json' % (n, str(D0).replace('/', '_'), str(A).replace('/', '_'), sys.argv[4].replace('/', '_')))
assert not out.exists(); json.dump(res, open(out, 'w'), indent=1)
print('RESULT %s: n=%d, %d pairs = %d certified rows confirmed + %d empty confirmed + %d needing cells (%d confirmed); %d not covered; problems %s; largest re-checked: table %s, cells %s' % (
    res['result'], n, len(rows), res['certified_rows_confirmed'], len(emp), len(need), res['cells_confirmed'], len(missing), problems, res['largest_rechecked_table'], res['largest_rechecked_cells']))
