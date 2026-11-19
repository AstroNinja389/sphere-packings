"""Exact continuum verification and common-class composition for the dimension-14 difference charges."""
from pathlib import Path
from fractions import Fraction as F
import json,math,sys
import sympy as sp
from flint import arb,fmpq,ctx
from rank14_population import h,old,read,sha,get,prefix,N
def audit(tag):
    src=h/(tag+'.json');p=read(src);E=list(map(F,p['edges']));n=14;assert E[0]==1 and E[-1]==2 and E==sorted(set(E))
    e,v,dependencies=get('sharp-ref@384',True);assert p['sources']=={d.name:sha(d) for d in dependencies}
    assert set(E[1:])<=set(e)
    scale=F(p['scale']);assert scale>0
    values=[max(vi for x,vi in zip(e,v[1:]) if l<x<=r) for l,r in zip(E,E[1:])]+[v[0]]
    y=sp.symbols('t');base=[sp.Poly(1,y,domain='QQ'),sp.Poly(y,y,domain='QQ')]
    for k in range(1,2*p['K']):base.append(((2*k+12)*base[1]*base[k]-k*base[k-1]).mul_ground(sp.Rational(1,k+12)))
    charge=F(0);verified=[]
    for pool,b in zip(p['pools'],p['b'],strict=True):
        A,B=map(F,pool);b=list(map(F,b));assert all(x>=0 for x in b) and A<B and A in E and B in E
        if not any(b):continue
        pol=sum((base[2*j].mul_ground(sp.Rational(x.numerator,x.denominator)) for j,x in enumerate(b)),sp.Poly(0,y,domain='QQ'))
        coeff=list(map(F,pol.all_coeffs()));derivative_bound=sum((len(coeff)-1-i)*abs(c) for i,c in enumerate(coeff))
        dp=pol.diff();iv=dp.intervals(eps=sp.Rational(1,10**22),inf=0,sup=1)
        def ev(t):
            v=F(0)
            for x in coeff:v=v*t+x
            return v
        crit=[(F(a),F(b),ev(F(a))+derivative_bound*F(b-a)) for (a,b),_ in iv]
        def upper(a,b):
            return max([ev(a),ev(b)]+[z for l,r,z in crit if l<=b and r>=a])
        error=max(F(0),upper(F(0),1-1/B))
        f0=b[0]
        assert ev(1)==sum(b) and error<=ev(1)
        charge+=(ev(1)-error)/(N*scale)
        penalties=[]
        for j,(l,r) in enumerate(zip(E,E[1:])):
            lo=max(F(0),1-r/(2*A));hi=1-l/(2*B)
            z=max(F(0),upper(lo,hi)-error) if lo<=hi else F(0)
            penalties.append(z)
            values[j]+=(2*z-(f0-error)*int(A<=l<r<=B))/scale
        verified.append({'pool':pool,'polynomial':list(map(str,coeff)),'f0':str(f0),'uncharged':str(error),
                    'extra':list(map(str,penalties)),'at_one':str(ev(1))})
    caps=prefix()
    # Independent greedy evaluation: at each score threshold count how many classes could attain it.
    # Equivalent to putting each of N sorted order-statistic slots in its best possible bin.
    capacity=[min([N]+[c for t,c in caps.items() if t>=e]) for e in E[1:]]+[N]
    order=sorted(range(len(values)),key=values.__getitem__,reverse=True);filled=0;bound=charge
    for i in order:
        add=max(0,capacity[i]-filled);bound+=F(add,N)*values[i];filled+=add
    assert filled==N
    ctx.prec=180;comp=arb.pi()**7/(5040*arb(314).sqrt());limit=max(math.ceil(bound*10**15),int(float(comp)*10**15)+1)
    assert comp<arb(fmpq(limit,10**15)) and bound<=F(limit,10**15)
    out=h/(tag+'-exact.json');out.write_text(json.dumps({'status':'exact','D':314,'actual_density_upper_1e15':limit,'conditional':str(bound),
           'complement':str(comp),'proof_source':sha(src),'inputs':p['sources'],'paid':verified,'edges':list(map(str,E)),'scale':str(scale)},indent=1)+'\n')
    print(tag,limit/10**15,flush=True)
if __name__=='__main__':audit(sys.argv[1])
