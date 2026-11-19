"""Certified rank-thirteen partial frame test for a dimension-fourteen lattice."""
from pathlib import Path
from flint import fmpq as Q,fmpq_mat,arb,ctx
from fractions import Fraction as F
from itertools import combinations
import json,sys
H=Path(__file__).resolve().parent
def vertices(n,m,cap):
    for neg in (0,1):
        start=[tuple((cap*(-1 if i==0 and neg else 1) if i>=j else F(0)) for i in range(n)) for j in range(n+1)]
        f=lambda v:sum(max(F(0),x) for x in v)
        v={z for z in start if f(z)<=m}
        for x,y in combinations(start,2):
            a,b=f(x),f(y)
            if (a-m)*(b-m)<0:
                t=(m-a)/(b-a);v.add(tuple(l+t*(r-l) for l,r in zip(x,y)))
        yield from v
def test(m,cap,ambient=310,save=False):
    n=13;cc=0;maximum=Q(0);witness=None
    for z in vertices(n,m,cap):
        R=fmpq_mat([[Q(str(1+x if i==j else -(x+y)/2)) for j,y in enumerate(z)] for i,x in enumerate(z)])
        for j in range(1,n+1):assert fmpq_mat([[R[k,l] for l in range(j)] for k in range(j)]).det()>0
        S=R.inv();b=max(S[i,i]+S[j,j]+2*S[i,j] for i,j in combinations(range(n),2))
        if b>maximum:maximum=b;witness=list(map(str,z))
        cc+=1
    ctx.prec=120;A=arb(Q(729,4))**(arb(13)/11);rem=2*A-ambient*arb(maximum)-arb(2**14)/81*arb(Q(str(m))).exp()
    out=dict(mass=str(m),individual=str(cap),rank=n,ambient_det_cap=ambient,vertices=cc,dual_pair_upper=str(maximum),worst=witness,margin=str(rem),passed=rem>0)
    if save:(H/f'partial-frame-{m.numerator}-{m.denominator}.json').write_text(json.dumps(out,indent=2)+'\n')
    return out
if __name__=='__main__':
    for s in sys.argv[1:]:
        m=F(s);o=test(m,m,save=True);print(m,o['dual_pair_upper'],o['margin'],o['passed'])
