"""Thirteen-vector circle packing with the actual upper length of the last slot."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
from pathlib import Path
import json,sys,math,itertools
from fractions import Fraction as F
from flint import fmpq_mat,fmpq as Q,arb,ctx
h=Path(__file__).resolve().parent;old=h/'geometry';sys.path.insert(0,str(old))
from sharper_partial import check
n=13
def independent(proof):
    a=F(proof['u']);m=F(proof['m']);d=proof['ambient_det_cap'];b1=Q(proof['inverse_single']);b2=Q(proof['inverse_pair'])
    checked=set()
    # Barycentric coordinates on the gaps simplex. Vertices have at most two nonzero weights on the clipped facet.
    for signed in (False,True):
        costs=[a*(k-(k==13 and signed)) for k in range(14)]
        def vertex(weights):
            row=[sum((w*a for k,w in weights if j+k>=13),F(0)) for j in range(13)]
            if signed:row[0]=-row[0]
            return tuple(row)
        for k in range(14):
            if costs[k]<=m:checked.add(vertex([(k,1)]))
            for j in range(14):
                if costs[k]<m<costs[j]:
                    w=(m-costs[k])/(costs[j]-costs[k]);checked.add(vertex([(k,1-w),(j,w)]))
    for row in checked:
        x=[Q(str(w)) for w in row];M=fmpq_mat([[1+x[i] if i==j else -(x[i]+x[j])/2 for j in range(13)] for i in range(13)])
        assert all((-M).charpoly()[j]>0 for j in range(14))
        inv=M.inv();assert all(inv[i,i]<=b1 for i in range(13))
        for i,j in itertools.combinations(range(13),2):assert inv[i,i]+inv[j,j]+2*inv[i,j]<=b2
    ctx.prec=160;A=(arb(729)/4)**(arb(13)/11);exp=arb(Q(str(m))).exp();one=Q(proof['single_spacing']);two=Q(proof['pair_spacing'])
    assert arb(d)*b1+65536*exp*(one**2)<2*A and arb(d)*b2+65536*exp*(two**2)<2*A
    assert 2**15*exp<(1+proof['jmax'])**2*A
    for j in range(1,proof['jmax']+1):
        for t in (1,2,4):
            if j%t or ((j%2==0)!=(t>1)):continue
            z=max([0]+[k for k in range(1,14) if j*one+(k-1)*j*two<=Q(1,2)])
            i=max(k for k in range(1,14) if (k-1)*j*two<=Q(1,2))
            g=max([1]+[k for k in range(2,14) if k*j*two<=1])
            assert z+(t-1)*i+((j-t)//2)*g<13
    return len(checked)
