"""Forward and backward class-budget replays, with the 13th actual bin selecting the certified floor."""
import os,sys,math,json,hashlib
for var in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[var]='1'
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from flint import arb,fmpq,ctx
here=Path(__file__).resolve().parent;old=here/'geometry'
sys.path.insert(0,str(old));sys.set_int_max_str_digits(0)
def ceil(x):return -((-x.numerator)//x.denominator)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Budget:
    def __init__(self,e,table,scale,direction):
        self.j=e.index(2);self.direction=direction;self.scale=scale
        self.inc=[ceil((r-2)*scale) for r in e[self.j+1:]]
        self.lower13=[ceil(scale*max(v for a,v in table if (r-2)/2<=a)) for r in e[self.j+1:]]
    def cb(self,W,pen,cap,off,J,*unused):
        assert not unused and self.j==J
        return self.val(tuple(W[J:]),tuple(pen),tuple(cap),off)
    @lru_cache(None)
    def val(self,weights,ps,caps,offset):
        maxc=caps[-1];sc=self.scale;R=max(ceil(F(3,2)*sc),max(self.lower13))
        mag=(maxc+1)*max(map(abs,weights))+(maxc+1)**2*sum(map(abs,ps));assert mag<2**59
        ix=np.arange(R+1);need12=ceil(F(1,10)*sc);need15=ceil(F(3,2)*sc)
        if self.direction=='back':
            V=np.zeros((maxc+1,R+1),dtype=np.int64)
            for j in reversed(range(len(caps))):
                nxt=V.copy();g=caps[j];go=np.minimum(R,ix+self.inc[j]);req={12:need12,13:self.lower13[j],15:need15}
                for k in range(g,-1,-1):
                    q=k+offset;nxt[k]=V[k]-ps[j]*q*(q-1)
                    if k<g:
                        good=go>=req.get(q+1,0)
                        nxt[k,good]=np.maximum(nxt[k,good],weights[j]+nxt[k+1,go[good]])
                V=nxt
            return int(V[0,0])
        # Here the state is the best score that already achieves AT LEAST the indicated mass.
        V=np.full((maxc+1,R+1),-2**61,dtype=np.int64);V[0,0]=0
        for j,g in enumerate(caps):
            nxt=V.copy();req={12:need12,13:self.lower13[j],15:need15}
            for k in range(1,g+1):
                before=np.maximum(0,np.maximum(ix,req.get(k+offset,0))-self.inc[j])
                nxt[k]=np.maximum(V[k],nxt[k-1,before]+weights[j])
            for k in range(g+1):
                q=k+offset;nxt[k]-=ps[j]*q*(q-1)
            V=nxt
        return int(V[:,0].max())
