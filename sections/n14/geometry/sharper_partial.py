"""Use finite group orders, the zero character, and exact circle/interval capacities."""
from codim_one import *
from math import exp,sqrt
def check(m,cap,det_cap=310):
    b1=Q(0);b2=Q(0);n=13
    for z in vertices(n,m,cap):
        A=fmpq_mat([[Q(str(1+x if i==j else -(x+y)/2)) for j,y in enumerate(z)] for i,x in enumerate(z)])
        for j in range(1,14):assert fmpq_mat([[A[k,l] for l in range(j)] for k in range(j)]).det()>0
        T=A.inv();b1=max(b1,max(T[i,i] for i in range(n)));b2=max(b2,max(T[i,i]+T[j,j]+2*T[i,j] for i,j in combinations(range(n),2)))
    ctx.prec=160;a=arb(Q(729,4))**(arb(13)/11);e=arb(Q(str(m))).exp()
    # Shortest-squared-two normalization in rank 13.
    jmax=int(float((arb(2)**(arb(15)/2)*e.sqrt()/a.sqrt())))
    assert arb(2)**(arb(15)/2)*e.sqrt()/a.sqrt()<jmax+1
    sq=[(2*a-det_cap*arb(b))/(2**16*e) for b in [b1,b2]]
    if min(map(float,sq))<=0:return dict(m=str(m),passed=False)
    # Rational *lower* spacings, rounded strictly downward by the Arb check.
    denom=10**8;rr=[int(float(v.sqrt())*denom)-1 for v in sq]
    assert all(r>0 and v>arb(Q(r,denom))**2 for r,v in zip(rr,sq))
    ray,sep=[F(i,denom) for i in rr];rows=[]
    for j in range(1,jmax+1):
        for t in [1,2,4]:
            if j%t or (j//t)%2==0 and t==1 or (j-t)%2:continue
            # 2-torsion has the indicated size. Odd-order groups have t=1.
            if j%2 and t!=1:continue
            ell=j*sep;r=j*ray
            non=max(1,int(1//ell))
            folded=1+int(F(1,2)//ell)
            zero=max(0,1+int((F(1,2)-r)//ell))
            N=zero+(t-1)*folded+(j-t)//2*non
            rows.append([j,t,N])
    return dict(m=str(m),u=str(cap),inverse_single=str(b1),inverse_pair=str(b2),jmax=jmax,single_spacing=str(ray),pair_spacing=str(sep),capacities=rows,worst=max(row[-1] for row in rows),passed=all(row[-1]<13 for row in rows),ambient_det_cap=det_cap)
if __name__=='__main__':
    for arg in sys.argv[1:]:
        m=F(arg);v=check(m,m)
        print(arg,v.get('worst'),v.get('capacities'),flush=True)
        (H/f'partial-interval-{m.numerator}-{m.denominator}.json').write_text(json.dumps(v,indent=2)+'\n')
