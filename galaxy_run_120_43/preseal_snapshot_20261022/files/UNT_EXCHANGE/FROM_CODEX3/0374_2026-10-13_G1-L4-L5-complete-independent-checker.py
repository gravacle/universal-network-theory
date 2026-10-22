"""SOURCE ONLY. Root complete independent eleven-file L4/L5 G1 comparison.
CLI --archive ORIGINAL_ABS --output FRESH_ROOT_ABS --L 4|5 --sector old|Born
--axes 012|021|102|210. No numerical authorship, producer imports or self-review.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace
B=Path('/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001')
ROLE='P60_L45_FIXEDPOINT_SIXTEEN_V001'
CAPS={'cpu':1,'rss_bytes':256*2**20,'seconds':120,'output_bytes':16*2**20,'scientific_reserve_bytes':8*2**20}
FILES={'START.json','CONFIG.json','SOURCES.json','GATES.json','DOMAIN_PRE.json','DOMAIN_RETURN.json',
    'ACTUAL_PRE.json','PROGRESS.jsonl','ACTUAL_RETURN.json','INPUT_MANIFEST.json','FINISH.json'}
CALLER = Path('/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_l45_sixteen_case_root_caller_v001.py')
CALLER_SHA = '52362b8e9ed9dfc36c42447726d09b0c875a1747b9cf916c8b0fb8301abf3ab0'
SOURCE = {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P60_CODEX2/p60_exact_ice_fixedpoint_count_v001.py', 'sha256': '9bfed34cbc4c8695ecf8528598f6532f6980de91de12c139cea2e58332952533', 'bytes': 9540}
LINEAGE = {'c159': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_AFFINE_COMPLETE_CENSUS_ACCEPTANCE_V001.json', 'sha256': 'fa4c464234b701728ab605279cd7aee19c445a21a05966e2f965ffb5896ea6f5', 'bytes': 15878}, 'c162': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_LITERAL_ICE_ANALYTIC_COMPRESSION_ACCEPTANCE_V001.json', 'sha256': '6ed2ddc4e7dc04595d3915bf46a64265754793ae2a9c5b22da5250e04c3835ba', 'bytes': 2797}, 'c168': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_FIXEDPOINT_L2_METHOD_ACCEPTANCE_V001.json', 'sha256': '5accbd8f9cd3b2f51bba412b69a82767a225dbaaf977676d86072bab6a2024f7', 'bytes': 75435}, 'c174': {'path': '/Users/bgm/Research/UNT_EXCHANGE/KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_ICE_CYCLE_ZERO_AND_BOUNDARY_IDENTITIES_ACCEPTANCE_V001.json', 'sha256': 'b9e7088e9958e2527e42e715913136ff5526728723c55b091193d67213013471', 'bytes': 1482}}
HELPERS = {'custody': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0331_2026-10-13_warning-independent-custody.py', '6fab6cd9636fca18463fe158f0da7b1641e51ff9fe3276e4a52c4220edfb5f47'), 'math': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0373_2026-10-13_G1-L4-L5-independent-graph-and-frontier.py', 'c02b0f35fd6b039d38d817f412864d2bf31660a4fe1410e4f947e6bfcc767ba7')}


def domain(g):
    records=g['records'];boundary=g['boundary'];ends={e:(a,b) for e,a,b in records};factors=[]
    for orbit in g['orbits']:
        multiplicity={}
        for edge in orbit:
            for vertex in ends[edge]:multiplicity[vertex]=multiplicity.get(vertex,0)+1
        factors.append({'edge_orbit':orbit,'vertex_degree_exponents':[[v,multiplicity[v]] for v in sorted(multiplicity)],
            'K_exponents':[len(set(orbit)&row) for row in boundary],
            'marked_exponent':len(set(orbit)&set(g['cuts'])) if g['sector']=='old' else 0})
    return {'schema':'P60_COMPLETE_FIXEDPOINT_DOMAIN_V001','L':g['L'],'sector':g['sector'],'axis_permutation':g['axes'],
        'vertices':g['vertices'],'all_edges_stable_ids':records,
        'edge_permutation':[[e,g['image'][e]] for e in sorted(g['image'])],
        'marked_old_edge_ids':g['cuts'],'all_edge_K_weights':[[e,[int(e in row) for row in boundary]] for e,a,b in records],
        'complete_edge_orbits':g['orbits'],'complete_orbit_polynomial_factors':factors,
        'coefficient_target':'all vertex degrees2; retain all K and old marked degrees; eligible old marked2',
        'polynomial_coefficients_evaluated_here':False,'full_H_invariant_sector_claim':False,'physical_release':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--L',type=int,choices=[4,5],required=True);ap.add_argument('--sector',choices=['old','Born'],required=True)
    ap.add_argument('--axes',choices=['012','021','102','210'],required=True)
    a=ap.parse_args();start=time.monotonic()
    def guard():
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        if time.monotonic()-start>120 or rss>256*2**20:raise RuntimeError('whole independent120s256MiB checker cap')
    modules={}
    for label,(filename,sha) in HELPERS.items():
        p=Path(filename)
        if not p.is_absolute() or p.resolve()!=p or p.is_symlink() or p.stat().st_size>65536:raise ValueError('plain checker helper')
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('checker helper digest')
        ns={'__name__':'root_g1_independent_'+label,'__file__':filename}
        exec(compile(raw,filename,'exec'),ns);modules[label]=SimpleNamespace(**ns);guard()
    C,M=modules['custody'],modules['math'];need,exact,decode=C.need,C.exact,C.decode;I=C.Inputs(guard)
    for filename,sha in HELPERS.values():I.read(Path(filename),sha,65536)
    I.read(Path(__file__).resolve(),cap=65536)
    root,out=a.archive,a.output
    need(root.is_absolute() and root.resolve()==root and not root.is_symlink() and root.is_dir() and B in root.parents,'literal root producer archive')
    need(out.is_absolute() and out.resolve()==out and not out.exists() and B in out.parents,'fresh literal root checker output')
    need({p.name for p in root.iterdir()}==FILES,'complete eleven scientific files')
    data,rawfiles,filemeta={},{},{}
    for name in sorted(FILES):
        raw=I.read(root/name,cap=8*2**20);rawfiles[name]=raw
        if name!='PROGRESS.jsonl':data[name]=decode(raw)
        pin=I.pins[str(root/name)];filemeta[name]={'bytes':pin['bytes'],'sha256':pin['sha256']}
    need(sum(v['bytes'] for v in filemeta.values())<=8*2**20,'whole original science reserve')
    producer_paths=[]
    def pp(pin):
        raw=I.pin(pin,cap=2*2**20)
        if pin['path'] not in producer_paths:producer_paths.append(pin['path'])
        return raw
    case={'L':a.L,'sector':a.sector,'axes':a.axes};axes=list(map(int,a.axes))
    st=data['START.json'];pid=st['pid'];cp=st['config']
    need(type(pid)is int and pid>0,'original producer PID syntax only')
    need(Path(cp['path']).parent==B,'root original config namespace')
    cfg=decode(pp(cp));exact(data['CONFIG.json'],cfg,'whole config snapshot')
    need(set(cfg)=={'schema','role','released_by','execute','case','caps','output','source_gate','lineage_gate'},'closed config')
    need(cfg['schema']=='P60_L45_FIXEDPOINT_RELEASE_V001' and cfg['role']==ROLE and cfg['released_by']=='/root'
        and cfg['execute'] is True and cfg['output']==str(root),'actual root release')
    exact(cfg['case'],case,'frozen exact case');exact(cfg['caps'],CAPS,'whole role caps')
    callerpin={'path':str(CALLER),'sha256':CALLER_SHA};callerraw=pp(callerpin)
    gates={}
    for name in ('source_gate','lineage_gate'):
        need(Path(cfg[name]['path']).parent==B,'root-owned actual gate');gates[name]=decode(pp(cfg[name]))
    exact(data['GATES.json'],gates,'whole gate snapshots');sg,lg=gates['source_gate'],gates['lineage_gate']
    need(sg['acceptor']=='/root' and str(sg['status']).startswith('PASS') and sg['role']==ROLE
        and sg['reviewer_id'] not in (None,'Codex2'),'distinct caller/science source gate')
    exact(sg['source'],SOURCE,'pinned unchanged DP');exact(sg['caller'],callerpin,'whole literal caller pin')
    need(lg['acceptor']=='/root' and str(lg['status']).startswith('PASS') and lg['role']==ROLE
        and lg['complete_original_opening_checked'] is True and lg['complete_original_closing_root_obligation'] is True,'root whole lineage custody')
    exact(lg['case'],case,'actual lineage case');exact(lg['lineage_pins'],LINEAGE,'all four original ancestry pins')
    for label,pin in LINEAGE.items():
        doc=decode(pp(pin));need(doc['acceptor']=='/root','actual accepted lineage '+label)
    scientific=pp(SOURCE)
    exact(data['SOURCES.json'],{'caller':callerraw.decode(),'fixedpoint':scientific.decode()},'every producer/helper source byte')
    exact(st,{'schema':'P60_L45_FIXEDPOINT_START_V001','pid':pid,'executor':'/root','config':cp,'case':case,
        'caps':CAPS,'external_supervisor_required':True,'scientific_acceptance':False},'wholeSTART')
    exact(data['DOMAIN_PRE.json'],{'function':'graph_and_map_plus_complete_orbit_polynomial','L':a.L,'sector':a.sector,
        'axis_permutation':axes,'phase':'BEFORE_ACTUAL_DOMAIN_CALL','source':SOURCE},'whole domain actual PRE')
    g=M.graph(a.L,a.sector,axes);whole_domain=domain(g)
    exact(data['DOMAIN_RETURN.json'],{'exception':None,'value':whole_domain},'every graph/action/orbit/polynomial field')
    dp={'path':str(root/'DOMAIN_RETURN.json'),**filemeta['DOMAIN_RETURN.json']}
    exact(data['ACTUAL_PRE.json'],{'function':'fixed_point','L':a.L,'sector':a.sector,'axis_permutation':axes,'live_cap':65536,
        'complete_domain':dp,'domain_selector':'value','phase':'BEFORE_ACTUAL_DP_CALL',
        'retention':'complete domain and every completed-orbit summary; intermediate coefficient frontiers not archived'},'whole actual DP PRE')
    expected,progress=M.reconstruct(g,guard)
    raw=rawfiles['PROGRESS.jsonl'];lines=raw.splitlines()
    need((not raw or raw.endswith(b'\n')) and all(lines) and len(lines)<=len(g['orbits']),'complete bounded progress records')
    exact([decode(line) for line in lines],progress,'every completed orbit and exact frontier cardinality')
    exact(data['ACTUAL_RETURN.json'],{'exception':None,'value':expected},'whole exact count OR scientific cap refusal')
    exact(data['INPUT_MANIFEST.json'],{'complete_consumed_input_files':[I.pins[p] for p in producer_paths],
        'root_complete_original_closing_required':True,'selected_inputs_are_whole_process_custody':False},'entire ordered input manifest')
    exact(data['FINISH.json'],{'schema':'P60_L45_FIXEDPOINT_FINISH_V001','pid':pid,'case':case,
        'files_before_finish':{k:v for k,v in filemeta.items() if k!='FINISH.json'},'progress_records':len(progress),
        'all_consumed_input_closing_bytes_match':True,'algorithm_disposition':expected['status'],
        'status':'RAW_COUNT_OR_CAP_REFUSAL_REQUIRES_DISTINCT_COMPLETE_COMPARISON','subgroup_dimensions_called':False,
        'full_H_invariant_sector_claim':False,'physical_release':False},'wholeFINISH')
    need({p.name for p in root.iterdir()}==FILES,'closing whole eleven-file census');I.close();guard()
    report={'schema':'CODEX3_P60_L45_COMPLETE_INDEPENDENT_COMPARISON_V001','status':'PASS_COMPLETE_SAVED_COMPARISON_PENDING_ROOT_RUNTIME_CUSTODY',
        'case':case,'source_author':'Codex2','checker_author':'Codex3','self_review':False,
        'archive':str(root),'all11_scientific_files':filemeta,'all_domain_graph_action_orbits_and_polynomial_fields_compared':True,
        'all_completed_orbit_summaries_compared':len(progress),'complete_actual_return':expected,
        'independent_representation':'radix-coordinate graph; full unpacked byte degrees, explicit K tuple and cut exponent; exact positive coefficient extraction',
        'full_vertex_choice_exhaustive_enumeration_claim':False,'intermediate_tables_archived_claim':False,
        'complete_checker_input_pins':I.pins,'all_opened_input_closing_pins_match':True,
        'producer_actual_runtime_and_whole_original_namespaces_authenticated_here':False,
        'dimension_inferred_from_partial_table':False,'subgroup_dimensions_authorized':False,
        'full_H_invariant_sector_claim':False,'physical_release':False}
    raw=(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    need(len(raw)<=8*2**20,'whole checker science reserve');out.mkdir(exist_ok=False)
    with (out/'INDEPENDENT_REPORT.json').open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    guard();print(json.dumps({'status':report['status'],'algorithm_status':expected['status'],'sha256':hashlib.sha256(raw).hexdigest()}),flush=True)


if __name__=='__main__':main()
