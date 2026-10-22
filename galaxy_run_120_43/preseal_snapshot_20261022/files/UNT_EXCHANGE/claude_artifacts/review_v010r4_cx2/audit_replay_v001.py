"""Independent Codex2 bounded replay and plan audit; no scientific launches.
Resource instruction: nice unavailable (sandbox); 0514 waiver.
One process, single-thread BLAS; direct saved-state evaluators and in-process dry-run only.
"""
import ast,copy,contextlib,datetime,hashlib,importlib.util,io,json,math,os,re,resource,sys,time,traceback
from pathlib import Path
import numpy as np
EX=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');B=EX/'tail_scheme_impl_c2';O=EX/'review_v010r4_cx2'
R=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13');C2=R/'CLAUDE2'
CHECKS=[];INPUTS={};ERRORS=[]
def guard(event,args):
 if event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','socket.connect'):raise RuntimeError('NO_LAUNCH_OR_NETWORK '+event)
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.fsdecode(args[0]);q=os.path.realpath(p)
  if 'KMAX_A2F10_C5H_RUN_V001' in q or '/runs_ext/UVT_' in q or ('/.codex/' in q and ('session' in q or 'history' in q)) or ('NGC3198' in q and any(s in q.lower() for s in ['observed','target','rotmod'])):raise RuntimeError('FORBIDDEN_READ '+q)
sys.addaudithook(guard)
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:assert os.environ[k]=='1'
def sha(p):
 p=Path(p);h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 INPUTS[str(p)]=h.hexdigest();return h.hexdigest()
def readj(p):sha(p);return json.loads(Path(p).read_text())
def load(p,name):
 sha(p);s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def check(name,ok,**detail):CHECKS.append(dict(name=name,status='TESTED',passed=bool(ok),**detail));print(name,bool(ok),flush=True)
def attempt(name,fun):
 try:fun()
 except Exception as e:ERRORS.append(dict(name=name,type=type(e).__name__,message=str(e),trace=traceback.format_exc(limit=4)));print('ERROR',name,str(e),flush=True)
def same(a,b):return a.dtype==b.dtype and a.shape==b.shape and a.tobytes()==b.tobytes()
def rel(a,b):return float(np.max(np.abs(a-b))/max(float(np.max(np.abs(b))),1e-300))
lib=load(B/'module/owned_uv_tail_lapse_v001.py','cx2_tail');nodes=load(B/'nodes_v001/lib/owned_uv_tail_nodes_v001.py','cx2_nodes');provider=load(B/'module/posix_libm_bessel_jn_provider_c2v001.py','cx2_jn');jn=provider.create_provider()
KPC=lib.KPC_M
# Replay the saved C5R3 iteration-0 source, never C5H. Independently build the tensor axes and complement.
def node_replay():
 g4=readj(C2/'runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/inputs/seed_c2v001.json')['numerical_inputs']['composite_grid_spec']
 run=C2/'runs_ext/KMAX_A2F10_C5R3_RUN_V001';seed=readj(run/'inputs/seed_c2v001.json');ni=seed['numerical_inputs'];g5=ni['composite_grid_spec'];ck=run/'stages/01_route_a/checkpoint';start=readj(ck/'iteration_0000/START.json')
 def blob(key):
  r=start[key];p=ck/r['blob'];assert sha(p)==r['file_sha256'];a=np.load(p,allow_pickle=False,mmap_mode='r');assert list(a.shape)==r['shape'] and a.dtype.str==r['dtype'];return a
 wave=blob('prepared_wavevectors');source=blob('current_source_fourier_J')
 # Independent panel loop, same declared floating point operations as the owned prep.
 def axis(g):
  a=[];w=[]
  for lo,hi,n in zip(g['breaks_inverse_kpc'][:-1],g['breaks_inverse_kpc'][1:],g['panel_orders']):
   x,v=np.polynomial.legendre.leggauss(n);a.extend(((lo+hi)/2+(hi-lo)*x/2)/KPC);w.extend((hi-lo)*v/(2*KPC))
  return np.array(a),np.array(w)
 ax,w=axis(g5);ak,wk=axis(g4)
 expected=np.array([(x,y,z) for x in ax for y in ax for z in ax])
 check('G5_saved_waves_bitwise_independent_tensor',same(np.asarray(wave),expected),shape=list(wave.shape))
 own=nodes.ext_context(ext_spec=g5,kept_spec=g4,kpc_m=KPC)
 inner=np.isin(ax,ak);mask=~(inner[:,None,None]&inner[None,:,None]&inner[None,None,:]);kept=~mask
 check('G5_minus_G4_mask_exact',np.array_equal(own['mask3'],mask) and int(mask.sum())==108**3-96**3,extra_nodes=int(mask.sum()),kept_nodes=int(kept.sum()))
 check('G4_axis_weights_bitwise_subset',same(ax[inner],ak) and same(w[inner],wk))
 bad=copy.deepcopy(g5);bad['panel_orders'][1]=4;bad['panel_orders'][-2]=4;bad['total_axis_nodes']-=4
 try:nodes.ext_context(ext_spec=bad,kept_spec=g4,kpc_m=KPC);refused=False
 except ValueError:refused=True
 check('nodes_rejects_changed_kept_panel_order',refused)
 flat=mask.ravel();S=np.asarray(source[:,0,0]);Sext=np.ascontiguousarray(S[flat]);wv=expected[flat];dk=((w[:,None,None]*w[None,:,None])*w[None,None,:]).ravel()
 # Positive gamma for algebraic replay, explicitly not a new solution or assertion of seed calibration.
 gamma=float(ni['gamma'])*float(seed['scale_seed']);lam=1.0
 cfg=readj(B/'route_b/fixtures/rp2_cfg_on.json');cfg['source_rule']={'rule':'nodes_v001','ext_grid':g5};cfg=lib.normalize_config(cfg)
 state=nodes.build_state(config=cfg,kept={'shape':'cube','K_inverse_kpc':4.0},ctx=own,parts=[('saved_current',1,Sext,{'source':'C5R3 iteration0 stored current packet'})],gamma_eff=gamma,c_m_s=299792458.0,i1t={'verdict':'NOT_APPLICABLE_SYNTHETIC','scope':'saved-packet evaluator replay; no transform replica claim'},stage_kind='route_a')
 pts=KPC*np.array([[0.2,0,0],[1.48,0,0],[1.48/math.sqrt(2),1.48/math.sqrt(2),0.4],[3.7,-0.3,-0.15]])
 got=state.jet(pts,2);amp=lam*dk[flat]/(2*math.pi)**3*Sext/(4*gamma*np.sum(wv*wv,axis=1))
 fields=[];grads=[];hess=[]
 for p in pts:
  e=amp*np.exp(1j*(wv@p));fields.append(np.sum(e).real);grads.append(np.sum(e[:,None]*(1j*wv),axis=0).real);hess.append(-np.einsum('n,ni,nj->ij',e,wv,wv,optimize=False).real)
 errs={'field':rel(got['boundary_fields'][:,0,0],np.array(fields)),'gradient':rel(got['boundary_gradient'][:,0,0],np.array(grads)),'hessian':rel(got['boundary_hessian'][:,0,0],np.array(hess))}
 check('nodes_saved_packet_independent_direct_jet',max(errs.values())<1e-11,errors=errs,points=len(pts),gamma_for_replay=gamma)
 # Full-minus-kept packet sums independent from the state evaluator.
 allamp=lam*dk/(2*math.pi)**3*S/(4*gamma*np.sum(expected*expected,axis=1));vals=[]
 for p in pts:
  e=allamp*np.exp(1j*(expected@p));vals.append((np.sum(e)-np.sum(e[~flat])).real)
 err=rel(np.array(fields),np.array(vals));check('nodes_equals_G5_full_minus_G4_kept',err<1e-10,relative_error=err)
 b0,bd=state.lapse_pair(pts[1,0],pts[1,1],0);check('nodes_midplane_difference_positive_zero_bytes',bd.tobytes()==np.zeros(1).tobytes())
 check('nodes_non_lapse_components_exact_zero',all(np.count_nonzero(v[:,1:])==0 for v in got.values()))
 # Scaling sign and coefficient directly on saved source, with Q_inf * T_N in J convention.
 G=6.67430e-11;c=299792458.;q=c**4/(16*math.pi*G*gamma);tn=4*math.pi*G/(c**4*np.sum(wv*wv,axis=1));ti=1/(4*gamma*np.sum(wv*wv,axis=1));err=rel(q*tn,ti)
 check('tail_symbol_Qinf_times_TN_saved_nodes',err<5e-16,relative_error=err,Qinf=q,source_J_convention='negative rest energy; not positive mass')
attempt('node_replay',node_replay)
# Replay a preexisting module fixture, bounded to four points. Numerical derivatives challenge returned jets.
def continuum_replay():
 man=readj(B/'route_b/fixtures/syn2_1792303455_man_ok.json');p=B/'route_b/fixtures/syn2_1792303455_state.npz';sha(p)
 with np.load(p,allow_pickle=False) as f:a={k:f[k].copy() for k in f.files}
 st=lib.TailState.from_arrays(a,man['state']['record'],jn_provider=jn,expected_digest=man['state']['digest'])
 pts=KPC*np.array([[0.4,0.2,0.0],[0.8,0.5,0.15],[1.48/math.sqrt(2),1.48/math.sqrt(2),-0.1]])
 jet=st.jet(pts,2);h=1e-4*KPC;gd=np.zeros((len(pts),3))
 for i in range(3):
  d=np.zeros(3);d[i]=h;gd[:,i]=(st.value(pts+d)-st.value(pts-d))/(2*h)
 er=rel(gd,jet['boundary_gradient'][:,0,0]);check('saved_continuum_jet_finite_difference',er<1e-6,relative_error=er,step_kpc=h/KPC)
 b0,bd=st.lapse_pair(pts[1,0],pts[1,1],0);check('continuum_midplane_difference_positive_zero_bytes',bd.tobytes()==np.zeros(1).tobytes())
 check('continuum_non_lapse_slots_zero',all(np.count_nonzero(v[:,1:])==0 for v in jet.values()))
 # Exact boundary cases: disabled wrapper returns original offset object, even negative zeros.
 rb=load(B/'route_b/uvt_route_b_binding_c2v001.py','cx2_rb')
 import types
 off=rb.Binding(types.SimpleNamespace(), 'offset',{'enabled':False},'none');x=np.array([[-0.0]*10,[1.0]*10]);before=x.tobytes();y=off.offset_fields(x,pts[:2])
 check('route_B_off_offset_preserves_identity_and_signed_zeros',y is x and y.tobytes()==before)
 z=off.jets(pts);check('route_B_off_jets_exact_zero',all(v.tobytes()==np.zeros_like(v).tobytes() for v in z.values()))
attempt('continuum_replay',continuum_replay)
# B0 actual positive plan case. In-process cmd_dry_run performs no stage or subprocess launch; guard enforces that.
def plan_replay():
 paths={'new':B/'driver_r4/galaxy_m0_forward_c2v010.py','EXT':EX/'kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py','GEO':EX/'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py'}
 spec=C2/'specs/CALL_A2_ANCHOR_F10_C2V001.json';sha(spec);mods={};dirs={};outcomes={}
 for tag,p in paths.items():
  m=load(p,'cx2_driver_'+tag);mods[tag]=m;rd=O/('plan_A2F10_'+tag+'_v001');assert not rd.exists();dirs[tag]=rd
  buf=io.StringIO()
  with contextlib.redirect_stdout(buf):ret=m.cmd_dry_run(str(spec),str(rd))
  outcomes[tag]={'return':ret,'stdout_lines':len(buf.getvalue().splitlines())}
  check('B0_positive_plan_report_exists:'+tag,(rd/'DRYRUN_REPORT.json').is_file())
 bp=B/'driver_r4/gates/b0_plan_identity_c2v002.py';sha(bp);ts=ast.parse(bp.read_text())
 names={'sha_b','sha_f','geo_pin_pairs','files','apply','ext_feature_map','driver_needle_map','ro1_key_map','compare'}
 ns={'Path':Path,'hashlib':hashlib,'json':json,'re':re,'V008':EX/'driver_v008_c2/galaxy_m0_forward_c2v008.py','DRIVERS':{k:(paths[k],sha(paths[k])) for k in ['EXT','GEO']},'EX':EX,'PREP_V009':(EX/'kmax_prereg_v005_c2/extension_c5c6/prep_successor/ddo_actual_initial_source_preparation_v009.py','b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc'),'RO1_NON_ARMED':{'rule':'RO1','fired':False,'events':[],'armed':False,'worker_sha256':None,'binding_sha256':None}}
 ns['__name__']='cx2_extract_b0';exec(compile(ast.Module(body=[n for n in ts.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(bp),'exec'),ns)
 for tag in ['EXT','GEO']:
  pairs=([(str(paths[tag]),str(paths['new'])),(sha(paths[tag]),sha(paths['new']))]);pairs=(ns['geo_pin_pairs']()+pairs) if tag=='EXT' else pairs
  r=ns['compare'](dirs[tag],dirs['new'],pairs,tag)
  check('B0_positive_actual_plan_identical:'+tag,r['identical'] and r['files_parent']>0 and r['files_v010']>0,comparison=r,outcomes=outcomes)
 with (O/'PLAN_COMPARISON_V001.json').open('x') as f:json.dump({'status':'TESTED','resource_waiver':'nice unavailable (sandbox); 0514 waiver','outcomes':outcomes},f,indent=2);f.write('\n')
attempt('plan_replay',plan_replay)
record={'schema':'CODEX2_0511_LANE_B_REPLAY_V001','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resource_waiver':'nice unavailable (sandbox); 0514 waiver','effective_nice':os.getpriority(os.PRIO_PROCESS,0),'single_thread_env':{k:os.environ[k] for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']},'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'launches':0,'checks':CHECKS,'errors':ERRORS,'input_sha256':INPUTS,'untested':['Full route-A or route-B scientific launch (prohibited)','C5H/UVT_* T2-I/production results (prohibited)','NGC3198 real-data replay']}
with (O/'REPLAY_EVIDENCE_V001.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'checks':len(CHECKS),'passed':sum(c['passed'] for c in CHECKS),'failed':[c['name'] for c in CHECKS if not c['passed']],'errors':ERRORS,'max_rss_bytes_macos':record['max_rss_bytes_macos']},indent=2))
