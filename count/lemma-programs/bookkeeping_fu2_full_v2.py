"""Bookkeeping for a FULL two-class table (2026-11-18, v2: the re-check files must be named as the parts 0..NP-1 of NP; see mk_bookkeeping_v2.py). It only matches lists; it proves nothing itself.
Claim to be covered: for every (case of q, case of 2q, interval of 2q, cell) of the scheme the certificate value is below
the claimed TARGET. Every one of the 40 x 9 x 329 = 118,440 rows (9 = one row for the 2q-case '3' and four intervals
each for the cases 'e', 'o') must be either a certified row confirmed by the re-check or a row recorded as empty and
confirmed empty by the re-check; no row may be left to cells. The re-check outputs (halves all:P:NP of the whole table)
must carry the same N, DELTA0, A, B, a target <= the claim, the same table files, and together cover every certified
and every empty row exactly once.
Usage: bookkeeping_fu2_full_v2.py N DELTA0 A B CLAIM OUT.json TABLE0.npy TABLE1.npy -- RECHECK0.json RECHECK1.json
"""
import sys, json
import numpy as np
from fractions import Fraction as F
n = int(sys.argv[1]); D0 = F(sys.argv[2]); A = F(sys.argv[3]); B = F(sys.argv[4]); T = F(sys.argv[5]); out = sys.argv[6]
rest = sys.argv[7:]; k = rest.index('--'); tables = rest[:k]; rechecks = [json.load(open(f)) for f in rest[k+1:]]
import re
names = [f.replace(chr(92), '/').split('/')[-1] for f in rest[k+1:]]; halves = [re.search(r'-table-all-(\d+)of(\d+)\.json$', x) for x in names]
rows = np.vstack([np.load(f) for f in tables]); problems = []
keys = [tuple(int(round(x)) for x in r[:4]) for r in rows]
expected = {(g, p, c, d) for g in range(40) for p in range(3) for d in ([0] if p == 0 else [1, 2, 3, 4]) for c in range(329)}
if len(keys) != len(set(keys)): problems.append('a row occurs twice')
if set(keys) != expected: problems.append('rows do not match the 118,440 expected rows: missing %d, extra %d' % (len(expected - set(keys)), len(set(keys) - expected)))
st = rows[:, 5].astype(int); cert = np.flatnonzero(st == 0); emp = np.flatnonzero(st == 3); left = np.flatnonzero((st == 1) | (st == 2))
if len(left): problems.append('%d rows left to cells (not certified in the table)' % len(left))
if len(cert) and not (float(rows[cert, 4].max()) < float(T)): problems.append('a stored certified value is not below the claim')
nn = len(rechecks); seen = set(); tot_c = tot_e = 0; worst = None
for S in rechecks:
    if not (S['n'] == n and F(S['delta0']) == D0 and F(S['A']) == A and F(S['B']) == B and F(S['target']) <= T): problems.append('a re-check has other parameters or a weaker target')
    if [f.replace('\\', '/').split('/')[-1] for f in S['files']] != [f.replace('\\', '/').split('/')[-1] for f in tables]: problems.append('a re-check read other table files')
    if not (S['rows_total'] == len(rows) and S['certified'] == len(cert) and S['empty'] == len(emp)): problems.append('a re-check saw another table')
    if S['nfail'] != 0 or S['failed_rows'] or S['empty_not_confirmed'] or not S['result'].startswith('PASS_ALL_ROWS_OF_THIS_PART'): problems.append('a re-check did not pass')
    tot_c += S['rechecked']; tot_e += S['empty_checked']
    if S['largest_rechecked'] is not None: worst = S['largest_rechecked'] if worst is None else max(worst, S['largest_rechecked'])
# the halves all:P:NP pick cert[P::NP] and emp[P::NP]; with NP = number of re-check files and P = 0..NP-1 they partition both lists
if not all(halves) or [(int(m.group(1)), int(m.group(2))) for m in halves if m] != [(p, len(names)) for p in range(len(names))]: problems.append('the re-check files are not named as the parts 0..NP-1 of NP, in order')
elif [S['rechecked'] for S in rechecks] != [len(cert[p::nn]) for p in range(nn)] or [S['empty_checked'] for S in rechecks] != [len(emp[p::nn]) for p in range(nn)]: problems.append('a re-check covers another number of rows than its part should')
if tot_c != len(cert) or tot_e != len(emp): problems.append('the re-checks cover %d certified and %d empty rows, the table has %d and %d' % (tot_c, tot_e, len(cert), len(emp)))
if sorted(len(cert[p::nn]) for p in range(nn)) != sorted(S['rechecked'] for S in rechecks): problems.append('the halves are not the parts 0..NP-1 of NP')
if worst is not None and not (F(str(worst)) < T): problems.append('largest re-checked value not below the claim')
res = dict(n=n, delta0=str(D0), A=str(A), B=str(B), claim=str(T), rows=len(rows), certified_rows_confirmed=int(len(cert)) if not problems else None,
           empty_rows_confirmed=int(len(emp)) if not problems else None, rows_left_to_cells=int(len(left)),
           largest_stored_certified=float(rows[cert, 4].max()) if len(cert) else None, largest_rechecked=worst, problems=problems, halves_identified_by='file names of the re-check outputs', result='COMPLETE' if not problems else 'INCOMPLETE')
json.dump(res, open(out, 'w'), indent=1)
print('RESULT %s: n=%d, two-class table at A=%s, B=%s, claim %s: %d rows = %d certified + %d empty + %d left; largest stored %s, largest re-checked %s; problems %s' % (
    res['result'], n, A, B, T, len(rows), len(cert), len(emp), len(left), res['largest_stored_certified'], worst, problems))
