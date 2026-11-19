"""Cell mode for the rows a two-class table left above its target, and for certified rows the re-check did not confirm
(2026-11-18, v1). FRAME_N must be set in the environment.
Usage: run_cells_fu2_v1.py CELL_TARGET DEPTH TABLE0.json TABLE1.json [-- RECHECK0.json RECHECK1.json TABLE0.npy TABLE1.npy]
   (DELTA0, A, B are read from the table json files; with the optional part, rows listed as failed by the re-checks are added)
Runs frame_u2_scheme_s3_v1.py DELTA0 A B CELL_TARGET cell gi pi ci d DEPTH for every such row, then
frame_u2_recheck_s3_v1.py ... cells 0 1 on all cell files of that target. One line per step; exit code 0 in every case."""
import sys, json, subprocess, glob, os
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; CT = sys.argv[1]; DEPTH = sys.argv[2]; rest = sys.argv[3:]
extra = []
if '--' in rest: k = rest.index('--'); extra = rest[k+1:]; rest = rest[:k]
tabs = [json.loads((H/f).read_text()) for f in rest]; n = tabs[0]['n']; D0 = tabs[0]['delta0']; A = tabs[0]['A']; B = tabs[0]['B']
assert all(t['n'] == n and t['delta0'] == D0 and t['A'] == A and t['B'] == B for t in tabs) and int(os.environ['FRAME_N']) == n
todo = {tuple(r[:4]) for t in tabs for r in t['not_certified']}
if extra:
    rc = [json.loads((H/f).read_text()) for f in extra if f.endswith('.json')]; rows = np.vstack([np.load(H/f) for f in extra if f.endswith('.npy')])
    for S in rc:
        assert S['nfail'] == len(S['failed_rows'])
        for i in S['failed_rows']: todo.add(tuple(int(round(x)) for x in rows[i, :4]))
todo = sorted(todo); PY = sys.executable
print('rows needing cells: %d' % len(todo), flush=True)
if not todo: sys.exit(0)
def last_result(r):
    lines = [x for x in r.stdout.splitlines() if x.startswith('RESULT')]
    return lines[-1] if lines else ('NO RESULT LINE: ' + r.stderr[-300:])
bad = 0
for gi, pi_, ci, d in todo:
    r = subprocess.run([PY, '-B', '-W', 'ignore', 'frame_u2_scheme_s3_v1.py', D0, A, B, CT, 'cell', str(gi), str(pi_), str(ci), str(d), DEPTH],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=str(H)); res = last_result(r)
    if not res.startswith('RESULT PASS'): bad += 1
    print('cell g%d p%d c%d d%d: %s' % (gi, pi_, ci, d, res[:150]), flush=True)
tag = 'N%d-D%s-A%s-B%s-T%s' % (n, D0.replace('/', '_'), A.replace('/', '_'), B.replace('/', '_'), CT)
files = sorted(os.path.basename(f) for f in glob.glob(str(H/('FU2-CELL-%s-g*.json' % tag))))
r = subprocess.run([PY, '-B', '-W', 'ignore', 'frame_u2_recheck_s3_v1.py', D0, A, B, CT, 'cells', '0', '1'] + files,
                   stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=str(H))
print('cells: %d rows, %d not PASS in cell mode; cells re-check of %d files: %s' % (len(todo), bad, len(files), last_result(r)[:200]), flush=True)
