"""Linear partition of a built cube-kept cylindrical tail into radial unit shells.
Reuses source factors and exact corner-family convention. No module file is modified.
All requested radii must be precomputed; the caller uses only those radii.
"""
import copy,math
import numpy as np

def filter_state(U,st,lo,hi,radii):
    a=st._a;kp=a['kp'];kz=a['kz'];nz=len(kz);radii=np.asarray(radii,float)
    arr=dict(a);out=np.zeros((len(radii),3,nz),complex);jn=st._provider();KPC=U.KPC_M
    for s0 in range(0,len(kp),U._block_rows(nz)):
        sl=slice(s0,min(s0+U._block_rows(nz),len(kp)));k=kp[sl]
        mag=np.hypot(k[:,None],kz[None,:])*KPC;mask=(mag>=lo)&(mag<hi)
        if not np.any(mask):continue
        c0=U._c0_D(st.record['kept'],st.record['outer'],k*KPC,kz*KPC)
        fac=(st.record['pref']*a['wkp'][sl]*k)[:,None]*a['wz'][None,:]/(k[:,None]**2+kz[None,:]**2)*c0*mask
        sr=a['P'][sl]@a['F'].real.T;si=a['P'][sl]@a['F'].imag.T
        ar=sr*fac;ai=si*fac;x=np.outer(radii,k)
        j0=jn.j0(x);j1=jn.j1(x);j2=jn.jn(2,x)
        for d,b in enumerate((j0,-k[None,:]*j1,k[None,:]**2*(j2-j0)/2)):
            out[:,d,:]+=b@ar+1j*(b@ai)
    arr['ring_radii_m']=radii;arr['ring_tables']=out
    for fi,fam in enumerate(st.record['families']):
        cm=a[f'corner_M_{fi}'];cp=a[f'corner_kp_{fi}'];mag=np.hypot(cp[:,None],kz[None,:cm.shape[1]])*KPC
        arr[f'corner_M_{fi}']=cm*((mag>=lo)&(mag<hi))
    if 'sph_A' in a:raise ValueError('SHELL_FILTER_CUBE_KEPT_ONLY')
    rec=copy.deepcopy(st.record);rec['diagnostic_shell_inverse_kpc']=[lo,hi]
    return st.__class__(empty=False,record=rec,arrays=arr,jn_provider=jn)
