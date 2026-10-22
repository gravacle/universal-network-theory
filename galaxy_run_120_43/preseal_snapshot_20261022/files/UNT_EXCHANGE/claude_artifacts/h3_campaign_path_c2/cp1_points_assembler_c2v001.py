"""CP-1 list-of-points assembler (Claude2 h3_campaign_path_c2, c2v001; V006 A192 item 2): successor of registry_assembler_c3v004
(cb5c61ee).

Table mode (no --points-list): this CLI IS the c3v004 assembler's main(argv), from its pinned bytes (rows 1-31 unchanged:
bundle, registry, verify).
List mode (--points-list L --points-list-sha256 H; cp1_points_common_c2v001 for the list rules):
  bundle   c3v004 assemble_bundle on one list row (EPS from adapter v003, GQ from gq_producer v005, LO_RHO_SLOT from the slot
           proof producer; the lo slot is the point's registered rho record; every c3v004 refusal holds);
  records  the ledger records of a wave: for EVERY list point exactly one bundle, read from its bytes, whose identity is the
           list spec's identity (core recipe) and whose three proofs name approved producers; per point the registry record
           {identity, bundle, eps_certificate, lo_certificate} (c3v004 assemble_registry L301-302, the form the wrapper's
           lookup reads) plus the list's theta, pending spec sha and wave, which the entry's ledger-append needs to rebuild
           the planned spec.  The EPS source pins must agree across the points and, given --genesis-registry, with the
           genesis registry's eps_source_pins_digest (c3v004 L308-309: upstream code or data drifted).  Exclusive create:
           <out-root>/LEDGER_RECORDS_W<wave>_<n>pts_<UTC>.json, schema CP1_POINTS_LEDGER_RECORDS_C2V001;
  verify   OFFLINE and read-only, c3v004's replica per list point: c1_policy_gate on the C1 document (it must name the
           genesis registry), then verify_point (wrapper q5b1 L80-93, L145-191 executed from the 7a6af535 bytes, the L30
           guard's verify_bundle) with the records as the registry; and no record key is a genesis key.  Not launch
           authorization; the entry's ledger-append runs the wrapper's own prelaunch_check before it appends.
Out-roots are c3v004's rule: an existing canonical <s4rc1_c3>/registry_<name> folder.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
SELF = os.path.realpath(__file__)
COMMON2 = (HERE + '/cp1_points_common_c2v001.py', '302abdad6b076190f7bc8e79cc71cf4de91402a1a216eb94c254acf2be22c27e')     # P2


def _load_common2():
    p = COMMON2[0]
    with open(p, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != COMMON2[1]:
        raise SystemExit('REFUSED: cp1_points_common pin mismatch')
    sp = importlib.util.spec_from_file_location('cp1_points_common_c2v001_a', p)
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    exec(compile(raw, p, 'exec'), m.__dict__)
    return m


P = _load_common2()
A = P.load_module(P.ASSEMBLER[0], P.ASSEMBLER[1], 'registry_assembler_c3v004')
C = A.C
Refusal = C.Refusal


def self_pin():
    return P.pin_of_self(SELF)


def assemble_records(list_ref, doc, rows, bundle_paths, *, approved, out_root, roots=(C.ART,), genesis_ref=None):
    by_key = {r['key']: r for r in rows}
    recs, deps, seen = [], {}, set()
    for bp in bundle_paths:
        pin = C.pin_of(bp, roots, 'bundle')
        b = C.read_json_pinned(pin, roots, 'bundle')
        if b.get('schema') != C.BUNDLE_SCHEMA:
            raise Refusal('BUNDLE_SCHEMA')
        ident = b.get('identity')
        key = C.digest(ident)
        row = by_key.get(key)
        if row is None:
            raise Refusal('BUNDLE_POINT_NOT_IN_POINTS_LIST: ' + key[:16])
        if ident != C.point_identity(A.load_point_spec(row)):
            raise Refusal('BUNDLE_IDENTITY_DIFFERS_FROM_THE_LIST_SPEC')
        if key in seen:
            raise Refusal('DUPLICATE_POINT: ' + key[:16])
        seen.add(key)
        slots = b.get('driver_certificate_bindings') or {}
        if set(slots) != {'eps_certificate', 'lo_certificate'} or not all(C.is_pin(v) for v in slots.values()):
            raise Refusal('BUNDLE_SLOT_BINDINGS')
        eps_rec = C.read_json_pinned(slots['eps_certificate'], roots, 'EPS numeric record', max_bytes=None)
        deps[key] = C.digest({'dependencies': eps_rec.get('dependencies'), 'producer': eps_rec.get('producer')})
        for gate in ('EPS', 'GQ', A.SLOT_GATE):
            proof = C.read_json_pinned(b['prelaunch'][gate], roots, gate + ' proof')
            if proof.get('producer') not in approved:
                raise Refusal(gate + '_PRODUCER_NOT_APPROVED')
        recs.append({'key': key, 'label': row['label'], 'row': row['row'], 'wave': row['wave'], 'theta': row['theta'],
                     'pending_spec_sha256': row['pending_spec_sha256'],
                     'record': {'identity': ident, 'bundle': pin, 'eps_certificate': slots['eps_certificate'],
                                'lo_certificate': slots['lo_certificate']}})
    missing = [r['label'] for r in rows if r['key'] not in seen]
    if missing:
        raise Refusal('POINTS_WITHOUT_A_BUNDLE (a wave is registered whole): %s' % missing)
    if len(set(deps.values())) != 1:
        raise Refusal('EPS_SOURCE_PINS_DIFFER_ACROSS_POINTS (upstream code or data drifted during CP-1)')
    eps_digest = next(iter(deps.values()))
    gen = None
    if genesis_ref is not None:
        gen = C.read_json_pinned(genesis_ref, roots, 'genesis registry')
        gd = gen.get('eps_source_pins_digest')
        if gd is not None and gd != eps_digest:
            raise Refusal('EPS_SOURCE_PINS_DIFFER_FROM_THE_GENESIS_REGISTRY (upstream code or data drifted since CP-1)')
        clash = [r['key'][:16] for r in recs if r['key'] in (gen.get('points') or {})]
        if clash:
            raise Refusal('POINT_ALREADY_IN_THE_GENESIS_REGISTRY: %s' % clash)
    order = {r['key']: i for i, r in enumerate(rows)}
    recs.sort(key=lambda x: order[x['key']])
    out = {'schema': P.RECORDS_SCHEMA, 'utc': C.utc(), 'points_list': dict(list_ref), 'wave': doc['wave'], 'count': len(recs),
           'records': recs, 'eps_source_pins_digest': eps_digest, 'genesis_registry': genesis_ref,
           'approved_certificate_producers': approved, 'generator': self_pin(),
           'c3v004_assembler': {'path': P.ASSEMBLER[0], 'sha256': P.ASSEMBLER[1]},
           'record_rule': ('records[i].record = {identity, bundle, eps_certificate, lo_certificate} (c3v004 assemble_registry '
                           'L301-302; core L249-259, wrapper L86-90); the entry ledger-append rebuilds the spec from theta')}
    return C.write_new(os.path.join(out_root, 'LEDGER_RECORDS_W%04d_%02dpts_%s.json' % (doc['wave'], len(recs), C.utc_compact())),
                       out, out_root)


def verify_list(records_ref, rows, *, c1_ref, genesis_ref, custody_loader, guard, roots=(C.ART,), guard_roots=None):
    doc = C.read_json_pinned(records_ref, roots, 'ledger records')
    if doc.get('schema') != P.RECORDS_SCHEMA or not isinstance(doc.get('records'), list):
        raise Refusal('LEDGER_RECORDS_SCHEMA')
    registry = {'points': {r['key']: r['record'] for r in doc['records']}}
    gen = C.read_json_pinned(genesis_ref, roots, 'genesis registry')
    clash = [k[:16] for k in registry['points'] if k in (gen.get('points') or {})]
    tr, policy = A.c1_policy_gate(c1_ref, genesis_ref, roots=roots)
    approved, custody_fn = None, None
    if not policy:
        approved = tr['approved_certificate_producers']
        custody_fn = custody_loader(tr['custody_deriver'])
    out = [A.verify_point(r, registry, approved=approved, custody_fn=custody_fn, guard=guard, roots=roots,
                          guard_roots=guard_roots, policy_blockers=policy) for r in rows]
    unlisted = sorted(k[:16] for k in registry['points'] if k not in {r['key'] for r in rows})
    ok = not policy and not clash and not unlisted and all(x['ok'] for x in out)
    return {'schema': 'CP1_POINTS_OFFLINE_VERIFY_C2V001', 'utc': C.utc(), 'records': records_ref, 'c1': c1_ref,
            'genesis_registry': genesis_ref, 'c1_policy_gate': {'ok': not policy, 'blockers': policy},
            'keys_already_in_genesis': clash, 'record_keys_not_in_the_list': unlisted, 'points': out, 'ok': ok,
            'n_ok': sum(x['ok'] for x in out), 'n': len(out), 'generator': self_pin(),
            'scope': 'c3v004 offline replica (verify_point) per list point; not launch authorization'}


def list_rows(ns):
    ref = {'path': ns.points_list, 'sha256': ns.points_list_sha256}
    doc, rows = P.load_points_list(C, ref)
    return ref, doc, rows


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--points-list' not in argv:
        return A.main(argv)                           # table mode: the c3v004 CLI itself
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('bundle')
    for a in ('--out-root', '--point', '--eps-proof', '--gq-proof', '--lo-proof', '--approved-producers'):
        b.add_argument(a, required=True)
    r = sub.add_parser('records')
    r.add_argument('--out-root', required=True)
    r.add_argument('--bundle', action='append', required=True)
    r.add_argument('--approved-producers', required=True)
    r.add_argument('--genesis-registry')
    r.add_argument('--genesis-registry-sha256')
    v = sub.add_parser('verify')
    v.add_argument('--records', required=True)
    v.add_argument('--records-sha256', required=True)
    v.add_argument('--c1', required=True)
    v.add_argument('--c1-sha256', required=True)
    v.add_argument('--genesis-registry', required=True)
    v.add_argument('--genesis-registry-sha256', required=True)
    v.add_argument('--out-root')
    for sp_ in (b, r, v):
        sp_.add_argument('--points-list', required=True)
        sp_.add_argument('--points-list-sha256', required=True)
    ns = ap.parse_args(argv)
    try:
        ref, doc, rows = list_rows(ns)
        if ns.cmd in ('bundle', 'records'):
            approved, _ = A.load_approved(ns.approved_producers, (C.ART,))
        if ns.cmd == 'bundle':
            sel = P.select_list_rows(C, rows, ns.point)
            if len(sel) != 1:
                raise Refusal('ONE_POINT_REQUIRED')
            pin = A.assemble_bundle(sel[0], eps_proof=ns.eps_proof, gq_proof=ns.gq_proof, lo_proof=ns.lo_proof,
                                    approved=approved, out_root=A._out_root(ns.out_root))
            print(json.dumps({'bundle': pin}))
            return 0
        if ns.cmd == 'records':
            g = None
            if ns.genesis_registry:
                g = {'path': C.require_canonical(ns.genesis_registry), 'sha256': ns.genesis_registry_sha256}
            pin = assemble_records(ref, doc, rows, ns.bundle, approved=approved, out_root=A._out_root(ns.out_root),
                                   genesis_ref=g)
            print(json.dumps({'records': pin}))
            return 0
        if not C.background_qos():
            raise Refusal('BACKGROUND_QOS_REQUIRED for custody derivation: run under taskpolicy -b')
        rec_ref = {'path': C.require_canonical(ns.records), 'sha256': ns.records_sha256}
        rep = verify_list(rec_ref, rows, c1_ref={'path': C.require_canonical(ns.c1), 'sha256': ns.c1_sha256},
                          genesis_ref={'path': C.require_canonical(ns.genesis_registry), 'sha256': ns.genesis_registry_sha256},
                          custody_loader=A.real_custody_fn, guard=A.real_guard())
        if ns.out_root:
            o = A._out_root(ns.out_root)
            rep['written'] = C.write_new(os.path.join(o, 'VERIFY_LIST_%s_%s.json' % (ns.records_sha256[:12], C.utc_compact())),
                                         rep, o)
        print(json.dumps({'ok': rep['ok'], 'n_ok': rep['n_ok'], 'n': rep['n'], 'written': rep.get('written'),
                          'c1_policy_gate_blockers': rep['c1_policy_gate']['blockers']}))
        return 0 if rep['ok'] else 3
    except Refusal as exc:
        print(json.dumps({'status': 'REFUSED', 'reason': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
