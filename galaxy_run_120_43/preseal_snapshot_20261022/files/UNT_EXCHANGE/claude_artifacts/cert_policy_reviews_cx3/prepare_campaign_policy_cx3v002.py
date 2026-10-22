"""0860 / D018: prepare locally, then sign only against root's actual C1 post."""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from types import SimpleNamespace

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE')
ART = BASE / 'claude_artifacts'
OUT = ART / 'cert_policy_reviews_cx3'
CHAIN = ART / 'eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4'
FINAL = OUT / 'DDO154_CERTIFICATE_POLICY_REVIEW_CAMPAIGN_CX3V002.json'
PREP = OUT / 'CAMPAIGN_POLICY_PREPARATION_CX3V002.json'
VALIDATION = OUT / 'CAMPAIGN_POLICY_VALIDATION_CX3V002.json'
WORK = '/Volumes/UNT_CAMPAIGN/DDO154_CAMPAIGN_V001'
LEDGER = {'schema': 'DDO154_CERTIFICATE_LEDGER_C2V003', 'path': WORK + '/CERTIFICATE_LEDGER.jsonl'}
PINS = {
    'prior': (OUT / 'DDO154_CERTIFICATE_POLICY_REVIEW_CAMPAIGN_CX3V001.json', '5592686026d18a69a80e2c1c7fd907d6e8a0d4294078d499a3dfdc3e85098efb'),
    'policy': (OUT / 'DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V002.json', 'cb372bdece1da31150ca99d763d7e65f5f7b0f4e323b9259ebf90c8949c06148'),
    'draft': (ART / 'root_thu_checklist_c3/c1_successor/draft_c3v001/C1_H1_DRAFT_C2V003.json', '387b1b35988e83435fc74826a744868d5ff54fbf9f52e5d5d031ef6c792ad1c1'),
    'fill': (ART / 'root_thu_checklist_c3/c1_successor/fill_c1_pin_c2v003_c3v001.py', '8a645ca33fbe630b270057da0b36a492a8886f0530148a88863d3f8d013a67b7'),
    'wrapper': (CHAIN / 'calibration_orchestrator_cx2v006r12_c4_q5b1.py', 'db0d1646af5d078a288a78ec304b37a74ac546e171a8d021a37e669255492d12'),
    'core': (CHAIN / 'calibration_core_cx2v006r12_c4.py', '192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73'),
    'guard': (ART / 'eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py', '3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25'),
    'path_ruling': (BASE / 'FROM_CODEX/0840_2026-10-21_codex3_campaign_work_dir_path_ruled_sign_now.md', '013d435339df4953e1efe4700bc248a2bb0fab9a19cfda9e6c3f2da50b0dbf7a'),
}
BINDINGS = ('driver_sha256', 'custody_deriver', 'state_enumerator', 'approved_certificate_producers',
            'guard_sha256', 'driver_slot_rule', 'post_state_handoff', 'certificate_ledger')
TAIL_DIGEST = '3c03bae3473954fdeb842de508c64702602c981675f839d604c7156b8c5db030'
CACHE = {}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def strict(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, 'DUPLICATE_KEY')
            out[k] = v
        return out
    def bad(value):
        raise ValueError('NONFINITE_' + value)
    out = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    canon(out)
    return out


def ref(key):
    p, h = PINS[key]
    return {'path': str(p), 'sha256': h}


def read(pin):
    need(set(pin) == {'path', 'sha256'}, 'EXACT_PIN')
    p = Path(pin['path'])
    need(p.is_absolute() and p.is_relative_to(BASE), 'READ_SCOPE')
    need(p.resolve() == p and all(not x.is_symlink() for x in (p, *p.parents)), 'READ_PATH')
    s = p.stat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and s.st_size <= 8388608, 'READ_FILE_TYPE')
    raw = p.read_bytes()
    need(sha(raw) == pin['sha256'], 'BYTE_PIN:' + str(p))
    CACHE[str(p)] = raw
    return raw


def expected_c1(draft, policy, utc):
    out = copy.deepcopy(draft)
    out['tail_readiness']['certificate_policy_review'] = ref('policy')
    out.pop('placeholder')
    out['schema'] = 'UNT_DDO154_C1_TAIL_READINESS_H1_C2V002'
    out['status'] = ('C1 (H1) successor C2V002 (A298), filled from the signed re-review. It is the frozen C1 once '
                     'root records it in V006. Never edited (A134 Q9).')
    out['frozen'] = {'utc': utc, 'from_draft': ref('draft'), 'certificate_policy_review': ref('policy'),
        'check_script': policy['check_script'], 'fill_tool': ref('fill'), 'synthetic_test': False,
        'c1_tail_readiness_digest_excluding_review': TAIL_DIGEST,
        'c1_tail_readiness_digest': sha(canon(out['tail_readiness']))}
    return out


def validate_c1(obj, draft, policy):
    utc = obj.get('frozen', {}).get('utc')
    need(isinstance(utc, str) and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', utc), 'C1_FREEZE_UTC')
    need(canon(obj) == canon(expected_c1(draft, policy, utc)), 'C1_DIFFERS_FROM_REVIEWED_FILL')


def validate_ruling(text, c1_sha):
    need(re.search(r'Codex3|Codex\s*\(any account\)|all[ _-]lanes', text, re.I), 'ROOT_POST_NOT_TO_LANE')
    need(c1_sha in text, 'ROOT_POST_MISSING_C1_SHA')


def policy_bindings(policy):
    return {k: copy.deepcopy(LEDGER if k == 'certificate_ledger' else policy[k]) for k in BINDINGS}


def gate_harness(policy, tail):
    wt = ast.parse(CACHE[str(PINS['wrapper'][0])])
    ct = ast.parse(CACHE[str(PINS['core'][0])])
    cls = next(n for n in wt.body if isinstance(n, ast.ClassDef) and n.name == 'Context')
    fn = lambda name: next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == name)
    nodes = [n for n in ct.body if isinstance(n, ast.FunctionDef) and n.name in ('pin_doc', 'gate_pending', 'checked_gate')]
    nodes += [fn(n) for n in ('certificate_policy_gate', 'ledger_policy_problems', 'ledger_entries')]
    expr = next(n.args[2] for n in ast.walk(fn('certificate_policy_gate')) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute) and n.func.attr == 'checked_gate')
    context = {'DRIVER_SHA': policy['driver_sha256'], 'r': tail, 'producers': tail['approved_certificate_producers'],
               'O': SimpleNamespace(sha256_file=lambda p: sha(CACHE[str(p)])),
               'G': SimpleNamespace(__file__=str(PINS['guard'][0]))}
    found = eval(compile(ast.Expression(expr), '<selected A296 binding expression>', 'eval'), {'__builtins__': {}}, context)
    need(canon(found) == canon(policy_bindings(policy)), 'ACTUAL_EIGHT_BINDINGS')
    memory = {}
    class AbsentLedger:
        def __init__(self, path):
            need(path == LEDGER['path'], 'UNEXPECTED_LEDGER_PATH')
        def exists(self):
            return False
        def read_bytes(self):
            raise AssertionError('No real ledger read is allowed')
    def read_mem(pin, label):
        raw = memory[pin['path']] if pin['path'] in memory else CACHE[pin['path']]
        need(sha(raw) == pin['sha256'], 'MEMORY_PIN')
        return raw
    env = {'json': json, 'Error': ValueError, 'POLICY_SCHEMA': policy['schema'],
           'DRIVER_SHA': policy['driver_sha256'], 'LEDGER_SCHEMA': LEDGER['schema'],
           'LEDGER_NAME': 'CERTIFICATE_LEDGER.jsonl', 'Path': AbsentLedger,
           'O': SimpleNamespace(read_pinned=read_mem, sha256_file=lambda p: sha(CACHE[str(p)])),
           'G': SimpleNamespace(__file__=str(PINS['guard'][0]))}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<selected policy functions only>', 'exec'), env)
    env['M'] = SimpleNamespace(checked_gate=env['checked_gate'], gate_pending=env['gate_pending'])
    def gate(doc, cfg_tail=None):
        r = copy.deepcopy(tail if cfg_tail is None else cfg_tail)
        raw = canon(doc)
        memory[str(FINAL)] = raw
        r['certificate_policy_review'] = {'path': str(FINAL), 'sha256': sha(raw)}
        obj = SimpleNamespace(cfg={'tail_readiness': r}, work_dir=PurePosixPath(WORK))
        obj.ledger_policy_problems = lambda: env['ledger_policy_problems'](obj)
        obj.ledger_entries = lambda: env['ledger_entries'](obj)
        return env['certificate_policy_gate'](obj)
    return gate


def make_review(prior, policy, c1_ref):
    out = copy.deepcopy(prior)
    out.update(policy_bindings(policy))
    out.update(frozen_c1=c1_ref, inherited_policy_review=ref('policy'),
               check_script={'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())},
               q8_rule=policy['q8_rule'], disclosure=policy['disclosure'],
               eight_bindings_digest=sha(canon(policy_bindings(policy))),
               scope='D018 / 0860 campaign certificate-policy binding to root-frozen C1 C2V002, the seven proof producers and A296 guard.',
               post_state_policy='Campaign acceptance-step adoption and execution remain root dependencies. This review changes no acceptance classification, rerun rule or scientific threshold.',
               validation_scope='TESTED selected A296 r12 wrapper/core policy functions with an absent-ledger stand-in. No production Context, guard, verifier or volume is executed or opened.')
    need(out['planned_work_dir'] == WORK and out['certificate_ledger'] == LEDGER
         and out['root_path_ruling'] == ref('path_ruling'), 'PLANNED_PATH_CHANGED')
    for k in BINDINGS:
        if k not in ('approved_certificate_producers', 'guard_sha256'):
            need(canon(out[k]) == canon(prior[k]), 'OTHER_BINDING_CHANGED:' + k)
    return out


def controls(review, gate, tail, draft, policy):
    cases = []
    def record(label, ok):
        cases.append({'id': label, 'status': 'PASS' if ok else 'FAIL'})
    record('exact_eight_binding_gate', gate(review)['ok'] is True)
    for key in BINDINGS:
        mutant = copy.deepcopy(review)
        mutant[key] = None
        record('refuse_binding_' + key, gate(mutant)['ok'] is False)
    for key, value in [('ok', False), ('status', 'UNTESTED'), ('schema', 'WRONG')]:
        mutant = copy.deepcopy(review)
        mutant[key] = value
        record('refuse_review_' + key, gate(mutant)['ok'] is False)
    for key, value in [('path', WORK + '_OTHER/CERTIFICATE_LEDGER.jsonl'), ('schema', 'WRONG')]:
        mutant = copy.deepcopy(tail)
        mutant['certificate_ledger'][key] = value
        record('refuse_ledger_' + key, gate(review, mutant)['ok'] is False)
    fixture = expected_c1(draft, policy, '2000-01-01T00:00:00Z')
    validate_c1(fixture, draft, policy)
    record('in_memory_C1_standin_contract', True)
    mutants = []
    for key, value in [('certificate_policy_review', {'path': 'wrong', 'sha256': '0' * 64}),
                       ('candidate_K_big_inverse_kpc', 64),
                       ('approved_certificate_producers', policy['approved_certificate_producers'][:-1])]:
        m = copy.deepcopy(fixture)
        m['tail_readiness'][key] = value
        mutants.append(('C1_tail_' + key, m))
    for label, field, value in [('C1_wrong_schema', 'schema', 'WRONG'),
                                ('C1_placeholder_retained', 'placeholder', {})]:
        m = copy.deepcopy(fixture)
        m[field] = value
        mutants.append((label, m))
    m = copy.deepcopy(fixture)
    m['frozen']['synthetic_test'] = True
    mutants.append(('C1_test_fill_refused', m))
    for label, mutant in mutants:
        try:
            validate_c1(mutant, draft, policy)
            ok = False
        except ValueError:
            ok = True
        record('refuse_' + label, ok)
    validate_ruling('To Codex3: new C1 ' + 'a' * 64, 'a' * 64)
    record('root_post_exact_sha', True)
    try:
        validate_ruling('To Codex3: no new pin yet', 'a' * 64)
        ok = False
    except ValueError:
        ok = True
    record('refuse_missing_root_C1_sha', ok)
    need(all(x['status'] == 'PASS' for x in cases), 'CONTROL_FAILURE')
    return cases


def write_new(path, obj):
    with path.open('xb') as handle:
        handle.write(encoded(obj))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--prepare', action='store_true')
    for key in ('c1', 'c1-sha256', 'root-dispatch', 'root-dispatch-sha256'):
        ap.add_argument('--' + key)
    args = ap.parse_args()
    supplied = [args.c1, args.c1_sha256, args.root_dispatch, args.root_dispatch_sha256]
    need(not any(supplied) if args.prepare else all(supplied), 'PREPARE_OR_ALL_FOUR_FINALIZE_ARGUMENTS')
    def audit(event, values):
        if event.startswith('socket.') or event in ('os.system', 'os.fork', 'os.posix_spawn'):
            raise PermissionError('Network/process forbidden')
        if event == 'subprocess.Popen':
            need(values[0] == '/bin/date' and values[1][:2] == ['/bin/date', '-u'], 'ONLY_DATE_PROCESS')
        if event == 'open' and isinstance(values[0], (str, bytes)):
            path = os.fsdecode(values[0])
            need(not path.startswith('/Volumes/'), 'NO_VOLUME_OPEN')
    sys.addaudithook(audit)
    for key in PINS:
        read(ref(key))
    prior, policy, draft = [strict(CACHE[str(PINS[k][0])]) for k in ('prior', 'policy', 'draft')]
    need(policy['ok'] is True and not policy['blocking_findings'], 'C1_POLICY_NOT_PASS')
    need(policy['reviewed_c1_draft'] == ref('draft') and policy['c1_tail_readiness_digest_excluding_review'] == TAIL_DIGEST, 'C1_POLICY_SCOPE')
    for pin in [policy['certificate_registry'], policy['custody_deriver'], policy['state_enumerator'],
                policy['check_script'], *policy['approved_certificate_producers']]:
        read(pin)
    tail = copy.deepcopy(draft['tail_readiness'])
    need(sha(canon({k: v for k, v in tail.items() if k != 'certificate_policy_review'})) == TAIL_DIGEST, 'DRAFT_TAIL_DIGEST')
    tail['certificate_ledger'] = copy.deepcopy(LEDGER)
    gate = gate_harness(policy, tail)
    root_ref = None
    if args.prepare:
        c1_ref = {'path': 'IN_MEMORY_STANDIN_NOT_A_C1_FILE', 'sha256': sha(canon(expected_c1(draft, policy, '2000-01-01T00:00:00Z')))}
    else:
        c1_ref = {'path': args.c1, 'sha256': args.c1_sha256}
        need(Path(args.c1).parent == ART / 'c1_h1_c2', 'C1_PARENT')
        root_ref = {'path': args.root_dispatch, 'sha256': args.root_dispatch_sha256}
        need(Path(args.root_dispatch).parent == BASE / 'FROM_CODEX'
             and re.match(r'\d{4}_', Path(args.root_dispatch).name), 'NUMBERED_ROOT_POST_REQUIRED')
        text = read(root_ref).decode()
        validate_ruling(text, args.c1_sha256)
        c1 = strict(read(c1_ref))
        validate_c1(c1, draft, policy)
    review = make_review(prior, policy, c1_ref)
    cases = controls(review, gate, tail, draft, policy)
    sources = [{'path': p, 'sha256': sha(raw)} for p, raw in sorted(CACHE.items())]
    for pin in sources:
        need(sha(Path(pin['path']).read_bytes()) == pin['sha256'], 'SOURCE_CHANGED')
    tool = {'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())}
    record = {'schema': 'CX3_CAMPAIGN_A296_POLICY_PREPARATION_V002', 'status': 'TESTED', 'checks': cases,
              'n_pass': len(cases), 'n_total': len(cases), 'sources': sources, 'tool': tool,
              'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
              'scope': 'Selected policy functions only, in-memory C1 stand-in and absent-ledger branch. No real C1 freeze or campaign Context. No producer, guard or verifier executed. No volume opened.',
              'real_C1_and_root_post_checked': not args.prepare}
    if args.prepare:
        record['production_signature_written'] = False
        record['mode'] = 'PREPARATION_ONLY'
        write_new(PREP, record)
        print(json.dumps({'preparation': {'path': str(PREP), 'sha256': sha(PREP.read_bytes())},
                          'checks': len(cases), 'production_signature_written': False}))
        return
    review.update(sources=sources, checks=cases, root_c1_ruling=root_ref,
                  date_u=subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
                  signed_utc=subprocess.check_output(['/bin/date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], text=True).strip())
    need(gate(review)['ok'] is True, 'FINAL_REVIEW_GATE')
    write_new(FINAL, review)
    saved = strict(FINAL.read_bytes())
    need(gate(saved)['ok'] is True, 'SAVED_REVIEW_GATE')
    record['review'] = {'path': str(FINAL), 'sha256': sha(FINAL.read_bytes())}
    record['mode'] = 'ROOT_C1_FINALIZATION'
    write_new(VALIDATION, record)
    print(json.dumps({'review': record['review'], 'checks': len(cases),
                      'validation': {'path': str(VALIDATION), 'sha256': sha(VALIDATION.read_bytes())}}))


if __name__ == '__main__':
    main()
