"""Certified pooling of Fourier inequalities BEFORE maximizing over common short-class populations."""
import os
for var in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[var]='1'
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,math,bisect
from flint import arb,fmpq,ctx
sys.set_int_max_str_digits(0)
h=Path(__file__).resolve().parent;old=h/'geometry'
N=16383
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prefix():
    # Reconstruct normalized ultraspherical polynomials by the three-term recurrence in the power basis.
    # Then express the supplied even LP polynomials in that basis by exact elimination.
    ans={};base=[[F(1)],[F(0),F(1)]]
    for k in range(1,20):
        p=[F(0)]+[(2*k+12)*v/(k+12) for v in base[-1]]
        for j,v in enumerate(base[-2]):p[j]-=k*v/(k+12)
        base.append(p)
    for row in read(old/'prefix-polynomials.json'):
        s=F(row['end']);assert 1<=s<2
        p=list(map(F,row['p']));shift=row['shift'];q=(1-1/(2*s))**2
        v=[F(0)]*(4*(len(p)-1)+2*shift+3)
        for i,x in enumerate(p):
            for j,y in enumerate(p):
                k=2*(shift+i+j);v[k]-=q*x*y;v[k+2]+=x*y
        diag=sum(v);g=[]
        for k in reversed(range(len(v))):
            c=v[k]/base[k][-1];assert c>=0;g.append(c)
            for j,w in enumerate(base[k]):v[j]-=c*w
        cap=diag//g[-1];assert not any(v) and g[-1]>0 and cap==row['cap'];ans[s]=cap
    return ans
def get(tag,local):
    if local:
        stem,scale=tag.split('@');bundle=(old if stem=='sharp-ref' else h)/(stem+'-bundle.json')
        name='rank14-joint-'+stem+'-314-'+scale+'-'
        f=h/(name+'front-fourier.json');b=h/(name+'back-fourier.json')
        # This pipeline freshly binds the physical and integer-budget checks.
        for di in ('front','back'):
            cert=read(h/(name+di+'-result.json'));assert cert['d']==314
            for file in [h/(name+di+'-fourier.json'),h/'rank14-adaptive-314.json',old/'two-torus-audit.json',old/'glue-audit.json',bundle]:assert cert['hashes'][file.name]==sha(file)
    else:
        stem,scale=tag.split('@');assert stem.startswith(('torus','sharp'))
        bundle=old/(stem+'-bundle.json');f=old/(stem+'-mass-front-'+scale+'.json');b=old/(stem+'-mass-back-'+scale+'.json')
        for di in ('front','back'):
            c=read(old/(stem+'-composed-'+di+'-'+scale+'.json'));assert c['status']=='PASS' and c['source']==(f if di=='front' else b).name
        assert read(old/'sharper-partial-audit.json')['ambient_det_cap']>=314
        if stem.startswith('torus'):assert read(old/'two-torus-audit.json')['ambient_det_cap']>=314
    r=read(f);other=read(b);bb=read(bundle);fp=bundle.parent/bb['baseline'];cc=read(fp)
    assert r['n']==14 and r['status'].startswith('PASS') and sha(bundle)==r['bundle_sha256']==other['bundle_sha256']
    assert r['integer_branch_maxima']==other['integer_branch_maxima'] and r['rho']==other['rho']
    assert sha(fp)==bb['baseline_sha256']==r['dependencies'][fp.name]
    E=list(map(F,bb['E']));J=E.index(2);M=list(map(int,r['integer_branch_maxima']));assert len(M)==J+1
    tau=F(cc['tau0']);c=list(map(F,cc['c']));q=sum((-1)**j*math.comb(j+6,6)*a for j,a in enumerate(c));assert q>0
    p=sum(math.comb(j+6,6)*a for j,a in enumerate(c));assert (p+F(r['class_budget_scaled']))/q==F(r['rho'])
    fac=(tau/8)**7/5040;v=[fac*(F(r['rho'])+F(m-max(M),10**16)/q) for m in M]
    return E[1:J+1],v,[f,b,bundle,fp]
