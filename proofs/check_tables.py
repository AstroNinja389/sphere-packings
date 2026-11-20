"""Verify the published table, comparison arithmetic, archive digests and proof cross-references."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read(path):
    return json.loads(path.read_bytes())


def main():
    if not __debug__:
        raise RuntimeError("Run with assertions enabled.")
    comparison = read(HERE / "comparison.json")
    catalog = read(ROOT / "results.json")
    table = (HERE / "COMPARISON.md").read_text(encoding="utf-8")
    archives = read(HERE / "archives.json")
    for name, entry in archives.items():
        data = (HERE / name).read_bytes()
        assert len(data) == entry["bytes"] and sha256(data).hexdigest() == entry["sha256"]
    high = read(HERE / "bounds-25-48.json")
    with ZipFile(HERE / "n25-48-proofs-r9.zip") as bundle:
        assert high == json.loads(bundle.read("BOUNDS.json"))
        manifest = json.loads(bundle.read("MANIFEST.json"))
        assert len(manifest) + 1 == len(bundle.namelist()) and set(manifest) | {"MANIFEST.json"} == set(bundle.namelist())
        assert all(sha256(bundle.read(k)).hexdigest() == h for k,h in manifest.items())
    rows = comparison["dimensions"]
    assert [r["dimension"] for r in rows] == list(range(13,49))
    assert catalog["comparison_source"]["url"] == comparison["previously_established_lattice_table"]
    assert [r["dimension"] for r in rows if r.get("rank12_theorem")] == [13,14]
    markdown = {int(line.split("|")[1]): [c.strip() for c in line.split("|")[1:-1]]
                for line in table.splitlines() if line.startswith("| ") and line.split("|")[1].strip().isdecimal()}
    assert set(markdown) == set(range(13,49))
    landing = (ROOT / "README.md").read_text(encoding="utf-8")
    landing_values = {int(line.split("|")[1]): [c.strip() for c in line.split("|")[1:6]]
                      for line in landing.splitlines() if line.startswith("| ") and line.split("|")[1].strip().isdecimal()}
    assert landing_values == {n:cells[:5] for n,cells in markdown.items()}
    for r in rows:
        n = r["dimension"]
        best = [e for e in catalog["results"] if e["n"] == n and not e.get("superseded_in_this_repository_by")]
        assert len(best) == 1, n
        entry = best[0]
        upper = Fraction(r["proof_upper_rational"])
        assert 0 < upper <= Fraction(r["density_upper"]) == Fraction(entry["density_upper"])
        cells = markdown[n]
        if n != 24:
            assert cells[1] == r["density_upper"]
            assert Fraction(entry["density_upper"]) == min(Fraction(e["density_upper"]) for e in catalog["results"] if e["n"] == n)
        where = r["proof_location"]
        if not where.startswith("https://"):
            assert (HERE / where).is_file() and where in cells[-1]
        if n != 24:
            ext, lower = map(Fraction, (r["previously_established_upper"],r["named_lattice_lower"]))
            expected_upper = r["previously_established_upper"]
            expected_lower = r["named_lattice_lower"]
            if n == 13:
                assert r["comparison_scope"] == entry["comparison_upper_scope"] == "all sphere packings"
                assert expected_upper == entry["comparison"] == "0.059905026"
                assert r["comparison_source"] == comparison["dimension_13_general_packing_table"]
                assert r["comparison_source"].endswith("/" + catalog["comparison_source"]["revision"] + "/RESULTS.json")
                expected_upper += " (all packings)"
                expected_lower += " (K₁₃)"
            assert 0 < lower <= upper < ext and cells[2:4] == [expected_upper, expected_lower]
            gap = 100*(ext-upper)/(ext-lower)
            assert abs(gap-Fraction(str(r["gap_closed_percent"]))) < Fraction(1,10**12) and cells[4] == f"{float(gap):.3f}%"
        if n >= 25:
            assert Fraction(high[str(n)]["upper"]) == upper and high[str(n)]["display"] == cells[1]
        elif n in (14,15,17,18,19,20,21,22,23):
            p = ROOT / "sections/n14/tightmatching14-final-packing-proof.json" if n == 14 else HERE / where
            assert Fraction(read(p)["upper"]) == upper
        elif n == 13:
            pending = entry["stronger_target"]
            marks = (ROOT / pending["open_markings_path"]).read_text().splitlines()
            assert pending["status"] == r["stronger_target_status"] == "open"
            assert pending["density_approx"] == r["stronger_target"] and Fraction(r["stronger_target"]) < upper
            remaining = len({s.split()[0] for s in marks if s.strip()})
            assert remaining == len(marks) == pending["open_families"] == r["open_families"]
            assert pending["excluded_markings"] + remaining == pending["initial_markings"] == 1746860
            section = ROOT / "sections/n13"
            prior = {line.split()[0] for line in (section/"FINAL-OPEN-MARKS.txt").read_text().splitlines()}
            proofs = [json.loads(line)["key"] for line in (section/"contact-prices.jsonl").read_text().splitlines()]
            assert len(prior) == 32 and len(proofs) == len(set(proofs)) == 17
            assert set(proofs) <= prior and prior-set(proofs) == {s.split()[0] for s in marks}
        elif n == 24:
            assert r["density_exact"] == entry["density_exact"] == "pi^12/12!" and cells[1] == "π¹²/12!"
            assert r["previously_established_upper_exact"] == r["density_exact"]
            assert cells[2:5] == ["π¹²/12!", "π¹²/12! (Leech)", "Exact"] and r["gap_closed_percent"] is None
    print(f"PASS: all 36 comparison rows, archive digests, proof bounds and {remaining} open dimension-13 families.")


if __name__ == "__main__":
    main()
