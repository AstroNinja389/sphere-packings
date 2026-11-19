"""Independent exact test using only integer lengths, correlated lift triples and admissible traces."""
import hashlib,json,math,sqlite3,struct,sys
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
from flint import fmpz_mat as M
here=Path(__file__).resolve().parent
from database import database_path, DATABASE_SHA256
sql=sqlite3.connect(database_path().as_uri()+'?mode=ro&immutable=1',uri=True)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def matrix(blob):
    G=M(9,9);a=iter(struct.unpack('<45h',blob))
    for i in range(9):
        for j in range(i,9):G[i,j]=G[j,i]=next(a)
    return G
def check(r):
    kind,s,blob=sql.execute('select kind,scale,gram from form where key=?',(r['key'],)).fetchone()
    assert kind==r['kind'];G=matrix(blob);assert min(G[i,i] for i in range(9))<=s
    E=F(99331,100);floor=F(768 if kind=='virtual' else 1113)
    e=F(4,s)**9*int(G.det())
    for step in r['steps']:
        # The direct flag has u>=3d/(4E) and t>=2d/(3E); the reversed flag has u>9799/10000.
        # In either flag e<=1133u and t>=3u/4.
        rev=F(9799,10000);u=min(rev,max(e/1133,3*floor/(4*E)))
        t=min(3*rev/4,max(3*u/4,2*floor/(3*E)))
        beta=F(0);A=M(9,9)
        for weight,vec in step['weights']:
            assert type(weight)==int and weight>0 and len(vec) in (1,3) and all(len(x)==9 and any(x) and all(type(v)==int for v in x) for x in vec)
            if len(vec)==3:
                assert any(all(vec[0][j]+a*vec[1][j]+b*vec[2][j]==0 for j in range(9)) for a in (-1,1) for b in (-1,1))
                value=max(3*t,F(5,2)*u)
            else:value=t
            beta+=value*weight/10000
            V=M(vec);A+=weight*(V.transpose()*V)
        coeff=F(4,s)*(1+beta/9)
        den=math.lcm(coeff.denominator,10000)
        B=(den*coeff.numerator//coeff.denominator)*G-(den//10000)*A
        co=(-B).charpoly().coeffs()
        if not all(v>0 for v in co):return False
        actual=F(int(co[0]),den**9)
        if actual>=F(27757,25):return True
        trial=F(step['next_e100'],100)
        if trial>actual:break
        e=max(e,trial)
        l,h=0,1134
        while h-l>1:
            m=(h+l)//2
            if m**4*4**5<=e**5:l=m
            else:h=m
        floor=max(floor,l)
    return False
def run(path):
    passed=[];stats=Counter()
    with path.open() as stream:
        for line in stream:
            r=json.loads(line);ok=check(r);stats[r['kind']+('_pass' if ok else '_open')]+=1
            if ok:passed.append(r['key'])
    assert len(set(passed))==len(passed)
    dest=path.with_suffix('.audit.json');dest.write_text(json.dumps({'status':'exact successful determinant exclusions','source_sha256':sha(path),'database_sha256':DATABASE_SHA256,'counts':stats,'excluded':sorted(passed)},indent=1)+'\n')
    print(stats,flush=True)
if __name__=='__main__':run(here/sys.argv[1])
