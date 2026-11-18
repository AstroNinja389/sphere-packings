"""Independent rational composition with backward class DP. No numerical producer imports.

Portable copy of audit_full_dimension_bound_v2.py (sha256 4f3f1790af2742e69b42df560643ef85e5d72ca71f9da72933a93dfd6a720512).
Only path handling differs: the repository root is found from this file, the bundle names its inputs relative to its
own folder, and the comparison density is read from the bundle instead of a second certificate file.
Usage: python joint/audit_joint_bound.py joint/n19/bundle.json OUTPUT.json   (OUTPUT.json must not exist)
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,math,time
from bisect import bisect_right
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'verify'))
import bernstein as vb
import mpmath as mp

def ceil(x):return -((-x.numerator)//x.denominator)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def backward(weights,penalty,caps,offset,J):
    limit=caps[-1];future=[0]*(limit+1);bad=-(10**200)
    for j in range(len(caps)-1,-1,-1):
        current=[bad]*(limit+1)
        for old in range(caps[j]+1):
            current[old]=max((k-old)*weights[J+j]-penalty[j]*(k+offset)*(k+offset-1)+future[k] for k in range(old,caps[j]+1))
        future=current
    return future[0]

def audit(bundle,output):
    start=time.time();bundle=Path(bundle);data=json.loads(bundle.read_text());n=data['n'];base=bundle.parent/data['baseline'];comparison=str(data['comparison_density']);assert F(comparison)>0
    assert sha(base)==data['baseline_sha256'];cert=vb.parse_certificate(base.read_text());assert cert.n==n
    # Verify the unchanged Fourier function and original valid majorants anew.
    p,q=vb.laguerre_pair(cert);vb.prove_polynomial_obligations(cert,p,q)
    E=list(map(F,data['E']));assert sorted(set(E))==E and set(cert.E)<=set(E) and E[0]==1 and E[-1]==cert.E[-1];J=E.index(F(2));C=2*(2**n-1)
    assert E[-1]<3 and n*(1-2/E[-1])**2<1
    raw=[g/vb.exp_partial_sum(cert.tau0*cert.E[i]/2) for i,g in enumerate(cert.Gam)]
    for i in range(len(raw)-2,cert.J-1,-1):raw[i]=max(raw[i],raw[i+1])
    weights=[C*raw[bisect_right(cert.E,e)-1] for e in E[:-1]];penalties=[F(0)]*(len(E)-1-J);bonus=F(0);dependencies={base.name:sha(base)}
    for i,cut in enumerate(data['cuts']):
        lam=F(cut['multiplier']);assert lam>=0
        if lam==0:continue
        cp=bundle.parent/cut['candidate'];cc=json.loads(cp.read_text());assert cc['n']==n
        if 'source_schur_B' in cc:from audit_schur_kernel import audit as ka
        else:from audit_joint_kernel import audit as ka
        fresh=Path(output).with_name(Path(output).stem+f'-kernel{i}.json');ka(cp,fresh);a=json.loads(fresh.read_text());dependencies[cp.name]=sha(cp);dependencies[fresh.name]=sha(fresh)
        S=F(a['source_cap']);assert S in E and S-1 in E and 2<S<=E[-1]
        diag=list(map(F,a['diagonal_local_power']));m0,m1,m2=map(F,cc['matrix_entries'][:3]);w0,w1=map(F,cc['moment_anchor']);assert m0>=0 and m2>=0 and m0*m2-m1*m1>=0
        D=[diag[0]-2*(m0*w0+m1*w1),diag[1]-2*(m1*w0+m2*w1),diag[2]];assert D[2]>=0
        beta=m0*w0*w0+2*m1*w0*w1+m2*w1*w1;assert beta>=0;bonus+=lam*beta/(2**n-1)
        for j in range(E.index(S-1)):
            lo,hi=[(x-1)/(S-2) for x in E[j:j+2]];weights[j]+=lam*max(D[0]+D[1]*lo+D[2]*lo*lo,D[0]+D[1]*hi+D[2]*hi*hi)
        B=F(cc.get('source_schur_B','0'))
        if 'source_schur_B' in cc:
            slope,cross=F(cc['source_slope']),F(cc['source_cross']);assert 0<=B<=1 and cross>=0 and cross*B>=slope*slope/4
            for j in range(E.index(S)):
                lo,hi=[max(F(-1),min(F(1),(x-2)/(S-2))) for x in E[j:j+2]];weights[j]+=lam*max(cross*lo*lo-slope*lo+B,cross*hi*hi-slope*hi+B)
        penalties[E.index(S)-1-J]+=lam*(1-B)
    # Directed integer rounding: upper weights, lower nonnegative penalties.
    den=10**16;W=[ceil(x*den) for x in weights];pen=[(x*den).numerator//(x*den).denominator for x in penalties];assert min(pen)>=0
    caps0=[vb.long_cap(n,s) for s in E[J+1:]];values=[backward(W,pen,caps0,0,J)];cap_rows=[caps0]
    for j,t in enumerate(E[1:J+1]):
        caps=[vb.short_cap(n,t,s) for s in E[J+1:]];cap_rows.append(caps);values.append(W[j]+backward(W,pen,caps,1,J))
    budget=F(max(values),den)+bonus;rho=(p[0]+budget)/q[0];assert rho>0
    mp.mp.dps=70;r=mp.mpf(rho.numerator)/rho.denominator;t=mp.mpf(cert.tau0.numerator)/cert.tau0.denominator
    density=(t/8)**(mp.mpf(n)/2)*r/mp.gamma(mp.mpf(n)/2+1);hermite=t/(2*mp.pi)*r**(mp.mpf(2)/n)
    ds=mp.nstr(density*(1+mp.mpf('1e-11')),14);hs=mp.nstr(hermite*(1+mp.mpf('1e-11')),14)
    from dataclasses import replace
    checked=replace(cert,density=F(ds),hermite=F(hs),density_text=ds,hermite_text=hs);vb.check_claims(checked,rho)
    out={'status':'PASS_INDEPENDENT_GENERAL_DIMENSION_JOINT_DENSITY','n':n,'density':ds,'hermite':hs,'comparison_density':comparison,'gain_percent':float((1-F(ds)/F(comparison))*100),'class_budget_scaled':str(budget),'rho':str(rho),'classes_checked':len(values),'caps_sha256':hashlib.sha256(json.dumps(cap_rows).encode()).hexdigest(),'integer_branch_maxima':list(map(str,values)),'rounding_denominator':den,'dependencies':dependencies,'bundle_sha256':sha(bundle),'auditor_sha256':sha(__file__),'seconds':time.time()-start,'scope':'Universal lattice upper bound; complete backward class DP, actual parity half-vector kernel signs, source PSD identities, positive root moment bonus, unchanged independently verified Fourier function. No lattice or extremality assumption.'}
    path=Path(output);assert not path.exists();path.write_text(json.dumps(out,indent=2)+'\n');print('DIMENSION_CERTIFIED',n,'density',ds,'gain',out['gain_percent'],'seconds',round(out['seconds'],2),flush=True)
    return out

if __name__=='__main__':
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
    audit(sys.argv[1],sys.argv[2])
