"""Verify the radius of each marked neighborhood using two explicit projected integer directions."""
from audit_mark_vectors import here,sql,matrix,sha
from flint import fmpq_mat as R,fmpz_mat as M
from fractions import Fraction as F
import json
def main():
    a=here/'reference-neighborhoods.json';z=json.loads(a.read_bytes());out=[]
    for v in z['marks']:
        k=v['key'];kind,s,b=sql.execute('select kind,scale,gram from form where key=?',(k,)).fetchone();G=matrix(b)
        c=v['c_1e4']
        if c is None:continue
        c=F(c,10000);assert 0<c<=1
        S=4*R(G)/s;d=F(str(S.det()))
        # Use bordered determinants instead of building S inverse.
        def border(Z):
            m=len(Z);B=R(9+m,9+m)
            for i in range(9):
                for j in range(9):B[i,j]=S[i,j]
                for j in range(m):B[i,9+j]=B[9+j,i]=Z[j][i]
            return (-1)**m*F(str(B.det()))/d
        t=border([v['z']]);e=border(v['plane'])
        assert 0<t==F(v['dual_length']) and 0<e==F(v['dual_area_squared'])
        assert c**11*d>2*F(99331,100)*t*t or 4*c**11*d>9*F(99331,100)*e or kind=='trace'
        assert t<3*c*F(9799,10000)/4 or 2*e<(c*F(9799,10000))**2
        out.append(k)
    (here/'neighborhood-audit-v1.json').write_text(json.dumps({'status':'exact, Loewner-conditional only','source_sha256':sha(a),'passed_keys':out},indent=1)+'\n')
    print('neighborhoods',len(out))
if __name__=='__main__':main()
