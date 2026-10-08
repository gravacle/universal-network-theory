"""Fixed baryonic reconstruction: measurements plus explicit endpoint models."""
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
DISTANCE_MPC = 13.8
G_KPC_KMS2_MSUN = 4.30091e-6
A0_KMS2_KPC = 1.2e-10*3.085677581491367e19/1e6
HI_ARCMIN = np.arange(24)/2
# Independently visually verified against Begeman1989 Table3, printed p55.
HI_BARE = np.array([3.17,3.88,4.53,4.97,5.24,5.19,4.73,3.95,3.26,2.94,
                    2.66,2.29,2.12,1.98,1.62,1.27,1.14,1.11,1.01,.86,
                    .72,.57,.36,.14])
HI_RADII = HI_ARCMIN*DISTANCE_MPC*1000*math.pi/(180*60)
ROWS = json.loads((ROOT/'NGC3198_BARYON_INPUT.json').read_text())['rows']


class Profile:
    def __init__(self,radii,surface,tail_scale):
        self.r = np.array(radii,dtype=float)
        self.s = np.array(surface,dtype=float)
        self.tail = tail_scale
        if self.r[0] > 0:
            self.r = np.r_[0.,self.r]
            self.s = np.r_[self.s[0],self.s]
        assert np.all(np.diff(self.r)>0) and np.all(self.s>=0)

    def sigma(self,radius):
        radius = np.asarray(radius)
        result = np.interp(radius,self.r,self.s,left=self.s[0],right=0.)
        if self.tail is not None:
            result = np.where(radius>self.r[-1],
                  self.s[-1]*np.exp(-np.maximum(radius-self.r[-1],0)/self.tail),result)
        return result

    def integral(self,lower,upper):
        """Integral R Sigma(R)dR in kpc^2 Msun/pc^2; exact chosen interpolant."""
        lower,upper = np.broadcast_arrays(np.asarray(lower,dtype=float),np.asarray(upper,dtype=float))
        assert np.all(lower>=0) and np.all(upper>=lower)
        out = np.zeros_like(lower)
        for left,right,sigma,next_sigma in zip(self.r,self.r[1:],self.s,self.s[1:]):
            a = np.maximum(lower,left)
            b = np.minimum(upper,right)
            width = np.maximum(b-a,0.)
            slope = (next_sigma-sigma)/(right-left)
            start_sigma = sigma+slope*(a-left)
            out += width*(a*start_sigma+(a*slope+start_sigma)*width/2+slope*width**2/3)
        if self.tail is not None:
            a = np.maximum(lower,self.r[-1])
            b = np.maximum(upper,self.r[-1])
            scale = self.tail
            def primitive(x):
                finite = np.where(np.isfinite(x),x,self.r[-1])
                value = scale*(finite+scale)*np.exp(-(finite-self.r[-1])/scale)
                return np.where(np.isfinite(x),value,0.)
            out += self.s[-1]*(primitive(a)-primitive(b))
        return out


def profiles(hi_tail,h2_tail):
    star_r = [row['radius_kpc'] for row in ROWS]
    star_s = [row['stars_Msun_pc2'] for row in ROWS]
    molecular = [row for row in ROWS if row['H2_Msun_pc2'] is not None]
    hi_scale = (HI_RADII[-1]-HI_RADII[-2])/math.log(HI_BARE[-2]/HI_BARE[-1]) if hi_tail else None
    return {'HI_He':Profile(HI_RADII,1.36*HI_BARE,hi_scale),
            'stars':Profile(star_r,star_s,3.2),
            'H2_He':Profile([row['radius_kpc'] for row in molecular],
                            [row['H2_Msun_pc2'] for row in molecular],2.7 if h2_tail else None)}


def masses(components):
    return {name:float(2*math.pi*1e6*p.integral(0.,np.inf)) for name,p in components.items()}


def bottom_flux(edges,components):
    integral = sum(p.integral(edges[:-1],edges[1:]) for p in components.values())
    return 2*math.pi*1e6*G_KPC_KMS2_MSUN/A0_KMS2_KPC*integral
