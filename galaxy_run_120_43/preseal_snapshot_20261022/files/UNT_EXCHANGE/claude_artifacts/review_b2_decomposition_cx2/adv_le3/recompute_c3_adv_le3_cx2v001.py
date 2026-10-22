"""Owned static C3 le3 ADV-reference recomputation. No stages or scientific modules imported.
AST selection executes only axis_nodes/cart_tail/rows_with and inert observation helpers.
Inputs are exact pinned permitted C3 saved arrays + target-free artifacts. Output exclusive-create.
"""
import ast, bisect, ctypes, hashlib, io, json, math, os, resource, sys, time, types, zipfile
from pathlib import Path
import numpy as np
T0=time.monotonic()
DATE_U=os.environ['REVIEW_DATE_U']
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
ROOT=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
OUT=A/'review_b2_decomposition_cx2/adv_le3'
RUN=ROOT/'CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001'
FILES={
'adv':(A/'uv_tail_study_c2/check/adv_tail_check_v001.py',None),
'ind':(A/'gate_b2_c3/out/path2/IND_C3R3_BASE.json','fdbacd7de467c10924d5201b0b168f974a8206d59ee2100473b9340623cfcbce'),
'cm':(A/'gate_b2_c3/out/path1/C3R3_CM_ON/observation/result.json','9735dc5adc90a75175348959210f9f5a75429c5ebb72263216f3a2581d134224'),
'eval':(RUN/'stages/19_le3_rotation/rotation/rotation_base_arrays.npz','f5709f8423fcf7de1373cab4043efad261ad2d5aece22e5342d5254e4b449d04'),
'source':(RUN/'stages/15_le2_rotation/rotation/rotation_base_arrays.npz','05a7793aebd5fb9269ab973bc7d85a3e81ff1e2a536e9b750e8c5ca9ac6e7ad6'),
'seed':(RUN/'inputs/seed_c2v001.json','f7b3f980ec2013116a20cecd602cf3b495de292470c6a14cfed19ce886f0bcd3'),
'profile':(ROOT/'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json','f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
'binding':(ROOT/'CODEX1/DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json','f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
'obs':(ROOT/'helpers/recovered_packet_audit/galaxy_hi_observation_forward_v001.py','8e30897e875a619b132ba07e93459333cfd9302bbe2fc98d9a2ff0a2ec6d815d'),
'adapter':(ROOT/'helpers/recovered_packet_audit/owned_column_mean_streaming_observation_v002.py','6790e28eb6631c0144f2efda26071a5933f47f7bda7d0c15d3b81e3581cc548c'),
'forward_source':(ROOT/'helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py','e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad'),
'dispatch':(A.parent/'FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md',None),
'harness':(Path(__file__),None),
}
# Preload only stdlib libm. This matches ADV J0/J1 and starts no process.
lib=ctypes.CDLL('/usr/lib/libm.dylib')
for name in ('j0','j1'):
 getattr(lib,name).argtypes=[ctypes.c_double]; getattr(lib,name).restype=ctypes.c_double
_J0=np.frompyfunc(lib.j0,1,1); _J1=np.frompyfunc(lib.j1,1,1)
def J0(x): return _J0(np.asarray(x,float)).astype(float)
def J1(x): return _J1(np.asarray(x,float)).astype(float)
CL=299792458.0
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
assert all(os.environ.get(k)=='1' for k in THREADS)
# Guards are installed before candidate function execution or any saved-state read.
# Deny all run files except the three exact C3 files above, and every protected spelling.
READS=set(str(p) for p,_ in FILES.values()); CANONICAL={}
OLDSTAT=os.stat; OLDLSTAT=os.lstat; OLDLINK=os.readlink
DENIED=[]
def norm(p):
 if isinstance(p,int): return None
 return os.path.normpath(os.fsdecode(p))
def protected(s):
 low=s.lower()
 return ('kmax_a2f10_c5h' in low or '/runs_ext/uvt_' in low or '/.codex/' in low or '/.vol/' in low or ('ngc3198' in low and any(t in low for t in ('target','observ','velocity'))))
def permitted_run_meta(s):
 if '/runs/' not in s and '/runs_ext/' not in s: return True
 marker='/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001'
 if marker not in s: return False
 suffix=s.split(marker,1)[1]
 allowed=['/stages/19_le3_rotation/rotation/rotation_base_arrays.npz','/stages/15_le2_rotation/rotation/rotation_base_arrays.npz','/inputs/seed_c2v001.json']
 return any(x==suffix or x.startswith(suffix.rstrip('/')+'/') for x in allowed)
def check(p,kind):
 s=norm(p)
 if s is None:return
 if protected(s) or not permitted_run_meta(s):
  DENIED.append([kind,s]); raise PermissionError('PROTECTED_PATH_REFUSED')
 if kind=='read' and s not in READS:
  DENIED.append([kind,s]); raise PermissionError('NON_ALLOWLIST_READ_REFUSED')
def safe_stat(p,*a,**k):check(p,'stat');return OLDSTAT(p,*a,**k)
def safe_lstat(p,*a,**k):check(p,'lstat');return OLDLSTAT(p,*a,**k)
def safe_readlink(p,*a,**k):
 check(p,'readlink'); target=OLDLINK(p,*a,**k)
 resolved=os.path.normpath(os.path.join(os.path.dirname(os.fsdecode(p)),target));check(resolved,'linktarget')
 return target
os.stat=safe_stat;os.lstat=safe_lstat;os.readlink=safe_readlink
def audit(event,args):
 if event=='open':
  p,mode,flags=args;writing=bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if writing:
   s=norm(p)
   if not s.startswith(str(OUT)+'/') or not flags & os.O_EXCL: raise PermissionError('EXCLUSIVE_OWN_OUTPUT_ONLY')
  else:check(p,'read')
 elif event in ('os.listdir','os.scandir'):
  raise PermissionError('NO_DIRECTORY_TRAVERSAL')
 elif event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','os.exec','os.remove','os.rename','os.rmdir'):
  raise PermissionError('NO_PROCESS_OR_DESTRUCTIVE_ACTION')
sys.addaudithook(audit)
for name,(path,_) in FILES.items():
 canonical=str(path.resolve(strict=True));check(canonical,'canonical');CANONICAL[name]=canonical;READS.add(canonical)
PINS={}; RAW={}
for name,(path,expected) in FILES.items():
 raw=path.read_bytes();got=hashlib.sha256(raw).hexdigest()
 if expected is not None and got!=expected:raise ValueError('PIN:'+name)
 RAW[name]=raw;PINS[name]={'path':str(path),'canonical_path':CANONICAL[name],'sha256':got,'bytes':len(raw)}
assert PINS['adv']['sha256'].startswith('67a6eeb6')
def extract(source,names,ns,filename):
 tree=ast.parse(source); selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert len(selected)==len(names)
 exec(compile(ast.Module(body=selected,type_ignores=[]),filename,'exec'),ns)
 return ns
# Exactly pure functions; no Case, main, validate, module import, driver, or stage executes.
adv=extract(RAW['adv'],{'axis_nodes','cart_tail','rows_with'},dict(np=np,math=math,CL=CL,J0=J0,J1=J1),str(FILES['adv'][0]))
obsns=extract(RAW['obs'],{'_real','_inclination','hi_moment','thin_axisymmetric_reference'},dict(math=math),str(FILES['obs'][0]))
obs=types.SimpleNamespace(__file__=str(FILES['obs'][0]),**{k:v for k,v in obsns.items() if not k.startswith('__')})
adapns=extract(RAW['adapter'],{'real','text','evaluate'},dict(bisect=bisect,hashlib=hashlib,math=math,Path=Path,OBSERVATION_SHA256=PINS['obs']['sha256']),str(FILES['adapter'][0]))
adapter=types.SimpleNamespace(evaluate=adapns['evaluate'])
ind=json.loads(RAW['ind']); cm=json.loads(RAW['cm']);ni=json.loads(RAW['seed'])['numerical_inputs'];binding=json.loads(RAW['binding'])
prof=json.loads(RAW['profile'])['galaxies']['DDO154']['stellar_reference']
rotkeys=('radial_nodes_m','z','rho0','enthalpy','rotation_Omega_squared','rotation_A')
with np.load(io.BytesIO(RAW['eval']),allow_pickle=False) as f:rot={k:f[k].copy() for k in rotkeys}
with np.load(io.BytesIO(RAW['source']),allow_pickle=False) as f:src={k:f[k].copy() for k in ('radial_nodes_m','z','rho0','volume_weights_m3')}
# Reconstruct ADV discrete star GL rings directly from its documented equations.
x,w=np.polynomial.legendre.leggauss(ni['source_gauss_order']);kpc=ni['kpc_m'];su=ni['solar_mass_kg']/(kpc/1000)**2
radii=[float(v) for v in prof['radius_kpc']];sig=[float(v) for v in prof['surface_density_Msun_pc2']];rd=float(prof['outer_scale_kpc']);height=float(prof['height_kpc'])
cuts=sorted(set([0.]+radii));nodes=[]
for lo,hi in zip(cuts,cuts[1:]):
 for xx,ww in zip(x,w):nodes.append(((lo+hi)/2+(hi-lo)*xx/2,(hi-lo)*ww/2))
for xx,ww in zip(x,w):
 u=(xx+1)/2;nodes.append((radii[-1]-rd*math.log(u),rd*ww/(2*u)))
def surface(r):
 if r<=radii[0]:return sig[0]
 if r>=radii[-1]:return sig[-1]*math.exp(-(r-radii[-1])/rd)
 i=bisect.bisect_right(radii,r)-1
 return sig[i]+(sig[i+1]-sig[i])*(r-radii[i])/(radii[i+1]-radii[i])
stars=dict(Rr=np.array([r*kpc for r,_ in nodes]),Mr=np.array([surface(r)*su*(r*kpc)*(dr*kpc)*2*math.pi for r,dr in nodes]),zu=np.array([2*height*kpc*math.atanh(u) for u in x]),wu=w/2,h_m=height*kpc)
# A finite-node crosscheck against AST-selected radial_surface validates exact transcription only.
fw=extract(RAW['forward_source'],{'radial_surface','nonnegative','positive'},dict(math=math,bisect_right=bisect.bisect_right),str(FILES['forward_source'][0]))
profile_diff=max(abs(surface(r)-fw['radial_surface'](r,radii,sig,outer_scale=rd)) for r,_ in nodes)
assert profile_diff==0
assert np.array_equal(src['rho0'],np.broadcast_to(src['rho0'][:,:1,:],src['rho0'].shape))
gas=(src['radial_nodes_m'],src['z'][:,0,:],np.sum(src['volume_weights_m3']*src['rho0'],axis=1))
W=np.array([c['emissivity_path_weights'] for c in cm['prediction']['columns']]);rho=rot['rho0'][:,0,:]
assert W.shape==rho.shape==(72,32)
# CM_ON saved weights are target-free and use the same frozen rho. Undo only the scalar HI ratio and rho.
cols=[{'weights_m':(W[i]/(rho[i]*binding['HI_to_HI_plus_He_mass_ratio'])).tolist()} for i in range(72)]
c=types.SimpleNamespace(K=3.,gamma=float(ind['gamma_eff']))
base,Avec=adv['rows_with'](c,rot,cols,None,binding,obs,adapter)
baseline_diff=float(np.max(np.abs(base-np.asarray(ind['rows_saved_le3_km_s']))))
Arel=float(np.max(np.abs(Avec/rot['rotation_A']-1)))
assert baseline_diff<1e-10,(baseline_diff,Arel)
assert Arel<1e-12,Arel
ax,aw=adv['axis_nodes'](12.,3.,.25,6,True);zz,zw=adv['axis_nodes'](12.,3.,.25,6,False)
print(json.dumps({'status':'STATIC_QUADRATURE_START','date_u':DATE_U,'source_le2':PINS['source']['sha256'],'eval_le3':PINS['eval']['sha256'],'baseline_max_abs_km_s':baseline_diff,'A_max_rel':Arel,'positive_axis_nodes':len(ax),'full_axis_nodes':len(zz),'quarter_xy_full_z_nodes':len(ax)**2*len(zz),'star_nodes':len(stars['Rr']),'prep_seconds':time.monotonic()-T0}),flush=True)
tq=time.monotonic()
f16,f0=adv['cart_tail'](c,gas,stars,ni,12.,.25,6,rot['radial_nodes_m'],rot['z'][:,0,:])
quadseconds=time.monotonic()-tq
r16,_=adv['rows_with'](c,rot,cols,f16,binding,obs,adapter);r0,_=adv['rows_with'](c,rot,cols,f0,binding,obs,adapter)
disc=np.asarray(ind['rows']['discrete_total']['rows_km_s'])
comparison=r16-disc
# Saved IND discrete_total is the corresponding linear discrete gas+stars group.
assert float(np.max(np.abs(comparison)))<1e-4
buf=io.BytesIO();np.savez(buf,f16_m_s2=f16,f0_m_s2=f0,rows_P16_km_s=r16,rows_m0_km_s=r0,rows_OFF_km_s=base)
npz=buf.getvalue();npzpath=OUT/'C3_LE3_ADV_O6_CX2V001.npz'
with npzpath.open('xb') as f:f.write(npz)
END={}
for name,(path,_) in FILES.items():
 got=hashlib.sha256(path.read_bytes()).hexdigest();END[name]=got
 assert got==PINS[name]['sha256'],('SOURCE_CHANGED',name)
result={'schema':'CX2_C3_LE3_ADV_STATIC_REFERENCE_V001','status':'TESTED','date_u':DATE_U,
 'scope':'Static quadrature on the explicitly permitted saved C3R3 le2 source and le3 evaluation. No scientific launch, Case/main, producer or stage execution.',
 'method':{'K_inverse_kpc':3.,'Kout_inverse_kpc':12.,'panel_width_inverse_kpc':.25,'Gauss_order':6,'azimuths':16,'symmetry':'original ADV quadrant xy factor4, full kz','quarter_xy_full_z_nodes':int(len(ax)**2*len(zz)),'source':'saved le2 discrete gas rings + original discrete GL star rings','bessel':'stdlib ctypes libm j0,j1 as original ADV; numpy only third-party','readout':'AST-selected original rows_with and inert pinned observation/adapter; weights reconstructed from pinned target-free CM_ON emission weights'},
 'controls':{'baseline_max_abs_km_s':baseline_diff,'A_max_rel':Arel,'star_radial_surface_transcription_max_abs':profile_diff,'source_axisymmetry_exact':True,'threads':{k:os.environ[k] for k in THREADS},'forbidden_accesses':DENIED},
 'row_ids':ind['row_ids'],'rows_OFF_km_s':base.tolist(),'rows_P16_km_s':r16.tolist(),'rows_m0_km_s':r0.tolist(),
 'comparison':{'IND_discrete_total_rows_km_s':disc.tolist(),'P16_minus_IND_discrete_total_km_s':comparison.tolist(),'max_abs_P16_minus_IND_discrete_total_km_s':float(np.max(np.abs(comparison))),'P16_minus_m0_km_s':(r16-r0).tolist(),'max_abs_P16_minus_m0_km_s':float(np.max(np.abs(r16-r0)))},
 'inputs':PINS,'input_end_sha256':END,'all_input_pins_unchanged':True,
 'array_artifact':{'path':str(npzpath),'sha256':hashlib.sha256(npz).hexdigest(),'bytes':len(npz)},
 'quadrature_seconds':quadseconds,'total_seconds':time.monotonic()-T0,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'limitations':['One O6,width0.25 reference evaluation, not a new quadrature-convergence claim. Independent IND O12 comparison measured.','No actual scientific solver or production launch; no acceptance or seal promotion.','No unit-response/Fourier source custody replay in this bounded task; saved array byte identity and source reconstruction checked.','No gas-continuum rerun here; separate lane computes its saved-vector effect.']}
resultbytes=(json.dumps(result,indent=1,allow_nan=False)+'\n').encode();resultpath=OUT/'RESULTS_CX2V001.json'
with resultpath.open('xb') as f:f.write(resultbytes)
print(json.dumps({'status':'TESTED_COMPLETE','result':str(resultpath),'sha256':hashlib.sha256(resultbytes).hexdigest(),'P16_vs_IND_max_abs_km_s':float(np.max(np.abs(comparison))),'P16_vs_m0_max_abs_km_s':float(np.max(np.abs(r16-r0))),'seconds':quadseconds,'rss':result['peak_rss_bytes']}),flush=True)
