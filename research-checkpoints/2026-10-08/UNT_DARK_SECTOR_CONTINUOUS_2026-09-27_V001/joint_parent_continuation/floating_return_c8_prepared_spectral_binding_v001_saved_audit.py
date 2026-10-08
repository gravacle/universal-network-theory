#!/usr/bin/env python3
"""Independent saved-state acceptance audit; root alone executes after review."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,time,traceback
from pathlib import Path
import numpy as np

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_PREPARED_SPECTRAL_BINDING_V001'
STEM='floating_return_c8_prepared_spectral_binding_v001';CP=J/(STEM+'_checkpoints')
TAG='FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001';TS='floating_return_c8_tagged_probe_reaction_v001'
RESET='FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001';RS='floating_return_c8_endpoint_record_isolation_v001'
OUT,MD,RECEIPT,ERROR=[J/(NAME+x) for x in ('_AUDIT.json','_AUDIT.md','_AUDIT_RECEIPT.json','_AUDIT_ERROR.json')]
PINS={STEM+'.py':'bb259fa261e7835b2f5055798114799506cabc5bedb0de1389f3a4da0e69d2ea',
      NAME+'.md':'25ca8b91cc3f30cf46e210036eeb04564a44e7fd570904ce53de0799667d525b',
      NAME+'_RESULT.json':'ca1841c6f9cb9d5ae4ea9049e0a19d2919b610872c3cd39f273af659c2802edb',
      NAME+'_RECEIPT.json':'2ccabf17a7099c3dae6870e451d873af5362b2e1e87a19b2edc5ce3622a659bd'}
TIMES=('0','1/5','2','8');EPS=1e-9;TOL=5e-10
INPUTS={};CHECKS=[];ACTIVE={};START=time.monotonic()

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def blob(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def exact(label,ok):
    CHECKS.append({'label':label,'passed':bool(ok),'scalar_assertions':1})
    if not ok:raise AssertionError(label)
def close(label,a,b,tol=TOL):
    a,b=np.asarray(a),np.asarray(b);finite=bool(np.isfinite(a).all() and np.isfinite(b).all());error=float(np.max(abs(a-b))) if finite else None
    CHECKS.append({'label':label,'passed':finite and error<=tol,'maximum_error':error,'tolerance':tol,'scalar_assertions':int(np.broadcast_arrays(a,b)[0].size)})
    if not finite or error>tol:raise AssertionError(label)
def register(p,want):
    p=Path(p).resolve();exact('seal '+str(p),sha(p)==want);name=str(p.relative_to(ROOT))
    exact('unambiguous seal',name not in INPUTS or INPUTS[name]==want);INPUTS[name]=want
def recheck():
    for n,h in INPUTS.items():exact('unchanged '+n,sha(ROOT/n)==h)
def write(p,v):
    with Path(p).open('xb') as f:f.write(blob(v)+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)

def authenticate():
    for f,h in PINS.items():register(J/f,h)
    p=read(J/(NAME+'_RESULT.json'));r=read(J/(NAME+'_RECEIPT.json'))
    exact('raw/canonical result',r['result_raw_sha256']==sha(J/(NAME+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(blob(p)).hexdigest())
    register(J/(NAME+'_RESULT.md'),r['report_sha256'])
    exact('complete successful controls',p['passed']==r['passed']==len(p['checks']) and p['failed']==r['failed']==0 and all(c['passed'] for c in p['checks']))
    exact('status and input map',p['status']==r['status']=='QUALIFIED_SAVED_SPECTRAL_ARITHMETIC_ONLY' and p['input_sha256']==r['input_sha256'])
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cm=r['checkpoint_sha256'];exact('210 exclusive checkpoint census',len(cm)==210 and set(cm)=={f.name for f in CP.iterdir() if f.name!='journal.jsonl'})
    for f,h in cm.items():register(CP/f,h)
    raw=(CP/'journal.jsonl').read_bytes();lines=raw.splitlines();es=[json.loads(x) for x in lines]
    exact('214 complete events',len(es)==214)
    exact('receipt boundary',hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'] and es[-1]=={'event':'receipt_saved','sha256':sha(J/(NAME+'_RECEIPT.json'))})
    exact('result/report commits',es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and es[-2]=={'event':'report_saved','sha256':r['report_sha256'],'preparation_rows':104})
    commits={}
    for e in es[:-3]:
        if e['event'] in ('row_saved','probabilities_saved'):
            exact('unique checkpoint commit',e['file'] not in commits);commits[e['file']]=e['sha256']
    exact('complete committed map',commits==cm)
    m=read(CP/'manifest.json');starts=[e for e in es if e['event']=='started']
    exact('manifest/start',len(starts)==1 and m['PID']==r['PID']==p['PID']==starts[0]['PID'] and m['input_sha256']==r['input_sha256']==starts[0]['input_sha256'] and starts[0]['manifest_sha256']==cm['manifest.json'])
    exact('manifest fixed census',m['threshold_tolerance']==EPS and m['preparation_count']==104 and m['forward_times']==list(TIMES))
    register(CP/'journal.jsonl',sha(CP/'journal.jsonl'))
    return p,r

def parents():
    out=[]
    for name,stem,count in ((TAG,TS,14830),(RESET,RS,24473)):
        p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'));a=read(J/(name+'_AUDIT.json'))
        exact('sealed parent complete',p['passed']==r['passed']==len(p['checks'])==count and p['failed']==r['failed']==0 and all(c['passed'] for c in p['checks']))
        exact('accepted parent audit',a['audit_status']=='PASS' and a['failed_assertions']==0 and a['audited_preparations']==104 and a['result_raw_sha256']==r['result_raw_sha256'] and a['receipt_sha256']==sha(J/(name+'_RECEIPT.json')))
        exact('parent raw/canonical/report',r['result_raw_sha256']==sha(J/(name+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(blob(p)).hexdigest() and r['report_sha256']==sha(J/(name+'_RESULT.md')))
        cp=J/(stem+'_checkpoints');cm=r['checkpoint_sha256'];lines=(cp/'journal.jsonl').read_bytes().splitlines();events=[json.loads(x) for x in lines]
        exact('parent full checkpoint/event census',len(cm)==1146 and len(events)==1149 and set(cm)=={f.name for f in cp.iterdir() if f.name!='journal.jsonl'})
        exact('parent journal boundary',hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'] and events[-1]=={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))})
        manifest=read(cp/'manifest.json');commits={'manifest.json':sha(cp/'manifest.json')}
        for e in events[1:-3]:exact('unique parent commit',e['file'] not in commits);commits[e['file']]=e['sha256']
        exact('parent complete committed map',commits==cm and manifest['input_sha256']==r['input_sha256']==events[0]['input_sha256'] and manifest['PID']==r['original_manifest_PID']==events[0]['PID'] and commits['manifest.json']==p['manifest_sha256']==events[0]['manifest_sha256'])
        exact('parent final events',events[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and events[-2]=={'event':'report_saved','sha256':r['report_sha256'],'paired_data_rows':416})
        out.append(p)
    return out

def coefficients(psi,v,load):
    # An explicit per-word BLAS transform, distinct from the producer einsum.
    n=psi.shape[0];flat=psi.reshape(n,112,psi.shape[-1]);co=np.empty_like(flat)
    for word in range(n):co[word]=v[int(load[word])].conj().T@flat[word]
    return co
def probabilities(psi,co):
    mode=np.sum(np.square(co.real)+np.square(co.imag),axis=2)
    word=np.sum(np.square(psi.real)+np.square(psi.imag),axis=(1,2,3));close('independent Parseval',mode.sum(1),word)
    close('complete mixture norm',word.sum(),1.)
    joint=None
    if psi.shape[-1]==32:
        joint=np.stack([np.sum(np.square(co[:,:,c*8:(c+1)*8].real)+np.square(co[:,:,c*8:(c+1)*8].imag),axis=2) for c in range(4)],axis=2)
    return mode,word,joint
def check_weights(saved,mode,word,joint,load,masks):
    close('word probability',saved['q_probability'],word);lo=0.;mid=0.;hi=0.
    for s in range(3):
        ix=np.flatnonzero(load==s);aggregate=mode[ix].sum(0);low,uncertain,above=masks[s];st=saved['strata'][s]
        exact('all s strata',st['s']==s);close('stratum modes',st['mode_probability'],aggregate);close('stratum word weight',st['sector_probability'],word[ix].sum())
        values=[float(aggregate[low].sum()),float(aggregate[uncertain].sum()),float(aggregate[above].sum())]
        close('stratum endpoints',[st['lower_weight'],st['unresolved_weight'],st['upper_weight'],st['above_weight']],[values[0],values[1],sum(values[:2]),values[2]])
        lo+=values[0];mid+=values[1];hi+=values[2]
    close('full weight endpoints',[saved['lower_weight'],saved['upper_weight'],saved['unresolved_weight'],saved['above_weight'],saved['norm']],[lo,lo+mid,mid,hi,float(word.sum())])
    exact('raw arithmetic allowance',saved['inherited_arithmetic_allowance']==TOL)
    if joint is not None:
        close('apparatus mode marginal',joint.sum(2),mode);close('saved q apparatus marginal',saved['q_apparatus_probability'],joint.sum(1))
    return lo,lo+mid

def main():
    exact('exact --execute',sys.argv[1:]==['--execute']);exact('exclusive audit paths',not any(p.exists() for p in (OUT,MD,RECEIPT,ERROR)))
    p,r=authenticate();tag,reset=parents();spect=read(CP/'threshold_modes.json')
    bindings=read(J/'FLOATING_RETURN_C8_RECORD_INTERACTION_RESOLVENT_V001_RESULT.json')['binding']
    exact('duplicate spectra summary custody',p['spectra']==spect['spectra'])
    exact('all three accepted bindings',[x['s'] for x in bindings]==[0,1,2])
    with np.load(J/(TS+'_checkpoints/reaction_eigensystems.npz'),allow_pickle=False) as z:
        ev=z['tagged_base_eigenvalues'].copy();vec=z['tagged_base_eigenvectors'].copy();e1=z['reference_base_eigenvalues'].copy()
    bits=np.array([[(q>>v)&1 for q in range(256)] for v in range(8)]);load=bits[0]+bits[4]
    with np.load(J/(RS+'_checkpoints/reused_eigensystems.npz'),allow_pickle=False) as z:rest=z['rest_global_words'].copy();end=z['apparatus_endpoint_bits'].copy()
    exact('all basis dimensions',ev.shape==(3,112) and vec.shape==(3,112,112) and e1.shape==(3,16))
    exact('stored global maps',spect['retained_global_words']==list(range(256)) and spect['reset_rest_global_words']==rest.tolist() and spect['reset_apparatus_endpoint_bits']==end.tolist())
    eta=read(J/(TAG+'_AUDIT.json'))['maximum_absolute_residual'];allowance=lambda d:d*eta*math.sqrt(1+d*eta)/(1-d*eta)
    budget=allowance(112)+2*allowance(16)+64*np.finfo(float).eps*max(1.,float(np.max(abs(ev))))
    close('inherited conservative energy budget',spect['inherited_energy_allowance'],budget);exact('budget below fixed ambiguity',budget<EPS)
    masks=[]
    for s in range(3):
        u=s/2;d=2+u;e0=8+(d-math.sqrt(d*d+4/25))/2;threshold=2*e1[s,0]-e0;delta=ev[s]-threshold
        close('analytic vacuum characteristic',(e0-8)*(e0-8-d),1/25)
        below=np.array([x < -EPS for x in delta]);uncertain=np.array([-EPS<=x<=EPS for x in delta]);above=~(below|uncertain)
        masks.append((below,uncertain,above));row=spect['spectra'][s]
        exact('duplicate accepted binding custody',row['baseline_or_record_loading_binding']==bindings[s])
        close('independent matched ground binding',delta[0],bindings[s]['B_s'],1e-9)
        exact('unselected loading',row['s']==s and row['u_lambda_s']==u and row['threshold_tolerance']==EPS)
        close('threshold values',[row['E0_without_common_ARpop'],row['E1_ground_without_common_ARpop'],row['matched_threshold_without_common_ARpop']],[e0,e1[s,0],threshold])
        close('all signed modes',row['mode_minus_threshold'],delta);close('all mode energies',row['mode_energies_without_common_ARpop'],ev[s])
        for key,mask in (('definitely_below_indices',below),('unresolved_indices',uncertain),('definitely_above_indices',above)):exact('complete untrimmed indices',row[key]==np.flatnonzero(mask).tolist())
    exact('all104 ordered preparations',[x['preparation'] for x in p['preparations']]==[x['preparation'] for x in tag['preparations']]==[x['preparation'] for x in reset['preparations']] and len(p['preparations'])==104)
    summaries=[]
    for result,t,rr in zip(p['preparations'],tag['preparations'],reset['preparations']):
        label=result['preparation'];ACTIVE.update(preparation=label);exact('full preparation CP',read(CP/(label+'.json'))==result)
        exact('probability bundle seal',result['probabilities_sha256']==r['checkpoint_sha256'][result['probabilities_file']])
        for key in ('case','preparation_time_index','preparation_x_rational','AR_rational','formation_gamma_rational'):exact('matched preparation '+key,result[key]==t[key]==rr[key])
        with np.load(CP/result['probabilities_file'],allow_pickle=False) as z:bundles={k:z[k].copy() for k in z.files}
        initial={};last=[]
        for i,row in enumerate(result['rows']):
            ACTIVE.update(forward_time_index=i);tr=t['rows'][i];zr=rr['rows'][i];exact('four fixed forward ages',row['forward_time_index']==i and row['x_rational']==TIMES[i])
            exact('parent state seal identities',row['retained_state_sha256']==tr['state_sha256'] and row['reset_state_sha256']==zr['state_sha256'])
            current={}
            for channel,stem,old,loads in (('retained_source_present',TS,tr,load),('reset_source_present',RS,zr,np.zeros(64,dtype=int))):
                with np.load(J/(stem+'_checkpoints')/old['state_file'],allow_pickle=False) as z:psi=z['psi_tagged'].copy()
                exact('full saved shape',psi.shape==((256,2,56,8) if stem==TS else (64,2,56,32)))
                co=coefficients(psi,vec,loads);mode,word,joint=probabilities(psi,co);close('saved full mode probabilities',mode,bundles[channel+'_q_mode_probability'][i])
                if joint is not None:close('saved full apparatus modes',joint,bundles[channel+'_q_apparatus_mode_probability'][i])
                current[channel]=check_weights(row[channel],mode,word,joint,loads,masks)
                if i==0:
                    initial[channel]=(mode.copy(),current[channel],psi.copy())
                    with np.load(J/(stem+'_checkpoints')/(label+'_initial.npz'),allow_pickle=False) as z:close('independent initial spectral coefficients',co,z['tagged_spectral_coefficients']);close('exact initial states',psi,z['psi_tagged_initial'],0.)
                close('all age invariant mode weights',mode,initial[channel][0]);close('all age invariant threshold endpoints',current[channel],initial[channel][1])
                del psi,co
            wt,wr=current['retained_source_present'],current['reset_source_present'];difference=(wt[0]-wr[1],wt[1]-wr[0])
            close('raw signed loading envelope',[row['retained_minus_reset_weight']['lower_difference'],row['retained_minus_reset_weight']['upper_difference']],difference)
            if t['formation_gamma_rational']=='0':close('blank gamma0 baseline equality',wt,wr)
            exact('references not manufactured',row['retained_source_removed']=={'status':'NOT_DEFINED_IN_ONE_CARRIER_SECTOR','existing_controls':tr['paired_reference']} and row['reset_source_removed']=={'status':'NOT_DEFINED_IN_ONE_CARRIER_SECTOR','existing_controls':zr['paired_reference_reset']})
            for key in ('copy_off_work','insertion_work','source_removal_reference_work'):close('retained complete work '+key,row[key],tr[key])
            for key in ('network_reset_work_tagged','network_reset_work_reference'):close('reset complete work '+key,row[key],zr[key])
            last.append({'age':TIMES[i],'retained':wt,'reset':wr,'signed_loading_envelope':difference})
        a=initial['retained_source_present'][2];b=initial['reset_source_present'][2];aa=a.reshape(256,112,8);bb=b.reshape(64,112,32)
        ma=sum((x@x.conj().T for x in aa),np.zeros((112,112),complex));mb=sum((x@x.conj().T for x in bb),np.zeros((112,112),complex));close('exact initial full marginal kept',ma,mb)
        for c,(qa,qb) in enumerate(end):close('exact endpoint apparatus transfer',b[:,:,:,8*c:8*(c+1)],a[rest+int(qa)+(int(qb)<<4)],0.)
        summaries.append({'preparation':label,'formation_gamma_rational':t['formation_gamma_rational'],'AR_rational':t['AR_rational'],'formation_age':t['preparation_x_rational'],'rows':last})
    exact('all104x4x2 weights',len(summaries)==104 and sum(len(x['rows']) for x in summaries)==416)
    report=(J/(NAME+'_RESULT.md')).read_text();exact('104 report rows',sum(x.startswith('| data ') for x in report.splitlines())==104)
    recheck();values=sum(c['scalar_assertions'] for c in CHECKS);maximum=max(c.get('maximum_error',0.) or 0. for c in CHECKS)
    result={'audit_status':'PASS','assertions':len(CHECKS),'scalar_and_metadata_assertions':values,'failed_assertions':0,'maximum_absolute_error':maximum,
        'audited_preparations':104,'audited_forward_rows':416,'audited_source_present_spectral_weights':832,'input_sha256':INPUTS,
        'producer_result_raw_sha256':r['result_raw_sha256'],'producer_receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'checks':CHECKS,'summaries':summaries,
        'audit_source_sha256':sha(__file__),'method':'saved full states; explicit per-word V-dagger multiplication, real/imag squared probabilities; no H assembly/action, eigensolver, propagation, producer import or RNG',
        'elapsed_seconds':time.monotonic()-START}
    raw=write(OUT,result)
    with MD.open('x') as f:f.write('# Prepared spectral saved-only audit V001\n\nPASS: %d scalar/metadata assertions, all104x4x2 weights and full q/apparatus marginals; maximum residual %.12g.\n\nFinite same-graph numerical threshold only. References remain undefined; conserved weight is not autonomous capture or a physical force. All raw loading signs and old blank baselines retained.\n'%(values,maximum));f.flush();os.fsync(f.fileno())
    receipt={'audit_status':'PASS','audit_raw_sha256':raw,'audit_report_sha256':sha(MD),'audit_source_sha256':sha(__file__),'input_sha256':INPUTS,'assertions':len(CHECKS),'scalar_and_metadata_assertions':values,'failed_assertions':0,'elapsed_seconds':time.monotonic()-START}
    rh=write(RECEIPT,receipt);print(json.dumps({'audit_status':'PASS','assertions':values,'raw_sha256':raw,'receipt_sha256':rh}),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as error:
        if not ERROR.exists():write(ERROR,{'audit_status':'FAILED_ATTEMPT_PRESERVED','error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'audit_source_sha256':sha(__file__)})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
