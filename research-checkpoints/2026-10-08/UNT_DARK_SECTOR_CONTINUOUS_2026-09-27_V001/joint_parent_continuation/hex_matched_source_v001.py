#!/usr/bin/env python3
"""NEW sealed-data Fraction assembly only; no scientific producer is imported."""
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import os
import resource
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME = 'HEX_MATCHED_SOURCE_V001'
SOURCE = Path(__file__).resolve()
PROTOCOL = J/(NAME+'.md')
RESULT = J/(NAME+'_RESULT.json')
REPORT = J/(NAME+'_RESULT.md')
RECEIPT = J/(NAME+'_RECEIPT.json')
CP = J/'hex_matched_source_v001_checkpoints'
JS = 'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001'
VS = 'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001'
JOINT = 'BS10_RECORD_FEEDBACK_HEX_JOINT_V001'
Q63 = 'BS10_RECORD_FEEDBACK_HEX_SOURCE_V001'
VAC = 'BS10_RECORD_FEEDBACK_HEX_VACUUM_V001'
BASE = 'BS10_RECORD_FEEDBACK_HEX_FINITE_V001'
ALPHA = Fraction(1,20)
ATTEMPT_CREATED = False
STAGES = {}
INPUTS = {
    'bs10_record_feedback_hex_joint_source_v001.py':'1ef4287d6f654aede296d8f1681e917f6d21830307d596baf80b800a90163678',
    'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001.md':'8d8d2f4695e3834786e48bd462eb0c9690ea57190febff2ad53bca3e281593a9',
    'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001_RESULT.json':'2fb189f2685f5367fc535fad054c38692cbfa3e871627a34a2b18673a6d953ed',
    'BS10_RECORD_FEEDBACK_HEX_JOINT_SOURCE_V001_RECEIPT.json':'e3cfadec3a4f7b06e835ac48e26932da2722a99188b4e38e0e1600cd2dfc18d8',
    'bs10_record_feedback_hex_source_vacuum_v001.py':'3df379b5dbc0c0a4b27cc7f0ad265cdc6e673b174c83f3db0b4e597219495c5b',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001.md':'eba3c816494a4c3be13091e15803688cf604388d1fb76011e0b30c5ddb70394f',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001_RESULT.json':'48c649d26ab8a2718c0119f40976950e941d90babc4a18a6e4b36558bc29fb4c',
    'BS10_RECORD_FEEDBACK_HEX_SOURCE_VACUUM_V001_RECEIPT.json':'711f3291d0626864926ebae6fa79dcd7724b833e2c7189600f1bd9da461e9da2',
    'HELD_HEX_COMPLETE_NONUNIFORM_ADDITION_SOURCE_GATE_V001.md':'c99ceb680037c35f87d6b280c0fd11bb456f1bc798fc429175e3d9a8cc55cbdc',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def exact(value):
    value = Fraction(value)
    displays = []
    for mode in (ROUND_FLOOR,ROUND_CEILING):
        with localcontext() as context:
            context.prec,context.rounding = 20,mode
            displays.append(str(Decimal(value.numerator)/Decimal(value.denominator)))
    return {'numerator':value.numerator,'denominator':value.denominator,
            'decimal20_lower':displays[0],'decimal20_upper':displays[1]}


def frac(value):
    return Fraction(value['numerator'],value['denominator'])


def bounds(value):
    return frac(value['lower']),frac(value['upper'])


def interval(lo,hi):
    return {'lower':exact(lo),'upper':exact(hi),'width':exact(hi-lo)}


def subtract(first,second):
    a,b = bounds(first)
    c,d = bounds(second)
    return interval(a-d,b-c)


def scale(value,factor):
    a,b = bounds(value)
    return interval(factor*a,factor*b) if factor>=0 else interval(factor*b,factor*a)


def same(first,second):
    return bounds(first)==bounds(second)


def contains(outer,inner):
    a,b = bounds(outer)
    c,d = bounds(inner)
    return a<=c<=d<=b


def sign(value):
    lo,hi = bounds(value)
    return 'POSITIVE' if lo>0 else ('NEGATIVE' if hi<0 else 'ZERO_CONTAINING_OR_UNRESOLVED')


def add(checks,label,condition):
    checks.append({'label':label,'passed':bool(condition)})


def exclusive(path,obj):
    with path.open('xb') as stream:
        stream.write(canonical(obj)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    return sha(path)


def event(kind,**fields):
    row = {'event':kind,'pid':os.getpid(),'elapsed_seconds':time.perf_counter()-T0,**fields}
    with (CP/'journal.jsonl').open('ab') as stream:
        stream.write(canonical(row)+b'\n')
        stream.flush()
        os.fsync(stream.fileno())


def save(name,obj,**fields):
    digest = exclusive(CP/name,obj)
    STAGES[name] = digest
    event('stage_complete',filename=name,sha256=digest,**fields)
    return digest


def verify_map(mapping,directory,label):
    out = {}
    for name,wanted in mapping.items():
        got = sha(directory/name)
        if got != wanted:
            raise RuntimeError(label+' changed: '+name)
        out[name] = got
    return out


def packet(tag,source_name,expected):
    directory = J/(source_name[:-3]+'_checkpoints')
    result = json.loads((J/(tag+'_RESULT.json')).read_text())
    receipt = json.loads((J/(tag+'_RECEIPT.json')).read_text())
    raw_hash,receipt_hash = sha(J/(tag+'_RESULT.json')),sha(J/(tag+'_RECEIPT.json'))
    if raw_hash != expected[tag+'_RESULT.json'] or receipt_hash != expected[tag+'_RECEIPT.json']:
        raise RuntimeError('Parent anchor mismatch: '+tag)
    if receipt['result_raw_sha256'] != raw_hash or receipt['result_canonical_sha256'] != hashlib.sha256(canonical(result)).hexdigest():
        raise RuntimeError('Parent raw/canonical mismatch: '+tag)
    report_hash = sha(J/(tag+'_RESULT.md'))
    if report_hash != receipt['report_sha256']:
        raise RuntimeError('Parent current report mismatch: '+tag)
    for key,name in (('source_sha256',source_name),('protocol_sha256',tag+'.md')):
        if not(result[key]==receipt[key]==expected[name]==sha(J/name)):
            raise RuntimeError('Parent code pin mismatch: '+tag)
    key = 'authenticated_inputs' if 'authenticated_inputs' in receipt else 'input_sha256'
    if result[key] != receipt[key] or result['checkpoint_sha256'] != receipt['checkpoint_sha256']:
        raise RuntimeError('Parent input/checkpoint equality mismatch: '+tag)
    checkpoints = verify_map(receipt['checkpoint_sha256'],directory,'Parent checkpoint '+tag)
    manifest_hash = checkpoints['input_manifest.json']
    if not(result['manifest_sha256']==receipt['manifest_sha256']==manifest_hash):
        raise RuntimeError('Parent manifest equality mismatch: '+tag)
    manifest = json.loads((directory/'input_manifest.json').read_text())
    if manifest['source_sha256'] != receipt['source_sha256'] or manifest['protocol_sha256'] != receipt['protocol_sha256'] or (key in manifest and manifest[key] != receipt[key]):
        raise RuntimeError('Parent manifest payload mismatch: '+tag)
    lines = (directory/'journal.jsonl').read_bytes().splitlines(keepends=True)
    events = [json.loads(line) for line in lines]
    if not events or events[-1]['event'] != 'receipt_complete' or events[-1]['receipt_sha256'] != receipt_hash:
        raise RuntimeError('Parent final receipt commit mismatch: '+tag)
    prefix = hashlib.sha256(b''.join(lines[:-1])).hexdigest()
    if prefix != receipt['journal_prefix_sha256']:
        raise RuntimeError('Parent prefix mismatch: '+tag)
    starts = [row for row in events if row['event']=='started']
    if len(starts)!=1 or starts[0]['manifest_sha256']!=manifest_hash:
        raise RuntimeError('Parent start seal mismatch: '+tag)
    for filename,wanted in checkpoints.items():
        if sum(row.get('filename')==filename and row.get('sha256')==wanted for row in events)!=1:
            raise RuntimeError('Parent checkpoint commit mismatch: '+tag+'/'+filename)
    if result['checks_failed']!=0 or receipt['checks_failed']!=0:
        raise RuntimeError('Parent arithmetic unqualified: '+tag)
    proof = {'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'report_sha256':report_hash,
             'checkpoint_sha256':checkpoints,'journal_prefix_sha256':prefix,'authenticated_inputs':receipt[key]}
    return proof,result


def authenticate():
    direct = verify_map(INPUTS,J,'Frozen direct input')
    jsp,js = packet(JS,'bs10_record_feedback_hex_joint_source_v001.py',direct)
    vsp,vs = packet(VS,'bs10_record_feedback_hex_source_vacuum_v001.py',direct)
    ji,vi = jsp['authenticated_inputs'],vsp['authenticated_inputs']
    jp,joint = packet(JOINT,'bs10_record_feedback_hex_joint_v001.py',ji['direct_input_sha256'])
    qp,q63 = packet(Q63,'bs10_record_feedback_hex_source_v001.py',vi['direct_input_sha256'])
    if jp!=ji['joint_parent'] or qp!=ji['q63_source_parent'] or qp['authenticated_inputs']!=vi['source_parent_authenticated_inputs']:
        raise RuntimeError('Shared parent receipt/input proof mismatch')
    v0p,vacuum = packet(VAC,'bs10_record_feedback_hex_vacuum_v001.py',jp['authenticated_inputs']['direct_input_sha256'])
    bp,finite = packet(BASE,'bs10_record_feedback_hex_finite_v001.py',qp['authenticated_inputs']['direct_input_sha256'])
    if v0p!=ji['vacuum_parent'] or bp!=ji['finite_parent']:
        raise RuntimeError('Shared baseline proof mismatch')
    inherited = {}
    for label,mapping,directory in (
        ('joint0_direct',jp['authenticated_inputs']['direct_input_sha256'],J),
        ('joint0_inherited_direct',jp['authenticated_inputs']['inherited_direct_input_sha256'],J),
        ('joint0_root',jp['authenticated_inputs']['inherited_root_input_sha256'],ROOT),
        ('q63_direct',qp['authenticated_inputs']['direct_input_sha256'],J),
        ('q63_root',qp['authenticated_inputs']['inherited_input_sha256'],ROOT)):
        inherited[label]=verify_map(mapping,directory,'Inherited '+label)
    if bp['authenticated_inputs']!=inherited['q63_root'] or bp['authenticated_inputs']!=inherited['joint0_root']:
        raise RuntimeError('Original finite root-input proof mismatch')
    original = json.loads((J/'bs10_record_feedback_hex_finite_v001_checkpoints/structure.json').read_text())
    prefix,alias = original['checks'],finite['structural_checks']['checks']
    if prefix != alias[:len(prefix)] or ji['preserved_finite_stage_alias']!={'prefix_count':len(prefix),'nested_count':len(alias),'prefix_equal':True}:
        raise RuntimeError('Preserved original stage-check alias mismatch')
    if js['ground_certificate_status']!='FULL_HELD_SOURCE_GROUND_INTERVAL_CERTIFIED' or not vacuum['q63_strict_selected']:
        raise RuntimeError('Certified matched premises missing')
    a = js['finite_source_assembly']
    if not(same(a['E10_authenticated'],joint['final_ground_interval_raw']) and same(a['Ebg0_authenticated'],vacuum['global_vacuum_interval'])
           and same(a['Ebg63alpha_authenticated'],q63['new_Ealpha_interval']) and same(vs['retained_q63_source_vacuum_interval'],q63['new_Ealpha_interval'])):
        raise RuntimeError('Shared source/background reference mismatch')
    proofs = {'direct_input_sha256':direct,'joint_source_parent':jsp,'source_vacuum_parent':vsp,
              'baseline_joint_parent':jp,'retained_q63_parent':qp,'zero_source_vacuum_parent':v0p,
              'original_finite_parent':bp,'inherited_current_input_bytes':inherited,
              'preserved_original_stage_alias':ji['preserved_finite_stage_alias']}
    return proofs,js,vs,joint,vacuum,q63


def assemble(js,vs,joint,vacuum,q63):
    references = {'E10':joint['final_ground_interval_raw'],'E1alpha':js['final_ground_interval_raw'],
                  'Ebg0':vacuum['global_vacuum_interval'],'Ebg_alpha_global':vs['global_source_vacuum_interval'],
                  'Ebg_alpha_retained63':vs['retained_q63_source_vacuum_interval']}
    delta0 = subtract(references['E10'],references['Ebg0'])
    values = {'Delta0':delta0,'F1':scale(subtract(references['E10'],references['E1alpha']),2/(ALPHA*ALPHA))}
    checks = []
    add(checks,'Delta0_equals_sealed_joint_addition',same(delta0,joint['final_matched_addition_interval_raw']))
    saved = js['finite_source_assembly']
    for suffix,bg in (('global',references['Ebg_alpha_global']),('retained63',references['Ebg_alpha_retained63'])):
        addition = subtract(references['E1alpha'],bg)
        fbg = scale(subtract(references['Ebg0'],bg),2/(ALPHA*ALPHA))
        fadd = scale(subtract(delta0,addition),2/(ALPHA*ALPHA))
        d = scale(subtract(addition,delta0),2/(ALPHA*ALPHA))
        values.update({'Delta_alpha_'+suffix:addition,'Fbg_'+suffix:fbg,'Fadd_'+suffix:fadd,'Dalpha_'+suffix:d})
        add(checks,'Fadd_equals_F1_minus_Fbg_'+suffix,same(fadd,subtract(values['F1'],fbg)))
        add(checks,'Dalpha_equals_negative_Fadd_'+suffix,same(d,scale(fadd,-1)))
    for name,oldname in (('Delta0','Delta0_authenticated'),('F1','F1_raw'),('Delta_alpha_retained63','Delta_alpha63_raw'),
                         ('Fbg_retained63','Fbg63_authenticated'),('Fadd_retained63','Fadd63_raw'),('Dalpha_retained63','Dalpha63_raw')):
        add(checks,'matches_saved_joint_source_'+oldname,same(values[name],saved[oldname]))
    separation = subtract(references['Ebg_alpha_retained63'],references['Ebg_alpha_global'])
    delta_difference_loose = subtract(values['Delta_alpha_global'],values['Delta_alpha_retained63'])
    d_difference = scale(separation,2/(ALPHA*ALPHA))
    d_difference_loose = subtract(values['Dalpha_global'],values['Dalpha_retained63'])
    f_difference = scale(separation,-2/(ALPHA*ALPHA))
    f_difference_loose = subtract(values['Fadd_global'],values['Fadd_retained63'])
    add(checks,'independent_addition_difference_encloses_shared_reference_cancellation',contains(delta_difference_loose,separation))
    add(checks,'independent_D_difference_encloses_shared_reference_cancellation',contains(d_difference_loose,d_difference))
    add(checks,'independent_F_difference_encloses_shared_reference_cancellation',contains(f_difference_loose,f_difference))
    separations = {'source_reference_retained63_minus_global':separation,
                   'addition_global_minus_retained63_direct_shared_terms':separation,
                   'addition_global_minus_retained63_independent_bounds':delta_difference_loose,
                   'Dglobal_minus_Dretained63_direct_shared_terms':d_difference,
                   'Dglobal_minus_Dretained63_independent_bounds':d_difference_loose,
                   'Fglobal_minus_Fretained63_direct_shared_terms':f_difference,
                   'Fglobal_minus_Fretained63_independent_bounds':f_difference_loose}
    for name,value in {**references,**values,**separations}.items():
        lo,hi = bounds(value)
        add(checks,'endpoint_order_'+name,lo<=hi)
    endpoints = [{'qword':row['qword'],'origin':row['origin'],'ground_interval':row['ground_interval'],
                  'negative_source_partner_qword':row['negative_source_partner_qword']} for row in vs['all64_source_records']]
    return {'references_inherited':references,'quantities':values,'reference_separations':separations,
            'raw_sign_descriptors':{name:sign(value) for name,value in {**values,**separations}.items()},
            'all64_source_endpoints_inherited':endpoints,'all64_negative_source_endpoints_inherited':vs['all64_negative_source_records'],
            'joint_source_stage_endpoints_inherited':[{'iteration':row['iteration'],'ground_interval_raw':row['ground_interval_raw'],
                    'retained63_addition_interval_raw':row['retained63_addition_interval_raw']} for row in js['certificate_stages']],
            'global_vs_retained_preparation_scope':'GLOBAL_STATIC_EQUILIBRIUM_VS_SECTOR_GROUND_PREPARATION_OR_COMPARISON',
            'source_alone_implies_relaxation_or_record_conversion':False,'checks':list(checks)},checks


def reflection_evidence(vs):
    l = vs['complete_source_and_R3_controls']['L_plus_numerators_over40']
    vertex_map,edge_map = [(-v)%6 for v in range(6)],[(-e-1)%6 for e in range(6)]
    reflected30 = sum(((30>>v)&1)<<vertex_map[v] for v in range(6))
    rows = {row['qword']:row for row in vs['all64_source_records']}
    common_upper = max(bounds(rows[q]['ground_interval'])[1] for q in (30,60))
    margin = min(bounds(row['ground_interval'])[0] for q,row in rows.items() if q not in (30,60))-common_upper
    checks = []
    add(checks,'reflection_vertex_and_edge_bijections',sorted(vertex_map)==sorted(edge_map)==list(range(6)))
    add(checks,'profile_preserving_reflection',all(l[v]==l[vertex_map[v]] for v in range(6)))
    add(checks,'reflection30_maps_to60',reflected30==60)
    add(checks,'saved_possible_minima_exactly30_60',vs['possible_minimizing_qwords']==[30,60])
    add(checks,'saved30_60_brackets_identical',same(rows[30]['ground_interval'],rows[60]['ground_interval']))
    add(checks,'all_other62_saved_lowers_strictly_above_common_upper',margin>0)
    add(checks,'saved_complete64_census',sorted(rows)==list(range(64)))
    return {'vertex_map':vertex_map,'edge_map':edge_map,'l_profile':l,'q30_bits':[(30>>v)&1 for v in range(6)],
            'q60_bits':[(60>>v)&1 for v in range(6)],'reflected_q30':reflected30,
            'analytic_action_proof':'l_v=l_-v; reflected delta exchanges adjacent edges; each midpoint feedback/flip and uniform exterior stub maps with its owned weight; hence H60=Pi H30 Pi^-1 exactly. No Hamiltonian enumeration here.',
            'symmetry_is_independent_of_bracket_coincidence':True,
            'simple_sector_ground_reason':'Each64-state incidence hypercube has strictly negative flip ports with positive sources, so Perron ground is simple.',
            'exact_two_sector_degeneracy_candidate':True,'scope':'DECLARED_B_X_NC0_HELD_DIRECT_SUM_ONLY',
            'q30_interval_inherited':rows[30]['ground_interval'],'q60_interval_inherited':rows[60]['ground_interval'],
            'other62_word_energy_separation_lower':exact(margin),'alpha_minus_minimizing_qwords_by_owned_R3':[39,51],
            'formation_bulk_phase_full_alphabet_claim':False,'checks':list(checks)},checks


def report_text(result):
    def rat(value):
        return str(value['numerator'])+'/'+str(value['denominator'])
    assembly = result['scalar_assembly']
    lines = ['# Held hexagon: both matched source references V001','',
             f"Controls: {result['checks_passed']}/{result['checks_total']}; failed {result['checks_failed']}.",
             'Status: '+result['status']+'.','', '| inherited energy reference | exact lower | exact upper |','|---|---:|---:|']
    for name,value in assembly['references_inherited'].items():
        lines.append('| '+name+' | '+rat(value['lower'])+' | '+rat(value['upper'])+' |')
    lines += ['', '| signed derived quantity | exact lower | exact upper | raw sign |','|---|---:|---:|---|']
    for name,value in assembly['quantities'].items():
        lines.append('| '+name+' | '+rat(value['lower'])+' | '+rat(value['upper'])+' | '+assembly['raw_sign_descriptors'][name]+' |')
    lines += ['', '| shared-term reference separation | exact lower | exact upper |','|---|---:|---:|']
    for name,value in assembly['reference_separations'].items():
        lines.append('| '+name+' | '+rat(value['lower'])+' | '+rat(value['upper'])+' |')
    proof = result['analytic_reflection_evidence']
    lines += ['', 'Exact two-sector degeneracy earned: '+str(result['exact_two_sector_degeneracy_earned'])+'.',
              'The profile-preserving reflection v->-v, e->-e-1 mapsq30 toq60 and the complete source action exactly. This proof is separate from equal brackets. Every other62 saved sector lower is above the common upper by at least '+rat(proof['other62_word_energy_separation_lower'])+'. Each sector ground is simple; the exact degeneracy concerns only the declared held B/x Nc0 direct sum.',
              'The source changed the global static minimizing record sectors; q63 is retained as a distinct sector-ground reference. Record conservation alone does not prepare a new sector or an adiabatic ground history.',
              'Fadd is a finite-field decrease; Dalpha is its opposite increase. Both raw references and all signs remain. These quantities are not zero-field derivatives, a normalized gravitational law, physical metric/ruler or transport pole.',
              'All inherited endpoints and early joint-source stage intervals stay sealed. This packet performs only JSON/Fraction scalar assembly and six-bit/profile checks; no Hamiltonian, eigensolve, inertia, NumPy, propagation or prior producer is replayed.',
              'Definite-q carrier injection has qualitative finite-line visibility, but coherent degenerate-sector combinations can cancel. No universal residue, state formation, bulk phase, galaxy/expansion fit, superiority or Stage3 completion is claimed.',
              '',f"Elapsed seconds: {result['elapsed_seconds']}; native peak RSS: {result['ru_maxrss_native']}.",'']
    return '\n'.join(lines)


def main():
    global ATTEMPT_CREATED
    if sys.argv[1:]!=['--execute']:
        raise RuntimeError('Explicit --execute required; no scalar assembly launched')
    for path in (RESULT,REPORT,RECEIPT,CP):
        if path.exists():
            raise FileExistsError('Exclusive output exists: '+str(path))
    inputs,js,vs,joint,vacuum,q63 = authenticate()
    source_hash,protocol_hash = sha(SOURCE),sha(PROTOCOL)
    CP.mkdir()
    ATTEMPT_CREATED = True
    manifest = {'schema':NAME+'_INPUT_MANIFEST','pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,
                'authenticated_inputs':inputs,'alpha':exact(ALPHA),'science_producers_imported_or_replayed':False}
    manifest_hash = save('input_manifest.json',manifest)
    event('started',manifest_sha256=manifest_hash,source_sha256=source_hash,protocol_sha256=protocol_hash)
    assembly,checks = assemble(js,vs,joint,vacuum,q63)
    save('both_reference_scalar_assembly.json',assembly)
    checks = list(checks)
    proof,extra = reflection_evidence(vs)
    save('analytic_reflection_and_saved_separation.json',proof)
    checks.extend(extra)
    final_inputs,*unused = authenticate()
    add(checks,'all_parent_input_checkpoint_report_bytes_unchanged',final_inputs==inputs)
    add(checks,'source_protocol_bytes_unchanged',sha(SOURCE)==source_hash and sha(PROTOCOL)==protocol_hash)
    add(checks,'scalar_stage_private_check_list_unchanged',assembly['checks']==checks[:len(assembly['checks'])])
    failed = sum(not row['passed'] for row in checks)
    result = {'schema':NAME+'_RESULT','status':'EXACT_SCALAR_ASSEMBLY_PASS' if not failed else 'SCALAR_FAILED_PRESERVED',
              'pid':os.getpid(),'source_sha256':source_hash,'protocol_sha256':protocol_hash,'authenticated_inputs':inputs,
              'manifest_sha256':manifest_hash,'checkpoint_sha256':dict(STAGES),'scalar_assembly':assembly,
              'analytic_reflection_evidence':proof,'exact_two_sector_degeneracy_earned':not failed,
              'earned_sign_descriptors':assembly['raw_sign_descriptors'] if not failed else None,
              'operator_numPy_eigensolve_inertia_propagation_replay':False,
              'numeric_derivative_gravity_mass_metric_phase_completion_claim':False,
              'checks':checks,'checks_total':len(checks),'checks_passed':len(checks)-failed,'checks_failed':failed,
              'elapsed_seconds':time.perf_counter()-T0,'ru_maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    report = report_text(result)
    a = report.split('| inherited energy reference |',1)[1].split('| signed derived quantity |',1)[0]
    b = report.split('| signed derived quantity |',1)[1].split('| shared-term reference separation |',1)[0]
    c = report.split('| shared-term reference separation |',1)[1].split('Exact two-sector degeneracy earned:',1)[0]
    if a.count('\n| ')!=5 or b.count('\n| ')!=10 or c.count('\n| ')!=7:
        raise RuntimeError('Report must show5 references,10 signed quantities and7 separation DATA rows')
    raw_hash = exclusive(RESULT,result)
    with REPORT.open('x',encoding='utf-8') as stream:
        stream.write(report)
        stream.flush()
        os.fsync(stream.fileno())
    report_hash = sha(REPORT)
    event('result_complete',raw_sha256=raw_hash,report_sha256=report_hash,checks_passed=result['checks_passed'],checks_total=result['checks_total'])
    receipt = {'schema':NAME+'_RECEIPT','pid':os.getpid(),'result_raw_sha256':raw_hash,
               'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':report_hash,
               'manifest_sha256':manifest_hash,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'checkpoint_sha256':dict(STAGES),
               'source_sha256':source_hash,'protocol_sha256':protocol_hash,'authenticated_inputs':inputs,
               'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],'checks_failed':failed,'elapsed_seconds':result['elapsed_seconds']}
    receipt_hash = exclusive(RECEIPT,receipt)
    event('receipt_complete',receipt_sha256=receipt_hash)
    print(json.dumps({'pid':os.getpid(),'status':result['status'],'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],
                      'result_raw_sha256':raw_hash,'receipt_sha256':receipt_hash,'elapsed_seconds':result['elapsed_seconds']}),flush=True)
    return 0 if not failed else 2


if __name__=='__main__':
    T0 = time.perf_counter()
    try:
        sys.exit(main())
    except Exception as error:
        if ATTEMPT_CREATED:
            payload = {'pid':os.getpid(),'exception_type':type(error).__name__,'error':str(error),
                       'traceback':traceback.format_exc(),'elapsed_seconds':time.perf_counter()-T0}
            path = CP/'ERROR.json'
            if not path.exists():
                digest = exclusive(path,payload)
                event('error',filename=path.name,sha256=digest)
        traceback.print_exc()
        sys.exit(3)
