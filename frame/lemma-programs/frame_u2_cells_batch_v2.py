"""Batch driver (2026-11-18, v2: optional cap on the multipliers, environment variable FRAME_MCAP; otherwise v1): mode 'cell' of frame_u2_scheme_v1.py for many (case, cell) pairs in ONE process.
For every pair (gi, ci) of a list and every one of the nine (2q-case, 2q-cell) combinations (pi, d) it calls the
unchanged main_cell() of frame_u2_scheme_v1.py (imported as a module), after restoring the module's grids, so the
output files FU2-CELL-<tag>-g..-p..-c..-d...json are exactly those of separate runs. Existing files are skipped.
Usage: FRAME_N=N frame_u2_cells_batch_v2.py DELTA0 A B TARGET PAIRS.txt PART NPARTS [MAXDEPTH]
       PAIRS.txt: lines "gi ci".
"""
import sys, os, time, io, contextlib
argv = sys.argv[:]; PAIRS = argv[5]; PART = int(argv[6]); NPARTS = int(argv[7]); DEP = argv[8] if len(argv) > 8 else '3'
sys.argv = argv[:5] + ['cell', '0', '0', '0', '0', DEP]
import frame_u2_scheme_v1 as m
if os.environ.get("FRAME_MCAP"):
    _cap = float(os.environ["FRAME_MCAP"]); _orig = m.lp_mult
    def _capped(pats, cons, names, extra, MCAP=300.0): return _orig(pats, cons, names, extra, MCAP=min(MCAP, _cap))
    m.lp_mult = _capped                               # multipliers are data: a smaller cap only changes which certificate is found
YG0 = m.YG.copy(); K0 = m.K; YG20 = m.YG2.copy()
pairs = [tuple(map(int, l.split())) for l in open(PAIRS) if l.strip()][PART::NPARTS]
combos = [(0, 0)] + [(p, d) for p in (1, 2) for d in (1, 2, 3, 4)]
t0 = time.time(); done = 0; bad = 0
for n, (gi, ci) in enumerate(pairs):
    for pi_, d in combos:
        out = m.HERE/('FU2-CELL-%s-g%d-p%d-c%d-d%d.json' % (m.TAG0, gi, pi_, ci, d))
        if out.exists(): continue
        m.YG = YG0.copy(); m.K = K0; m.YG2 = YG20.copy()
        sys.argv = argv[:5] + ['cell', str(gi), str(pi_), str(ci), str(d), DEP]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): m.main_cell()
        last = buf.getvalue().strip().splitlines()[-1]; done += 1
        if 'RESULT PASS' not in last: bad += 1; print('NOT PASSED %d %d %d %d: %s' % (gi, pi_, ci, d, last[:150]), flush=True)
    if n % 20 == 19: print('  %d/%d pairs, %d cell files written, %d not passed  [%.0fs]' % (n+1, len(pairs), done, bad, time.time()-t0), flush=True)
print('BATCH DONE part %d/%d: %d pairs, %d cell files written, %d not passed, %.0f s' % (PART, NPARTS, len(pairs), done, bad, time.time()-t0), flush=True)
