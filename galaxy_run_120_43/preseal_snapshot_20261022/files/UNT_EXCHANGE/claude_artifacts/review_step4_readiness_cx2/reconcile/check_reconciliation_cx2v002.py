"""Independent saved-record reconciliation. No project imports or producer execution.
Python -I -B, stdlib only. Guard production paths before reads, including metadata.
The supplied reconciliation source was inspected, not executed or imported.
v002 corrects unexecuted v001's pending-slot literal and reads the newly published Markdown.
"""
import os, sys, json, hashlib, struct, copy, datetime, collections, re

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
B = ART + 'step4_launch_readiness_c4/'
C = ART + 'calib_tail_readiness_cx2/'
OUT = ART + 'review_step4_readiness_cx2/reconcile/'
DENIED = []

def ban(p):
    if isinstance(p, int) or p is None:
        return
    s = os.fsdecode(p)
    parts = s.replace('\\', '/').split('/')
    if any(x in ('runs', 'runs_ext') or x.startswith('UVT_') or 'C5H' in x for x in parts) or '/.codex/' in s or any(x in s.lower() for x in ('observed_veloc', 'target_veloc')):
        DENIED.append(s)
        raise RuntimeError('PROTECTED_PATH')

for name in ('stat', 'lstat', 'readlink', 'listdir', 'scandir'):
    old = getattr(os, name)
    def wrapper(p='.', *a, _old=old, **kw):
        ban(p)
        return _old(p, *a, **kw)
    setattr(os, name, wrapper)

def audit(event, args):
    if event in ('open', 'os.listdir', 'os.scandir') and args:
        ban(args[0])
    if event.startswith(('subprocess.', 'socket.')) or event in ('os.system', 'os.remove', 'os.rename', 'os.rmdir', 'os.truncate'):
        raise RuntimeError('EXECUTION_OR_MUTATION_FORBIDDEN')
sys.addaudithook(audit)

PINS = {}
CHECKS = []
def strict_pairs(pairs):
    d = {}
    for k,v in pairs:
        if k in d:
            raise ValueError('duplicate JSON key')
        d[k] = v
    return d

def raw(path):
    ban(path)
    resolved = os.path.realpath(path)
    ban(resolved)
    if not (path.startswith(B) or path.startswith(C) or path.startswith(OUT)):
        raise RuntimeError('NOT_EXPLICIT_SAFE_REVIEW_SCOPE:' + path)
    with open(path, 'rb') as f:
        data = f.read()
    h = hashlib.sha256(data).hexdigest()
    if path in PINS and PINS[path] != h:
        raise RuntimeError('INPUT_MUTATED')
    PINS[path] = h
    return data

def load(path):
    return json.loads(raw(path), object_pairs_hook=strict_pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def pin(ref):
    b = raw(ref['path'])
    check('PIN:' + ref['path'], hashlib.sha256(b).hexdigest() == ref['sha256'])
    return json.loads(b, object_pairs_hook=strict_pairs)

def check(name, ok, detail=None):
    rec = {'name': name, 'pass': bool(ok)}
    if not ok or detail is not None:
        rec['detail'] = detail
    CHECKS.append(rec)
    return bool(ok)

def representation(x):
    if isinstance(x, float):
        return ('float64', struct.pack('>d',x).hex())
    if isinstance(x, dict):
        return ('dict', tuple((k,representation(v)) for k,v in sorted(x.items())))
    if isinstance(x, list):
        return ('list', tuple(map(representation,x)))
    return (type(x).__name__, x)

def same(a,b):
    return representation(a) == representation(b)

def diff(a,b,path=()):
    if type(a) is not type(b):
        return [path]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            out += [path+(k,)] if k not in a or k not in b else diff(a[k],b[k],path+(k,))
        return out
    if isinstance(a,list):
        if len(a)!=len(b): return [path]
        return [p for i,(x,y) in enumerate(zip(a,b)) for p in diff(x,y,path+(i,))]
    return [] if same(a,b) else [path]

def canon(x):
    return json.dumps(x,sort_keys=True,separators=(',', ':'),allow_nan=False).encode()

def point(spec,driver):
    n=copy.deepcopy(spec['numerics'])
    n['uv_tail'].pop('eps_certificate',None)
    n['uv_tail'].pop('lo_certificate',None)
    return hashlib.sha256(canon({'driver_sha256':driver,'physical':spec['physical'],
        'coefficients':spec['coefficients'],'numerics':n})).hexdigest()

def unique(rows,key):
    keys=[key(r) for r in rows]
    if len(keys)!=len(set(keys)): raise ValueError('duplicate record identifier')
    return dict(zip(keys,rows))

def inv_id(name):
    if name=='TAIL_REANCHOR': return 'S4-RA'
    if name=='WORKERS_8_CANDIDATE_ANCHOR': return 'S4-W8'
    if name=='HEADLINE_TRIAL': return 'S4-CAP-TRIAL'
    if name=='CAMPAIGN_W1_SEED': return 'S4-CAMPAIGN'
    if name.startswith('HEADLINE_CORNER_'): return 'S4-CAP-C'+name[-3:]
    if name.startswith('SENS_CORNER_'):
        code,side=name[len('SENS_CORNER_'):].split('_D')
        return 'S4-SENS-'+code+'-'+side
    if name.startswith('SENS_DISTANCE_'): return 'S4-SENS-DIST-'+('LO' if name.endswith('LOWER') else 'HI')
    if name.startswith('DECIDING_III_'):
        _,_,edge,drv=name.split('_')
        return 'S4-DIII-'+('LO' if edge=='LOW' else 'HI')+'-'+('REF' if drv=='V009GEO' else 'NEW')
    raise ValueError(name)

def main():
    start=datetime.datetime.now(datetime.timezone.utc)
    stamp=start.strftime('%Y%m%dT%H%M%SZ')+'_'+str(os.getpid())
    run=OUT+'run_'+stamp+'/'
    os.mkdir(run)
    inv=load(B+'inventory/INVENTORY_C4V001.json')
    dp=load(B+'dryplans/DRYPLANS_C4V002.json')
    rc=load(B+'launch_order/work/RECONCILE_C4V002.json')
    launch=load(B+'launch_order/LAUNCH_ORDER_C4V001.json')
    roots=load(B+'launch_order/work/ROOT_ITEMS_FINAL_C4V001.json')
    oldroots=load(B+'inventory/ROOT_ITEMS_C4V001.json')
    cfg=load(C+'v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json')
    for rel in ('inventory/INVENTORY_C4V001.md','inventory/ROOT_ITEMS_C4V001.md',
                'dryplans/DRYPLANS_C4V001.md','launch_order/ROOT_ITEMS_FINAL_C4V001.md',
                'launch_order/tools/reconcile_c4v002.py','launch_order/LAUNCH_ORDER_C4V001.md'):
        raw(B+rel)
    core_text=raw(C+'v006r9/calibration_core_cx2v006r9.py').decode()
    wrapper_text=raw(C+'v006r9/calibration_orchestrator_cx2v006r9.py').decode()
    policy_text=raw(C+'v006r7/adoption_policy_cx2v006r7.py').decode()
    invs=unique(inv['runs'],lambda r:r['id'])
    recs=unique(dp['records'],lambda r:r['name']+'@'+r['driver_key'])
    pairs=unique(rc['pairs'],lambda r:r['inventory_id'])
    check('inventory_count_37',len(invs)==37)
    check('dryplan_count_34',len(recs)==34)
    check('saved_check_count_253',sum(len(r['checks']) for r in rc['pairs'])==253)
    check('saved_claim_all_true',rc['n_pair_checks']==253 and rc['all_pair_checks_true'] is True)
    ids=set(); specs={}; keys={}; rows=[]; recomputed253=[]; normalizer_changes={}
    for name,d in recs.items():
        rid=inv_id(d['name']); i=invs[rid]; ids.add(rid)
        check(rid+':one_to_one_saved',pairs[rid]['dryplan_records']==[name])
        s=pin(d['spec']); specs[name]=s
        p=pin(d['driver_plan']['report'])
        local=pin(d['record'])
        check(rid+':record_no_launch_claim',local['launches_performed']==0 and local['verdict']=='PLANNED')
        check(rid+':saved_report_join',p['call_spec']==d['spec']['path'] and p['call_spec_sha256']==d['spec']['sha256'] and p['driver_sha256']==d['driver']['sha256'])
        check(rid+':saved_executed_zero',p['executed_stages']==0 and d['driver_plan']['executed_stages']==0 and d['driver_plan']['exit']==0)
        check(rid+':physical_report_equal',same(p['normalized_spec']['physical'],s['physical']) and same(d['physical'],s['physical']))
        check(rid+':coefficient_report_equal',same(p['normalized_spec']['coefficients'],s['coefficients']))
        normalizer_changes[name]=[list(x) for x in diff(s,p['normalized_spec'])]
        c={'one_to_one':True,'driver_equal':i['driver']['sha256']==d['driver']['sha256'],
           'dp_spec_rehash_equal':PINS[d['spec']['path']]==d['spec']['sha256']}
        if i.get('physical') is not None: c['physical_equal_bitwise']=same(i['physical'],s['physical'])
        if i.get('D_Mpc') is not None: c['D_equal']=same(i['D_Mpc'],s['physical']['distance_Mpc'])
        if d['tail_on']:
            key=point(s,d['driver']['sha256']);keys.setdefault(key,[]).append(name)
            check(rid+':independent_point_digest',key==d['orchestrator_layer']['certificate_point_key'])
            if i.get('point_key_r5') is not None: c['point_key_equal']=key==i['point_key_r5']
            check(rid+':production_grid',s['numerics']['uv_tail']['outer']=={'shape':'cylinder','K_big_inverse_kpc':128.0} and s['numerics']['uv_tail']['gas']=={'M_s':128,'interp':'lagrange3_s_gl4'})
            check(rid+':pending_slots',all(s['numerics']['uv_tail'][k]=='PENDING_UV_TAIL_CERTIFICATE' for k in ('eps_certificate','lo_certificate')))
            pp=d['post_adoption_probe']; provisional=pin(pp)
            pdiff=diff(s,provisional)
            allowed={('label',),('numerics','uv_tail','eps_certificate'),('numerics','uv_tail','lo_certificate')}
            check(rid+':provisional_only_label_slots',all(x in allowed or x[:3] in allowed for x in pdiff) and any(x[:3]==('numerics','uv_tail','eps_certificate') for x in pdiff) and any(x[:3]==('numerics','uv_tail','lo_certificate') for x in pdiff),pdiff)
            check(rid+':provisional_point_unchanged',point(provisional,d['driver']['sha256'])==key)
        else:
            check(rid+':tail_off','uv_tail' not in s['numerics'])
            check(rid+':tail_off_has_no_point_key',d['orchestrator_layer'] is None or not d['orchestrator_layer'].get('certificate_point_key'))
            fixed=C+'v006r7/DECIDING_III_'+('LOW' if '-LO-' in rid else 'HIGH')+'_'+('V009_GEO' if rid.endswith('REF') else 'V010_R5')+'_CALL.json'
            c['diii_fixed_spec_sha_equal_dp']=hashlib.sha256(raw(fixed)).hexdigest()==d['spec']['sha256']
        template=i.get('dry_template') or (i.get('spec') or {}).get('prototype_dry_only')
        delta=None
        if template and d['tail_on']:
            t=pin(template);delta=diff(t,s)
            c['template_rehash_equal']=PINS[template['path']]==template['sha256']
            c['template_vs_dp_spec_only_label']=delta==[('label',)]
        check(rid+':253_individual_checks_recomputed',c==pairs[rid]['checks'] and all(c.values()),c)
        recomputed253.extend({'id':rid,'check':k,'pass':v} for k,v in c.items())
        rows.append({'inventory_id':rid,'dryplan':name,'point':d['orchestrator_layer'].get('certificate_point_key') if d['orchestrator_layer'] else None,'template_delta':delta})
    unplanned={'S4-DIII-LO-NEW-R6','S4-DIII-HI-NEW-R6','S4-POST-S1'}
    check('exact_unplanned_three',set(invs)-ids==unplanned)
    for rid in sorted(unplanned):
        c={'no_dry_plan_expected':True}
        check(rid+':recorded_unplanned',pairs[rid]['checks']==c and pairs[rid]['dryplan_records']==[])
        recomputed253.append({'id':rid,'check':'no_dry_plan_expected','pass':True})
    check('independent_253_total',len(recomputed253)==253 and all(x['pass'] for x in recomputed253))
    check('32_distinct_spec_bytes',len({d['spec']['sha256'] for d in recs.values()})==32)
    check('34_actual_spec_paths',len({d['spec']['path'] for d in recs.values()})==34)
    check('30_tail_on',sum(d['tail_on'] for d in recs.values())==30)
    check('28_independent_points',len(keys)==28)
    check('point_group_matches_record',keys and {k:sorted(v) for k,v in keys.items()}==rc['counts']['point_keys'])
    anchor=point(specs['TAIL_REANCHOR@r5'],recs['TAIL_REANCHOR@r5']['driver']['sha256'])
    seed=point(specs['CAMPAIGN_W1_SEED@r5'],recs['CAMPAIGN_W1_SEED@r5']['driver']['sha256'])
    check('anchor_three_roles_one_point',set(keys[anchor])=={'TAIL_REANCHOR@r5','HEADLINE_TRIAL@r5','WORKERS_8_CANDIDATE_ANCHOR@r5'})
    check('seed_not_anchor',seed!=anchor and keys[seed]==['CAMPAIGN_W1_SEED@r5'])
    check('inventory_27_plus_seed',len({x['point_key_r5'] for x in inv['runs'] if x.get('point_key_r5')})==27 and set(keys)-{x['point_key_r5'] for x in inv['runs'] if x.get('point_key_r5')}=={seed})
    for edge in ('LOW','HIGH'):
        a=recs['DECIDING_III_'+edge+'_R5@r5'];b=recs['DECIDING_III_'+edge+'_V009GEO@v009geo']
        check(edge+':same_pair_bytes',a['spec']['sha256']==b['spec']['sha256'])
        check(edge+':different_drivers',a['driver']['sha256']!=b['driver']['sha256'])
    counts=collections.Counter(b['class'] for d in recs.values() for b in d['blockers'])
    check('93_blocker_entries',dict(counts)=={'OTHER_ROOT_ITEM':63,'V007_ADOPTION_PIN':30})
    check('campaign_still_gated',dp['orchestrator_plan']['gates_ok'] is False and len(dp['campaign_level_gates'])==7)
    check('certificate_registry_pending',cfg['tail_readiness']['certificate_registry'] is None and cfg['tail_readiness']['certificate_policy_review'] is None and cfg['tail_readiness']['approved_certificate_producers']==[])
    check('adoption_inputs_pending',all(cfg['numerics'].get(k) is None for k in ('verdict_artifact','block_source','compare','sealed_prereg','adopted_result')))
    check('seal_allowlist_source_empty','APPROVED_V007_SEALS = frozenset()' in policy_text)
    check('launch_order_no_authorization','Nothing here launches, schedules or authorizes a run' in launch['authority'])
    newitems=unique(roots['items'],lambda r:r['id'])
    olditems=unique(oldroots['items'],lambda r:r['id'])
    check('root_items_31_to_36',len(olditems)==31 and len(newitems)==36 and set(olditems)<=set(newitems))
    check('new_five_items',set(newitems)-set(olditems)=={'R-A6','R-B6','R-C8','R-D15','R-D16'})
    codes={b['code'] for d in recs.values() for b in d['blockers'] if b['class']!='V007_ADOPTION_PIN'}
    check('non_v007_blocker_traceability',codes==set(roots['traceability']['dryplan_non_v007_codes']))
    check('campaign_gate_traceability',{g['gate'] for g in dp['campaign_level_gates']}==set(roots['traceability']['dryplan_campaign_gates']))
    check('root_final_28_points','28' in newitems['R-C1']['title'])
    check('launch_copy_of_reconcile_counts',launch['reconcile']['result']['pair_checks']==len(recomputed253) and launch['reconcile']['result']['counts']['dryplan_distinct_certificate_point_keys']==len(keys))
    # Own comparator controls: exact type/float preservation, structural empties, scientific deltas.
    a=copy.deepcopy(specs['TAIL_REANCHOR@r5']);b=copy.deepcopy(a);b['label']='own control'
    check('CONTROL:label_only',diff(a,b)==[('label',)])
    b=copy.deepcopy(a);b['physical']['distance_Mpc']+=0.01
    check('CONTROL:distance_detected',diff(a,b)==[('physical','distance_Mpc')])
    check('CONTROL:signed_zero_detected',not same(0.0,-0.0))
    check('CONTROL:integer_float_distinct',not same(1,1.0))
    check('CONTROL:empty_container_addition_detected',diff({}, {'x':{}})==[('x',)])
    try: json.loads('{"a":1,"a":1}',object_pairs_hook=strict_pairs)
    except ValueError: dup=True
    else: dup=False
    check('CONTROL:duplicate_JSON_rejected',dup)
    # Re-read exactly consumed safe inputs; no recursive hashes or embedded production-pointer traversal.
    for p,h in list(PINS.items()):
        check('UNCHANGED:'+p,hashlib.sha256(raw(p)).hexdigest()==h)
    result={'schema':'STEP4_RECONCILIATION_REVIEW_CX2V002','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'status':'TESTED_STATIC_SAVED_RECORDS','launchability':'UNTESTED_NOT_AUTHORIZED',
      'checks':CHECKS,'passed':sum(x['pass'] for x in CHECKS),'total':len(CHECKS),'failures':[x for x in CHECKS if not x['pass']],
      'claimed_253_recomputed':recomputed253,'rows':rows,'point_groups':keys,'normalization_differences':normalizer_changes,
      'input_pins':PINS,'protected_attempts':DENIED,
      'limitations':['No supplied tools, driver, Context, or scientific modules imported/executed.',
      'Plan process history and gate probe booleans are archived claims, not rerun.',
      'Production receipts/run pointers inside records were not followed.',
      'No final package BUILD/index is asserted; this reviews exact current named records.',
      'Future final spec regeneration and actual admission remain untested.']}
    with open(run+'RESULTS_CX2V001.json','x') as f:json.dump(result,f,indent=1,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'result':run+'RESULTS_CX2V001.json','sha256':hashlib.sha256(open(run+'RESULTS_CX2V001.json','rb').read()).hexdigest(),
        'passed':result['passed'],'total':result['total'],'failures':result['failures'],'pins':len(PINS),'denied':len(DENIED)}))

if __name__=='__main__': main()
