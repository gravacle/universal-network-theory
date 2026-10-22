"""KS6 handoff (ks_k3_chain_c2 c2v001; root A160): acceptance_handoff_c2v004 (5ff464cc) with the KS6 LO adapter for
S1_UA_C3T only.

accept_call hands every spec that is not S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise) to the unchanged
5ff464cc module object (P, by path and sha): its records, the handoff pin and LO_ADAPTER 211a3220 included, are
5ff464cc's. For S1_UA_C3T the handoff is 5ff464cc's code with LO_ADAPTER_KS6 (the KS6 adapter) in place of LO_ADAPTER.
load_deps accepts either adapter pin (deps carry no spec); each accept_call path checks its own. Root supplies the other
deps, as before; for S1_UA_C3T they must be K=3-capable (lo_core KS6, guard KS5; enumerator/evidence/SRB successors
are open items for root). The 5ff464cc text follows.

Q2 acceptance input side, part 3 (A134; rulings 56774ba7 Q2, Q3, Q4(c), Q5 readings, Q10): the acceptance handoff.

Root runs accept_call() once per tail-ON direct call (HEADLINE11, SENS_LO9, SENS_HI9) after the call's FINISHED
receipt and before any value from the call is scored, adopted, handed to the engine, used in R-A4/H3 or SENS, or
reported. It is glue around pinned, unchanged producers and verifiers. It never writes a proof and never approves:
- inputs: replay_inputs_writer_c2v002 (plan/descriptors/I1-T packets), row_reference_producer_c2v003 (row records);
- inventory: the C1 state enumerator (consumed_states_cx2v010 e48cca3c, or its successor), unchanged;
- per state: current_source_evidence export_lo_source (v004 7289f2ba or its b1 successor) for the source
  reconstruction and the GQ premises (nonnegative) / GQ_SIGNED (offset); the state input below;
- LO for every state (v003, A138 V01(a), the A134 split): Claude3's call-level adapt_call_lo, by the exact path and sha
  in LO_ADAPTER. It runs the unchanged lo_core produce_current_lo (12d36305) on each state input and returns the
  per-state verdicts and guard LO proofs, which this handoff adopts. The handoff no longer calls lo_core itself;
- accepted final-rotation state only (0690 OPEN-3: the unique own_source_state at le{final_pass}_rotation): Claude3's
  SRB-ROT adapter (Q10; adapt_call_srb_rot signature), which carries AMB-04, fed the rows input that
  row_reference_producer extracts from that stage's own outputs (OPEN-10/11);
- verification: the guard acceptance phase (certificate_guard verify_bundle L155-219) directly, or the wrapper
  successor's write_acceptance / certificate_check(spec,'acceptance') (Q3).
Readings are the frozen Q5/Q10 texts with the A134 reading points of FROM_CODEX/0690 (OPEN-4/5/6), applied
mechanically (READINGS below). Every per-state result is preserved.
v002: a later acceptance pass on the same call reuses the call's byte-verified plan and input set (writer v002), and
writes its TailState exports into a fresh attempt directory, so a pass before the G1/review rulings never blocks the
call (A115(a)).
v003 (A138 V01; Claude3 0196 V01): (a) the LO adapter call above; (b) every state input carries `execution`
{fresh_call, resumed, retried, route_a_completed_normally, run_root}, read from the call's own records
(execution_block), and every row reference carries `state_files` (the call's own out/result.json pin; row producer
v003). Everything else is v002's behaviour, including the 10-key bitwise rho check, now applied to the adapter's core
record of each state.
v004 (A145; Claude3 0208 N4, N5; v003 verify notes N2, N4): (a) LO_ADAPTER pins Claude3's published proof side c3v003
adapter (211a3220: A138 V02 b1 enumerator 4ca7f364, V03 10-key rho, B3 0690 OPEN-6 call reading); (b) adopt_lo adopts
an adapter PASS only with an exact core_record pin, so the 10-key rho check has run on every adopted PASS (N2);
(c) route_a_completed_normally needs converged_finite_fixed_point is True, as consumed_states_cx2v005 L237 does (N4);
(d) root's trusted_source_producers must name the b1 evidence module 7044e131 (export_lo_source; offset_b1 README item
5, 0208 N5). Without it the handoff records a blocker and the call reads INCOMPLETE; root's list is forwarded to both
adapters unchanged. Everything else is v003's behaviour.
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
ANCHOR_POINT = '8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8'   # TAIL_REANCHOR (brief table row 1)
STATE_SCHEMA = 'UNT_POINT_LO_STATE_INPUT_CX2V001'          # lo_core L34, L195
SOURCE_SCHEMA = 'UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001'  # evidence L348
RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'             # point_response_producer L30
RECORD_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'
REQUESTS_SCHEMA = 'DDO154_CURRENT_SOURCE_REVIEW_REQUESTS_C2V001'
LO_THRESHOLD_BLOCKER = 'LO_NUMERICAL_INDICATOR_ABOVE_THRESHOLD'   # lo_core L258-259
# A138 V01(a): Claude3's per-state LO adapter, by exact path and sha. v004 (A145): the published proof side c3v003
# (Claude3 0208), which carries the A138 V02 (b1 enumerator 4ca7f364) and V03 (10-key rho) errata and B3.
LO_ADAPTER = {'path': str(ART / 's4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py'),
              'sha256': '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c',
              'entry': 'adapt_call_lo'}
# v004 (A145; offset_b1 README item 5; Claude3 0208 N5): with b1 inventories export_lo_source is the b1 evidence module,
# so root's trusted_source_producers must name it. The handoff only checks the list; it never adds to it.
# KS6 (A160): the KS6 adapter, for S1_UA_C3T only; 5ff464cc itself, for every other spec.
LO_ADAPTER_KS6 = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/lo_state_proof_adapter_c3v003_ks6_c2v001.py',
                  'sha256': '8fa371a719b41c174175942308ca64bebe40fb1e0d42b99ae27def939cbe6c33', 'entry': 'adapt_call_lo'}
PREDECESSOR = {'path': str(ART / 's4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py'),
               'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}
CB_PIN = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
          'sha256': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'}
S1_C3T_LABEL = re.compile(r'S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}')
B1_EVIDENCE = {'path': str(ART / 's4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py'),
               'sha256': '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'}
B1_UNTRUSTED_BLOCKER = 'TRUSTED_SOURCE_PRODUCERS_WITHOUT_B1_EVIDENCE_7044E131 (offset_b1 README item 5; Claude3 0208 N5)'
LO_ADAPTER_DIR = 'LO_ADAPTER_C3'                           # adapter out_root, inside this pass's records dir
# A138 V01(b): lo_producer_cx2v004 L56-59 keys, read from the call's own records by the 0528 rule that discovery
# consumed_states_cx2v005 fresh_scope (L223-257) applies. A value the records do not establish is None (refused).
EXECUTION_RULE = ('A138 V01(b); keys of lo_producer_cx2v004 L56-59; values read from this call by the 0528 rule of '
                  'consumed_states_cx2v005 fresh_scope L223-257: fresh_call = discovery coverage FRESH_COMPLETED, no '
                  'spec.admit, result and out/finish.json COMPLETED and valid, finish bound to this result; retried = '
                  'finish.retries != 0 or more than one route_a stage record; resumed = the single route_a stage argv '
                  'lacks --start-iteration 0, or carries a resume/retry flag, or a --checkpoint-mode other than new; '
                  'route_a_completed_normally = that stage executed with exit 0, route_a_outcome CONVERGED / '
                  'converged_finite_fixed_point is True / CONVERGED_FINITE_FIXED_POINT, identity.route_a.mode computed; '
                  'run_root = <call>/out')
FRESH_SCOPE = 'FRESH_COMPLETED'                            # consumed_states_cx2v005 L474
ROUTE_A_CONVERGED = {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                     'outcome': 'CONVERGED_FINITE_FIXED_POINT'}   # consumed_states_cx2v005 L236-239
# Call reading precedence. Every per-state reading is recorded; the call reads the first that applies.
READINGS = ('NON_LAPSE_TAIL_MATERIAL',      # Q5: actual LO failure at the accepted / an inherited route-A state or a route-B stage state
            'BOUND_INSUFFICIENT',           # Q10: unflagged SRB-ROT fail
            'UNDECIDABLE_FLAGGED',          # Q10/AMB-04: SRB-ROT fail on a TAIL_SOURCE_UNDERCONVERGED call
            'LO_UNCERTIFIED_TRANSIENT',     # Q5: LO failure confined to route-A iterates other than the accepted state
                                            #     (0690 OPEN-6: needs every non-iterate state at PASS; else INCOMPLETE)
            'INCOMPLETE',                   # Q3: some consumed state lacks LO, GQ or the Q10 bound at TESTED/PASS
            'ACCEPTED_PASS_FLAGGED',        # Q10/AMB-04: every gate PASS; SRB-ROT pass on a flagged call
            'ACCEPTED')                     # Q3: every consumed state LO, GQ and Q10 at TESTED/PASS; guard ok
NOT_MODEL_OUTPUT = ('NON_LAPSE_TAIL_MATERIAL', 'BOUND_INSUFFICIENT')
# 0690 OPEN-5: any LO FAIL at the anchor reads the step-4 stop, the class reading recorded beside it. v001's
# call-reading stops are kept (conservative: an SRB-ROT failure at the anchor also stops for root).
ANCHOR_STOP = ('NON_LAPSE_TAIL_MATERIAL', 'LO_UNCERTIFIED_TRANSIENT', 'BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED')
TAILSTATES_DIR = 'ACCEPTANCE_TAILSTATES_C2V002_A%03d'      # one directory per acceptance pass (v002)
MAX_ATTEMPTS = 999
SRB_READINGS = {False: ('PASS', 'BOUND_INSUFFICIENT'), True: ('PASS_FLAGGED', 'UNDECIDABLE_FLAGGED')}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and \
        isinstance(x['sha256'], str) and len(x['sha256']) == 64


def read_ref(ref):
    raw = Path(ref['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise ValueError('byte pin mismatch: ' + str(ref['path']))
    return json.loads(raw)


def load_pinned(ref, name):
    """Load a module from its canonical path after checking its bytes (proof producer pins are path+sha, R4)."""
    p = Path(ref['path'])
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        raise ValueError('module pin mismatch: ' + str(p))
    sp = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, str(p), 'exec'), m.__dict__)
    return m


_CB = {}


def _s1_c3t_spec(spec):
    """KS6 gate (as KS1's): the S1 C3T label AND composite_grid_spec == CB C3T bitwise; other labels never read CB."""
    lab = spec.get('label') if isinstance(spec, dict) else None
    if not (isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None):
        return False
    try:
        grid = spec['numerics']['composite_grid_spec']
        if not _CB:
            raw = Path(CB_PIN['path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
                raise ValueError('CB case block: sha256 mismatch')
            _CB['C3T'] = json.loads(raw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']
        return canonical(grid) == canonical(copy.deepcopy(_CB['C3T']))
    except (KeyError, TypeError, ValueError):
        return False


def load_deps(pins):
    """pins: enumerator, evidence, lo_core, guard, writer, row_producer as {path, sha256}; lo_adapter and srb_adapter
    as {path, sha256, entry}. Root supplies them (C1 and the A134 build table); nothing here chooses a version,
    except that the LO adapter must be exactly LO_ADAPTER (A138 V01(a)).
    v002: the srb_adapter entry is called with srb_rot_adapter_c3v001.adapt_call_srb_rot's signature.
    v003: lo_core is used for point_context only; the lo_adapter entry is adapt_call_lo."""
    if pins.get('lo_adapter') not in (LO_ADAPTER, LO_ADAPTER_KS6):   # KS6: accept_call checks the one its spec needs
        raise ValueError('LO_ADAPTER_PIN_NOT_A138 (the handoff calls only %s %s)' % (LO_ADAPTER['path'], LO_ADAPTER['sha256']))
    d = {k: load_pinned(pins[k], 'q2_acceptance_' + k) for k in ('enumerator', 'evidence', 'lo_core', 'guard', 'writer', 'row_producer')}
    for k in ('lo_adapter', 'srb_adapter'):
        m = load_pinned(pins[k], 'q2_acceptance_' + k)
        d[k] = getattr(m, pins[k]['entry'])
    d['pins'] = pins
    return d


def lo_adapter_problem(deps, want=LO_ADAPTER):
    """A138 V01(a): the callable is the pinned adapt_call_lo, compiled from the pinned file, whose bytes still match.
    KS6: want is LO_ADAPTER_KS6 on the S1_UA_C3T path."""
    fn = deps.get('lo_adapter')
    if (deps.get('pins') or {}).get('lo_adapter') != want:
        return 'LO_ADAPTER_PIN_NOT_A138 (required %s %s)' % (want['path'], want['sha256'])
    if getattr(fn, '__name__', None) != want['entry'] or \
            getattr(getattr(fn, '__code__', None), 'co_filename', None) != want['path']:
        return 'LO_ADAPTER_CALLABLE_NOT_THE_PINNED_ENTRY'
    if sha_file(want['path']) != want['sha256']:
        return 'LO_ADAPTER_BYTES_CHANGED'
    return None


def execution_block(*, call, spec, result, result_ref, discovery):
    """A138 V01(b): the execution facts of lo_producer_cx2v004 L56-59, each read from this call's own records
    (EXECUTION_RULE). Nothing is assumed: a fact the records do not establish stays None, and the adapter refuses it."""
    out = call / 'out'
    ex = {'fresh_call': None, 'resumed': None, 'retried': None, 'route_a_completed_normally': None, 'run_root': str(out)}
    try:
        fin_raw = (out / 'finish.json').read_bytes()
        fin = json.loads(fin_raw)
        stages = [r for r in result.get('stage_records') or [] if isinstance(r, dict) and r.get('kind') == 'route_a']
        argv = stages[0].get('argv') if len(stages) == 1 else None
        argv = argv if isinstance(argv, list) and all(isinstance(x, str) for x in argv) else None

        def value(flag):
            if argv is None or argv.count(flag) != 1 or argv.index(flag) + 1 >= len(argv):
                return None
            return argv[argv.index(flag) + 1]
        retries = fin.get('retries')
        if len(stages) > 1 or (type(retries) is int and retries != 0):
            ex['retried'] = True
        elif len(stages) == 1 and type(retries) is int and retries == 0:
            ex['retried'] = False
        if argv is not None:
            flags = [x.casefold() for x in argv if x.startswith('--')]
            ex['resumed'] = not (value('--start-iteration') == '0' and not any('resume' in f or 'retry' in f for f in flags)
                                 and ('--checkpoint-mode' not in argv or value('--checkpoint-mode') == 'new'))
        if len(stages) == 1:
            st = stages[0]
            outcome = result.get('route_a_outcome') or {}
            ex['route_a_completed_normally'] = (
                st.get('executed') is True and type(st.get('exit_code')) is int and st['exit_code'] == 0
                and all(outcome.get(k) == v for k, v in ROUTE_A_CONVERGED.items())
                and outcome.get('converged_finite_fixed_point') is True     # v004 (verify N4): is True, as v005 L237
                and ((result.get('identity') or {}).get('route_a') or {}).get('mode') == 'computed')
        scope = ((discovery or {}).get('coverage') or {}).get('fresh_call_scope')
        ex['fresh_call'] = (scope == FRESH_SCOPE and not spec.get('admit') and result.get('status') == 'COMPLETED'
                            and result.get('valid') is True and fin.get('status') == 'COMPLETED' and fin.get('valid') is True
                            and fin.get('result_sha256') == result_ref['sha256'])
        ex['basis'] = {'rule': EXECUTION_RULE, 'discovery_fresh_call_scope': scope, 'route_a_stage_records': len(stages),
                       'finish': {'path': str((out / 'finish.json').resolve()), 'sha256': hashlib.sha256(fin_raw).hexdigest()}}
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        ex['basis'] = {'rule': EXECUTION_RULE, 'not_established': '%s: %s' % (type(exc).__name__, exc)}
    return ex


class Store:
    """Exclusive-create JSON writer for one call's acceptance records (under claude_artifacts: guard L37-55)."""

    def __init__(self, records_dir):
        self.dir = Path(records_dir).resolve()
        if not self.dir.is_relative_to(ART):
            raise ValueError('RECORDS_DIR_OUTSIDE_CLAUDE_ARTIFACTS (the guard reads bundle and proofs only there)')
        if any(s.casefold().startswith('uvt_') or 'ngc3198' in s.casefold() or s.casefold() == 'kmax_a2f10_c5h_run_v001'
               for s in self.dir.parts):
            raise ValueError('RECORDS_DIR_FORBIDDEN_COMPONENT')
        self.dir.mkdir(parents=True, exist_ok=False)
        self.tdir = None
        self.files = []

    def open_tailstates(self, tailstate_dir, call):
        """v002: called inside accept_call's try, so a refusal is recorded. Default: the call's first free
        ACCEPTANCE_TAILSTATES_C2V002_A<nnn> (created exclusively; one per pass)."""
        if tailstate_dir is not None:
            Path(tailstate_dir).mkdir(exist_ok=False)
            self.tdir = Path(tailstate_dir)
            return self.tdir
        for n in range(1, MAX_ATTEMPTS + 1):
            try:
                (call / (TAILSTATES_DIR % n)).mkdir(exist_ok=False)
                self.tdir = call / (TAILSTATES_DIR % n)
                return self.tdir
            except FileExistsError:
                continue
        raise ValueError('TAILSTATE_ATTEMPTS_EXHAUSTED')

    def put(self, name, obj, where=None):
        p = (where or self.dir) / name
        raw = canonical(obj) + b'\n'
        with open(p, 'xb') as f:
            f.write(raw)
        ref = {'path': str(p.resolve()), 'sha256': hashlib.sha256(raw).hexdigest()}
        self.files.append(ref)
        return ref

    def put_arrays(self, name, arrays):
        p = self.tdir / name
        with open(p, 'xb') as f:
            np.savez(f, **arrays)
        ref = {'path': str(p.resolve()), 'sha256': sha_file(p)}
        self.files.append(ref)
        return ref


_PRED = {}


def _predecessor():
    """KS6: 5ff464cc, unchanged, by path and sha (loaded on first use)."""
    if 'm' not in _PRED:
        _PRED['m'] = load_pinned(PREDECESSOR, 'ks6_predecessor_acceptance_handoff_c2v004')
    return _PRED['m']


def receipt_ok(receipt_ref, result_sha):
    """Q2/Q3: run only after the FINISHED receipt (same fields wrapper r10_c4 L109-113 requires)."""
    rc = read_ref(receipt_ref)
    return (rc.get('status') == 'FINISHED' and rc.get('driver_status') == 'COMPLETED'
            and (rc.get('result') or {}).get('sha256') == result_sha)


def state_class(state, accepted_digest):
    if state['stage_kind'] != 'route_a':
        return 'ROUTE_B_STAGE'
    return 'ACCEPTED_ROUTE_A' if state['state_sha256'] == accepted_digest else 'ROUTE_A_ITERATE'


def tail_state_refs(store, deps, state, occurrence, manifest, accepted_digest, tag):
    """Saved TailState for lo_core (record JSON + arrays npz). The accepted route-A state reuses the call's own
    manifest arrays; any other state is the pinned reconstruction's static replay of its descriptor."""
    if state['stage_kind'] == 'route_a' and state['state_sha256'] == accepted_digest:
        return {'record': store.put(tag + '_TAILSTATE_RECORD.json', manifest['state']['record'], store.tdir),
                'arrays': {'path': manifest['state']['arrays']['path'], 'sha256': manifest['state']['arrays']['sha256']}}
    _, p = deps['evidence'].R.replay_state(occurrence['reconstruction'])
    if p.state_sha256 != state['state_sha256']:
        raise ValueError('REPLAYED_STATE_DIFFERS_FROM_INVENTORY')
    return {'record': store.put(tag + '_TAILSTATE_RECORD.json', p.state.record, store.tdir),
            'arrays': store.put_arrays(tag + '_TAILSTATE_ARRAYS.npz', p.state.to_arrays())}


# Q5: the rho acceptance recomputes must equal the slot's registered rho record bitwise. Same key set as the
# wrapper_q5 successor's acceptance check (wrapper_q5 README, L148-161 change): run metadata and provenance pins excluded.
# A138 V03 rules this 10-key form for the adapter too; v003 applies it to the adapter's core record of each state.
RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')


def rho_bitwise(lo, slot):
    rho = lo.get('rho') or {}
    if slot.get('schema') != RHO_SCHEMA or slot.get('full_registered_search_executed') is not True:
        return False
    return all(k in rho and k in slot for k in RHO_COMPARE_KEYS) and \
        canonical({k: rho[k] for k in RHO_COMPARE_KEYS}) == canonical({k: slot[k] for k in RHO_COMPARE_KEYS})


def adopt_lo(rec, lo_call, slot):
    """v003: adopt adapt_call_lo's per-state verdicts (A138 V01(a)). A PASS state carries the adapter's guard LO proof;
    a FAIL state reads LO_ABOVE_THRESHOLD; anything else stays UNAVAILABLE with the adapter's blockers. v002's
    10-key bitwise rho check is applied to the adapter's core record of the state.
    v004 (verify N2): a PASS is adopted only when its core_record is an exact {path, sha256} pin, so that check ran."""
    by_state = {}
    for s in lo_call.get('states') or []:
        if isinstance(s, dict) and isinstance(s.get('state'), dict):
            by_state.setdefault(digest(s['state']), []).append(s)
    call_blockers = [str(b) for b in lo_call.get('blockers') or []]
    for entry in rec['states']:
        got = by_state.get(digest(entry['state'])) or []
        if len(got) != 1:
            entry['blockers'].append('LO_ADAPTER_STATE_RESULT_UNAVAILABLE' + (': ' + '; '.join(call_blockers) if call_blockers else ''))
            continue
        a = got[0]
        entry['lo_adapter_state'] = {k: a.get(k) for k in ('verdict', 'reading', 'state_class', 'blockers', 'record', 'core_record')}
        if is_pin(a.get('core_record')):
            try:
                core = read_ref(a['core_record'])
            except (OSError, ValueError) as exc:
                entry['blockers'].append('LO_CORE_RECORD_UNREADABLE: %s: %s' % (type(exc).__name__, exc))
                continue
            entry['lo_record'] = a['core_record']
            entry['summed_max_over_tau'] = core.get('summed_max_over_tau')
            entry['lo_blockers'] = list(core.get('blockers') or [])
            entry['rho_bitwise_equal_to_slot'] = rho_bitwise(core, slot)
            if not entry['rho_bitwise_equal_to_slot']:
                entry['blockers'].append('RHO_NOT_BITWISE_EQUAL_TO_SLOT')
        elif a.get('verdict') == 'PASS':     # v004 (verify N2): no PASS without the core record the rho check reads
            entry['blockers'].append('LO_ADAPTER_PASS_WITHOUT_EXACT_CORE_RECORD_PIN')
        if entry['blockers']:
            entry['blockers'] += [str(b) for b in a.get('blockers') or []]
        elif a.get('verdict') == 'PASS' and is_pin(a.get('record')):
            entry['LO'] = a['record']
            entry['reading'] = 'PASS'
        elif a.get('verdict') == 'FAIL' and entry.get('lo_blockers') == [LO_THRESHOLD_BLOCKER]:
            entry['reading'] = 'LO_ABOVE_THRESHOLD'
        else:
            entry['blockers'] += ([b for b in entry.get('lo_blockers') or [] if b != LO_THRESHOLD_BLOCKER] +
                                  [str(b) for b in a.get('blockers') or []]) or ['LO_ADAPTER_STATE_NOT_PASS_OR_FAIL']


def accept_call(*, call_dir, spec, deps, policy, records_dir, tailstate_dir=None, mode='guard', wrapper_context=None,
                initial_rings_ref=None, final_next_gas_ref=None):
    if not _s1_c3t_spec(spec):                        # KS6: 5ff464cc's own code path
        return _predecessor().accept_call(call_dir=call_dir, spec=spec, deps=deps, policy=policy, records_dir=records_dir,
                                          tailstate_dir=tailstate_dir, mode=mode, wrapper_context=wrapper_context,
                                          initial_rings_ref=initial_rings_ref, final_next_gas_ref=final_next_gas_ref)
    t0 = time.monotonic()
    timing = {}
    call = Path(call_dir).resolve(strict=True)
    out = call / 'out'
    store = Store(records_dir)
    rec = {'schema': RECORD_SCHEMA, 'call_dir': str(call), 'mode': mode, 'reading': 'INCOMPLETE', 'blockers': [],
           'states': [], 'srb_rot': None, 'guard': None, 'handoff': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
           'pins': deps.get('pins')}

    def finish():
        rec['outputs_are_evidence'] = rec['reading'] in ('ACCEPTED', 'ACCEPTED_PASS_FLAGGED')
        rec['rows_are_model_output'] = (True if rec['outputs_are_evidence'] else
                                        False if rec['reading'] in NOT_MODEL_OUTPUT else None)
        lo_fail = [e['state'] for e in rec['states'] if e.get('reading') == 'LO_ABOVE_THRESHOLD']
        anchor = rec.get('point_sha256') == ANCHOR_POINT
        rec['step4_stop_for_root_ruling'] = anchor and (bool(lo_fail) or rec['reading'] in ANCHOR_STOP)   # 0690 OPEN-5
        rec['step4_stop_basis'] = ((['ANCHOR_LO_FAIL'] if lo_fail else []) +
                                   (['ANCHOR_CALL_READING_' + rec['reading']] if rec['reading'] in ANCHOR_STOP else [])) if anchor else []
        rec['timing_seconds'] = dict(timing, total=time.monotonic() - t0)
        rec['files'] = list(store.files)
        return store.put('ACCEPTANCE_RECORD.json', rec)

    try:
        bad = lo_adapter_problem(deps, LO_ADAPTER_KS6)   # v003: A138 V01(a), before anything is read (KS6 adapter)
        if bad:
            rec['blockers'].append(bad)
            return rec, finish()
        result_raw = (out / 'result.json').read_bytes()
        result = json.loads(result_raw)
        result_ref = {'path': str((out / 'result.json').resolve()), 'sha256': hashlib.sha256(result_raw).hexdigest()}
        rec['result'] = result_ref
        if not receipt_ok(policy['receipt'], result_ref['sha256']):
            rec['blockers'].append('FINISHED_RECEIPT_REQUIRED')
            return rec, finish()
        # 1. inputs and the complete consumed-state inventory (v010, unchanged)
        s = time.monotonic()
        discovery = deps['enumerator'].D.consumed_states(spec=spec, result=result, call_dir=call)
        w = deps['writer'].write_replay_inputs(call_dir=call, spec=spec, result=result, discovery=discovery,
                                               initial_rings_ref=initial_rings_ref, final_next_gas_ref=final_next_gas_ref)
        rec['writer'] = {'status': w['status'], 'report': w['report'], 'plan': w['plan']}
        timing['writer'] = time.monotonic() - s
        if w['status'] not in ('WRITTEN', 'REUSED'):     # v002: REUSED = the call's existing plan, checked from bytes
            rec['blockers'] += ['REPLAY_INPUTS_UNAVAILABLE: %s' % g['code'] for g in w['gaps']]
            return rec, finish()
        s = time.monotonic()
        inv = deps['enumerator'].consumed_states(spec=spec, result=result, call_dir=str(call))
        timing['inventory'] = time.monotonic() - s
        rec['inventory'] = {'complete': inv.get('complete'), 'states': inv.get('states'), 'blockers': inv.get('blockers')}
        if inv.get('complete') is not True:
            rec['blockers'].append('COMPLETE_CONSUMED_STATE_INVENTORY_UNAVAILABLE')
            return rec, finish()
        # v003: A138 V01(b), the execution facts every state input carries
        rec['execution'] = execution = execution_block(call=call, spec=spec, result=result, result_ref=result_ref,
                                                       discovery=discovery)
        # 2. point context once per call (lo_core.PR.point_context; custody details inside)
        s = time.monotonic()
        ctx = deps['lo_core'].PR.point_context(spec)
        details = ctx['details']
        timing['point_context'] = time.monotonic() - s
        rec['point_sha256'] = point = details['point_sha256']
        prelaunch = read_ref(policy['prelaunch_bundle'])
        uniform_gq = prelaunch['prelaunch']['GQ']
        slot = read_ref(spec['numerics']['uv_tail']['lo_certificate'])
        manifest = read_ref(result['uv_tail']['manifest'])
        accepted_digest = manifest['state']['digest']
        rcs = details['custody']['row_contract_sha256']
        row_review = policy['row_policy_reviews'].get(rcs)
        flags = ((result.get('uv_tail') or {}).get('route_a_record') or {}).get('flags')
        requests = []
        by_state = {}
        for j in inv['joined_occurrences']:
            by_state.setdefault(digest(j['state']), j)
        rec['tailstate_dir'] = str(store.open_tailstates(tailstate_dir, call))
        # 3. per consumed state: source/GQ evidence, row reference, state input (v003: LO runs in step 3b)
        state_inputs = {}
        for idx, state in enumerate(inv['states']):
            s = time.monotonic()
            tag = 'S%03d' % idx
            j = by_state[digest(state)]
            occurrence = j['occurrence_receipt']['occurrence']
            entry = {'state': state, 'class': state_class(state, accepted_digest), 'ordinal': j['ordinal'],
                     'reading': 'UNAVAILABLE', 'blockers': []}
            rec['states'].append(entry)
            try:
                tail = tail_state_refs(store, deps, state, j, manifest, accepted_digest, tag)
                entry['tail_state'] = tail
                review = policy['packet_binding_reviews'].get(digest(occurrence))
                if review is None:
                    requests.append({'schema': 'DDO154_CURRENT_SOURCE_REVIEW_CX2V001', 'verdict': 'PENDING_DISTINCT_LANE',
                                     'point_sha256': point, 'custody_sha256': details['custody_sha256'],
                                     'producer': policy['evidence_producer'], 'reconstruction': j['reconstruction'],
                                     'packet_descriptor': j['packet'], 'occurrence_sha256': digest(occurrence),
                                     'packet_selectors_and_preparation_arguments_verified': 'PENDING'})
                src = deps['evidence'].export_lo_source(
                    spec, j['reconstruction'], j['packet'], occurrence, tail, uniform_gq_ref=uniform_gq, review_ref=review,
                    approved_review_sha256=policy['approved_review_sha256'],
                    approved_producer_sha256=policy['approved_evidence_producer_sha256'],
                    approved_uniform_producer_sha256=policy['approved_uniform_producer_sha256'])
                entry['source_reconstruction'] = src_ref = store.put(tag + '_SOURCE_RECONSTRUCTION.json', src)
                gq = src['current_gq']
                entry['current_gq'] = store.put(tag + '_' + gq['gate'] + '.json', gq)
                if state['nonnegative_masses'] is False and gq['gate'] != 'GQ_SIGNED':
                    raise ValueError('SIGNED_STATE_WITHOUT_GQ_SIGNED')
                row = deps['row_producer'].row_reference(state=state, row_contract=details['row_contract'], row_contract_sha256=rcs,
                                                         result=result, result_ref=result_ref, policy_review=row_review)
                entry['row_reference'] = row_ref = store.put(tag + '_ROWS.json', row)
                entry['state_input'] = sin = store.put(tag + '_LO_STATE_INPUT.json', {
                    'schema': STATE_SCHEMA, 'identity': details['identity'], 'custody': details['custody'], 'state': state,
                    'tail_state': tail, 'row_reference': row_ref, 'source_reconstruction': src_ref,
                    'call_result': result_ref,       # v002: srb_rot_adapter_c3v001 L360-362 binds the state input to the call
                    'execution': execution})         # v003: A138 V01(b); lo_producer_cx2v004 L56-59
                state_inputs[state['state_sha256']] = sin
            except Exception as exc:     # every failure is typed and preserved; nothing is retried or relabelled
                entry['blockers'].append('%s: %s' % (type(exc).__name__, exc))
            entry['seconds'] = time.monotonic() - s
        # 3b. v003, A138 V01(a): Claude3's adapt_call_lo runs the unchanged lo_core on every state input
        s = time.monotonic()
        tsp = policy.get('trusted_source_producers')        # v004 (0208 N5): checked here, forwarded unchanged
        b1_untrusted = not (isinstance(tsp, (list, tuple)) and B1_EVIDENCE['sha256'] in tsp)
        if b1_untrusted:
            rec['blockers'].append(B1_UNTRUSTED_BLOCKER)
        try:
            lo_root = store.dir / LO_ADAPTER_DIR
            lo_root.mkdir(exist_ok=False)
            lo_call = deps['lo_adapter'](
                spec, call_dir=str(call), result=result, inventory=inv, bundle_ref=policy['prelaunch_bundle'],
                state_inputs=state_inputs, root_ruling_refs=policy['root_ruling_refs'],
                approved_producer_sha256=[p['sha256'] for p in policy['approved_certificate_producers']],
                trusted_source_producers=policy['trusted_source_producers'],
                trusted_row_policy_review_sha256=[] if row_review is None else [row_review['sha256']],
                out_root=str(lo_root))
            rec['lo_adapter'] = {'pin': dict(LO_ADAPTER_KS6), 'call_record': store.put('LO_ADAPTER_CALL_RECORD.json', lo_call),
                                 'call_lo_reading': lo_call.get('call_lo_reading'), 'class_reading': lo_call.get('class_reading'),
                                 'step4_stop': lo_call.get('step4_stop'), 'blockers': lo_call.get('blockers'),
                                 'out_root': str(lo_root)}
        except Exception as exc:
            lo_call = {'states': [], 'blockers': ['LO_ADAPTER_CALL_FAILED: %s: %s' % (type(exc).__name__, exc)]}
            rec['lo_adapter'] = {'pin': dict(LO_ADAPTER_KS6), 'call_record': None, 'blockers': lo_call['blockers']}
        adopt_lo(rec, lo_call, slot)
        timing['lo_adapter'] = time.monotonic() - s
        if requests:
            rec['packet_binding_review_requests'] = store.put('PACKET_BINDING_REVIEW_REQUESTS.json',
                                                              {'schema': REQUESTS_SCHEMA, 'requests': requests})
        sums = [e['summed_max_over_tau'] for e in rec['states'] if isinstance(e.get('summed_max_over_tau'), (int, float))]
        rec['summed_lo_max_over_states'] = max(sums) if sums else None      # Q4(c): for R-C2 to cite
        # 4. SRB-ROT on the accepted final-rotation state only (Q10; 0690 OPEN-3: own_source_state at le{final_pass}_rotation)
        s = time.monotonic()
        if not isinstance(flags, list):
            rec['srb_rot'] = {'reading': 'UNAVAILABLE', 'detail': 'ROUTE_A_FLAG_STATUS_UNRECORDED'}
        else:
            flagged = 'TAIL_SOURCE_UNDERCONVERGED' in flags
            try:
                target, stage, _ = deps['row_producer'].final_rotation_target(inv, result)
                tgt = [e for e in rec['states'] if e['state'] == target and e.get('state_input')]
                if len(tgt) != 1:
                    raise ValueError('FINAL_ROTATION_STATE_INPUT_UNAVAILABLE: ' + stage)
                tgt[0]['srb_rot_target'] = True
                rows_in = store.put('SRB_ROT_ROWS_INPUT.json', deps['row_producer'].srb_rot_rows_input(
                    state=target, inventory=inv, row_contract=details['row_contract'], row_contract_sha256=rcs,
                    result=result, result_ref=result_ref, call_dir=call))
                srb = deps['srb_adapter'](spec, call_dir=str(call), result=result, inventory=inv,
                                          bundle_ref=policy['prelaunch_bundle'], state_input_ref=tgt[0]['state_input'],
                                          rows_input_ref=rows_in, root_ruling_refs=policy['root_ruling_refs'],
                                          approved_producer_sha256=[p['sha256'] for p in policy['approved_certificate_producers']],
                                          trusted_source_producers=policy['trusted_source_producers'])
                ref = store.put('SRB_ROT.json', srb)
                reading = srb.get('reading') if srb.get('reading') in SRB_READINGS[flagged] else 'UNAVAILABLE'
                proof = srb.get('proof') if reading in ('PASS', 'PASS_FLAGGED') else None
                if reading in ('PASS', 'PASS_FLAGGED') and not isinstance(proof, dict):
                    reading = 'UNAVAILABLE'                 # a pass is read only with its SRB_ROT proof (OPEN-2)
                rec['srb_rot'] = {'reading': reading, 'record': ref, 'flagged': flagged, 'state': target, 'stage': stage,
                                  'rows_input': rows_in,
                                  'proof': store.put('SRB_ROT_PROOF.json', proof) if isinstance(proof, dict) else None}
            except Exception as exc:
                rec['srb_rot'] = {'reading': 'UNAVAILABLE', 'detail': '%s: %s' % (type(exc).__name__, exc)}
        timing['srb_rot'] = time.monotonic() - s
        # 5. post-state bundle and the guard acceptance phase (only when every state has its proofs)
        ready = all(e['reading'] == 'PASS' and (e['state']['nonnegative_masses'] or e.get('current_gq')) for e in rec['states'])
        if ready:
            s = time.monotonic()
            bundle = dict(prelaunch)
            bundle['parent_prelaunch_bundle'] = policy['prelaunch_bundle']      # wrapper r10_c4 L141-144
            bundle['states'] = [dict({'state': e['state'], 'LO': e['LO']},
                                     **({} if e['state']['nonnegative_masses'] else {'GQ_SIGNED': e['current_gq']}))
                                for e in rec['states']]
            rec['bundle'] = bundle_ref = store.put('POST_STATE_BUNDLE.json', bundle)
            if mode == 'guard':
                g = deps['guard'].verify_bundle(bundle_ref, details['identity'], expected_custody=details['custody'],
                                                approved_producer_sha256=[p['sha256'] for p in policy['approved_certificate_producers']],
                                                phase='acceptance', required_states=inv['states'])
            else:
                try:
                    g = wrapper_context.write_acceptance(call, bundle_ref)
                except Exception as exc:
                    g = {'ok': False, 'blockers': ['%s: %s' % (type(exc).__name__, exc)]}
            rec['guard'] = {'ok': g.get('ok') is True, 'blockers': g.get('blockers'), 'note': g.get('note')}
            timing['guard'] = time.monotonic() - s
        # 6. readings (Q5, Q10, Q3), mechanically
        failed = [e for e in rec['states'] if e['reading'] == 'LO_ABOVE_THRESHOLD']
        unavailable = [e for e in rec['states'] if e['reading'] == 'UNAVAILABLE']
        non_iterate = [e for e in rec['states'] if e['class'] != 'ROUTE_A_ITERATE']
        srb = (rec['srb_rot'] or {}).get('reading')
        found = set()
        if any(e['class'] in ('ACCEPTED_ROUTE_A', 'ROUTE_B_STAGE') for e in failed):
            found.add('NON_LAPSE_TAIL_MATERIAL')      # 0690 OPEN-6: decisive even with other states UNAVAILABLE
        elif failed and all(e['reading'] == 'PASS' for e in non_iterate):
            found.add('LO_UNCERTIFIED_TRANSIENT')     # 0690 OPEN-6: every non-iterate state at PASS
        elif failed:
            rec['transient_candidate_unconfirmed'] = [e['state'] for e in failed]
        if srb in ('BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED'):
            found.add(srb)
        if unavailable or srb not in ('PASS', 'PASS_FLAGGED', 'BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED') \
                or not (rec['guard'] or {}).get('ok') or b1_untrusted:     # v004: 0208 N5
            found.add('INCOMPLETE')
        found.add('ACCEPTED_PASS_FLAGGED' if srb == 'PASS_FLAGGED' else 'ACCEPTED')
        rec['reading'] = next(r for r in READINGS if r in found)
        rec['all_readings'] = sorted(found - {'ACCEPTED', 'ACCEPTED_PASS_FLAGGED'}) or [rec['reading']]
    except Exception as exc:
        rec['blockers'].append('%s: %s' % (type(exc).__name__, exc))
        rec['reading'] = 'INCOMPLETE'
    return rec, finish()
