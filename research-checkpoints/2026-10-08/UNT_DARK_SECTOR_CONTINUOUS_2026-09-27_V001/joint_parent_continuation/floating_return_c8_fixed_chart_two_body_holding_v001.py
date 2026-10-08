#!/usr/bin/env python3
"""NEW conditional fixed-chart static holding sources; root alone executes."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,time,resource,traceback,re
from pathlib import Path
import numpy as np
J=Path(__file__).resolve().parent;ROOT=J.parent.parent;D=J.parent
NAME='FLOATING_RETURN_C8_FIXED_CHART_TWO_BODY_HOLDING_V001'
CP=J/'floating_return_c8_fixed_chart_two_body_holding_v001_checkpoints'
RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PROTOCOL_SHA='ab51f8a60d78840a1fd788dfc7317e0b8072277ef1698d8dfafeb9da8d80a6a0'
CONTRACT='LOCAL_RECORD_FEEDBACK_FIXED_CHART_TWO_BODY_HOLDING_SOURCE_V001.md'
LAW='LOCAL_RECORD_FEEDBACK_OCCUPIED_INCIDENCE_MEMORY_LAW_V001.md'
PACKETS=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','floating_return_c8_tagged_probe_reaction_v001',1146,416),
         ('FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001','floating_return_c8_retained_record_geometry_v001',3018,1352))
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple((CYCLE[k],CYCLE[(k+1)%8]) for k in range(8))
PAIRS=tuple((a,b) for a in range(8) for b in range(8) if a!=b)
KAPPAS=(.1,.5,2.);KAPPA_RATIONAL=('1/10','1/2','2')
ARS=(0.,.125,.175,.25);AR_RATIONAL=('0','1/8','7/40','1/4')
H=.2;T=.1;JC=.25;LAM=.5;RADIUS=1.;TOL=5e-10;OBS_TOL=1e-9;GAP_FLOOR=1e-9
CHECKS=[];INPUTS={};COMMITS={};ACTIVE={};STARTED=False
PINS={'LOCAL_RECORD_FEEDBACK_OCCUPIED_INCIDENCE_MEMORY_LAW_V001.md': '9239dcce75623cee38dd2ca4df78686b4d75f87d4baa975139549a29f15a0f26', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001.md': '68b4a61ded02e9e6ecdfcf1819680d519f794eb8e3ba08b5b7a1ba329ed1aab9', 'floating_return_c8_tagged_probe_reaction_v001.py': '778ff1615b0ab38c964ca4feb40b756c0df04771103afc953871c12c890e26c0', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RESULT.json': 'd7e4e759b357dd8154567a8a103c433f72236d5b0799123a67b6d40c628baae4', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RESULT.md': '18541d435152d6022cd1ea35285ed339015a7df8f19012cfbfd3a8a54aad4a23', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RECEIPT.json': '7896e0b78db294fe3b66886449d088afee4a6a413ee27056d09b6dde5ed05669', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_AUDIT.json': 'bd324e35eaf8bafa7b8686d49f6d1e4add0ad48c8deb6189d21ed2177f5687d7', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_AUDIT.md': '21c242bf4ed545facdc63dc574a26bb06efd594a5e66cc2bf33dae08708af750', 'floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz': '06432406fd969f8ec3c8d93a606207ff5c4bd1ce0deb0281b87e41e190ebcc1a', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001.md': '8f3dc32381e76a4e6badfe23fff6c8bdd4830cb32ed0aff99b1aef57eba5ce5b', 'floating_return_c8_retained_record_geometry_v001.py': '49f2684fe46bce5d46e8e86782f82d73a0293e304d617a46eb5b84e98638396a', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_RESULT.json': '4104ec10a4c0a6a9183e9943743d80ce847dff4bad8b82013c0f2594bc581eac', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_RESULT.md': 'f209ad41386602049bb51b9310e0224d95f2c52a07c8768f9560b846b6264288', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_RECEIPT.json': '2151436c1ce895c6fb577c72c673faefed184c1c011b57c98368c33dbf0663d5', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_AUDIT.json': '5c519d1bef61c0e4b2cdf71424de9df08fa0d7f926b26c6ab9496c986d97e84f', 'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_AUDIT.md': 'efcc01cdc3c4f2e94e19b921854f97453d0215dca9496c3e1845569222987432', 'floating_return_c8_retained_record_geometry_v001_checkpoints/release_eigensystems.npz': '4dd6c3d1a4d69761e8fb4ecb7755113f81d41473129614a0df9a8f0bcff09ebc', 'LOCAL_RECORD_FEEDBACK_FIXED_CHART_TWO_BODY_HOLDING_SOURCE_V001.md': 'deb197eb8de380498162b90def7632691e834d8e411f3a3e5435a8cdb803f813'}

def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):d.update(b)
    return d.hexdigest()

def read(p):return json.loads(Path(p).read_text())

def clean(v):
    if isinstance(v,np.ndarray):return clean(v.tolist())
    if isinstance(v,np.generic):return clean(v.item())
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    if isinstance(v,complex):return [clean(float(v.real)),clean(float(v.imag))]
    if isinstance(v,float) and not math.isfinite(v):return {'nonfinite':repr(v)}
    return v

def blob(v):return json.dumps(clean(v),sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def write_json(p,v):
    with Path(p).open('xb') as f:
        f.write(json.dumps(clean(v),sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)

def event(v):
    with (CP/'journal.jsonl').open('ab') as f:f.write(blob(v)+b'\n');f.flush();os.fsync(f.fileno())

def commit(p,v,kind):
    h=write_json(p,v);COMMITS[Path(p).name]=h;event({'event':kind,'file':Path(p).name,'sha256':h});return h

def commit_npz(p,**a):
    with Path(p).open('xb') as f:np.savez_compressed(f,**a);f.flush();os.fsync(f.fileno())
    h=sha(p);COMMITS[Path(p).name]=h;event({'event':'operators_saved','file':Path(p).name,'sha256':h});return h

def gate(name,a,b=0.,tol=TOL):
    a,b=np.asarray(a),np.asarray(b);ok=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
    err=float(np.max(abs(a-b))) if ok else float('inf')
    CHECKS.append({'name':name,'error':clean(err),'tolerance':tol,'passed':ok and err<=tol})

def exact(name,ok):CHECKS.append({'name':name,'passed':bool(ok),'exact':True})

def input_id():return hashlib.sha256(blob(INPUTS)).hexdigest()

def recheck():
    for f,h in INPUTS.items():
        if sha(ROOT/f)!=h:raise RuntimeError('input changed: '+f)

def register(p,h):
    if sha(p)!=h:raise RuntimeError('input seal: '+str(p))
    k=str(Path(p).relative_to(ROOT))
    if k in INPUTS and INPUTS[k]!=h:raise RuntimeError('contradictory input seal: '+k)
    INPUTS[k]=h

def authenticate_parent(name,stem,count,frames):
    cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'));a=read(J/(name+'_AUDIT.json'))
    if r['result_raw_sha256']!=sha(J/(name+'_RESULT.json')) or r['result_canonical_sha256']!=hashlib.sha256(blob(p)).hexdigest() or r['report_sha256']!=sha(J/(name+'_RESULT.md')):raise RuntimeError('parent result/canonical/report: '+name)
    if p['failed']!=0 or r['failed']!=0 or p['passed']!=r['passed'] or p['input_sha256']!=r['input_sha256'] or len(p['checks'])!=p['passed'] or not all(c['passed'] for c in p['checks']):raise RuntimeError('parent arithmetic: '+name)
    if a['audit_status']!='PASS' or a['failed_assertions']!=0:raise RuntimeError('parent audit status: '+name)
    if frames==416:
        if a['result_raw_sha256']!=r['result_raw_sha256'] or a['receipt_sha256']!=sha(J/(name+'_RECEIPT.json')) or a['audited_preparations']!=104 or a['audited_tagged_frames']!=416 or a['audited_paired_reference_frames']!=416:raise RuntimeError('tagged audit identity/census')
    else:
        if a['preparations']!=104 or a['frames']!=1352:raise RuntimeError('release audit census')
        for suffix in ('_RESULT.json','_RECEIPT.json'):
            k=str((J/(name+suffix)).relative_to(ROOT))
            if a['input_sha256'][k]!=sha(ROOT/k):raise RuntimeError('release audit parent identity')
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cmap=r['checkpoint_sha256']
    if len(cmap)!=count or {f.name for f in cp.iterdir() if f.name!='journal.jsonl'}!=set(cmap):raise RuntimeError('parent checkpoint census: '+name)
    for f,h in cmap.items():register(cp/f,h)
    jb=(cp/'journal.jsonl').read_bytes();lines=jb.splitlines();es=[json.loads(x) for x in lines]
    if len(es)!=count+3 or hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()!=r['journal_prefix_sha256']:raise RuntimeError('parent journal prefix: '+name)
    expected_report={'event':'report_saved','sha256':r['report_sha256'],('paired_data_rows' if frames==416 else 'data_rows'):frames}
    if es[-3]!={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']} or es[-2]!=expected_report or es[-1]!={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))}:raise RuntimeError('parent final commits: '+name)
    m=read(cp/'manifest.json');mh=sha(cp/'manifest.json')
    if mh!=p['manifest_sha256'] or mh!=es[0]['manifest_sha256'] or m['input_sha256']!=r['input_sha256'] or es[0]['input_sha256']!=r['input_sha256'] or m['PID']!=r['original_manifest_PID'] or es[0]['PID']!=m['PID']:raise RuntimeError('parent manifest/start: '+name)
    commits={'manifest.json':mh}
    for e in es[1:-3]:
        if 'file' not in e or 'sha256' not in e or e['file'] in commits:raise RuntimeError('parent unique commit: '+name)
        commits[e['file']]=e['sha256']
    if commits!=cmap or len(p['preparations'])!=104:raise RuntimeError('parent committed map: '+name)
    register(cp/'journal.jsonl',sha(cp/'journal.jsonl'))
    return cmap


def authenticate():
    if sha(J/(NAME+'.md'))!=PROTOCOL_SHA:raise RuntimeError('unfrozen protocol')
    if len(PINS)!=18:raise RuntimeError('required18 direct inputs')
    for f,h in PINS.items():register(J/f,h)
    anchors=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',(J/CONTRACT).read_text(),re.M)
    if len(anchors)!=8:raise RuntimeError('contract8 resident inputs')
    for f,h in anchors:register((D/f if f.startswith('joint_parent_continuation/') else ROOT/f),h)
    ancestry=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',(J/LAW).read_text(),re.M)
    if len(ancestry)!=15:raise RuntimeError('law15 ancestry inputs')
    for f,h in ancestry:register(J/f,h)
    register(J/(NAME+'.md'),PROTOCOL_SHA);register(Path(__file__).resolve(),sha(__file__))
    maps=[authenticate_parent(*p) for p in PACKETS]
    for i,(stem,f) in enumerate(((PACKETS[0][1],'reaction_eigensystems.npz'),(PACKETS[1][1],'release_eigensystems.npz'))):
        es=[json.loads(x) for x in (J/(stem+'_checkpoints/journal.jsonl')).read_text().splitlines()]
        if [e for e in es if e.get('file')==f]!=[{'event':'eigensystems_saved','file':f,'sha256':maps[i][f]}]:raise RuntimeError('unique native bundle commit')

def source_profile(theta,kappa,phi):
    return kappa*(1-np.cos(theta-phi)),-kappa*np.sin(theta-phi),kappa*np.cos(theta-phi)

def native_structure(labels):
    # Independent native mismatch/hopping action, retaining the complete field self.
    index={p:i for i,p in enumerate(labels)};n=len(labels);nc=len(labels[0])
    cuts=np.zeros((2,n));hops=[]
    for edge in range(2):
        terms=[]
        for col,pos in enumerate(labels):
            occupied=set(pos)
            for u,v in EDGES:
                if edge==0 and {u,v}=={0,4}:continue
                cuts[edge,col]+=int((u in occupied)!=(v in occupied))
                for particle,a in enumerate(pos):
                    dest=v if a==u else (u if a==v else None)
                    if dest is not None and dest not in occupied:
                        moved=list(pos);moved[particle]=dest;terms.append((index[tuple(moved)],col))
        hops.append(tuple(terms))
    return {'labels':labels,'nc':nc,'cuts':cuts,'hops':hops}

def native_action(v,structure,u,well):
    d=len(structure['labels']);was_vector=v.ndim==1;x=v.reshape(2,d,-1)
    diagonal=8+structure['nc']+2*np.array([1,0])[:,None]+u*np.array([1,0])[:,None]+JC*structure['cuts']+well[None,:]
    y=diagonal[:,:,None]*x-H*x[::-1]
    for edge in range(2):
        for row,col in structure['hops'][edge]:y[edge,row]-=T*x[edge,col]
    return y.reshape(2*d) if was_vector else y.reshape(2*d,-1)

def source_arrays(labels,theta,kappa,phiA,phiB=None):
    va,da,ca=source_profile(theta,kappa,phiA)
    if len(labels[0])==1:
        w=np.array([va[a[0]] for a in labels]);dv=np.array([[da[a[0]] for a in labels]]);ct=np.array([[ca[a[0]] for a in labels]])
    else:
        vb,db,cb=source_profile(theta,kappa,phiB)
        w=np.array([va[a]+vb[b] for a,b in labels]);dv=np.array([[da[a] for a,b in labels],[db[b] for a,b in labels]])
        ct=np.array([[ca[a] for a,b in labels],[cb[b] for a,b in labels]])
    return w,np.tile(dv,(1,2)),np.tile(ct,(1,2))

def observables(ground,structure,theta,phis,kappa):
    d=len(structure['labels']);p=np.sum(abs(ground.reshape(2,d))**2,axis=0)
    q=np.zeros((8,8)) if structure['nc']==2 else None
    marginals=np.zeros((structure['nc'],8))
    for value,pos in zip(p,structure['labels']):
        for particle,node in enumerate(pos):marginals[particle,node]+=value
        if q is not None:q[pos]+=value
    gate('position norm',p.sum(),1.,OBS_TOL);gate('each carrier norm',marginals.sum(1),np.ones(structure['nc']),OBS_TOL)
    sites=[]
    for i,(prob,phi) in enumerate(zip(marginals,phis)):
        z=prob@np.exp(1j*theta);mod=float(abs(z));mu=float(prob@(1-np.cos(theta-phi)))
        sites.append({'site_probability':prob,'circular_first_moment':z,'circular_concentration':mod,
            'circular_mean_angle':float(np.angle(z)) if mod>OBS_TOL else None,
            'mean_chord_position':[RADIUS*float(z.real),RADIUS*float(z.imag)],'well_misalignment':mu,
            'well_energy':kappa*mu,'center_phi':phi})
        exact('probabilities nonnegative',bool(np.all(prob>=-OBS_TOL)));exact('circular concentration range',mod<=1+OBS_TOL)
    pair=None
    if q is not None:
        gate('same-site exclusion',np.diag(q),np.zeros(8),0.);gate('pair marginal A',q.sum(1),marginals[0],OBS_TOL);gate('pair marginal B',q.sum(0),marginals[1],OBS_TOL)
        cycle_index={v:j for j,v in enumerate(CYCLE)};dist=np.zeros(4);arc=0.;chord=0.
        for (a,b),value in zip(structure['labels'],p):
            raw=abs(cycle_index[a]-cycle_index[b]);step=min(raw,8-raw);dist[step-1]+=value
            arc+=value*RADIUS*step*math.pi/4;chord+=value*2*RADIUS*math.sin(step*math.pi/8)
        gate('complete distance distribution',dist.sum(),1.,OBS_TOL)
        pair={'ordered_pair_probability':q,'cycle_step_probability':dist,'mean_shortest_arc_distance':float(arc),
            'mean_chord_distance':float(chord),'adjacent_probability':float(dist[0]),'anchor_pair_probability':float(q[0,4]+q[4,0]),'same_site_probability':0.}
    return {'site_readouts':sites,'pair_readout':pair},p

def energy_inventory(ground,structure,u,well,ar_pop=0.):
    x=ground.reshape(2,-1);p=abs(x)**2;empty=float(p[0].sum());hopping=0.
    for edge in range(2):
        hopping-=T*sum(float(np.real(x[edge,row].conjugate()*x[edge,col])) for row,col in structure['hops'][edge])
    components={'field_self':8.,'carrier_storage':float(structure['nc']),'degree_defect':2*empty,
        'native_record_feedback':u*empty,'current_square':JC*float(np.sum(p*structure['cuts'])),
        'occupied_hopping':hopping,'incidence_flip':-2*H*float(np.real(np.vdot(x[0],x[1]))),
        'holding_wells':float(np.sum(p*well[None,:])),'record_charging_ARpop':ar_pop}
    return components

def solve_target(base,structure,u,well,vertices,contacts,theta,phis,kappa,label):
    matrix=base+np.diag(np.tile(well,2));gate(label+'_matrix_Hermitian',matrix,matrix.T)
    # These are NEW holding eigenproblems; no source-off eigensolver is called.
    energies,modes=np.linalg.eigh(matrix);ground=modes[:,0];gap=float(energies[1]-energies[0]);qualified=gap>GAP_FLOOR
    gate(label+'_all_modes',native_action(modes,structure,u,well),modes*energies[None,:])
    gate(label+'_orthonormal_modes',modes.T@modes,np.eye(len(modes)))
    exact(label+'_finite_ordered_spectrum',bool(np.isfinite(energies).all() and np.all(np.diff(energies)>=0)))
    gate(label+'_native_target_action',native_action(np.eye(len(modes)),structure,u,well),matrix)
    gate(label+'_source_diagonal_assembly',matrix-base,np.diag(np.tile(well,2)))
    # The literal profile derivatives are preserved as diagonal arrays.
    dv=modes.T@(vertices.T*ground[:,None]);direct=np.diag(contacts@(ground**2));gradient=dv[0]
    susceptibility=2*np.real((dv[1:]/(energies[1:]-energies[0])[:,None]).conj().T@dv[1:]) if qualified else None
    hessian=direct-susceptibility if qualified else None
    readouts,prob=observables(ground,structure,theta,phis,kappa);inventory=energy_inventory(ground,structure,u,well)
    gate(label+'_complete_energy_inventory',sum(inventory.values()),energies[0],OBS_TOL)
    for i,site in enumerate(readouts['site_readouts']):
        z=complex(*site['circular_first_moment']) if isinstance(site['circular_first_moment'],list) else site['circular_first_moment'];rot=np.exp(-1j*phis[i])*z
        gate(label+'_first_vertex_from_actual_position'+str(i),gradient[i],-kappa*rot.imag,OBS_TOL)
        gate(label+'_second_contact_from_actual_position'+str(i),direct[i,i],kappa*rot.real,OBS_TOL)
        gate(label+'_well_from_actual_position'+str(i),site['well_energy'],kappa*(1-rot.real),OBS_TOL)
        gate(label+'_literal_sin_vertex'+str(i),vertices[i],np.tile([-kappa*math.sin(theta[pos[i]]-phis[i]) for pos in structure['labels']],2))
        gate(label+'_literal_cos_contact'+str(i),contacts[i],np.tile([kappa*math.cos(theta[pos[i]]-phis[i]) for pos in structure['labels']],2))
    if qualified:
        gate(label+'_susceptibility_Hermitian',susceptibility,susceptibility.T,OBS_TOL)
        gate(label+'_contact_response_identity',hessian+susceptibility,direct,OBS_TOL)
        exact(label+'_spectral_diagonal_response_positive',bool(np.all(np.diag(susceptibility)>=-OBS_TOL)))
    # Connected full negative hop/flip graph supplies uniqueness independently.
    adjacency=matrix<0;seen={0};pending=[0]
    while pending:
        v=pending.pop()
        for dest in np.flatnonzero(adjacency[v]):
            if int(dest) not in seen:seen.add(int(dest));pending.append(int(dest))
    exact(label+'_complete_stoquastic_connected_graph',len(seen)==len(matrix) and np.all(matrix[~np.eye(len(matrix),dtype=bool)]<=0))
    out={'ground_energy_without_common_ARpop':float(energies[0]),'ground_gap':gap,'gap_floor':GAP_FLOOR,
        'spectral_response_status':'RESOLVED_FINITE_GROUND_SPECTRAL_RESPONSE' if qualified else 'GROUND_GAP_UNQUALIFIED',
        'gradient':gradient,'direct_contact':direct,'spectral_susceptibility':susceptibility,'ground_hessian':hessian,
        'energy_inventory_without_common_ARpop':inventory,'localization':readouts}
    arrays={'matrix':matrix,'eigenvalues':energies,'eigenvectors':modes,'ground':ground,'well_diagonal':np.tile(well,2),
        'source_vertices_diagonal':vertices,'source_direct_contacts_diagonal':contacts,'source_mode_couplings':dv}
    return out,arrays

def vacuum(s):
    d=2+LAM*s;root=math.sqrt(d*d+4*H*H);e=8+(d-root)/2;p=(1-d/root)/2;g=np.array([math.sqrt(p),math.sqrt(1-p)])
    matrix=np.array([[8+d,-H],[-H,8.]])
    gate('analytic vacuum characteristic',(e-8)*(e-8-d),H*H,OBS_TOL);gate('analytic vacuum ground',matrix@g,e*g)
    gate('analytic vacuum norm',np.vdot(g,g),1.,OBS_TOL)
    inventory={'field_self':8.,'degree_defect':2*p,'native_record_feedback':LAM*s*p,'incidence_flip':-2*H*math.sqrt(p*(1-p)),'record_charging_ARpop':0.}
    gate('analytic vacuum complete inventory',sum(inventory.values()),e,OBS_TOL)
    return {'ground_energy_without_common_ARpop':e,'empty_probability':p,'energy_inventory_without_common_ARpop':inventory},matrix,g

def main():
    global STARTED,ACTIVE
    started=time.monotonic()
    if sys.argv[1:]!=['--execute']:raise RuntimeError('root-only exact --execute required')
    if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)):raise RuntimeError('reserved output exists; no retry/overwrite')
    authenticate();CP.mkdir();STARTED=True
    manifest={'PID':os.getpid(),'Python':sys.version,'NumPy':np.__version__,'threads':1,'input_sha256':INPUTS,
        'parameters':{'h':H,'t':T,'j':JC,'lambda':LAM,'radius':RADIUS,'global_cycle':CYCLE,'kappa_rational':KAPPA_RATIONAL,
            'B_center_pi_eighths':list(range(16)),'A_center':0,'s':[0,1,2],'AR_rational':AR_RATIONAL,
            'mode_tolerance':TOL,'observable_tolerance':OBS_TOL,'spectral_gap_floor':GAP_FLOOR},'group_count':48,'row_count':144}
    mh=write_json(CP/'manifest.json',manifest);COMMITS['manifest.json']=mh;event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':INPUTS})
    with np.load(J/(PACKETS[0][1]+'_checkpoints/reaction_eigensystems.npz'),allow_pickle=False) as f:data={k:f[k].copy() for k in f.files}
    with np.load(J/(PACKETS[1][1]+'_checkpoints/release_eigensystems.npz'),allow_pickle=False) as f:release={k:f[k].copy() for k in f.files}
    gate('authentic global cyclic map',data['cycle_global_nodes'],np.array(CYCLE),0.);gate('all ordered tagged pairs',data['ordered_tagged_pairs'],np.array(PAIRS),0.)
    bits=np.array([[(q>>v)&1 for q in range(256)] for v in range(8)]);load=bits[0]+bits[4];pop=bits.sum(0)
    gate('all global q bits',data['global_record_bits'],bits,0.);exact('complete q classes',[int(np.sum(load==s)) for s in range(3)]==[64,128,64])
    eligible=tuple((a,b) for a in range(4) for b in range(4,8));occupied={tuple(sorted(e)) for e in EDGES}
    exact('literal K44 eligibility and anchor',len(eligible)==16 and occupied.issubset(set(eligible)) and (0,4) in occupied)
    for bit in (0,1):
        degree=np.zeros(8,dtype=int)
        for a,b in occupied:
            if bit==0 and (a,b)==(0,4):continue
            degree[a]+=1;degree[b]+=1
        expected=np.full(8,2);expected[[0,4]]=1 if bit==0 else 2
        gate('held15 and released anchor degrees '+str(bit),degree,expected,0.)
    for suffix in ('matrices','eigenvalues','eigenvectors'):gate('separate native one-carrier_'+suffix,data['reference_base_'+suffix],release['base_'+suffix])
    theta=np.zeros(8)
    for cyclic,global_node in enumerate(CYCLE):theta[global_node]=cyclic*math.pi/4
    gate('actual cyclic chart pullback',theta[np.array(CYCLE)],np.arange(8)*math.pi/4,0.)
    structures={'one':native_structure(tuple((v,) for v in range(8))),'two':native_structure(PAIRS)}
    for key,two in (('one',False),('two',True)):
        sector='tagged' if two else 'reference';st=structures[key];d=2*len(st['labels'])
        exact('complete native input shape '+key,data[sector+'_base_matrices'].shape==(3,d,d))
        for s in range(3):gate('independent complete unheld native action '+key+str(s),native_action(np.eye(d),st,LAM*s,np.zeros(d//2)),data[sector+'_base_matrices'][s])
    rows=[];groups=[];cache={}
    for k,kappa in enumerate(KAPPAS):
        for m in range(16):
            phi=m*math.pi/8;name='k%d_m%02d'%(k,m);ACTIVE={'group':name};before=len(CHECKS);arrays={};group=[]
            for s in range(3):
                ACTIVE={'group':name,'s':s};u=LAM*s
                wa,va,ca=source_arrays(structures['one']['labels'],theta,kappa,phi)
                b,ba=solve_target(data['reference_base_matrices'][s],structures['one'],u,wa,va,ca,theta,(phi,),kappa,name+'_B_s'+str(s))
                if m==0:cache[k,s]=(b,ba)
                a,aa=cache[k,s];w2,v2,c2=source_arrays(PAIRS,theta,kappa,0.,phi)
                pair,pa=solve_target(data['tagged_base_matrices'][s],structures['two'],u,w2,v2,c2,theta,(0.,phi),kappa,name+'_AB_s'+str(s))
                v0,vm,vg=vacuum(s);e2=pair['ground_energy_without_common_ARpop'];ea=a['ground_energy_without_common_ARpop'];eb=b['ground_energy_without_common_ARpop'];e0=v0['ground_energy_without_common_ARpop']
                w=e2-ea-eb+e0;g=np.asarray(pair['gradient'])-np.array([a['gradient'][0],b['gradient'][0]])
                contact=np.asarray(pair['direct_contact'])-np.diag([a['direct_contact'][0,0],b['direct_contact'][0,0]])
                qualified=all(z['ground_hessian'] is not None for z in (a,b,pair))
                susceptibility=np.asarray(pair['spectral_susceptibility'])-np.diag([a['spectral_susceptibility'][0,0],b['spectral_susceptibility'][0,0]]) if qualified else None
                curvature=contact-susceptibility if qualified else None;torque=-g
                gate('source A reused exact at zero center',a['gradient'],cache[k,s][0]['gradient'],0.)
                if m==0:gate('one A B identical physical source',a['gradient'],b['gradient'],0.)
                gate('complete connected energy subtraction',w,e2-ea-eb+e0,OBS_TOL)
                if qualified:gate('matched full Hessian subtraction',curvature,np.asarray(pair['ground_hessian'])-np.diag([a['ground_hessian'][0,0],b['ground_hessian'][0,0]]),OBS_TOL)
                gate('fixed-chart reaction vertex',-(v2[0]+v2[1]),np.tile([kappa*(math.sin(theta[x])+math.sin(theta[y]-phi)) for x,y in PAIRS],2))
                sourcework={'static_holding_ground_shift_AB':e2-float(data['tagged_base_eigenvalues'][s,0]),
                    'static_holding_ground_shift_A':ea-float(data['reference_base_eigenvalues'][s,0]),
                    'static_holding_ground_shift_B':eb-float(data['reference_base_eigenvalues'][s,0]),
                    'held_ground_well_energy_AB':pair['energy_inventory_without_common_ARpop']['holding_wells'],
                    'held_ground_well_energy_A':a['energy_inventory_without_common_ARpop']['holding_wells'],
                    'held_ground_well_energy_B':b['energy_inventory_without_common_ARpop']['holding_wells'],
                    'translation_work_vertices_connected':g,
                    'scope':'static energy changes and literal work vertices only; no actual holding/switch/insertion trajectory or apparatus material work executed'}
                row={'group':name,'strength_index':k,'kappa':kappa,'kappa_rational':KAPPA_RATIONAL[k],'B_center_index':m,'phiA':0.,'phiB':phi,'s':s,'u_lambda_s':u,
                    'vacuum':v0,'A_reference':a,'B_reference':b,'AB_ground':pair,'connected_W':w,'connected_gradient':g,
                    'connected_torque':torque,'connected_arc_force':torque/RADIUS,'fixed_chart_connected_reaction_torque':-float(torque.sum()),
                    'connected_direct_contact':contact,'connected_spectral_susceptibility':susceptibility,'connected_ground_hessian':curvature,
                    'connected_response_status':'RESOLVED_FINITE_CONNECTED_GROUND_RESPONSE' if qualified else 'GROUND_GAP_UNQUALIFIED',
                    'source_work_inventory':sourcework,'trap_center_shortest_arc':RADIUS*min(phi,2*math.pi-phi),
                    'radial_derivative_status':'NOT_DEFINED_AT_CENTER_CUSP' if m in (0,8) else 'ORIENTED_TRANSLATION_REPORTED_NO_BODY_CENTER_IDENTIFICATION',
                    'constant_common_ARpop_cancels':True,'input_map_sha256':input_id()}
                for sec,target in (('A',aa),('B',ba),('AB',pa)):
                    for field,array in target.items():arrays['s%d_%s_%s'%(s,sec,field)]=array
                arrays['s%d_vacuum_matrix'%s]=vm;arrays['s%d_vacuum_ground'%s]=vg
                group.append(row)
            for row in group:
                base=group[0];row['loading_difference_W']=row['connected_W']-base['connected_W'];row['loading_difference_gradient']=np.asarray(row['connected_gradient'])-np.asarray(base['connected_gradient'])
                row['loading_difference_torque']=np.asarray(row['connected_torque'])-np.asarray(base['connected_torque']);row['loading_difference_arc_force']=np.asarray(row['connected_arc_force'])-np.asarray(base['connected_arc_force'])
                row['loading_difference_ground_hessian']=np.asarray(row['connected_ground_hessian'])-np.asarray(base['connected_ground_hessian']) if row['connected_ground_hessian'] is not None and base['connected_ground_hessian'] is not None else None
            full=np.array([[group[int(s)]['AB_ground']['ground_energy_without_common_ARpop'],group[int(s)]['A_reference']['ground_energy_without_common_ARpop'],group[int(s)]['B_reference']['ground_energy_without_common_ARpop'],group[int(s)]['vacuum']['ground_energy_without_common_ARpop']] for s in load])
            absolute=np.array([full+ar*pop[:,None] for ar in ARS]);arrays['absolute_ground_energies_AR_q_AB_A_B_0']=absolute
            connected=absolute[:,:,0]-absolute[:,:,1]-absolute[:,:,2]+absolute[:,:,3]
            gate('all 256 q and four absolute AR branch cancellations',connected,np.tile([group[int(s)]['connected_W'] for s in load],(4,1)),OBS_TOL)
            for v in (1,2,3,5,6,7):
                lower=np.flatnonzero(bits[v]==0);upper=lower+(1<<v)
                gate('nonendpoint record source-null loading '+str(v),load[upper],load[lower],0.)
                gate('formed clock scalar generator difference '+str(v),absolute[:,upper]-absolute[:,lower],
                    np.broadcast_to(np.array(ARS)[:,None,None],(4,128,4)),OBS_TOL)
            arrays.update(global_cycle_nodes=np.array(CYCLE),theta_global=theta,global_record_bits=bits,record_loading_s=load,record_population=pop,
                ordered_tagged_pairs=np.array(PAIRS),AR_branches=np.array(ARS))
            filename=name+'.npz';nh=commit_npz(CP/filename,**arrays)
            record={'group':name,'strength_index':k,'B_center_index':m,'rows':group,'eigensystems_file':filename,'eigensystems_sha256':nh,
                'absolute_energy_order':['AB','A','B','vacuum'],'all_global_record_words':list(range(256)),'AR_rational':AR_RATIONAL,
                'input_map_sha256':input_id(),'checks':CHECKS[before:]}
            jf=name+'.json';commit(CP/jf,record,'row_saved');record['row_file']=jf;groups.append(record);rows.extend(group)
            print(json.dumps({'group':name,'rows':3,'failed':sum(not c['passed'] for c in CHECKS[before:])}),flush=True)
    exact('full144 frozen ordered census',[(r['strength_index'],r['B_center_index'],r['s']) for r in rows]==[(k,m,s) for k in range(3) for m in range(16) for s in range(3)])
    exact('48 committed holding groups',len(groups)==48)
    recheck();failed=sum(not c['passed'] for c in CHECKS);status='QUALIFIED_CONDITIONAL_STATIC_HOLDING_ARITHMETIC' if failed==0 else 'ARITHMETIC_FAILED'
    result={'status':status,'PID':os.getpid(),'passed':len(CHECKS)-failed,'failed':failed,'checks':CHECKS,'input_sha256':INPUTS,'manifest_sha256':mh,
        'groups':groups,'rows':rows,'group_count':48,'row_count':144,'AR_rational':AR_RATIONAL,'global_record_word_count':256,
        'elapsed_seconds':time.monotonic()-started,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'fixed declared C8 chart and ideal cosine holding sources; finite conserved-q ground comparison, not actual formed holding history, metric/gravity or a physical source calibration'}
    raw=write_json(RESULT,result);canonical=hashlib.sha256(blob(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':canonical})
    lines=['# Fixed-chart C8 two-body holding V001','',status+'. Arithmetic %d/%d; failed%d.'%(result['passed'],len(CHECKS),failed),'',
        'All144 cells: three strengths, sixteen centers, three endpoint loadings. All absolute q/AR energies and full eigensystems/contacts are retained in lossless NPZ bundles. Native direct/exclusion interaction remains in s0. No force sign selects a row.','',
        '| Group | kappa | B center/pi | s | W | torque A | torque B | loading delta W | loading delta torque B | mean pair arc | localization A | localization B |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        pair=row['AB_ground']['localization'];sites=pair['site_readouts'];lines.append('| data %s_s%d | %.6g | %d/8 | %d | %+.12g | %+.12g | %+.12g | %+.12g | %+.12g | %.12g | %.12g | %.12g |'%(row['group'],row['s'],row['kappa'],row['B_center_index'],row['s'],row['connected_W'],row['connected_torque'][0],row['connected_torque'][1],row['loading_difference_W'],row['loading_difference_torque'][1],pair['pair_readout']['mean_shortest_arc_distance'],sites[0]['circular_concentration'],sites[1]['circular_concentration']))
    lines+=['','| Reference group | kappa | B center/pi | s | vacuum | A | B | AB | response status |','|---|---:|---:|---:|---:|---:|---:|---:|---|']
    for row in rows:lines.append('| reference %s_s%d | %.6g | %d/8 | %d | %.12g | %.12g | %.12g | %.12g | %s |'%(row['group'],row['s'],row['kappa'],row['B_center_index'],row['s'],row['vacuum']['ground_energy_without_common_ARpop'],row['A_reference']['ground_energy_without_common_ARpop'],row['B_reference']['ground_energy_without_common_ARpop'],row['AB_ground']['ground_energy_without_common_ARpop'],row['connected_response_status']))
    lines+=['','The listed reference energies have the disclosed common ARpop removed for display only; all four physical AR branch shifts remain in each complete absolute energy in NPZ. Full contacts, spectral susceptibilities, Hessians, native/holding energy inventories and localization probabilities remain in JSON/NPZ. The fixed-chart apparatus reaction balances the two trap torques; no microscopic covariant stress is asserted.','',
        'Trap centers are declared apparatus coordinates and are not identified with actual carrier positions. These ground comparisons do not execute insertion, switching or a holding trajectory. Six nonendpoint dressed clocks retain their carrier-source commutator, but proper clock/light/source calibration and the adopted effective-theory join remain open.']
    if sum(x.startswith('| data ') for x in lines)!=144 or sum(x.startswith('| reference ') for x in lines)!=144:raise RuntimeError('report144 data/reference census')
    with REPORT.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    rh=sha(REPORT);event({'event':'report_saved','sha256':rh,'data_rows':144,'reference_rows':144})
    recheck();receipt={'status':status,'PID':os.getpid(),'input_sha256':INPUTS,'checkpoint_sha256':COMMITS,'result_raw_sha256':raw,
        'result_canonical_sha256':canonical,'report_sha256':rh,'passed':result['passed'],'failed':failed,'journal_prefix_sha256':sha(CP/'journal.jsonl'),
        'elapsed_seconds':time.monotonic()-started,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    rr=write_json(RECEIPT,receipt);event({'event':'receipt_saved','sha256':rr});print(json.dumps({'status':status,'passed':result['passed'],'failed':failed,'raw_sha256':raw,'receipt_sha256':rr,'elapsed_seconds':receipt['elapsed_seconds']}),flush=True)
    return 0 if failed==0 else 3

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        info={'status':'EXECUTION_ERROR_PRESERVED','PID':os.getpid(),'error_type':type(error).__name__,'error':str(error),
            'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'committed_checkpoint_sha256':COMMITS}
        if not ERROR.exists():write_json(ERROR,info)
        if STARTED:event({'event':'error','sha256':sha(ERROR),'error_type':type(error).__name__})
        print(str(error),file=sys.stderr);sys.exit(3)
