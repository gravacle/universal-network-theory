#!/usr/bin/env python3
"""Saved failed-holding diagnostic: unchanged data, no eigensolver/evolution.

Original ARITHMETIC_FAILED is preserved. Exact-binary Decimal subtraction is
only an arithmetic diagnostic, not a response certificate. Spectrum/force
uncertainty bounds below are mathematically valid in exact arithmetic; their
binary64 evaluations are explicitly nondirected estimates. All three failed
AB Hessians stay unqualified. All nine identical-well cells additionally get
a NEW exchange-even projection, with no automatic ground qualification.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,time,traceback
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_FIXED_CHART_TWO_BODY_HOLDING_V001'
STEM='floating_return_c8_fixed_chart_two_body_holding_v001';CP=J/(STEM+'_checkpoints')
OUT,MD,RECEIPT,ERROR=[J/(NAME+x) for x in ('_SAVED_DIAGNOSTIC.json','_SAVED_DIAGNOSTIC.md','_SAVED_DIAGNOSTIC_RECEIPT.json','_SAVED_DIAGNOSTIC_ERROR.json')]
PINS={STEM+'.py':'52b0dfb906fa0e3f5d9934d31dc0dbfd740ce50dfc646ff6faabecc6cc1d51fa',
      NAME+'.md':'ab51f8a60d78840a1fd788dfc7317e0b8072277ef1698d8dfafeb9da8d80a6a0',
      'LOCAL_RECORD_FEEDBACK_FIXED_CHART_TWO_BODY_HOLDING_SOURCE_V001.md':'deb197eb8de380498162b90def7632691e834d8e411f3a3e5435a8cdb803f813',
      NAME+'_RESULT.json':'3e9d18da149260abf35ed508bbe8975aff446160a7def4f8d5a1db626ab42232',
      NAME+'_RECEIPT.json':'c0631259124fca49ae4f60487cd992cabe8fd9d1d37e09c56a55040a3753a531'}
CYCLE=(0,4,3,7,2,6,1,5);PAIRS=tuple((a,b) for a in range(8) for b in range(8) if a!=b)
KS=(.1,.5,2.);ARS=(0.,.125,.175,.25);TOL=5e-10;OBS=1e-9
INPUTS={};CHECKS=[];ACTIVE={};START=time.monotonic()
FAILED_NAMES=['k2_m00_AB_s%d_contact_response_identity'%s for s in range(3)]
RESPONSE_DIAGNOSTICS=[];PROJECTIONS=[]

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
def close(label,a,b,tol=OBS):
    a,b=np.asarray(a),np.asarray(b);finite=bool(np.isfinite(a).all() and np.isfinite(b).all())
    err=float(np.max(abs(a-b))) if finite else None
    CHECKS.append({'label':label,'passed':finite and err<=tol,'maximum_error':err,'tolerance':tol,
                   'scalar_assertions':int(np.broadcast_arrays(a,b)[0].size)})
    if not finite or err>tol:raise AssertionError(label)
def register(p,h):
    p=Path(p).resolve();exact('seal '+str(p),sha(p)==h);k=str(p.relative_to(ROOT))
    exact('unique consistent seal',k not in INPUTS or INPUTS[k]==h);INPUTS[k]=h
def write(p,v):
    with Path(p).open('xb') as f:f.write(blob(v)+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)

def authenticate():
    for f,h in PINS.items():register(J/f,h)
    p,r=read(J/(NAME+'_RESULT.json')),read(J/(NAME+'_RECEIPT.json'))
    exact('raw/canonical result',r['result_raw_sha256']==sha(J/(NAME+'_RESULT.json')) and
          r['result_canonical_sha256']==hashlib.sha256(blob(p)).hexdigest())
    register(J/(NAME+'_RESULT.md'),r['report_sha256'])
    failed=[x for x in p['checks'] if not x['passed']]
    exact('complete FAILED producer preserved',p['status']==r['status']=='ARITHMETIC_FAILED' and
          p['passed']==r['passed']==9147 and p['failed']==r['failed']==3 and len(p['checks'])==9150 and
          [x['name'] for x in failed]==FAILED_NAMES and all(x['tolerance']==OBS and x['error']>OBS for x in failed))
    exact('matching input maps',p['input_sha256']==r['input_sha256'])
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cm=r['checkpoint_sha256'];exact('97 complete checkpoints',len(cm)==97 and set(cm)=={x.name for x in CP.iterdir() if x.name!='journal.jsonl'})
    for f,h in cm.items():register(CP/f,h)
    lines=(CP/'journal.jsonl').read_bytes().splitlines();es=[json.loads(x) for x in lines]
    exact('100 complete journal events',len(es)==100)
    exact('journal receipt boundary',hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'] and
          es[-1]=={'event':'receipt_saved','sha256':sha(J/(NAME+'_RECEIPT.json'))})
    exact('result/report commits',es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} and
          es[-2]=={'event':'report_saved','sha256':r['report_sha256'],'data_rows':144,'reference_rows':144})
    m=read(CP/'manifest.json');exact('manifest/start',es[0]=={'event':'started','PID':p['PID'],'manifest_sha256':p['manifest_sha256'],'input_sha256':r['input_sha256']} and
          m['PID']==p['PID']==r['PID'] and m['input_sha256']==r['input_sha256'] and cm['manifest.json']==p['manifest_sha256'])
    commits={'manifest.json':p['manifest_sha256']}
    for e in es[1:-3]:
        exact('unique valid checkpoint event',e['event'] in ('row_saved','operators_saved') and e['file'] not in commits);commits[e['file']]=e['sha256']
    exact('complete checkpoint commit map',commits==cm);register(CP/'journal.jsonl',sha(CP/'journal.jsonl'))
    exact('manifest full fixed census',m['group_count']==48 and m['row_count']==144 and m['parameters']['B_center_pi_eighths']==list(range(16)) and
          m['parameters']['s']==[0,1,2] and m['parameters']['global_cycle']==list(CYCLE) and
          m['parameters']['kappa_rational']==['1/10','1/2','2'] and m['parameters']['AR_rational']==['0','1/8','7/40','1/4'] and
          m['parameters']['radius']==1 and m['parameters']['A_center']==0 and m['parameters']['spectral_gap_floor']==OBS)
    return p,r

def literal_sources(labels,theta,kappa,phis):
    well=np.array([sum(kappa*(1-math.cos(theta[v]-phis[l])) for l,v in enumerate(pos)) for pos in labels])
    first=np.array([[-kappa*math.sin(theta[pos[l]]-phis[l]) for pos in labels] for l in range(len(phis))])
    second=np.array([[kappa*math.cos(theta[pos[l]]-phis[l]) for pos in labels] for l in range(len(phis))])
    return np.tile(well,2),np.tile(first,(1,2)),np.tile(second,(1,2))

def location(g,labels,theta,phis,kappa,saved):
    n=len(labels);weights=np.array([abs(g[i])**2+abs(g[n+i])**2 for i in range(n)])
    close('complete ground probability',weights.sum(),1.);marg=np.zeros((len(phis),8));joint=np.zeros((8,8))
    for w,pos in zip(weights,labels):
        for l,v in enumerate(pos):marg[l,v]+=w
        if len(phis)==2:joint[pos]+=w
    for l,phi in enumerate(phis):
        old=saved['site_readouts'][l];z=sum(marg[l,v]*complex(math.cos(theta[v]),math.sin(theta[v])) for v in range(8))
        mu=sum(marg[l,v]*(1-math.cos(theta[v]-phi)) for v in range(8))
        close('full site marginal',marg[l],old['site_probability']);close('circular moment',[z.real,z.imag],old['circular_first_moment'])
        close('circular concentration',abs(z),old['circular_concentration']);close('well misalignment',mu,old['well_misalignment'])
        close('well energy',kappa*mu,old['well_energy']);close('mean chord position',[z.real,z.imag],old['mean_chord_position'])
        exact('mean angle refusal', (old['circular_mean_angle'] is None)==(abs(z)<=OBS))
        if abs(z)>OBS:close('raw mean angle',math.atan2(z.imag,z.real),old['circular_mean_angle'])
    if len(phis)==2:
        old=saved['pair_readout'];dist=np.zeros(4);ci={v:i for i,v in enumerate(CYCLE)}
        for w,(a,b) in zip(weights,labels):
            d=abs(ci[a]-ci[b]);dist[min(d,8-d)-1]+=w
        close('full ordered pair probability',joint,old['ordered_pair_probability']);close('same-site exclusion',np.diag(joint),np.zeros(8),0.)
        close('cycle distance distribution',dist,old['cycle_step_probability'])
        close('mean proper arc',sum(dist[d-1]*d*math.pi/4 for d in range(1,5)),old['mean_shortest_arc_distance'])
        close('mean chord distance',sum(dist[d-1]*2*math.sin(d*math.pi/8) for d in range(1,5)),old['mean_chord_distance'])
        close('adjacent probability',dist[0],old['adjacent_probability']);close('anchor probability',joint[0,4]+joint[4,0],old['anchor_pair_probability'])
    return weights

def inventory(g,labels,u,well,saved,H):
    n=len(labels);x=g.reshape(2,n);prob=abs(x)**2;empty=float(prob[0].sum());cuts=np.zeros((2,n))
    edges=[(CYCLE[i],CYCLE[(i+1)%8]) for i in range(8)]
    for e in range(2):
        for k,pos in enumerate(labels):
            for a,b in edges:
                if e==0 and {a,b}=={0,4}:continue
                cuts[e,k]+=int((a in pos)!=(b in pos))
    hop=0.
    for e in range(2):
        block=H[e*n:(e+1)*n,e*n:(e+1)*n].copy();np.fill_diagonal(block,0.)
        hop+=float(np.real(np.vdot(x[e],block@x[e])))
    vals={'field_self':8.,'carrier_storage':float(len(labels[0])),'degree_defect':2*empty,'native_record_feedback':u*empty,
          'current_square':.25*float(np.sum(prob*cuts)),'occupied_hopping':hop,'incidence_flip':-.4*float(np.real(np.vdot(x[0],x[1]))),
          'holding_wells':float(prob.reshape(-1)@well),'record_charging_ARpop':0.}
    for k,v in vals.items():close('complete inventory '+k,v,saved[k])
    return sum(vals.values())

def spectrum_uncertainty(h,e,v):
    # Polar U=V(V*V)^(-1/2) is used ONLY in the proof, not constructed here.
    # ||U-V|| <= sqrt(1+eta)*eta/[sqrt(1-eta)*(1+sqrt(1-eta))].
    eta=float(np.linalg.norm(v.conj().T@v-np.eye(len(e)),ord='fro'))
    r=float(np.linalg.norm(h@v-v*e[None,:],ord='fro'))
    hnorm=float(np.max(np.sum(abs(h),axis=1)));emax=float(np.max(abs(e)))
    if eta>=1:delta=None;d=None
    else:
        q=math.sqrt(1-eta);d=math.sqrt(1+eta)*eta/(q*(1+q))
        delta=r+(hnorm+emax)*d
    return {'mode_orthogonality_Frobenius':eta,'mode_residual_Frobenius':r,
            'H_row_norm_upper':hnorm,'saved_maximum_absolute_eigenvalue':emax,
            'polar_distance_bound_estimate':d,'ordered_spectrum_error_bound_estimate':delta,
            'true_gap_lower_bound_estimate':None if delta is None else float(e[1]-e[0]-2*delta),
            'qualification':'NONDIRECTED_FLOAT_EVALUATION_OF_EXACT_ARITHMETIC_BOUND'}

def state_uncertainty(h,e,g,cert,vertices,contacts):
    ng=float(np.linalg.norm(g));x=g/ng;ray=float(np.real(np.vdot(x,h@x)))
    residual=float(np.linalg.norm(h@x-ray*x));delta=cert['ordered_spectrum_error_bound_estimate']
    distance=None if delta is None else float(e[1]-delta-ray)
    angle=None if distance is None or distance<=0 else min(1.,residual/distance)
    first=np.max(abs(vertices),axis=1);second=np.max(abs(contacts),axis=1);norm_defect=abs(ng*ng-1.)
    return {'state_norm':ng,'Rayleigh_energy':ray,'ground_residual_norm':residual,
            'excited_distance_lower_bound_estimate':distance,'ground_sine_angle_upper_estimate':angle,
            'raw_stored_state_norm_square_defect':norm_defect,
            'source_gradient_error_upper_estimates':None if angle is None else ((2*angle+norm_defect)*first).tolist(),
            'source_contact_error_upper_estimates':None if angle is None else ((2*angle+norm_defect)*second).tolist(),
            'bounded_probability_error_upper_estimate':None if angle is None else 2*angle+norm_defect,
            'qualification':'NONDIRECTED_FORCE_AND_CONTACT_UNCERTAINTY_ESTIMATE_NOT_NEW_CERTIFIED_INTERVAL'}

def binary_contact_diagnostic(direct,susceptibility,old_hessian):
    # Inputs are precisely the sealed binary64 values. Decimal cannot improve
    # their spectral accuracy and never changes the old Hessian/status.
    with localcontext() as ctx:
        ctx.prec=70
        d=np.asarray(direct);s=np.asarray(susceptibility);old=np.asarray(old_hessian)
        new=[];old_loss=[];new_loss=[]
        for a in range(len(d)):
            nr=[];orr=[];nrr=[]
            for b in range(len(d)):
                dd=Decimal.from_float(float(d[a,b]));ss=Decimal.from_float(float(s[a,b]))
                exact_binary_difference=dd-ss
                nr.append(str(exact_binary_difference))
                orr.append(str(Decimal.from_float(float(old[a,b]))+ss-dd))
                nrr.append(str(exact_binary_difference+ss-dd))
            new.append(nr);old_loss.append(orr);new_loss.append(nrr)
    return {'NEW_exact_binary_contact_minus_susceptibility_decimal':new,
            'sealed_rounded_Hessian_closure_loss_decimal':old_loss,
            'NEW_decimal_expression_closure_loss':new_loss,
            'qualification':'ARITHMETIC_EXPRESSION_ONLY_NOT_PHYSICAL_HESSIAN_ACCURACY'}

def exchange_projection(h,e,v,g,vertices,contacts,cert,group,s,u):
    index={p:i for i,p in enumerate(PAIRS)};half=len(PAIRS)
    perm=np.array([index[(b,a)] for a,b in PAIRS]+[half+index[(b,a)] for a,b in PAIRS])
    close('coincident full exchange symmetry',h[np.ix_(perm,perm)],h,TOL)
    close('exchange swaps the two source vertices',vertices[0,perm],vertices[1],TOL)
    close('exchange swaps the direct contacts',contacts[0,perm],contacts[1],TOL)
    plus=(g+g[perm])/2;plus_norm=float(np.linalg.norm(plus));exact('nonzero exchange-even projection',plus_norm>0)
    even=plus/plus_norm;close('NEW projected exact evenness',even,even[perm],TOL)
    grad=np.real(vertices@abs(even)**2);contact=np.diag(contacts@abs(even)**2)
    old_grad=np.real(vertices@abs(g)**2);old_contact=np.diag(contacts@abs(g)**2)
    close('NEW even source-gradient equality',grad[0],grad[1],OBS)
    close('NEW even contact equality',contact[0,0],contact[1,1],OBS)
    original=state_uncertainty(h,e,g,cert,vertices,contacts)
    projected=state_uncertainty(h,e,even,cert,vertices,contacts)
    bound=original['source_gradient_error_upper_estimates']
    discrepancy=float(old_grad[0]-old_grad[1])
    return {'group':group,'s':s,'NEW_projection':'P_plus=(I+species_exchange)/2; normalized; no eigensolver',
            'PF_argument':'Identical wells and labelblind native action commute with exchange; unique positive exact ground is even.',
            'projected_plus_norm':plus_norm,'saved_odd_component_norm':float(np.linalg.norm((g-g[perm])/2)),
            'saved_gradient':old_grad.tolist(),'saved_exchange_gradient_difference':discrepancy,
            'exchange_force_error_sum_estimate':None if bound is None else sum(bound),
            'saved_discrepancy_consistent_with_estimate':None if bound is None else abs(discrepancy)<=sum(bound)+OBS,
            'NEW_Rayleigh_energy':projected['Rayleigh_energy'],
            'NEW_minus_saved_energy':projected['Rayleigh_energy']-float(e[0]),
            'NEW_gradient':grad.tolist(),'NEW_gradient_minus_saved':(grad-old_grad).tolist(),
            'NEW_contact':contact.tolist(),'NEW_contact_minus_saved':(contact-old_contact).tolist(),
            'NEW_torque_absolute_AB':(-grad).tolist(),'NEW_exchange_evenness_residual':float(np.linalg.norm(even-even[perm])),
            'saved_state_uncertainty':original,'NEW_projected_state_uncertainty':projected,
            'spectrum_uncertainty':cert,'qualification':'NEW_SYMMETRY_PROJECTION_ONLY_NO_AUTOMATIC_GROUND_OR_HESSIAN_CERTIFICATION'}

def sector(arr,prefix,labels,theta,kappa,phis,u,saved,base):
    h=arr[prefix+'matrix'];e=arr[prefix+'eigenvalues'];v=arr[prefix+'eigenvectors'];g=arr[prefix+'ground'];d=len(g)
    exact('complete finite sector shapes',h.shape==(d,d) and v.shape==(d,d) and e.shape==(d,) and d==2*len(labels))
    exact('ordered real finite saved spectrum',np.isrealobj(e) and bool(np.isfinite(e).all() and np.all(np.diff(e)>=0)))
    close('saved matrix Hermitian',h,h.conj().T,TOL);close('all saved eigenmode residuals',h@v,v*e[None,:],TOL)
    close('all mode norm',v.conj().T@v,np.eye(d),TOL);close('literal saved ground',g,v[:,0],0.)
    gap=float(e[1]-e[0]);close('ground energy',e[0],saved['ground_energy_without_common_ARpop']);close('ground gap',gap,saved['ground_gap'])
    well,vertices,contacts=literal_sources(labels,theta,kappa,phis)
    close('independent bounded well',well,arr[prefix+'well_diagonal'],TOL)
    close('independent source vertex',vertices,arr[prefix+'source_vertices_diagonal'],TOL)
    close('independent direct second contact',contacts,arr[prefix+'source_direct_contacts_diagonal'],TOL)
    close('full saved mode/source couplings',v.conj().T@(vertices.T*g[:,None]),arr[prefix+'source_mode_couplings'],TOL)
    close('complete holding affine matrix',h-base,np.diag(well),TOL)
    gradient=np.array([np.real(np.vdot(g,w*g)) for w in vertices]);direct=np.diag(contacts@abs(g)**2)
    close('independent source gradient',gradient,saved['gradient']);close('complete direct contact',direct,saved['direct_contact'])
    location(g,labels,theta,phis,kappa,saved['localization']);close('complete native plus holding energy',inventory(g,labels,u,well,saved['energy_inventory_without_common_ARpop'],h),e[0])
    qualified=gap>OBS;exact('frozen gap refusal',saved['spectral_response_status']==('RESOLVED_FINITE_GROUND_SPECTRAL_RESPONSE' if qualified else 'GROUND_GAP_UNQUALIFIED'))
    cert=spectrum_uncertainty(h,e,v);uncertainty=state_uncertainty(h,e,g,cert,vertices,contacts)
    label=ACTIVE['group']+'_'+prefix.rstrip('_').split('_')[1]+'_s'+str(ACTIVE['s'])
    parent_failed=(label+'_contact_response_identity') in FAILED_NAMES
    response={'sector':label,'spectrum_uncertainty':cert,'saved_state_uncertainty':uncertainty,
              'original_response_status':saved['spectral_response_status'],'original_parent_failed_control':parent_failed}
    hessian=None
    if qualified:
        response['exact_binary_arithmetic']=binary_contact_diagnostic(saved['direct_contact'],saved['spectral_susceptibility'],saved['ground_hessian'])
    if parent_failed:
        response['diagnostic_status']='NEAR_DEGENERATE_HESSIAN_UNQUALIFIED_ORIGINAL_FAILURE_PRESERVED'
        response['bordered_solve']='REFUSED_FOR_THE_THREE_ORIGINAL_FAILED_AB_CURVATURES'
    elif qualified:
        # Complete saved H only: no eigensolver, native reassembly or propagation.
        border=np.empty((d+1,d+1),dtype=np.result_type(h,g,complex));border[:d,:d]=h-e[0]*np.eye(d);border[:d,d]=g;border[d,:d]=g.conj();border[d,d]=0.
        rhs=np.zeros((d+1,len(phis)),complex);rhs[:d]=-(vertices*g[None,:]).T
        try:
            sol=np.linalg.solve(border,rhs);tangent=sol[:d]
            candidate=direct+2*np.real(tangent.conj().T@(vertices*g[None,:]).T)
            errors={'linear_equation':float(np.max(abs(border@sol-rhs))),
                    'normalization_tangent':float(np.max(abs(g.conj()@tangent))),
                    'HF_multiplier':float(np.max(abs(sol[d]+gradient))),
                    'Hessian_symmetry':float(np.max(abs(candidate-candidate.T))),
                    'bordered_vs_spectral_Hessian':float(np.max(abs(candidate-np.asarray(saved['ground_hessian'])))),
                    'bordered_vs_spectral_susceptibility':float(np.max(abs(direct-candidate-np.asarray(saved['spectral_susceptibility']))))}
            finite=bool(np.isfinite(candidate).all() and all(math.isfinite(x) for x in errors.values()))
            consistent=finite and max(errors.values())<=OBS
            response.update(bordered_comparison_errors=errors if finite else None,
                            bordered_Hessian_candidate=candidate.tolist() if finite else None,
                            comparison_tolerance_unchanged=OBS,
                            diagnostic_status='BORDERED_NUMERICAL_CONSISTENCY_ONLY' if consistent else 'BORDERED_RESPONSE_COMPARISON_UNQUALIFIED')
            if consistent:hessian=candidate
        except np.linalg.LinAlgError as error:
            response.update(diagnostic_status='BORDERED_LINEAR_SOLVE_UNQUALIFIED',linear_solver_error=str(error))
    else:
        exact('refused Hessian preserved',saved['ground_hessian'] is None and saved['spectral_susceptibility'] is None)
        response['diagnostic_status']='ORIGINAL_GROUND_GAP_REFUSAL_PRESERVED'
    response['scope']='Numerical agreement is not an independently directed physical Hessian-error interval.'
    RESPONSE_DIAGNOSTICS.append(response)
    if labels==PAIRS and ACTIVE['m']==0:
        PROJECTIONS.append(exchange_projection(h,e,v,g,vertices,contacts,cert,ACTIVE['group'],ACTIVE['s'],u))
    return float(e[0]),gradient,direct,hessian,uncertainty,cert

def main():
    exact('root-only exact --execute',sys.argv[1:]==['--execute']);exact('exclusive audit outputs',not any(p.exists() for p in (OUT,MD,RECEIPT,ERROR)))
    p,r=authenticate();expected=[(k,m,s) for k in range(3) for m in range(16) for s in range(3)]
    exact('full ordered144 census',[(z['strength_index'],z['B_center_index'],z['s']) for z in p['rows']]==expected)
    exact('48 full groups',len(p['groups'])==48 and p['group_count']==48 and p['row_count']==144)
    with np.load(J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz',allow_pickle=False) as z:
        bases={x:z[x].copy() for x in ('tagged_base_matrices','reference_base_matrices','tagged_base_eigenvalues','reference_base_eigenvalues')}
    theta=np.zeros(8)
    for i,v in enumerate(CYCLE):theta[v]=i*math.pi/4
    bits=np.array([[(q>>v)&1 for q in range(256)] for v in range(8)]);loading=bits[0]+bits[4];pop=bits.sum(0);summaries=[]
    for group in p['groups']:
        k,m=group['strength_index'],group['B_center_index'];ACTIVE.update(group=group['group'],m=m);phi=m*math.pi/8;kappa=KS[k]
        exact('group checkpoint comparison excluding result-only row_file',read(CP/group['row_file'])=={x:y for x,y in group.items() if x!='row_file'})
        exact('committed bundle identity',group['eigensystems_sha256']==r['checkpoint_sha256'][group['eigensystems_file']])
        with np.load(CP/group['eigensystems_file'],allow_pickle=False) as z:arrays={x:z[x].copy() for x in z.files}
        close('true global cycle',arrays['global_cycle_nodes'],CYCLE,0.);close('true chart',arrays['theta_global'],theta,0.)
        close('all global q bits',arrays['global_record_bits'],bits,0.);close('loading map',arrays['record_loading_s'],loading,0.)
        close('population map',arrays['record_population'],pop,0.);close('ordered tagged pairs',arrays['ordered_tagged_pairs'],PAIRS,0.)
        exact('class census',[int(np.sum(loading==s)) for s in range(3)]==[64,128,64]);close('AR census',arrays['AR_branches'],ARS,0.)
        values=[]
        for s,row in enumerate(group['rows']):
            ACTIVE.update(s=s);exact('row identity',(row['strength_index'],row['B_center_index'],row['s'])==(k,m,s))
            exact('flat/group row identity',row==p['rows'][(k*16+m)*3+s]);u=s/2
            data={}
            for name,labels,phis,source in (('A',tuple((v,) for v in range(8)),(0.,),'A_reference'),('B',tuple((v,) for v in range(8)),(phi,),'B_reference'),('AB',PAIRS,(0.,phi),'AB_ground')):
                base=bases['tagged_base_matrices' if name=='AB' else 'reference_base_matrices'][s]
                data[name]=sector(arrays,'s%d_%s_'%(s,name),labels,theta,kappa,phis,u,row[source],base)
            d0=2+u;e0=8+(d0-math.sqrt(d0*d0+.16))/2;vac=arrays['s%d_vacuum_matrix'%s];vg=arrays['s%d_vacuum_ground'%s]
            close('literal vacuum block',vac,[[8+d0,-.2],[-.2,8]],0.);close('analytic vacuum eigenstate',vac@vg,e0*vg,TOL)
            close('analytic vacuum ground energy',e0,row['vacuum']['ground_energy_without_common_ARpop'])
            energies=np.array([data['AB'][0],data['A'][0],data['B'][0],e0]);w=float(energies@[1,-1,-1,1])
            grad=data['AB'][1]-[data['A'][1][0],data['B'][1][0]];contact=data['AB'][2]-np.diag([data['A'][2][0,0],data['B'][2][0,0]])
            hess=data['AB'][3]-np.diag([data['A'][3][0,0],data['B'][3][0,0]]) if all(data[x][3] is not None for x in ('A','B','AB')) else None
            raw_hess=None if any(row[z]['ground_hessian'] is None for z in ('AB_ground','A_reference','B_reference')) else (
                np.array(row['AB_ground']['ground_hessian'])-np.diag([row['A_reference']['ground_hessian'][0][0],row['B_reference']['ground_hessian'][0][0]]))
            close('complete connected energy',w,row['connected_W']);close('complete connected gradient',grad,row['connected_gradient'])
            close('connected torque/arc force',-grad,row['connected_torque']);close('connected arc force radiusone',-grad,row['connected_arc_force'])
            close('declared apparatus reaction',sum(grad),row['fixed_chart_connected_reaction_torque']);close('connected direct contact',contact,row['connected_direct_contact'])
            if raw_hess is None:exact('complete original connected refusal',row['connected_ground_hessian'] is None and row['connected_spectral_susceptibility'] is None and row['connected_response_status']=='GROUND_GAP_UNQUALIFIED')
            else:
                close('raw connected Hessian subtraction preserved',raw_hess,row['connected_ground_hessian'])
                close('raw connected susceptibility subtraction preserved',np.array(row['AB_ground']['spectral_susceptibility'])-np.diag([
                    row['A_reference']['spectral_susceptibility'][0][0],row['B_reference']['spectral_susceptibility'][0][0]]),row['connected_spectral_susceptibility'])
                exact('original connected status retained',row['connected_response_status']=='RESOLVED_FINITE_CONNECTED_GROUND_RESPONSE')
            force_bounds=[]
            for l,name in enumerate(('A','B')):
                ab=data['AB'][4]['source_gradient_error_upper_estimates'];ref=data[name][4]['source_gradient_error_upper_estimates']
                force_bounds.append(None if ab is None or ref is None else ab[l]+ref[0])
            energy_bounds=[data[x][5]['ordered_spectrum_error_bound_estimate'] for x in ('AB','A','B')]
            energy_error=None if any(x is None for x in energy_bounds) else sum(energy_bounds)
            connected_consistency=None if hess is None or raw_hess is None else float(np.max(abs(hess-raw_hess)))
            if m==0:
                projection=PROJECTIONS[-1]
                exact('ordered coincident projection identity',projection['group']==group['group'] and projection['s']==s)
                new_torque=-(np.array(projection['NEW_gradient'])-np.array([data['A'][1][0],data['B'][1][0]]))
                close('NEW even connected torque equality',new_torque[0],new_torque[1],OBS)
                projection['NEW_connected_torque']=new_torque.tolist()
                projection['NEW_connected_torque_minus_saved']=(new_torque-np.array(row['connected_torque'])).tolist()
            work=row['source_work_inventory']
            for name,idx in (('AB',0),('A',1),('B',2)):
                ev=bases['tagged_base_eigenvalues' if name=='AB' else 'reference_base_eigenvalues'][s,0]
                close('static holding ground shift '+name,energies[idx]-ev,work['static_holding_ground_shift_'+name])
                close('held ground well energy '+name,row['AB_ground' if name=='AB' else name+'_reference']['energy_inventory_without_common_ARpop']['holding_wells'],work['held_ground_well_energy_'+name])
            close('inclusive source work vertices',grad,work['translation_work_vertices_connected'])
            close('trap-center separation',min(phi,2*math.pi-phi),row['trap_center_shortest_arc'])
            exact('cusp refusal',row['radial_derivative_status']==('NOT_DEFINED_AT_CENTER_CUSP' if m in (0,8) else 'ORIENTED_TRANSLATION_REPORTED_NO_BODY_CENTER_IDENTIFICATION'))
            values.append((energies,w,grad,raw_hess))
            summaries.append({'group':group['group'],'s':s,'W':w,'torque':(-grad).tolist(),
                'connected_energy_error_bound_estimate':energy_error,'connected_force_error_upper_estimates':force_bounds,
                'bordered_connected_comparison_error':connected_consistency,
                'connected_Hessian_diagnostic_status':('ORIGINAL_FAILED_AB_HESSIAN_UNQUALIFIED' if k==2 and m==0 else
                    'BORDERED_NUMERICAL_CONSISTENCY_ONLY' if connected_consistency is not None and connected_consistency<=OBS else 'CONNECTED_RESPONSE_COMPARISON_UNQUALIFIED'),
                'original_connected_response_status':row['connected_response_status'],
                'scope':'Raw energy/force/contact arithmetic verified; nondirected uncertainties, no automatic physical ground-response precision.'})
        absolute=arrays['absolute_ground_energies_AR_q_AB_A_B_0']
        target=np.array([np.array([values[int(s)][0] for s in loading])+ar*pop[:,None] for ar in ARS])
        close('all absolute q/AR energies',absolute,target);close('all scalar cancellation',absolute[:,:,0]-absolute[:,:,1]-absolute[:,:,2]+absolute[:,:,3],np.tile([values[int(s)][1] for s in loading],(4,1)))
        for v in (1,2,3,5,6,7):
            low=np.flatnonzero(bits[v]==0);high=low+(1<<v)
            close('nonendpoint scalar clock source difference',absolute[:,high]-absolute[:,low],np.broadcast_to(np.array(ARS)[:,None,None],(4,128,4)))
        for s,row in enumerate(group['rows']):
            close('all raw loading W',values[s][1]-values[0][1],row['loading_difference_W'])
            close('all raw loading gradient',values[s][2]-values[0][2],row['loading_difference_gradient'])
            close('all raw loading torque',-(values[s][2]-values[0][2]),row['loading_difference_torque'])
            close('all raw loading arc force',-(values[s][2]-values[0][2]),row['loading_difference_arc_force'])
            if values[s][3] is None or values[0][3] is None:exact('loading Hessian refusal',row['loading_difference_ground_hessian'] is None)
            else:close('loading connected Hessian',values[s][3]-values[0][3],row['loading_difference_ground_hessian'])
    exact('all144 audited cells',len(summaries)==144)
    exact('all432 sector response diagnostics',len(RESPONSE_DIAGNOSTICS)==432)
    exact('all9 coincident symmetry projections',[(x['group'],x['s']) for x in PROJECTIONS]==[('k%d_m00'%k,s) for k in range(3) for s in range(3)])
    exact('all3 original AB curvatures refused',sum(x['diagnostic_status']=='NEAR_DEGENERATE_HESSIAN_UNQUALIFIED_ORIGINAL_FAILURE_PRESERVED' for x in RESPONSE_DIAGNOSTICS)==3)
    report=(J/(NAME+'_RESULT.md')).read_text();exact('full report tables',sum(x.startswith('| data ') for x in report.splitlines())==144 and sum(x.startswith('| reference ') for x in report.splitlines())==144)
    for f,h in INPUTS.items():exact('unchanged '+f,sha(ROOT/f)==h)
    scalars=sum(x['scalar_assertions'] for x in CHECKS);maximum=max(x.get('maximum_error',0.) or 0. for x in CHECKS)
    result={'diagnostic_status':'PASS_SAVED_ACTION_AND_READOUT_SCOPE_WITH_UNQUALIFIED_RESPONSE','failed_assertions':0,
            'producer_status_preserved':p['status'],'producer_failed_controls_preserved':[x for x in p['checks'] if not x['passed']],
            'assertions':len(CHECKS),'scalar_and_metadata_assertions':scalars,'maximum_absolute_error':maximum,
            'audited_cells':144,'input_sha256':INPUTS,'producer_result_raw_sha256':r['result_raw_sha256'],'producer_receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),
            'diagnostic_source_sha256':sha(__file__),'checks':CHECKS,'summaries':summaries,
            'sector_response_diagnostics':RESPONSE_DIAGNOSTICS,'NEW_coincident_exchange_even_projections':PROJECTIONS,
            'elapsed_seconds':time.monotonic()-START,
            'method':'complete saved matrices; literal trig vertices/localization; polar/residual uncertainty estimates; bordered comparisons with original3refused; NEWall9 exchange-even projections; exact-binary Decimal subtraction; no eigensolver, native H rebuild, trajectory or producer import'}
    raw=write(OUT,result)
    report=['# Fixed-chart holding saved diagnostic V001','',
        'Saved action/readout scope PASS: all144 cells, %d scalar/metadata assertions; maximum checked residual %.12g.'%(scalars,maximum),'',
        'The sealed producer remains ARITHMETIC_FAILED with exactly3 failed contact-reconstruction controls. All3 corresponding AB/connected/loading Hessians remain unqualified. Decimal reconstructs only a NEW exact-binary arithmetic expression; it does not improve spectral accuracy.','',
        'All432 sector diagnostics retain raw response statuses, bordered comparison/refusal and nondirected polar/residual/gap force/contact uncertainty estimates. Agreement is numerical consistency, not an independently certified physical Hessian interval.','',
        'All9 identical-well cells have a separately labelled NEW exchange-even projection, Rayleigh energy, gradient/contact, residual/gap uncertainty and old/new differences. Original states and readouts remain sealed; no projection is made for separated traps.','',
        '| group | s | W | torque A | torque B | Hessian diagnostic |','|---|---:|---:|---:|---:|---|']
    for z in summaries:report.append('| data %s | %d | %.12g | %.12g | %.12g | %s |'%(z['group'],z['s'],z['W'],*z['torque'],z['connected_Hessian_diagnostic_status']))
    report+=['','| group | s | saved exchange gradient difference | NEW Rayleigh energy | NEW connected torque A | NEW connected torque B |','|---|---:|---:|---:|---:|---:|']
    for z in PROJECTIONS:report.append('| projection %s | %d | %.12g | %.12g | %.12g | %.12g |'%(z['group'],z['s'],z['saved_exchange_gradient_difference'],z['NEW_Rayleigh_energy'],*z['NEW_connected_torque']))
    report+=['','Full uncertainties, raw comparisons and Decimal matrices are in the lossless diagnostic JSON. No eigensolver, new native action, trajectory, RNG or producer import was used. Physical proper chart/probe calibration remains open.']
    with MD.open('x') as f:f.write('\n'.join(report)+'\n');f.flush();os.fsync(f.fileno())
    receipt={'diagnostic_status':result['diagnostic_status'],'producer_status_preserved':p['status'],'failed_assertions':0,
             'diagnostic_raw_sha256':raw,'diagnostic_report_sha256':sha(MD),'diagnostic_source_sha256':sha(__file__),
             'input_sha256':INPUTS,'assertions':len(CHECKS),'scalar_and_metadata_assertions':scalars,'audited_cells':144,'NEW_projection_cells':9}
    rh=write(RECEIPT,receipt);print(json.dumps({'diagnostic_status':result['diagnostic_status'],'assertions':scalars,'raw_sha256':raw,'receipt_sha256':rh}),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as error:
        if not ERROR.exists():write(ERROR,{'diagnostic_status':'FAILED_ATTEMPT_PRESERVED','error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'diagnostic_source_sha256':sha(__file__)})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
