#!/usr/bin/env python3
"""Run every applicable exact verifier on every certificate in certificates/.

Verifiers (they share no implementation code):
  taylor.py     integer Taylor bounds with interval bisection        (standard library only)
  bernstein.py  Bernstein coefficients with subdivision              (standard library only)
  descartes.py  Descartes sign variations, even dimensions only      (needs python-flint)
  pari.py       exact real-root counting                             (needs PARI/GP; pass --gp or set PARI_GP)
A verifier that cannot run here (missing python-flint or gp) is reported as SKIPPED, never as passed.
Exit status 0 only if no verifier rejected a certificate and at least one verifier ran on each.

Usage: python verify/run_all.py [--gp PATH_TO_GP] [--only taylor,bernstein,...] [certificate.json ...]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("certificates", nargs="*", type=Path)
    parser.add_argument("--gp", default=os.environ.get("PARI_GP", shutil.which("gp")))
    parser.add_argument("--only", default="taylor,bernstein,descartes,pari")
    args = parser.parse_args()
    files = args.certificates or sorted((ROOT / "certificates").glob("n*.json"))
    if not files:
        print("no certificates found")
        return 1
    wanted = [name for name in args.only.split(",") if name]
    have_flint = importlib.util.find_spec("flint") is not None
    failed = False
    for path in files:
        n = json.loads(path.read_text())["n"]
        ran = 0
        for name in wanted:
            if name == "descartes" and n % 2:
                continue
            if name == "descartes" and not have_flint:
                print(f"n={n:3d} {name:9s} SKIPPED (python-flint not installed)")
                continue
            if name == "pari" and not args.gp:
                print(f"n={n:3d} {name:9s} SKIPPED (gp not found; pass --gp)")
                continue
            command = [sys.executable, "-B", str(HERE / f"{name}.py"), str(path)]
            if name == "pari":
                command += ["--gp", args.gp]
            start = time.time()
            result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL)
            lines = (result.stdout + result.stderr).strip().splitlines()
            last = lines[-1] if lines else ""
            ok = result.returncode == 0 and "PASS" in result.stdout
            ran += ok
            failed |= not ok
            print(f"n={n:3d} {name:9s} {'PASS' if ok else 'FAIL'} ({time.time() - start:.0f} s)  {last[:120]}")
        if not ran:
            failed = True
            print(f"n={n:3d} NO VERIFIER PASSED")
    print("RESULT", "FAIL" if failed else "ALL PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
