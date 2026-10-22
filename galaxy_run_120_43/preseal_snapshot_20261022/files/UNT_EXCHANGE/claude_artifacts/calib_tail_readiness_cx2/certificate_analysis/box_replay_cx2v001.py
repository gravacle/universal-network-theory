"""0515 bounded calibration-box saved/static replay, no solver launches.

Modes symbol and gq write separate immutable outputs. Only NumPy + stdlib.
Symbol outputs are finite-grid estimates, NOT box-wide certificates. LO holds
the saved C4R3 source, row speeds and radii fixed and scales existing B1 values.
GQ is the stronger positive-mass all-column radial bound at every production kp.
"""
import datetime
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
TOOLS = ART/'tail_scheme_impl_c2/certificates_v001/tools'
sys.path.insert(0,str(TOOLS))
import certs_common_c2v001 as CC
import lo_cert_c2v001 as LO

SPEC = ART/'calibration_orchestrator_c2/DDO154_CALIBRATION_COORDINATE_SPEC_V001.json'
ADD = ART/'calibration_orchestrator_c2/v005/COORDINATE_SPEC_ADDENDUM_V005.json'
ENGINE = ART/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py'
LOFILE = ART/'tail_scheme_impl_c2/certificates_v002/gates/LO_CERT_V002.json'
WAIVER = 'nice unavailable (sandbox); 0514 waiver'
def pin(p):
    return {'path':str(p),'sha256':CC.sha(p)}
def write(name,obj):
    raw=(json.dumps(obj,indent=1,allow_nan=False)+'\n').encode()
    with (HERE/name).open('xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def setup():
    CC.require_env()
    s=load(SPEC); a=load(ADD)
    assert CC.sha(SPEC)==a['applies_to_coordinate_spec_sha256']
    co={x['name']:x for x in s['coordinates']}
    assert a['coordinate_mode']['free_coordinates']==['common_scale_s','gamma_over_Eref','ell_F_m']
    names=a['coordinate_mode']['free_coordinates']
    def at(n,u):
        c=co[n]
        if u==0:return c['lower']
        if u==1:return c['upper']
        return math.exp(math.log(c['lower'])+u*(math.log(c['upper'])-math.log(c['lower'])))
    us=list(itertools.product((0.,1.),repeat=3))+list(itertools.product((.25,.5,.75),repeat=3))
    pts=[dict(point='corner_%02d'%i if i<8 else 'interior_%02d'%(i-8),u=list(u),
          **{n:at(n,x) for n,x in zip(names,u)},Eref_base_J=co['Eref_base_J']['trial_value'],
          distance_Mpc=4.04,inclination_deg=66.0) for i,u in enumerate(us)]
    base={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'producer':pin(Path(__file__)),
          'waiver':WAIVER,'coordinate_spec':pin(SPEC),'coordinate_addendum':pin(ADD),'engine':pin(ENGINE),
          'grid_declaration':{'coordinates':names,'corners':'{0,1}^3 (8 points)',
             'strict_interior':'{0.25,0.5,0.75}^3 (27 points), uniform in engine log-box coordinates',
             'distance':'headline fixed4.04; D endpoints only separate GQ sensitivity',
             'Eref':'fixed trial value; placeholder box NOT treated as free',
             'inclination':'fixed66; driver forbids redeprojection'},
          'points':pts,'env':{k:os.environ.get(k) for k in CC.THREAD_ENV}}
    return co,pts,base

def symbol():
    start=time.monotonic(); co,pts,base=setup()
    L,anchor,info,(grid,Cb,mu)=CC.qinf_binder()
    reproduction=CC.repro_qinf_anchor(L,anchor)
    assert reproduction['bitwise_equal']
    dirs=CC.direction_sets(L)[1]
    records=load(LOFILE); EB=co['Eref_base_J']['trial_value']
    sref=co['common_scale_s']['trial_value']
    # Base/replay records contain actual saved velocities, not target velocities.
    v=np.asarray(records['v_state_km_s']); R=np.asarray(records['R_kpc'])*L.KPC
    tau=np.asarray(records['tau_km_s'])
    ev,V=np.linalg.eigh(Cb); isq=(V/np.sqrt(ev))@V.T
    combos=sorted({(p['gamma_over_Eref'],p['ell_F_m']) for p in pts})
    # Every unit shell, closed endpoints and geometric midpoint, 52 directions.
    ranges=[(float(i),float(i+1)) for i in range(4,182)]
    kval=np.array([x for lo,hi in ranges for x in (lo,math.sqrt(lo*hi),hi)])
    kv=(kval[:,None,None]*dirs[None,:,:]/L.KPC).reshape(-1,3)
    eps_rows=[]; rho_rows=[]; scaling=[]
    def full(B,kv):return CC.full_response(B,kv,chunk=512)
    for j,(r,ell) in enumerate(combos):
        B=L.Binder(grid,Cb,mu,Eref=sref*EB,ell=ell,gam=sref*r*EB)
        x=full(B,kv); q=4*B.gam*np.sum(kv*kv,axis=1)*x[:,0]
        dev=np.abs(1-q).reshape(len(ranges),-1)
        ss=[]
        for n,(lo,hi) in enumerate(ranges):
            k=int(np.argmax(dev[n])); row=n*len(dirs)*3+k
            ss.append({'range_inverse_kpc':[lo,hi],'sampled_eps':float(dev[n,k]),
                       'k_argmax_inverse_kpc':(kv[row]*L.KPC).tolist()})
        imax=int(np.argmax(dev)); si,di=np.unravel_index(imax,dev.shape)
        eps_rows.append({'gamma_over_Eref':r,'ell_F_m':ell,'shells':ss,
                         'max_sampled_eps':float(dev.max()),'argmax_shell':list(ranges[si]),
                         'max_abs_imag_q':float(np.max(np.abs(q.imag)))})
        rs=[]
        for sh in records['shells'][:9]:
            lo,hi=sh['range_inverse_kpc']
            # Include the high-frequency range of enclosing saved-B1 shells.
            kk=np.array([lo,math.sqrt(lo*hi),hi])
            waves=(kk[:,None,None]*dirs[None,:,:]/L.KPC).reshape(-1,3)
            waves=waves[np.max(np.abs(waves),axis=1)*L.KPC>4*(1+1e-12)]
            xx=full(B,waves)
            gh=isq@LO.mandel_mat(xx[:,1:7])@isq
            vals=np.linalg.norm(gh,ord=2,axis=(1,2))*4*B.gam*np.sum(waves*waves,axis=1)
            index=int(np.argmax(vals))
            rs.append({'range_inverse_kpc':[lo,hi],'sampled_rho':float(vals[index]),
                       'k_argmax_inverse_kpc':(waves[index]*L.KPC).tolist(),
                       'saved_B1_per_m':sh['B1_per_m']})
        rho_rows.append({'gamma_over_Eref':r,'ell_F_m':ell,'shells':rs})
        # Scaling explicitly replayed at 52 directions at |k|4.5 for both s ends
        # and a doubled Eref with r held fixed (not a free coordinate).
        probe=dirs*4.5/L.KPC; ref=CC.q_of(B,probe)
        for tag,scale,eb in [('s_lower',co['common_scale_s']['lower'],EB),
                             ('s_upper',co['common_scale_s']['upper'],EB),('Eref_x2',sref,2*EB)]:
            bb=L.Binder(grid,Cb,mu,Eref=scale*eb,ell=ell,gam=scale*r*eb)
            qq=CC.q_of(bb,probe)
            scaling.append({'pair':j,'case':tag,'max_abs_q_change':float(np.max(np.abs(qq-ref)))})
        print('symbol pair %d/%d eps %.6g elapsed %.1fs'%(j+1,len(combos),dev.max(),time.monotonic()-start),flush=True)
    results=[]
    for p in pts:
        j=combos.index((p['gamma_over_Eref'],p['ell_F_m']))
        geff=p['common_scale_s']*p['gamma_over_Eref']*EB
        amp=anchor.gam/geff
        shares=[]
        for sh in rho_rows[j]['shells']:
            d=v*R*sh['sampled_rho']*sh['saved_B1_per_m']*amp/(4*tau)
            shares.append({'range_inverse_kpc':sh['range_inverse_kpc'],'max_over_tau':float(d.max()),
                           'row_argmax_1based':int(np.argmax(d))+1})
        candidates={}
        for kb,n in ((64,8),(128,9)):
            selected=shares[:n]
            candidates[str(kb)]={'enclosing_shell_endpoint':selected[-1]['range_inverse_kpc'][1],
                'max_shell_over_tau':max(s['max_over_tau'] for s in selected),
                'sum_max_over_tau':sum(s['max_over_tau'] for s in selected),
                'finite_sample_thresholds_pass':all(s['max_over_tau']<=.005 for s in selected) and sum(s['max_over_tau'] for s in selected)<=.05}
        results.append({'point':p['point'],'pair_index':j,'gamma_eff':geff,
                        'Qinf':CC.C**4/(16*math.pi*CC.G*geff),'LO_saved_source_scaling':amp,
                        'EPS_sampled_max':eps_rows[j]['max_sampled_eps'],'LO_fixed_state':candidates,'shell_shares':shares})
    base.update(status='TESTED_FINITE_GRID_ESTIMATES_NOT_BOX_CERTIFICATE',
        labels={'EPS':'finite52-direction 3-radii/unit-shell samples; no cardinal-torus envelope maximization; lower-bound estimate of supremum',
                'LO':'fixed saved C4R3 source/rows; sampled rho and existing quadrature B1 scaled1/gamma; enclosing shells; NOT solved states',
                'production':'UNTESTED absent perpoint state and complete envelope proof; use fail-closed rule'},
        qinf_anchor_reproduction=reproduction,anchor_info=info,LO_B1_source=pin(LOFILE),
        direction_count=len(dirs),symbol_pairs=len(combos),EPS=eps_rows,rho=rho_rows,point_results=results,
        scaling_checks=scaling,max_scaling_abs_q_change=max(x['max_abs_q_change'] for x in scaling),
        EPS_worst=max(results,key=lambda x:x['EPS_sampled_max']),
        LO_worst={str(k):max(results,key=lambda x:x['LO_fixed_state'][str(k)]['max_shell_over_tau']) for k in (64,128)},
        seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    h=write('BOX_SYMBOL_LO_REPLAY_CX2V001.json',base)
    print(json.dumps({'sha256':h,'seconds':base['seconds'],'rss':base['peak_rss_bytes'],
      'EPS_max':base['EPS_worst']['EPS_sampled_max'],'scale_q_abs':base['max_scaling_abs_q_change']}))

def gq():
    start=time.monotonic(); co,pts,base=setup()
    U,RS,PV=CC.uvt_modules(); jn=PV.create_provider()
    prof=load(Path(CC.PINS['profile'][0])); oldedges=np.asarray(prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'])
    kept=U.kept_region('route_a',None,4/U.KPC_M)
    quad={'order':8,'w_perp_max_inverse_kpc':.05,'w_z_max_inverse_kpc':.02}
    grids={kb:U._grid(kept,{'shape':'cylinder','K_big_inverse_kpc':float(kb)},quad,14.2)['kp'] for kb in (64,128)}
    union=np.unique(np.concatenate(list(grids.values())))
    cases=[]
    for D in (4.04,co['distance_Mpc']['lower'],co['distance_Mpc']['upper']):
        # Geometry rescaling only, no new hydrostatic state. Pi does not use mass/z.
        edges=oldedges*(D/4.04)**2
        radii,rdr=RS.annulus_columns(edges,U.KPC_M)
        n=len(radii)
        args=dict(s_edges_kpc2=edges,kpc_m=U.KPC_M,column_R_m=radii,column_rdr_m2=rdr,
                  present=np.ones(n,bool),elements_z=[np.zeros(1) for _ in range(n)],elements_m=[np.ones(1) for _ in range(n)])
        A=RS.GasColumns(M_s=64,**args);B=RS.GasColumns(M_s=128,**args)
        exact=2*math.pi*np.asarray(rdr)
        p0A=A.radial_factors(np.array([0.]),jn.j0)[0];p0B=B.radial_factors(np.array([0.]),jn.j0)[0]
        zerr=float(max(np.max(np.abs(p0A/exact-1)),np.max(np.abs(p0B/exact-1))))
        # Process 256 kp values at once; bounded provider transient arrays.
        worst={kb:{'raw':0.,'kp':None,'column_1based':None} for kb in grids}
        for k0 in range(0,len(union),256):
            kp=union[k0:k0+256]
            aa=A.radial_factors(kp/U.KPC_M,jn.j0);bb=B.radial_factors(kp/U.KPC_M,jn.j0)
            diff=np.abs(aa-bb)/exact
            for kb,gg in grids.items():
                # Exact membership, because union was formed from these bytes.
                present=np.isin(kp,gg)
                if not present.any():continue
                vals=diff[present];idx=np.unravel_index(np.argmax(vals),vals.shape);v=float(vals[idx])
                if v>worst[kb]['raw']:worst[kb]={'raw':v,'kp':float(kp[present][idx[0]]),'column_1based':int(idx[1])+1}
            if k0%4096==0:print('GQ D %.8g kp %d/%d elapsed %.1fs'%(D,k0,len(union),time.monotonic()-start),flush=True)
        cases.append({'distance_Mpc':D,'kind':'headline' if D==4.04 else 'distance_sensitivity_geometry_only',
             'all_columns':n,'all_production_kperp':{str(k):len(v) for k,v in grids.items()},
             'zero_mode_relative_error':zerr,'M_s':64,'M_s_doubled':128,
             'worst':{str(k):dict(v,conservative_bound=v['raw']/(1-zerr),
                                passes_threshold=v['raw']/(1-zerr)<=1e-12) for k,v in worst.items()},
             'geometry_rule':'registered s_edges*(D/4.04)^2; direct driver-derived edge bytes not claimed identical',
             'scope':'all nonnegative masses and vertical positions at this radial geometry; no new source state'})
        print('GQ completed',D,cases[-1]['worst'],flush=True)
    base.update(status='TESTED_GEOMETRY_FINITE_NODE_GQ',cases=cases,
      labels={'headline':'uniform over every nonnegative source at fixed registered radial geometry, independent s/r/ell',
              'distance':'geometry sensitivity, not actual solved-state certificate; rebind driver-derived geometry bytes before admission'},
      profile=CC.pin('profile'),modules={k:CC.pin(k) for k in ('uvt_lapse','uvt_roster','uvt_jn')},
      provider=jn.custody(),seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    h=write('BOX_GQ_REPLAY_CX2V001.json',base)
    print(json.dumps({'sha256':h,'seconds':base['seconds'],'rss':base['peak_rss_bytes']}))

if __name__=='__main__':
    {'symbol':symbol,'gq':gq}[sys.argv[1]]()
