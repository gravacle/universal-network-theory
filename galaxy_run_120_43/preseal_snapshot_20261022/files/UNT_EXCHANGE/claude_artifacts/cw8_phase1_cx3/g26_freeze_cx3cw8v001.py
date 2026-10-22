"""G26: root-operated step-8 saved-state replay and exclusive freeze.

No launcher, target reader, scorer, or subprocess is exposed. Production use is
after root's seal/reading gates. The externally recorded ledger-head pin is
mandatory. Reviewed dependencies are fixed; changes require a successor.

Lineage disclosure (A205 item 10): the pinned v003g FORBIDDEN set inherits the
P46 prediction-harness set plus four interface target-row names. This wrapper
reuses that code; it is not independent blinding evidence.
"""
import argparse
import contextlib
import hashlib
import json
import math
import os
import stat
import sys
import types

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
BUILDER_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3/roster_builder_c2v007_cx3cw8v001.py'
BUILDER_SHA256 = 'e6102ba15542e6b2a10c073b4f8647c48facaadf2209d664818e81ee6058da31'
FREEZE_SHA256 = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
SPEC_SHA256 = 'e2a7650e166a9230138ffd16453ac8fdabab41a8695169844940c4c061a894ec'
NOTES_CANONICAL_SHA256 = '56ac5c6440bfd0def9b42077e97677e6844cd2d38bd45de65b4690da1ab8535a'
SLOTS_SHA256 = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
QUERY_ROLE = 'PROGRAM_PIN'
INPUT_SCHEMA = 'G26_FREEZE_INPUT_CX2V001'
RESULT_SCHEMA = 'G26_FREEZE_RESULT_CX2V001'
INPUT_KEYS = ('schema', 'pass_input', 'ledger_head', 'slots', 'notes',
              'parameter_region', 'observation_rule', 'code_files', 'input_files')
SLOT_FIELDS = ('name', 'transform', 'lower', 'upper', 'trial_value',
               'units', 'reference_value')
NUMERIC_FIELDS = ('lower', 'upper', 'trial_value', 'reference_value')
OUTPUT_NAMES = ('FREEZE_MANIFEST.json', 'FREEZE_REGISTRATION.json',
                'G26_RESULT.json', 'SINGLE_READ_AUDIT.json')


class BootstrapRefusal(Exception):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def bootstrap_builder():
    """Read and execute the pinned source once; seed its command cache."""
    real = os.path.realpath(BUILDER_PATH)
    before = os.stat(real)
    if not stat.S_ISREG(before.st_mode):
        raise BootstrapRefusal('BUILDER_NOT_REGULAR')
    fd = os.open(real, os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0))
    try:
        first = os.fstat(fd)
        if not stat.S_ISREG(first.st_mode) or (first.st_dev, first.st_ino) != (
                before.st_dev, before.st_ino):
            raise BootstrapRefusal('BUILDER_CHANGED')
        chunks = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        last = os.fstat(fd)
        if (first.st_size, first.st_mtime_ns, first.st_ctime_ns) != (
                last.st_size, last.st_mtime_ns, last.st_ctime_ns):
            raise BootstrapRefusal('BUILDER_CHANGED')
    finally:
        os.close(fd)
    raw = b''.join(chunks)
    if digest(raw) != BUILDER_SHA256:
        raise BootstrapRefusal('BUILDER_PIN_MISMATCH')
    rb = types.ModuleType('g26_builder_' + BUILDER_SHA256[:12])
    rb.__file__ = real
    exec(compile(raw, real, 'exec'), rb.__dict__)
    return rb, (real, raw, (first.st_dev, first.st_ino))


def seed_snapshot(snapshot, bootstrap):
    real, raw, identity = bootstrap
    if snapshot.paths or snapshot.identities:
        raise BootstrapRefusal('BOOTSTRAP_SNAPSHOT_ALREADY_USED')
    snapshot.paths[real] = (raw, identity)
    snapshot.identities[identity] = (raw, identity)
    snapshot.reads[real] = 1
    snapshot.requests[real] = 1


def require(rb, condition, code):
    if not condition:
        raise rb.Refused(code)


def read_pins(rb, pins, where):
    require(rb, isinstance(pins, list), 'G26_PIN_LIST')
    normalized = []
    for pin in pins:
        _, norm = rb.read_bytes_pin(pin, where)
        normalized.append(norm)
    require(rb, len({p['path'] for p in normalized}) == len(normalized),
            'G26_DUPLICATE_PIN')
    return normalized


def merge_pins(rb, *groups):
    by_path = {}
    for group in groups:
        for pin in group:
            old = by_path.get(pin['path'])
            require(rb, old is None or old == pin, 'G26_CONFLICTING_PIN')
            by_path[pin['path']] = pin
    return list(by_path.values())


def coordinate_projection(rb, rows, *, slots=False):
    require(rb, isinstance(rows, list) and len(rows) == 2,
            'G26_DN2_COORDINATE_SHAPE')
    projected = []
    names = set()
    for row in rows:
        require(rb, isinstance(row, dict) and set(SLOT_FIELDS) <= set(row),
                'G26_DN2_COORDINATE_SHAPE')
        require(rb, isinstance(row['name'], str) and row['name'] and row['name'] not in names,
                'G26_DN2_COORDINATE_SHAPE')
        names.add(row['name'])
        item = {}
        for key in SLOT_FIELDS:
            value = row[key]
            if key in NUMERIC_FIELDS:
                if value is None and key == 'reference_value':
                    item[key] = None
                else:
                    require(rb, type(value) in (int, float) and math.isfinite(value),
                            'G26_DN2_COORDINATE_SHAPE')
                    # IEEE-754 bits, including signed zero; no tolerance or rounding.
                    item[key] = float(value).hex()
            else:
                require(rb, isinstance(value, str), 'G26_DN2_COORDINATE_SHAPE')
                item[key] = value
        if not slots:
            require(rb, row.get('scope') == 'ngc3198_nuisance'
                    and row.get('role') == 'nuisance', 'G26_DN2_COORDINATE_SHAPE')
        projected.append(item)
    return projected


def check_coordinates(rb, coordinates, slots):
    require(rb, isinstance(coordinates, list), 'G26_DN2_COORDINATE_SHAPE')
    rows = [row for row in coordinates
            if isinstance(row, dict) and row.get('scope') == 'ngc3198_nuisance']
    expected = coordinate_projection(rb, slots.get('ngc3198_slots'), slots=True)
    actual = coordinate_projection(rb, rows)
    require(rb, actual == expected, 'G26_DN2_COORDINATES_MISMATCH')


@contextlib.contextmanager
def manifest_dn2_guard(rb, fm, slots, notes):
    """Check assembled manifest before v003g's exclusive write/registration."""
    original = fm._validate_manifest_structure
    seen = []
    def validate(manifest, reasons):
        try:
            check_coordinates(rb, manifest.get('coordinates'), slots)
            require(rb, rb.canonical_bytes(manifest.get('notes')) == rb.canonical_bytes(notes),
                    'G26_DN2_MANIFEST_NOTES_MISMATCH')
            seen.append(True)
        except rb.Refused as exc:
            reasons.append(exc.code)
            return
        return original(manifest, reasons)
    fm._validate_manifest_structure = validate
    try:
        yield seen
    finally:
        fm._validate_manifest_structure = original


def cleared_head(rb, ctx, head_pin):
    ledger = ctx['ledger']
    require(rb, not ctx['superseded'] and ledger['results'], 'G26_STEP7_NOT_CLEARED')
    head = ledger['results'][-1]
    require(rb, head.get('status') == 'NO_NEW_DISCREPANCY'
            and head.get('replay_plan_sha256') == ctx['plan_sha']
            and head.get('kind') in (None, 'COMPARE'), 'G26_STEP7_NOT_CLEARED')
    raw, norm = rb.read_bytes_pin(head_pin, 'external ledger head')
    expected_path = os.path.realpath(os.path.join(
        ledger['dir'], 'STEP7_%04d.json' % ledger['n']))
    require(rb, norm['sha256'] == ledger['last_sha'] and norm['path'] == expected_path
            and rb.strict_json(raw, 'ledger head') == head, 'G26_LEDGER_HEAD_MISMATCH')
    sha = head.get('pass_k_sha256')
    require(rb, rb._is_hex64(sha), 'G26_LEDGER_HEAD_PASS')
    pass_raw, pass_pin = rb.read_bytes_pin(
        {'path': os.path.join(ledger['dir'], 'PASS_' + sha + '.json'), 'sha256': sha},
        'ledger head PASS_K')
    passed = rb.strict_json(pass_raw, 'ledger head PASS_K')
    require(rb, passed.get('pass_label') == 'PASS_K', 'G26_LEDGER_HEAD_PASS')
    return head, norm, pass_raw, pass_pin


def freeze(rb, input_pin, out_dir):
    """One public command; only saved-state replay is reachable."""
    with rb.snapshot_scope() as snapshot:
        doc, inorm, _ = rb.read_json_pin(input_pin, 'G26 input')
        rb._keys(doc, INPUT_KEYS, 'G26 input')
        require(rb, doc['schema'] == INPUT_SCHEMA, 'G26_INPUT_SCHEMA')
        require(rb, isinstance(out_dir, str) and os.path.isabs(out_dir)
                and not os.path.lexists(out_dir), 'G26_OUTPUT_EXISTS_OR_NOT_ABSOLUTE')
        parent = os.path.dirname(os.path.abspath(out_dir))
        require(rb, os.path.isdir(parent), 'G26_OUTPUT_PARENT')
        passed_doc, pass_input_pin, _ = rb.read_json_pin(doc['pass_input'], 'PASS_K input')
        rb._keys(passed_doc, rb.PASS_INPUT_KEYS, 'PASS_K input')
        require(rb, passed_doc.get('schema') == 'PASS_INPUT_C2V003'
                and passed_doc.get('pass_label') == 'PASS_K', 'G26_PASS_K_REQUIRED')
        require(rb, passed_doc['freeze_module'].get('sha256') == FREEZE_SHA256,
                'G26_FREEZE_MODULE_PIN')
        _, builder_pin = rb.read_bytes_pin(
            {'path': BUILDER_PATH, 'sha256': BUILDER_SHA256}, 'fixed builder')
        require(rb, rb.own_pin() == builder_pin, 'G26_BUILDER_PIN')
        fm = rb.load_freeze_module(passed_doc['freeze_module'])
        rb.share_freeze_snapshot(fm)
        ctx = rb._plan_context(passed_doc['build_record'], passed_doc['replay_plan'], 'G26')
        plan = ctx['plan']
        require(rb, plan.get('stage') == 'FULL', 'G26_FULL_REQUIRED')
        head, head_pin, head_pass_raw, head_pass_pin = cleared_head(rb, ctx, doc['ledger_head'])
        spec, spec_pin, _ = rb.read_json_pin(passed_doc['spec'], 'spec of record')
        require(rb, spec_pin['sha256'] == SPEC_SHA256, 'G26_DN2_SPEC_SHA')
        notes, notes_pin, _ = rb.read_json_pin(doc['notes'], 'notes')
        require(rb, isinstance(notes, dict)
                and digest(rb.canonical_bytes(notes)) == NOTES_CANONICAL_SHA256,
                'G26_DN2_NOTES_SHA')
        slots, slots_pin, _ = rb.read_json_pin(doc['slots'], 'slots V003')
        require(rb, isinstance(slots, dict) and slots_pin['sha256'] == SLOTS_SHA256
                and fm.ROOT_SLOTS_SHA256 == SLOTS_SHA256
                and slots_pin['path'] == os.path.realpath(fm.ROOT_SLOTS_PATH),
                'G26_DN2_SLOTS_PIN')
        check_coordinates(rb, spec.get('coordinates'), slots)
        allow = rb.allow_incomplete_value(plan)
        require(rb, type(allow) is bool and plan.get('allow_incomplete') is allow,
                'G26_ALLOW_INCOMPLETE_NOT_REDERIVED')
        selection, selection_pin, _ = rb.read_json_pin(passed_doc['selection'], 'selection')
        roster_doc, roster_map_pin, _ = rb.read_json_pin(passed_doc['roster_pins'], 'roster mapping')
        roster_pins = roster_doc.get('row_registration_rosters')
        require(rb, isinstance(roster_pins, dict), 'G26_ROSTER_MAPPING')
        primary_roster, _, _ = rb.read_json_pin(roster_pins.get(plan['primary']), 'primary roster')
        qm_pin = primary_roster.get('query_manifest')
        qm_raw, qm_pin = rb.read_bytes_pin(qm_pin, 'query manifest')
        qm = fm.load_query_manifest(path=qm_pin['path'], expected_sha256=qm_pin['sha256'])
        require(rb, isinstance(qm, dict) and qm.get('ok') is True, 'G26_QUERY_MANIFEST')
        if QUERY_ROLE == 'PROGRAM_PIN':
            require(rb, qm_pin['sha256'] == fm.PROGRAM_QUERY_MANIFEST_SHA256,
                    'G26_PROGRAM_QUERY_MANIFEST')
        parameter_region, parameter_pin, _ = rb.read_json_pin(doc['parameter_region'], 'parameter region')
        observation_rule, observation_pin, _ = rb.read_json_pin(doc['observation_rule'], 'observation rule')
        code_pins = read_pins(rb, doc['code_files'], 'code files')
        input_pins = read_pins(rb, doc['input_files'], 'input files')
        own_raw, own_real = snapshot.read(__file__, 'G26 source')
        own_pin = {'path': own_real, 'sha256': digest(own_raw)}
        _, freeze_pin = rb.read_bytes_pin(passed_doc['freeze_module'], 'freeze source')
        code_pins = merge_pins(rb, code_pins, [builder_pin, freeze_pin, own_pin])
        # Preserve external evidence, specification and metadata bytes in the freeze.
        input_pins = merge_pins(rb, input_pins, [
            inorm, pass_input_pin, head_pin, head_pass_pin, ctx['record_pin'],
            passed_doc['replay_plan'], spec_pin, notes_pin, slots_pin, selection_pin,
            roster_map_pin, qm_pin, parameter_pin, observation_pin])
        require(rb, not {p['path'] for p in code_pins}.intersection(
            p['path'] for p in input_pins), 'G26_CODE_INPUT_OVERLAP')
        alternatives = slots.get('alternatives')
        require(rb, isinstance(alternatives, dict)
                and alternatives.get('primary') == plan['primary'], 'G26_ALTERNATIVES')
        record, extract, memory = rb.pass_driver(fm, passed_doc)
        require(rb, extract is None and rb.dump_bytes(record) == head_pass_raw,
                'G26_PASS_K_BYTES_DIFFER')
        # Everything above is read-only. A failure below leaves its new directory
        # and any partial files intact. Retry uses a different output directory.
        os.mkdir(out_dir)
        manifest_path = os.path.join(out_dir, OUTPUT_NAMES[0])
        registration_path = os.path.join(out_dir, OUTPUT_NAMES[1])
        with rb.geometry_runtime(fm, plan), manifest_dn2_guard(rb, fm, slots, notes) as seen:
            result = fm.write_freeze_manifest(
                out_path=manifest_path, registration_path=registration_path,
                parameter_region=parameter_region, observation_rule=observation_rule,
                spec=spec, selection=selection, alternatives=alternatives,
                alternative_evaluations=memory['envelopes'], reference=memory['reference'],
                sensitivity=memory['sensitivity'], query_ids=qm['query_ids'],
                query_manifest=dict(qm_pin, role=QUERY_ROLE),
                code_files=[p['path'] for p in code_pins],
                input_files=[p['path'] for p in input_pins], notes=notes,
                allow_incomplete=allow, row_registration_rosters=roster_pins)
        require(rb, isinstance(result, dict) and result.get('ok') is True,
                'G26_WRITER_REFUSED')
        require(rb, seen, 'G26_MANIFEST_DN2_NOT_EXECUTED')
        manifest_pin = {'path': manifest_path, 'sha256': result['manifest_file_sha256']}
        manifest, manifest_pin, _ = rb.read_json_pin(manifest_pin, 'written manifest')
        check_coordinates(rb, manifest.get('coordinates'), slots)
        require(rb, rb.canonical_bytes(manifest.get('notes')) == rb.canonical_bytes(notes),
                'G26_DN2_MANIFEST_NOTES_MISMATCH')
        require(rb, manifest.get('row_registration_rosters') == roster_pins,
                'G26_MANIFEST_ROSTERS_CHANGED')
        registration_pin = {'path': registration_path, 'sha256': result['registration_file_sha256']}
        registration, registration_pin, _ = rb.read_json_pin(registration_pin, 'registration')
        require(rb, registration.get('expected_manifest_file_sha256') == manifest_pin['sha256']
                and registration.get('manifest_path') == manifest_pin['path'],
                'G26_REGISTRATION_BINDING')
        report = {
            'schema': RESULT_SCHEMA, 'verdict': 'PASS', 'input': inorm,
            'builder': builder_pin, 'freeze_module': freeze_pin, 'wrapper': own_pin,
            'ledger_head': head_pin, 'ledger_pass_k': head_pass_pin,
            'pass_k_byte_equal': True, 'allow_incomplete': allow,
            'dn2_spec': spec_pin, 'dn2_notes': notes_pin,
            'dn2_notes_canonical_sha256': NOTES_CANONICAL_SHA256,
            'dn2_slots': slots_pin, 'dn2_coordinates_equal': True,
            'manifest': manifest_pin, 'registration': registration_pin,
            'freeze_status': result['freeze_status'],
            'scientific_launch_performed': False, 'target_access_performed': False,
            'root_prerequisites': 'seal/reading gates and G28 ledger-root adoption remain external',
            'forbidden_set_lineage': 'v003g inherits P46 set plus four interface target-row names',
        }
        audit = snapshot.audit()
        require(rb, not audit['violations'], 'G26_SINGLE_READ_VIOLATION')
        rb.write_exclusive(os.path.join(out_dir, OUTPUT_NAMES[2]), rb.dump_bytes(report))
        rb.write_exclusive(os.path.join(out_dir, OUTPUT_NAMES[3]), rb.dump_bytes(audit))
        return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True)
    ap.add_argument('--input-sha256', required=True)
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args(argv)
    try:
        rb, bootstrap = bootstrap_builder()
        with rb.snapshot_scope() as snapshot:
            seed_snapshot(snapshot, bootstrap)
            report = freeze(rb, {'path': args.input, 'sha256': args.input_sha256}, args.out_dir)
        print(json.dumps({'verdict': 'PASS', 'manifest': report['manifest'],
                          'registration': report['registration']}, sort_keys=True))
        return 0
    except Exception as exc:
        # No prediction, coordinate, target-like key, or arbitrary exception text.
        code = exc.code if hasattr(exc, 'code') else (
            str(exc) if isinstance(exc, BootstrapRefusal) else type(exc).__name__)
        print(json.dumps({'verdict': 'REFUSED', 'code': code,
                          'partial_outputs_preserved': True}, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
