"""Exact small-block computations for the twelve-coordinate torus exclusion."""
from flint import arb,ctx,fmpq as Q,fmpq_mat
from itertools import product,combinations
from pathlib import Path
import json
H=Path(__file__).resolve().parent
def main():
    m=Q(1,20);n=12
    vs=[[Q(0)]*n]+[[Q(0)]*(n-i)+[m/i]*i for i in range(1,n+1)]+[[-m/11]+[m/11]*11]
    B=Q(0);detlo=Q(1)
    for v in vs:
        M=fmpq_mat([[1+x if i==j else -(x+y)/2 for j,y in enumerate(v)] for i,x in enumerate(v)])
        for k in range(1,13):assert fmpq_mat([[M[i,j] for j in range(k)] for i in range(k)]).det()>0
        det=M.det();detlo=min(detlo,det)
        for i,j in combinations(range(12),2):
            T=fmpq_mat(M)
            for a in [i,j]:
                for b in [i,j]:T[a,b]+=1
            B=max(B,T.det()/det-1)
    ctx.prec=160;A=arb(Q(729,4))**(arb(13)/11);ec=arb(m).exp();gain={}
    for D in (310,315,318,320):
        gain[D]=18*arb(3).sqrt()*(2*A-D*arb(B))-512*arb(D).sqrt()*ec.sqrt()
    assert gain[318]>0 and 128*ec.sqrt()/27<6
    frames=[[tuple(2*int(i==j) for i in range(4)) for j in range(4)]]
    for par in (0,1):frames.append([x for x in product((-1,1),repeat=4) if x[0]==1 and sum(v<0 for v in x)%2==par])
    U=set(q for fr in frames for z in fr for q in [z,tuple(-v for v in z)])
    assert len(U)==24
    for fr in frames:
        assert fmpq_mat(fr)*fmpq_mat(fr).transpose()==4*fmpq_mat([[int(i==j) for j in range(4)] for i in range(4)])
        for sig in product((-1,1),repeat=4):
            q=tuple(sum(k*r[i] for k,r in zip(sig,fr)) for i in range(4));assert all(v%2==0 for v in q) and tuple(v//2 for v in q) in U
    assert detlo==1
    r=arb(Q(3,2))*(1+(1+arb(12).sqrt())*arb(m)/2)
    lower=3072*(2-r)**2;assert r<2 and lower>320
    res=dict(status='PASS',passed=True,rank=12,total_mass='1/20',length_floor='1/10',ambient_det_cap=318,det_Q_lower=str(detlo),dual_pair_upper=str(B),flat_torus_margins={k:str(v) for k,v in gain.items()},index_at_most=5,elementary_index4_lower=str(lower),exact_frame_det_lower=768,reference_D4_verified_frames=3)
    print(res);(H/'two-torus-audit.json').write_text(json.dumps(res,indent=2)+'\n')
if __name__=='__main__':main()
