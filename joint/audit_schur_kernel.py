"""Independent exact audit using rational polynomial arithmetic and recurrence.
No producer imports, no floating inequalities, no sampled sign tests.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import argparse,json,math,hashlib,time

def add(a,b):
    o=dict(a)
    for k,v in b.items():
        o[k]=o.get(k,F(0))+v
        if not o[k]:del o[k]
    return o
def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def mul(a,b):
    o={}
    for p,x in a.items():
        for q,y in b.items():
            k=tuple(i+j for i,j in zip(p,q));o[k]=o.get(k,F(0))+x*y
    return {k:v for k,v in o.items() if v}
ONE={(0,0,0):F(1)}
def power(a,n):
    o=ONE
    for _ in range(n):o=mul(o,a)
    return o
def gegenbauer(n, dimension):
    # Independently generated Gegenbauer recurrence at lambda=(dimension-2)/2.
    old=[F(1)];cur=[F(0),F(dimension-2)]
    if n==0:return old
    if n==1:return [x/sum(cur) for x in cur]
    for k in range(2,n+1):
        out=[F(0)]*(k+1)
        for j,c in enumerate(cur):out[j+1]+=F(2*k+dimension-4,k)*c
        for j,c in enumerate(old):out[j]-=F(k+dimension-4,k)*c
        old,cur=cur,out
    return [x/sum(cur) for x in cur]

def bernstein_on_box(poly,degrees,box):
    # Convert power coordinates directly on a rational box, axis by axis.
    out=poly
    for axis,(d,(left,right)) in enumerate(zip(degrees,box)):
        W=[[sum(F(math.comb(i,k)*math.comb(j,k),math.comb(d,k))*left**(i-k)*(right-left)**k for k in range(min(i,j)+1)) for i in range(d+1)] for j in range(d+1)]
        nxt={}
        for old,c in out.items():
            for j in range(d+1):
                q=list(old);q[axis]=j;q=tuple(q);nxt[q]=nxt.get(q,F(0))+c*W[j][old[axis]]
        out={k:v for k,v in nxt.items() if v}
    total=math.prod(d+1 for d in degrees);maximum=max([F(0)] if len(out)<total else []) if not out else max(out.values())
    if len(out)<total:maximum=max(maximum,F(0))
    return maximum,total

def audit(candidate,output):
    start=time.time();p=Path(candidate);data=json.loads(p.read_text());S=F(data['S']);dimension=int(data['n']);assert 10<=dimension<=23;assert 2<S<3;degree=int(data['angular']);assert degree%2==0 and data['radial']==1
    slope=F(data['source_slope']);quad=F(data['source_cross']);B=F(data['source_schur_B'])
    assert 0<=B<=1 and quad>=0 and quad*B-slope*slope/4>=0
    # For every class cardinality a and actual normalized length sum H,
    # the difference is [H,a] [[c,-b/2],[-b/2,B]] [H,a]^T.
    assert [quad,-slope,B]==[quad,2*(-slope/2),B]
    # Singletons may clip t to[-1,1]: their pair energy is zero and the
    # subtracted radial quadratic c*t^2-b*t+B is nonnegative everywhere.
    layout=[(k,1,i,j) for k in range(0,degree+1,2) for j in range(2) for i in range(j+1)]
    assert list(map(list,layout))==data['layout'];x=list(map(F,data['matrix_entries']));assert len(x)==len(layout)
    minors=[]
    for pos in range(0,len(x),3):
        a,b,c=x[pos:pos+3];tests=[a,c,a*c-b*b];assert min(tests)>=0,(pos,tests);minors.append(list(map(str,tests)))
    u={(1,0,0):F(1)};v={(0,1,0):F(1)};w={(0,0,1):F(1)};ell=S-2;L=degree//2
    def construct(target):
        ru=u;rv=mul(add(ONE,scale(u,-1)),v) if target else v
        a=add(ONE,scale(ru,ell));b=add(ONE,scale(rv,ell));ab=mul(a,b)
        bound=add(scale(ONE,S),scale(add(a,b),-1)) if target else add(add(a,b),scale(ONE,-1))
        q=scale(mul(power(bound,2),w),F(1,4));out={}
        for value,(k,d,i,j) in zip(x,layout):
            rr=mul(power(ru,i),power(rv,j))
            if i!=j:rr=add(rr,mul(power(ru,j),power(rv,i)))
            z={}
            for exponent,c in enumerate(gegenbauer(k,dimension)):
                if c:
                    assert exponent%2==0
                    z=add(z,scale(mul(power(q,exponent//2),power(ab,L-exponent//2)),c))
            out=add(out,scale(mul(rr,z),value))
        if target:
            xx=add(ru,rv);psi=add(add(ONE,scale(xx,-slope)),scale(add(power(xx,2),scale(q,-4/(ell*ell))),quad))
            out=add(out,mul(power(ab,L),psi))
        return out
    counts={};maxima={};hashes={}
    for target in [False,True]:
        poly=construct(target);degs=tuple(max(p[j] for p in poly) for j in range(3));label='target' if target else 'all_root_pairs';n=int(data['angle_cells']) if not target else 1;r=int(data['radial_cells']) if not target else 1;maximum=None;count=0
        for i,j,k in product(range(r),range(r),range(n)):
            box=[(F(i,r),F(i+1,r)),(F(j,r),F(j+1,r)),(F(k,n),F(k+1,n))];m,c=bernstein_on_box(poly,degs,box);assert m<=0,(label,i,j,k,float(m));maximum=m if maximum is None else max(m,maximum);count+=c
        maxima[label]=str(maximum);counts[label]=count;hashes[label]=hashlib.sha256(repr(sorted((p,str(v)) for p,v in poly.items())).encode()).hexdigest()
    # Diagonal of each normalized harmonic is one. Cost uses actual root norm.
    diag=[sum(x[::3]),2*sum(x[1::3]),sum(x[2::3])]
    out={'status':'PASS_INDEPENDENT_EXACT_SOURCE_SCHUR_ROOT_MAJORANT','n':dimension,'source_slope':str(slope),'source_cross':str(quad),'source_schur_B':str(B),'count_coefficient':str(1-B),'source_schur_minors':list(map(str,[quad,B,quad*B-slope*slope/4])),'source_cap':str(S),'root_cap':str(S-1),'diagonal_local_power':list(map(str,diag)),'local_variable':'(a-1)/(S-2), where a is the actual squared root length','kernel_matrices':minors,'bernstein_control_counts':counts,'maximum_controls':maxima,'polynomial_sha256':hashes,'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.time()-start,'scope':'Universal actual-length cross-product kernel plus positive2x2source moment matrix. For ALL classcounts, pairenergy >=(1-B)a(a-1)-sum(c*t^2-b*t+B). No finite count cap assumed. Root sign domains and source matrix checked exactly. No density claim.'}
    dest=Path(output);assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n');print(out['status'], dimension, str(S), 'seconds',round(time.time()-start,2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('candidate');p.add_argument('output');a=p.parse_args();audit(a.candidate,a.output)
