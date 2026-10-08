#!/usr/bin/env python3
"""NEW saved finite-M Kubo-query third cumulant; no producer/H/RNG imports."""
from pathlib import Path
import hashlib
import json
import math
import os
import sys
import time
import traceback
import numpy as np

J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME = 'LOCAL_RECORD_FEEDBACK_3D_KUBO_QUERY_SOURCE_RECIPROCITY_V001'
JOINT = 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
QUERY = 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001'
PULL = 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J / (NAME + '.md')
PROTOCOL_SHA = '8bd6d050ba303c6df62977eeee30563172186f148370e229cd96d7fa8fb6faeb'
PINS = {'local_record_feedback_3d_pair_coordination_response_v001.py': '0fdfd2ad3d20cd7e72a2b4e5055bfd3e422a706f85100ddfb6204f1f0f0212fb', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001.md': 'e862125ece9b312e51802a4f6fe46128088a27f4077d62ba3f311db4cc8be6c7', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json': '74042b5f40401085c151b10b4e32cda5257ca09c86a831f1ef98965abf4649a8', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.md': '687e4643a8268b103f7e3e6a49b831deae0d5191c82050299386c0e159d3a513', 'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RECEIPT.json': '36de22839fba41a440f78d14ef24bb1930e2c1cebe0e9a9f8e1220bbc47a81c8', 'local_record_feedback_3d_query_response_recovery_v001.py': '618a557ca85d7bcd9d4eb9d0a1d3090cfc935e85899548383aa85c1c9b6ee358', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001.md': '784888d9d6ab11d462e40c402fecf86bdda4894b2e23202d021ffa852707abf1', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RESULT.json': '679c40e69cca152498af8af9763467467ad48315286bf150a45f813dce614b0a', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RESULT.md': '64860630cf647f2abb069ff5982ec01d0fb7d184d46e8edb48148054c68e0266', 'LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001_RECEIPT.json': '22207c521d03eb59b1edc1d3a3505c186279729568da1ff3de9ae48aaa5d8217', 'local_record_feedback_3d_coulomb_pullback_v001.py': 'b50da4fcde6d758cd941248757cae398be816af9423b133b489a9cc253c64e36', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001.md': '6bf9dd0fcf1fcc865aed06581c93220ec6fd9682b3ae2f8b25db5f9f9818a7ee', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RESULT.json': 'a0ed403a7bbd41ed460605c568a8b57260897d31e0e2218286b649c83c1871d5', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RESULT.md': 'fe6fd129e8948e5208597d8bcf1fff2c4ea98072681cc21456c22477eee6d269', 'LOCAL_RECORD_FEEDBACK_3D_COULOMB_PULLBACK_V001_RECEIPT.json': 'c1888849fc79daf6ff32c90db2fa558947e204fc2a3d5d98ef42c95e8c6a122c'}
PARENTS = [(JOINT, 'local_record_feedback_3d_pair_coordination_response_v001', 180914),
           (QUERY, 'local_record_feedback_3d_query_response_recovery_v001', 364),
           (PULL, 'local_record_feedback_3d_coulomb_pullback_v001', 200)]
PCP = J / (PARENTS[0][1] + '_checkpoints')
CP = J / 'local_record_feedback_3d_kubo_query_source_reciprocity_v001_checkpoints'
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
    require(len(PINS) == 15, 'all15 direct pins')
    for name, wanted in PINS.items(): track(J / name, wanted)
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


def blocks_from_traces(b, q):
    require(b.shape[1:] == (4,) and q.shape == (len(b), 14) and len(b) in (1024, 4096) and np.isfinite(b).all() and np.isfinite(q).all(), 'paired finite trace shapes')
    r = q @ V_A
    values = {'b': b, 'q': q, 'r': r, 'bb': b[:, :, None] * b[:, None, :].conj(),
              'br': b * r[:, None], 'bc_r': b.conj() * r[:, None],
              'bbr': b[:, :, None] * b[:, None, :].conj() * r[:, None, None]}
    return {key: value.reshape(len(b)//32, 32, *value.shape[1:]).mean(axis=1) for key, value in values.items()}


def calculate(raw, beta):
    b, r = raw['b'], raw['r']; bb = raw['bb']
    covariance = bb - b[:, None] * b[None, :].conj()
    cumulant = raw['bbr'] - bb*r - raw['br'][:, None]*b[None, :].conj() - b[:, None]*raw['bc_r'][None, :] + 2*b[:, None]*b[None, :].conj()*r
    K = 4*beta*P @ covariance @ P
    derivative = 4*beta**2*math.sqrt(27)*P @ cumulant @ P
    return {'mean_b': b, 'mean_r': r, 'connected_b_covariance': covariance, 'centered_b_bstar_r_cumulant': cumulant,
            'K_A_cell_normalized': K, 'dK_A_da_clamped': derivative,
            'K_equal_port_allnode_normalized': 2*K, 'dK_equal_port_allnode_da_clamped': 2*derivative,
            'trace_K_A': np.trace(K), 'trace_dK_A_da': np.trace(derivative),
            'trace_K_equal_port_allnode': 2*np.trace(K), 'trace_dK_equal_port_allnode_da': 2*np.trace(derivative)}


def summarize(label, b, q, beta, query, pull, old):
    blocks = blocks_from_traces(b, q); count = len(blocks['b']); require(count == query['block_count'], 'block count ' + label)
    for new, prior in [('b','n'), ('bb','nn'), ('q','q')]: close(label+'_saved_block_'+new, blocks[new], unpack(query['raw_block_sufficient_sums'][prior])/32)
    close(label+'_raw_k0_imaginary', np.r_[b.imag.ravel(), q.imag.ravel()], np.zeros(b.size+q.size))
    raw = {key: value.mean(axis=0) for key, value in blocks.items()}; central = calculate(raw, beta)
    replicas = [calculate({key: (count*value.mean(axis=0)-value[i])/(count-1) for key,value in blocks.items()}, beta) for i in range(count)]
    errors = {}
    for key in central:
        a = np.asarray([rep[key] for rep in replicas])
        errors[key] = {part+'_se': np.sqrt((count-1)/count*((getattr(a,part)-getattr(a,part).mean(axis=0))**2).sum(axis=0)) for part in ('real','imag')}
    bc, rc = b-b.mean(axis=0), q @ V_A - (q @ V_A).mean()
    direct_cov = np.einsum('ni,nj->ij',bc,bc.conj())/len(b)
    direct_cum = np.einsum('ni,nj,n->ij',bc,bc.conj(),rc)/len(b)
    xi = -2*b @ P; xc = xi-xi.mean(axis=0)
    close(label+'_raw_vs_direct_centered_cov',central['connected_b_covariance'],direct_cov)
    close(label+'_raw_vs_direct_centered_third',central['centered_b_bstar_r_cumulant'],direct_cum)
    close(label+'_parent_S_zero',central['connected_b_covariance'],unpack(old['estimates']['S_zero'])[0])
    close(label+'_independent_Xi_K',central['K_A_cell_normalized'],beta*np.einsum('ni,nj->ij',xc,xc.conj())/len(b))
    close(label+'_independent_Xi_derivative',central['dK_A_da_clamped'],beta**2*math.sqrt(27)*np.einsum('ni,nj,n->ij',xc,xc.conj(),rc)/len(b))
    mean_D = 1+raw['r']/(2*math.sqrt(27))
    close(label+'_mean_D_old',mean_D,old['estimates']['scalars'][1])
    close(label+'_mean_D_pullback',mean_D,unpack(pull['values']['mean_D_density']))
    for key in ('K_A_cell_normalized','dK_A_da_clamped'):
        matrix = central[key]
        close(label+'_'+key+'_Hermitian',matrix,matrix.T.conj())
        close(label+'_'+key+'_P',P@matrix@P,matrix)
        close(label+'_'+key+'_query_null',matrix.sum(axis=1),np.zeros(4))
        close(label+'_'+key+'_k0_imaginary',matrix.imag,np.zeros((4,4)))
    close(label+'_K_allnode_factor2',central['K_equal_port_allnode_normalized'],2*central['K_A_cell_normalized'])
    close(label+'_derivative_allnode_factor2',central['dK_equal_port_allnode_da_clamped'],2*central['dK_A_da_clamped'])
    close(label+'_trace_K_direct',central['trace_K_A'],4*beta*np.trace(P@direct_cov@P))
    close(label+'_trace_derivative_direct',central['trace_dK_A_da'],4*beta**2*math.sqrt(27)*np.trace(P@direct_cum@P))
    return {'id':label,'beta':beta,'block_count':count,'block_measurements':32,'parent_status':query['parent_status'],
            'values':{key:pack(value) for key,value in central.items()},
            'component_errors':{key:{part:pack(value) for part,value in error.items()} for key,error in errors.items()},
            'raw_block_sufficient_sums':{key:pack(32*value) for key,value in blocks.items()},
            'normalization':'K_A_PER_A_CELL_MODE__EQUAL_PORT_ALLNODE_SEPARATE_FACTOR2',
            'source_query_scope':'FIXED_NATIVE_PORT_QUERY_AND_OFFSET_COULOMB_FIRST_JET_ONLY',
            'no_new_significance_inverse_metric_or_continuum_claim':True}


def format_report(rows):
    lines=['# Saved Kubo-query/source reciprocity V001','',
           'Finite-M k0 susceptibility and its clamped source derivative, with full correlated block errors and unchanged parent status. K_A is per A-cell normalized mode; the separately saved equal-port all-node convention is exactly2K_A.', '',
           '| Dataset | trace K_A Re +/- SE | trace derivative_a K_A Re +/- SE | Parent status |','|---|---|---|---|']
    for row in rows:
        val,err=row['values'],row['component_errors']; a=unpack(val['trace_K_A']); b=unpack(val['trace_dK_A_da'])
        lines.append(f"| {row['id']} | {a.real:.10g} +/- {err['trace_K_A']['real_se']:.3g} | {b.real:.10g} +/- {err['trace_dK_A_da']['real_se']:.3g} | {row['parent_status']} |")
    require(sum(line.startswith('| c') for line in lines)==20,'all20 report rows')
    lines.extend(['','All full signed matrices, raw complete-block moments and real/imaginary component SE are retained. Query/operator and source remain clamped.',
                  'This finite-Trotter Duhamel derivative is distinct from equal-time covariance, SLD/QFI or a physical spatial metric. No empirical inverse, new mixing/significance gate, proper-volume/light/matter binding, Ward identity or gravity completion follows.',''])
    return '\n'.join(lines)


def main():
    global CREATED,ACTIVE
    require(sys.argv[1:]==['--execute'],'exact --execute'); require(not any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT)),'reserved absence')
    inputs,joint,query,pull,old=authenticate(); CP.mkdir(); CREATED=True
    save('manifest.json',{'input_sha256':inputs,'pid':os.getpid(),'mode':[0,0,0],'source_direction':V_A.tolist(),'all20_datasets':True})
    event('started',input_sha256=inputs,manifest_sha256=STAGES['manifest.json'])
    rows, groups=[],{}
    for prior in joint['chains']:
        label=prior['id']; ACTIVE={'dataset':label,'phase':'SAVED_PAIRED_TRACE_KUBO_CUMULANT'}; ref=prior['checkpoints'][-1]
        with np.load(PCP/ref['bundle'],allow_pickle=False) as arrays:
            b=arrays['mean_z'][:,0].copy(); q=arrays['bar_Q_every_production_measurement'][:,0].copy()
        require(b.shape==(1024,4) and q.shape==(1024,14),'fixed1024 trace census')
        row=summarize(label,b,q,prior['beta'],query[label],pull[label],old[label]); rows.append(row); save(label+'.json',row)
        groups.setdefault(prior['condition'],[]).append((b,q,prior['beta']))
    for condition in range(4):
        label=f'condition{condition}'; ACTIVE={'dataset':label,'phase':'SAVED_RAW_POOLED_KUBO_CUMULANT'}; group=groups[condition]
        require(len(group)==4 and len({x[2] for x in group})==1,'four unchanged pooled chains')
        b=np.concatenate([x[0] for x in group]); q=np.concatenate([x[1] for x in group])
        row=summarize(label,b,q,group[0][2],query[label],pull[label],old[label]); rows.append(row); save(label+'.json',row)
    require(authenticate()[0]==inputs,'unchanged inputs before seal'); ACTIVE=None
    result={'name':NAME,'input_sha256':inputs,'rows':rows,'checks':CHECKS.copy(),'passed':len(CHECKS),'failed':0,
            'status':'SAVED_KUBO_QUERY_RECIPROCITY_PARENT_QUALIFICATIONS_UNCHANGED','elapsed_seconds':time.perf_counter()-T0}
    output=format_report(rows); raw=exclusive(RESULT,result); event('result_complete',filename=RESULT.name,sha256=raw)
    with REPORT.open('x') as stream: stream.write(output); stream.flush(); os.fsync(stream.fileno())
    event('report_complete',filename=REPORT.name,sha256=sha(REPORT))
    receipt={'result_sha256':raw,'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':sha(REPORT),
             'input_sha256':inputs,'checkpoint_sha256':STAGES.copy(),'journal_prefix_sha256':sha(CP/'journal.jsonl'),
             'passed':len(CHECKS),'failed':0,'pid':os.getpid(),'status':result['status'],'elapsed_seconds':time.perf_counter()-T0}
    digest=exclusive(RECEIPT,receipt); event('receipt_complete',filename=RECEIPT.name,sha256=digest)
    print(json.dumps({'passed':len(CHECKS),'failed':0,'result_sha256':raw,'receipt_sha256':digest}),flush=True)


if __name__=='__main__':
    T0=time.perf_counter()
    try: main()
    except Exception as error:
        if CREATED: save('ERROR.json',safe({'error':str(error),'error_type':type(error).__name__,'traceback':traceback.format_exc(),'active':ACTIVE,
                                          'checks':CHECKS.copy(),'status':'ARITHMETIC_FAILED' if isinstance(error,ArithmeticError) else 'EXECUTION_FAILED'}))
        print(traceback.format_exc(),file=sys.stderr); sys.exit(3)
