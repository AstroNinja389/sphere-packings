"""Verify independent reverse-flag certificates with fixed lift floor and a single shared circle."""
from fractions import Fraction as F
import json,math,sys,zlib
from flint import fmpz_mat as M
from audit_mark_vectors import here,sql,matrix,sha
u=F(9799,10000)
def test(r):
    kd,s,b,p=sql.execute('select kind,scale,gram,cert from form where key=?',(r['key'],)).fetchone()
    assert r['kind']==kd=='trace' and r['orientation']=='reverse'
    G=matrix(b)
    if min(G[i,i] for i in range(9))>s:
        x=M(9,1,json.loads(zlib.decompress(p))['x']);assert any(x.entries()) and (x.transpose()*G*x)[0,0]<=s
    for step in r['steps']:
        A=M(9,9);val=F(0)
        for w,z in step['weights']:
            assert type(w)==int and w>0 and all(len(v)==9 and any(v) for v in z) and len(z) in (1,3)
            if len(z)==3:assert any(all(z[0][i]+a*z[1][i]+b*z[2][i]==0 for i in range(9)) for a in (-1,1) for b in (-1,1))
            val+=F(w,10000)*u*(F(3,4) if len(z)==1 else F(5,2));V=M(z);A+=w*(V.transpose()*V)
        q=F(4,s)*(1+val/9);h=math.lcm(q.denominator,10000)
        C=int(h*q)*G-(h//10000)*A
        # Sylvester in raw basis
        det=int(C.det())
        if 25*det<27757*h**9:continue
        if all(M(j,j,[C[i,k] for i in range(j) for k in range(j)]).det()>0 for j in range(1,9)):return True
    return False
def main():
    files=[here/k for k in sys.argv[1:]];passed=[];seen=set()
    frontier={line.split()[0] for line in (here/'flag-open-v1.txt').read_text().splitlines() if line.endswith(' reverse_trace_open')}
    for p in files:
        for line in p.open():
            r=json.loads(line);key=r['key'];assert key in frontier and key not in seen;seen.add(key)
            if test(r):passed.append(key)
    assert seen==frontier
    (here/'reverse-audit-v1.json').write_text(json.dumps({'seen':len(seen),'sha256':{p.name:sha(p) for p in files},'pass':len(passed),'excluded':sorted(passed)},indent=1)+'\n');print(len(seen),len(passed))
if __name__=='__main__':main()
