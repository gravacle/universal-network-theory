"""Mutation witnesses. Every disabled guard must admit the prohibited state;
an unrelated refusal is not credited as a killed negative mutant."""
import contextlib
import math

original_g = g
baseline_source = G26.read_text()
mutation_results = []
mutation_serial = 0


@contextlib.contextmanager
def patch(obj, **changes):
    old = {key:getattr(obj,key) for key in changes}
    for key,value in changes.items():
        setattr(obj,key,value)
    try:
        yield
    finally:
        for key,value in old.items():
            setattr(obj,key,value)


def candidate(source, name):
    m=module(source.encode(),G26,'g26_mutant_'+name)
    m.SPEC_SHA256=b.spec_pin['sha256'];m.SLOTS_SHA256=b.slots['sha256']
    m.QUERY_ROLE='SYNTHETIC_FIXTURE'
    return m


def execute_candidate(m, doc=None):
    global mutation_serial
    mutation_serial+=1
    given=input_doc if doc is None else doc
    pin=fixture.jwrite(WORK/('mutant_input_%03d.json'%mutation_serial),given)
    return m.freeze(rb,pin,str(WORK/('mutant_freeze_%03d'%mutation_serial)))


def observe(fn):
    try:
        return {'accepted':True,'value':fn()}
    except rb.Refused as exc:
        return {'accepted':False,'code':exc.code}
    except original_g.BootstrapRefusal as exc:
        return {'accepted':False,'code':str(exc)}
    except Exception as exc:
        if type(exc).__name__=='BootstrapRefusal':
            return {'accepted':False,'code':str(exc)}
        return {'accepted':False,'code':type(exc).__name__}


def negative(name, old, new, witness, code):
    assert baseline_source.count(old)==1,(name,baseline_source.count(old))
    changed=baseline_source.replace(old,new)
    original=candidate(baseline_source,name+'_control')
    mutant=candidate(changed,name)
    before=observe(lambda:witness(original))
    after=observe(lambda:witness(mutant))
    killed=before.get('code')==code and after['accepted']
    row={'id':name,'type':'negative restoring witness','expected_code':code,
         'control':{k:v for k,v in before.items() if k!='value'},
         'mutant':{k:v for k,v in after.items() if k!='value'},
         'mutant_source_sha256':hashlib.sha256(changed.encode()).hexdigest(),
         'verdict':'KILLED' if killed else 'NOT_KILLED'}
    mutation_results.append(row);print(json.dumps(row,sort_keys=True),flush=True)


def bad_constant(m,name):
    setattr(m,name,'e'*64)
    return execute_candidate(m)


negative('M01_spec_pin',
         "spec_pin['sha256'] == SPEC_SHA256",
         "True",
         lambda m:bad_constant(m,'SPEC_SHA256'),'G26_DN2_SPEC_SHA')
negative('M02_notes_canonical_pin',
         "digest(rb.canonical_bytes(notes)) == NOTES_CANONICAL_SHA256",
         "True",
         lambda m:bad_constant(m,'NOTES_CANONICAL_SHA256'),'G26_DN2_NOTES_SHA')
negative('M03_slots_authority_pin',
         "isinstance(slots, dict) and slots_pin['sha256'] == SLOTS_SHA256\n"
         "                and fm.ROOT_SLOTS_SHA256 == SLOTS_SHA256\n"
         "                and slots_pin['path'] == os.path.realpath(fm.ROOT_SLOTS_PATH)",
         "True",
         lambda m:bad_constant(m,'SLOTS_SHA256'),'G26_DN2_SLOTS_PIN')


head_copy=t.wbytes(str(WORK/'mutant_head_copy.json'),Path(head_pin['path']).read_bytes())
negative('M04_external_head_path',
         "norm['path'] == expected_path", "True",
         lambda m:execute_candidate(m,dict(input_doc,ledger_head=head_copy)),
         'G26_LEDGER_HEAD_MISMATCH')


ctx=rb._plan_context(t.pin(os.path.join(out,'BUILD_RECORD.json')),plan_pin,'mutation fixture')
def superseded(m):
    c=copy.deepcopy(ctx);c['superseded']=True
    return m.cleared_head(rb,c,head_pin)
negative('M05_superseded_head',
         "not ctx['superseded'] and ledger['results']", "ledger['results']",
         superseded,'G26_STEP7_NOT_CLEARED')


slotdoc=t.jload(b.slots['path'])
coords=copy.deepcopy(spec['coordinates'])
c=next(c for c in coords if c['scope']=='ngc3198_nuisance')
c['trial_value']=math.nextafter(c['trial_value'],math.inf)
negative('M06_coordinate_equality',
         "actual == expected, 'G26_DN2_COORDINATES_MISMATCH'",
         "True, 'G26_DN2_COORDINATES_MISMATCH'",
         lambda m:m.check_coordinates(rb,coords,slotdoc),'G26_DN2_COORDINATES_MISMATCH')
negative('M07_no_coordinate_rounding',
         "float(value).hex()", "round(float(value), 10)",
         lambda m:m.check_coordinates(rb,coords,slotdoc),'G26_DN2_COORDINATES_MISMATCH')


def manifest_guard(m):
    with patch(b.fm,_validate_manifest_structure=lambda doc,reasons:None):
        with m.manifest_dn2_guard(rb,b.fm,slotdoc,notes):
            reasons=[]
            b.fm._validate_manifest_structure({'coordinates':coords,'notes':notes},reasons)
            if reasons:
                raise rb.Refused(reasons[0])
negative('M08_manifest_prewrite_guard',
         "check_coordinates(rb, manifest.get('coordinates'), slots)\n            require",
         "pass  # mutant: no prewrite coordinates\n            require",
         manifest_guard,'G26_DN2_COORDINATES_MISMATCH')


def changed_notes(m):
    with patch(b.fm,_validate_manifest_structure=lambda doc,reasons:None):
        with m.manifest_dn2_guard(rb,b.fm,slotdoc,notes):
            reasons=[]
            b.fm._validate_manifest_structure(
                {'coordinates':spec['coordinates'],'notes':dict(notes,synthetic_changed=True)},reasons)
            if reasons:
                raise rb.Refused(reasons[0])
negative('M09_manifest_notes_guard',
         "rb.canonical_bytes(manifest.get('notes')) == rb.canonical_bytes(notes),\n"
         "                    'G26_DN2_MANIFEST_NOTES_MISMATCH'",
         "True,\n                    'G26_DN2_MANIFEST_NOTES_MISMATCH'",
         changed_notes,'G26_DN2_MANIFEST_NOTES_MISMATCH')


negative('M10_bootstrap_byte_pin',
         "if digest(raw) != BUILDER_SHA256:", "if False:",
         lambda m:(setattr(m,'BUILDER_SHA256','e'*64),m.bootstrap_builder())[1],
         'BUILDER_PIN_MISMATCH')


def derived_completeness(m):
    context=copy.deepcopy(ctx);context['plan']['phase']='PHASE_2'
    context['plan']['allow_incomplete']=False
    # Phase-2 saved plan here still has UNEVALUATED members. DN5 derives True.
    assert rb.allow_incomplete_value(context['plan']) is True
    captured=[]
    def writer(**kwargs):
        captured.append(kwargs['allow_incomplete'])
        return {'ok':False}
    with patch(rb,_plan_context=lambda *a:context,pass_driver=lambda *a:(pk,None,{})):
        with patch(b.fm,write_freeze_manifest=writer):
            try:
                execute_candidate(m)
            except (rb.Refused,KeyError):
                if captured:
                    assert captured==[False]
                    return
                raise
    raise AssertionError('missing writer witness')

# Supply real in-memory outputs so the witness reaches the writer, without
# changing the bound PASS_K byte record.
_,_,witness_memory=t.drive(env,b,out,'PASS_K')
def derived_witness(m):
    context=copy.deepcopy(ctx);context['plan']['phase']='PHASE_2'
    context['plan']['allow_incomplete']=False
    # Explicit UNEVALUATED cause in the synthetic counterfactual plan.
    context['plan']['alternatives'][0]['members'][0]['own_disposition']='UNEVALUATED_CUSTODY_BREACH'
    assert rb.allow_incomplete_value(context['plan']) is True
    captured=[]
    def writer(**kwargs):
        captured.append(kwargs['allow_incomplete']);return {'ok':False}
    with patch(rb,_plan_context=lambda *a:context,pass_driver=lambda *a:(pk,None,witness_memory)):
        with patch(b.fm,write_freeze_manifest=writer):
            try:
                execute_candidate(m)
            except rb.Refused:
                if captured:
                    assert captured==[False]
                    return 'writer reached with forbidden operator value'
                raise
    raise AssertionError('missing writer witness')
negative('M11_DN5_rederive',
         "allow = rb.allow_incomplete_value(plan)", "allow = plan.get('allow_incomplete')",
         derived_witness,'G26_ALLOW_INCOMPLETE_NOT_REDERIVED')


def writer_adapter_observation(m):
    original_result=b.fm._root_result_rows
    original_frozen=b.fm._root_frozen_rows
    changed=[]
    def writer(**kwargs):
        changed.append(b.fm._root_result_rows is not original_result and
                       b.fm._root_frozen_rows is not original_frozen)
        return {'ok':False}
    with patch(b.fm,write_freeze_manifest=writer):
        try:
            execute_candidate(m)
        except rb.Refused as exc:
            assert exc.code=='G26_WRITER_REFUSED'
    assert b.fm._root_result_rows is original_result and b.fm._root_frozen_rows is original_frozen
    return changed==[True]
old="with rb.geometry_runtime(fm, plan), manifest_dn2_guard(rb, fm, slots, notes) as seen:"
new="with manifest_dn2_guard(rb, fm, slots, notes) as seen:"
assert baseline_source.count(old)==1
changed=baseline_source.replace(old,new)
control=writer_adapter_observation(candidate(baseline_source,'adapter_control'))
mutated=writer_adapter_observation(candidate(changed,'adapter_removed'))
mutation_results.append({'id':'M12_geometry_writer_adapter','type':'positive writer boundary witness',
    'control':control,'mutant':mutated,'verdict':'KILLED' if control and not mutated else 'NOT_KILLED',
    'mutant_source_sha256':hashlib.sha256(changed.encode()).hexdigest()})


# Append a valid comparison with semantically equal, byte-different PASS_K.
compact=t.wbytes(str(WORK/'mutant_pass_compact.json'),rb.canonical_bytes(pk))
comparison,_,_=t.step7(env,out,plan_pin,p1pin,compact)
assert comparison['status']=='NO_NEW_DISCREPANCY'
compact_head=t.pin(os.path.join(t.ledger_dir(out),'STEP7_0002.json'))
negative('M13_exact_PASS_K_bytes',
         "rb.dump_bytes(record) == head_pass_raw",
         "record == rb.strict_json(head_pass_raw, 'mutant semantic comparison')",
         lambda m:execute_candidate(m,dict(input_doc,ledger_head=compact_head)),
         'G26_PASS_K_BYTES_DIFFER')


fixture.jwrite(WORK/'MUTATION_RECORD.json',{
    'schema':'G26_MUTATIONS_CX2V001','sources_from_bytes':PINS,
    'scope':__doc__,'n_mutants':len(mutation_results),
    'n_killed':sum(x['verdict']=='KILLED' for x in mutation_results),
    'mutants':mutation_results,
    'seams':'same synthetic registry and fixed constants as integration; individual gate counterfactuals are in memory',
})
print('%d/%d mutants killed'%(sum(x['verdict']=='KILLED' for x in mutation_results),len(mutation_results)))
raise SystemExit(0 if all(x['verdict']=='KILLED' for x in mutation_results) else 1)
