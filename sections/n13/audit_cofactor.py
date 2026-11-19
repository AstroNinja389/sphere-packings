"""Exact rank-eight cofactor and marked-matrix auditing. Discovery inputs supply directions only."""
import sys,math,json,zlib
from fractions import Fraction as F
from pathlib import Path
from flint import fmpz_mat as M,fmpq_mat as R,fmpq as Q
from audit_mark_vectors import here,sql,matrix,sha
from audit_cone import enumerate_min
def q(f):
    if isinstance(f,Q):return f
    f=F(f);return Q(f.numerator,f.denominator)
UE=Q(27757,25)
def check(r,front):
    k=r['key'];kind,s,g,payload=sql.execute('select kind,scale,gram,cert from form where key=?',(k,)).fetchone()
    assert kind==r['kind'] and ((front[k]=='reverse_trace_open')==r['reverse'])
    G=matrix(g);P=(R(G)*4)/s;E=Q(99331,100);u0=Q(9799,10000)
    if min(G[i,i] for i in range(9))>s:
        x=M(9,1,json.loads(zlib.decompress(payload))['x']);assert any(x.entries()) and (x.transpose()*G*x)[0,0]<=s
    if r['reverse']:u=u0;t=3*u/4
    else:
        d=768 if kind=='virtual' else 1113
        u=min(u0,max(P.det()/1133,3*d/(4*E)));t=min(3*u0/4,max(3*u/4,2*d/(3*E)))
    S=[R(M(v))/100000 for v in r['sources']]
    for v in S:
        assert v==v.transpose() and all(a>0 for a in (-v).charpoly().coeffs())
    determinants=[v.det() for v in S]
    C=enumerate_min(G,s) if r['mark'] else None
    for step in r['steps']:
        if step['estimated']<1110.25:continue
        H=R(9,9);h=Q(0)
        for w,feature in step['weights']:
            assert type(w)==int and w>0
            if feature[0]=='cofactor':
                _,j,vec,m=feature;S0=S[j];assert len(vec)==9 and any(vec) and m>0
                x=R(9,1,vec);v=S0*x;px=(x.transpose()*v)[0,0];b=Q(m,10**6)
                assert (b/8)**8 *UE*px<=4*determinants[j]
                a=S0-(v*v.transpose())/px
            else:
                assert feature[0]=='lift';vec=feature[1];assert all(len(x)==9 and any(x) for x in vec)
                if len(vec)==1:b=t
                else:
                    assert len(vec)==3 and any(all(x+i*y+j*z==0 for x,y,z in zip(*vec)) for i in (-1,1) for j in (-1,1))
                    b=max(3*t,5*u/2)
                z=R(vec);a=z.transpose()*z
            h+=w*b/10**6;H+=(a*w)/10**6
        if C is None:K=P*(1+h/9)-H
        else:
            K=R(M(step['K']))/10**6;assert K==K.transpose()
            V=R(C)*(K+H)
            v=max(sum(V[i,j]*C[i,j] for j in range(9)) for i in range(C.nrows()))
            K-=P*(max(Q(0),v-4-4*h/9)/4)
        a=(-K).charpoly().coeffs()
        if all(x>0 for x in a) and a[0]>=UE:return True
    return False
def main():
    front=dict(v.split() for v in (here/'dimension13-open-keys.txt').read_text().splitlines())
    p=here/(sys.argv[1]+'.jsonl');seen=set();passed=[]
    for l in p.open():
        r=json.loads(l);k=r['key'];assert k in front and k not in seen;seen.add(k)
        if check(r,front):passed.append(k)
    (here/(sys.argv[1]+'-audit.json')).write_text(json.dumps({'status':'independent rational cofactor exclusions','source':sha(p),
         'frontier':sha(here/'dimension13-open-keys.txt'),'candidates':len(seen),'pass':len(passed),'keys':sorted(passed)},indent=1)+'\n')
    print(p.name,len(seen),len(passed))
if __name__=='__main__':main()
