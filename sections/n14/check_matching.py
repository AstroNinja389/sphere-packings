"""Check the fixed-difference matching refinement against the published rank-14 population."""
from fractions import Fraction
from flint import arb, ctx
from crosscheck_difference import P, Q, rat, sign_on
from rank14_population import N, get, h, old, prefix, read, sha


def main():
    if not __debug__:
        raise RuntimeError("Run with assertions enabled.")
    claim = read(h / "tightmatching14-final-packing-proof.json")
    assert claim["n"] == 14 and claim["status"] == "PASS"
    for name, digest in claim["inputs"].items():
        path = h / name if (h / name).is_file() else old / name
        assert sha(path) == digest, name

    edges = list(map(Fraction, read(h / "angle-price-v1-exact.json")["edges"]))
    assert edges[0] == 1 and edges[-1] == 2 and all(a < b for a,b in zip(edges,edges[1:]))
    anchors, values, _ = get("sharp-ref@384", True)
    assert set(edges[1:]) <= set(anchors)
    scores = [max(v for x,v in zip(anchors, values[1:]) if a < x <= b)
              for a,b in zip(edges,edges[1:])] + [values[0]]
    caps = prefix()
    capacity = [min([N]+[count for end,count in caps.items() if end >= b])
                for b in edges[1:]] + [N]
    assert capacity == sorted(capacity)
    X = P([0,1])
    harmonic = [P([1]), X]
    fixed = Fraction(0)
    checked = 0
    for row, weight in claim["rows"]:
        weight = Fraction(weight)
        coeff = list(map(rat,row["co"]))
        A, B = map(Fraction,row["pool"])
        eps = rat(row["eps"])
        extra = list(map(rat,row["pay"]))
        assert weight >= 0 and coeff and min(coeff) >= 0 and 1 <= A < B < 2
        assert A in edges and B in edges and len(extra) == len(edges)-1 and min(extra) >= 0
        while len(harmonic) <= 2*(len(coeff)-1):
            k = len(harmonic)-1
            harmonic.append(((2*k+12)*X*harmonic[k]-k*harmonic[k-1])/(k+12))
        polynomial = sum((c*g for c,g in zip(coeff,harmonic[::2])),P([]))
        assert 0 <= eps <= polynomial(1)
        sign_on(eps-polynomial, Q(0), rat(1-1/B))
        checked += 1
        for j,(a,b,amount) in enumerate(zip(edges,edges[1:],extra)):
            lo, hi = max(Fraction(0),1-b/(2*A)), 1-a/(2*B)
            if lo <= hi:
                sign_on(eps+amount-polynomial,rat(lo),rat(hi))
                checked += 1
            scores[j] += weight*Fraction(str(amount-(coeff[0]-eps)*int(A<=a<b<=B)))
        fixed += weight*Fraction(str(polynomial(1)-eps))/N
    pooled = fixed + sum(Fraction(b-a,N)*max(scores[j:])
                         for j,(a,b) in enumerate(zip([0]+capacity,capacity)))
    assert checked == claim["angular_sturm_intervals"] and pooled == Fraction(claim["conditional"])
    upper = Fraction(claim["upper"])
    ctx.prec = 384
    complement = arb.pi()**7/(5040*arb(314).sqrt())
    assert complement < arb(rat(upper)) and pooled <= upper <= Fraction("0.03399687961750058")
    print("PASS dimension 14, 194 angular intervals and both determinant cases:", upper)


if __name__ == "__main__":
    main()
