"""Check the original integer budgets and final bounds in dimensions 15 and 17–23."""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
RANKS = (15, 17, 18, 19, 20, 21, 22, 23)


def read(path):
    return json.loads(path.read_bytes())


def copy_archive(work):
    archive = HERE / "native-proofs.zip"
    digests = read(HERE / "archives.json")
    assert sha256(archive.read_bytes()).hexdigest() == digests[archive.name]["sha256"]
    with ZipFile(archive) as bundle:
        entries = bundle.namelist()
        manifest = json.loads(bundle.read("MANIFEST.json"))
        assert len(entries) == len(manifest) + 1 and set(entries) == set(manifest) | {"MANIFEST.json"}
        for name, expected in manifest.items():
            target = (work / name).resolve()
            assert target.is_relative_to(work) and target != work
            data = bundle.read(name)
            assert sha256(data).hexdigest() == expected, name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)


def main():
    if not __debug__:
        raise RuntimeError("Run with assertions enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dimensions", type=int, nargs="*")
    parser.add_argument("--final-only", action="store_true",
                        help="Use the recorded census receipts and rerun the final arithmetic.")
    args = parser.parse_args()
    ranks = args.dimensions or RANKS
    if any(n not in RANKS for n in ranks):
        parser.error("Supported dimensions are 15 and 17 through 23.")
    with TemporaryDirectory(prefix="lat-") as location:
        work = Path(location).resolve()
        copy_archive(work)
        # Preserve the layout expected by the original census scripts even in a renamed clone.
        repo = work / "sphere-packings"
        for folder in ("verify", "joint", "frame", "dim15", "mixed"):
            shutil.copytree(HERE.parent / folder, repo / folder, ignore=shutil.ignore_patterns("__pycache__"))
        proofs = work / "native"
        census = work / "sweep"
        expected = read(HERE / "comparison.json")["dimensions"]
        environment = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
                           OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
        environment.pop("PYTHONOPTIMIZE", None)
        environment["PYTHONPATH"] = str(work / "support")
        def run(script, arguments, directory, env):
            subprocess.run([sys.executable, "-B", "-u", str(script), *arguments],
                           cwd=directory, env=env, check=True)
        for n in ranks:
            home = census / f"n{n}"
            claim = next(row for row in expected if row["dimension"] == n)
            final = HERE / claim["proof_location"]
            packed = proofs / final.name
            assert packed.read_bytes() == final.read_bytes()
            assert Fraction(read(packed)["upper"]) == Fraction(claim["proof_upper_rational"])
            if not args.final_only:
                # Some historical checkers create output files. Work on a private copy.
                active = work / f"work-{n}"
                shutil.copytree(census, active)
                build = active / home.name
                receipt = read(next(iter(sorted(proofs.glob(f"native-full-{n}-*.json")))))
                for name in receipt["inputs"]:
                    assert sha256((home/name).read_bytes()).hexdigest() == receipt["inputs"][name]
                    for output in build.glob(Path(name).stem + "*.json"):
                        output.unlink()
                prog, *options = receipt["commands"]
                env = dict(environment, CENSUS_WORK=str(build))
                if n >= 20:
                    union = read(home / (options[0] + "-96-union.json"))
                    env.update(DUAL_START=union["dual_arg"], DET_BRANCH=union["det_split"])
                run(build / prog, options, build, env)
                for name in receipt["inputs"]:
                    old, fresh = read(home / name), read(build / name)
                    for key in ("integer_branch_maxima", "rounding_denominator", "class_budget_scaled", "rho", "density"):
                        assert old[key] == fresh[key], (n, key)
                if n in (17, 18):
                    run(proofs / "capture_small.py", [str(n)], proofs, env)
                if n == 19:
                    run(proofs / "audit_capture19.py", [], proofs, env)
            run(proofs / "verify_final.py", [final.name, claim["proof_upper_rational"]], proofs, environment)
            print(f"PASS dimension {n}: density <= {claim['density_upper']}", flush=True)


if __name__ == "__main__":
    main()
