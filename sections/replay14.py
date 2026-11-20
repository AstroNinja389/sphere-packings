"""Replay the two determinant ranges, parity geometry, Fourier budgets and both angular checks."""
import json
import os
from fractions import Fraction as F
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

from flint import arb, ctx, fmpq

HOME = Path(__file__).resolve().parent
SOURCE = HOME / "n14"

def read(path):
    return json.loads(path.read_bytes())

def verify(work):
    sys.path[:0] = [str(work), str(work / "geometry"), str(HOME.parent / "frame")]
    import audit_frame_bound as fourier
    from rank14_length_dp import Budget
    from rank14_adaptive import independent
    from sharper_partial import check
    from fifteen import check_matrix
    from rank14_population import prefix
    import torus_check

    ctx.prec = 180
    den = 10**15
    claim = arb(fmpq(33997010427326, den))
    assert arb.pi()**7 / (5040*arb(314).sqrt()) < claim
    geometry = work / "geometry"
    torus_check.main()
    for field in ("rank", "length_floor", "ambient_det_cap", "dual_pair_upper", "index_at_most", "reference_D4_verified_frames"):
        assert read(geometry / "two-torus-audit.json")[field] == read(SOURCE/"geometry/two-torus-audit.json")[field]
    fifteen = check_matrix(15, F(3,4), F(5,16))
    assert [[n,v] for n,v in fifteen] == read(geometry/"glue-audit.json")["dependent_fifteen_determinants"]
    assert all(F(det)>0 for _,det in fifteen)
    rows = read(work / "rank14-adaptive-314.json")
    table = []
    for row in rows:
        cap, mass = F(row["u"]), F(row["m"])
        assert cap>0 and 0<mass<F(3,4) and row["ambient_det_cap"] == 314
        recomputed = check(mass,cap,314)
        assert recomputed["passed"] and all(row[k] == value for k,value in recomputed.items())
        assert independent(row) == row["independent_vertices"] > 0
        table.append((cap, 2*mass))

    bundle = geometry / "sharp-ref-bundle.json"
    arguments = read(bundle)
    edges = list(map(F,arguments["E"]))
    assert arguments["n"] == 14 and not arguments.get("frame") and edges[-1] == F(21,8)
    assert max(a for a,_ in table) >= (edges[-1]-2)/2
    assert prefix()
    for direction in ("front", "back"):
        budget = Budget(edges,table,384,direction)
        fourier.backward = budget.cb
        output = work / f"fresh-{direction}.json"
        result = fourier.audit(bundle,output)
        name = f"rank14-joint-sharp-ref-314-384-{direction}"
        reference = read(SOURCE / (name+"-fourier.json"))
        for key in ("rho", "integer_branch_maxima", "classes_checked", "class_budget_scaled",
                    "density", "bundle_sha256", "rounding_denominator", "status"):
            assert result[key] == reference[key], key
        assert result["classes_checked"] == len(result["integer_branch_maxima"]) == 577
        assert result["rounding_denominator"] == 10**16
    # The archived budget hashes bind the inputs of the final sign certificates.
    # All their mathematical fields used downstream have just been recomputed.
    shutil.copyfile(SOURCE/"geometry/two-torus-audit.json",geometry/"two-torus-audit.json")
    for script in ("audit_difference.py", "crosscheck_difference.py"):
        subprocess.run([sys.executable,"-B",str(work/script),"angle-price-v1"],check=True)
    exact = read(work/"angle-price-v1-exact.json")
    ref = read(SOURCE/"angle-price-v1-exact.json")
    for key in ("inputs","proof_source","paid","edges","scale","conditional","actual_density_upper_1e15","D"):
        assert exact[key] == ref[key], key
    checked = read(work/"angle-price-v1-sturm-audit.json")
    assert checked["domain_checks"] == 194 and checked["upper_integer_1e15"] == 33997010427326
    print("PASS. Original dimension-14 angular certificate.")
    subprocess.run([sys.executable, "-B", str(SOURCE / "check_matching.py")], check=True)

if __name__ == "__main__":
    if not __debug__:
        sys.exit("Replay requires assertions. Run without -O.")
    sys.set_int_max_str_digits(0)
    for name in ("MKL_NUM_THREADS","OPENBLAS_NUM_THREADS","OMP_NUM_THREADS"):
        os.environ[name] = "1"
    with TemporaryDirectory() as directory:
        work = Path(directory)/"n14"
        shutil.copytree(SOURCE,work)
        verify(work)
