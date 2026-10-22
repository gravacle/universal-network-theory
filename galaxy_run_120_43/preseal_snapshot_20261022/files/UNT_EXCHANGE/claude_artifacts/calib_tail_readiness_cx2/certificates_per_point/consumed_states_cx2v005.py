"""Read-only consumed-state discovery for the pinned v010 r5 driver (campaign call_dir/out layout).

This is deliberately NOT a production-complete enumerator: v010 r5 archives only an accepted route-A TailState. Under ruling 0528, only
fresh completed calls qualify; invalid/interrupted/resumed calls are excluded.
Digest-only observations never become guard-ready states. No source rebuild,
TailState.build, driver import, solver, subprocess, network or write is present.
"""
import hashlib
import io
import json
import math
from pathlib import Path
import re
import zipfile
import numpy as np

ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
DRIVER = ROOT / 'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
SOURCE_PINS = {
    '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md': 'd11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83',
    str(DRIVER): DRIVER_SHA,
    str(ROOT / 'tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py'): 'c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc',
    str(ROOT / 'tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py'): '1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329',
    str(ROOT / 'tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/driver/route_a_tail_manifest_c2v001_r5.py'): '44b31a8b8a91bf7ff67426a1def0b441f4e6d6dc69d00474892883f68ca93b33',
    str(ROOT / 'tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py'): '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54',
}
KINDS = {'reference': 'reference', 'body': 'body', 'offset': 'offset', 'columns_v001': 'fs_columns',
         'rotation_v001': 'fs_rotation', 'columns_v003': 'rfs_columns', 'columns_v005': 'le_columns',
         'rotation_v005': 'le_rotation'}
SCHEMA = 'DDO154_CONSUMED_STATE_DISCOVERY_CX2V005'
MAX_JSON_BYTES = 16 * 1024 * 1024
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024
MAX_PIN_BYTES = 1024 * 1024 * 1024
MAX_FILES = 20000
HEX = re.compile(r'[0-9a-f]{64}\Z')

class InventoryError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def _hex(x):
    return isinstance(x, str) and HEX.fullmatch(x) is not None

def _pairs(items):
    out = {}
    for k, v in items:
        if k in out:
            raise InventoryError('DUPLICATE_JSON_KEY')
        out[k] = v
    return out

def _strict_json(raw):
    return json.loads(raw, object_pairs_hook=_pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(InventoryError('NONFINITE_JSON_NUMBER')))

def _forbidden(path):
    parts = [p.casefold() for p in Path(path).parts]
    return ('.codex' in parts or 'kmax_a2f10_c5h_run_v001' in parts or
            ('runs_ext' in parts and any(p.startswith('uvt_') for p in parts)) or
            any('ngc3198' in p or 'observed_velocit' in p or 'target_velocit' in p for p in parts))

def safe_path(path):
    if not isinstance(path, (str, Path)) or not Path(path).is_absolute():
        raise InventoryError('ABSOLUTE_PATH_REQUIRED')
    if _forbidden(path):
        raise InventoryError('FORBIDDEN_INPUT_PATH')
    p = Path(path).resolve(strict=True)
    if _forbidden(p):
        raise InventoryError('FORBIDDEN_RESOLVED_INPUT_PATH')
    if not (p.is_relative_to('/Users/bgm/Research') or p.is_relative_to('/Volumes/External1')):
        raise InventoryError('INPUT_OUTSIDE_RESEARCH_ROOTS')
    return p

def _file_sha(path):
    p = safe_path(path)
    if not p.is_file() or p.stat().st_size > MAX_PIN_BYTES:
        raise InventoryError('PIN_FILE_MISSING_OR_TOO_LARGE')
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

class Discovery:
    def __init__(self):
        self.blockers = []
        self.occurrences = []
        self.evidence = {}
        self.archives = []
        self.fresh_completed = False

    def block(self, code, where, detail, owner='Claude2 driver/stage author'):
        item = dict(code=code, where=str(where), detail=detail, owner=owner, status='UNTESTED',
                    severity='BLOCKING')
        if item not in self.blockers:
            self.blockers.append(item)

    def read(self, path, expected=None, *, document=True, where='input', required_pin=False):
        try:
            if len(self.evidence) >= MAX_FILES:
                raise InventoryError('INVENTORY_FILE_LIMIT')
            if required_pin and not _hex(expected):
                raise InventoryError('REQUIRED_BYTE_PIN_MISSING')
            p = safe_path(path)
            if expected is not None and not _hex(expected):
                raise InventoryError('MALFORMED_BYTE_PIN')
            if document:
                if p.stat().st_size > MAX_JSON_BYTES:
                    raise InventoryError('JSON_TOO_LARGE')
                raw = p.read_bytes()
                actual = hashlib.sha256(raw).hexdigest()
            else:
                actual = _file_sha(p)
            if expected is not None and actual != expected:
                raise InventoryError('BYTE_PIN_MISMATCH')
            old = self.evidence.get(str(p))
            if old is not None and old['sha256'] != actual:
                raise InventoryError('BYTES_CHANGED_DURING_DISCOVERY')
            self.evidence[str(p)] = {'path': str(p), 'sha256': actual, 'expected_sha256': expected,
                                     'pin_verified': expected is not None}
            return _strict_json(raw) if document else actual
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self.block(getattr(exc, 'code', 'READ_OR_PARSE_FAILED'), where, type(exc).__name__ + ': ' + str(exc))
            return None

    def ref(self, ref, *, document=True, where='reference'):
        if not isinstance(ref, dict) or not isinstance(ref.get('path'), str) or not _hex(ref.get('sha256')):
            self.block('PIN_REFERENCE_REQUIRED', where, 'Expected a path and a full SHA256 from bytes.')
            return None
        return self.read(ref['path'], ref['sha256'], document=document, where=where)

    def occurrence(self, *, stage, role, state, source=None, evidence=None, iteration=None, kind=None):
        event = {'ordinal': len(self.occurrences), 'stage': stage, 'stage_kind': kind or stage,
                 'role': role, 'iteration': iteration, 'state_sha256_claimed': state,
                 'source_sha256_claimed': source, 'evidence': evidence, 'guard_ready': False}
        if not _hex(state):
            self.block('STATE_DIGEST_MISSING_OR_INVALID', stage + ':' + role, 'No usable state identity.')
        self.occurrences.append(event)
        return event

    def sidecar(self, uv, attempt_ref):
        sc = uv.get('sidecar')
        if not isinstance(sc, dict):
            self.block('ROUTE_A_SIDECAR_REQUIRED', 'route_a', 'No file-pinned history; final state is insufficient.')
            return
        finish = self.ref(sc.get('finish'), where='route_a.sidecar.finish')
        files = sc.get('files')
        if not isinstance(files, dict) or len(files) > MAX_FILES:
            self.block('ROUTE_A_SIDECAR_FILES_REQUIRED', 'route_a', 'Full byte-pinned file table required.')
            return
        if not isinstance(finish, dict) or finish.get('files') != files or finish.get('record') != {k:v for k,v in uv.items() if k != 'sidecar'}:
            self.block('SIDECAR_FINISH_CONTENT_MISMATCH', 'route_a', 'Finish must bind this exact record and file table.')
        records = {}
        sidecar_identity = None
        for name, sha in files.items():
            if not isinstance(name, str) or Path(name).name != name or not _hex(sha):
                self.block('SIDECAR_ENTRY_INVALID', 'route_a', 'Names must be basenames with full byte pins.')
                continue
            path = str(Path(sc.get('directory', '')) / name)
            val = self.read(path, sha, document=name.endswith('.json'), where='route_a.sidecar.' + name)
            if name == 'SIDECAR_IDENTITY.json':
                sidecar_identity = val
            if name.startswith('iteration_') and name.endswith('.json') and isinstance(val, dict):
                records[name] = val
        if (not isinstance(sidecar_identity, dict) or
            sidecar_identity.get('identity_sha256') != digest(sidecar_identity.get('identity')) or
            (sidecar_identity.get('identity') or {}).get('checkpoint_identity_sha256') != uv.get('checkpoint_identity_sha256')):
            self.block('SIDECAR_IDENTITY_MISMATCH', 'route_a', 'Sidecar identity digest/checkpoint identity must agree.')
        summary = uv.get('iterations')
        if not isinstance(summary, list):
            self.block('ROUTE_A_ITERATION_LIST_REQUIRED', 'route_a', 'Cannot infer history from accepted_iteration.')
            summary = []
        if len({x.get('iteration') for x in summary if isinstance(x, dict)}) != len(summary):
            self.block('ROUTE_A_DUPLICATE_ITERATION', 'route_a', 'Duplicate iteration summaries are ambiguous.')
        if any(isinstance(x,dict) and (x.get('reloaded') or x.get('reproduced_existing_record')) for x in summary):
            self.block('FRESH_ROUTE_A_RESUME_OR_REPRODUCTION_FORBIDDEN', 'route_a', '0528 excludes resumed and repeated histories.')
            self.fresh_completed = False
        prior_next = None
        for expected_i, s in enumerate(summary):
            if not isinstance(s, dict) or type(s.get('iteration')) is not int or s['iteration'] != expected_i:
                self.block('ROUTE_A_HISTORY_GAP', 'route_a', 'Completed/reloaded history must include every index from zero.')
                continue
            i = s['iteration']
            name = 'iteration_%04d.json' % i
            payload = (records.get(name) or {}).get('payload')
            if not isinstance(payload, dict) or payload.get('iteration') != i:
                self.block('ROUTE_A_ITERATION_RECORD_MISSING', name, 'Each summarized completion needs its verified record.')
                continue
            comparable = {k:v for k,v in s.items() if k not in ('reloaded','reproduced_existing_record')}
            if payload.get('summary') != comparable:
                self.block('ROUTE_A_SUMMARY_PAYLOAD_MISMATCH', name, 'Summary may differ only by controller resume/reproduction flags.')
            for key in ('state_digest', 'next_state_digest'):
                if s.get(key) != payload.get(key):
                    self.block('ROUTE_A_ITERATION_DIGEST_MISMATCH', name, key)
            if prior_next is not None and payload.get('state_digest') != prior_next:
                self.block('ROUTE_A_CURRENT_NEXT_CHAIN_MISMATCH', name, 'Current state differs from preceding next-state digest.')
            prior_next = payload.get('next_state_digest')
            self.occurrence(stage='route_a', kind='route_a', role='current_begin_inferred_from_completion',
                            state=payload.get('state_digest'), evidence={'path': str(Path(sc['directory']) / name), 'sha256': files[name]}, iteration=i)
            self.occurrence(stage='route_a', kind='route_a', role='next_built_and_monitor_consumed',
                            state=payload.get('next_state_digest'), evidence={'path': str(Path(sc['directory']) / name), 'sha256': files[name]}, iteration=i+1)
            el = payload.get('elements') or {}
            if el.get('file') not in files:
                self.block('ROUTE_A_ELEMENTS_NOT_PINNED', name, 'Missing element roster file in sidecar table.')
            else:
                self.elements_archive(str(Path(sc['directory']) / el['file']), files[el['file']], el, name)
            self.block('ROUTE_A_STATE_SOURCE_RECONSTRUCTION_UNAVAILABLE', name,
                       'Per-iteration current/next state and full stellar+gas source reconstruction from this call checkpoint/element archives is not implemented. Digest-only observations cannot substitute. No always-missing raw input is asserted.')
        if set(records) != {'iteration_%04d.json' % i for i in range(len(summary))}:
            self.block('ROUTE_A_UNMATCHED_SIDECAR_ITERATION', 'route_a', 'Sidecar iteration files and completed/reloaded history differ.')
        self.occurrence(stage='route_a', role='boundary_at_return', state=uv.get('boundary_state_digest_at_return'), evidence=attempt_ref)
        # 0528: fresh successfully completed calls have no interrupted/resumed
        # begins to reconstruct; do not demand a general durable begin ledger.

    def fresh_scope(self, spec, result, finish, stages):
        """0528: restrict certificate eligibility to own fresh completed calls."""
        before = len(self.blockers)
        if spec.get('admit'):
            self.block('FRESH_CALL_ADMISSION_FORBIDDEN', 'spec.admit', '0528 requires this call own states; no admitted producer or route A.')
        if result.get('status') != 'COMPLETED' or result.get('valid') is not True:
            self.block('FRESH_COMPLETED_VALID_CALL_REQUIRED', 'result', 'Interrupted, failed, invalid or unfinished calls are not admitted.')
        if (not isinstance(finish,dict) or finish.get('status') != 'COMPLETED' or finish.get('valid') is not True
            or type(finish.get('retries')) is not int or finish['retries'] != 0):
            self.block('FRESH_FINISH_NO_RETRY_REQUIRED', 'finish', 'Completed valid finish and exact integer retries=0 required.')
        ra = (result.get('identity') or {}).get('route_a') or {}
        if ra.get('mode') != 'computed':
            self.block('FRESH_ROUTE_A_COMPUTED_REQUIRED', 'identity.route_a', 'Admitted/resumed/unknown route-A identity is excluded.')
        outcome = result.get('route_a_outcome') or {}
        if (outcome.get('classification') != 'CONVERGED' or outcome.get('converged_finite_fixed_point') is not True
            or outcome.get('outcome') != 'CONVERGED_FINITE_FIXED_POINT'):
            self.block('FRESH_ROUTE_A_CONVERGED_REQUIRED', 'route_a_outcome', 'Interrupted or nonconverged route A is excluded.')
        runs = [x for x in stages if isinstance(x,dict) and x.get('kind')=='route_a']
        if len(runs) != 1:
            self.block('FRESH_EXACTLY_ONE_ROUTE_A_REQUIRED', 'stage_records', 'No missing, duplicate or retry route-A stage.')
        else:
            r = runs[0]; argv = r.get('argv')
            ok = (r.get('executed') is True and type(r.get('exit_code')) is int and r['exit_code']==0 and isinstance(argv,list))
            if ok:
                ok = argv.count('--start-iteration') == 1
                if ok:
                    j=argv.index('--start-iteration')
                    ok = j+1<len(argv) and argv[j+1]=='0'
                ok = ok and not any(isinstance(x,str) and ('resume' in x.casefold() or 'retry' in x.casefold()) for x in argv if isinstance(x,str) and x.startswith('--'))
                if '--checkpoint-mode' in argv:
                    j=argv.index('--checkpoint-mode')
                    ok=ok and argv.count('--checkpoint-mode')==1 and j+1<len(argv) and argv[j+1]=='new'
            if not ok:
                self.block('FRESH_ROUTE_A_START_ZERO_NO_RESUME_REQUIRED', 'route_a.request', 'Executed successful stage, start iteration zero, no resume/retry flags required.')
        self.fresh_completed = len(self.blockers)==before

    def elements_archive(self, path, expected, record, where):
        """Verify archived element shape, dtype, digest and byte stability only."""
        try:
            p = safe_path(path)
            if _file_sha(p) != expected:
                raise InventoryError('BYTE_PIN_MISMATCH')
            with zipfile.ZipFile(p) as z:
                if sum(x.file_size for x in z.infolist()) > MAX_ARCHIVE_BYTES:
                    raise InventoryError('ARCHIVE_EXPANSION_TOO_LARGE')
            with np.load(p, allow_pickle=False) as f:
                if set(f.files) != {'positions_m','integrated_J'} or len(f.files) != 2:
                    raise InventoryError('ELEMENT_ARCHIVE_FIELDS_INVALID')
                pos, J = np.ascontiguousarray(f['positions_m']), np.ascontiguousarray(f['integrated_J'])
            if (pos.dtype.hasobject or J.dtype.hasobject or not np.isfinite(pos).all() or not np.isfinite(J).all()
                or pos.ndim != 2 or pos.shape[1] != 3 or J.ndim != 1 or len(pos) != len(J)
                or type(record.get('count')) is not int or len(J) != record['count']):
                raise InventoryError('ELEMENT_ARRAY_SHAPE_OR_VALUES_INVALID')
            for a, k in ((pos,'positions_digest'),(J,'J_digest')):
                h = hashlib.sha256(('%s|%s|' % (a.dtype.str,a.shape)).encode())
                h.update(a.tobytes())
                if h.hexdigest() != record.get(k):
                    raise InventoryError('ELEMENT_ARRAY_DIGEST_MISMATCH')
            if _file_sha(p) != expected:
                raise InventoryError('BYTES_CHANGED_DURING_DISCOVERY')
        except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as exc:
            self.block(getattr(exc,'code','ELEMENT_ARCHIVE_UNREADABLE'),where,str(exc))

    def state_archive(self, man, ref):
        """Verify archived accepted state digest without evaluating or rebuilding a field."""
        st = man.get('state') or {}
        record = st.get('record')
        arrref = st.get('arrays')
        if not isinstance(record, dict) or not _hex(st.get('digest')) or self.ref(arrref, document=False, where='manifest.state.arrays') is None:
            self.block('ACCEPTED_STATE_ARCHIVE_INVALID', 'route_a_manifest', 'State record/array pin/digest missing.')
            return
        try:
            p = safe_path(arrref['path'])
            with zipfile.ZipFile(p) as z:
                if sum(x.file_size for x in z.infolist()) > MAX_ARCHIVE_BYTES:
                    raise InventoryError('ARCHIVE_EXPANSION_TOO_LARGE')
            h = hashlib.sha256(canonical(record))
            with np.load(p, allow_pickle=False) as arrays:
                if len(set(arrays.files)) != len(arrays.files):
                    raise InventoryError('DUPLICATE_ARCHIVE_MEMBER')
                for k in sorted(arrays.files):
                    a = np.ascontiguousarray(arrays[k])
                    if a.dtype.hasobject or not np.isfinite(a).all():
                        raise InventoryError('STATE_ARRAY_NONFINITE_OR_OBJECT')
                    h.update(('|%s|%s|%s|' % (k, a.dtype, a.shape)).encode())
                    h.update(a.tobytes())
            if h.hexdigest() != st['digest'] or _file_sha(p) != arrref['sha256']:
                raise InventoryError('STATE_ARCHIVE_DIGEST_MISMATCH')
            self.archives.append({'kind': 'accepted_route_a_state', 'state_sha256': st['digest'], 'arrays': arrref,
                                  'source_sha256_claimed': record.get('roster_digest'), 'guard_ready': False})
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
            self.block(getattr(exc, 'code', 'STATE_ARCHIVE_UNREADABLE'), 'route_a_manifest', str(exc))
        roster = man.get('roster') or {}
        self.ref(roster.get('arrays'), document=False, where='manifest.gas_roster.arrays')
        self.block('FULL_SOURCE_ROSTER_NOT_ARCHIVED', 'route_a_manifest',
                   'Full source reconstruction from this call checkpoint, registered stars and gas_IT archive is unimplemented; gas_IT alone does not verify the full roster digest, positivity or normalization.')

    def stage(self, s, summary, start_pins):
        name, kind = s.get('name'), s.get('kind')
        if not isinstance(name, str) or not isinstance(kind, str):
            self.block('STAGE_ID_REQUIRED', 'stage_records', 'Missing stage name/kind.')
            return
        if not s.get('executed'):
            self.block('UNEXECUTED_STAGE_IN_RESULT', name, 'Planning records cannot establish consumption.')
            return
        req = self.read(s.get('request_path'), s.get('request_sha256'), where=name + '.request', required_pin=True)
        meta = {'stage_dir','executed','exit_code','elapsed_seconds','request_path','request_sha256'}
        if not isinstance(req, dict) or req != {k:v for k,v in s.items() if k not in meta}:
            self.block('STAGE_REQUEST_CONTENT_MISMATCH', name, 'Stage record differs from pinned request bytes.')
        pin = s.get('script_sha256')
        self.read(s.get('script'), pin, document=False, where=name + '.script', required_pin=True)
        if not isinstance(start_pins, dict) or start_pins.get(s.get('script')) != pin:
            self.block('STAGE_SCRIPT_NOT_IN_START_PINS', name, 'No matching driver start static pin.')
        if kind not in KINDS and kind != 'route_a_tail_manifest':
            return
        argv = s.get('argv')
        if not isinstance(argv, list) or argv.count('--outdir') != 1:
            self.block('STAGE_OUTDIR_AMBIGUOUS', name, 'Exactly one --outdir needed.')
            return
        try:
            outdir = argv[argv.index('--outdir')+1]
        except IndexError:
            self.block('STAGE_OUTDIR_MISSING', name, 'Missing --outdir value.')
            return
        if not isinstance(summary, dict) or summary.get('kind') != kind:
            self.block('TAIL_STAGE_SUMMARY_MISSING', name, 'No one-to-one byte-pinned finish summary.')
            return
        fin = self.read(str(Path(outdir) / 'finish.json'), summary.get('finish_sha256'), where=name + '.finish', required_pin=True)
        if not isinstance(fin, dict):
            return
        u = fin if kind == 'route_a_tail_manifest' else fin.get('uv_tail')
        if not isinstance(u, dict):
            self.block('TAIL_STAGE_RECORD_MISSING', name, 'No tail record in pinned finish.')
            return
        if u.get('state_digest') != summary.get('state_digest'):
            self.block('TAIL_STAGE_STATE_DIGEST_MISMATCH', name, 'Finish and driver summary disagree.')
        if kind == 'route_a_tail_manifest':
            return
        if u.get('stage_kind') != KINDS[kind]:
            self.block('TAIL_STAGE_KIND_MISMATCH', name, 'Unexpected binding stage kind.')
        role = 'inherited_route_a' if kind in ('reference','body') else ('signed_body_minus_route_a' if kind == 'offset' else 'own_source_state')
        event = self.occurrence(stage=name, kind=KINDS[kind], role=role, state=u.get('state_digest'), source=u.get('roster_digest'),
                               evidence={'path':str(Path(outdir)/'finish.json'),'sha256':summary.get('finish_sha256')})
        event['lineage_claims'] = u.get('lineage')
        if kind == 'offset':
            event['nonnegative_masses'] = False
            self.occurrence(stage=name, kind='offset_positive_component', role='body_gas_component', state=None, evidence=event['evidence'])
            component = self.occurrence(stage=name, kind='offset_negative_component', role='route_a_gas_component', state=None, evidence=event['evidence'])
            component['parent_stellar_plus_gas_state_digest_claimed'] = u.get('route_a_state_digest')
            self.block('SIGNED_COMPONENT_RECONSTRUCTION_UNAVAILABLE', name,
                       '0528 permits the finite signed-normalization branch. Both actual component rosters and a strictly positive signed-denominator lower bound still require independent reconstruction/proof.', owner='Codex2 source reconstruction and certificate implementation')
        self.block('ROUTE_B_STATE_SOURCE_RECONSTRUCTION_UNAVAILABLE', name,
                   'Finish contains digest metadata, not an own-state P/F archive. Raw saved stage NPZ inputs may permit exact source/state reconstruction, but this adapter does not implement or verify it. Certificate UNAVAILABLE; point INCOMPLETE until required state is recovered or archived.')

def consumed_states(*, spec, result, call_dir):
    d = Discovery()
    campaign = None
    call = None
    try:
        for path, sha in SOURCE_PINS.items():
            if d.read(path, sha, document=False, where='enumerator.source') is None:
                raise InventoryError('ENUMERATOR_SOURCE_PIN_FAILED')
        if not isinstance(spec, dict) or spec.get('galaxy') != 'DDO154':
            raise InventoryError('DDO154_SPEC_REQUIRED')
        uv = (spec.get('numerics') or {}).get('uv_tail')
        if not isinstance(uv, dict) or uv.get('enabled') is not True or uv.get('source_rule') != 'continuum_v001':
            raise InventoryError('CONTINUUM_TAIL_ON_SPEC_REQUIRED')
        campaign = safe_path(call_dir)
        call = safe_path(campaign/'out')
        if not campaign.is_dir() or not call.is_dir() or not call.is_relative_to(campaign):
            raise InventoryError('CAMPAIGN_OUTPUT_DIRECTORY_REQUIRED')
        raw_result = d.read(str(call/'result.json'), where='result')
        finish = d.read(str(call/'finish.json'), where='finish')
        if not isinstance(raw_result, dict) or not isinstance(result, dict) or canonical(raw_result) != canonical(result):
            raise InventoryError('SUPPLIED_RESULT_DIFFERS_FROM_BYTES')
        result_pin = d.evidence.get(str((call/'result.json').resolve()), {}).get('sha256')
        if not isinstance(finish, dict) or finish.get('result_sha256') != result_pin:
            d.block('CALL_FINISH_RESULT_PIN_MISMATCH', 'call', 'finish.json must bind result.json bytes.')
        if result.get('driver_sha256') != DRIVER_SHA:
            raise InventoryError('UNSUPPORTED_DRIVER_BYTES')
        archived_spec = d.read(str(call/'inputs/call_spec.json'), result.get('call_spec_sha256'), where='call_spec', required_pin=True)
        if archived_spec != spec:
            raise InventoryError('SUPPLIED_SPEC_DIFFERS_FROM_ARCHIVED_BYTES')
        start = d.read(str(call/'start.json'), where='start') or {}
        if start.get('driver_sha256') != DRIVER_SHA or start.get('call_spec_sha256') != result.get('call_spec_sha256'):
            d.block('CALL_START_IDENTITY_MISMATCH', 'start', 'Driver/spec custody differs.')
        if start.get('normalized_spec') != result.get('normalized_spec'):
            d.block('NORMALIZED_SPEC_START_RESULT_MISMATCH', 'call', 'Cannot splice histories across normalized specs.')
        # No self-asserted inventory/complete flag is read anywhere in this adapter.
        stages = result.get('stage_records')
        uv_result = result.get('uv_tail') or {}
        summaries = uv_result.get('stage_records')
        if not isinstance(stages, list) or not isinstance(summaries, list):
            raise InventoryError('FULL_STAGE_HISTORY_REQUIRED')
        d.fresh_scope(spec, result, finish, stages)
        names = [x.get('name') for x in stages if isinstance(x, dict)]
        snames = [x.get('stage') for x in summaries if isinstance(x, dict)]
        if len(names) != len(stages) or len(set(names)) != len(names) or len(snames) != len(summaries) or len(set(snames)) != len(snames):
            raise InventoryError('DUPLICATE_OR_INVALID_STAGE_HISTORY')
        smap = {x['stage']:x for x in summaries}
        wanted = {s['name'] for s in stages if s.get('executed') and s.get('kind') in set(KINDS)|{'route_a_tail_manifest'}}
        if set(smap) != wanted:
            d.block('TAIL_SUMMARY_STAGE_COVERAGE_MISMATCH', 'stages', 'Summary must cover each executed tail stage exactly once.')
        for s in stages:
            d.stage(s, smap.get(s['name']), start.get('static_pins'))
        outcome = result.get('route_a_outcome') or {}
        aref = {'path':outcome.get('result_path'), 'sha256':outcome.get('result_sha256')}
        attempt = d.ref(aref, where='route_a.attempt')
        if isinstance(attempt, dict):
            afin = d.read(str(Path(aref['path']).parent/'finish.json'), where='route_a.attempt_finish')
            if not isinstance(afin, dict) or afin.get('result_sha256') != aref['sha256']:
                d.block('ROUTE_A_ATTEMPT_FINISH_PIN_MISMATCH', 'route_a', 'Attempt finish/result mismatch.')
            auv = (attempt.get('result') or {}).get('uv_tail')
            if isinstance(auv, dict):
                d.sidecar(auv, aref)
            else:
                d.block('ROUTE_A_TAIL_RECORD_MISSING', 'route_a', 'No complete iteration/source record.')
        manifest_ref = uv_result.get('manifest')
        if isinstance(manifest_ref, dict):
            man = d.ref(manifest_ref, where='route_a.manifest')
            if isinstance(man, dict):
                d.state_archive(man, manifest_ref)
        else:
            d.block('ACCEPTED_ROUTE_A_MANIFEST_MISSING', 'route_a', 'Even the accepted state archive is absent.')
        # Admitted reference/body bypass execution-stage summaries. Preserve them explicitly.
        for kind in ('reference','body'):
            adm = (spec.get('admit') or {}).get(kind)
            if isinstance(adm, dict):
                for file, key in (('start.json','start_sha256'), ('finish.json','finish_sha256')):
                    if key in adm:
                        rec = d.read(str(Path(adm.get('directory',''))/file),adm[key],where='admitted.'+kind+'.'+file)
                        u = (rec or {}).get('uv_tail') if isinstance(rec,dict) else None
                        if isinstance(u,dict):
                            d.occurrence(stage='admitted_'+kind,kind=kind,role='inherited_admitted',state=u.get('state_digest'),source=u.get('roster_digest'))
                d.block('ADMITTED_PRODUCER_HISTORY_REQUIRED','admitted.'+kind,
                        'A pinned finish proves this artifact, not every state consumed in the admitted producer or its resumed attempts.')
        # 0528 restricts admission to one fresh completed call: no general
        # crash/attempt ledger is required for that allowed domain.
        d.block('GUARD_READY_STATES_WITHHELD', 'inventory',
                'Claimed state/source digests are observations only. Full source reconstruction, positivity, signed-component policy and complete occurrence coverage are unestablished.')
        d.block('POSITIVE_TOTAL_ZERO_MODE_REQUIRED', 'inventory',
                'Nonnegative element masses alone permit an all-zero source. Normalized GQ needs a verified strictly positive total zero mode (including stars), or a separately reviewed exact-zero-source rule.', owner='Claude2 root + source/certificate reviewer')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        d.block(getattr(exc,'code','INVENTORY_INPUT_INVALID'),'inventory',type(exc).__name__+': '+str(exc))
    return {'schema': SCHEMA, 'complete': False, 'certificate_status': 'UNAVAILABLE',
            'point_status': 'INCOMPLETE' if d.fresh_completed else 'INELIGIBLE', 'states': [], 'occurrences': d.occurrences,
            'blockers': d.blockers, 'verified_files': list(d.evidence.values()), 'verified_state_archives': d.archives,
            'driver_sha256': DRIVER_SHA, 'source_pins': SOURCE_PINS,
            'campaign_call_dir': str(campaign) if campaign is not None else None,
            'driver_output_dir': str(call) if call is not None else None,
            'coverage': {'completed_iterations': 'discovered when byte-pinned', 'next_monitor_states': 'discovered when byte-pinned',
                         'fresh_call_scope': 'FRESH_COMPLETED' if d.fresh_completed else 'INELIGIBLE_OR_UNESTABLISHED', 'full_route_b_source_rosters': 'UNESTABLISHED'},
            'guard_state_schema': ['state_sha256','source_sha256','stage_kind','nonnegative_masses'],
            'status': 'UNTESTED_PRODUCTION_COMPLETENESS', 'note': 'No launch; no scientific arithmetic or full rebuild. No caller completeness assertion is trusted.'}
