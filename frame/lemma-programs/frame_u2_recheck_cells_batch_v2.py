"""Batch driver (2026-11-18, v2: uses frame_u2_recheck_v2.py): mode 'cells' of frame_u2_recheck_v2.py for all cell files matching a glob pattern
(the list is too long for a command line). It sets sys.argv inside the process and calls the unchanged main_cells().
Usage: FRAME_N=N frame_u2_recheck_cells_batch_v2.py DELTA0 A B TARGET PART NPARTS "GLOB"
Output: FU2-RECHECK-v2-<tag>-cells-<PART>of<NPARTS>.json (as written by main_cells()).
"""
import sys, glob
argv = sys.argv[:]; files = sorted(glob.glob(argv[7])); assert files, 'no files'
sys.argv = argv[:5] + ['cells', argv[5], argv[6]] + files
import frame_u2_recheck_v2 as m
m.main_cells()
