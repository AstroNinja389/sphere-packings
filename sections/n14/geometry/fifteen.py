"""Direct integer-matrix and signed representative replay of the dimension-fourteen frame floor."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from math import prod,comb
import json
from flint import fmpq_mat,fmpq,arb,ctx
H=Path(__file__).resolve().parent;D=F(7,20)
def check_matrix(n,m,u):
    hist=[]
    for sg in (1,-1):
        v=[(F(0),)*(n-k)+(u,)*k for k in range(n+1)]
        if sg<0:v=[(-z[0],)+z[1:] for z in v]
        cap=lambda z:sum(q for q in z if q>0)
        pts={z for z in v if cap(z)<=m}
        for x,y in combinations(v,2):
            a=cap(x);b=cap(y)
            if (a-m)*(b-m)<0:
                k=(m-a)/(b-a);pts.add(tuple(l+(r-l)*k for l,r in zip(x,y)))
        low=None
        for z in pts:
            R=fmpq_mat([[fmpq(str(1+x if i==j else -(x+y)/2)) for j,y in enumerate(z)] for i,x in enumerate(z)])
            for j in range(1,n):
                assert fmpq_mat([[R[k,l] for l in range(j)] for k in range(j)]).det()>0
            det=R.det();assert det>0;low=det if low is None else min(det,low)
        hist.append((len(pts),str(low)))
    return hist
