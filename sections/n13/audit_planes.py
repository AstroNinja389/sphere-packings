"""Audit reciprocal plane area, capped contact weights, and the union with the earlier u-interval proofs."""
from fractions import Fraction as F
import json,sys
from flint import fmpq_mat as R,fmpq as Q,fmpz_mat as M
from audit_cells import here,sql,matrix,enumerate_min,interval,sha
def check(v,C,P,info,kind,r,det):
    u,t,cap,tri=info;area=u**2/2
    if r<=F(9799,10000):area=max(area,4*max(det,u*(768 if kind=='virtual' else 1113))/(9*Q(99331,100)))
    S=[R(M(x))/100000 for x in v['sources']]
    assert all(s==s.transpose() and all(y>0 for y in (-s).charpoly().coeffs()) for s in S)
    h=Q(0);H=R(9,9)
    for w,code in v['weights']:
        assert type(w)==int and w>0
        if code[0]=='area':
            Z=R(code[1]);D=R(M(code[2]))/10000;b=Q(code[3],10**6)
            assert Z.nrows()==Z.rank()==2 and Z.ncols()==9 and D==D.transpose() and D[0,0]>0 and D.det()>0 and b>=0 and b*b<=4*D.det()*area
            A=Z.transpose()*D*Z
        elif code[0]=='cofactor':
            _,j,x,y=code;V=S[j];x=R(9,1,x);assert any(x.entries())
            p=V*x;q=(x.transpose()*p)[0,0];b=Q(y,10**6);assert b>0 and (b/8)**8*cap*q<=4*V.det()
            A=V-p*p.transpose()/q
        else:
            assert code[0]=='lift';Z=M(code[1]);assert Z.ncols()==9 and all(any(z) for z in code[1])
            if Z.nrows()==1:b=t
            else:
                assert Z.nrows()==3 and Z.rank()==2 and any(all(x+i*y+j*z==0 for x,y,z in zip(*code[1])) for i in (-1,1) for j in (-1,1))
                b=max(3*t,5*u/2,tri)
            A=R(Z.transpose()*Z)
        H+=(w*A)/10**6;h+=w*b/10**6
    K=R(M(v['K']))/10**6;assert K==K.transpose()
    V=R(C)*(K+H)
    z=sorted([sum(V[i,j]*C[i,j] for j in range(9)) for i in range(C.nrows())],reverse=True)
    assert len(z)>=9;loss=max(Q(0),sum(z[:9])-36-4*h)/36
    K-=loss*P
    coeff=(-K).charpoly().coeffs()
    if not all(a>0 for a in coeff) or coeff[0]<=cap:return False
    assert min(z)-4*loss>0 and sum(z[:9])-36*loss<=36+4*h
    return True
def main():
    tag=sys.argv[1];path=here/f'planes-{tag}.jsonl';prefix={};front=dict(l.split() for l in (here/'dimension13-open-after-cofactors.txt').read_text().splitlines());deps={}
    for x in 'ab':
        f=here/f'cells-{x}-audit.json';d=json.loads(f.read_bytes());deps[f.name]=sha(f);prefix.update(d['partial_prefixes'])
        for k in d['keys']:del front[k]
    seen=set();passed=[];partial={}
    for line in path.open():
        o=json.loads(line);k=o['key'];assert k in front and k not in seen;seen.add(k)
        kind,s,b=sql.execute('select kind,scale,gram from form where key=?',(k,)).fetchone();G=matrix(b);C=enumerate_min(G,s);P=R(G)*4/s;det=P.det()
        last=F(prefix[k][-1]) if k in prefix else F(0);assert last==F(o['old_prefix']);prev=last
        for l,r,v in o['pieces']:
            l,r=F(l),F(r);assert last==l<r;info=interval(kind,l,r,F(str(det)))
            if v=='empty':assert info is None
            elif not check(v,C,P,info,kind,r,det):break
            last=r
        if last**5*768>1024:passed.append(k)
        elif last>prev:partial[k]=str(last)
    (here/f'planes-{tag}-audit.json').write_text(json.dumps(dict(status='exact whole-interval coverage',source=sha(path),deps=deps,seen=sorted(seen),keys=passed,partial=partial),indent=1)+'\n')
    print(tag,len(seen),len(passed),len(partial))
if __name__=='__main__':main()
