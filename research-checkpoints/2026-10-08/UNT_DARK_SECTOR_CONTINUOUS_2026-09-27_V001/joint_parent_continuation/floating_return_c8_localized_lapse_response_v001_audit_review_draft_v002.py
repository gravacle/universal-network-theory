#!/usr/bin/env python3
"""Independent SAVED-ONLY localized network-lapse audit; root alone executes.
Literal physical q/carrier columns, independent basis projections and direct
inner products audit all 1664 frames / 4160 rows. Integrals use expm1 divided
differences, not the producer's sinc formula or a desired Ward. No eigensolver,
baseline propagation, producer import, preparation or RNG replay. Final result
pins remain prospective until the parent's natural closure.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001';STEM='floating_return_c8_localized_lapse_response_v001';CP=J/(STEM+'_checkpoints')
OUT=J/(NAME+'_AUDIT.json');MD=J/(NAME+'_AUDIT.md');ERROR=J/(NAME+'_AUDIT_ERROR.json')
PINS={STEM+'.py':'4cabbc45b4a7a7655c927e3b57a259de05a23c721c0110431d4e5ca3f09683a8',
      NAME+'.md':'84a212a3da0fe97b1391dde1a8f6dd50db98a958f0e6ae8c676ef78bf2bfe70b',
      NAME+'_RESULT.json':'PENDING_NATURAL_CLOSURE',NAME+'_RECEIPT.json':'PENDING_NATURAL_CLOSURE'}
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple(zip(CYCLE,CYCLE[1:]+CYCLE[:1]));REST=(1,2,3,5,6,7)
TIMES=(0.,.2,2.,8.);TRATS=('0','1/5','2','8');ORDER=tuple((t,s) for t in range(4) for s in range(t+1));KINDS=('Vc','Vm','H')
AGES=('0','1/10','1/5','2/5','4/5','1','2','4','8','12','16','24','32');ARS=('0','1/8','7/40','1/4')
CHANNELS=('retained_on','retained_reference','reset_on','reset_reference');OP=5e-10;OBS=1e-9;EN=5e-9
INPUTS={};CHECKS=[];ACTIVE={};INTEGRAL_BASES={};STARTED=False;BEGIN=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def exact(name,ok):
    CHECKS.append({'name':name,'passed':bool(ok),'scalar_assertions':1})
    if not ok:raise AssertionError(name)
def close(name,a,b,tol=OBS):
    a,b=np.asarray(a),np.asarray(b);finite=bool(np.isfinite(a).all() and np.isfinite(b).all());err=float(np.max(abs(a-b))) if finite else None
    CHECKS.append({'name':name,'passed':finite and err<=tol,'maximum_error':err,'tolerance':tol,'scalar_assertions':int(np.broadcast_arrays(a,b)[0].size)})
    if not finite or err>tol:raise AssertionError(name)
def register(p,h):
    p=Path(p).resolve();key=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    exact('current seal '+key,sha(p)==h);exact('consistent seal '+key,key not in INPUTS or INPUTS[key]==h);INPUTS[key]=h
def write(p,v):
    with Path(p).open('xb') as f:f.write(canon(v)+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def complex_values(v):
    a=np.asarray(v,float);return a[...,0]+1j*a[...,1]
def authenticate():
    for f,h in PINS.items():register(J/f,h)
    p,r=read(J/(NAME+'_RESULT.json')),read(J/(NAME+'_RECEIPT.json'))
    exact('final raw/canonical/result',r['result_raw_sha256']==sha(J/(NAME+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(canon(p)).hexdigest())
    register(J/(NAME+'_RESULT.md'),r['report_sha256']);exact('complete arithmetic result',p['status']==r['status']=='QUALIFIED_ARITHMETIC_PREPARED_NETWORK_ENERGY_SOURCE' and p['failed']==r['failed']==0 and p['passed']==r['passed']==len(p['checks']) and all(c['passed'] for c in p['checks']))
    exact('matching input maps',p['input_sha256']==r['input_sha256'])
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cmap=r['checkpoint_sha256'];exact('7594 unique committed checkpoints',len(cmap)==7594 and set(cmap)=={x.name for x in CP.iterdir() if x.name!='journal.jsonl'})
    for f,h in cmap.items():register(CP/f,h)
    raw=(CP/'journal.jsonl').read_bytes();lines=raw.splitlines();es=[json.loads(x) for x in lines]
    exact('7597 journal events',len(es)==7597);exact('receipt prefix',hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'])
    exact('final result/report/receipt commits',es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and es[-2]=={'event':'report_saved','sha256':r['report_sha256'],'data_rows':4160} and es[-1]=={'event':'receipt_saved','sha256':sha(J/(NAME+'_RECEIPT.json'))})
    m=read(CP/'manifest.json');exact('manifest/start',p['manifest_sha256']==cmap['manifest.json'] and m['PID']==p['PID']==r['PID'] and m['input_sha256']==r['input_sha256'] and es[0]=={'event':'started','PID':p['PID'],'manifest_sha256':p['manifest_sha256'],'input_sha256':r['input_sha256']})
    cm={'manifest.json':p['manifest_sha256']}
    for e in es[1:-3]:exact('unique checkpoint journal commit',e['file'] not in cm);cm[e['file']]=e['sha256']
    exact('complete commit map',cm==cmap);register(CP/'journal.jsonl',sha(CP/'journal.jsonl'))
    exact('fixed source/census/units',p['frame_count']==r['frame_count']==1664 and p['ordered_pair_count']==r['ordered_pair_count']==4160 and p['source_order']==list(KINDS) and len(p['preparations'])==104 and p['physical_units']['native_hbar']==1 and not p['physical_units']['Eunit_selected'] and not p['physical_units']['c_p_selected'])
    exact('report4160 rows',sum(x.startswith('|case') for x in (J/(NAME+'_RESULT.md')).read_text().splitlines())==4160)
    return p,r
def labels(two):return tuple((a,b) for a in range(8) for b in range(8) if a!=b) if two else tuple((v,) for v in range(8))
def model(reset,two,ar):
    words=np.array([sum(((r>>k)&1)<<v for k,v in enumerate(REST)) for r in range(64)]) if reset else np.arange(256)
    bits=np.array([[(int(q)>>v)&1 for q in words] for v in range(8)]);return {'words':words,'bits':bits,'s':bits[0]+bits[4],'pop':bits.sum(0),'ar':ar,'two':two,'labels':labels(two)}
def act(a,m,kind):
    """Direct occupation/allowed-content moves, not producer vertex helpers."""
    pos=m['labels'];lookup={p:i for i,p in enumerate(pos)};bits=m['bits'];nc=len(pos[0]);occ=np.array([[int(v in p) for p in pos] for v in range(8)])
    if kind=='H':
        out=(8+nc+m['ar']*m['pop'])[:,None,None,None]*a;out[:,0]+=(2+.5*m['s'])[:,None,None]*a[:,0];edge_factor=1.;edge_indices=range(8)
    else:
        out=(1+m['ar']*bits[0])[:,None,None,None]*a;out[:,0]+=(1+.5*bits[0])[:,None,None]*a[:,0];out+=occ[0][None,None,:,None]*a;edge_factor=.5;edge_indices=(0,7)
        if kind=='Vm':out+=(bits[0]-bits[5])[:,None,None,None]*a/4;out[:,1]+=(bits[0]-bits[4])[:,None,None]*a[:,1]/4
    for ei in edge_indices:
        u,v=EDGES[ei];cut=np.array([int((u in p)!=(v in p)) for p in pos]);allowed_bits=(1,) if ei==0 else (0,1)
        for n in allowed_bits:
            out[:,n]+=(.25*edge_factor)*cut[None,:,None]*a[:,n]
            for i,p in enumerate(pos):
                for content,site in enumerate(p):
                    target=v if site==u else u if site==v else None
                    if target is None or target in p:continue
                    q=list(p);q[content]=target;out[:,n,lookup[tuple(q)]]-=.1*edge_factor*a[:,n,i]
    return out-(.2 if kind=='H' else .1)*a[:,::-1]
def project(a,vec,m):
    flat=a.reshape(len(m['words']),-1,a.shape[-1]);out=np.empty_like(flat)
    for s in range(3):
        qs=np.flatnonzero(m['s']==s)
        if len(qs):out[qs]=np.einsum('ij,qjc->qic',vec[s].conj().T,flat[qs],optimize=True)
    return out
def expand(c,vec,m):
    out=np.empty_like(c)
    for s in range(3):
        qs=np.flatnonzero(m['s']==s)
        if len(qs):out[qs]=np.einsum('ij,qjc->qic',vec[s],c[qs],optimize=True)
    return out.reshape(len(m['words']),2,len(m['labels']),c.shape[-1])
def beta(a,words):
    lookup={int(q):i for i,q in enumerate(words)};z=[]
    for v in range(8):
        pairs=[(i,lookup[int(q)+(1<<v)]) for i,q in enumerate(words) if not (int(q)>>v)&1 and int(q)+(1<<v) in lookup]
        z.append(2*sum(np.vdot(a[hi],a[lo]) for lo,hi in pairs))
    return np.asarray(z,complex)
def beta_dot(a,b,words):
    lookup={int(q):i for i,q in enumerate(words)};z=[]
    for v in range(8):
        pairs=[(i,lookup[int(q)+(1<<v)]) for i,q in enumerate(words) if not (int(q)>>v)&1 and int(q)+(1<<v) in lookup]
        z.append(2j*sum(np.vdot(b[hi],a[lo])-np.vdot(a[hi],b[lo]) for lo,hi in pairs))
    return np.asarray(z,complex)
def integral_columns(c,ev,vec,m,dt):
    """Full spectral operator integral: expm1/omega, exact zero gaps retained."""
    output={k:np.empty_like(c) for k in KINDS};d=c.shape[1]
    for s in range(3):
        qs=np.flatnonzero(m['s']==s)
        if not len(qs):continue
        cachekey=(m['two'],s)
        if cachekey not in INTEGRAL_BASES:
            sm=model(False,m['two'],0.);sm={**sm,'words':np.array([0]),'bits':np.zeros((8,1),int),'s':np.array([0]),'pop':np.array([0])}
            physical=vec[s].reshape(1,2,len(m['labels']),d);v0=vec[s].conj().T@act(physical,sm,'Vc').reshape(d,d)
            pe=vec[s].conj().T@np.diag(np.r_[np.ones(d//2),np.zeros(d//2)])@vec[s]
            INTEGRAL_BASES[cachekey]=(v0,pe)
        v0,pe=INTEGRAL_BASES[cachekey]
        omega=ev[s][:,None]-ev[s][None,:];f=np.empty_like(omega,complex);zero=omega==0;f[zero]=dt;f[~zero]=np.expm1(1j*omega[~zero]*dt)/(1j*omega[~zero])
        base=np.einsum('ij,qjc->qic',v0*f,c[qs],optimize=True);empty=np.einsum('ij,qjc->qic',pe*f,c[qs],optimize=True)
        q0,q4,q5=m['bits'][[0,4,5]][:,qs];E=ev[s][None,:]+m['ar']*m['pop'][qs,None];phase=np.exp(-1j*E*dt)[:,:,None]
        cap=base+.5*q0[:,None,None]*empty+m['ar']*q0[:,None,None]*dt*c[qs]
        mid=cap+(q0-q4)[:,None,None]*(dt*c[qs]-empty)/4+(q0-q5)[:,None,None]*dt*c[qs]/4
        output['Vc'][qs]=cap*phase;output['Vm'][qs]=mid*phase;output['H'][qs]=dt*E[:,:,None]*c[qs]*phase
    return {k:expand(v,vec,m) for k,v in output.items()}
def main():
    global STARTED
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute; no mutation.')
    if any('PENDING' in h for h in PINS.values()):raise SystemExit('Final natural-closure pins pending; no mutation.')
    if any(p.exists() for p in (OUT,MD,ERROR)):raise SystemExit('Exclusive audit outputs already exist; no mutation.')
    p,r=authenticate();STARTED=True;mapsha=hashlib.sha256(canon(p['input_sha256'])).hexdigest();frames=rows=0
    with np.load(J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz',allow_pickle=False) as z:
        be,bv,re,rv=[z[k].copy() for k in ('tagged_base_eigenvalues','tagged_base_eigenvectors','reference_base_eigenvalues','reference_base_eigenvectors')]
    with np.load(CP/'reused_localized_response_bases.npz',allow_pickle=False) as z:
        for key,a in [('tagged_eigenvalues',be),('tagged_eigenvectors',bv),('reference_eigenvalues',re),('reference_eigenvectors',rv)]:close('literal reused basis '+key,z[key],a,0.)
        bm=json.loads(str(z['metadata_json']));exact('reused basis map/checks',bm['input_map_sha256']==mapsha and bm['new_eigensolver_calls']==0 and all(c['passed'] for c in bm['checks']))
    parents=[read(J/(name+'_RESULT.json')) for name in ('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001')]
    parent_dirs=[J/(s+'_checkpoints') for s in ('floating_return_c8_tagged_probe_reaction_v001','floating_return_c8_endpoint_record_isolation_v001')]
    for pi,prep in enumerate(p['preparations']):
        case,ageindex=divmod(pi,13);name='case%02d_prep%02d'%(case,ageindex);exact('ordered104/four preparation',prep['preparation']==name and [c['channel'] for c in prep['channels']]==list(CHANNELS) and prep['AR_rational']==ARS[case//2] and prep['formation_gamma_rational']==('0','1/10')[case%2] and prep['preparation_x_rational']==AGES[ageindex]);exact('complete summary checkpoint',read(CP/(name+'_complete.json'))==prep);all_values=[];all_clocks=[]
        for ci,ch in enumerate(prep['channels']):
            reset=ci>=2;two=ci%2==0;old=parents[int(reset)]['preparations'][pi];m=model(reset,two,float(prep['AR_rational'].split('/')[0])/float(prep['AR_rational'].split('/')[1]) if '/' in prep['AR_rational'] else float(prep['AR_rational']));ev,vec=(be,bv) if two else (re,rv)
            exact('original preparation identity',all(old[k]==prep[k] for k in ('preparation','AR_rational','formation_gamma_rational','preparation_x_rational')) and len(old['rows'])==4);exact('ordered ten pairs',[(x['target_time_index'],x['source_time_index']) for x in ch['rows']]==list(ORDER));data=[];pk=('tagged_reset' if two else 'paired_reference_reset') if reset else ('tagged' if two else 'paired_reference')
            for si,oldrow in enumerate(old['rows']):
                ACTIVE.update(preparation=name,channel=ch['channel'],source_time_index=si)
                exact('ordered parent frame identity',oldrow['forward_time_index']==si and oldrow['x_rational']==TRATS[si])
                with np.load(parent_dirs[int(reset)]/oldrow['state_file'],allow_pickle=False) as z:a=z['psi_tagged' if two else 'psi_reference'].copy()
                info=read(CP/(name+'_'+ch['channel']+'_source%d.json'%si));bundle=CP/(name+'_'+ch['channel']+'_source%d.npz'%si)
                exact('source identity/order/input/parent',info['preparation']==name and info['channel']==ch['channel'] and info['source_time_index']==si and info['source_x_rational']==TRATS[si] and info['parent_state_sha256']==oldrow['state_sha256'] and info['input_map_sha256']==mapsha and info['bundle_sha256']==r['checkpoint_sha256'][bundle.name] and all(c['passed'] for c in info['checks']))
                direct={k:act(a,m,k) for k in KINDS};c=project(a,vec,m);cs={k:project(v,vec,m) for k,v in direct.items()};E=ev[m['s']]+m['ar']*m['pop'][:,None]
                with np.load(bundle,allow_pickle=False) as z:
                    exact('NPZ metadata matches JSON',json.loads(str(z['metadata_json']))=={k:v for k,v in info.items() if k!='bundle_sha256'});close('q-word map',z['global_record_words'],m['words'],0.);close('absolute NETWORK mode phases',z['absolute_eigenvalues'],E,0.);close('independent saved-state coefficients',z['saved_state_spectral_coefficients'],c,OP)
                    for k in KINDS:close('independent physical source coefficients '+k,z[k+'_source_coefficients'],cs[k],OP)
                close('full H source eigenenergy',cs['H'],E[:,:,None]*c,OP);cl=beta(a,m['words']);close('full joint beta',complex_values(info['joint_clock_beta_global']),cl);close('parent beta',cl,complex_values(oldrow[pk]['Bplus_beta_global']))
                energy={k:float(np.vdot(a,v).real) for k,v in direct.items()};rates={k:2*float(np.vdot(v,direct['H']).imag) for k,v in direct.items()}
                dots={k:beta_dot(a,direct[k],m['words']) for k in KINDS};empty=np.zeros_like(a);empty[:,0]=a[:,0];occupied=np.zeros_like(a);occupied[:,1]=a[:,1];eb=beta(empty,m['words']);ob=beta(occupied,m['words'])
                capdot=np.zeros(8,complex);capdot[0]=1j*(m['ar']*cl[0]+.5*eb[0]);middot=capdot.copy();middot[0]+=.25j*(cl[0]+ob[0]);middot[4]-=.25j*ob[4];middot[5]-=.25j*cl[5]
                close('literal candidate record-raising source',dots['Vc'],capdot);close('literal midpoint record-raising source',dots['Vm'],middot);close('parent complete network clock generator',dots['H'],complex_values(oldrow[pk]['Bplus_dot_global']));close('parent complete network energy',energy['H'],oldrow[pk]['full_energy'],EN)
                for k in KINDS:
                    close('absolute energy/work vertex '+k,info['source_energy_work_vertices'][k],energy[k],EN if k=='H' else OBS);close('source time derivative '+k,info['source_energy_time_derivatives'][k],rates[k],EN);close('joint record source commutator '+k,complex_values(info['joint_clock_generator_derivative_global'][k]),dots[k])
                    # Raw ratios are algebraic candidates, including refused
                    # tiny amplitudes. Check their serialized-input formula;
                    # the independent beta/commutator checks above are absolute
                    # and cannot imply a relative phase-error qualification.
                    stored_beta=complex_values(info['joint_clock_beta_global']);stored_dot=complex_values(info['joint_clock_generator_derivative_global'][k])
                    for v,den in enumerate(abs(stored_beta)**2):
                        tangent=info['joint_clock_phase_rate_tangent_global'][k][v]
                        if den==0:exact('zero amplitude raw ratio undefined',tangent is None)
                        else:close('serialized-input raw phase formula',tangent,float((stored_beta[v].conjugate()*stored_dot[v]).imag/den))
                exact('parent phase eligibility/refusal preserved',info['parent_phase_chart_eligible_global']==[v is not None for v in oldrow[pk]['Bplus_rate_global']] and not info['proper_clock_calibration_adopted'])
                close('zero additive contacts',info['direct_second_additive_N_contacts'],np.zeros((3,3)),0.);close('source allocation work',info['source_class_difference_energy_work'],energy['Vc']-energy['Vm']);close('fractional chart first contacts',[info['fractional_chart_mixed_L_eta_contacts'][k] for k in ('Vc','Vm')],[energy[k] for k in ('Vc','Vm')],OBS)
                if reset:close('conserved reset scalar work',energy['Vc']-energy['Vm'],float(np.sum(m['bits'][5][:,None,None,None]*abs(a)**2))/4)
                if prep['formation_gamma_rational']=='0':close('gamma0 actual source-allocation columns',direct['Vc'],direct['Vm'],OP)
                exact('inherited network work unchanged',info['inherited_network_controller_work']=={k:oldrow[k] for k in ('copy_off_work','insertion_work','source_removal_reference_work','network_reset_work_tagged','network_reset_work_reference') if k in oldrow})
                data.append((a,direct,c,cs,E,energy,rates,info));frames+=1
            computed=[]
            for ti,si in ORDER:
                ACTIVE.update(target_time_index=ti,source_time_index=si);row=ch['rows'][len(computed)];dt=TIMES[ti]-TIMES[si];f,g=data[ti],data[si];phase=np.exp(-1j*g[4]*dt)[:,:,None];prop={k:expand(g[3][k]*phase,vec,m) for k in KINDS};integ=integral_columns(g[2],ev,vec,m,dt);vals={}
                exact('ordered row/metadata/checkpoint',row['target_x_rational']==TRATS[ti] and row['source_x_rational']==TRATS[si] and row['input_map_sha256']==mapsha and row['target_baseline']=={k:v for k,v in f[7].items() if k!='bundle_sha256'} and row['source_baseline']=={k:v for k,v in g[7].items() if k!='bundle_sha256'} and read(CP/(name+'_'+ch['channel']+'_pair%d_%d.json'%(ti,si)))==row and all(c['passed'] for c in row['checks']))
                for aa in KINDS:
                    for b in KINDS:
                        key=aa+'_'+b;vals['chi_'+key]=-2*float(np.vdot(f[1][aa],prop[b]).imag);vals['integrated_chi_'+key]=-2*float(np.vdot(f[1][aa],integ[b]).imag)
                vals['chi_source_difference_source_difference']=-2*float(np.vdot(f[1]['Vc']-f[1]['Vm'],prop['Vc']-prop['Vm']).imag)
                nt=np.zeros_like(f[0]);nt[:,1]=f[0][:,1];ns=np.zeros_like(g[0]);ns[:,1]=g[0][:,1];pn=expand(project(ns,vec,m)*phase,vec,m);weight=(m['bits'][0]-m['bits'][4])**2
                vals['chi_record_correlated_incidence_oracle']=-2*float(np.vdot(weight[:,None,None,None]*nt,pn).imag)/16
                for k in ('Vc','Vm'):vals['inclusive_switched_network_energy_step_work_'+k]=-vals['integrated_chi_H_'+k]+f[5][k];vals['switched_energy_first_readout_contact_'+k]=f[5][k]
                exact('complete value field census',set(vals)==set(row['values']))
                for k,v in vals.items():close('direct saved kernel/integral/work '+k,v,row['values'][k],EN if 'H' in k or 'energy' in k else OBS)
                close('independent correlated delta identity',vals['chi_source_difference_source_difference'],vals['chi_record_correlated_incidence_oracle']);close('uniform causal HH',vals['chi_H_H'],0.,EN)
                if reset or prep['formation_gamma_rational']=='0':
                    for k in ('Vc_Vm','Vm_Vc','Vm_Vm'):close('exact prepared allocation null '+k,vals['chi_'+k],vals['chi_Vc_Vc'])
                    close('exact allocation null left H',vals['chi_H_Vc'],vals['chi_H_Vm'],EN);close('exact allocation null right H',vals['chi_Vc_H'],vals['chi_Vm_H'],EN)
                for k in ('Vc','Vm'):
                    close('uniform left derivative '+k,vals['chi_H_'+k],g[6][k],EN);close('uniform right derivative '+k,vals['chi_'+k+'_H'],-f[6][k],EN);close('energy integral boundary '+k,vals['integrated_chi_H_'+k],f[5][k]-g[5][k],EN);close('inclusive step work '+k,vals['inclusive_switched_network_energy_step_work_'+k],g[5][k],EN)
                close('row contact0',row['zero_direct_second_contacts'],np.zeros((3,3)),0.);computed.append(vals);rows+=1
            all_values.append(computed);all_clocks.append([beta(x[0],m['words'])[list(REST)] for x in data])
        for cl in all_clocks[1:]:close('all six common formed clocks',cl,all_clocks[0],OP)
        for index,contrast in enumerate(prep['signed_four_channel_contrasts']):
            exact('ordered contrast pair',(contrast['target_time_index'],contrast['source_time_index'])==ORDER[index]);z=[v[index] for v in all_values]
            for k in z[0]:
                sr=z[0][k]-z[1][k];sx=z[2][k]-z[3][k];on=z[0][k]-z[2][k];ref=z[1][k]-z[3][k];dd=sr-sx
                for key,value in [('source_presence_retained',sr),('source_presence_transferred',sx),('retained_minus_transferred_on',on),('retained_minus_transferred_reference',ref),('difference_of_differences',dd)]:close('full signed contrast '+key+' '+k,contrast[key][k],value,EN if 'H' in k or 'energy' in k else OBS)
                if prep['formation_gamma_rational']=='0':close('gamma0 record contrast',on,0.,EN if 'H' in k or 'energy' in k else OBS);close('gamma0 reference record contrast',ref,0.,EN if 'H' in k or 'energy' in k else OBS)
        print(json.dumps({'preparation':name,'frames':frames,'rows':rows,'assertions':len(CHECKS)}),flush=True)
    exact('complete1664/4160 audit',frames==1664 and rows==4160)
    for f,h in INPUTS.items():exact('unchanged '+f,sha(ROOT/f)==h)
    scalars=sum(c['scalar_assertions'] for c in CHECKS);maximum=max(c.get('maximum_error',0.) or 0. for c in CHECKS)
    result={'audit_status':'PASS','failed_assertions':0,'assertions':len(CHECKS),'scalar_and_metadata_assertions':scalars,'maximum_absolute_error':maximum,'audited_preparations':104,'audited_source_frames':frames,'audited_channel_time_rows':rows,'result_raw_sha256':r['result_raw_sha256'],'receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'audit_source_sha256':sha(__file__),'input_sha256':INPUTS,'checks':CHECKS,'elapsed_seconds':time.monotonic()-BEGIN,'scope':'Independent saved NETWORK energy-source arithmetic, all raw clock candidates and inherited refusals; no total-instrument stress, metric/clock calibration, new eigen/history/RNG or physical gravity claim.'}
    raw=write(OUT,result)
    with MD.open('x') as f:
        f.write('# Localized network lapse saved audit V001\n\nPASS: all104 preparations,1664 source frames and4160 ordered rows; %d scalar/metadata assertions; maximum residual %.12g.\n\nLiteral physical q/carrier/source columns, independent old-basis projections, direct physical two-time contractions and expm1 exact-gap integrals reproduce all nine signed kernels, correlated record projector, source work/contacts, all joint clocks and four-channel contrasts. Parent phase eligibility/refusals and external-apparatus network-port scope remain. No eigensolver, baseline evolution, producer import, sampler or RNG replay.\n\nAudit JSON SHA256: %s\n'%(scalars,maximum,raw));f.flush();os.fsync(f.fileno())
    print(json.dumps({'audit_status':'PASS','assertions':scalars,'json_sha256':raw,'report_sha256':sha(MD)}),flush=True)
if __name__=='__main__':
    try:main()
    except Exception as error:
        if STARTED and not ERROR.exists():write(ERROR,{'audit_status':'FAILED_ATTEMPT_PRESERVED','error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc(),'active':ACTIVE,'input_sha256':INPUTS,'checks':CHECKS,'audit_source_sha256':sha(__file__)})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
