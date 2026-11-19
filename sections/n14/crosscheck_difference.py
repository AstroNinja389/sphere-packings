"""Second polynomial-sign and class-population audit, using FLINT Sturm variations and sorted class slots."""
import json,math,sys
from fractions import Fraction as F
from flint import fmpq_poly as P,fmpq as Q
from rank14_population import h,old,get,prefix,N,sha,read
def rat(s):
    t=F(s);return Q(t.numerator,t.denominator)
def sign_count(seq,t):
    vals=[p(t) for p in seq];ns=[x>0 for x in vals if x!=0]
    return sum(x!=y for x,y in zip(ns,ns[1:]))
def sign_on(p,a,b):
    if not p:return
    assert p(a)>=0 and p(b)>=0
    # Check one interior nonroot; the sign can change only at odd-multiplicity roots.
    if a==b:return
    for k in range(2,p.degree()+4):
        s=p(a+(b-a)/k)
        if s:assert s>0;break
    else:raise AssertionError('no nonroot sample')
    _,parts=p.factor_squarefree()
    for q,e in parts:
        if e%2==0:continue
        for v in (a,b):
            if q(v)==0:
                q,r=divmod(q,P([-v,1]));assert not r
        if q.degree()<1:continue
        seq=[q,q.derivative()]
        while seq[-1].degree()>0:
            r=-(seq[-2]%seq[-1])
            if not r:break
            seq.append(r/abs(r.leading_coefficient()))
        assert sign_count(seq,a)==sign_count(seq,b)
def main():
    tag=sys.argv[1];d=read(h/(tag+'-exact.json'));src=read(h/(tag+'.json'));assert d['proof_source']==sha(h/(tag+'.json'))
    e,v,dependencies=get('sharp-ref@384',True);assert set(d['inputs'].values())=={sha(p) for p in dependencies}
    E=list(map(F,d['edges']));scale=F(d['scale']);vals=[max(w for t,w in zip(e,v[1:]) if l<t<=r) for l,r in zip(E,E[1:])]+[v[0]]
    x=P([0,1]);G=[P([1]),x]
    for k in range(1,2*src['K']):G.append(((2*k+12)*x*G[k]-k*G[k-1])/(k+12))
    bonus=F(0);domains=0
    for row in d['paid']:
        i=src['pools'].index(row['pool']);b=list(map(rat,src['b'][i]));assert min(b)>=0
        poly=sum((z*g for z,g in zip(b,G[::2])),P([]));assert poly==P(list(reversed(list(map(rat,row['polynomial'])))))
        A,B=map(F,row['pool']);err=rat(row['uncharged']);assert err>=0 and err<=poly(1)
        sign_on(err-poly,Q(0),rat(1-1/B));domains+=1
        bonus+=F(str(poly(1)-err))/scale
        for j,(l,r,s) in enumerate(zip(E,E[1:],row['extra'])):
            p=rat(s);assert p>=0
            t0=max(F(0),1-r/(2*A));t1=1-l/(2*B)
            if t0<=t1:sign_on(p+err-poly,rat(t0),rat(t1));domains+=1
            vals[j]+=F(str(2*p-(b[0]-err)*int(A<=l<r<=B)))/scale
    caps=prefix();lim=[min([N]+[y for z,y in caps.items() if z>=u]) for u in E[1:]]+[N]
    m=0;upper=bonus
    for j,l in enumerate(lim):
        assert l>=m
        if l>m:upper+=(l-m)*max(vals[j:]);m=l
    assert m==N and upper/N==F(d['conditional']);assert upper<=N*F(d['actual_density_upper_1e15'],10**15)
    (h/(tag+'-sturm-audit.json')).write_text(json.dumps({'status':'independent signs and integer population PASS','domain_checks':domains,
              'source_sha256':sha(h/(tag+'-exact.json')),'upper_integer_1e15':d['actual_density_upper_1e15']},indent=1)+'\n')
    print(domains,d['actual_density_upper_1e15'])
if __name__=='__main__':main()
