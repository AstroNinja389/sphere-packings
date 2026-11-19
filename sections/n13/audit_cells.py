"""Recompute every cut interval, including its scalar premises, determinant matrices and coverage."""
import json,sys,math
from fractions import Fraction as F
from functools import lru_cache
from flint import fmpq_mat as R,fmpz_mat as M,fmpq as Q
from audit_mark_vectors import here,sql,matrix,sha
from audit_cone import enumerate_min
def rt(x):return F(math.isqrt(x.numerator*10**12//x.denominator),10**6)
def q(f):return Q(f.numerator,f.denominator)
def interval(kind,low,high,ref):
    d=768 if kind=='virtual' else 1113
    E=F(99331,100);a=F(9799,10000);ce=F(27757,25)
    cap=min(ce,F(1133)*high,min(ce,F(1024)/low**4) if low else ce)
    if ref>cap or low**5*d>1024:return None
    u=max(low,ref/1133);tri=F(0)
    if high<=a:
        if kind=='trace':return None
        u=max(u,F(75*d,99331));elo=max(ref,u*d)
        t=max(3*u/4,F(200*d,297993),rt(elo/(2*E)));tri=rt(16*elo/(3*E))
    else:
        u=max(u,min(a,F(75*d,99331)));t=max(3*u/4,min(3*a/4,F(200*d,297993)))
        if kind=='trace':u=max(u,a);t=max(t,3*u/4)
    if high<u:return None
    return tuple(map(q,(u,t,cap,tri)))
def test(r,kind,P,C,u,t,cap,tri):
    assert r['kind']==kind and r['mark']
    SS=[R(M(m))/100000 for m in r['sources']]
    assert all(m==m.transpose() and all(a>0 for a in (-m).charpoly().coeffs()) for m in SS)
    for record in r['steps']:
        K=R(M(record['K']))/10**6;assert K==K.transpose()
        H=R(9,9);beta=Q(0)
        for weight,code in record['weights']:
            assert type(weight)==int and weight>0
            if code[0]=='lift':
                Z=M(code[1]);assert Z.ncols()==9 and all(any(v) for v in code[1])
                if Z.nrows()==1:b=t
                else:
                    assert Z.nrows()==3 and Z.rank()==2 and any(all(x+i*y+j*z==0 for x,y,z in zip(*code[1])) for i in (-1,1) for j in (-1,1))
                    b=max(3*t,5*u/2,tri)
                A=R(Z.transpose()*Z)
            else:
                assert code[0]=='cofactor'
                S=SS[code[1]];v=R(9,1,code[2]);assert any(v.entries());sv=S*v;sx=(v.transpose()*sv)[0,0]
                b=Q(code[3],10**6);assert b>=0 and (b/8)**8*cap*sx<=4*S.det()
                A=S-sv*sv.transpose()/sx
            beta+=weight*b/10**6;H+=(weight*A)/10**6
        c=R(C);a=c*(K+H)
        mx=max(sum(a[i,j]*c[i,j] for j in range(9)) for i in range(c.nrows()))
        K-=P*max(Q(0),mx-4-4*beta/9)/4
        cf=(-K).charpoly().coeffs()
        if all(v>0 for v in cf) and cf[0]>cap:return True
    return False
def main():
    path=here/('cells-'+sys.argv[1]+'.jsonl');front=dict(l.split() for l in (here/'dimension13-open-after-cofactors.txt').read_text().splitlines())
    yes=[];partial={};seen=set()
    for line in path.open():
        r=json.loads(line);key=r['key'];assert key in front and key not in seen;seen.add(key);kind,s,blob=sql.execute('select kind,scale,gram from form where key=?',(key,)).fetchone()
        assert r['kind']==kind
        G=matrix(blob);C=enumerate_min(G,s);P=4*R(G)/s;det=F(str(P.det()))
        head=F(0);pieces=[]
        for cell in r['pieces']:
            l,h=F(cell['l']),F(cell['r']);assert head==l<h
            f=interval(kind,l,h,det)
            if f is None:assert cell.get('empty');ok=True
            elif cell.get('candidate'):
                assert cell['witness']['key']==key;ok=test(cell['witness'],kind,P,C,*f)
            else:ok=False
            if not ok:break
            head=h;pieces.append(str(h))
        if head**5*768>1024:yes.append(key)
        elif pieces:partial[key]=pieces
    out=here/('cells-'+sys.argv[1]+'-audit.json');out.write_text(json.dumps({'status':'exact full coverage only counted','source':sha(path),
        'frontier':sha(here/'dimension13-open-after-cofactors.txt'),'seen':sorted(seen),'pass':len(yes),'keys':yes,'partial_prefixes':partial},indent=1)+'\n')
    print(path.name,len(seen),len(yes),len(partial))
if __name__=='__main__':main()
