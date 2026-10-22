"""0552 GQ review: own polynomial quadrature, own gas contraction and own node axes.
No producer numeric imports. Saved DDO state only; no scientific launch.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    assert os.environ.get(name) == '1', name
import ctypes
import hashlib
import io
import json
import math
from pathlib import Path
import resource
import subprocess
import sys
import time
import numpy as np

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
CERT = ART / 'tail_scheme_impl_c2/certificates_v003'
OUT = Path(__file__).parent
START = time.time()
DATE_U = subprocess.check_output(['date','-u'],text=True).strip()
LIB = ctypes.CDLL('/usr/lib/libSystem.B.dylib')
J0 = LIB.j0
J0.argtypes = [ctypes.c_double]
J0.restype = ctypes.c_double
UF = np.frompyfunc(J0,1,1)
ALLOWED = {str(Path(__file__).absolute())}
PINS = {}
DENIED = []
READS = set()
def permitted_path(p):
    p = Path(p)
    for s in (str(p.absolute()),str(p.resolve())):
        if '/runs_ext/UVT_' in s or '/KMAX_A2F10_C5H_RUN_V001' in s or '/.codex/' in s:
            raise RuntimeError('FORBIDDEN_PATH: '+s)
    return p
def audit(event,args):
    if event == 'open' and isinstance(args[0],(str,bytes)):
        path = str(permitted_path(os.fsdecode(args[0])).absolute())
        mode,flags = args[1],args[2]
        writing = bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing:
            ok = path.startswith(str(OUT)+'/') and bool(flags & os.O_EXCL)
        else:
            ok = path in ALLOWED or path.startswith(sys.prefix+'/') or path.startswith(sys.base_prefix+'/')
            READS.add(path)
        if not ok:
            DENIED.append([event,path]);raise RuntimeError('AUDIT_REFUSAL: '+path)
    elif event in ('os.remove','os.rename','os.replace','os.rmdir','subprocess.Popen','os.system') or event.startswith('socket.'):
        DENIED.append(event);raise RuntimeError('AUDIT_REFUSAL: '+event)
sys.addaudithook(audit)
def read(p,expected=None):
    p = permitted_path(p);ALLOWED.add(str(p.absolute()))
    data=p.read_bytes();h=hashlib.sha256(data).hexdigest()
    if expected is not None:assert h==expected,(str(p),h,expected)
    PINS[str(p)]={'path':str(p),'sha256':h,'size_bytes':len(data)}
    return data
def doc(p,expected=None):return json.loads(read(p,expected))
def write(name,d):
    data=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    with (OUT/name).open('xb') as f:f.write(data)
    return hashlib.sha256(data).hexdigest()
def bessel(x):return UF(np.asarray(x,float)).astype(float)
checks=[]
def check(name,ok,evidence=None):
    checks.append({'name':name,'status':'TESTED_PASS' if ok else 'TESTED_FAIL','evidence':evidence})
    if not ok:print('FAIL '+name+' '+str(evidence),flush=True)

gate=doc(CERT/'gates/GQ_CERT_V005_MS128.json','fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21')
for key in ('producer','common','part_producer'):read(gate[key]['path'],gate[key]['sha256'])
read(ART/'tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py','c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22')
read(ART/'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py')
read(ART.parent/'FROM_CODEX/0552_2026-10-18_codex3_crosslineage_review_r5_and_certs_v003.md')
profiles={};parts={};ddo=[];record_checks=[]
for r in gate['rosters']:
    if not r['roster'].startswith('DDO_'):continue
    ddo.append(r)
    part=doc(r['part_record']['path'],r['part_record']['sha256']);parts[r['geometry']]=part
    pro=r['all_nodes']['row_max_profile']
    with np.load(io.BytesIO(read(pro['path'],pro['sha256'])),allow_pickle=False) if False else io.BytesIO() as _unused:
        pass
    a=np.load(io.BytesIO(read(pro['path'],pro['sha256'])),allow_pickle=False)
    profiles[r['geometry']]=a
    sample=part['contract_sample']
    check('record_sample_fields_'+r['geometry'],all(r[k]==v for k,v in sample.items() if k!='roster'))
    check('record_full_fields_'+r['geometry'],all(r['all_nodes'][k]==v for k,v in part['full_domain'].items() if k!='histogram'))
    check('record_node_profile_shape_'+r['geometry'],a.shape==(3,r['grid']['N_perp']))
    check('record_max_profile_'+r['geometry'],float(a[1].max())==r['all_nodes']['max_abs_diff_over_P0'])
    check('record_ms128_vs256_'+r['geometry'],r['M_s']==128 and r['M_s_doubled']==256 and r['nodes']==4096)
    check('record_gate_maxima_'+r['geometry'],r['max_abs_diff_over_P0']<=1e-12 and r['all_nodes']['max_abs_diff_over_P0']<=1e-12)
check('aggregate_full_max',max(r['all_nodes']['max_abs_diff_over_P0'] for r in ddo)==gate['max_abs_diff_over_P0_DDO_all_nodes'])
check('aggregate_full_node_count',sum(r['all_nodes']['nodes'] for r in ddo)==gate['all_nodes_total'])
check('aggregate_sample_max',max(r['max_abs_diff_over_P0'] for r in ddo)==gate['max_abs_diff_over_P0_DDO_sample'])
check('DDO_all_three_rosters_reach256',all(any(r['roster']==nm and r['k_range_inverse_kpc'][1]==256.0 for r in ddo) for nm in ('DDO_C2T','DDO_C3T','DDO_C4T')))
check('record_label_component_vs_magnitude',gate['coverage_inverse_kpc']['DDO']==[2.0,256.0] and all(r['k_abs_max_inverse_kpc']==math.sqrt(2)*256 for r in ddo if r['k_range_inverse_kpc'][1]==256.0))

part=parts['C2T_KB256'];profile=profiles['C2T_KB256']
run=UPC/'CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001'
res=doc(run/'result.json','1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169')
finish=doc(run/'finish.json');check('source_finish_result_pin',finish['result_sha256']==PINS[str(run/'result.json')]['sha256'])
request=doc(Path(res['passes'][-1]['field']).parent/'request.json')
argv=request['argv'];rot=Path(argv[argv.index('--rotation-directory')+1])
check('source_rotation_custody',str(rot)==part['source_rotation'])
seed=doc(run/'inputs/seed_c2v001.json');kpc=seed['numerical_inputs']['kpc_m']
with np.load(io.BytesIO(read(rot/'rotation_base_arrays.npz')),allow_pickle=False) as z:
    arrays={k:z[k].copy() for k in ('rho0','volume_weights_m3','radial_nodes_m','z')}
prof=doc(UPC/'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json','f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b')
edges=np.array(prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],float)
x4,w4=np.polynomial.legendre.leggauss(4)
mid=(edges[:-1]+edges[1:])/2;half=np.diff(edges)/2
columnR=np.sqrt(mid[:,None]+half[:,None]*x4).ravel()*kpc
rho,vol=arrays['rho0'],arrays['volume_weights_m3']
check('source_mass_positive',bool(np.all(rho>=0) and np.all(vol>=0)))
check('source_axisymmetric',np.array_equal(rho,np.broadcast_to(rho[:,:1,:],rho.shape)) and np.array_equal(arrays['z'],np.broadcast_to(arrays['z'][:,:1,:],arrays['z'].shape)))
ringmass=np.sum(rho*vol,axis=1)
nodesR=arrays['radial_nodes_m'];mapping=np.argmin(abs(nodesR[:,None]-columnR),axis=1)
check('source_unique_GL4_columns',len(set(mapping.tolist()))==len(mapping) and bool(np.all(abs(nodesR-columnR[mapping])<=1e-12*nodesR)))
order=np.argsort(mapping);columns=mapping[order];masses=ringmass[order];z_kpc=arrays['z'][order,0,:]/kpc
total=float(np.sum(masses));fractions=masses.sum(axis=1)/total
check('source_mass_matches_certificate',abs(total/part['gas_mass_kg']-1)<2e-15,{'own_kg':total,'record_kg':part['gas_mass_kg']})
check('source_P0_equals_mass',abs(part['P0']/total-1)<2e-15)

# Own normalized-cardinal polynomial representation; independent arithmetic from producer's products in s.
RULES={}
for M in (64,128,256):
    x,w=np.polynomial.legendre.leggauss(M)
    co=[]
    for i in range(4):
        c=np.polynomial.polynomial.polyfromroots(np.delete(x4,i))
        c=c/np.polynomial.polynomial.polyval(x4[i],c)
        co.append(np.polynomial.polynomial.polyval(x,c))
    RULES[M]=(x,(w[:,None]*np.array(co).T)/w4[None,:])
def Q(kp,M):
    kp=np.atleast_1d(np.asarray(kp,float));x,basis=RULES[M]
    ans=np.empty((len(kp),len(columnR)))
    for j in range(len(mid)):
        radius=np.sqrt(mid[j]+half[j]*x)
        ans[:,4*j:4*j+4]=bessel(kp[:,None]*radius[None,:])@basis
    return ans[:,columns]
def vertical(kz):
    kz=np.atleast_1d(np.asarray(kz,float));out=np.empty((len(kz),len(columns)),complex)
    for j in range(len(columns)):
        out[:,j]=np.exp(-1j*kz[:,None]*z_kpc[j][None,:])@(masses[j]/total)
    return out

# Rebuild production axes directly from the declared panel rules, without module imports or saved profile node reuse.
x8,_=np.polynomial.legendre.leggauss(8)
def panel_nodes(cuts):
    cuts=np.asarray(cuts)
    return ((cuts[1:,None]+cuts[:-1,None])/2+np.diff(cuts)[:,None]*x8/2).ravel()
def uniform(lo,hi,width):
    n=max(1,math.ceil((hi-lo)/width-1e-12))
    return panel_nodes(np.linspace(lo,hi,n+1)),n
def own_axes(K,B):
    first,n1=uniform(0,K,.05)
    end=math.acos(1/math.sqrt(2));cuts=[0.0];step=1.5/(math.sqrt(2)*K*14.2+40)
    while cuts[-1]<end*(1-1e-15):
        a=cuts[-1];cuts.append(min(a+step,math.acos(min(1.,K/(K/math.cos(a)+.05))),end))
    central=K/np.cos(panel_nodes(cuts))
    last,n3=uniform(math.sqrt(2)*K,B,.05)
    za,nza=uniform(0,K,.02);zb,nzb=uniform(K,B,.02)
    return np.concatenate((first,central,last)),np.concatenate((za,zb)),[n1,len(cuts)-1,n3],[nza,nzb]
kp,kz,npan,nzpan=own_axes(2.,256.)
check('independent_axis_counts',len(kp)==part['grid']['N_perp'] and len(kz)==part['grid']['N_z_plus'],[len(kp),len(kz)])
check('independent_panel_counts',npan==[x['panels'] for x in part['grid']['kp_intervals']] and nzpan==[x['panels'] for x in part['grid']['kz_intervals']])
check('independent_kperp_nodes_vs_profile',np.array_equal(kp,profile[0]),float(np.max(abs(kp-profile[0]))))
nodes=int(len(kp)*len(kz)-np.count_nonzero(kp<=2)*np.count_nonzero(kz<=2))
check('independent_node_domain_count',nodes==part['full_domain']['nodes'],{'own':nodes,'record':part['full_domain']['nodes']})
reach=math.hypot(256,256)
check('full_DDO_reach_is_component_cylinder_not_sphere362',reach==part['full_domain']['k_abs_max_inverse_kpc'] and math.hypot(kp[-1],kz[-1])>362.)

# J0 sanity from a separate cosine integral: quadrature count well above oscillation count.
xs=np.array([0.,1.,32.,256.,1024.,3620.])
ref=[]
for v in xs:
    n=max(512,int(math.ceil(abs(v)))+128)
    ref.append(float(np.mean(np.cos(v*np.sin(math.pi*np.arange(n)/n)))))
jerr=float(np.max(abs(bessel(xs)-ref)))
check('libm_j0_independent_integral_check',jerr<3e-14,jerr)

# All production k_perp nodes: positivity gives |S128-S256|/M <= sum_i f_i |Q128-Q256| for EVERY k_z.
bound=np.empty(len(kp));rosterfree=np.empty(len(kp));q128=np.empty((len(kp),len(columns)));q256=np.empty_like(q128)
for a in range(0,len(kp),512):
    sl=slice(a,min(a+512,len(kp)))
    q128[sl]=Q(kp[sl],128);q256[sl]=Q(kp[sl],256)
    dq=abs(q128[sl]-q256[sl]);bound[sl]=dq@fractions;rosterfree[sl]=dq.max(axis=1)
    if a%4096==0:print(json.dumps({'phase':'all_kperp_bound','rows':sl.stop,'total':len(kp),'elapsed_s':round(time.time()-START,1)}),flush=True)
own_bound=float(bound.max());own_free=float(rosterfree.max())
check('all_production_nodes_bound_below_threshold',own_bound<1e-12,own_bound)
check('all_nonnegative_rosters_bound_below_threshold',own_free<1e-12,own_free)

# Explicit upper shell (256, sqrt(2)*256]: every kz at independent selected rows, including the reach corner.
rng=np.random.default_rng(552)
picked=np.unique(np.r_[np.argsort(profile[1])[-12:],np.arange(len(kp)-12,len(kp)),rng.choice(len(kp),24,replace=False)])
cut_q={128:q128[picked],256:q256[picked],64:Q(kp[picked],64)}
shell={'lower_exclusive':256.,'upper_inclusive':reach,'row_count':int(len(picked)),'nodes':0,'max_k_abs':0.,'max_abs_128_256':0.,'max_abs_64_128_canary':0.,'max_subtraction_difference':0.}
perrow=np.zeros(len(picked));perrow_whole=np.zeros(len(picked));locations={}
for a in range(0,len(kz),2048):
    sl=slice(a,min(a+2048,len(kz)));zk=kz[sl];v=vertical(zk)
    S128=cut_q[128]@v.T;S256=cut_q[256]@v.T;S64=cut_q[64]@v.T
    direct=(cut_q[128]-cut_q[256])@v.T
    d=np.maximum(abs(S128-S256),abs(direct));canary=abs(S64-S128)
    kval=np.hypot(kp[picked,None],zk[None,:]);mask=kval>256.
    shell['nodes']+=int(mask.sum());shell['max_k_abs']=max(shell['max_k_abs'],float(kval.max()))
    perrow=np.maximum(perrow,np.max(np.where(mask,d,0.),axis=1));perrow_whole=np.maximum(perrow_whole,np.max(d,axis=1))
    for key,val in [('max_abs_128_256',d),('max_abs_64_128_canary',canary)]:
        arr=np.where(mask,val,-1.)
        i,j=np.unravel_index(np.argmax(arr),arr.shape);value=float(arr[i,j])
        if value>shell[key]:
            shell[key]=value;locations[key]={'k_perp':float(kp[picked[i]]),'k_z':float(zk[j]),'k_abs':float(kval[i,j])}
    shell['max_subtraction_difference']=max(shell['max_subtraction_difference'],float(np.max(abs((S128-S256)-direct))))
shell['maxima_locations']=locations
shell['row_indices']=picked.tolist()
shell['per_row_max_shell']=perrow.tolist()
shell['per_row_max_whole_cylinder']=perrow_whole.tolist()
shell['record_per_row_max_whole_cylinder']=profile[1,picked].tolist()
check('upper_shell_explicit_nodes_pass',shell['max_abs_128_256']<=1e-12,shell['max_abs_128_256'])
check('upper_shell_Ms64_canary_fails',shell['max_abs_64_128_canary']>1e-12,shell['max_abs_64_128_canary'])
check('upper_shell_reaches_362',shell['max_k_abs']>362.,shell['max_k_abs'])
check('upper_shell_respects_all_kperp_bound',float(perrow_whole.max())<=own_bound+4e-16,{'whole_max':float(perrow_whole.max()),'bound':own_bound})

# Re-evaluate the producer's global dmax coordinate; roundoff-scale maximum values are not mathematically exact bounds.
at=part['full_domain']['at']['dmax'];qs={m:Q([at['k_perp']],m)[0] for m in (128,256)};vs=vertical([at['k_z']])[0]
sd={m:complex(qs[m]@vs) for m in qs};at_sub=float(abs(sd[128]-sd[256]));at_dq=float(abs((qs[128]-qs[256])@vs))
point={'coordinate':at,'own_subtracted_over_mass':at_sub,'own_difference_first_over_mass':at_dq,'own_S256_over_mass':abs(sd[256]),'record_P0_over_mass':part['P0']/total}
check('record_dmax_coordinate_source_agrees',abs(abs(sd[256])-at['S_over_P0'])<2e-14,point)
neg=vertical(-kz[[0,len(kz)//2,-1]])
pos=vertical(kz[[0,len(kz)//2,-1]])
check('negative_kz_conjugacy',np.array_equal(neg,pos.conj()))
allpins=list(PINS.values())
report={'date_u':DATE_U,'status':'PASS_WITH_FINDINGS' if all(c['status']=='TESTED_PASS' for c in checks) else 'FAIL','checks':checks,'n_checks':len(checks),'n_passed':sum(c['status']=='TESTED_PASS' for c in checks),'high_shell':shell,'all_kperp_bound':{'rows':len(kp),'max_over_mass':own_bound,'at_k_perp':float(kp[np.argmax(bound)]),'roster_free_max':own_free,'record_bound_over_P0':part['full_domain']['all_kperp_nodes_bound_over_P0'],'covers':'All positive/negative kz at every production k_perp node; in particular every production node in (256,sqrt(2)*256]. This is a bound, not a re-enumerated full tensor maximum.'},'record_dmax_replay':point,'source_mass_kg':total,'domain_nodes':nodes,'full_aggregate_nodes':gate['all_nodes_total'],'independence':'Own normalized-coordinate polynomial cardinal quadrature, gas-column reconstruction, vertical mass contraction and production axis construction. Shared inputs only: saved C2R3 state, radial profile, declared grid/rule definitions and platform libm J0. No certificate/producer/module numeric code imported.','limitations':['Full tensor node maximum not re-enumerated; full upper-shell acceptance independently certified by positivity bound at every production k_perp node and explicit selected-row replay.','Producer maximum and bound are floating-point estimates, not interval bounds. Independent arithmetic differs at roundoff; the acceptance threshold margin is assessed directly.','Only C2R3 source independently reconstructed numerically; other DDO geometry records and byte pins checked by aggregation.','Real targets, NGC source numerics and scientific runs were not used.'],'elapsed_seconds':time.time()-START,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'pins':allpins,'denied':DENIED}
h=write('GQ_REVIEW_CX3V001.json',report)
print(json.dumps({'status':report['status'],'checks':report['n_checks'],'passed':report['n_passed'],'bound':own_bound,'upper_shell_max':shell['max_abs_128_256'],'canary':shell['max_abs_64_128_canary'],'sha256':h,'elapsed_s':report['elapsed_seconds'],'peak_rss_bytes':report['peak_rss_bytes']}),flush=True)
