"""0515 small sampled cardinal-torus audit, NOT a supremum certificate."""
import importlib.util
from pathlib import Path
import resource
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('cx2_box_inert',HERE/'box_replay_cx2v001.py')
B=importlib.util.module_from_spec(sp);sys.modules[sp.name]=B;sp.loader.exec_module(B)
sys.path.insert(0,str(B.ART/'tail_scheme_impl_c2/certificates_v002/tools'))
import certs2_common_c2v002 as C2
start=time.monotonic();co,points,base=B.setup()
base['producer']=B.pin(Path(__file__));base['helper']=B.pin(HERE/'box_replay_cx2v001.py')
base['envelope_helper']=B.pin(Path(C2.__file__))
L,anchor,info,(grid,Cb,mu)=B.CC.qinf_binder()
dirs=B.CC.direction_sets(L)[1];torus=C2.torus_grid_v(4)
kvalues=[4.,4.5,5.,8.,32.,64.,128.,182.]
combos=sorted({(p['gamma_over_Eref'],p['ell_F_m']) for p in points})
EB=co['Eref_base_J']['trial_value'];s=co['common_scale_s']['trial_value']
ev,V=np.linalg.eigh(Cb);isq=(V/np.sqrt(ev))@V.T
out=[];selftests=[]
for j,(r,ell) in enumerate(combos):
    binder=L.Binder(grid,Cb,mu,Eref=s*EB,ell=ell,gam=s*r*EB)
    E=C2.Envelope(L,binder);nr=len(torus);nd=len(dirs)
    t=np.tile(torus,(nd,1));rows=[]
    for k in kvalues:
        kv=np.repeat(dirs*k/L.KPC,nr,axis=0)
        x=C2.env_full(E,kv,t)
        q=4*binder.gam*np.sum(kv*kv,axis=1)*x[:,0]
        dev=np.abs(1-q);a=int(np.argmax(dev))
        gh=isq@B.LO.mandel_mat(x[:,1:7])@isq
        rho=np.linalg.norm(gh,ord=2,axis=(1,2))*4*binder.gam*np.sum(kv*kv,axis=1)
        z=int(np.argmax(rho))
        rows.append({'k_inverse_kpc':k,'sampled_envelope_eps':float(dev[a]),
            'eps_argmax_direction':dirs[a//nr].tolist(),'eps_argmax_t':torus[a%nr].tolist(),
            'sampled_envelope_rho':float(rho[z]),'rho_argmax_direction':dirs[z//nr].tolist(),
            'rho_argmax_t':torus[z%nr].tolist()})
    probe=dirs*4.5/L.KPC
    d=np.max(np.abs(E.q(probe,E.t_of(probe))-B.CC.q_of(binder,probe)))
    selftests.append({'pair':j,'max_abs_env_actual_q_difference':float(d)})
    out.append({'pair_index':j,'gamma_over_Eref':r,'ell_F_m':ell,'rows':rows,
                'max_sampled_envelope_eps':max(v['sampled_envelope_eps'] for v in rows)})
    print('envelope spot %d/%d eps %.6g %.1fs'%(j+1,len(combos),out[-1]['max_sampled_envelope_eps'],time.monotonic()-start),flush=True)
base.update(status='TESTED_SAMPLED_ENVELOPE_SPOTS_NOT_CERTIFIED_SUP',
    direction_count=len(dirs),torus_points=len(torus),k_values_inverse_kpc=kvalues,
    pairs=out,selftests=selftests,max_env_actual_difference=max(x['max_abs_env_actual_q_difference'] for x in selftests),
    worst=max(out,key=lambda x:x['max_sampled_envelope_eps']),
    limitations=['Finite direction/torus/radial grid; maxima are lower bounds on supremum',
      'No Lipschitz/global optimization certificate; cannot satisfy production EPS envelope rule',
      'Full shell coverage still requires perpoint certificate producer'],
    seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
h=B.write('BOX_ENVELOPE_SPOT_REPLAY_CX2V001.json',base)
print({'sha256':h,'max_eps':base['worst']['max_sampled_envelope_eps'],'seconds':base['seconds'],'rss':base['peak_rss_bytes']})
