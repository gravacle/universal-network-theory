#!/usr/bin/env python3
"""Independent saved-operator audit only; root alone executes after review."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_k]='1'
import sys,json,hashlib,math,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_RECORD_INTERACTION_RESOLVENT_V001'
CP=J/'floating_return_c8_record_interaction_resolvent_v001_checkpoints'
OUT=J/(NAME+'_AUDIT.json');MD=J/(NAME+'_AUDIT.md')
REC=J/(NAME+'_AUDIT_RECEIPT.json');ERR=J/(NAME+'_AUDIT_ERROR.json')
PINS={'floating_return_c8_record_interaction_resolvent_v001.py':'75e5cba71872e49f1639b85404d58767c2b7b63224cf5232e1345bd90c428634',
      NAME+'.md':'ebbfb9fb4c206696daf275fe95f49abbda1c26213f697cf04cfd235c5436ae13',
      NAME+'_RESULT.json':'b0da27a402924b51c87acfb71347d92b03ab66db7047e4d6426cb9ea535590f7',
      NAME+'_RECEIPT.json':'c5149436f339ddfde974ae6cddf6fd1263a9f2c762b91f191766091225f4823a'}
CYCLE=(0,4,3,7,2,6,1,5);H=.2;T=.1;JCUR=.25;LAM=.5
CHECKS=[];INPUTS={};ACTIVE={};T0=time.monotonic()

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def read(p):return json.loads(Path(p).read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def exact(name,ok):
    CHECKS.append({'name':name,'passed':bool(ok),'exact':True})
    if not ok:raise AssertionError(name)

def close(name,a,b,tol=5e-10):
    a,b=np.asarray(a),np.asarray(b)
    finite=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
    e=float(np.max(abs(a-b))) if finite else None
    ok=finite and e<=tol
    CHECKS.append({'name':name,'passed':ok,'error':e,'tolerance':tol,'scalar_values':int(np.broadcast_arrays(a,b)[0].size)})
    if not ok:raise AssertionError(name)

def pin(p,want):
    got=sha(p);exact('seal:'+str(p.relative_to(ROOT)),got==want);INPUTS[str(p.relative_to(ROOT))]=got

def recheck():
    for name,want in INPUTS.items():exact('after:'+name,sha(ROOT/name)==want)

def write(p,v):
    with p.open('xb') as f:f.write(json.dumps(v,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)

def arrays(p):
    with np.load(p,allow_pickle=False) as z:return {k:z[k].copy() for k in z.files}

def comm(a,b):return a@b-b@a

def summary(a):
    off=a[~np.eye(len(a),dtype=bool)]
    return {'Frobenius_norm':np.linalg.norm(a,'fro'),'infinity_norm':np.linalg.norm(a,np.inf),
            'diagonal_min':np.diag(a).min(),'diagonal_max':np.diag(a).max(),
            'offdiagonal_min':off.min(),'offdiagonal_max':off.max()}

def entries(name,a,record,labels):
    exact(name+'labels',record['labels']==labels.tolist())
    close(name+'diagonal',record['diagonal'],np.diag(a))
    listed=record['offdiagonal_upper_all'];d=len(a)
    exact(name+'entry_census',len(listed)==d*(d-1)//2)
    pos={v:k for k,v in enumerate(CYCLE)};seen=[]
    for item in listed:
        i,k=item['i'],item['j'];seen.append((i,k));exact(name+'upper',0<=i<k<d)
        close(name+'value',item['value'],a[i,k])
        steps=[min(abs(pos[int(x)]-pos[int(y)]),8-abs(pos[int(x)]-pos[int(y)])) for x,y in zip(labels[i],labels[k])]
        exact(name+'coordinate',item['supplied_cycle_steps_per_tag']==steps)
    exact(name+'unique_entries',seen==[(i,k) for i in range(d) for k in range(i+1,d)])

def main():
    global ACTIVE
    exact('exact_execute',sys.argv[1:]==['--execute'])
    exact('exclusive_outputs',not any(p.exists() for p in (OUT,MD,REC,ERR)))
    for f,h in PINS.items():pin(J/f,h)
    p=read(J/(NAME+'_RESULT.json'));r=read(J/(NAME+'_RECEIPT.json'))
    exact('producer_status',p['status']==r['status']=='QUALIFIED_ARITHMETIC' and p['failed']==r['failed']==0)
    exact('260_completed_controls',p['passed']==r['passed']==len(p['checks'])==260 and all(c['passed'] for c in p['checks']))
    exact('raw_and_canonical',r['result_raw_sha256']==sha(J/(NAME+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(canon(p)).hexdigest())
    pin(J/(NAME+'_RESULT.md'),r['report_sha256']);exact('complete_input_map',p['input_sha256']==r['input_sha256'])
    for f,h in r['input_sha256'].items():pin(ROOT/f,h)
    cmap=r['checkpoint_sha256'];exact('18_CP_census',len(cmap)==18 and set(cmap)=={f.name for f in CP.iterdir() if f.name!='journal.jsonl'})
    for f,h in cmap.items():pin(CP/f,h)
    lines=(CP/'journal.jsonl').read_bytes().splitlines();es=[json.loads(x) for x in lines]
    exact('21_journal_events',len(es)==21)
    exact('journal_prefix',hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'])
    m=read(CP/'manifest.json');exact('start_manifest',es[0]=={'event':'started','PID':p['PID'],'manifest_sha256':p['manifest_sha256'],'input_sha256':r['input_sha256']} and m['PID']==p['PID']==r['PID'] and m['input_sha256']==r['input_sha256'])
    exact('manifest_sha',sha(CP/'manifest.json')==p['manifest_sha256'])
    commits={'manifest.json':p['manifest_sha256']}
    for e in es[1:-3]:
        exact('unique_commit',e['file'] not in commits);commits[e['file']]=e['sha256']
    exact('exact_committed_map',commits==cmap)
    exact('final_commits',es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and es[-2]=={'event':'report_saved','sha256':r['report_sha256'],'resolvent_rows':6,'difference_rows':6,'binding_rows':3} and es[-1]=={'event':'receipt_saved','sha256':sha(J/(NAME+'_RECEIPT.json'))})
    pin(CP/'journal.jsonl',sha(CP/'journal.jsonl'))
    data=arrays(J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz')
    ref=arrays(J/'floating_return_c8_retained_record_geometry_v001_checkpoints/release_eigensystems.npz')
    for key in ('matrices','eigenvalues','eigenvectors'):close('separate_reference_'+key,data['reference_base_'+key],ref['base_'+key])
    exact('6_rows_2_differences_3_binding',len(p['rows'])==6 and len(p['record_differences'])==2 and len(p['binding'])==3)
    exact('unselected_difference_sector_census',[x['sector'] for x in p['record_differences']]==['reference','tagged'])
    exact('unselected_binding_loading_census',[x['s'] for x in p['binding']]==[0,1,2])
    expected=[(a,s) for a in ('reference','tagged') for s in range(3)]
    exact('unselected_row_census',[(x['sector'],x['s']) for x in p['rows']]==expected)
    allops={};grounds={};iid=hashlib.sha256(canon(r['input_sha256'])).hexdigest()
    for row in p['rows']:
        sector,s=row['sector'],row['s'];ACTIVE={'sector':sector,'s':s}
        a=arrays(CP/row['operators_file']);d=row['carrier_dimension'];eye=np.eye(d);zero=np.zeros((d,d));labels=a['labels']
        mat=data[sector+'_base_matrices'][s];ev=data[sector+'_base_eigenvalues'][s];vec=data[sector+'_base_eigenvectors'][s]
        close('saved_matrix',a['saved_matrix'],mat);close('saved_all_modes',mat@vec,vec*ev[None,:]);close('saved_basis',vec.T@vec,np.eye(2*d))
        exact('simple_sorted_ground',np.all(np.isfinite(ev)) and np.all(np.diff(ev)>=0) and ev[1]>ev[0])
        close('saved_global_labels',labels,np.array([(v,) for v in range(8)]) if sector=='reference' else data['ordered_tagged_pairs'])
        he=mat[:d,:d];ho=mat[d:,d:];close('exact_h_blocks',mat[:d,d:],-H*eye);close('other_h_block',mat[d:,:d],-H*eye)
        close('same_loaded_occupied',ho,data[sector+'_base_matrices'][0][d:,d:]);close('loading_shift',he,data[sector+'_base_matrices'][0][:d,:d]+LAM*s*eye)
        z=9.5 if sector=='reference' else 11.;gap=(1.65 if sector=='reference' else 1.)+LAM*s
        close('fixed_z_and_gap',[row['zbar'],row['gap_bound']], [z,gap]);exact('row_input',row['input_map_sha256']==iid)
        # Independent PSD gap witness inferred from the SAVED empty matrix, not a rebuilt native Hamiltonian.
        he0=he-LAM*s*eye;off=he0-np.diag(np.diag(he0));adj=-off/T;deg=adj.sum(1)
        close('unweighted_open_adjacency',adj,np.rint(adj));exact('open_adjacency_nonnegative',np.all(adj>=0));close('open_adjacency_symmetry',adj,adj.T)
        constant=11. if sector=='reference' else 12.;close('empty_Laplacian_decomposition',he0,constant*eye+JCUR*np.diag(deg)-T*adj)
        exact('open_degree_bounds',np.all(deg>=1) and np.all(deg<=(2 if sector=='reference' else 4)))
        exact('analytical_PSD_gap',constant+(JCUR-T)*(1 if sector=='reference' else 0)+LAM*s-z>=gap-1e-12)
        R=a['R'];S=a['Sigma'];Sz=a['Sigma_z'];N=a['norm_metric']
        close('real_R_residual',(z*eye-he)@R,eye);close('R_right_residual',R@(z*eye-he),eye);close('Sigma_identity',S,H*H*R)
        close('energy_derivative',Sz,-H*H*R@R);close('norm_metric',N,eye-Sz)
        for key,target in (('negative_Sigma_factor',-S),('negative_Sigma_z_factor',-Sz),('norm_metric_factor',N)):
            L=a[key];close('positive_factor_'+key,L@L.T,target);exact('positive_factor_diagonal',np.all(np.diag(L)>0))
            exact('positive_factor_upper_triangle_zero',np.all(np.triu(L,1)==0))
        exact('row_factors_available',row['positive_factor_available']==[True,True,True])
        close('operator_ceilings',[row['operator_ceiling'],row['Sigma_z_operator_ceiling']],[H*H/gap,H*H/gap**2])
        exact('Frobenius_ceilings',np.linalg.norm(S,'fro')<=math.sqrt(d)*H*H/gap+5e-10 and np.linalg.norm(Sz,'fro')<=math.sqrt(d)*H*H/gap**2+5e-10)
        for key,value in summary(S).items():close('summary_'+key,row['summary'][key],value)
        entries('row_entries_',S,row['signed_Sigma_entries'],labels)
        M=z*np.eye(2*d)-mat;schur=z*eye-ho-S;close('Schur_saved',a['Schur'],schur)
        close('real_Schur_columns',M@np.vstack((-H*R,eye)),np.vstack((zero,schur)))
        L=np.block([[eye,zero],[H*R,eye]]);D=np.block([[z*eye-he,zero],[zero,schur]]);U=np.block([[eye,H*R],[zero,eye]])
        close('full_LDU',L@D@U,M)
        zc=z+1j*H;Rc=a['complex_R'];Sc=a['complex_Schur'];G=a['complex_G'];Gdirect=a['complex_G_direct']
        close('complex_R_residual',(zc*eye-he)@Rc,eye);close('complex_Schur',Sc,zc*eye-ho-H*H*Rc)
        Goo=G[d:,d:];close('complex_Goo_residual',Sc@Goo,eye)
        oracle=np.block([[Rc+H*H*Rc@Goo@Rc,-H*Rc@Goo],[-H*Goo@Rc,Goo]])
        close('all_four_G_blocks',G,oracle);close('complex_direct',G,Gdirect)
        for gg in (G,Gdirect):close('complex_complete_residual',(zc*np.eye(2*d)-mat)@gg,np.eye(2*d));close('complex_right_residual',gg@(zc*np.eye(2*d)-mat),np.eye(2*d))
        n=np.diag(np.r_[np.zeros(d),np.ones(d)]);Ht=1j*comm(n,mat);Htt=-comm(n,comm(n,mat))
        close('phase_direct_contact',Htt,np.block([[zero,H*eye],[H*eye,zero]]))
        close('first_G_source',a['complex_G_theta'],G@Ht@G);close('first_G_Ward',a['complex_G_theta'],1j*comm(n,G))
        close('second_G_contact',a['complex_G_thetatheta'],G@Htt@G+2*G@Ht@G@Ht@G)
        close('second_G_Ward',a['complex_G_thetatheta'],-comm(n,comm(n,G)))
        close('occupied_phase_first_null',a['complex_G_theta'][d:,d:],zero);close('occupied_phase_second_null',a['complex_G_thetatheta'][d:,d:],zero)
        e0=float(ev[0]);v=a['saved_ground_vector'];close('owned_ground_vector',v,vec[:,0]);close('owned_e0',row['saved_base_ground_energy'],e0,1e-9)
        exact('pole_below_independent_empty_floor',e0<constant+(JCUR-T)*(1 if sector=='reference' else 0)+LAM*s)
        close('ground_residual',mat@v,e0*v);Rp=a['pole_R'];close('pole_inverse_residual',(e0*eye-he)@Rp,eye)
        close('pole_Sigma',a['pole_Sigma'],H*H*Rp);close('pole_energy_derivative',a['pole_Sigma_z'],-H*H*Rp@Rp)
        close('pole_norm_operator',a['pole_norm_metric'],eye-a['pole_Sigma_z']);empty,occupied=v[:d],v[d:]
        close('empty_reconstruction',empty,-H*Rp@occupied);pe=float(np.vdot(empty,empty).real)
        close('empty_norm',pe,np.vdot(occupied,-a['pole_Sigma_z']@occupied),1e-9);close('full_norm',np.vdot(v,v),1.,1e-9)
        close('projected_full_norm',np.vdot(occupied,a['pole_norm_metric']@occupied),1.,1e-9);close('JSON_empty_probability',row['saved_ground_empty_probability'],pe,1e-9)
        jr=read(CP/row['row_file']);jr['row_file']=row['row_file'];exact('saved_row_JSON',jr==row)
        exact('row_operator_hash',row['operators_sha256']==cmap[row['operators_file']]);allops[sector,s]=(a,row);grounds[sector,s]=(e0,pe)
    for diff in p['record_differences']:
        sector=diff['sector'];ACTIVE={'differences':sector};arr=arrays(CP/diff['operators_file']);exact('all_three_loading_pairs',[(x['from_s'],x['to_s']) for x in diff['all_three_record_differences']]==[(0,1),(0,2),(1,2)])
        for entry in diff['all_three_record_differences']:
            i,k=entry['from_s'],entry['to_s'];ai,ri=allops[sector,i];ak,rk=allops[sector,k]
            inc=arr['increment_%d_%d'%(i,k)];factor=arr['increment_factor_%d_%d'%(i,k)]
            close('loading_saved_difference',inc,ak['Sigma']-ai['Sigma']);close('loading_resolvent_identity',inc,LAM*(k-i)*H*H*ak['R']@ai['R'])
            close('loading_factor',factor@factor.T,inc);exact('loading_factor_diagonal',np.all(np.diag(factor)>0) and entry['positive_factor_available'])
            exact('loading_factor_upper_triangle_zero',np.all(np.triu(factor,1)==0))
            bound=LAM*(k-i)*H*H/(rk['gap_bound']*ri['gap_bound']);close('loading_ceiling',entry['operator_ceiling'],bound)
            exact('loading_Frobenius_ceiling',np.linalg.norm(inc,'fro')<=math.sqrt(len(inc))*bound+5e-10)
            for key,value in summary(inc).items():close('loading_summary_'+key,entry['summary'][key],value)
            entries('loading_entries_',inc,entry['signed_entries'],ai['labels'])
        jd=read(CP/diff['row_file']);jd['row_file']=diff['row_file'];exact('saved_difference_JSON',jd==diff)
        exact('difference_operator_hash',diff['operators_sha256']==cmap[diff['operators_file']] and diff['input_map_sha256']==iid)
    calculated=[]
    for row in p['binding']:
        s=row['s'];ACTIVE={'binding':s};u=LAM*s;root=math.sqrt((2+u)**2+4*H*H);e0=8+(2+u-root)/2;pe0=(1-(2+u)/root)/2
        e1,pe1=grounds['reference',s];e2,pe2=grounds['tagged',s];b=e2-2*e1+e0
        want={'s':s,'u_lambda_s':u,'E0_min_without_common_ARpop':e0,'E1_min_without_common_ARpop':e1,'E2_min_without_common_ARpop':e2,'B_s':b,'Delta_B_s':b-(calculated[0]['B_s'] if calculated else b),'empty_probability_0':pe0,'empty_probability_1':pe1,'empty_probability_2':pe2,'loading_slope_dB_du':pe2-2*pe1+pe0}
        exact('binding_schema',set(row)==set(want))
        for key,value in want.items():close('binding_'+key,row[key],value,1e-9)
        close('vacuum_characteristic',(e0-8)*(e0-8-2-u),H*H,1e-9);calculated.append(want)
    exact('binding_CP',read(CP/'all_binding_outcomes.json')['binding']==p['binding'])
    report=(J/(NAME+'_RESULT.md')).read_text();exact('report_6_6_3_rows',sum(x.startswith('|') for x in report.splitlines())==21)
    recheck();count=len(CHECKS);values=sum(c.get('scalar_values',1) for c in CHECKS);maximum=max((c.get('error') or 0.) for c in CHECKS)
    result={'audit_status':'PASS','failed_assertions':0,'assertions':count,'scalar_and_metadata_assertions':values,'maximum_error':maximum,'checks':CHECKS,
            'audit_script_sha256':sha(Path(__file__)),'result_raw_sha256':r['result_raw_sha256'],'receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),
            'input_sha256':INPUTS,'audited_resolvent_rows':6,'audited_loading_differences':6,'audited_binding_rows':3,'elapsed_seconds':time.monotonic()-T0,
            'method':'saved matrices/operators/vectors and JSON only; matrix products and analytical scalar vacuum; no solve/eigh/propagation/native assembly/producer import/RNG',
            'binding':p['binding']}
    raw=write(OUT,result)
    text='# C8 resolvent independent saved-only audit V001\n\nPASS: %d scalar/metadata assertions; maximum residual %.12g.\n\nAll six operators, six loading differences, complete phase contacts, six saved poles and three signed binding outcomes verified without a solve, eigensolver or propagation. Complete source/reference and all input/checkpoint seals retained.\n'%(values,maximum)
    with MD.open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
    receipt={'audit_status':'PASS','audit_raw_sha256':raw,'audit_report_sha256':sha(MD),'audit_script_sha256':sha(Path(__file__)),'producer_result_raw_sha256':r['result_raw_sha256'],'producer_receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'assertions':count,'scalar_and_metadata_assertions':values,'failed_assertions':0,'elapsed_seconds':time.monotonic()-T0}
    rh=write(REC,receipt);print(json.dumps({'audit_status':'PASS','assertions':values,'maximum_error':maximum,'raw_sha256':raw,'receipt_sha256':rh}));return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:
        payload={'audit_status':'FAILED_ATTEMPT_PRESERVED','error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'audit_script_sha256':sha(Path(__file__))}
        if not ERR.exists():write(ERR,payload)
        print(str(e),file=sys.stderr);sys.exit(3)
