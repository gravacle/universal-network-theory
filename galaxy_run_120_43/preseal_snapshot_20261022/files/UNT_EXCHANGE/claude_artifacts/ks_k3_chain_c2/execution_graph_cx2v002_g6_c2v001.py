"""G6a (ks_k3_chain_c2 G-wave c2v001; root A175, A176): execution_graph_cx2v002 (6d59f1d0) with custody KS1, for
S1_UA_C3T only.

expected_stages and validate_graph hand every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 6d59f1d0 module
object (PRED, by path and sha), so its record is 6d59f1d0's. For S1_UA_C3T they are 6d59f1d0's code with C = KS1, whose
derive_details admits the +-3 cube (6d59f1d0 L67 derived it with 6810b7c3: 'K4 cube required'). Nothing else here reads
K: the stage grammar, the A32 hull (L35) and the row checks are unchanged. Edits: this docstring head, the custody pin
lines (KS1) plus the predecessor after them, and the first line of expected_stages and of validate_graph.

Independent expected-stage graph for the frozen calibration call grammar.

Read-only static verification of saved model outputs (DDO154 only). No solver.
This supplements the byte-pinned discovery adapter; neither alone establishes
source reconstruction. Restricted to the v006 calibration rule-mode grammar.
"""
import hashlib
import importlib.util
import math
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/custody_cx2v002_ks1_c2v001.py');SHA='ad020470aee354201ab6c68926784d75d3ebe2e16628323d49280bd2eb18aea6'   # G6a: KS1 (6810b7c3 for every other spec)
if hashlib.sha256(P.read_bytes()).hexdigest()!=SHA:raise ValueError('custody source changed')
s=importlib.util.spec_from_file_location('g6a_graph_custody_ks1',P);C=importlib.util.module_from_spec(s)
sys.modules[s.name]=C;s.loader.exec_module(C)
# G6a: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (PRED).
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/execution_graph_cx2v002.py'),
             '6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G6a: execution_graph 6d59f1d0 pin mismatch')
_psp=importlib.util.spec_from_file_location('g6a_predecessor_execution_graph_cx2v002',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)

def finite(x):
    return type(x) in (int,float) and math.isfinite(x)

def expected_stages(spec,pass_count):
    if not C.s1_c3t_spec(spec):return PRED.expected_stages(spec,pass_count)   # G6a: 6d59f1d0's own code
    C.production_scope(spec)
    if spec.get('galaxy')!='DDO154' or spec.get('admit'):raise ValueError('fresh DDO154 required')
    n=spec['numerics'];uv=n['uv_tail'];pic=n['picard']
    if uv['outer']!={'shape':'cylinder','K_big_inverse_kpc':128.0} or uv.get('source_rule')!='continuum_v001':
        raise ValueError('0530 production P128 continuum required')
    if n['column_workers']!=2 or n['brackets']['mode']!='rule' or pic['observe_every_pass'] is not True:
        raise ValueError('unsupported calibration execution grammar')
    if not finite(pic['speed_change_bound_km_s']) or pic['speed_change_bound_km_s']<=0:
        raise ValueError('finite serial observed Picard bound required')
    if type(pic['passes']) is not int or type(pass_count) is not int or not 1<=pass_count<=pic['passes']:
        raise ValueError('pass count outside plan')
    hull=n['brackets']['rule']['fs_absolute_overrides']
    if set(hull)!=set(map(str,range(72))) or any(x!=[151250000.0,317625000.0] for x in hull.values()):
        raise ValueError('full uniform A32 hull required')
    out=[('route_a','route_a'),('route_a_tail_manifest','route_a_tail_manifest'),
         ('reference','reference'),('body','body'),('offset','offset'),
         ('fs_columns_00','columns_v001'),('fs_columns_01','columns_v001'),
         ('fs_rotation','rotation_v001'),('fs_feedback','feedback_v002'),
         ('rfs_columns_00','columns_v003'),('rfs_columns_01','columns_v003')]
    for i in range(1,pass_count+1):
        out.extend([(f'le{i}_columns_00','columns_v005'),(f'le{i}_rotation','rotation_v005'),
                    (f'le{i}_column_mean','column_mean_v004')])
        if i<pass_count:out.append((f'le{i}_feedback','feedback_v004'))
    return out

def argv_value(argv,flag):
    if not isinstance(argv,list) or argv.count(flag)!=1:raise ValueError('ambiguous argument '+flag)
    i=argv.index(flag)
    if i+1==len(argv):raise ValueError('missing argument '+flag)
    return argv[i+1]

def validate_graph(*,spec,result):
    if not C.s1_c3t_spec(spec):return PRED.validate_graph(spec=spec,result=result)   # G6a: 6d59f1d0's own code
    out={'schema':'DDO154_EXECUTION_GRAPH_CX2V002','status':'TESTED','ok':False,'blockers':[],'controls':[]}
    try:
        if result.get('status')!='COMPLETED' or result.get('valid') is not True:raise ValueError('valid completed call required')
        passes=result['passes'];N=len(passes)
        expected=expected_stages(spec,N)
        stages=result['stage_records']
        if [(x.get('name'),x.get('kind')) for x in stages]!=expected:
            raise ValueError('complete stage sequence differs from independent frozen-grammar derivation')
        if any(x.get('executed') is not True or type(x.get('exit_code')) is not int or x['exit_code']!=0 for x in stages):
            raise ValueError('unexecuted or unsuccessful stage')
        if [x.get('pass') for x in passes]!=list(range(1,N+1)) or result.get('final_pass')!=N:
            raise ValueError('pass sequence/final-pass mismatch')
        details=C.derive_details(spec=spec);ids=[x['id'] for x in details['row_contract']['rows']]
        speeds=[]
        for i,p in enumerate(passes):
            rows=p.get('rows')
            if not isinstance(rows,list) or [r.get('id') for r in rows]!=ids:
                raise ValueError('pass rows must have exact ordered unique IDs')
            v=[r.get('speed_km_s') for r in rows]
            if not all(finite(x) and x>=0 for x in v):raise ValueError('invalid model row speed')
            speeds.append(v)
            if i:
                delta=max(abs(a-b) for a,b in zip(v,speeds[i-1]))
                if p.get('max_abs_change_km_s')!=delta:raise ValueError('Picard change differs from raw model rows')
                if i<N-1 and delta<=spec['numerics']['picard']['speed_change_bound_km_s']:
                    raise ValueError('driver should have stopped at earlier pass')
        if result.get('rows')!=passes[-1]['rows']:raise ValueError('final rows differ from final pass')
        if N<spec['numerics']['picard']['passes']:
            if N<2 or passes[-1]['max_abs_change_km_s']>spec['numerics']['picard']['speed_change_bound_km_s']:
                raise ValueError('unsupported early stop')
        groups={}
        for st in stages:
            if st['kind'] not in ('columns_v001','columns_v003','columns_v005'):continue
            args=st['argv'];ref={'path':argv_value(args,'--controls'),'sha256':argv_value(args,'--controls-sha256')}
            control=C.read_pin(ref);indices=control.get('radial_indices')
            if not isinstance(indices,list) or not indices or any(type(i) is not int or not 0<=i<72 for i in indices):
                raise ValueError('invalid control radial indices')
            tag=st['name'].split('_columns_')[0];groups.setdefault(tag,[]).extend(indices)
            out['controls'].append(ref)
        if any(sorted(indices)!=list(range(72)) for indices in groups.values()):
            raise ValueError('column controls do not partition the 72 columns exactly once')
        out.update(ok=True,expected_stages=expected,passes=N,point_sha256=details['point_sha256'])
    except (ValueError,KeyError,TypeError,OSError,IndexError,AttributeError) as e:out['blockers'].append(str(e))
    return out
