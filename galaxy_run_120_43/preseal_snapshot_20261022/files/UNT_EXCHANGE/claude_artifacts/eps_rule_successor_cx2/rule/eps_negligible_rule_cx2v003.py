#!/usr/bin/env python3
"""A296 saved-record re-evaluation. No EPS search, project imports or launches.

Trust boundary: record and audit bytes, and audit-producer source bytes, are
independently pinned by the caller. A matching hash establishes byte identity,
not scientific or signer approval. Every changed output requires review.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import math
import os
import re
import subprocess
import sys

M = 10
F = 0.1
ABSOLUTE_FLOOR = 1e-6
AUDIT_RATIO_MAX = 1.05
ORIGINAL_PRODUCER_SHA256 = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
AUTHORITY_SHA256 = 'd1656a16e386b5bb1d0c6dd566706cd3d06ed47ec83ae1d6bf69b9d10238ea92'
AUTHORITY_PATH = str(Path(__file__).parent.parent / 'A296_AUTHORITY_CX2V001.json')
NEW_VERDICT = 'NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED'
OLD_PASS = 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED'
AUDIT_SCHEMA = 'UNT_EPS_NEGLIGIBLE_DENSE_AUDIT_CX2V001'


class Refusal(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def finite(value, label, positive=False):
    require(type(value) in (int, float), label + ': finite number required; bool forbidden')
    try:
        is_finite = math.isfinite(value)
    except OverflowError:
        is_finite = False
    require(is_finite, label + ': finite representable number required')
    require(not positive or value > 0, label + ': positive required')
    return value


def epsilon(value, label):
    value = finite(value, label)
    require(value >= 0, label + ': nonnegative epsilon required')
    return value


def check_finiteness(value):
    if type(value) is float:
        require(math.isfinite(value), 'nonfinite JSON number')
    elif isinstance(value, dict):
        for v in value.values():
            check_finiteness(v)
    elif isinstance(value, list):
        for v in value:
            check_finiteness(v)


def sha_string(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None, 'invalid sha256')
    return value


def pin(value, label):
    require(isinstance(value, dict) and set(value) == {'path', 'sha256'}, label + ': exact path/sha256 pin required')
    require(isinstance(value['path'], str) and value['path'] != '', label + ': path required')
    sha_string(value['sha256'])
    return value


def pair(value, label):
    require(isinstance(value, list) and len(value) == 2, label + ': two numeric endpoints required')
    return [finite(v, label) for v in value]


def strict_json(raw):
    def unique(items):
        obj = {}
        for key, value in items:
            require(key not in obj, 'duplicate JSON key: ' + key)
            obj[key] = value
        return obj
    try:
        obj = json.loads(raw, object_pairs_hook=unique, parse_constant=lambda value: (_ for _ in ()).throw(Refusal('nonfinite JSON token: ' + value)))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise Refusal('malformed JSON') from exc
    check_finiteness(obj)
    return obj


def validate_record(record):
    require(isinstance(record, dict), 'record object required')
    check_finiteness(record)
    require(record.get('schema') == 'UNT_POINT_EPS_NUMERICAL_CX2V001', 'wrong EPS schema')
    require(record.get('gate') == 'EPS', 'wrong EPS gate')
    require(record.get('status') == 'TESTED' and record.get('settings') == 'registered', 'TESTED registered settings required')
    require(record.get('full_registered_search_executed') is True and record.get('coverage_complete') is True, 'full registered coverage required')
    require(pair(record.get('required_coverage_inverse_kpc'), 'coverage') == [4, 182], 'coverage must be [4,182]')
    require(record.get('production_admissible') is False and record.get('rigorous_supremum') is False, 'original numerical-only record required')
    sha_string(record.get('point_sha256'))
    require(pin(record.get('producer'), 'original producer')['sha256'] == ORIGINAL_PRODUCER_SHA256, 'original producer pin mismatch')
    require('successor_rule_verdict' not in record and 'accepted_shells' not in record, 'successor cannot be re-applied')
    shells = record.get('shells')
    require(isinstance(shells, list) and len(shells) == 178, 'exactly178 shells required')
    eps_max = epsilon(record.get('eps_max'), 'eps_max')
    max_shell = pair(record.get('eps_max_shell'), 'eps_max_shell')
    failures = []
    for index, shell in enumerate(shells):
        require(isinstance(shell, dict), 'shell object required')
        expected = [index + 4, index + 5]
        require(pair(shell.get('range_inverse_kpc'), 'shell range') == expected, 'shell gap/order/range mismatch')
        require(finite(shell.get('lo_inverse_kpc'), 'shell lo') == expected[0] and finite(shell.get('hi_inverse_kpc'), 'shell hi') == expected[1], 'shell endpoint mismatch')
        require(type(shell.get('certified')) is bool, 'shell certified boolean required')
        refinements = shell.get('refinements')
        require(type(refinements) is int and refinements in (0, 1, 2), 'invalid refinements')
        require('accepted_negligible' not in shell and 'eps_measured_before_negligible_substitution' not in shell, 'already-substituted shell forbidden')
        levels = shell.get('levels')
        require(isinstance(levels, dict) and set(levels) == ({'0', '1'} if refinements == 0 else {'0', '1', '2'}), 'wrong saved level set')
        values = {}
        for level, entry in levels.items():
            require(isinstance(entry, dict), 'level object required')
            values[level] = epsilon(entry.get('eps'), 'level epsilon')
        base = epsilon(shell.get('eps_base'), 'eps_base')
        refined = epsilon(shell.get('eps_refined'), 'eps_refined')
        if refinements == 0:
            require(base == values['0'] and refined == values['1'] and refined <= 1.1 * base, 'level0/1 rule mismatch')
        else:
            require(values['1'] > 1.1 * values['0'], 'spurious level2 refinement')
            require(base == values['1'] and refined == values['2'], 'level1/2 fields mismatch')
            require((refinements == 1) == (refined <= 1.1 * base), 'level2 decision mismatch')
        require(shell['certified'] == (refinements != 2), 'original certification flag mismatch')
        measured = epsilon(shell.get('eps'), 'measured shell epsilon')
        envelope = shell.get('envelope')
        actual = shell.get('actual')
        require(isinstance(envelope, dict) and isinstance(actual, dict), 'envelope/actual records required')
        env = epsilon(envelope.get('estimate'), 'envelope estimate')
        envelope_with_saved_audits = epsilon(shell.get('eps_envelope'), 'eps_envelope')
        require(envelope_with_saved_audits >= env, 'envelope field below production estimate')
        actual_eps = epsilon(actual.get('estimate'), 'actual estimate')
        require(measured >= max(base, refined, envelope_with_saved_audits, actual_eps), 'measured shell epsilon below saved component')
        if refinements == 2:
            failures.append(index)
    require(eps_max == max(s['eps'] for s in shells), 'eps_max inconsistent with measured shells')
    require(any(s['range_inverse_kpc'] == max_shell and s['eps'] == eps_max for s in shells), 'eps_max_shell mismatch')
    if failures:
        require(record.get('registered_discrete_verdict') == 'EPS_UNCERTIFIED' and record.get('verdict') == 'EPS_UNCERTIFIED', 'original failed verdict mismatch')
    else:
        require(record.get('registered_discrete_verdict') == 'CERTIFIED' and record.get('verdict') == OLD_PASS, 'original pass verdict mismatch')
    return failures


def validate_audit(audit, record, shell, record_pin, audit_producer_pin):
    require(isinstance(audit, dict), 'dense audit object required')
    check_finiteness(audit)
    require(audit.get('schema') == AUDIT_SCHEMA, 'wrong dense audit schema')
    require(audit.get('status') == 'TESTED' and audit.get('settings') == 'registered', 'registered TESTED dense audit required')
    require(pin(audit.get('source_record'), 'audit source record') == record_pin, 'audit record identity mismatch')
    require(audit.get('point_sha256') == record['point_sha256'], 'audit point identity mismatch')
    require(pin(audit.get('original_producer'), 'audit original producer') == record['producer'], 'audit original producer mismatch')
    require(pin(audit.get('audit_producer'), 'audit producer') == audit_producer_pin, 'audit producer pin mismatch')
    require(pair(audit.get('range_inverse_kpc'), 'audit shell') == shell['range_inverse_kpc'], 'audit shell mismatch')
    production = finite(audit.get('production'), 'audit production', True)
    require(production == shell['envelope']['estimate'], 'audit denominator differs from saved production envelope')
    dense = epsilon(audit.get('dense'), 'audit dense')
    search = audit.get('dense_search')
    require(isinstance(search, dict), 'dense search metadata required')
    require(epsilon(search.get('estimate'), 'dense search estimate') == dense, 'dense estimate mismatch')
    for key, expected in (('torus_m', 20), ('direction_count', 400), ('starts', 16), ('n_grid', 16000000)):
        require(type(search.get(key)) is int and search[key] == expected, 'registered dense search metadata mismatch: ' + key)
    radial = search.get('radial_fractions')
    require(isinstance(radial, list) and len(radial) == 5, 'dense radial grid missing')
    require([finite(v, 'dense radial fraction') for v in radial] == [0, 0.25, 0.5, 0.75, 1], 'dense radial grid mismatch')
    ratio = epsilon(audit.get('dense_over_production'), 'audit ratio')
    require(ratio == dense / production, 'audit ratio inconsistent with saved values')
    require(ratio <= AUDIT_RATIO_MAX, 'R1c: dense audit ratio exceeds1.05')
    return ratio


def reevaluate(record, audit, *, record_pin, audit_pin=None, audit_producer_pin=None,
               successor_producer, date_u):
    """Pure saved-record arithmetic. Caller authenticates all passed byte pins."""
    pin(record_pin, 'input record')
    pin(successor_producer, 'successor producer')
    failures = validate_record(record)
    if not failures:
        return {'status': 'UNCHANGED', 'source_record': record_pin,
                'reason': 'Original registered discrete rule already certifies every shell; no output record needed.'}, None
    require(len(failures) == 1, 'R1d: every other shell must certify; multiple failing shells refused')
    index = failures[0]
    shell = record['shells'][index]
    measured = shell['eps']
    substituted = M * measured
    require(math.isfinite(substituted) and substituted <= F * record['eps_max'], 'R1a: ten times measured shell epsilon exceeds0.1 eps_max')
    growth = abs(shell['levels']['2']['eps'] - shell['levels']['1']['eps'])
    require(growth <= ABSOLUTE_FLOOR, 'R1b: absolute level2-level1 change exceeds1e-6')
    require(audit is not None and audit_pin is not None and audit_producer_pin is not None, 'R1c: authenticated dense audit required')
    pin(audit_pin, 'dense audit file')
    pin(audit_producer_pin, 'dense audit producer source')
    ratio = validate_audit(audit, record, shell, record_pin, audit_producer_pin)
    result = copy.deepcopy(record)
    changed = result['shells'][index]
    changed.update({'eps': substituted, 'eps_measured_before_negligible_substitution': measured,
                    'accepted_negligible': True, 'acceptance': 'ACCEPTED_NEGLIGIBLE',
                    'negligible_acceptance_evidence': {'M': M, 'f': F, 'absolute_floor': ABSOLUTE_FLOOR,
                        'absolute_level2_minus_level1': growth, 'dense_over_production': ratio,
                        'dense_audit': copy.deepcopy(audit_pin)}})
    require(changed['certified'] is False and changed['refinements'] == 2, 'discrete history changed')
    require(result['eps_max'] == record['eps_max'] and result['eps_max_shell'] == record['eps_max_shell'], 'maximum metadata changed')
    result.update({'verdict': NEW_VERDICT, 'successor_rule_verdict': 'ACCEPTED_NEGLIGIBLE',
                   'accepted_shells': [copy.deepcopy(changed['range_inverse_kpc'])],
                   'approved_signer_review_required': True,
                   'predecessor': {'record': copy.deepcopy(record_pin), 'producer': copy.deepcopy(record['producer']),
                                   'verdict': record['verdict'], 'registered_discrete_verdict': record['registered_discrete_verdict']},
                   'producer': copy.deepcopy(successor_producer),
                   'rule_authority': {'path': AUTHORITY_PATH, 'sha256': AUTHORITY_SHA256, 'heading': 'A296'},
                   'successor_date_u': date_u,
                   'successor_limitations': 'Saved numerical-rule re-evaluation only. No new supremum guarantee or scientific admission. Approved-signer review and root adoption required.'})
    return {'status': NEW_VERDICT, 'source_record': record_pin, 'accepted_shells': result['accepted_shells']}, result


def load_pinned(path, expected):
    sha_string(expected)
    raw = Path(path).read_bytes()
    require(digest(raw) == expected, 'input bytes do not match supplied sha256: ' + path)
    return strict_json(raw), {'path': path, 'sha256': expected}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', required=True)
    parser.add_argument('--record-sha256', required=True)
    parser.add_argument('--audit')
    parser.add_argument('--audit-sha256')
    parser.add_argument('--audit-producer-sha256')
    parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        require(not Path(args.output).exists(), 'output already exists; immutable successor requires a new path')
        require(digest(Path(AUTHORITY_PATH).read_bytes()) == AUTHORITY_SHA256, 'A296 authority snapshot bytes mismatch')
        record, record_pin = load_pinned(args.record, args.record_sha256)
        audit = audit_pin = producer_pin = None
        supplied = [args.audit is not None, args.audit_sha256 is not None, args.audit_producer_sha256 is not None]
        require(not any(supplied) or all(supplied), 'all three audit arguments required together')
        if all(supplied):
            audit, audit_pin = load_pinned(args.audit, args.audit_sha256)
            require(isinstance(audit, dict), 'dense audit object required')
            producer_pin = pin(audit.get('audit_producer'), 'audit producer')
            require(producer_pin['sha256'] == sha_string(args.audit_producer_sha256), 'caller audit producer pin mismatch')
            require(digest(Path(producer_pin['path']).read_bytes()) == args.audit_producer_sha256, 'audit producer source bytes mismatch')
        source = {'path': str(Path(__file__).absolute()), 'sha256': digest(Path(__file__).read_bytes())}
        date_u = subprocess.check_output(['/bin/date', '-u'], env={**os.environ, 'LC_ALL': 'C'}, text=True).strip()
        result, successor = reevaluate(record, audit, record_pin=record_pin, audit_pin=audit_pin,
                                      audit_producer_pin=producer_pin, successor_producer=source, date_u=date_u)
        if successor is not None:
            raw = (json.dumps(successor, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
            with Path(args.output).open('xb') as output:
                output.write(raw)
            result['output'] = {'path': args.output, 'sha256': digest(raw)}
        result['date_u'] = date_u
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (Refusal, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
