"""Cell mode for the pairs a one-class table left above its target (2026-11-18, v1), ten coordinates.
Usage: run_cells_fu1_v1.py TABLE.json CELL_TARGET DEPTH     (N, DELTA0, A are read from the table's json)
Runs frame_u_scheme_n10_v1.py ... cell gi 0 ci 0 DEPTH for every pair listed as not certified, then
frame_u_recheck_n10_v1.py ... cells 0 1 on the cell files. Prints one line per step; exits 0 also if a cell stays above."""
import sys, json, subprocess, glob
from pathlib import Path
H = Path(__file__).resolve().parent; S = json.loads((H/sys.argv[1]).read_text()); CT = sys.argv[2]; DEPTH = sys.argv[3]
n = S['n']; assert n == 10; D0 = S['delta0']; A = S['A']; left = S['not_certified']; PY = sys.executable
print('pairs left by the table: %d' % len(left), flush=True)
if not left: sys.exit(0)
def last_result(r):
    lines = [x for x in r.stdout.splitlines() if x.startswith('RESULT')]
    return lines[-1] if lines else ('NO RESULT LINE: ' + r.stderr[-300:])
for gi, pi_, ci, d, val in left:
    r = subprocess.run([PY, '-B', '-W', 'ignore', str(H/'frame_u_scheme_n10_v1.py'), str(n), D0, A, CT, 'cell', str(gi), '0', str(ci), '0', DEPTH],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=str(H))
    print('cell g%d c%d (table value %.4f): %s' % (gi, ci, val, last_result(r)), flush=True)
files = sorted(glob.glob(str(H/('FU1-CELL-N%d-D%s-A%s-T%s-g*.json' % (n, D0.replace('/', '_'), A.replace('/', '_'), CT)))))
r = subprocess.run([PY, '-B', '-W', 'ignore', str(H/'frame_u_recheck_n10_v1.py'), str(n), D0, A, CT, 'cells', '0', '1'] + files,
                   stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=str(H))
print('cells re-check: %s' % last_result(r), flush=True)
