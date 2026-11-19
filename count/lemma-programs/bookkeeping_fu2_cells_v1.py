"""Bookkeeping for a two-class table WITH CELL FILES (2026-11-18, v1). It only matches lists; it proves nothing itself.
Claim to be covered: for every (case of q, case of 2q, interval of 2q, cell) of the scheme the certificate value is below
the claimed TARGET. Every one of the 40 x 9 x 329 = 118,440 rows must be exactly one of
  (a) a certified table row confirmed by the re-check (the re-check halves all:P:NP together cover every certified row once),
  (b) a row recorded as empty and confirmed empty by the re-check,
  (c) a row whose (case, cell) is covered by a cell file all of whose pieces were confirmed by the cells re-check and
      whose pieces cover the cell (flags of the re-check: no failure, covered), with largest re-checked value below the claim.
Rows the table left above its target, and certified rows the re-check did not confirm, need (c).
Every re-check output must carry the same N, DELTA0, A, B and a target <= the claim.
(bookkeeping_fu2_full_v2.py is the version without cells; the checks of the halves are the same.)
Usage: bookkeeping_fu2_cells_v1.py N DELTA0 A B CLAIM OUT.json TABLE0.npy TABLE1.npy -- RECHECK0.json RECHECK1.json -- [CELLS-RECHECK.json ...]
"""
import sys, json, re
import numpy as np
from fractions import Fraction as F
n = int(sys.argv[1]); D0 = F(sys.argv[2]); A = F(sys.argv[3]); B = F(sys.argv[4]); T = F(sys.argv[5]); out = sys.argv[6]
rest = sys.argv[7:]; k = rest.index('--'); tables = rest[:k]; rest2 = rest[k+1:]; k2 = rest2.index('--'); rc_names = rest2[:k2]; cell_names = rest2[k2+1:]
rechecks = [json.load(open(f)) for f in rc_names]; cellchecks = [json.load(open(f)) for f in cell_names]
def base(f): return f.replace(chr(92), '/').split('/')[-1]
names = [base(f) for f in rc_names]; halves = [re.search(r'-table-all-(\d+)of(\d+)\.json$', x) for x in names]
rows = np.vstack([np.load(f) for f in tables]); problems = []
keys = [tuple(int(round(x)) for x in r[:4]) for r in rows]
expected = {(g, p, c, d) for g in range(40) for p in range(3) for d in ([0] if p == 0 else [1, 2, 3, 4]) for c in range(329)}
if len(keys) != len(set(keys)): problems.append('a row occurs twice')
if set(keys) != expected: problems.append('rows do not match the 118,440 expected rows: missing %d, extra %d' % (len(expected - set(keys)), len(set(keys) - expected)))
st = rows[:, 5].astype(int); cert = np.flatnonzero(st == 0); emp = np.flatnonzero(st == 3); left = np.flatnonzero((st == 1) | (st == 2))
if len(cert) + len(emp) + len(left) != len(rows): problems.append('a row has an unknown status')
nn = len(rechecks); tot_c = tot_e = 0; worst = None; failed = set()
def same(S): return S['n'] == n and F(S['delta0']) == D0 and F(S['A']) == A and F(S['B']) == B and F(str(S['target'])) <= T
for S in rechecks:
    if not same(S): problems.append('a table re-check has other parameters or a weaker target')
    if [base(f) for f in S['files']] != [base(f) for f in tables]: problems.append('a table re-check read other table files')
    if not (S['rows_total'] == len(rows) and S['certified'] == len(cert) and S['empty'] == len(emp)): problems.append('a table re-check saw another table')
    if S['empty_not_confirmed']: problems.append('empty rows not confirmed')
    if S['nfail'] != len(S['failed_rows']): problems.append('a failed-row list is truncated')
    if not S['result'].endswith('_ALL_ROWS_OF_THIS_PART'): problems.append('a table re-check is not a re-check of a whole part')
    failed |= set(int(i) for i in S['failed_rows']); tot_c += S['rechecked']; tot_e += S['empty_checked']
    if S['largest_rechecked'] is not None and S['nfail'] == 0: worst = S['largest_rechecked'] if worst is None else max(worst, S['largest_rechecked'])
if not all(halves) or [(int(m.group(1)), int(m.group(2))) for m in halves if m] != [(p, len(names)) for p in range(len(names))]: problems.append('the re-check files are not named as the parts 0..NP-1 of NP, in order')
elif [S['rechecked'] for S in rechecks] != [len(cert[p::nn]) for p in range(nn)] or [S['empty_checked'] for S in rechecks] != [len(emp[p::nn]) for p in range(nn)]: problems.append('a re-check covers another number of rows than its part should')
if tot_c != len(cert) or tot_e != len(emp): problems.append('the re-checks cover %d certified and %d empty rows, the table has %d and %d' % (tot_c, tot_e, len(cert), len(emp)))
if not failed.issubset(set(int(i) for i in cert)): problems.append('a failed row is not a certified row of the table')
need = {keys[i] for i in left} | {keys[i] for i in failed}
confirmed = set(); worst_cells = None
for S in cellchecks:
    if not same(S): problems.append('a cells re-check has other parameters or a weaker target'); continue
    for gi, pi_, ci, d, npieces, nfail, cov, w in S['cells']:
        if nfail == 0 and cov and (w is None or F(str(w)) < T):
            confirmed.add((gi, pi_, ci, d))
            if (gi, pi_, ci, d) in need and w is not None: worst_cells = w if worst_cells is None else max(worst_cells, w)
missing = sorted(need - confirmed)
good = [i for i in cert if int(i) not in failed]
if good and not (float(rows[good, 4].max()) < float(T)): problems.append('a stored certified value is not below the claim')
if failed and worst is None: pass
if worst is not None and not (F(str(worst)) < T): problems.append('largest re-checked table value not below the claim')
ok = not problems and not missing
res = dict(n=n, delta0=str(D0), A=str(A), B=str(B), claim=str(T), rows=len(rows), certified_rows_confirmed=len(good), empty_rows_confirmed=int(len(emp)),
           rows_needing_cells=len(need), cells_confirmed=len(confirmed & need), rows_not_covered=[list(x) for x in missing][:200], n_rows_not_covered=len(missing),
           largest_stored_certified=float(rows[good, 4].max()) if good else None, largest_rechecked=worst, largest_rechecked_cells=worst_cells,
           table_rows_failed_in_recheck=len(failed), problems=problems, halves_identified_by='file names of the re-check outputs', result='COMPLETE' if ok else 'INCOMPLETE')
json.dump(res, open(out, 'w'), indent=1)
print('RESULT %s: n=%d, two-class table at A=%s, B=%s, claim %s: %d rows = %d certified and confirmed + %d empty + %d needing cells (%d confirmed, %d not covered); largest re-checked: table %s, cells %s; problems %s' % (
    res['result'], n, A, B, T, len(rows), len(good), len(emp), len(need), len(confirmed & need), len(missing), worst, worst_cells, problems))
