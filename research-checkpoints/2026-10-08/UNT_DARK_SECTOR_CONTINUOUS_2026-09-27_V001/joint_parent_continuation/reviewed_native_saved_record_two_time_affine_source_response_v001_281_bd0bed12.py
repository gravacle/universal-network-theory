#!/usr/bin/env python3
"""Root-only prepared two-time source response from closed BS10 power arrays."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import traceback
AUTHOR_DRAFT=True
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
STEM='NATIVE_SAVED_RECORD_TWO_TIME_AFFINE_SOURCE_RESPONSE_V001'
SOURCE=HERE/'native_saved_record_two_time_affine_source_response_v001.py';PROTOCOL=HERE/(STEM+'.md')
OWNER=HERE/(STEM+'_OWNER_START.json');MANIFEST=HERE/(STEM+'_MANIFEST.json');JOURNAL=HERE/(STEM+'_JOURNAL.jsonl')
RESULT=HERE/(STEM+'_RESULT.json');REPORT=HERE/(STEM+'_REPORT.md');RECEIPT=HERE/(STEM+'_RECEIPT.json');ERROR=HERE/(STEM+'_ERROR.json')
PARENT_RESULT=HERE/'NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RESULT.json'
PARENT_RECEIPT=HERE/'NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RECEIPT.json'
POWER_SOURCE=HERE/'native_saved_record_formation_feedback_power_v001.py'
DIM=1536;TOL=2e-10
TICKS=(0,1000,2000,5000,10000,20000,50000,1,-1,2,-2)
LABELS=('main0','main1','main2','main3','main4','main5','main6','early0_plus','early0_minus','early1_plus','early1_minus')
UNITS=dict(Ud=1.,hbar=1.,time='hbar/Ud',kernel='Ud^2/hbar',physical_conversion=None)
FLAGS={k:False for k in ('physical_source_metric','physical_record_current','phase_charge_exchange','stable_record_birth','entropy_production','physical_clock','physical_native_inertia','source_history','galactic_force','observational_fit','cosmological_preparation','Stage3_complete')}
OUTPUTS={};RECORDS=[];RAW={};CONTEXT={};SERIAL=0;CONTROL_SERIAL=0;NP=None;SELF_SHA=None
READY_PINS={
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001.md':'bf28c601d7369ad1038d73576b82196c0a3596f7422114fcfd5768925b8dd44b',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RECEIPT.json':'fd27c9c5ff0a07d10eb9d43c8a7106cf0d969c163177562dc2794907c81da54d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RESULT.json':'f0f7a6098188870d31d938de477d5cc9bdbc6b0a6c057b1a624fdedf2c53e008',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_TWO_TIME_AFFINE_SOURCE_RESPONSE_V001.md':'2ca22fe9ed66ef2352e37909c6b8324561702b6e9fe7567342c01accabeb6e4d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/native_saved_record_formation_feedback_power_v001.py':'60f6520cbdcd66eae8c9506709c23da6b53ab4ff2c3d4954d7853c47e6311c94',
}
PINS=dict(READY_PINS)

def enc(value):
    if isinstance(value,dict):return {str(k):enc(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [enc(v) for v in value]
    if hasattr(value,'item'):return enc(value.item())
    if isinstance(value,float) and not math.isfinite(value):raise ValueError('Nonfinite JSON scalar')
    return value

def encoded(value):return (json.dumps(enc(value),sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def exclusive(path,data):
    data=data if isinstance(data,bytes) else encoded(data)
    with Path(path).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    Path(path).chmod(0o444);OUTPUTS[str(path)]=sha(path)
    if Path(path).read_bytes()!=data:raise RuntimeError('Publication bytes differ')
    return OUTPUTS[str(path)]

def journal(kind,**data):
    row=encoded(dict(event=kind,pid=os.getpid(),utc=datetime.now(timezone.utc).isoformat(),**data))
    with JOURNAL.open('ab') as f:f.write(row.replace(b'\n',b'')+b'\n');f.flush();os.fsync(f.fileno())

def finite(np,a):
    a=np.asarray(a)
    return a.dtype.kind in 'biufc' and bool(np.isfinite(a).all())

def checkpoint(np,key,arrays,meta,qualified=True):
    global SERIAL
    SERIAL+=1;p=HERE/(STEM+'_'+str(SERIAL).zfill(5)+'_'+key+'.npz');cp=p.with_suffix('.COMMIT.json')
    local={str(k):np.asarray(v) for k,v in arrays.items()}
    if any(a.dtype.kind=='O' for a in local.values()):raise TypeError('Object checkpoint operand')
    if qualified and any(not finite(np,a) for a in local.values()):raise ArithmeticError('Nonfinite qualified checkpoint')
    text=encoded(dict(meta,record_key=key,serial=SERIAL,source_sha256=SELF_SHA,parent_result_sha256=PINS[str(PARENT_RESULT)],operand_schema_qualified=qualified)).decode()
    detached=json.loads(text);local['metadata_json']=np.array(text)
    with p.open('xb') as f:np.savez(f,**local);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);ph=sha(p);OUTPUTS[str(p)]=ph
    commit=dict(checkpoint=p.name,sha256=ph,metadata=detached,arrays={n:dict(shape=list(a.shape),dtype=a.dtype.str) for n,a in local.items()},owner_pid=os.getpid(),status='ACCEPTED_RAW' if qualified else 'UNQUALIFIED_RAW')
    exclusive(cp,commit)
    with np.load(p,allow_pickle=False) as z:
        if set(z.files)!=set(local):raise RuntimeError('Checkpoint array names changed')
        for n,a in local.items():
            b=z[n]
            if a.shape!=b.shape or a.dtype!=b.dtype or not (np.array_equal(a,b,equal_nan=True) if a.dtype.kind in 'biufc' else np.array_equal(a,b)):raise RuntimeError('Checkpoint array reread')
        if json.loads(str(z['metadata_json']))!=detached:raise RuntimeError('Checkpoint metadata reread')
    rec=dict(npz=str(p),npz_sha256=ph,commit=str(cp),commit_sha256=OUTPUTS[str(cp)],metadata=detached,commit_object=commit)
    RECORDS.append(rec);journal('checkpoint',key=key,npz=p.name,npz_sha256=ph,commit=cp.name,commit_sha256=OUTPUTS[str(cp)])
    return dict(npz=p.name,npz_sha256=ph,commit=cp.name,commit_sha256=OUTPUTS[str(cp)])

def check(np,checks,name,actual,expected,tol,scale=1.):
    global CONTROL_SERIAL
    CONTROL_SERIAL+=1;prefix='control_'+str(CONTROL_SERIAL).zfill(5)+'_'+name
    a=np.asarray(actual);b=np.asarray(expected);RAW[prefix+'_actual']=a;RAW[prefix+'_expected']=b
    CONTEXT.update(control_ordinal=CONTROL_SERIAL,control_name=name)
    if a.shape!=b.shape or not finite(np,a) or not finite(np,b) or not math.isfinite(float(scale)) or scale<=0:raise ArithmeticError('Control operand schema/finite')
    error=float(np.max(np.abs(a-b))) if a.size else 0.
    passed=error<=tol*scale
    checks.append(dict(name=name,passed=passed,maximum_absolute_error=error,scale=float(scale),tolerance=float(tol),raw_prefix=prefix))
    return passed

def recheck(ownerbytes,strict=True,owner_required=True):
    for p,h in PINS.items():
        if sha(p)!=h:raise RuntimeError('Input seal changed')
    if owner_required and (not OWNER.exists() or OWNER.read_bytes()!=ownerbytes):raise RuntimeError('Owner bytes changed')
    for r in RECORDS:
        if sha(r['npz'])!=r['npz_sha256'] or sha(r['commit'])!=r['commit_sha256'] or json.loads(Path(r['commit']).read_text())!=r['commit_object']:raise RuntimeError('Complete pair closure')
        with NP.load(r['npz'],allow_pickle=False) as z:
            if set(z.files)!=set(r['commit_object']['arrays']):raise RuntimeError('Final pair array names')
            if json.loads(str(z['metadata_json']))!=r['metadata']:raise RuntimeError('Final pair metadata')
            for k,d in r['commit_object']['arrays'].items():
                a=z[k]
                if list(a.shape)!=d['shape'] or a.dtype.str!=d['dtype'] or (k!='metadata_json' and r['metadata']['operand_schema_qualified'] and not finite(NP,a)):raise RuntimeError('Final pair schema/finite')
    if strict:
        expected={Path(r['npz']).name for r in RECORDS};actual={p.name for p in HERE.glob(STEM+'_*.npz')}
        ce={Path(r['commit']).name for r in RECORDS};ca={p.name for p in HERE.glob(STEM+'_*.COMMIT.json')}
        if expected!=actual or ce!=ca:raise RuntimeError('Orphan payload/commit')
    for p,h in OUTPUTS.items():
        if Path(p)!=JOURNAL and sha(p)!=h:raise RuntimeError('Output seal changed')

def failure(exc,ownerbytes):
    trace=traceback.format_exc();preservation=None
    if NP is not None and RAW:
        try:checkpoint(NP,'ERROR_RAW',RAW,dict(error_context=CONTEXT,traceback=trace),False)
        except BaseException:preservation=traceback.format_exc()
    preserved_receipt_sha=sha(RECEIPT) if RECEIPT.exists() else None
    for p in HERE.glob(STEM+'*'):
        if p==PROTOCOL or not p.is_file() or p==ERROR:continue
        p.chmod(0o444);OUTPUTS[str(p)]=sha(p)
    orphans=[p.name for p in HERE.glob(STEM+'_*.npz') if str(p) not in {r['npz'] for r in RECORDS}]
    obj=dict(status='CLOSED_ERROR',pid=os.getpid(),source_sha256=SELF_SHA,error_context=CONTEXT,traceback=trace,raw_preservation_traceback=preservation,inputs=PINS,outputs=dict(OUTPUTS),records=RECORDS,unqualified_orphan_payloads=orphans,preserved_receipt_sha256=preserved_receipt_sha,physical_flags=FLAGS)
    if not ERROR.exists():exclusive(ERROR,obj)
    if not RECEIPT.exists():exclusive(RECEIPT,dict(status='CLOSED_ERROR',pid=os.getpid(),inputs=PINS,outputs=dict(OUTPUTS),records=RECORDS,physical_flags=FLAGS))
    if preserved_receipt_sha is not None and sha(RECEIPT)!=preserved_receipt_sha:raise RuntimeError('Prior receipt changed')
    recheck(ownerbytes,False,OWNER.exists() and OWNER.read_bytes()==ownerbytes)

def authenticate():
    for p,h in READY_PINS.items():
        if sha(p)!=h:raise RuntimeError('Direct parent bytes changed')
    r=json.loads(PARENT_RESULT.read_text());c=json.loads(PARENT_RECEIPT.read_text())
    if r['status']!='ARITHMETIC_PASS' or r['passed']!=1076 or r['failed']!=0 or r['new_control_count']!=1076 or len(r['states'])!=44 or len(r['records'])!=46:raise RuntimeError('Power result census/outcome')
    if c['status']!='CLOSED' or c['outcome']!=r['status'] or c['pid']!=r['pid'] or c['pid']!=3631 or c['source_sha256']!=READY_PINS[str(POWER_SOURCE)] or c['records']!=r['records'] or c['inputs']!=r['inputs']:raise RuntimeError('Power receipt/result owner/binding')
    if any(c['physical_flags'].values()) or c['physical_flags']!=r['physical_flags']:raise RuntimeError('Parent physical qualification changed')
    if len(r['new_controls'])!=1076 or any(x['passed'] is not True for x in r['new_controls']) or len(r['copied_parent_checks'])!=656 or any(x['passed'] is not True for x in r['copied_parent_checks']):raise RuntimeError('Copied old/new predicates')
    seals=dict(READY_PINS)
    for mapping in (c['inputs'],c['outputs']):
        for p,h in mapping.items():
            if p in seals and seals[p]!=h:raise RuntimeError('Contradictory parent seal')
            seals[p]=h
    seals[str(POWER_SOURCE)]=c['source_sha256']
    for p,h in seals.items():
        if sha(p)!=h:raise RuntimeError('Full closed power map changed: '+p)
    records={}
    for x in c['records']:
        m=x['metadata'];key=m['record_key']
        if key in records or json.loads(Path(x['commit']).read_text())!=x['commit_object'] or x['commit_object']['metadata']!=m:raise RuntimeError('Power full pair metadata')
        if c['outputs'].get(x['npz'])!=x['npz_sha256'] or c['outputs'].get(x['commit'])!=x['commit_sha256']:raise RuntimeError('Power pair output membership')
        if m['source_sha256']!=c['source_sha256'] or m['operand_schema_qualified'] is not True or m['qualified'] is not True or x['commit_object']['status']!='ACCEPTED_RAW':raise RuntimeError('Power record qualification')
        records[key]=x
    if set(records)!=set(['g0_H_INPUT','g1_H_INPUT']+[g+'_n'+str(start)+'_'+name for g in ('g0','g1') for start in (21,42) for name in LABELS]):raise RuntimeError('Power exact pair key census')
    rows={x['state_key']:x for x in r['states']}
    for key,row in rows.items():
        rec=records[key];m=rec['metadata']
        if row['checkpoint']['npz']!=Path(rec['npz']).name or row['checkpoint']['npz_sha256']!=rec['npz_sha256'] or row['checkpoint']['commit']!=Path(rec['commit']).name or row['checkpoint']['commit_sha256']!=rec['commit_sha256']:raise RuntimeError('Power state final binding')
        for k,v in row.items():
            if k!='checkpoint' and m.get(k)!=v:raise RuntimeError('Power state summary/metadata mismatch')
    if len(rows)!=44:raise RuntimeError('Power duplicate state summaries')
    PINS.update(seals)
    return r,records,rows

def load_arrays(np,record,names):
    with np.load(record['npz'],allow_pickle=False) as z:
        if set(z.files)!=set(record['commit_object']['arrays']) or json.loads(str(z['metadata_json']))!=record['metadata']:raise RuntimeError('Power payload metadata/schema')
        out={}
        for k in names:
            a=z[k].copy();RAW['current_parent_'+k]=a;d=record['commit_object']['arrays'][k]
            if a.dtype.kind not in 'biufc' or list(a.shape)!=d['shape'] or a.dtype.str!=d['dtype'] or not finite(np,a):raise ArithmeticError('Parent numeric payload schema')
            out[k]=a
        return out

def family(np,g,start,E,V,records,rows):
    global RAW,CONTROL_SERIAL
    RAW={};CONTROL_SERIAL=0;CONTEXT.clear();CONTEXT.update(g=g,start=start,operation='spectral_columns')
    psi=[];source=[];means=[];bindings=[]
    for label,tick in zip(LABELS,TICKS):
        key=g+'_n'+str(start)+'_'+label;r=rows[key];rec=records[key]
        if r['g']!=(0. if g=='g0' else .1) or r['start']!=start or r['tau']!=tick/1000.:raise RuntimeError('Exact parent age identity')
        a=load_arrays(np,rec,('complete_state','complete_source_actions','complete_source_means_complex'))
        if a['complete_state'].shape!=(DIM,) or a['complete_source_actions'].shape!=(2,DIM) or a['complete_source_means_complex'].shape!=(2,):raise RuntimeError('Parent column dimensions')
        psi.append(a['complete_state']);RAW['available_saved_states']=np.stack(psi);source.append(a['complete_source_actions']);RAW['available_saved_source_columns']=np.stack(source);means.append(a['complete_source_means_complex']);RAW['available_saved_source_means']=np.stack(means);bindings.append(dict(state_key=key,npz=Path(rec['npz']).name,npz_sha256=rec['npz_sha256'],commit=Path(rec['commit']).name,commit_sha256=rec['commit_sha256']))
    psi=np.stack(psi);source=np.stack(source);means=np.stack(means)
    RAW.update(complete_saved_states=psi,complete_saved_source_columns=source,saved_source_means=means,complete_eigenvalues=E,time_ticks=np.array(TICKS,dtype=np.int64))
    columns=[]
    for x in source:
        columns.append((V.T@x.T).T);RAW['available_spectral_source_columns']=np.stack(columns)
    C=np.stack(columns);RAW['spectral_source_columns']=C
    reconstructed=[]
    for x in C:
        reconstructed.append((V@x.T).T);RAW['available_column_reconstruction']=np.stack(reconstructed)
    reconstructed=np.stack(reconstructed);RAW['source_column_reconstruction']=reconstructed
    checks=[];column_scale=max(1.,float(np.max(np.abs(source))))
    check(np,checks,'complete_spectral_source_column',reconstructed,source,TOL,column_scale)
    observed=np.einsum('td,tad->ta',psi.conj(),source);RAW['same_state_source_means']=observed
    check(np,checks,'same_saved_source_means',observed,means,TOL,max(1.,float(np.max(np.abs(means)))))
    sourcecp=checkpoint(np,g+'_n'+str(start)+'_COLUMNS',RAW,dict(g=g,start=start,parent_state_pairs=bindings,spectral_column_axes=['Gx','Gy'],units=UNITS,controls=checks,qualified=all(x['passed'] for x in checks)))
    # Full absolute E and saved phase origins remain; there is no gap or mean-energy subtraction.
    nt=len(TICKS);z=np.zeros((2,2,nt,nt),dtype=complex);independent=np.zeros((2,2,nt,nt));contrib=np.zeros((2,2,nt,nt,DIM),dtype=complex);phase=np.zeros((nt,nt,DIM),dtype=complex);done=np.zeros((nt,nt),dtype=bool)
    RAW.update(current_complex_product=z,current_independent_kernel=independent,current_signed_interference=contrib,current_absolute_phase=phase,current_completed_time_pairs=done)
    for it,t in enumerate(TICKS):
        for js,s in enumerate(TICKS):
            CONTEXT.update(target_tick=t,source_tick=s,target_index=it,source_index=js)
            delta=(t-s)/1000.;phase[it,js]=np.exp(-1j*E*delta)
            for a in range(2):
                for b in range(2):
                    v=C[it,a].conj()*C[js,b];term=v*phase[it,js];contrib[a,b,it,js]=term;z[a,b,it,js]=np.sum(term)
                    independent[a,b,it,js]=-2*np.sum(v.imag*np.cos(E*delta)-v.real*np.sin(E*delta))
            done[it,js]=True
    chi=-2*z.imag;envelope=2*np.sum(np.abs(contrib),axis=-1);scale=max(1.,float(envelope.max()))
    RAW.update(absolute_energy_phase=phase,full_signed_spectral_interference=contrib,complex_two_time_product=z,full_prepared_commutator_kernel=chi,independent_trigonometric_kernel=independent,uncancelled_spectral_envelope=envelope)
    check(np,checks,'full_kernel_independent_sum',chi,independent,TOL,scale)
    opposite=-chi.transpose(1,0,3,2);RAW['kernel_antisymmetric_partner']=opposite
    check(np,checks,'Hermitian_commutator_antisymmetry',chi,opposite,TOL,scale)
    auto=np.array([[chi[a,a,it,it] for it in range(nt)] for a in range(2)])
    check(np,checks,'equal_time_self_commutator_zero',auto,np.zeros((2,nt)),TOL,scale)
    mirror=[i for i,t in enumerate(TICKS) if -t in TICKS];mi=[TICKS.index(-TICKS[i]) for i in mirror]
    now=chi[:,:,mirror,:][:,:,:,mirror];rev=-chi[:,:,mi,:][:,:,:,mi]
    RAW.update(time_reversal_available_indices=np.array(mirror,dtype=int),time_reversal_kernel=rev,time_reversal_original=now)
    check(np,checks,'available_saved_time_reversal',now,rev,TOL,scale)
    dt=np.subtract.outer(np.array(TICKS,dtype=np.int64),np.array(TICKS,dtype=np.int64));causal=dt>0;equal=dt==0;RAW.update(strict_retarded_mask=causal,equal_time_mask=equal,retarded_kernel_strict_mask=chi*causal[None,None],fixed_affine_direct_contact=np.zeros((2,2)))
    triples=[(it,js,TICKS.index(t-s)) for it,t in enumerate(TICKS) for js,s in enumerate(TICKS) if t-s in TICKS]
    contrasts=np.stack([chi[:,:,it,js]-chi[:,:,ds,0] for it,js,ds in triples],axis=-1)
    RAW.update(nonstationary_translation_indices=np.array(triples,dtype=np.int64),nonstationary_translation_differences=contrasts)
    if len(checks)!=6:raise RuntimeError('Six family arithmetic control census')
    summary=dict(g=g,copy_g=0. if g=='g0' else .1,start=start,parent_state_pairs=bindings,column_checkpoint=sourcecp,controls=checks,qualified=all(x['passed'] for x in checks),time_ticks=list(TICKS),time_units='0.001 hbar/Ud',kernel_shape=[2,2,11,11],kernel_sign='chi=i<[GA(t),GB(s)]>/hbar=-2Im z/hbar; plus-source response=-integral chi deltaL',strict_causal_mask_definition='t>s; all equal-time values preserved independently',absolute_energy_and_preparation_retained=True,nonstationarity_pairs=len(triples),nonstationarity_is_not_gate=True,direct_affine_contact=0.,physical_source_registration=None)
    summary['kernel_checkpoint']=checkpoint(np,g+'_n'+str(start)+'_KERNEL',RAW,summary)
    return summary,chi,independent,envelope

def main():
    global NP,SELF_SHA,RAW,CONTROL_SERIAL
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root-execute',action='store_true');args=a.parse_args()
    if not args.root_execute:print(json.dumps(dict(prospective=True,AUTHOR_DRAFT=AUTHOR_DRAFT,families=4,times=11,axes=2,new_checks=26,pairs=10,power_closed=True,saved_power_audits_required=True)));return 0
    if AUTHOR_DRAFT:raise RuntimeError('Author draft refuses execution')
    if sys.platform!='darwin' or Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Root Mac/source context')
    if [p for p in HERE.glob(STEM+'*') if p!=PROTOCOL]:raise FileExistsError('Exclusive namespace already used')
    parent,records,rows=authenticate();SELF_SHA=sha(SOURCE)
    ownerbytes=encoded(dict(pid=os.getpid(),utc=datetime.now(timezone.utc).isoformat(),source_sha256=SELF_SHA,parent_pid=3631,parent_result_sha256=READY_PINS[str(PARENT_RESULT)]))
    summaries=[];checks=[];kernels={};trig={};envelopes={}
    try:
        exclusive(OWNER,ownerbytes)
        exclusive(MANIFEST,dict(pid=os.getpid(),source_sha256=SELF_SHA,inputs=PINS,parent_result_sha256=READY_PINS[str(PARENT_RESULT)],parent_receipt_sha256=READY_PINS[str(PARENT_RECEIPT)],family_count=4,time_ticks=list(TICKS),axes=['Gx','Gy'],planned_pairs=10,new_checks=26,units=UNITS,physical_flags=FLAGS))
        JOURNAL.touch(exist_ok=False);journal('OWNER_START',source_sha256=SELF_SHA)
        for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[n]='1'
        import numpy as np
        NP=np
        for g in ('g0','g1'):
            RAW={};CONTEXT.clear();CONTEXT.update(g=g,operation='authentic_spectrum')
            data=load_arrays(np,records[g+'_H_INPUT'],('complete_eigenvalues','eigenvectors_columns'))
            E=data['complete_eigenvalues'];V=data['eigenvectors_columns']
            if E.shape!=(DIM,) or V.shape!=(DIM,DIM):raise RuntimeError('Full parent spectrum dimension')
            for start in (21,42):
                summary,k,kt,e=family(np,g,start,E,V,records,rows);summaries.append(summary);checks+=summary['controls'];kernels[g,start]=k;trig[g,start]=kt;envelopes[g,start]=e
            del E,V,data
        for start in (21,42):
            RAW={};CONTROL_SERIAL=0;CONTEXT.clear();CONTEXT.update(start=start,operation='paired_copy_on_minus_off')
            delta=kernels['g1',start]-kernels['g0',start];ind=trig['g1',start]-trig['g0',start];env=envelopes['g1',start]+envelopes['g0',start]
            RAW.update(copy_on_kernel=kernels['g1',start],copy_off_kernel=kernels['g0',start],signed_active_minus_null=delta,independent_active_minus_null=ind,uncancelled_paired_envelope=env,time_ticks=np.array(TICKS,dtype=np.int64))
            cc=[];check(np,cc,'paired_signed_active_minus_null',delta,ind,TOL,max(1.,float(env.max())));checks+=cc
            checkpoint(np,'n'+str(start)+'_ON_MINUS_OFF',RAW,dict(start=start,controls=cc,qualified=cc[0]['passed'],not_force_or_gain=True,parent_family_keys=['g0_n'+str(start),'g1_n'+str(start)]))
        if len(checks)!=26 or len(RECORDS)!=10 or len(summaries)!=4:raise RuntimeError('Complete fixed prospective census')
        recheck(ownerbytes);status='ARITHMETIC_PASS' if all(x['passed'] for x in checks) else 'ARITHMETIC_FAILED'
        result=dict(status=status,pid=os.getpid(),source_sha256=SELF_SHA,inputs=PINS,parent_pid=3631,parent_result_sha256=READY_PINS[str(PARENT_RESULT)],copied_power_checks=parent['new_controls'],copied_BS10_checks=parent['copied_parent_checks'],copied_parent_outcome=parent['status'],new_checks=checks,new_check_count=26,passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),families=summaries,records=RECORDS,units=UNITS,physical_flags=FLAGS,physical_unknowns=dict(source_metric_map=None,source_history=None,source_dependent_preparation=None,physical_clock=None,galaxy_force=None,continuum_sigma=None))
        exclusive(RESULT,result)
        report=('# Saved prepared two-time native affine source response V001\n\nStatus '+status+'. New arithmetic checks '+str(result['passed'])+'/26. Four complete paired families retain all11 existing ages, all2-axis matrix entries, both copy arms and both ice preparations; old1076+656 controls unchanged.\n\nSigned kernels, nonstationarity and active-minus-null are native source-response outcomes; no positive gain, physical metric/stress, formation history, inertia or galaxy-force claim. No prepared trajectory or constructor was rerun.\n')
        exclusive(REPORT,report.encode());journal('CLOSED',status=status,pairs=10,new_checks=26);JOURNAL.chmod(0o444);OUTPUTS[str(JOURNAL)]=sha(JOURNAL)
        recheck(ownerbytes);receipt=dict(status='CLOSED',outcome=status,pid=os.getpid(),source_sha256=SELF_SHA,inputs=dict(PINS),outputs=dict(OUTPUTS),records=RECORDS,physical_flags=FLAGS)
        exclusive(RECEIPT,receipt);recheck(ownerbytes)
        if json.loads(RECEIPT.read_text())!=receipt:raise RuntimeError('Full terminal receipt mismatch')
        print(json.dumps(dict(status=status,checks=26,passed=result['passed'],failed=result['failed'],families=4,pairs=10,result_sha256=OUTPUTS[str(RESULT)],receipt_sha256=OUTPUTS[str(RECEIPT)])))
        return 0 if status=='ARITHMETIC_PASS' else 3
    except BaseException as exc:failure(exc,ownerbytes);raise

if __name__=='__main__':sys.exit(main())
