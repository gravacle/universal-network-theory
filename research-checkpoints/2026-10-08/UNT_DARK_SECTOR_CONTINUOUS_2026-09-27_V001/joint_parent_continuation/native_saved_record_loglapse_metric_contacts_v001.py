#!/usr/bin/env python3
"""Root-only conditional nonlinear held-material lapse contacts on saved states."""
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
AUTHOR_DRAFT=False
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
STEM='NATIVE_SAVED_RECORD_LOGLAPSE_METRIC_CONTACTS_V001'
SOURCE=HERE/'native_saved_record_loglapse_metric_contacts_v001.py';PROTOCOL=HERE/(STEM+'.md')
OWNER=HERE/(STEM+'_OWNER_START.json');MANIFEST=HERE/(STEM+'_MANIFEST.json');JOURNAL=HERE/(STEM+'_JOURNAL.jsonl')
RESULT=HERE/(STEM+'_RESULT.json');REPORT=HERE/(STEM+'_REPORT.md');RECEIPT=HERE/(STEM+'_RECEIPT.json');ERROR=HERE/(STEM+'_ERROR.json')
PARENT_RESULT=HERE/'NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RESULT.json'
PARENT_RECEIPT=HERE/'NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RECEIPT.json'
POWER_SOURCE=HERE/'native_saved_record_formation_feedback_power_v001.py'
DIM=1536;OP_TOL=1e-11;OBS_TOL=2e-10
UD,LR,LJ,ER,EP,HFLIP,THOP=1.,.5,.25,1.,1.,.1,.1
TICKS=(0,1000,2000,5000,10000,20000,50000,1,-1,2,-2)
LABELS=('main0','main1','main2','main3','main4','main5','main6','early0_plus','early0_minus','early1_plus','early1_minus')
CONTACTS=('Cxx','Cxy','Cyy')
UNITS=dict(Ud=1.,hbar=1.,time='hbar/Ud',contact='Ud per dimensionless eta^2',eta='ell*a_SI/cp^2',physical_contact='Eunit*ell^2/cp^4 times C',physical_conversion=None)
FLAGS={k:False for k in ('physical_lapse_identification','full_Hilbert_stress','independent_U_vertex','physical_record_current','phase_charge_exchange','stable_record_birth','entropy_production','physical_clock','physical_native_inertia','source_history','galactic_force','observational_fit','cosmological_preparation','Stage3_complete')}
OUTPUTS={};RECORDS=[];RAW={};CONTEXT={};SERIAL=0;CONTROL_SERIAL=0;NP=None;SELF_SHA=None
READY_PINS={'/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001.md': 'bf28c601d7369ad1038d73576b82196c0a3596f7422114fcfd5768925b8dd44b', '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RECEIPT.json': 'fd27c9c5ff0a07d10eb9d43c8a7106cf0d969c163177562dc2794907c81da54d', '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001_RESULT.json': 'f0f7a6098188870d31d938de477d5cc9bdbc6b0a6c057b1a624fdedf2c53e008', '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/native_saved_record_formation_feedback_power_v001.py': '60f6520cbdcd66eae8c9506709c23da6b53ab4ff2c3d4954d7853c47e6311c94', '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001.py': '41843d768cde60d3a5404cc1db3e6bd799eb8aa0778856c2d7e020a7bce74428', '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/LOCAL_RECORD_FEEDBACK_MINIMAL_LEGENDRE_LAPSE_MAP_AND_TRANSPORT_FAMILY_V003.md': 'f041160b55cc37e09f6b0ef258012d01d0818ce9a0a80f8d7c0a751f50a2f66f', '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_LOGLAPSE_METRIC_CONTACTS_V001.md': 'fb20f0c491e6bec123c469391caae9601c666461f59e21bf7b30ed9c6aa5cfb9'}
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

def basis(np):
    rows=np.arange(DIM);ns=rows//24;carrier=(rows//4)%6;r=rows%4
    nb=np.array([[(n>>e)&1 for e in range(6)] for n in range(64)],dtype=float)
    p=np.eye(6)[carrier];q=np.zeros((DIM,6));q[:,0]=r&1;q[:,3]=(r>>1)&1
    pos=np.array([(np.cos(2*np.pi*v/6),np.sin(2*np.pi*v/6)) for v in range(6)])
    reflected_n=np.array([sum(((int(n)>>e)&1)<<((-e-1)%6) for e in range(6)) for n in ns])
    reflection=(reflected_n*6+((-carrier)%6))*4+r
    links={};transfers={};copies={}
    for e in range(6):
        links[e]=(rows,((ns^(1<<e))*6+carrier)*4+r)
        use=(nb[ns,e]==1)&((carrier==e)|(carrier==(e+1)%6));src=rows[use]
        newcarrier=np.where(carrier[use]==e,(e+1)%6,e)
        transfers[e]=(src,(ns[use]*6+newcarrier)*4+r[use])
    for bit,v in enumerate((0,3)):
        src=rows[carrier==v];copies[v]=(src,(ns[src]*6+carrier[src])*4+(r[src]^(1<<bit)))
    return dict(rows=rows,ns=ns,carrier=carrier,r=r,nb=nb,p=p,q=q,pos=pos,
                allpos=np.vstack([pos,2*pos]),reflection=reflection,
                links=links,transfers=transfers,copies=copies)

def weighted(np,g,s,lapses):
    value=np.zeros((DIM,DIM));diag=np.zeros(DIM)
    for v in range(6):
        degree=1+s['nb'][s['ns'],(v-1)%6]+s['nb'][s['ns'],v]
        diag+=lapses[v]*(UD*(degree-2)**2+ER*s['q'][:,v]+EP*s['p'][:,v])
        diag+=lapses[v+6]*UD+(lapses[v]+lapses[v+6])/2*(LJ*s['p'][:,v]-LR*s['q'][:,v])
    for e in range(6):
        nxt=(e+1)%6;weight=(lapses[e]+lapses[nxt])/2;n=s['nb'][s['ns'],e]
        a=s['p'][:,e]+s['p'][:,nxt]-2*s['p'][:,e]*s['p'][:,nxt]
        diag+=weight*n*(LJ*a-LR*(s['q'][:,e]+s['q'][:,nxt]))
        for mapping,coefficient in [(s['links'][e],-HFLIP),(s['transfers'][e],-THOP)]:
            src,dst=mapping;value[src,dst]+=weight*coefficient
    for v,(src,dst) in s['copies'].items():value[src,dst]+=g*lapses[v]
    value[s['rows'],s['rows']]=diag
    return value

def matrices(np,g,s,record):
    global RAW,CONTROL_SERIAL
    RAW={};CONTROL_SERIAL=0;CONTEXT.clear();CONTEXT.update(g=g,operation='nonlinear_lapse_contact_matrix')
    parent=load_arrays(np,record,('H','Gx','Gy'))
    if any(a.shape!=(DIM,DIM) or a.dtype.str!='<f8' for a in parent.values()):raise RuntimeError('Admitted H/G matrix shape/dtype')
    r=s['allpos'];RAW['whole_twelve_node_positions']=r
    w=np.stack([np.ones(12),r[:,0],r[:,1]])
    checked=[];checks=[];deltas=[]
    for i,k in enumerate(('H','Gx','Gy')):
        CONTEXT.update(certification=k)
        actual=weighted(np,0. if g=='g0' else .1,s,w[i]);RAW['weighted_'+k]=actual
        delta=actual-parent[k];RAW['weighted_minus_saved_'+k]=delta;deltas.append(delta)
        scale=max(1.,float(np.max(np.sum(np.abs(parent[k]),axis=1))))
        check(np,checks,'uniform_loglapse_H' if i==0 else 'linear_lapse_'+k,np.array(float(np.max(np.abs(delta)))),np.array(0.),OP_TOL,scale)
        checked.append(actual)
    cw=np.stack([r[:,0]*r[:,0],r[:,0]*r[:,1],r[:,1]*r[:,1]]);RAW['complete_node_second_weights']=cw
    cs=[]
    for k,a in zip(CONTACTS,cw):
        CONTEXT.update(contact=k);cs.append(weighted(np,0. if g=='g0' else .1,s,a));RAW['available_contact_matrices']=np.stack(cs)
    C=np.stack(cs);RAW['contact_matrices']=C
    error=np.array([float(np.max(np.abs(a-a.T))) for a in C]);RAW['contact_Hermitian_errors']=error
    check(np,checks,'complete_contact_Hermitian',error,np.zeros(3),OP_TOL,max(1.,float(np.max(np.sum(np.abs(C),axis=-1)))))
    mixed=np.stack([r[:,0]*r[:,1],r[:,1]*r[:,0]]);RAW['mixed_endpoint_weights']=mixed
    check(np,checks,'mixed_endpoint_symmetry',mixed[0],mixed[1],OP_TOL,max(1.,float(np.max(np.abs(mixed)))))
    ends=np.array([(i,(i+1)%6) for i in range(6)]+[(i,i+6) for i in range(6)],dtype=int);u=r[ends[:,0]];v=r[ends[:,1]];m=(u+v)/2;d=u-v
    direct=(np.einsum('ei,ej->eij',u,u)+np.einsum('ei,ej->eij',v,v))/2
    mean=np.einsum('ei,ej->eij',m,m);spread=np.einsum('ei,ej->eij',d,d)/4;reconstructed=mean+spread
    RAW.update(edge_node_indices=ends,edge_endpoint_positions=np.stack([u,v]),edge_second_weights=direct,edge_midpoint_square=mean,edge_endpoint_spread=spread,edge_second_reconstruction=reconstructed)
    check(np,checks,'endpoint_second_jet_identity',direct,reconstructed,OP_TOL,max(1.,float(np.max(np.abs(mean)+np.abs(spread)))))
    if len(checks)!=6:raise RuntimeError('Six matrix control census')
    summary=dict(g=g,copy_g=0. if g=='g0' else .1,controls=checks,qualified=all(x['passed'] for x in checks),parent_H_INPUT=dict(npz=Path(record['npz']).name,npz_sha256=record['npz_sha256'],commit=Path(record['commit']).name,commit_sha256=record['commit_sha256'],expected_fields=['H','Gx','Gy']),units=UNITS,contact_axes=list(CONTACTS),physical_registration=None)
    summary['checkpoint']=checkpoint(np,g+'_MATRICES',RAW,summary)
    return C,summary

def family(np,g,start,C,records,rows,matref,off=None):
    global RAW,CONTROL_SERIAL
    RAW={};CONTROL_SERIAL=0;CONTEXT.clear();CONTEXT.update(g=g,start=start,operation='new_contact_actions')
    states=[];actions=[];means=[];copied=[];bindings=[];operand_keys=('complete_state','component_means_complex','component_powers_complex','complete_energy_complex','complete_source_means_complex','complete_source_powers_complex','all_rates_complex','original_state_norm')
    available={k:[] for k in operand_keys}
    for label,tick in zip(LABELS,TICKS):
        key=g+'_n'+str(start)+'_'+label;row=rows[key];record=records[key];CONTEXT.update(state_key=key,tick=tick)
        if row['g']!=(0. if g=='g0' else .1) or row['start']!=start or row['tau']!=tick/1000.:raise RuntimeError('Exact saved age/preparation')
        a=load_arrays(np,record,operand_keys)
        if a['complete_state'].shape!=(DIM,) or a['component_means_complex'].shape!=(11,) or a['component_powers_complex'].shape!=(11,) or a['all_rates_complex'].shape!=(3,6):raise RuntimeError('Complete saved state/history dimensions')
        for k,x in a.items():available[k].append(x);RAW['available_'+k]=np.stack(available[k])
        psi=a['complete_state'];states.append(psi)
        ca=[]
        for name,c in zip(CONTACTS,C):
            CONTEXT.update(contact=name);ca.append(c@psi);RAW['current_state_contact_actions']=np.stack(ca)
        action=np.stack(ca);actions.append(action);RAW['available_new_contact_actions']=np.stack(actions)
        mean=np.einsum('d,ad->a',psi.conj(),action);means.append(mean);RAW['available_new_contact_means']=np.stack(means)
        copied.append(row);bindings.append(dict(state_key=key,npz=Path(record['npz']).name,npz_sha256=record['npz_sha256'],commit=Path(record['commit']).name,commit_sha256=record['commit_sha256']))
    states=np.stack(states);actions=np.stack(actions);means=np.stack(means);RAW.update(saved_complete_states=states,new_contact_actions=actions,new_contact_means=means,time_ticks=np.array(TICKS,dtype=np.int64))
    envelope=np.einsum('td,tad->ta',np.abs(states),np.abs(actions));RAW['contact_expectation_uncancelled_envelope']=envelope
    checks=[];check(np,checks,'Hermitian_contact_means',means.imag,np.zeros((11,3)),OBS_TOL,max(1.,float(envelope.max())))
    if off is not None:RAW.update(copy_off_contact_means=off,signed_active_minus_null=means-off)
    for k,x in available.items():RAW['copied_'+k]=np.stack(x)
    summary=dict(g=g,copy_g=0. if g=='g0' else .1,start=start,controls=checks,qualified=checks[0]['passed'],matrix_checkpoint=matref,parent_state_pairs=bindings,copied_power_state_summaries=copied,contact_axes=list(CONTACTS),time_ticks=list(TICKS),units=UNITS,signed_contact_means_real=means.real.tolist(),signed_contact_means_imag=means.imag.tolist(),active_minus_null_real=None if off is None else (means-off).real.tolist(),active_minus_null_imag=None if off is None else (means-off).imag.tolist(),physical_registration=None)
    summary['checkpoint']=checkpoint(np,g+'_n'+str(start)+'_STATES',RAW,summary)
    return summary,means

def main():
    global NP,SELF_SHA,RAW
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root-execute',action='store_true');args=a.parse_args()
    if not args.root_execute:print(json.dumps(dict(prospective=True,AUTHOR_DRAFT=AUTHOR_DRAFT,families=4,states=44,new_checks=16,pairs=6,conditional_lapse_rule=True)));return 0
    if AUTHOR_DRAFT:raise RuntimeError('Author draft refuses execution')
    if sys.platform!='darwin' or Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Root Mac/source context')
    if [p for p in HERE.glob(STEM+'*') if p!=PROTOCOL]:raise FileExistsError('Exclusive namespace already used')
    parent,records,rows=authenticate();SELF_SHA=sha(SOURCE)
    ownerbytes=encoded(dict(pid=os.getpid(),utc=datetime.now(timezone.utc).isoformat(),source_sha256=SELF_SHA,parent_pid=3631,parent_result_sha256=READY_PINS[str(PARENT_RESULT)]))
    summaries=[];matrix_summaries=[];checks=[];off={}
    try:
        exclusive(OWNER,ownerbytes)
        exclusive(MANIFEST,dict(pid=os.getpid(),source_sha256=SELF_SHA,inputs=PINS,parent_result_sha256=READY_PINS[str(PARENT_RESULT)],parent_receipt_sha256=READY_PINS[str(PARENT_RECEIPT)],candidate_rule='N_v=exp(zeta+eta_i r_vi); held material endpoints before old halfedge averaging',new_checks=16,planned_pairs=6,states=44,units=UNITS,physical_flags=FLAGS))
        JOURNAL.touch(exist_ok=False);journal('OWNER_START',source_sha256=SELF_SHA)
        for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[n]='1'
        import numpy as np
        NP=np;s=basis(np)
        for g in ('g0','g1'):
            C,m=matrices(np,g,s,records[g+'_H_INPUT']);matrix_summaries.append(m);checks+=m['controls']
            for start in (21,42):
                q,values=family(np,g,start,C,records,rows,m['checkpoint'],off.get(start) if g=='g1' else None);summaries.append(q);checks+=q['controls']
                if g=='g0':off[start]=values
            del C
        if len(checks)!=16 or len(RECORDS)!=6 or len(summaries)!=4 or len(matrix_summaries)!=2:raise RuntimeError('Prospective complete census')
        recheck(ownerbytes);status='ARITHMETIC_PASS' if all(x['passed'] for x in checks) else 'ARITHMETIC_FAILED'
        result=dict(status=status,pid=os.getpid(),source_sha256=SELF_SHA,inputs=PINS,parent_pid=3631,parent_result_sha256=READY_PINS[str(PARENT_RESULT)],copied_power_checks=parent['new_controls'],copied_BS10_checks=parent['copied_parent_checks'],copied_parent_outcome=parent['status'],new_checks=checks,new_check_count=16,passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),matrices=matrix_summaries,families=summaries,records=RECORDS,units=UNITS,physical_flags=FLAGS,physical_unknowns=dict(full_metric_source=None,material_coframe=None,independent_U=None,map_count_reactions=None,physical_clock=None,physical_normalization=None,source_history=None,galaxy_force=None))
        exclusive(RESULT,result)
        exclusive(REPORT,('# Conditional held-material log-lapse metric contacts V001\n\nStatus '+status+'. New arithmetic controls '+str(result['passed'])+'/16; six complete pairs, all44 old states and1076+656 copied controls retained.\n\nOnly new Cxx/Cxy/Cyy actions are generated. Endpoint averaging and geometric contacts remain signed. This candidate is not a full metric/source/current law, physical normalization, galaxy force or an added energy budget. No state/trajectory/old spectrum was replayed.\n').encode())
        journal('CLOSED',status=status,pairs=6,new_checks=16);JOURNAL.chmod(0o444);OUTPUTS[str(JOURNAL)]=sha(JOURNAL)
        recheck(ownerbytes);receipt=dict(status='CLOSED',outcome=status,pid=os.getpid(),source_sha256=SELF_SHA,inputs=dict(PINS),outputs=dict(OUTPUTS),records=RECORDS,physical_flags=FLAGS)
        exclusive(RECEIPT,receipt);recheck(ownerbytes)
        if json.loads(RECEIPT.read_text())!=receipt:raise RuntimeError('Complete terminal receipt')
        print(json.dumps(dict(status=status,checks=16,passed=result['passed'],failed=result['failed'],states=44,pairs=6,result_sha256=OUTPUTS[str(RESULT)],receipt_sha256=OUTPUTS[str(RECEIPT)])))
        return 0 if status=='ARITHMETIC_PASS' else 3
    except BaseException as exc:failure(exc,ownerbytes);raise

if __name__=='__main__':sys.exit(main())
