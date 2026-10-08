#!/usr/bin/env python3
"""NEW saved charging-strain tensors; no producer/H/RNG imports."""
from pathlib import Path
import hashlib
import json
import math
import os
import sys
import time
import traceback
import re
from fractions import Fraction
import numpy as np

J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME = 'LOCAL_RECORD_FEEDBACK_3D_SIX_STRAIN_CHARGING_STIFFNESS_V001'
JOINT = 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
QUERY = 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001'
PULL = 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = 'dc0d347056b37ed616b299b417057bcb97db20c5cfd253126abe5d418972fc77'
PINS = {'local_record_feedback_3d_pair_coordination_response_v001.py': '0fdfd2ad3d20cd7e72a2b4e5055bfd3e422a706f85100ddfb6204f1f0f0212fb', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001.md': 'e862125ece9b312e51802a4f6fe46128088a27f4077d62ba3f311db4cc8be6c7', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json': '74042b5f40401085c151b10b4e32cda5257ca09c86a831f1ef98965abf4649a8', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.md': '687e4643a8268b103f7e3e6a49b831deae0d5191c82050299386c0e159d3a513', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RECEIPT.json': '36de22839fba41a440f78d14ef24bb1930e2c1cebe0e9a9f8e1220bbc47a81c8', 'local_record_feedback_3d_query_response_recovery_v001.py': '618a557ca85d7bcd9d4eb9d0a1d3090cfc935e85899548383aa85c1c9b6ee358', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001.md': '784888d9d6ab11d462e40c402fecf86bdda4894b2e23202d021ffa852707abf1', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RESULT.json': '679c40e69cca152498af8af9763467467ad48315286bf150a45f813dce614b0a', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RESULT.md': '64860630cf647f2abb069ff5982ec01d0fb7d184d46e8edb48148054c68e0266', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RECEIPT.json': '22207c521d03eb59b1edc1d3a3505c186279729568da1ff3de9ae48aaa5d8217', 'local_record_feedback_3d_coulomb_pullback_v001.py': 'b50da4fcde6d758cd941248757cae398be816af9423b133b489a9cc253c64e36', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001.md': '6bf9dd0fcf1fcc865aed06581c93220ec6fd9682b3ae2f8b25db5f9f9818a7ee', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RESULT.json': 'a0ed403a7bbd41ed460605c568a8b57260897d31e0e2218286b649c83c1871d5', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RESULT.md': 'fe6fd129e8948e5208597d8bcf1fff2c4ea98072681cc21456c22477eee6d269', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RECEIPT.json': 'c1888849fc79daf6ff32c90db2fa558947e204fc2a3d5d98ef42c95e8c6a122c'}
CONTRACT = 'LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md'
PINS[CONTRACT] = 'cc363bf1885917a9beededadb8d49b5d898c951bd54a1e2d2ad6ce5003ebaf63'
PARENTS = [(JOINT, 'local_record_feedback_3d_pair_coordination_response_v001', 180914),
           (QUERY, 'local_record_feedback_3d_query_response_recovery_v001', 364),
           (PULL, 'local_record_feedback_3d_coulomb_pullback_v001', 200)]
PCP = J / (PARENTS[0][1] + '_checkpoints')
CP = J / 'local_record_feedback_3d_six_strain_charging_stiffness_v001_checkpoints'
RESULT, REPORT, RECEIPT = (J / (NAME + suffix) for suffix in ('_RESULT.json', '_RESULT.md', '_RECEIPT.json'))
P = np.eye(4) - np.ones((4, 4)) / 4
V_A = np.r_[np.ones(12), -1, -1] / 2
CHECKS, STAGES = [], {}
CREATED, ACTIVE = False, None


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_bytes())
def canonical(value): return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def require(passed, label):
    if not passed: raise RuntimeError('Custody: ' + label)
def unpack(value): return np.asarray(value['real']) + 1j * np.asarray(value['imag']) if isinstance(value, dict) else np.asarray(value)
def pack(value):
    a = np.asarray(value)
    return {'real': a.real.tolist(), 'imag': a.imag.tolist()} if np.iscomplexobj(a) else a.tolist()
def safe(value):
    if isinstance(value, dict): return {key: safe(v) for key, v in value.items()}
    if isinstance(value, (tuple, list)): return [safe(v) for v in value]
    if isinstance(value, (float, np.floating)) and not math.isfinite(float(value)): return {'nonfinite': repr(float(value))}
    return value


def close(label, first, second):
    error = float(np.linalg.norm(np.asarray(first) - np.asarray(second)))
    tolerance = 3e-11 * max(1, float(np.linalg.norm(np.asarray(second))))
    row = {'label': label, 'passed': math.isfinite(error) and error <= tolerance, 'residual': error, 'tolerance': tolerance}
    CHECKS.append(safe(row))
    if not row['passed']: raise ArithmeticError(label)


def exclusive(path, value):
    with path.open('xb') as stream:
        stream.write(canonical(value) + b'\n'); stream.flush(); os.fsync(stream.fileno())
    return sha(path)
def event(kind, **fields):
    with (CP / 'journal.jsonl').open('ab') as stream:
        stream.write(canonical({'event': kind, 'pid': os.getpid(), **fields}) + b'\n'); stream.flush(); os.fsync(stream.fileno())
def save(name, value):
    STAGES[name] = exclusive(CP / name, value)
    event('stage_complete', filename=name, sha256=STAGES[name])


def authenticate():
    actual, cache, parents = {}, {}, {}
    def track(path, expected=None):
        path = path.resolve(); key = os.path.relpath(path, J)
        digest = cache.setdefault(key, sha(path)) if key not in cache else cache[key]
        require(expected is None or digest == expected, 'input ' + key); actual[key] = digest
        return digest
    require(len(PINS) == 16, 'all16 direct pins')
    for name, wanted in PINS.items(): track(J / name, wanted)
    anchors = re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$', (J/CONTRACT).read_text(), re.M)
    require(len(anchors)==9, 'nine frozen physical ancestry inputs')
    for name,wanted in anchors: track(J.parent.parent/name if name.startswith('program-worktree/') else J/name,wanted)
    actual['source'], actual['protocol'] = sha(SOURCE), sha(PROTOCOL)
    require(actual['protocol'] == PROTOCOL_SHA, 'new protocol')
    for name, stem, count in PARENTS:
        parent, receipt = read(J / (name + '_RESULT.json')), read(J / (name + '_RECEIPT.json'))
        require(receipt['result_sha256'] == actual[name + '_RESULT.json'] and receipt['report_sha256'] == actual[name + '_RESULT.md'], 'raw/report ' + name)
        require(receipt['result_canonical_sha256'] == hashlib.sha256(canonical(parent)).hexdigest(), 'canonical ' + name)
        require(receipt['input_sha256'] == parent['input_sha256'] and receipt['passed'] == parent['passed'] == len(parent['checks']) == count and
                receipt['failed'] == parent['failed'] == 0 and all(c['passed'] for c in parent['checks']) and receipt['status'] == parent['status'], 'controls/status ' + name)
        directory = J / (stem + '_checkpoints'); lines = (directory / 'journal.jsonl').read_bytes().splitlines(keepends=True)
        journal = [json.loads(line) for line in lines]
        require(hashlib.sha256(b''.join(lines[:-1])).hexdigest() == receipt['journal_prefix_sha256'] and journal[-1]['event'] == 'receipt_complete' and
                journal[-1]['sha256'] == actual[name + '_RECEIPT.json'], 'journal prefix/receipt ' + name)
        track(directory / 'journal.jsonl'); commits = {(e.get('filename'), e.get('sha256')) for e in journal}
        for filename, wanted in receipt['checkpoint_sha256'].items():
            track(directory / filename, wanted); require((filename, wanted) in commits, 'checkpoint commit ' + filename)
        manifest = read(directory / 'manifest.json')
        require(manifest['input_sha256'] == receipt['input_sha256'] and any(e['event'] == 'started' and e['input_sha256'] == receipt['input_sha256'] and
                e['manifest_sha256'] == receipt['checkpoint_sha256']['manifest.json'] for e in journal), 'manifest/start ' + name)
        for filename, wanted in receipt['input_sha256'].items():
            if filename == 'core_identity_canonical_sha256':
                require(hashlib.sha256(canonical(manifest['preserved_core_identity'])).hexdigest() == wanted, 'virtual core identity'); continue
            track(J / (stem + '.py' if filename == 'source' else name + '.md' if filename == 'protocol' else filename), wanted)
        parents[name] = parent
    joint, query, pull = (parents[n] for n in (JOINT, QUERY, PULL))
    ids = [f'c{i}_{start}' for i in range(4) for start in ('I01', 'I02', 'B', 'R')]
    require([r['id'] for r in joint['chains']] == ids and len(joint['conditions']) == 4 and joint['characters'][0] == [0, 0, 0], 'joint fixed census')
    old_rows = {r['id']: r for r in joint['chains']}; old_rows.update({f"condition{r['condition']}": r for r in joint['conditions']})
    for parent in (query, pull):
        require([r['id'] for r in parent['rows']] == ids + [f'condition{i}' for i in range(4)] and
                [r['block_count'] for r in parent['rows']] == [32]*16+[128]*4 and all(r['block_measurements'] == 32 for r in parent['rows']), 'all20 raw datasets')
        require(all(r['parent_status'] == old_rows[r['id']]['status'] for r in parent['rows']), 'unchanged inherited qualifications')
    joint_receipt = read(J / (JOINT + '_RECEIPT.json'))
    for row in joint['chains']:
        ref = row['checkpoints'][-1]; meta = read(PCP / ref['metadata'])
        require(ref['metadata'] == row['id'] + '_production1024.json' and ref['bundle'] == row['id'] + '_production1024.npz' and
                meta['completed_production_sweeps'] == row['production_sweeps'] == 1024 and meta['completed_burn_sweeps'] == 64, 'terminal census')
        require(ref['metadata_sha256'] == joint_receipt['checkpoint_sha256'][ref['metadata']] and ref['bundle_sha256'] == meta['bundle_sha256'] ==
                joint_receipt['checkpoint_sha256'][ref['bundle']] and meta['input_sha256'] == joint_receipt['input_sha256'] and
                meta['configuration'] == {key: row[key] for key in ('seed', 'beta', 'epsilon', 'M', 'start')}, 'terminal seals/configuration')
    return actual, joint, {r['id']: r for r in query['rows']}, {r['id']: r for r in pull['rows']}, old_rows



COORDINATES = ['xx','yy','zz','yz','xz','xy']
PAIRS = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
AR_VALUES = [Fraction(1,8),Fraction(7,40),Fraction(1,4)]
BASIS = []
for i,j in [(0,0),(1,1),(2,2),(1,2),(0,2),(0,1)]:
    b=np.zeros((3,3)); b[i,j]=b[j,i]=1; BASIS.append(b)
BASIS=np.asarray(BASIS)
T_SELECTOR=np.r_[np.ones(12),0,0]
Q_SELECTOR=np.r_[np.zeros(12),1,1]
UNIFORM=np.array([1.,1.,1.,0.,0.,0.])


def geometric_branch(AR):
    ar=float(AR); ed=em=.5; g=.25; er=2*ar; r=2.5; schur=er-4*g*g/r
    weights={'mutual':(em*er-g*g)/(ed*r*schur),'port_record':g/(r*schur),
             'port_return':(er-g)/(r*schur),'record_return':(r-4*g)/(r*schur)}
    require(schur>0 and min(weights.values())>=0, 'fixed passive branch')
    E=np.zeros((5,5));E[:4,:4]=ed*np.eye(4)+em*np.ones((4,4));E[:4,4]=g;E[4,:4]=g;E[4,4]=er
    U=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],dtype=float)/math.sqrt(3)
    eye=np.eye(5); branches=[]
    def add(kind,weight,normal,z):branches.append({'kind':kind,'weight':weight,'normal':normal,'incidence':z})
    for a,b in PAIRS:
        n=U[a]-U[b];n/=np.linalg.norm(n);add('mutual',weights['mutual'],n,eye[a]-eye[b])
    for a in range(4):
        add('port_record',weights['port_record'],U[a],eye[a]-eye[4])
        add('port_return',weights['port_return'],U[a],eye[a])
    for n in np.eye(3):add('record_return',weights['record_return']/3,n,eye[4])
    require(len(branches)==17,'all seventeen physical branches')
    C=np.zeros((5,5));CA=np.zeros((6,5,5));CAB=np.zeros((6,6,5,5))
    for branch in branches:
        n,z,w=branch['normal'],branch['incidence'],branch['weight']; zz=np.outer(z,z)
        f=np.array([np.trace(A)-2*n@A@n for A in BASIS]);C+=w*zz;CA+=w*f[:,None,None]*zz
        for a,A in enumerate(BASIS):
            for b,B in enumerate(BASIS):
                second=f[a]*f[b]-np.trace(A@B)+3*n@(A@B+B@A)@n-4*(n@A@n)*(n@B@n)
                CAB[a,b]+=w*second*zz
    close(f'AR{AR}_CE',C@E,np.eye(5));close(f'AR{AR}_uniform_C',CA[:3].sum(axis=0),C)
    close(f'AR{AR}_uniform_Caa',CAB[:3,:3].sum(axis=(0,1)),np.zeros((5,5)))
    G=np.array([-E@A@E/2 for A in CA]);L=np.empty((6,6,5,5))
    for a in range(6):
        for b in range(6):L[a,b]=(E@CA[a]@E@CA[b]@E+E@CA[b]@E@CA[a]@E-E@CAB[a,b]@E)/2
    mu=ed*ed*weights['mutual'];expected_mu=[Fraction(1,12),Fraction(9,100),Fraction(3,32)][AR_VALUES.index(AR)]
    close(f'AR{AR}_mu',mu,float(expected_mu));source=np.zeros((6,14));identity=np.zeros(6)
    groups=[{(0,1),(2,3)},{(0,2),(1,3)},{(0,3),(1,2)}]
    for a,A in enumerate(BASIS):
        tau=np.trace(A);pair=-tau*np.ones(6)/6
        for p,(i,j) in enumerate(PAIRS):
            if a<3:pair[p]+=mu*((1 if (i,j) in groups[a] else 0)-1/3)
        if a==3:pair[PAIRS.index((0,1))]+=2*mu/3;pair[PAIRS.index((2,3))]-=2*mu/3
        if a==4:pair[PAIRS.index((0,2))]+=2*mu/3;pair[PAIRS.index((1,3))]-=2*mu/3
        if a==5:pair[PAIRS.index((0,3))]+=2*mu/3;pair[PAIRS.index((1,2))]-=2*mu/3
        source[a,:6]=source[a,6:12]=pair;source[a,12:]=tau/6;identity[a]=-tau*(1+ar)/3-tau/3
    close(f'AR{AR}_source_uniform',UNIFORM@source,-V_A)
    close(f'AR{AR}_H_a_coeff',G[:3].sum(axis=0),-E/2)
    close(f'AR{AR}_H_aa_coeff',L[:3,:3].sum(axis=(0,1)),E)
    close(f'AR{AR}_contact_coordinate_symmetric',L,L.swapaxes(0,1))
    for word in range(16):
        z=np.array([1-2*((word>>a)&1) for a in range(4)]);x=np.r_[z,1];y=np.array([z[a]*z[b] for a,b in PAIRS]);c=-z.sum()/2
        actual=np.einsum('i,aij,j->a',x,G,x)
        declared=source[:,:6]@y+source[:,12]*c+identity
        close(f'AR{AR}_full_first_jet_word{word}',actual,declared)
    return {'AR_fraction':str(AR),'AR':ar,'alpha':1,'qstar':1,'qR':1,'U':1,'lambda':.5,'ed':ed,'em':em,'gcap':g,'eR':er,
            'Schur':schur,'weights':weights,'mu':mu,'branches':[{k:pack(v) if isinstance(v,np.ndarray) else v for k,v in b.items()} for b in branches],
            'E5':E,'C0':C,'C_A':CA,'C_AB':CAB,'G_A':G,'L_AB':L,'source_rows':source,'identity_density':identity}


def charge_moments(raw):
    spins=-2*raw['n']/math.sqrt(27);M=np.tile(np.eye(5,dtype=complex),(2,1,1))
    M[:,:4,4]=spins;M[:,4,:4]=spins
    for p,(a,b) in enumerate(PAIRS):M[:,a,b]=M[:,b,a]=raw['local_pair_mean'][:,p]
    return M,spins


def calculate(raw,beta,model,label):
    q=raw['q'];chi=beta*(raw['qq']-np.outer(q,q.conj()));mom,spins=charge_moments(raw)
    source=model['source_rows'];contact_star=np.einsum('abij,sij->sab',model['L_AB'],mom)
    contact=contact_star.mean(axis=0);sus=source@chi@source.T.conj()/2;curvature=contact-sus
    stress=source@q/(2*math.sqrt(27))+model['identity_density'];stress_star=np.einsum('aij,sij->sa',model['G_A'],mom)
    D=raw['local_c2_mean'].mean()-(q[12]+q[13])/(4*math.sqrt(27));Jmean=D+model['AR']+1
    scalar=.25*(T_SELECTOR@chi@T_SELECTOR-2*T_SELECTOR@chi@Q_SELECTOR+Q_SELECTOR@chi@Q_SELECTOR)/2
    uniform_contact=UNIFORM@contact@UNIFORM;uniform_sus=UNIFORM@sus@UNIFORM
    close(label+'_complete_stress_means',stress,stress_star.mean(axis=0))
    close(label+'_uniform_contact',uniform_contact,2*Jmean)
    close(label+'_uniform_chiDD',uniform_sus,scalar)
    close(label+'_uniform_curvature',UNIFORM@curvature@UNIFORM,2*Jmean-scalar)
    values={'mean_port_spin':spins,'mean_pair_A':raw['local_pair_mean'][0],'mean_pair_B':raw['local_pair_mean'][1],
            'mean_D_density':D,'mean_Jcap_density':Jmean,'mean_stress_density':stress,'contact_A_density':contact_star[0],
            'contact_B_density':contact_star[1],'contact_density':contact,'susceptibility_density':sus,'curvature_density':curvature,
            'chi14':chi,'uniform_contact_density':uniform_contact,'uniform_susceptibility_density':uniform_sus,
            'uniform_curvature_density':UNIFORM@curvature@UNIFORM,'trace_curvature_density':np.trace(curvature)}
    for name,matrix in [('contact',contact),('susceptibility',sus),('curvature',curvature)]:
        values[name+'_descriptive_eigenvalues']=np.linalg.eigvalsh((matrix+matrix.T.conj())/2)
    return values


def dataset(label,beta,query,pull,old,models):
    keys=['n','q','qq','local_pair_mean','local_c2_mean']
    blocks={k:unpack(query['raw_block_sufficient_sums'][k])/32 for k in keys};count=query['block_count']
    require(all(len(v)==count for v in blocks.values()) and count in (32,128),'complete block census')
    raw={k:v.mean(axis=0) for k,v in blocks.items()}
    close(label+'_Q14_mean',raw['q'],unpack(old['joint_estimates']['mean_Q'])[0])
    close(label+'_pair_mean',raw['local_pair_mean'],unpack(old['joint_estimates']['local_pair_mean']))
    close(label+'_spin_mean',np.tile(-2*raw['n']/math.sqrt(27),(2,1)),unpack(old['joint_estimates']['local_spin_mean']))
    require(all(np.isfinite(v).all() for v in blocks.values()),'finite raw blocks')
    branch_rows=[]
    for model in models:
        tag=label+'_AR'+model['AR_fraction'];ACTIVE['branch']=model['AR_fraction']
        values=calculate(raw,beta,model,tag+'_central')
        close(tag+'_parent_chi14',values['chi14'],unpack(old['joint_estimates']['chi_joint'])[0])
        close(tag+'_D_pullback',values['mean_D_density'],unpack(pull['values']['mean_D_density']))
        close(tag+'_chiDD_pullback',values['uniform_susceptibility_density'],unpack(pull['values']['chi_DD_density']))
        close(tag+'_K_D_plus_identity',values['uniform_curvature_density'],unpack(pull['values']['K_D_clamped_nonidentity_canonical'])+2*(model['AR']+1))
        for k in ('contact_A_density','contact_B_density','contact_density','susceptibility_density','curvature_density'):
            close(tag+'_'+k+'_Hermitian',values[k],values[k].T.conj());close(tag+'_'+k+'_k0_imaginary',values[k].imag,np.zeros((6,6)))
        replicas=[calculate({k:(count*v.mean(axis=0)-v[i])/(count-1) for k,v in blocks.items()},beta,model,tag+f'_replica{i}') for i in range(count)]
        errors={}
        for k in values:
            a=np.array([rep[k] for rep in replicas]);errors[k]={}
            for part in ('real','imag'):
                aa=getattr(a,part);errors[k][part+'_se']=pack(np.sqrt((count-1)/count*((aa-aa.mean(axis=0))**2).sum(axis=0)))
        branch_rows.append({'AR_fraction':model['AR_fraction'],'values':{k:pack(v) for k,v in values.items()},'component_errors':errors,
                            'parent_status':query['parent_status'],'no_full_mechanical_gravity_stability_claim':True})
        ACTIVE['completed_active_branch_rows']=branch_rows.copy()
    return {'id':label,'beta':beta,'block_count':count,'block_measurements':32,'parent_status':query['parent_status'],
            'raw_block_sufficient_sums':{k:pack(32*v) for k,v in blocks.items()},'branches':branch_rows,'coordinate_order':COORDINATES,
            'scope':'FIXED_Q1_CHARGING_SECTOR_LINEAR_F_CHART_FINITE_M_FIXED_BETA_ONLY'}


def format_report(rows):
    lines=['# Saved six-strain charging curvature V001','',
      'Actual linear symmetric plate strain, fixedq1, native-vertex density. All reference AR+alpha terms and all branches retained. Inherited qualifications remain.','',
      '| Dataset | AR | trace curvature ± SE | descriptive eigenvalue min/max | Parent status |','|---|---|---|---|---|']
    for row in rows:
        for branch in row['branches']:
            val=branch['values'];trace=unpack(val['trace_curvature_density']).real;se=branch['component_errors']['trace_curvature_density']['real_se'];ev=val['curvature_descriptive_eigenvalues']
            lines.append(f"| {row['id']} | {branch['AR_fraction']} | {trace:.10g} ± {se:.3g} | {ev[0]:.9g} / {ev[-1]:.9g} | {row['parent_status']} |")
    require(sum(line.startswith('| c') for line in lines)==60,'all sixty branch/dataset report rows')
    lines.extend(['','Full signed A/B and averaged contact, susceptibility, curvature, complete stress, coefficient arrays, raw blocks and correlated component/eigenvalue SE are saved in JSON.',
      'Eigenvalues are descriptive Hermitian-part quantities, with raw tensors preserved. These finite-M canonical charging-sector curvatures are not full mechanical stiffness, material equilibrium, a physical metric, gravity or expansion. Other material/code/support/rest source terms remain absent and unknown.',''])
    return '\n'.join(lines)


def main():
    global CREATED,ACTIVE
    require(sys.argv[1:]==['--execute'],'exact --execute');require(not any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT)),'reserved absence')
    inputs,joint,query,pull,old=authenticate();CP.mkdir();CREATED=True
    save('manifest.json',{'input_sha256':inputs,'pid':os.getpid(),'coordinate_order':COORDINATES,'AR_fractions':[str(v) for v in AR_VALUES],'all20_datasets':True})
    event('started',input_sha256=inputs,manifest_sha256=STAGES['manifest.json'])
    ACTIVE={'dataset':'geometric coefficient controls','branch':None};models=[geometric_branch(a) for a in AR_VALUES]
    packed_models=[{k:pack(v) if isinstance(v,np.ndarray) else v for k,v in m.items()} for m in models]
    save('geometric_coefficients.json',{'models':packed_models,'checks':CHECKS.copy()})
    rows=[]
    ids=[r['id'] for r in joint['chains']]+[f'condition{i}' for i in range(4)]
    for label in ids:
        ACTIVE={'dataset':label,'branch':None,'phase':'SAVED_COMPLETE_BLOCK_STRAIN_CONTRACTION'}
        row=dataset(label,query[label]['beta'],query[label],pull[label],old[label],models);rows.append(row);save(label+'.json',row)
    require(authenticate()[0]==inputs,'unchanged inputs before seal');ACTIVE=None
    result={'name':NAME,'input_sha256':inputs,'rows':rows,'models':packed_models,'checks':CHECKS.copy(),'passed':len(CHECKS),'failed':0,
            'status':'SAVED_CHARGING_STRAIN_PARENT_QUALIFICATIONS_UNCHANGED','elapsed_seconds':time.perf_counter()-T0}
    output=format_report(rows);raw=exclusive(RESULT,result);event('result_complete',filename=RESULT.name,sha256=raw)
    with REPORT.open('x') as stream:stream.write(output);stream.flush();os.fsync(stream.fileno())
    event('report_complete',filename=REPORT.name,sha256=sha(REPORT))
    receipt={'result_sha256':raw,'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':sha(REPORT),
      'input_sha256':inputs,'checkpoint_sha256':STAGES.copy(),'journal_prefix_sha256':sha(CP/'journal.jsonl'),'passed':len(CHECKS),'failed':0,
      'pid':os.getpid(),'status':result['status'],'elapsed_seconds':time.perf_counter()-T0}
    digest=exclusive(RECEIPT,receipt);event('receipt_complete',filename=RECEIPT.name,sha256=digest)
    print(json.dumps({'passed':len(CHECKS),'failed':0,'result_sha256':raw,'receipt_sha256':digest}),flush=True)


if __name__=='__main__':
    T0=time.perf_counter()
    try:main()
    except Exception as error:
        if CREATED:save('ERROR.json',safe({'error':str(error),'error_type':type(error).__name__,'traceback':traceback.format_exc(),'active':ACTIVE,
          'checks':CHECKS.copy(),'status':'ARITHMETIC_FAILED' if isinstance(error,ArithmeticError) else 'EXECUTION_FAILED'}))
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
