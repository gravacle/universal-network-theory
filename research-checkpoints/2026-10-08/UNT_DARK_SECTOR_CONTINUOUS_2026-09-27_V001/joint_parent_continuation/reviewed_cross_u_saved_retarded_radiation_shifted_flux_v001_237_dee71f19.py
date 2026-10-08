"""Guarded saved-source phase flux diagnostic; root alone evaluates frozen kernels."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, importlib, json, math, os, time, traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_RETARDED_RADIATION_SHIFTED_FLUX_V001'
PARENT='CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001'
PARENT_SOURCE='cross_u_full_flrw_retarded_history_v001.py'
INITIAL='CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000'
AUTHOR_GUARD=True
PROTOCOL_SHA='0d064197e486bae2ea87486ae40fe21dbad4f145209120e9ed72262549a0034d'
PINS={'cross_u_full_flrw_retarded_history_v001.py': 'cb638242b99f5788b5dbcd6dbe2bf0778e8c9e0b260f4b4c79f71308e17f86cb', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001.md': 'f06a5fd890ccae9e2f0e0f08c29a48f8222a2ed6d51176ab61652750f0f219b4', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_RESULT.json': 'c91fd50725e1d770881a13ba60615aa04d2fba8899bf4fefe34d1f8b733978aa', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_RECEIPT.json': 'd7507bc37c4880089fe4a70716ceff226bd251a5fa437329581d044620f31913', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_MANIFEST.json': '5ec81e4ab373bde45591b3335985b1c9f4f692f5d4390e7be3a363f3c54fcc1e', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_TIME512_CP_000512.npz': '7519e80eea03b9a446f0775f5e05c18dee95ad2e4668feb4ebafb05472c86699', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_TIME512_CP_000512_COMMIT.json': '0f9bd8b4461e805ace9085047c03dea7e80c543f5b110af02d880c78d40b313d', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_FINE1024_CP_001024.npz': 'f4e30ac85ca13bc469a39d3f0a1bf981557e80bcbaf5483f4e3104282004c22a', 'CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001_FINE1024_CP_001024_COMMIT.json': '4ebd83c4bf1ee75d27b12fe33be2b6b51fbefef0650e89abcd5ecf029aaf9724', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000.npz': '72aa7178724affa2a06c97e1f3990872670ed85df0cce720beca2b21f6c05879', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000_COMMIT.json': '43a762492edf95003e26c12c11ec3d34dead48b67b1da5760411607187537d95', 'CROSS_U_EXACT_RETARDED_RADIATION_MOMENT_OPERATOR_V001.md': 'c4fcedb21d45274bc6632b755e87c6eacf566f5d84268d103e625990bc299752'}
HELPER_SPANS={'fast_kernels': '121772a20a5821bd89582c8912f5aee9e172385d04d5dd11e227cd4727e6bffc', 'cardinal_coefficients': 'e952c04ca6fe8d9e04f179e43273d0698e222251e9dfdd1e6b9cf67038ebf381', 'cardinal': '3f8d8d857ad5444be042396487a3dc99c913f357ad8a95265f300a10d498ec5e', 'source_tensor': 'fab89e5fd422b0f795108aae0c7661c6c2d134727b405d156107409100d222b6', 'history_moments': '4096cb0d4236f4b766dea8e4ad88097a2024c7ae4981043ba0f07d6dd9d2c1b8', 'historical_flux': 'b909055215b06af01decae62cbb1d3e6b135c08f2cba258e2a0cefa03f9fb519', 'current_flux': 'e269946c80fc784fb8239da5aa766414e51de002644ca00eea45c92cbf86341d'}
TARGETS=(('TIME512',512,455),('FINE1024',1024,912))
ORDERS=(2,4,8,16,32,64)
BRANCH_TOL=1e-6; ARITH_TOL=2e-11; FLOOR=1e-13
FLAGS={n:False for n in ('original_log_time_gate_repaired','full_trajectory_qualified','prepared_universe','nonlinear_clock','native_normalization','mode_inertia','continuum_angular','observed_growth','observed_lensing','joint_epsilon_adopted')}
np=None; HELPER=None; INPUTS={}; CREATED={}; RECORDS=[]; RAW={}; OWNER=None; CONTEXT={}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def finite(x):return float(x) if math.isfinite(float(x)) else None

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:
        if not math.isfinite(v):raise ValueError('Nonfinite JSON scalar')
        return v
    raise TypeError(type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,v):
    raw=encode(v);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
    if p.read_bytes()!=raw:raise ValueError('Exact published JSON')
    CREATED[name]=sha(p);return CREATED[name]

def resolve_inputs():
    merged=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});todo=[PARENT+'_RECEIPT.json'];done=set()
    while todo:
        name=todo.pop()
        if name in done:continue
        if sha(BASE/name)!=merged[name]:raise ValueError('Receipt pin')
        r=json.loads((BASE/name).read_text());done.add(name)
        ins=dict(r.get('input_sha256',r.get('pins',{})));outs=r['output_sha256']
        if not outs:raise ValueError('Closed receipt outputs')
        manifest_name=Path(name).name[:-len('_RECEIPT.json')]+'_MANIFEST.json'
        matches=[key for key in outs if Path(key).name==manifest_name]
        if matches:
            if len(matches)!=1:raise ValueError('Unique parent manifest')
            m=json.loads((BASE/matches[0]).read_text())
            if 'manifest' in r and r['manifest']!=m:raise ValueError('Literal parent manifest')
            if 'manifest_sha256' in r and r['manifest_sha256']!=outs[matches[0]]:raise ValueError('Manifest seal')
            for key,h in dict(m.get('input_sha256',{}),**m.get('inherited_input_sha256',{})).items():
                if key in ins and ins[key]!=h:raise ValueError('Inherited map conflict')
                ins[key]=h
        for key,h in dict(ins,**outs).items():
            if key in merged and merged[key]!=h:raise ValueError('Input/output seal conflict')
            merged[key]=h
            if key.endswith('_RECEIPT.json') and key not in done:todo.append(key)
    for name,h in merged.items():
        if len(h)!=64 or sha(BASE/name)!=h:raise ValueError('Actual complete byte pin '+name)
    merged[Path(__file__).name]=sha(__file__)
    return merged

def authenticate():
    for name,h in INPUTS.items():
        if sha(BASE/name)!=h:raise ValueError('Changed admitted bytes '+name)
    if OWNER is not None and sha(__file__)!=OWNER['source_sha256']:raise ValueError('Changed own source')

def parent():
    r=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());rc=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    if rc['owner']!='root' or rc['pid']!=75633 or rc['status']!='NUMERICAL_FAILED' or not rc['closed']>rc['started']:raise ValueError('Actual natural parent closure')
    if rc['result_sha256']!=PINS[PARENT+'_RESULT.json'] or rc['source_sha256']!=PINS[PARENT_SOURCE]:raise ValueError('Closed result/source binding')
    if rc['checkpoint_pairs']!=67 or rc['predicate_count']!=305 or len(r['checkpoint_pairs'])!=67 or len(r['controls'])!=305 or len(r['comparisons'])!=56 or len(r['rows'])!=2:raise ValueError('Completed parent census')
    if any(v is not False for v in r['physical_flags'].values()):raise ValueError('Unchanged physical flags')
    for record in r['checkpoint_pairs']:
        p=record['payload'];cn=Path(p).stem+'_COMMIT.json'
        if INPUTS[p]!=record['payload_sha256'] or json.loads((BASE/cn).read_text())!=record:raise ValueError('Whole exact parent commit')
    for name,nstep,target in TARGETS:
        row=next(z for z in r['rows'] if z['trial']['name']==name)
        if row['trial']!=dict(name=name,nstep=nstep,k=.1,omega=.1,ns=32,na=64) or row['history_panel_count']!=nstep or row['maxima']['radiation_density']['nstep']!=target:raise ValueError('Actual recorded first maximum')
        if len(row['frames'])!=33 or len(row['solver_history'])!=nstep or len(row['maxima'])!=19:raise ValueError('Actual full terminal row')
    return r

def install_helpers():
    raw=(BASE/PARENT_SOURCE).read_text();lines=raw.splitlines(keepends=True);tree=ast.parse(raw);selected=[]
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name in HELPER_SPANS:
            if hashlib.sha256(''.join(lines[node.lineno-1:node.end_lineno]).encode()).hexdigest()!=HELPER_SPANS[node.name]:raise ValueError('Exact helper span '+node.name)
            selected.append(node)
    if len(selected)!=7:raise ValueError('Seven exact frozen mathematical definitions')
    ctx=dict(np=np,math=math,RAW=RAW,FLOOR=FLOOR,RULES={n:np.polynomial.legendre.leggauss(n) for n in ORDERS})
    exec(compile(ast.Module(body=selected,type_ignores=[]),PARENT_SOURCE+'::seven_bound_helpers','exec'),ctx)
    return ctx

def checkpoint(label,arrays,meta,failed=False):
    data=canonical(dict(owner=OWNER,context=dict(CONTEXT),failed=failed,physical_flags=FLAGS,metadata=meta,
        schema={n:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for n,v in arrays.items()}))
    if not failed and any(not d['finite'] for d in data['schema'].values()):raise ArithmeticError('Nonfinite accepted diagnostic arrays')
    text=encode(data).decode();data=json.loads(text);p=BASE/(STEM+'_'+str(len(RECORDS)).zfill(5)+'_'+label+'.npz')
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);record=dict(payload=p.name,payload_sha256=CREATED[p.name],metadata=data)
    ch=publish(p.stem+'_COMMIT.json',record);record=dict(record,commit_file=p.stem+'_COMMIT.json',commit_sha256=ch);RECORDS.append(record)
    reread(record,arrays);return record

def reread(record,expected=None):
    bare={k:v for k,v in record.items() if k not in ('commit_file','commit_sha256')}
    if sha(BASE/record['payload'])!=record['payload_sha256'] or sha(BASE/record['commit_file'])!=record['commit_sha256'] or json.loads((BASE/record['commit_file']).read_text())!=bare:raise ValueError('Exact own pair')
    with np.load(BASE/record['payload'],allow_pickle=False) as z:
        if json.loads(str(z['metadata']))!=record['metadata'] or set(z.files)!=set(record['metadata']['schema'])|{'metadata'}:raise ValueError('Whole own NPZ dictionary')
        for name,d in record['metadata']['schema'].items():
            v=z[name]
            if d!=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))):raise ValueError('Exact own array descriptor')
            if expected is not None and not np.array_equal(v,expected[name],equal_nan=True):raise ValueError('Immediate raw array reread')

def close():
    authenticate()
    for name,h in CREATED.items():
        if sha(BASE/name)!=h:raise ValueError('Changed owned output')
    for record in RECORDS:reread(record)
    pairs={r['payload'] for r in RECORDS};commits={r['commit_file'] for r in RECORDS}
    if {p.name for p in BASE.glob(STEM+'_*.npz')}!=pairs or {p.name for p in BASE.glob(STEM+'_*_COMMIT.json')}!=commits:raise ValueError('No orphan or unregistered own pair')
    if STEM+'_OWNER_START.json' in CREATED and json.loads((BASE/(STEM+'_OWNER_START.json')).read_text())!=OWNER:raise ValueError('Exact owner-start')

def load_initial():
    cp=json.loads((BASE/(INITIAL+'_COMMIT.json')).read_text())
    if cp['payload_sha256']!=PINS[INITIAL+'.npz'] or cp['nstep']!=0:raise ValueError('Authentic unchanged incoming CP0')
    with np.load(BASE/(INITIAL+'.npz'),allow_pickle=False) as z:
        values={n:z[n].copy() for n in z.files if n!='metadata'};meta=json.loads(str(z['metadata']))
    RAW.update({'incoming_'+n:v for n,v in values.items()})
    if meta!=cp['metadata'] or set(values)!={'core','native','angular','frame_core','frame_native','frame_angular','last_stage_core','last_stage_native','last_stage_angular'}:raise ValueError('Complete original incoming state')
    if values['core'].shape!=(11,2) or not all(np.all(np.isfinite(v)) for v in values.values()):raise ArithmeticError('Finite two-column original initial state')
    for name in ('core','native','angular'):
        if not np.array_equal(values[name],values['frame_'+name][0]) or len(values['last_stage_'+name])!=0:raise ValueError('Original incoming empty history')
    return values

def load_target(row,record):
    with np.load(BASE/record['payload'],allow_pickle=False) as z:
        values={n:z[n].copy() for n in z.files if n!='metadata'};meta=json.loads(str(z['metadata']))
    RAW.update({'terminal_'+n:v for n,v in values.items()})
    if meta!=record['metadata'] or set(values)!=set(meta['arrays']):raise ValueError('Whole terminal state dictionary')
    nstep=row['trial']['nstep'];target=row['maxima']['radiation_density']['nstep'];m=meta['metadata']
    if m['trial']!=row['trial'] or m['nstep']!=nstep or m['maxima']!=row['maxima'] or m['solver_history']!=row['solver_history']:raise ValueError('Terminal identity/history')
    for n,v in values.items():
        if meta['arrays'][n]!=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))):raise ValueError('Actual terminal schema '+n)
    if values['history_source'].shape!=(nstep,3,4,2) or values['history_theta'].shape!=(nstep,4):raise ValueError('Every authentic source panel')
    if not np.array_equal(values['history_start'][1:],values['history_end'][:-1]) or not np.array_equal(values['history_end'],values['history_start']+values['history_theta'][:,-1]):raise ValueError('Actual contiguous phase clock')
    if not np.array_equal(values['history_source'][1:,0,0],values['history_source'][:-1,0,-1]):raise ValueError('Exact curvature anchors')
    past={n:values['history_'+n][:target-1].copy() for n in ('start','theta','source','end','delta_end','cache16','cache32')}
    theta=values['history_theta'][target-1].copy();source=values['history_source'][target-1].copy();start=float(values['history_start'][target-1]);end=float(values['history_end'][target-1])
    if not np.all(np.diff(theta)>0) or theta[0]!=0 or theta[-1]<=0 or end!=start+theta[-1]:raise ValueError('Actual current phase window')
    return past,theta,source,start,end

def control(name,actual,expected,envelope,tol):
    RAW[name+'_actual']=np.asarray(actual).copy();RAW[name+'_expected']=np.asarray(expected).copy()
    if RAW[name+'_actual'].shape!=RAW[name+'_expected'].shape:raise ValueError('Arithmetic control shape')
    a=RAW[name+'_actual'];b=RAW[name+'_expected'];RAW[name+'_uncanceled_envelope']=np.asarray(envelope).copy()
    if a.shape!=RAW[name+'_uncanceled_envelope'].shape:raise ValueError('Arithmetic envelope shape')
    env=np.maximum(RAW[name+'_uncanceled_envelope'],FLOOR);error=float(np.max(abs(a-b)/env))
    return dict(name=name,error=finite(error),tolerance=tol,passed=math.isfinite(error) and error<=tol)

def one_panel(row,record,initial):
    name=row['trial']['name'];CONTEXT.update(trial=name,target_nstep=row['maxima']['radiation_density']['nstep'],stage='admit_target');RAW.clear();RAW.update({'incoming_'+n:v.copy() for n,v in initial.items()})
    past,theta,source,start,end=load_target(row,record);gamma=initial['core'][8].copy()
    # Keep only the authentic admitted past/current and incoming data in the INPUT pair.
    arrays={**{'past_'+n:v for n,v in past.items()},'current_theta':theta,'current_source':source,'current_start_end':np.asarray([start,end]),'incoming_gamma':gamma,**{'incoming_'+n:v for n,v in initial.items()}}
    context=dict(parent_terminal=record,trial=row['trial'],target_nstep=row['maxima']['radiation_density']['nstep'],parent_original_maxima=row['maxima'])
    input_record=checkpoint(name+'_INPUT',arrays,context);RAW.clear();RAW.update(arrays)
    coef=HELPER['cardinal_coefficients'](theta/theta[-1]);card=HELPER['cardinal'](coef,theta/theta[-1]);reconstructed=np.einsum('ij,fjc->fic',card,source)
    powers=np.asarray([(theta/theta[-1])**m for m in range(4)]).T;card_env=abs(powers)@abs(coef);source_env=np.einsum('ij,fjc->fic',card_env,abs(source))+abs(source)
    controls=[control(name+'_cardinal',card,np.eye(4),card_env+np.eye(4),ARITH_TOL),control(name+'_source_reconstruction',reconstructed,source,source_env,ARITH_TOL)]
    CONTEXT.update(stage='independent_reference');values,envelope=HELPER['history_moments'](past,np.asarray([start,end]),gamma,16);RAW.update(endpoint_past_values=values.copy(),endpoint_past_envelopes=envelope.copy())
    tensor=HELPER['source_tensor'](theta,float(theta[-1]),32);terms=tensor[...,None]*source[:,None,:,:];current=terms.sum(axis=(0,2));RAW.update(endpoint_current_tensor=tensor.copy(),endpoint_current_terms=terms.copy(),endpoint_current_moments=current.copy())
    endpoint=np.vstack([values[0,0],values[1,0]+current[0]]);delta_R=source[0,-1]-source[0,0];RAW.update(endpoint_Y0=endpoint.copy(),endpoint_R=source[0,[0,-1]].copy(),endpoint_A=source[1,[0,-1]].copy(),endpoint_Cp=source[2,[0,-1]].copy(),endpoint_delta_R=delta_R.copy())
    hf,he=HELPER['historical_flux'](past,start,end,gamma);RAW.update(reference_historical_flux=hf.copy(),reference_historical_envelope=he.copy())
    cf,ce=HELPER['current_flux'](theta,source);reference=hf+cf;reference_env=he+ce;balance=endpoint[1]-endpoint[0]-4*delta_R+reference;env=abs(endpoint[1])+abs(endpoint[0])+4*(abs(source[0,-1])+abs(source[0,0]))+reference_env
    RAW.update(reference_current_flux=cf.copy(),reference_current_envelope=ce.copy(),reference_flux=reference.copy(),reference_flux_envelope=reference_env.copy(),reference_balance=balance.copy(),reference_balance_envelope=env.copy())
    reference_rows=[]
    for col in range(2):
        error=float(abs(balance[col])/max(float(env[col]),FLOOR));rr=dict(name=name+'_reference_column_'+str(col),column=col,signed_balance=float(balance[col]),error=finite(error),envelope=float(env[col]),floor=FLOOR,tolerance=BRANCH_TOL,passed=math.isfinite(error) and error<=BRANCH_TOL);controls.append(rr);reference_rows.append(rr)
    checkpoint(name+'_REFERENCE',dict(RAW),dict(context,input_checkpoint=input_record,controls=controls,reference_columns=reference_rows));outcomes=[]
    for order in ORDERS:
        CONTEXT.update(stage='phase_quadrature',order=order);RAW.clear();node,weight=HELPER['RULES'][order];local=theta[-1]*(node+1)/2;ww=theta[-1]*weight/2;targets=start+local;RAW.update(phase_local_nodes=local.copy(),phase_absolute_nodes=targets.copy(),phase_weights=ww.copy())
        past_value,past_env=HELPER['history_moments'](past,targets,gamma,16);RAW.update(past_moments=past_value.copy(),past_moment_envelope=past_env.copy());tensors=[]
        for target in local:
            tensors.append(HELPER['source_tensor'](theta,float(target),32));RAW['current_tensors32']=np.asarray(tensors).copy()
        tensors=np.asarray(tensors);current_terms=tensors[...,None]*source[None,:,None,:,:];current_mom=current_terms.sum(axis=(1,3));current_env=abs(current_terms).sum(axis=(1,3));products=np.einsum('ij,fjc->fic',HELPER['cardinal'](coef,local/theta[-1]),source)
        Y1=past_value[:,1]+current_mom[:,1];integrand=Y1+4*products[1]/3;integrand_env=past_env[:,1]+current_env[:,1]+4*abs(products[1])/3;quadrature_terms=ww[:,None]*integrand;uncanceled_terms=ww[:,None]*integrand_env;flux=quadrature_terms.sum(axis=0);flux_env=uncanceled_terms.sum(axis=0);direct_env=abs(quadrature_terms).sum(axis=0)
        signed=endpoint[1]-endpoint[0]-4*delta_R+flux;den=abs(endpoint[1])+abs(endpoint[0])+4*(abs(source[0,-1])+abs(source[0,0]))+flux_env;diff=flux-reference;diff_env=flux_env+reference_env
        RAW.update(current_contracted_terms=current_terms.copy(),current_moments=current_mom.copy(),current_moment_envelope=current_env.copy(),interpolated_products=products.copy(),Y1=Y1.copy(),physical_flux_integrand=integrand.copy(),physical_integrand_envelope=integrand_env.copy(),quadrature_terms=quadrature_terms.copy(),uncanceled_quadrature_terms=uncanceled_terms.copy(),quadrature_flux=flux.copy(),quadrature_flux_envelope=flux_env.copy(),direct_integrand_absolute_envelope=direct_env.copy(),endpoint_Y0=endpoint.copy(),endpoint_R=source[0,[0,-1]].copy(),endpoint_A=source[1,[0,-1]].copy(),endpoint_Cp=source[2,[0,-1]].copy(),signed_balance=signed.copy(),balance_envelope=den.copy(),signed_reference_difference=diff.copy(),reference_difference_envelope=diff_env.copy())
        rows=[]
        for col in range(2):
            error=float(abs(signed[col])/max(float(den[col]),FLOOR));relative=float(abs(diff[col])/max(float(diff_env[col]),FLOOR));rr=dict(name=name+'_phase'+str(order)+'_column'+str(col),trial=name,target_nstep=context['target_nstep'],order=order,column=col,flux=float(flux[col]),signed_balance=float(signed[col]),uncanceled_envelope=float(den[col]),direct_flux_absolute_envelope=float(direct_env[col]),error=finite(error),error_reason=None if math.isfinite(error) else 'Nonfinite balance ratio; raw arrays retained',signed_reference_difference=float(diff[col]),reference_relative=finite(relative),floor=FLOOR,tolerance=BRANCH_TOL,passed=math.isfinite(error) and error<=BRANCH_TOL);rows.append(rr);outcomes.append(rr)
        checkpoint(name+'_RULE_'+str(order),dict(RAW),dict(context,input_checkpoint=input_record,outcomes=rows))
    return dict(trial=row['trial'],target_nstep=context['target_nstep'],phase_start=start,phase_end=end,phase_width=float(theta[-1]),input_checkpoint=input_record,controls=controls,outcomes=outcomes,parent_original_maxima=row['maxima'])

def main():
    global np,HELPER,INPUTS,OWNER
    if AUTHOR_GUARD:raise RuntimeError('Guarded prospective root-only diagnostic')
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('All existing runtime is preserved')
    INPUTS=resolve_inputs();old=parent();OWNER=dict(owner='root',pid=os.getpid(),source_sha256=sha(__file__),started=now());tick=time.monotonic();cases=[]
    try:
        publish(STEM+'_OWNER_START.json',OWNER);manifest=dict(owner=OWNER,input_sha256=INPUTS,targets=TARGETS,phase_orders=ORDERS,past_order=16,current_order=32,reference_flux_order=32,branch_tolerance=BRANCH_TOL,floor=FLOOR,arithmetic_tolerance=ARITH_TOL,checkpoint_pairs=16,arithmetic_count=8,outcome_count=24,helper_spans=HELPER_SPANS,no_trajectory_replay=True,physical_flags=FLAGS);publish(STEM+'_MANIFEST.json',manifest)
        np=importlib.import_module('numpy');authenticate();HELPER=install_helpers();initial=load_initial()
        for name,nstep,target in TARGETS:
            row=next(r for r in old['rows'] if r['trial']['name']==name);record=next(r for r in old['checkpoint_pairs'] if r['metadata']['label']==name+'_CP_'+str(nstep).zfill(6));cases.append(one_panel(row,record,initial))
        controls=[c for row in cases for c in row['controls']];outcomes=[o for row in cases for o in row['outcomes']]
        if len(RECORDS)!=16 or len(controls)!=8 or len(outcomes)!=24:raise ValueError('Complete prospective census')
        close();status='SHIFTED_FLUX_DIAGNOSTIC_PASS' if all(z['passed'] for z in controls+outcomes) else 'SHIFTED_FLUX_OUTCOMES_RETAINED'
        result=dict(status=status,owner=OWNER,manifest=manifest,cases=cases,arithmetic_controls=controls,outcomes=outcomes,checkpoint_pairs=RECORDS,parent_controls_copied_exactly=old['controls'],parent_comparisons_copied_exactly=old['comparisons'],parent_original_dispositions={k:v for k,v in old.items() if k.endswith('_copied_exactly')},parent_maxima_copied_exactly=[dict(trial=r['trial'],maxima=r['maxima']) for r in old['rows']],parent_physical_flags_copied_exactly=old['physical_flags'],physical_flags=FLAGS,elapsed_seconds=time.monotonic()-tick,scope='Saved-source shifted-flux quadrature only; original log-time gate and full-trajectory failures unchanged')
        rh=publish(STEM+'_RESULT.json',result);text=('# Saved-source same-window shifted radiation flux\n\n'+status+';24 phase branch outcomes and8 supporting arithmetic controls. Original log-time radiation, normal and trace failures remain unchanged.\n').encode();report=BASE/(STEM+'_REPORT.md')
        with report.open('xb') as f:f.write(text);f.flush();os.fsync(f.fileno())
        report.chmod(0o444)
        if report.read_bytes()!=text:raise ValueError('Exact report bytes')
        CREATED[report.name]=sha(report);close();receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,checkpoint_pairs=16,predicate_count=32,physical_flags=FLAGS);publish(STEM+'_RECEIPT.json',receipt);close()
        if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=receipt:raise ValueError('Exact terminal receipt')
        return 0 if status=='SHIFTED_FLUX_DIAGNOSTIC_PASS' else 3
    except Exception:
        trace=traceback.format_exc();rp=BASE/(STEM+'_RECEIPT.json');prior=dict(file=rp.name,sha256=sha(rp),registered_sha256=CREATED.get(rp.name)) if rp.exists() else None;raw_record=None
        if np is not None and RAW:raw_record=checkpoint('ERROR_RAW',dict(RAW),dict(context=CONTEXT,unaccepted=True,protected_prior_receipt=prior),True)
        eh=publish(STEM+'_ERROR.json',dict(status='ERROR_PRESERVED',owner=OWNER,failed=now(),traceback=trace,context=CONTEXT,error_raw=raw_record,protected_prior_receipt=prior,preserved_outputs=dict(CREATED),physical_flags=FLAGS))
        if prior is None:
            receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,physical_flags=FLAGS);publish(STEM+'_RECEIPT.json',receipt)
        else:
            if sha(rp)!=prior['sha256']:raise ValueError('Protected existing receipt changed')
        close();raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args()
    if not args.root_owned:raise RuntimeError('Root-owned execution requires explicit flag')
    raise SystemExit(main())
