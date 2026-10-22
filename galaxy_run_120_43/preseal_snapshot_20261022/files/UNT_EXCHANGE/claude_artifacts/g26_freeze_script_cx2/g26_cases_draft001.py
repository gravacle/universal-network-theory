"""Additional synthetic G26 tests; executed in the integration fixture namespace."""
import contextlib
import math


@contextlib.contextmanager
def patch(obj, **changes):
    before = {key:getattr(obj, key) for key in changes}
    for key, value in changes.items():
        setattr(obj, key, value)
    try:
        yield
    finally:
        for key, value in before.items():
            setattr(obj, key, value)


serial = 0
def call_with(**changes):
    global serial
    serial += 1
    changed = dict(input_doc, **changes)
    pin = fixture.jwrite(WORK / ('input_case_%03d.json' % serial), changed)
    return g.freeze(rb, pin, str(WORK / ('freeze_case_%03d' % serial)))


def changed_pass(**changes):
    global serial
    serial += 1
    value = t.jload(pass_input['path'])
    value.update(changes)
    return fixture.jwrite(WORK / ('pass_case_%03d.json' % serial), value)


def counterfactual_context(change):
    original = rb._plan_context
    def altered(*args):
        result = copy.deepcopy(original(*args))
        change(result)
        return result
    return patch(rb, _plan_context=altered)


def context_refusal(change):
    with counterfactual_context(change):
        return call_with()


case('G002_output_exists', lambda:g.freeze(rb,input_pin,str(WORK/'freeze_happy')),
     'G26_OUTPUT_EXISTS_OR_NOT_ABSOLUTE')
case('G003_no_operator_completeness_toggle', lambda:call_with(allow_incomplete=False), 'INPUT_KEY_UNKNOWN')
case('G004_PASS_ONE_refused', lambda:call_with(pass_input=changed_pass(pass_label='PASS_ONE')),
     'G26_PASS_K_REQUIRED')
case('G005_superseded_plan', lambda:context_refusal(lambda c:c.update(superseded=True)),
     'G26_STEP7_NOT_CLEARED')
case('G006_empty_ledger', lambda:context_refusal(lambda c:c['ledger'].update(results=[])),
     'G26_STEP7_NOT_CLEARED')
case('G007_uncleared_head', lambda:context_refusal(
    lambda c:c['ledger']['results'][-1].update(status='NEW_UNEVALUATED')), 'G26_STEP7_NOT_CLEARED')
case('G008_other_plan_head', lambda:context_refusal(
    lambda c:c['ledger']['results'][-1].update(replay_plan_sha256='e'*64)), 'G26_STEP7_NOT_CLEARED')
case('G009_custody_head', lambda:context_refusal(
    lambda c:c['ledger']['results'][-1].update(kind='CUSTODY')), 'G26_STEP7_NOT_CLEARED')
case('G010_FULL_required', lambda:context_refusal(lambda c:c['plan'].update(stage='MEMBERS')),
     'G26_FULL_REQUIRED')


def other_head_file():
    pin = t.wbytes(str(WORK/'head_copy.json'), Path(head_pin['path']).read_bytes())
    return call_with(ledger_head=pin)
case('G011_external_head_path_binding', other_head_file, 'G26_LEDGER_HEAD_MISMATCH')
case('G012_external_head_sha', lambda:call_with(ledger_head=dict(head_pin,sha256='a'*64)),
     'PIN_MISMATCH')


def bad_fixed(name):
    with patch(g, **{name:'e'*64}):
        return call_with()
case('G013_spec_fixed_sha', lambda:bad_fixed('SPEC_SHA256'), 'G26_DN2_SPEC_SHA')
case('G014_notes_fixed_canonical_sha', lambda:bad_fixed('NOTES_CANONICAL_SHA256'), 'G26_DN2_NOTES_SHA')
case('G015_slots_fixed_sha', lambda:bad_fixed('SLOTS_SHA256'), 'G26_DN2_SLOTS_PIN')
case('G016_freeze_module_sha', lambda:bad_fixed('FREEZE_SHA256'), 'G26_FREEZE_MODULE_PIN')
case('G017_wrong_plan_allow', lambda:context_refusal(lambda c:c['plan'].update(allow_incomplete=False)),
     'G26_ALLOW_INCOMPLETE_NOT_REDERIVED')
case('G018_production_query_role_refuses_synthetic', lambda:(
    production_role()), 'G26_PROGRAM_QUERY_MANIFEST') if False else None


def production_role():
    with patch(g, QUERY_ROLE='PROGRAM_PIN'):
        return call_with()
case('G018_production_query_role_refuses_synthetic', production_role, 'G26_PROGRAM_QUERY_MANIFEST')


def bootstrap_mismatch():
    with patch(g, BUILDER_SHA256='e'*64):
        try:
            g.bootstrap_builder()
        except g.BootstrapRefusal as exc:
            assert str(exc)=='BUILDER_PIN_MISMATCH'
            return
    raise AssertionError('unverified builder executed')
case('G019_bootstrap_sha_before_exec', bootstrap_mismatch)


def source_type_fence():
    with patch(g, BUILDER_PATH=str(WORK)):
        try:
            g.bootstrap_builder()
        except g.BootstrapRefusal as exc:
            assert str(exc)=='BUILDER_NOT_REGULAR'
            return
    raise AssertionError('non-regular builder accepted')
case('G020_bootstrap_regular_file', source_type_fence)


def notes_whitespace():
    pretty = t.wbytes(str(WORK/'notes_pretty.json'),
                     (json.dumps(notes,indent=4,sort_keys=False)+'\n').encode())
    result = call_with(notes=pretty)
    assert result['dn2_notes']['sha256'] != notes_pin['sha256']
    assert result['dn2_notes_canonical_sha256']==g.NOTES_CANONICAL_SHA256
case('G021_notes_canonical_not_file_hash', notes_whitespace)


slotdoc = t.jload(b.slots['path'])
for key in ('lower','upper','trial_value','reference_value'):
    def one_ulp(key=key):
        coordinates=copy.deepcopy(spec['coordinates'])
        row=next(c for c in coordinates if c['scope']=='ngc3198_nuisance' and c[key] is not None)
        row[key]=math.nextafter(row[key],math.inf)
        return g.check_coordinates(rb,coordinates,slotdoc)
    case('G022_one_ulp_'+key,one_ulp,'G26_DN2_COORDINATES_MISMATCH')
for name,change,code in [
    ('missing',lambda s:s['ngc3198_slots'].pop(),'G26_DN2_COORDINATE_SHAPE'),
    ('duplicate',lambda s:s['ngc3198_slots'].__setitem__(1,copy.deepcopy(s['ngc3198_slots'][0])),
     'G26_DN2_COORDINATE_SHAPE'),
    ('reordered',lambda s:s['ngc3198_slots'].reverse(),'G26_DN2_COORDINATES_MISMATCH'),
    ('boolean',lambda s:s['ngc3198_slots'][0].update(lower=True),'G26_DN2_COORDINATE_SHAPE'),
    ('nonfinite',lambda s:s['ngc3198_slots'][0].update(lower=float('nan')),'G26_DN2_COORDINATE_SHAPE'),
]:
    def altered_slots(change=change):
        s=copy.deepcopy(slotdoc);change(s)
        return g.check_coordinates(rb,spec['coordinates'],s)
    case('G023_coordinates_'+name,altered_slots,code)


def guard_before_registration():
    m={'coordinates':copy.deepcopy(spec['coordinates']),'notes':copy.deepcopy(notes)}
    ngc=next(c for c in m['coordinates'] if c['scope']=='ngc3198_nuisance')
    ngc['trial_value']=math.nextafter(ngc['trial_value'],math.inf)
    called=[]
    original=b.fm._validate_manifest_structure
    with patch(b.fm,_validate_manifest_structure=lambda m,r:called.append(True)):
        with g.manifest_dn2_guard(rb,b.fm,slotdoc,notes) as seen:
            reasons=[];b.fm._validate_manifest_structure(m,reasons)
            assert reasons==['G26_DN2_COORDINATES_MISMATCH'] and not seen and not called
    assert b.fm._validate_manifest_structure is original
case('G024_manifest_guard_before_registration',guard_before_registration)


def guard_notes():
    m={'coordinates':spec['coordinates'],'notes':dict(notes,edited=True)}
    with patch(b.fm,_validate_manifest_structure=lambda m,r:None):
        with g.manifest_dn2_guard(rb,b.fm,slotdoc,notes) as seen:
            reasons=[];b.fm._validate_manifest_structure(m,reasons)
            assert reasons==['G26_DN2_MANIFEST_NOTES_MISMATCH'] and not seen
case('G025_manifest_guard_notes',guard_notes)


def guard_restore_exception():
    original=b.fm._validate_manifest_structure
    try:
        with g.manifest_dn2_guard(rb,b.fm,slotdoc,notes):
            raise RuntimeError('synthetic')
    except RuntimeError:
        pass
    assert b.fm._validate_manifest_structure is original
case('G026_manifest_guard_restores_on_exception',guard_restore_exception)


def changed_pass_bytes():
    original=rb.pass_driver
    def wrong(*args):
        record,extract,memory=original(*args)
        record=copy.deepcopy(record);record['synthetic_extra']=True
        return record,extract,memory
    with patch(rb,pass_driver=wrong):
        return call_with()
case('G027_inprocess_PASS_K_difference',changed_pass_bytes,'G26_PASS_K_BYTES_DIFFER')


def partial_writer_failure():
    original_result=b.fm._root_result_rows
    original_frozen=b.fm._root_frozen_rows
    original_validate=b.fm._validate_manifest_structure
    paths=[]
    def broken_writer(**kwargs):
        paths.append(kwargs['out_path'])
        with open(kwargs['out_path'],'xb') as f:
            f.write(b'{"synthetic_partial":true}')
        return {'ok':False}
    with patch(b.fm,write_freeze_manifest=broken_writer):
        try:
            call_with()
        except rb.Refused as exc:
            assert exc.code=='G26_WRITER_REFUSED'
        else:
            raise AssertionError('failure swallowed')
    assert len(paths)==1 and Path(paths[0]).read_bytes()==b'{"synthetic_partial":true}'
    assert not Path(paths[0]).with_name('FREEZE_REGISTRATION.json').exists()
    assert b.fm._root_result_rows is original_result
    assert b.fm._root_frozen_rows is original_frozen
    assert b.fm._validate_manifest_structure is original_validate
case('G028_partial_outputs_preserved_and_adapters_restored',partial_writer_failure)


def no_op_writer():
    def writer(**kwargs):
        return {'ok':True}
    with patch(b.fm,write_freeze_manifest=writer):
        return call_with()
case('G029_writer_cannot_skip_DN2_guard',no_op_writer,'G26_MANIFEST_DN2_NOT_EXECUTED')


def dn5_rule(phase, disposition, sensitivity=False, evaluated=True):
    plan={'phase':phase,'primary':'P','alternatives':[{
        'name':'P','slots_status':rb.ALT_EVALUATED if evaluated else rb.ALT_NOT_EVALUATED,
        'members':[] if sensitivity else [{'own_disposition':disposition}]}],
        'sensitivity':{'entries':[{'own_disposition':disposition}] if sensitivity else []}}
    return rb.allow_incomplete_value(plan)
case('G030_phase1_incomplete_true',lambda:(
    None if dn5_rule('PHASE_1','EVALUATED') is True else (_ for _ in ()).throw(AssertionError())))
for disposition in ('UNEVALUATED_STEP7_DISCREPANCY','UNEVALUATED_CUSTODY_BREACH',
                    'UNEVALUATED_SCHEDULE_CEILING'):
    for sensitivity in (False,True):
        def check_dn5(d=disposition,s=sensitivity):
            assert dn5_rule('PHASE_2',d,s) is True
            assert dn5_rule('PHASE_2',d,s,False) is False
        case('G031_DN5_'+disposition+('_sensitivity' if sensitivity else '_member'),check_dn5)
def geometry_not_incomplete():
    assert dn5_rule('PHASE_2','GEOMETRY_NOT_EXPOSED_IN_MEMORY',True) is False
    assert dn5_rule('PHASE_2','EVALUATED') is False
case('G032_geometry_alone_not_incomplete',geometry_not_incomplete)


def bootstrap_full():
    before=len(fixture.READS)
    new_rb,bootstrap=g.bootstrap_builder()
    orig_loader=new_rb.load_freeze_module
    def load_synthetic(pin):
        loaded=orig_loader(pin)
        loaded.ROOT_SLOTS_PATH=b.slots['path'];loaded.ROOT_SLOTS_SHA256=b.slots['sha256']
        loaded.REGISTERED_GL_NODES_PATH=b.nodes['path']
        loaded.REGISTERED_GL_NODES_SHA256=b.nodes['sha256']
        return loaded
    new_rb.load_freeze_module=load_synthetic
    with new_rb.snapshot_scope() as snapshot:
        g.seed_snapshot(snapshot,bootstrap)
        result=g.freeze(new_rb,input_pin,str(WORK/'freeze_bootstrap'))
    counts=collections.Counter(fixture.READS[before:])
    assert counts and max(counts.values())==1,{k:n for k,n in counts.items() if n!=1}
    assert counts[g.BUILDER_PATH]==1 and result['verdict']=='PASS'
case('G033_bootstrap_full_writer_single_read',bootstrap_full)


def latest_ledger_not_supplied_head():
    t.step7(env,out,plan_pin,p1pin,pkpin)
    return call_with()
case('G034_appended_ledger_refuses_previous_external_head',
     latest_ledger_not_supplied_head,'G26_LEDGER_HEAD_MISMATCH')


def byte_not_semantic_equality():
    compact=t.wbytes(str(WORK/'pass_k_compact.json'),rb.canonical_bytes(pk))
    assert t.jload(compact['path'])==pk and compact['sha256']!=pkpin['sha256']
    comparison,_,_=t.step7(env,out,plan_pin,p1pin,compact)
    assert comparison['status']=='NO_NEW_DISCREPANCY'
    head=t.pin(os.path.join(t.ledger_dir(out),'STEP7_0003.json'))
    return call_with(ledger_head=head)
case('G035_byte_equality_not_JSON_equivalence',byte_not_semantic_equality,'G26_PASS_K_BYTES_DIFFER')
