#!/usr/bin/env python3
"""Saved-state spectral weight only; root owns execution after static review."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,re,time,traceback
from pathlib import Path
import numpy as np

J=Path(__file__).resolve().parent; ROOT=J.parent.parent
NAME='FLOATING_RETURN_C8_PREPARED_SPECTRAL_BINDING_V001'
STEM='floating_return_c8_prepared_spectral_binding_v001'
PROTOCOL_SHA='25ca8b91cc3f30cf46e210036eeb04564a44e7fd570904ce53de0799667d525b'
CP=J/(STEM+'_checkpoints')
RESULT,REPORT,RECEIPT,ERROR=[J/(NAME+x) for x in ('_RESULT.json','_RESULT.md','_RECEIPT.json','_ERROR.json')]
TAG='FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001'; TS='floating_return_c8_tagged_probe_reaction_v001'
RESET='FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001'; RS='floating_return_c8_endpoint_record_isolation_v001'
RES='FLOATING_RETURN_C8_RECORD_INTERACTION_RESOLVENT_V001'
TIMES=('0','1/5','2','8'); EPS=1e-9; TOL=5e-10
FORMATION_TIMES=('0','1/10','1/5','2/5','4/5','1','2','4','8','12','16','24','32')
CHECKS=[]; INPUTS={}; COMMITS={}; ACTIVE={}; CREATED=False

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def clean(v):
    if isinstance(v,np.ndarray):return clean(v.tolist())
    if isinstance(v,np.generic):return clean(v.item())
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    if isinstance(v,float) and not math.isfinite(v):return {'nonfinite':repr(v)}
    return v
def blob(v):return json.dumps(clean(v),sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def need(ok,label):
    if not ok:raise RuntimeError(label)
def exact(label,ok):
    CHECKS.append({'label':label,'passed':bool(ok),'exact':True})
    if not ok:raise ArithmeticError(label)
def close(label,a,b,tol=TOL):
    a,b=np.asarray(a),np.asarray(b); finite=np.isfinite(a).all() and np.isfinite(b).all()
    e=float(np.max(abs(a-b))) if finite else None
    CHECKS.append({'label':label,'passed':bool(finite and e<=tol),'maximum_error':e,'tolerance':tol})
    if not finite or e>tol:raise ArithmeticError(label)
def register(p,want):
    p=Path(p).resolve(); need(sha(p)==want,'input seal '+str(p))
    name=str(p.relative_to(ROOT)); need(name not in INPUTS or INPUTS[name]==want,'conflicting input')
    INPUTS[name]=want
def recheck():
    for p,h in INPUTS.items():need(sha(ROOT/p)==h,'changed input '+p)
def write(p,v):
    with Path(p).open('xb') as f:f.write(blob(v)+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def event(kind,**values):
    with (CP/'journal.jsonl').open('ab') as f:f.write(blob({'event':kind,**values})+b'\n');f.flush();os.fsync(f.fileno())
def commit(name,v):
    h=write(CP/name,v);COMMITS[name]=h;event('row_saved',file=name,sha256=h);return h
def commit_npz(name,values):
    with (CP/name).open('xb') as f:np.savez_compressed(f,**values);f.flush();os.fsync(f.fileno())
    h=sha(CP/name);COMMITS[name]=h;event('probabilities_saved',file=name,sha256=h);return h

def parent(name,stem,count):
    p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'));a=read(J/(name+'_AUDIT.json'))
    need(r['result_raw_sha256']==sha(J/(name+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(blob(p)).hexdigest() and r['report_sha256']==sha(J/(name+'_RESULT.md')),'parent result seals')
    need(p['passed']==r['passed']==len(p['checks'])==count and p['failed']==r['failed']==0 and all(x['passed'] for x in p['checks']),'parent controls')
    need(p['status']==r['status'] and p['input_sha256']==r['input_sha256'],'parent status/inputs')
    need(a['audit_status']=='PASS' and a['failed_assertions']==0 and a['result_raw_sha256']==r['result_raw_sha256'] and a['receipt_sha256']==sha(J/(name+'_RECEIPT.json')) and a['audited_preparations']==104,'parent audit identity')
    keys=('audited_tagged_frames','audited_paired_reference_frames') if name==TAG else ('audited_reset_tagged_frames','audited_reset_reference_frames')
    need(all(a[k]==416 for k in keys),'parent audit full frames')
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cp=J/(stem+'_checkpoints');cm=r['checkpoint_sha256']
    need(len(cm)==1146 and set(cm)=={f.name for f in cp.iterdir() if f.name!='journal.jsonl'},'parent CP census')
    for f,h in cm.items():register(cp/f,h)
    lines=(cp/'journal.jsonl').read_bytes().splitlines();es=[json.loads(x) for x in lines]
    need(len(es)==1149 and hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'],'parent journal prefix')
    m=read(cp/'manifest.json');mh=sha(cp/'manifest.json')
    need(mh==p['manifest_sha256']==es[0]['manifest_sha256'] and m['input_sha256']==es[0]['input_sha256']==r['input_sha256'] and m['PID']==r['original_manifest_PID']==es[0]['PID'],'parent start')
    commits={'manifest.json':mh}
    for e in es[1:-3]:
        need(e['file'] not in commits,'duplicate parent commit');commits[e['file']]=e['sha256']
    need(commits==cm and es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and es[-2]=={'event':'report_saved','sha256':r['report_sha256'],'paired_data_rows':416} and es[-1]=={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))},'parent committed map')
    register(cp/'journal.jsonl',sha(cp/'journal.jsonl'))
    need(len(p['preparations'])==104 and len({x['preparation'] for x in p['preparations']})==104,'104 parent preparations')
    groups={}
    for prep in p['preparations']:
        key=(prep['formation_gamma_rational'],prep['AR_rational']);groups.setdefault(key,[]).append(prep['preparation_time_index'])
        need(prep['preparation_x_rational']==FORMATION_TIMES[prep['preparation_time_index']],'frozen formation age')
    need(set(groups)=={(g,a) for g in ('0','1/10') for a in ('0','1/8','7/40','1/4')} and all(x==list(range(13)) for x in groups.values()),'all8x13 original preparations')
    iid=hashlib.sha256(blob(r['input_sha256'])).hexdigest()
    for prep in p['preparations']:
        need(prep['input_map_sha256']==iid and len(prep['rows'])==4,'parent preparation schema')
        for i,row in enumerate(prep['rows']):
            need(row['preparation']==prep['preparation'] and row['forward_time_index']==i and row['x_rational']==TIMES[i] and row['input_map_sha256']==iid and row['state_sha256']==cm[row['state_file']] and read(cp/row['row_file'])==row and all(x['passed'] for x in row['checks']),'parent full frame schema')
    return p,r,a

def authenticate():
    protocol=J/(NAME+'.md');need(sha(protocol)==PROTOCOL_SHA,'frozen protocol')
    pins=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',protocol.read_text(),re.M)
    need(len(pins)==24,'24 direct pins')
    for p,h in pins:register(J/p,h)
    register(protocol,PROTOCOL_SHA);register(Path(__file__).resolve(),sha(__file__))
    tagged=parent(TAG,TS,14830);reset=parent(RESET,RS,24473)
    rp=read(J/(RES+'_RESULT.json'));rr=read(J/(RES+'_RECEIPT.json'));ra=read(J/(RES+'_AUDIT.json'))
    need(rp['passed']==rr['passed']==len(rp['checks'])==260 and rp['failed']==rr['failed']==0 and all(c['passed'] for c in rp['checks']),'resolvent controls')
    need(ra['audit_status']=='PASS' and ra['failed_assertions']==0 and ra['result_raw_sha256']==rr['result_raw_sha256'] and ra['receipt_sha256']==sha(J/(RES+'_RECEIPT.json')) and ra['audited_binding_rows']==3,'accepted resolvent audit identity')
    need(rr['result_raw_sha256']==sha(J/(RES+'_RESULT.json')) and rr['result_canonical_sha256']==hashlib.sha256(blob(rp)).hexdigest() and rr['input_sha256']==rp['input_sha256'],'resolvent raw/canonical/input map')
    need(rr['report_sha256']==sha(J/(RES+'_RESULT.md')) and rp['status']==rr['status']=='QUALIFIED_ARITHMETIC','resolvent report/status')
    for f,h in ra['input_sha256'].items():register(ROOT/f,h)
    return tagged,reset,rp

def basis():
    with np.load(J/(TS+'_checkpoints/reaction_eigensystems.npz'),allow_pickle=False) as z:
        e=z['tagged_base_eigenvalues'].copy();v=z['tagged_base_eigenvectors'].copy();e1=z['reference_base_eigenvalues'].copy()
        bits=z['global_record_bits'].copy();pairs=z['ordered_tagged_pairs'].copy();meta=json.loads(str(z['metadata_json']))
    with np.load(J/(RS+'_checkpoints/reused_eigensystems.npz'),allow_pickle=False) as z:
        close('reset basis same s0',z['tagged_base_eigenvectors'],v[0],0.);close('reset spectrum same s0',z['tagged_base_eigenvalues'],e[0],0.)
        rest=z['rest_global_words'].copy();end=z['apparatus_endpoint_bits'].copy();rm=json.loads(str(z['metadata_json']))
    need(meta['input_sha256']==read(J/(TAG+'_RECEIPT.json'))['input_sha256'] and rm['input_sha256']==read(J/(RESET+'_RECEIPT.json'))['input_sha256'] and all(c['passed'] for c in meta['checks']+rm['checks']),'basis metadata')
    exact('full global words',np.array_equal(bits,np.array([[(q>>k)&1 for q in range(256)] for k in range(8)])))
    exact('full ordered carrier pairs',np.array_equal(pairs,np.array([(a,b) for a in range(8) for b in range(8) if a!=b])))
    exact('rest endpoints blank',len(rest)==64 and len(set(rest.tolist()))==64 and np.all(bits[[0,4]][:,rest]==0))
    exact('four apparatus labels',set(map(tuple,end.tolist()))=={(0,0),(0,1),(1,0),(1,1)})
    for s in range(3):
        exact('full sorted spectra s%d'%s,np.isfinite(e[s]).all() and np.isfinite(e1[s]).all() and np.all(np.diff(e[s])>=0) and np.all(np.diff(e1[s])>=0))
        close('orthonormal saved basis s%d'%s,v[s].T@v[s],np.eye(112))
    return e,v,e1,bits,rest,end

def spectral_data(e,e1,bindings):
    out=[];masks=[]
    for s in range(3):
        u=.5*s;e0=8+(2+u-math.sqrt((2+u)**2+.16))/2;threshold=2*e1[s,0]-e0
        delta=e[s]-threshold;low=delta < -EPS;middle=abs(delta)<=EPS;high=delta > EPS
        exact('complete threshold partition s%d'%s,np.all(low.astype(int)+middle.astype(int)+high.astype(int)==1))
        close('matched binding s%d'%s,e[s,0]-threshold,bindings[s]['B_s'],1e-9)
        masks.append((low,middle,high));out.append({'s':s,'u_lambda_s':u,'E0_without_common_ARpop':e0,'E1_ground_without_common_ARpop':e1[s,0],
            'matched_threshold_without_common_ARpop':threshold,'mode_energies_without_common_ARpop':e[s],'mode_minus_threshold':delta,
            'definitely_below_indices':np.flatnonzero(low),'unresolved_indices':np.flatnonzero(middle),'definitely_above_indices':np.flatnonzero(high),
            'threshold_tolerance':EPS,'baseline_or_record_loading_binding':bindings[s]})
    return out,masks

def weights(psi,vec,loadings,masks,label):
    nq,nedge,ncarrier,ncol=psi.shape;exact(label+'state shape',nedge==2 and ncarrier==56 and (nq,ncol) in ((256,8),(64,32)))
    coeff=np.einsum('qji,qjk->qik',vec[loadings],psi.reshape(nq,112,ncol),optimize=True)
    mode=np.sum(abs(coeff)**2,axis=2);qprob=np.sum(abs(psi)**2,axis=(1,2,3));close(label+'Parseval',mode.sum(1),qprob)
    norm=float(qprob.sum());close(label+'full mixture norm',norm,1.)
    strata=[]
    for s in range(3):
        ix=loadings==s;spec=mode[ix].sum(0);low,mid,high=masks[s]
        strata.append({'s':s,'sector_probability':qprob[ix].sum(),'mode_probability':spec,'lower_weight':spec[low].sum(),
                       'unresolved_weight':spec[mid].sum(),'upper_weight':spec[low|mid].sum(),'above_weight':spec[high].sum()})
    lower=sum(x['lower_weight'] for x in strata);unresolved=sum(x['unresolved_weight'] for x in strata);above=sum(x['above_weight'] for x in strata)
    close(label+'partition norm',lower+unresolved+above,norm)
    exact(label+'raw weight bounds',all(math.isfinite(x) and x>=0 for x in (lower,unresolved,above)) and lower<=lower+unresolved<=norm+TOL)
    apparatus={}
    if ncol==32:
        joint_modes=np.sum(abs(coeff.reshape(nq,112,4,8))**2,axis=3)
        joint_q=np.sum(abs(psi.reshape(nq,2,56,4,8))**2,axis=(1,2,4))
        close(label+'apparatus Parseval',joint_modes.sum(1),joint_q)
        apparatus={'q_apparatus_mode_probability':joint_modes,'q_apparatus_probability':joint_q}
    return {'lower_weight':lower,'upper_weight':lower+unresolved,'unresolved_weight':unresolved,'above_weight':above,'norm':norm,
            'q_probability':qprob,'q_mode_probability':mode,'strata':strata,'inherited_arithmetic_allowance':TOL,**apparatus},coeff

def saved(cp,row,expected_shape):
    with np.load(cp/row['state_file'],allow_pickle=False) as z:psi=z['psi_tagged'].copy();meta=json.loads(str(z['metadata_json']))
    need(psi.shape==expected_shape and meta['preparation']==row['preparation'] and meta['forward_time_index']==row['forward_time_index'] and meta['x_rational']==row['x_rational'] and meta['input_map_sha256']==row['input_map_sha256'],'saved state metadata')
    return psi

def run_preparation(p,r,v,bits,rest,masks):
    label=p['preparation'];begin=len(CHECKS);tpc=J/(TS+'_checkpoints');rpc=J/(RS+'_checkpoints');rows=[];initial={}
    fields=('case','preparation_time_index','preparation_x_rational','AR_rational','formation_gamma_rational')
    need(all(p[k]==r[k] for k in fields) and r['preparation']==label,'matched preparation identity')
    load=bits[0]+bits[4];rl=np.zeros(64,dtype=int)
    for i,(tr,rr) in enumerate(zip(p['rows'],r['rows'])):
        ACTIVE.update(preparation=label,forward_time_index=i);ap=saved(tpc,tr,(256,2,56,8));ar=saved(rpc,rr,(64,2,56,32))
        wt,ct=weights(ap,v,load,masks,label+'retained%d'%i);wr,cr=weights(ar,v,rl,masks,label+'reset%d'%i)
        if i==0:
            for kind,cp,co,st in (('retained',tpc,ct,tr),('reset',rpc,cr,rr)):
                im=read(cp/(label+'_initial.json'))
                need(im['initial_state_sha256']==st['initial_state_sha256'] and all(c['passed'] for c in im['checks']),'initial metadata custody')
                with np.load(cp/(label+'_initial.npz'),allow_pickle=False) as z:
                    close(label+kind+'saved initial coefficients',co,z['tagged_spectral_coefficients']);close(label+kind+'initial state',ap if kind=='retained' else ar,z['psi_tagged_initial'],0.)
            initial={'retained':wt,'reset':wr}
            marginal_t=np.einsum('qik,qjk->ij',ap.reshape(256,112,8),ap.reshape(256,112,8).conj(),optimize=True)
            marginal_r=np.einsum('qik,qjk->ij',ar.reshape(64,112,32),ar.reshape(64,112,32).conj(),optimize=True)
            close(label+'reset keeps full carrier edge marginal',marginal_t,marginal_r)
        for kind,w in (('retained',wt),('reset',wr)):
            close(label+kind+'invariant mode probabilities',w['q_mode_probability'],initial[kind]['q_mode_probability'])
            close(label+kind+'invariant weight endpoints',[w['lower_weight'],w['upper_weight']],[initial[kind]['lower_weight'],initial[kind]['upper_weight']])
        if p['formation_gamma_rational']=='0':close(label+'blank record loading contrast',[wt['lower_weight'],wt['upper_weight']],[wr['lower_weight'],wr['upper_weight']])
        contrast={'lower_difference':wt['lower_weight']-wr['upper_weight'],'upper_difference':wt['upper_weight']-wr['lower_weight']}
        rows.append({'forward_time_index':i,'x_rational':TIMES[i],'retained_source_present':wt,'reset_source_present':wr,'retained_minus_reset_weight':contrast,
          'retained_source_removed':{'status':'NOT_DEFINED_IN_ONE_CARRIER_SECTOR','existing_controls':tr['paired_reference']},
          'reset_source_removed':{'status':'NOT_DEFINED_IN_ONE_CARRIER_SECTOR','existing_controls':rr['paired_reference_reset']},
          'copy_off_work':tr['copy_off_work'],'insertion_work':tr['insertion_work'],'source_removal_reference_work':tr['source_removal_reference_work'],
          'network_reset_work_tagged':rr['network_reset_work_tagged'],'network_reset_work_reference':rr['network_reset_work_reference'],
          'retained_state_sha256':tr['state_sha256'],'reset_state_sha256':rr['state_sha256'],
          'initial_gamma_zero_is_old_direct_binding_control':p['formation_gamma_rational']=='0'})
        del ap,ar,ct,cr
    bundles={}
    for channel,fields2 in (('retained_source_present',('q_mode_probability',)),('reset_source_present',('q_mode_probability','q_apparatus_mode_probability'))):
        for key in fields2:bundles[channel+'_'+key]=np.stack([row[channel].pop(key) for row in rows])
    return {'preparation':label,**{k:p[k] for k in fields},'rows':rows,'checks':CHECKS[begin:]},bundles

def main():
    global CREATED
    start=time.monotonic();need(sys.argv[1:]==['--execute'],'exact root-only --execute required')
    need(not any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)),'exclusive output absence')
    (tag,_,ta), (reset,_,_),res=authenticate(); e,v,e1,bits,rest,end=basis()
    eta=float(ta['maximum_absolute_residual']);exact('accepted residual budget regular',math.isfinite(eta) and 0<=eta and 112*eta<1)
    def energy_budget(d):return d*eta*math.sqrt(1+d*eta)/(1-d*eta)
    energy_allowance=energy_budget(112)+2*energy_budget(16)+64*np.finfo(float).eps*max(1.,float(np.max(abs(e))))
    exact('fixed threshold dominates inherited energy budget',energy_allowance<EPS)
    need([x['s'] for x in res['binding']]==[0,1,2],'all three binding rows')
    spectra,masks=spectral_data(e,e1,res['binding']);CP.mkdir();CREATED=True
    mh=commit('manifest.json',{'PID':os.getpid(),'input_sha256':INPUTS,'threshold_tolerance':EPS,'preparation_count':104,'forward_times':TIMES});event('started',PID=os.getpid(),manifest_sha256=mh,input_sha256=INPUTS)
    commit('threshold_modes.json',{'spectra':spectra,'inherited_energy_allowance':energy_allowance,'retained_global_words':np.arange(256),'reset_rest_global_words':rest,'reset_apparatus_endpoint_bits':end,
          'interpretation':'FINITE_SAME_GRAPH_MATCHED_ADDITION_THRESHOLD_WITH_UNRESOLVED_MODES'})
    need([x['preparation'] for x in tag['preparations']]==[x['preparation'] for x in reset['preparations']],'ordered all104 parent match')
    rows=[]
    for p,r in zip(tag['preparations'],reset['preparations']):
        out,arrays=run_preparation(p,r,v,bits,rest,masks);fn=p['preparation']+'_probabilities.npz';h=commit_npz(fn,arrays)
        out.update(probabilities_file=fn,probabilities_sha256=h);commit(p['preparation']+'.json',out);rows.append(out)
    exact('all104x4x2 spectral census',len(rows)==104 and sum(len(x['rows']) for x in rows)==416)
    recheck();result={'name':NAME,'PID':os.getpid(),'status':'QUALIFIED_SAVED_SPECTRAL_ARITHMETIC_ONLY','passed':len(CHECKS),'failed':0,'checks':CHECKS,
        'input_sha256':INPUTS,'spectra':spectra,'preparations':rows,'scope':'ACTUAL_PREPARED_FINITE_THRESHOLD_WEIGHT; NO_CAPTURE_CONTINUUM_FORCE_OR_PROPER_CLOCK_CLAIM',
        'elapsed_seconds':time.monotonic()-start}
    raw=write(RESULT,result);event('result_saved',raw_sha256=raw,canonical_sha256=hashlib.sha256(blob(result)).hexdigest())
    lines=['# Actual prepared finite spectral weight V001','','All104 preparations and all4 ages retained. Threshold band1e-9 is unresolved, not clipped. Both removed-source references have no two-carrier projector. Forward invariance is a control, not autonomous capture.','',
      '| Preparation | gamma | AR | formation age | retained weight interval | reset weight interval | signed retained-minus-reset interval |','|---|---|---|---|---|---|---|']
    for row in rows:
        x=row['rows'][0];a=x['retained_source_present'];b=x['reset_source_present'];d=x['retained_minus_reset_weight']
        lines.append('| data %s | %s | %s | %s | [%.12g,%.12g] | [%.12g,%.12g] | [%+.12g,%+.12g] |'%(row['preparation'],row['formation_gamma_rational'],row['AR_rational'],row['preparation_x_rational'],a['lower_weight'],a['upper_weight'],b['lower_weight'],b['upper_weight'],d['lower_difference'],d['upper_difference']))
    need(sum(x.startswith('| data ') for x in lines)==104,'report104 preparation rows')
    lines+=['','Every416 forward row, unresolved mode, paired reference control and owned preparation/switch work remains in JSON. Full q/mode and reset q/apparatus/mode probabilities are in the referenced lossless NPZ bundles; source-present clock records remain in the sealed parent JSON. Blank gamma0 is the existing direct-current baseline, not a zero-bound-weight success gate.','Source and apparatus coherences are retained in the stored parent state; this block-diagonal spectral readout does not erase them. The threshold is not a physically separated continuum or a force criterion.']
    with REPORT.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    event('report_saved',sha256=sha(REPORT),preparation_rows=104);recheck()
    receipt={'status':result['status'],'PID':os.getpid(),'passed':len(CHECKS),'failed':0,'input_sha256':INPUTS,'checkpoint_sha256':COMMITS,
       'result_raw_sha256':raw,'result_canonical_sha256':hashlib.sha256(blob(result)).hexdigest(),'report_sha256':sha(REPORT),
       'journal_prefix_sha256':sha(CP/'journal.jsonl'),'elapsed_seconds':time.monotonic()-start}
    rh=write(RECEIPT,receipt);event('receipt_saved',sha256=rh);print(json.dumps({'passed':len(CHECKS),'failed':0,'raw_sha256':raw,'receipt_sha256':rh}),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as error:
        if not ERROR.exists():
            h=write(ERROR,{'status':'ARITHMETIC_FAILED' if isinstance(error,ArithmeticError) else 'EXECUTION_ERROR_PRESERVED','error_type':type(error).__name__,
                'error':str(error),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'committed_sha256':COMMITS})
            if CREATED:event('error_preserved',sha256=h)
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
