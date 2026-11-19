"""Independent rational primal-minimum enumeration and full normal-cone determinant test."""
import math,sys,json,hashlib
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
from flint import fmpz_mat as M
from audit_mark_vectors import matrix,here,sql,sha
def enumerate_min(G,s):
    # Raw original basis and rational square completion. No LLL or floating coordinates.
    n=9;diag=[];mu=[[F(0)]*9 for i in range(n)]
    for j in range(n):
        diag.append(int(G[j,j])-sum(diag[k]*mu[j][k]**2 for k in range(j)));assert diag[-1]>0
        for i in range(j+1,n):
            mu[i][j]=F(int(G[i,j])-sum(diag[k]*mu[j][k]*mu[i][k] for k in range(j)),diag[j])
    x=[0]*9;accepted=[]
    def visit(k,rem):
        if k<0:
            if any(x):
                assert rem==0
                if next(i for i in x if i)>0:accepted.append(list(x))
            return
        h=sum((x[j]*mu[j][k] for j in range(k+1,9)),F(0));p,q=h.as_integer_ratio()
        R=F(rem,diag[k])*q*q;w=math.isqrt(R.numerator//R.denominator)
        for v in range(-((w+p)//q),(w-p)//q+1):
            x[k]=v;visit(k-1,rem-diag[k]*(v+h)**2)
    visit(8,F(s));assert accepted;return M(accepted)
def test(r):
    kind,s,b=sql.execute('select kind,scale,gram from form where key=?',(r['key'],)).fetchone()
    assert kind==r['kind'];G=matrix(b);C=enumerate_min(G,s);e=F(4,s)**9*int(G.det());d=768 if kind=='virtual' else 1113
    for step in r['steps']:
        ul=min(F(9799,10000),max(e/1133,F(75*d,99331)))
        tl=min(F(29397,40000),max(F(3,4)*ul,F(200*d,297993)))
        top=M(step['K']);assert top==top.transpose() and top.nrows()==top.ncols()==9
        A=top;h=F(0)
        for w,vec in step['weights']:
            assert isinstance(w,int) and w>0 and len(vec) in (1,3) and all(any(x) and len(x)==9 for x in vec)
            if len(vec)==3:
                assert any(all(x+a*y+b*z==0 for x,y,z in zip(*vec)) for a in (-1,1) for b in (-1,1))
            v=tl if len(vec)==1 else max(3*tl,F(5,2)*ul)
            h+=F(w,10000)*v;Z=M(vec);A=A+100*w*(Z.transpose()*Z)
        # Correct any finite-precision violation against ALL true contacts by subtracting a multiple of P.
        raw=C*A
        largest=max(sum(raw[i,j]*C[i,j] for j in range(9)) for i in range(C.nrows()))
        excess=max(F(0),F(int(largest),10**6)-4-F(4,9)*h)
        coeff=excess/s
        den=math.lcm(10**6,coeff.denominator);K=(den//10**6)*top-(den*coeff.numerator//coeff.denominator)*G
        a=(-K).charpoly().coeffs()
        if not all(k>0 for k in a):return False
        val=F(int(a[0]),den**9)
        if val>=F(27757,25):return True
        v=F(step['next_e100'],100)
        if val<v:return False
        e=max(e,v)
        lo,hi=0,1134
        while hi-lo>1:
            k=(hi+lo)//2
            if k**4*4**5<=e**5:lo=k
            else:hi=k
        d=max(d,lo)
    return False
def main():
    p=here/'cone-witnesses-v1.jsonl'; passed=[];count=Counter()
    for line in p.open():
        o=json.loads(line)
        # A failed discovery run cannot promote a row; exact enumeration is needed only for a proposed witness.
        ok=o['estimated']>=1110.27 and test(o);count[(o['kind']+('_pass' if ok else '_open'))]+=1
        if ok:passed.append(o['key'])
    assert len(passed)==len(set(passed))
    (here/'cone-audit-v1.json').write_text(json.dumps({'sha256':sha(p),'counts':count,'excluded':passed},indent=1)+'\n')
    print(count,flush=True)
if __name__=='__main__':main()
