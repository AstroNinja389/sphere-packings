"""Recompute the rank-13 bound and the separate, incomplete exclusion at the 5% target."""
import argparse
from collections import Counter
from fractions import Fraction
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

from flint import arb, ctx, fmpq

SOURCE = Path(__file__).resolve().parent / "n13"

def records(path):
    pairs = [line.split() for line in path.read_text().splitlines()]
    result = dict(pairs)
    assert len(result) == len(pairs)
    return result

def verify_frontier(work, name, frontier):
    assert frontier == records(SOURCE / name)
    (work / name).write_bytes("".join(
        f"{key} {frontier[key]}\n" for key in sorted(frontier)
    ).encode("ascii"))

def remove(frontier, keys):
    keys = list(keys)
    assert len(set(keys)) == len(keys) and set(keys) <= frontier.keys()
    for key in keys:
        del frontier[key]

def contact_prices(work, frontier):
    report = json.loads(subprocess.check_output([sys.executable, "-B", str(work/"audit_contact_prices.py")], cwd=work))
    remove(frontier, report["whole_markings"])
    assert frontier == records(SOURCE / "OPEN-AFTER-CONTACT-PRICES.txt")
    assert Counter(frontier.values()) == {"virtual": 10, "tree": 5}
    print(f"PASS. {len(report['whole_markings'])} additional whole markings excluded. "
          f"{1746860-len(frontier):,} excluded in total. {len(frontier)} remain open.")

def mordell():
    ctx.prec = 180
    volume = 128 * arb.pi() ** 6 / 135135
    upper = volume / arb(fmpq(729, 4)) ** (arb(13) / 22)
    lower = volume * arb(3).sqrt() / 54
    target = (19 * upper + lower) / 20
    floor = Fraction(242111, 500)
    assert 1113**11 < 4**11 * 972**9
    assert upper < arb(fmpq(42023513562578, 10**15))
    assert volume / arb(fmpq(242111, 500)).sqrt() < target
    for rank, ceiling in [(12, Fraction(74821,100)), (11, Fraction(99331,100)),
                          (10, Fraction(1133)), (9, Fraction(27757,25))]:
        assert 4**(13*rank*(13-rank))*floor**(rank*(rank-1)) < ceiling**156
    print("Rank 13 Mordell upper", upper, "open target", target, flush=True)

def replay(work):
    def run(script, *args):
        subprocess.run([sys.executable, "-B", str(work / script), *args], cwd=work, check=True)
    def read(name):
        return json.loads((work / name).read_bytes())

    run("audit_both_flags.py")
    scan = read("two-flag-audit-v1.json")
    reference = json.loads((SOURCE / "two-flag-audit-v1.json").read_bytes())
    for key in ("input_sha256", "counts", "per_shard", "rows", "open_key_sha256"):
        assert scan[key] == reference[key]
    frontier = records(work / "flag-open-v1.txt")
    assert frontier == records(SOURCE / "flag-open-v1.txt") and len(frontier) == 14955
    assert scan["rows"] - scan["counts"]["cutoff"] == 1746860

    run("audit_mark_vectors.py", "mixed-mark-all.jsonl")
    run("audit_cone.py")
    run("audit_reverse.py", "reverse-part1.jsonl", "reverse-part2.jsonl")
    for name in ("mixed-mark-all.audit.json", "cone-audit-v1.json", "reverse-audit-v1.json"):
        marked = read(name)["excluded"]
        assert all((frontier[k] == "reverse_trace_open") == (name == "reverse-audit-v1.json") for k in marked)
        remove(frontier, marked)
    verify_frontier(work, "dimension13-open-keys.txt", frontier)
    assert len(frontier) == 7741
    for tag in ("cof-trace", "cof-full", "lc-a", "lc-b"):
        run("audit_cofactor.py", tag)
        remove(frontier, read(tag + "-audit.json")["keys"])
    verify_frontier(work, "dimension13-open-after-cofactors.txt", frontier)
    assert len(frontier) == 75

    for tag, size in (("cells", 36), ("planes", 32)):
        seen = []
        certified = []
        for part in ("a", "b"):
            run("audit_" + tag + ".py", part)
            audit = read(f"{tag}-{part}-audit.json")
            assert set(audit["keys"]) <= set(audit["seen"])
            seen.extend(audit["seen"])
            certified.extend(audit["keys"])
        assert len(seen) == len(frontier) and set(seen) == frontier.keys()
        remove(frontier, certified)
        assert len(frontier) == size
    verify_frontier(work, "FINAL-OPEN-MARKS.txt", frontier)
    assert Counter(frontier.values()) == {"tree":15, "glue":3, "virtual":10, "domain":3, "reverse_trace_open":1}
    run("audit_neighborhoods.py")
    partial = set(read("neighborhood-audit-v1.json")["passed_keys"]) & frontier.keys()
    assert len(partial) == 19
    contact_prices(work, frontier)

if __name__ == "__main__":
    if not __debug__:
        sys.exit("Replay requires assertions. Run without -O.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, help="Extracted k11_certificates_v3.sqlite from Zenodo 23979316")
    parser.add_argument("--contact-prices-only", action="store_true",
                        help="Recheck the latest exclusions and their earlier interval prefixes from the 32-mark frontier")
    args = parser.parse_args()
    if args.contact_prices_only and not args.database:
        parser.error("--contact-prices-only requires --database")
    mordell()
    if args.database:
        os.environ["RANK9_CERTIFICATE_DB"] = str(args.database.resolve(strict=True))
        if args.contact_prices_only:
            import hashlib
            sys.path.insert(0, str(SOURCE))
            from database import DATABASE_SHA256
            with args.database.open("rb") as db:
                assert hashlib.file_digest(db, "sha256").hexdigest() == DATABASE_SHA256
            contact_prices(SOURCE, records(SOURCE/"FINAL-OPEN-MARKS.txt"))
        else:
            with TemporaryDirectory() as directory:
                work = Path(directory) / "n13"
                shutil.copytree(SOURCE, work)
                replay(work)
    else:
        print("Mordell calculation only. Supply --database to replay the finite exclusions.")
