"""Portable copy of audit_frame_floor_bound_v2.py (sha256 5756f5575c6a201858b2ad60b157df60fd3715fa0e4e8e68104ee9b77508de57); only path handling differs:
the repository root is found from this file, and the bundle names its inputs relative to its own folder.

Exact rational audit of a class-budget bound with joint cuts AND a frame floor (2026-11-18, v2; v1 wrote the final density as a fraction string when a floor is present, v2 writes a decimal. No other change).

Same composition as the sweep's audit_full_dimension_bound_v2.py (the Fourier function is verified anew with the
published Bernstein verifier, every joint kernel is audited anew, weights are rounded up and penalties down to a
common denominator), with one more ingredient, the frame floor of N15-FRAME-FLOOR-THEOREM-v1.txt:
   a class with at least `count` pairs of squared length <= cap satisfies  sum_{first count slots} v - floor >= 0,
   v(bin) = upper end for bins from 2 on, min(2, upper end + short_add) for a bin below 2,
so for the multiplier mu >= 0 of the bundle the class budget is the maximum of
   case A: fewer than `count` pairs up to cap                      (no extra term),
   case B: at least `count` pairs up to cap, plus mu * (sum v - floor).
The floor applies to lattices denser than `complement_density`; the reported bound is
max(class bound, complement). The class maximum is computed here by an exact integer dynamic programme written for
this file (it shares no code with the search oracle). With no floor in the bundle the result must equal that of
audit_full_dimension_bound_v2.py; --selftest compares the dynamic programme with explicit enumeration.
Usage: python -B dim15/audit_frame_floor_bound.py dim15/bundle.json OUTPUT.json   |   python -B dim15/audit_frame_floor_bound.py --selftest
"""
from pathlib import Path
from fractions import Fraction as F
import json, sys, hashlib, time, itertools, random
from bisect import bisect_right
P = Path(__file__).resolve().parents[1]
SWEEP = P/'joint'
sys.path.insert(0, str(P/'verify')); sys.path.insert(0, str(SWEEP))
import bernstein as vb
import mpmath as mp

def ceil(x): return -((-x.numerator)//x.denominator)
def floor_int(x): return x.numerator//x.denominator
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
NEG = None

def class_max(W, pen, caps, offset, J, U=None, count=None, bstar=None, case='plain'):
    """Maximum over cumulative long counts 0 <= k_0 <= k_1 <= ... with k_j <= caps[j] of
         sum_j (k_j - k_{j-1}) W[J+j] - pen[j] (k_j+offset)(k_j+offset-1)
         + [case B] sum_{j <= bstar} U[J+j] * (min(k_j+offset, count) - min(k_{j-1}+offset, count)),
       with k_bstar + offset <= count-1 in case A and >= count in case B. Integers only. None if infeasible."""
    d = {0: 0}
    for j in range(len(caps)):
        top = caps[j]
        if case == 'A' and j <= bstar: top = min(top, count - 1 - offset)
        new = {}
        for k in range(0, top + 1):
            best = NEG
            for old, val in d.items():
                if old > k: continue
                v = val + (k - old)*W[J+j]
                if case == 'B' and j <= bstar: v += U[J+j]*(min(k+offset, count) - min(old+offset, count))
                if best is None or v > best: best = v
            if best is not None: new[k] = best - pen[j]*(k+offset)*(k+offset-1)
        if case == 'B' and j == bstar: new = {k: v for k, v in new.items() if k + offset >= count}
        d = new
        if not d: return None
    return max(d.values())

def selftest():
    rng = random.Random(20261118); checked = 0
    for trial in range(300):
        nb = rng.randint(2, 4); J = 1; caps = sorted(rng.randint(1, 4) for _ in range(nb)); count = rng.randint(2, 4); bstar = rng.randint(0, nb-1)
        W = [rng.randint(-5, 9) for _ in range(J+nb)]; U = [rng.randint(0, 6) for _ in range(J+nb)]; pen = [rng.randint(0, 2) for _ in range(nb)]
        for offset in (0, 1):
            exp = {'plain': None, 'A': None, 'B': None}
            for ks in itertools.product(*[range(c+1) for c in caps]):
                if any(ks[i] > ks[i+1] for i in range(nb-1)): continue
                base = sum((ks[j] - (ks[j-1] if j else 0))*W[J+j] - pen[j]*(ks[j]+offset)*(ks[j]+offset-1) for j in range(nb))
                extra = sum(U[J+j]*(min(ks[j]+offset, count) - min((ks[j-1] if j else 0)+offset, count)) for j in range(bstar+1))
                n_cap = ks[bstar] + offset
                exp['plain'] = base if exp['plain'] is None else max(exp['plain'], base)
                if n_cap <= count-1: exp['A'] = base if exp['A'] is None else max(exp['A'], base)
                else: exp['B'] = base+extra if exp['B'] is None else max(exp['B'], base+extra)
            for case in ('plain', 'A', 'B'):
                got = class_max(W, pen, caps, offset, J, U, count, bstar, case); assert got == exp[case], (trial, case, got, exp[case]); checked += 1
    print('SELFTEST PASS: %d comparisons of the dynamic programme with explicit enumeration' % checked)

def audit(bundle, output):
    start = time.time(); bundle = Path(bundle); data = json.loads(bundle.read_text()); n = data['n']; base = bundle.parent/data['baseline']
    assert sha(base) == data['baseline_sha256']; cert = vb.parse_certificate(base.read_text()); assert cert.n == n
    p, q = vb.laguerre_pair(cert); vb.prove_polynomial_obligations(cert, p, q)
    E = list(map(F, data['E'])); assert sorted(set(E)) == E and set(cert.E) <= set(E) and E[0] == 1 and E[-1] == cert.E[-1]; J = E.index(F(2)); C = 2*(2**n-1)
    assert E[-1] < 3 and n*(1-2/E[-1])**2 < 1
    raw = [g/vb.exp_partial_sum(cert.tau0*cert.E[i]/2) for i, g in enumerate(cert.Gam)]
    for i in range(len(raw)-2, cert.J-1, -1): raw[i] = max(raw[i], raw[i+1])
    weights = [C*raw[bisect_right(cert.E, e)-1] for e in E[:-1]]; penalties = [F(0)]*(len(E)-1-J); bonus = F(0); dependencies = {base.name: sha(base)}
    for i, cut in enumerate(data['cuts']):
        lam = F(cut['multiplier']); assert lam >= 0
        if lam == 0: continue
        cp = bundle.parent/cut['candidate']; cc = json.loads(cp.read_text()); assert cc['n'] == n
        if 'source_schur_B' in cc: from audit_schur_kernel import audit as ka
        else: from audit_joint_kernel import audit as ka
        fresh = Path(output).with_name(Path(output).stem+f'-kernel{i}.json'); ka(cp, fresh); a = json.loads(fresh.read_text()); dependencies[cp.name] = sha(cp); dependencies[fresh.name] = sha(fresh)
        S = F(a['source_cap']); assert S in E and S-1 in E and 2 < S <= E[-1]
        diag = list(map(F, a['diagonal_local_power'])); m0, m1, m2 = map(F, cc['matrix_entries'][:3]); w0, w1 = map(F, cc['moment_anchor']); assert m0 >= 0 and m2 >= 0 and m0*m2-m1*m1 >= 0
        D = [diag[0]-2*(m0*w0+m1*w1), diag[1]-2*(m1*w0+m2*w1), diag[2]]; assert D[2] >= 0
        beta = m0*w0*w0+2*m1*w0*w1+m2*w1*w1; assert beta >= 0; bonus += lam*beta/(2**n-1)
        for j in range(E.index(S-1)):
            lo, hi = [(x-1)/(S-2) for x in E[j:j+2]]; weights[j] += lam*max(D[0]+D[1]*lo+D[2]*lo*lo, D[0]+D[1]*hi+D[2]*hi*hi)
        B = F(cc.get('source_schur_B', '0'))
        if 'source_schur_B' in cc:
            slope, cross = F(cc['source_slope']), F(cc['source_cross']); assert 0 <= B <= 1 and cross >= 0 and cross*B >= slope*slope/4
            for j in range(E.index(S)):
                lo, hi = [max(F(-1), min(F(1), (x-2)/(S-2))) for x in E[j:j+2]]; weights[j] += lam*max(cross*lo*lo-slope*lo+B, cross*hi*hi-slope*hi+B)
        penalties[E.index(S)-1-J] += lam*(1-B)
    den = 10**16; W = [ceil(x*den) for x in weights]; pen = [floor_int(x*den) for x in penalties]; assert min(pen) >= 0
    fl = data.get('floor'); mu = F(0); floor_record = None
    if fl is not None:
        mu = F(fl['multiplier']); count = int(fl['count']); cap = F(fl['cap']); floor = F(fl['floor']); short_add = F(fl['short_add']); complement = F(fl['complement_density_upper'])
        assert mu >= 0 and count == n and cap in E and 2 < cap <= F(9, 4) and floor > 0 and short_add >= 0 and complement > 0
        # the premise: exactly the constants of the theorem note for this dimension
        assert (n, count, cap, floor, short_add) == (15, 15, F(9, 4), F(123, 4), F(3, 56)), 'floor constants are not those of N15-FRAME-FLOOR-THEOREM-v1.txt'
        assert sha(bundle.parent/fl['theorem']) == fl['theorem_sha256']; dependencies[fl['theorem']] = fl['theorem_sha256']
        last = E.index(cap)-1; bstar = last-J; assert bstar >= 0
        v = [(min(F(2), E[b+1]+short_add) if b < J else E[b+1]) if b <= last else F(0) for b in range(len(E)-1)]
        # the complement must be an upper bound for density(Lambda15) = 8 sqrt(2) pi^7 / 15!!   (pi < PI_UP)
        PI_UP = F('3.14159265358979323847'); assert complement**2 * 2027025**2 >= 128*PI_UP**14, 'complement is not an upper bound for the density of Lambda15'
        U = [ceil(mu*x*den) for x in v]; const = floor_int(mu*floor*den)          # upper weights, lower constant
        floor_record = {'count': count, 'cap': str(cap), 'floor': str(floor), 'short_add': str(short_add), 'multiplier': str(mu), 'complement_density_upper': str(complement)}
    def row_value(caps, offset, short_bin):
        head = W[short_bin] if short_bin is not None else 0
        if fl is None or mu == 0:
            return head + class_max(W, pen, caps, offset, J)
        a = class_max(W, pen, caps, offset, J, U, count, bstar, 'A'); b = class_max(W, pen, caps, offset, J, U, count, bstar, 'B'); vals = []
        if a is not None: vals.append(head + a)
        if b is not None: vals.append(head + b + (U[short_bin] if short_bin is not None else 0) - const)
        assert vals; return max(vals)
    caps0 = [vb.long_cap(n, s) for s in E[J+1:]]; values = [row_value(caps0, 0, None)]; cap_rows = [caps0]
    for j, t in enumerate(E[1:J+1]):
        caps = [vb.short_cap(n, t, s) for s in E[J+1:]]; cap_rows.append(caps); values.append(row_value(caps, 1, j))
    budget = F(max(values), den)+bonus; rho = (p[0]+budget)/q[0]; assert rho > 0
    mp.mp.dps = 70; r = mp.mpf(rho.numerator)/rho.denominator; t = mp.mpf(cert.tau0.numerator)/cert.tau0.denominator
    density = (t/8)**(mp.mpf(n)/2)*r/mp.gamma(mp.mpf(n)/2+1); hermite = t/(2*mp.pi)*r**(mp.mpf(2)/n)
    ds = mp.nstr(density*(1+mp.mpf('1e-11')), 14); hs = mp.nstr(hermite*(1+mp.mpf('1e-11')), 14)
    from dataclasses import replace
    checked = replace(cert, density=F(ds), hermite=F(hs), density_text=ds, hermite_text=hs); vb.check_claims(checked, rho)
    final = ds if (fl is None or F(ds) >= complement) else fl['complement_density_upper']
    out = {'status': 'PASS_EXACT_CLASS_BUDGET_WITH_JOINT_CUTS' + ('_AND_CONDITIONAL_FRAME_FLOOR' if fl is not None else ''), 'n': n,
           'class_bound_density': ds, 'hermite_of_class_bound': hs, 'density': final, 'floor': floor_record,
           'binding_term': 'class bound' if fl is None or F(ds) >= complement else 'complement',
           'class_budget_scaled': str(budget), 'rho': str(rho), 'classes_checked': len(values), 'caps_sha256': hashlib.sha256(json.dumps(cap_rows).encode()).hexdigest(),
           'integer_branch_maxima': list(map(str, values)), 'rounding_denominator': den, 'dependencies': dependencies, 'bundle_sha256': sha(bundle), 'auditor_sha256': sha(__file__),
           'seconds': time.time()-start,
           'scope': 'Lattice upper bound. Exact class dynamic programme over all admissible counts, joint kernels audited anew, Fourier function verified anew. '
                    'With a floor: valid given the frame-floor theorem named in the bundle, which is computer-checked and not reviewed by a second party.'}
    path = Path(output); assert not path.exists(); path.write_text(json.dumps(out, indent=2)+'\n'); print('AUDIT', out['status'], n, 'class bound', ds, 'final', final, 'seconds', round(out['seconds'], 2), flush=True)
    return out

if __name__ == '__main__':
    if hasattr(sys, 'set_int_max_str_digits'): sys.set_int_max_str_digits(0)
    if sys.argv[1] == '--selftest': selftest()
    else: audit(sys.argv[1], sys.argv[2])
