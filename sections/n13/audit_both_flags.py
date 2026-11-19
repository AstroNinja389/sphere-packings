"""Reconstruct all imported witnesses and verify the two flag orientations separately."""
import hashlib,json,sqlite3,struct,time,zlib
from pathlib import Path
from collections import Counter
from flint import fmpz_mat as M

home=Path(__file__).resolve().parent
from database import database_path, DATABASE_SHA256
db=database_path()
cap=1133
# rational lower bound on min of the balanced dual, for the reversed orientation only
a,b=9799,10000
assert a**5*cap<4**5*b**5
# exact direct KZ obstruction for d_old=4*972^(9/11), E<=99331/100
# E < (2/9)*d_old^(6/5)
assert (9*99331)**55 < (2*100)**55*4**66*972**54
assert 4**11*972**9 < cap**11

def write(path,value):
    dest=home/path;temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(value,indent=1)+'\n');temp.replace(dest)

def run():
    with db.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==DATABASE_SHA256
    con=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True)
    pair=[(i,j) for i in range(9) for j in range(i,9)]
    start=time.monotonic();stat=Counter();shards=[Counter() for _ in range(64)]
    keyset=hashlib.sha256();n=0
    with (home/'flag-open-pending.txt').open('w',encoding='ascii',newline='\n') as out:
        sql="select key,scale,gram,kind,case when kind='trace' then cert end from form order by id"
        for key,s,data,kind,payload in con.execute(sql):
            s=int(s);flat=struct.unpack('<45h',data)
            g=[[0]*9 for j in range(9)]
            for (i,j),v in zip(pair,flat):g[i][j]=g[j][i]=v
            G=M(g);dg=int(G.det());m=min(g[i][i] for i in range(9));assert dg>0 and m>0
            n+=1
            if 25*4**9*dg>=27757*m**9: typ='cutoff'
            elif kind!='trace': typ=kind
            else:
                o=json.loads(zlib.decompress(payload));D=o['D'];T=M(o['U']);weights=o['c'];S=s*D
                assert T.nrows()==T.ncols()==9 and abs(T.det())==1 and s>0 and D>0
                if m>s:
                    x=M(9,1,o['x']);assert any(x.entries()) and (x.transpose()*G*x)[0,0]<=s
                Z=M(o['z']); assert Z.ncols()==9 and Z.nrows()==len(weights)>0 and min(weights)>0
                assert all(any(row) for row in o['z'])
                weighted=M([[w*z for z in row] for row,w in zip(o['z'],weights)])
                H=(T*G*T.transpose())*D-weighted.transpose()*Z
                # Positive characteristic coefficients of det(xI+H), H real symmetric.
                coeff=(-H).charpoly().coeffs()
                assert len(coeff)==10 and all(v>0 for v in coeff)
                h=int(coeff[0]);c=sum(weights)
                # d >= (3/4)(10/9)^10 * 4^10 * c * h / S^10
                num=3*10**10*4**9*c*h;den=9**10*S**10
                assert num**11>=4**11*972**9*den**11
                if num>=cap*den:typ='old_witness_strong_enough'
                else:
                    # det Q >= det R/(1-uW/12)^9 > 27757/25?
                    # W=4c/S, det R=4^9 h/S^9
                    slack=3*b*S-a*c
                    if slack<=0 or 25*(12*b)**9*h>=27757*slack**9:
                        typ='both_flags_by_lift'
                    else:
                        typ='reverse_trace_open'
            if typ not in ('cutoff','old_witness_strong_enough','both_flags_by_lift'):
                line=key+' '+typ+'\n';out.write(line);keyset.update(line.encode())
            stat[typ]+=1;shards[int(key[:4])][typ]+=1
            if n%100000==0:write('flag-progress.json',dict(rows=n,counts=stat,seconds=time.monotonic()-start))
    assert n==4487813 and n-stat['cutoff']==1746860 and stat['old_witness_strong_enough']==1042245
    out.close();(home/'flag-open-pending.txt').replace(home/'flag-open-v1.txt')
    write('two-flag-audit-v1.json',dict(status='exact, external census completeness as cited',input_sha256=DATABASE_SHA256,
         rows=n,counts=stat,per_shard=shards,open_key_sha256=keyset.hexdigest(),seconds=time.monotonic()-start))
    print(stat,flush=True)
if __name__=='__main__':run()
