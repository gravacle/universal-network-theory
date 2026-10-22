# Claude4 helper, dispatch 0587 part (a): reconcile the inventory run list against the dry-plan spec list.
# v002 = v001 + (1) inventory v007_inputs mapped into the item set, (2) the dry plans' campaign_level_gates mapped into the
# S4-CAMPAIGN pair, (3) EXPLAIN entries for operational root items a plan-only run cannot see. v001's record is kept (superseded).
# Read-only on the two sibling folders; writes one exclusive-create JSON record in this folder.
# No driver or orchestrator is imported. The fence is installed first anyway.
# Usage: python3 -I -B reconcile_c4v001.py <new output json>
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_c4v001 as F  # audit hook installed at import
import hashlib, json, datetime

S4 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4'
CX2 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2'
# Expected full sha256 values pasted from `shasum -a 256` output taken at 19:2xZ in this session.
EXPECTED = {
    S4 + '/inventory/INVENTORY_C4V001.json': 'eb359e0f902298b4d8d41e879b1ba85f852e4bf29d7d9d126a66dc239baee75b',
    S4 + '/inventory/ROOT_ITEMS_C4V001.json': 'a48ca79d0b0192dc842366d8c50e63a2bd3d9ff45c732e048d39f926eaa0da22',
    S4 + '/inventory/INVENTORY_C4V001.md': 'cabdd70e7df0cedf47a76e4669c7b148bbe9dfb49a6a81f6890a873196cf61ec',
    S4 + '/inventory/ROOT_ITEMS_C4V001.md': 'e6e80d0df1fa5caf101e68662677522cee365fc64e7a1e57d309da47740b0c40',
    S4 + '/dryplans/DRYPLANS_C4V002.json': '756d36ec5ecf15406fd52ddefcb9c57c4212f261cfc5a8fd24489cc7eb77d22d',
    S4 + '/dryplans/DRYPLANS_C4V001.json': 'e301bafd6e3c77dbae806c85f6958c6d6b3de45273abf4d2ab8780807d40e87d',
    S4 + '/dryplans/DRYPLANS_C4V001.md': '1516c3c0a2c18b15778f78b95b965bfe75a3ca448d6595bd9d358dd21330ce8f',
}


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(p):
    with open(p, 'rb') as f:
        return json.loads(f.read())


def leaves(x, p=''):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(leaves(v, p + '/' + str(k)))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out.update(leaves(v, p + '/' + str(i)))
    else:
        out[p] = x
    return out


def leaf_diff(a, b):
    la, lb = leaves(a), leaves(b)
    keys = sorted(set(la) | set(lb))
    return [k for k in keys if (k not in la) or (k not in lb) or (type(la[k]) is not type(lb[k])) or la[k] != lb[k]]


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'))


# ------------------------------------------------------------------ mapping tables (documented, FORMAL)
INV_DEP_TO_ITEM = [
    ('GATE:V007_SEALED_ADOPT_TAIL', 'V007:V7-READ'),
    ('CFG:adopted block', 'V007:V7-BLOCK'),
    ('REGISTRY:prelaunch bundle for this point (if slots from registry)', 'R-C1(conditional)'),
    ('REGISTRY:prelaunch bundle', 'R-C1'),
    ('ROOT:direct-run caps (R-D8)', 'R-D8'), ('ROOT:caps (R-D8)', 'R-D8'),
    ('ROOT:designation (R-D2)', 'R-D2'),
    ('GATE:sensitivity_deciding_iii', 'R-B2+R-C5+R-D5'),
    ('ROOT:reading registered (R-C7)', 'R-C7'),
    ('ROOT:caps (R-D5)', 'R-D5'),
    ('ROOT:launch timing', 'R-D5'),
    ('ROOT:R-B1 driver ruling', 'R-B1'), ('r6 BUILD + identity gates (A89)', 'R-B1'),
    ('GATE:deciding_test', 'R-D4'), ('GATE:numerics_verdict', 'V007:numerics_verdict+R-A2'),
    ('GATE:driver_capability', 'R-D3'), ('GATE:adoption_regeneration', 'R-A4+R-A5'),
    ('GATE:u_i_carrier', 'R-C2'), ('GATE:certificate_policy', 'R-C1'),
    ('ROOT:launch entry, scheduling and caps', 'R-B4+R-D7+R-D8'),
    ('ROOT:registration (R-C6)', 'R-C6'), ('S4-CAMPAIGN FINAL_SUMMARY', 'RUN:S4-CAMPAIGN'),
]
INV_UNLOCK_TO_ITEM = [
    ('CFG:config.anchor', 'R-D4'), ('DOC:deciding_test', 'R-D4'), ('DOC:capability_evidence', 'R-D3'),
]
INV_V007_TO_ITEM = {'V7-READ': 'V007:V7-READ', 'V7-BLOCK': 'V007:V7-BLOCK', 'V7-DRIVER': 'V007:V7-DRIVER'}
DP_GATE_TO_ITEM = {'numerics_verdict': 'V007:numerics_verdict', 'numerics_verdict / seal allowlist': 'R-A2',
                   'adoption_regeneration': 'R-A4+R-A5', 'deciding_test': 'R-D4', 'driver_capability': 'R-D3',
                   'certificate_policy': 'R-C1', 'u_i_carrier': 'R-C2'}
DP_CODE_TO_ITEM = {
    'PENDING_UV_TAIL_CERTIFICATE': 'V007:V7-BLOCK',
    'CERTIFICATE_POLICY_PENDING': 'R-C1',
    'CONFIG_ANCHOR_TAIL_REANCHOR_PENDING': 'R-D4',
    'WORKERS_8_SPEC_NOT_REGISTERED': 'R-D2',
    'CAPABILITY_EVIDENCE_PENDING': 'R-D3',
    'SENSITIVITY_DECIDING_III_REQUIRED': 'R-B2+R-C5+R-D5',
    'COMPARATOR_A68_SUCCESSOR_REQUIRED': 'R-B2',
}
# Why a blocker can appear in one list and not the other (each is checked against the bytes cited).
EXPLAIN = {
    ('inv_only', 'R-D8'): 'Resource caps are root rulings passed to the monitor as argv (root_monitor_c2v001 --wall-cap-s/--rss-cap-bytes/--output-cap-bytes; launcher v007 monitor_argv L63-64). A driver dry plan has no cap check, so the dry-plan lane cannot see this item. Not a disagreement.',
    ('inv_only', 'R-D5'): 'Caps and launch timing of the tail-OFF pair runs are root rulings outside the driver plan (as R-D8). The dry plans report the specs plan with zero blockers. Not a disagreement.',
    ('inv_only', 'R-C7'): 'A recommended pre-launch registration (A23 reading of the D runs), not a code gate: sensitivity_gate checks only the per-D deciding-(iii) entry. Not a disagreement; ROOT_ITEMS_FINAL keeps it as a recommendation.',
    ('inv_only', 'V007:V7-READ'): 'A57/0533: calibration consumes only a sealed ADOPT_TAIL. The driver dry plan has no verdict input; the dry plans carry this as the block fill (V7-BLOCK). Same dependency at a different layer.',
    ('inv_only', 'R-C1(conditional)'): 'Agrees with the dry plans: CERTIFICATE_POLICY_PENDING is downstream (not on the launch path) for TAIL_REANCHOR/WORKERS_8 because check_deciding ignores the slots (r9 review N-1); it becomes launch-path only if root takes the run slots from the registry (DU-1).',
    ('dp_only', 'R-C1'): 'Dry plans list CERTIFICATE_POLICY_PENDING as a downstream (campaign-level) item for this run; the inventory lists it under the campaign gate certificate_policy. Same item.',
    ('dp_only', 'R-D4'): 'Post-run registration (config.anchor / deciding rows). The inventory lists it under `unlocks`, not `depends_on`. Same item.',
    ('dp_only', 'R-D3'): 'Post-run registration of the capability evidence. The inventory lists it under `unlocks`. Same item.',
    ('inv_only', 'R-D4'): 'The deciding_test document (R-D4) needs both rows; the dry plans attach the post-run registration to the TAIL_REANCHOR record (CONFIG_ANCHOR_TAIL_REANCHOR_PENDING) and to the campaign gate deciding_test, not to the workers_8 record. Same item, different placement.',
    ('inv_only', 'R-B4'): 'Launch entry (v006r9 CLI exposes plan and wave only; wrapper L333-349). A plan-only dry run cannot see a missing run entry. Not a disagreement.',
    ('inv_only', 'R-D7'): 'Campaign scheduling (max_concurrent 1, per-wave cap) is an operating choice in config, not a plan blocker. Not a disagreement.',
    ('inv_only', 'V007:V7-DRIVER'): 'The driver slot binding (V007 seal driver == DRIVER_SHA) is an adoption-time check; the dry plans fix the driver to r5 and do not carry it as a per-spec blocker. Same dependency.',
    ('dp_only', 'R-B2'): 'Evidence-step blocker (compute_pair refuses on COMPARATOR_A68_REVIEWED False before any run read); the runs themselves plan with zero blockers. The inventory carries R-B2 in the DAG edge and ROOT_ITEMS, not in the run depends_on. Same item.',
}


def items_from_inv(r):
    deps, unl = set(), set()
    for s in r.get('depends_on') or []:
        hit = None
        for pat, it in INV_DEP_TO_ITEM:
            if s.startswith(pat) or s == pat:
                hit = it
                break
        deps.add(hit or ('UNMAPPED:' + s))
    for s in r.get('unlocks') or []:
        for pat, it in INV_UNLOCK_TO_ITEM:
            if pat in s:
                unl.add(it)
    for s in r.get('v007_inputs') or []:
        if s in INV_V007_TO_ITEM:
            deps.add(INV_V007_TO_ITEM[s])
    return deps, unl


def explode(itemset):
    out = set()
    for x in itemset:
        for y in x.split('+'):
            out.add(y)
    return out


def main(out_path):
    utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    pins = {}
    pin_ok = True
    for p, exp in EXPECTED.items():
        got = sha_file(p)
        pins[p] = {'sha256': got, 'expected': exp, 'equal': got == exp}
        pin_ok = pin_ok and got == exp
    inv = load(S4 + '/inventory/INVENTORY_C4V001.json')
    dp = load(S4 + '/dryplans/DRYPLANS_C4V002.json')
    dp1 = load(S4 + '/dryplans/DRYPLANS_C4V001.json')
    runs = {r['id']: r for r in inv['runs']}
    recs = {r['name'] + '@' + r['driver_key']: r for r in dp['records']}
    findings = []

    # --- V002 vs V001 of the dry-plan record: only the r6 runner pointer may differ
    d12 = sorted(set(k for k in set(dp) | set(dp1) if canon(dp.get(k)) != canon(dp1.get(k))))
    findings.append({'id': 'RC-00', 'check': 'DRYPLANS V002 vs V001 top-level keys that differ', 'result': d12,
                     'label': 'TESTED', 'reading': 'V002 supersedes V001 only where these keys differ'})

    # --- match runs by family and physical
    fam_map = {'TAIL_REANCHOR': 'TAIL_REANCHOR', 'HEADLINE_CAPABILITY': 'HEADLINE_CORNER',
               'SENSITIVITY_CORNER': 'SENS_CORNER', 'SENSITIVITY_DISTANCE_PLAN': 'SENS_DISTANCE'}
    pairs = []
    used = set()
    for rid, r in runs.items():
        fam = r.get('family')
        if fam in fam_map:
            cands = [k for k, x in recs.items() if x['family'] == fam_map[fam] and canon(x.get('physical')) == canon(r.get('physical'))
                     and k not in used]
            pairs.append((rid, cands))
            for c in cands:
                used.add(c)
    # deciding row, deciding (iii), campaign, contingents, post-S1
    pairs.append(('S4-W8', ['WORKERS_8_CANDIDATE_ANCHOR@r5']))
    used.add('WORKERS_8_CANDIDATE_ANCHOR@r5')
    diii = {'S4-DIII-LO-REF': 'DECIDING_III_LOW_V009GEO@v009geo', 'S4-DIII-LO-NEW': 'DECIDING_III_LOW_R5@r5',
            'S4-DIII-HI-REF': 'DECIDING_III_HIGH_V009GEO@v009geo', 'S4-DIII-HI-NEW': 'DECIDING_III_HIGH_R5@r5'}
    for a, b in diii.items():
        pairs.append((a, [b]))
        used.add(b)
    pairs.append(('S4-CAMPAIGN', ['CAMPAIGN_W1_SEED@r5']))
    used.add('CAMPAIGN_W1_SEED@r5')
    unmatched_dp = sorted(set(recs) - used)
    unmatched_inv = sorted(rid for rid, c in pairs if not c)

    rows = []
    for rid, cands in pairs:
        r = runs[rid]
        row = {'inventory_id': rid, 'dryplan_records': cands, 'checks': {}}
        if len(cands) != 1:
            row['checks']['one_to_one'] = False
            rows.append(row)
            continue
        x = recs[cands[0]]
        c = row['checks']
        c['one_to_one'] = True
        # driver
        inv_drv = (r.get('driver') or {}).get('sha256')
        c['driver_equal'] = inv_drv == x['driver']['sha256']
        # D and physical
        if r.get('physical') is not None:
            c['physical_equal_bitwise'] = canon(r['physical']) == canon(x.get('physical'))
        if r.get('D_Mpc') is not None:
            c['D_equal'] = r['D_Mpc'] == (x.get('physical') or {}).get('distance_Mpc')
        # point key
        pk_dp = (x.get('orchestrator_layer') or {}).get('certificate_point_key')
        if r.get('point_key_r5') is not None:
            c['point_key_equal'] = r['point_key_r5'] == pk_dp
        row['point_key_dp'] = pk_dp
        # spec bytes: re-hash the dry-plan spec file; compare with inventory fixed file / dry template by leaves
        sp = x['spec']['path']
        sh = sha_file(sp)
        c['dp_spec_rehash_equal'] = sh == x['spec']['sha256']
        row['dp_spec'] = {'path': sp, 'sha256': sh}
        tmpl = r.get('dry_template') or ((r.get('spec') or {}).get('prototype_dry_only'))
        if r.get('family') == 'DECIDING_III_TAIL_OFF':
            # the inventory records the spec file by name; resolve and hash it
            name = {'S4-DIII-LO-REF': 'DECIDING_III_LOW_V009_GEO_CALL.json', 'S4-DIII-LO-NEW': 'DECIDING_III_LOW_V010_R5_CALL.json',
                    'S4-DIII-HI-REF': 'DECIDING_III_HIGH_V009_GEO_CALL.json', 'S4-DIII-HI-NEW': 'DECIDING_III_HIGH_V010_R5_CALL.json'}[rid]
            fp = CX2 + '/v006r7/' + name
            fsh = sha_file(fp)
            row['inventory_fixed_spec'] = {'path': fp, 'sha256': fsh}
            c['diii_fixed_spec_sha_equal_dp'] = fsh == sh
        elif tmpl:
            tp = tmpl['path']
            tsh = sha_file(tp)
            row['inventory_template'] = {'path': tp, 'sha256': tsh, 'pinned': tmpl['sha256'], 'rehash_equal': tsh == tmpl['sha256']}
            c['template_rehash_equal'] = tsh == tmpl['sha256']
            diff = leaf_diff(load(tp), load(sp))
            row['template_vs_dp_spec_differing_leaves'] = diff
            c['template_vs_dp_spec_only_label'] = diff == ['/label']
        # blockers
        deps, unl = items_from_inv(r)
        inv_items = explode(deps) | explode(unl)
        dp_items = explode({DP_CODE_TO_ITEM.get(b['code'], 'UNMAPPED:' + b['code']) for b in x['blockers']})
        if rid == 'S4-CAMPAIGN':
            gl = {DP_GATE_TO_ITEM.get(g['gate'], 'UNMAPPED:' + g['gate']) for g in dp['campaign_level_gates']}
            dp_items |= explode(gl)
            row['dryplan_campaign_gates'] = sorted(g['gate'] for g in dp['campaign_level_gates'])
        row['inventory_items'] = sorted(inv_items)
        row['dryplan_items'] = sorted(dp_items)
        row['dryplan_launch_path_codes'] = sorted({b['code'] for b in x['blockers'] if b['on_launch_path']})
        row['common'] = sorted(inv_items & dp_items)
        diffs = []
        for it in sorted(inv_items - dp_items):
            key = ('inv_only', it)
            diffs.append({'side': 'inventory_only', 'item': it, 'explained': key in EXPLAIN, 'why': EXPLAIN.get(key)})
        for it in sorted(dp_items - inv_items):
            key = ('dp_only', it)
            diffs.append({'side': 'dryplans_only', 'item': it, 'explained': key in EXPLAIN, 'why': EXPLAIN.get(key)})
        row['blocker_differences'] = diffs
        rows.append(row)

    # contingent / unregistered rows have no dry plan by construction
    special = {
        'S4-DIII-LO-NEW-R6': 'dry plans: ALL_SPECS@r6 DEFERRED (r6 BUILD not landed); inventory: CONTINGENT, r6 sha UNAVAILABLE. Agree.',
        'S4-DIII-HI-NEW-R6': 'as S4-DIII-LO-NEW-R6. Agree.',
        'S4-POST-S1': 'inventory: UNREGISTERED, spec NOT_DEFINED; the dry plans cannot plan an undefined spec. Agree (root item R-C6).',
    }
    for rid, why in special.items():
        rows.append({'inventory_id': rid, 'dryplan_records': [], 'checks': {'no_dry_plan_expected': True}, 'why': why})

    # --- counts
    counts = {
        'inventory_records': len(inv['runs']),
        'inventory_direct_root_runs_listed': inv['run_counts'].get('direct_root_runs_listed'),
        'dryplan_records': len(dp['records']),
        'dryplan_distinct_spec_files': len({x['spec']['sha256'] for x in dp['records']}),
        'dryplan_tail_on_records': sum(1 for x in dp['records'] if x.get('tail_on')),
        'explanation': ('inventory 37 = 33 direct root runs (1 RA + 1 W8 + 9 CAP + 16 SENS corners + 2 SENS distance + 4 DIII) + 2 contingent r6 '
                        '(iii) runs + 1 campaign + 1 unregistered post-S1. Dry plans 34 = the same 33 direct runs (the 4 DIII as 2 files x 2 drivers) '
                        '+ 1 campaign wave-1 seed call; the campaign beyond wave 1 is engine-adaptive and cannot be planned before results; the 2 r6 '
                        'contingents are DEFERRED; post-S1 is not defined.'),
    }
    # distinct tail-ON certificate points (registry keys) in the dry plans
    keys = {}
    for k, x in recs.items():
        pk = (x.get('orchestrator_layer') or {}).get('certificate_point_key')
        if pk:
            keys.setdefault(pk, []).append(k)
    counts['dryplan_distinct_certificate_point_keys'] = len(keys)
    counts['point_keys'] = {pk: sorted(v) for pk, v in sorted(keys.items())}

    # --- named cross-checks
    rk = lambda n: (recs[n].get('orchestrator_layer') or {}).get('certificate_point_key')
    findings.append({'id': 'RC-01', 'check': 'TAIL_REANCHOR, HEADLINE_TRIAL and WORKERS_8 candidate share one certificate point key (anchor)',
                     'result': len({rk('TAIL_REANCHOR@r5'), rk('HEADLINE_TRIAL@r5'), rk('WORKERS_8_CANDIDATE_ANCHOR@r5')}) == 1,
                     'value': rk('TAIL_REANCHOR@r5'), 'inventory_S4-RA': runs['S4-RA'].get('point_key_r5'),
                     'inventory_S4-CAP-TRIAL': runs['S4-CAP-TRIAL'].get('point_key_r5'), 'label': 'TESTED'})
    seed = rk('CAMPAIGN_W1_SEED@r5')
    findings.append({'id': 'RC-02', 'check': 'campaign wave-1 seed point key differs from the anchor key (log/exp seed, R-D10)',
                     'result': seed != rk('TAIL_REANCHOR@r5'), 'seed_point_key': seed,
                     'reading': 'The pre-campaign registry needs this 28th point in addition to the inventory R-C1 count of 27 direct-run points.',
                     'label': 'TESTED'})
    inv_keys = {r['point_key_r5'] for r in inv['runs'] if r.get('point_key_r5')}
    findings.append({'id': 'RC-03', 'check': 'inventory distinct point keys vs dry-plan distinct point keys',
                     'inventory_distinct': len(inv_keys), 'dryplans_distinct': len(keys),
                     'dryplan_keys_not_in_inventory': sorted(set(keys) - inv_keys),
                     'inventory_keys_not_in_dryplans': sorted(inv_keys - set(keys)), 'label': 'TESTED'})
    findings.append({'id': 'RC-04', 'check': 'r6 status in both records', 'inventory_driver_rule': inv.get('driver_rule'),
                     'dryplans': dp.get('r6'), 'label': 'TESTED (as recorded by each lane)'})

    all_checks = [v for row in rows for k, v in row['checks'].items()]
    unexplained = [(row['inventory_id'], d['item'], d['side']) for row in rows for d in row.get('blocker_differences', []) if not d['explained']]
    out = {
        'schema': 'STEP4_RECONCILE_C4V002', 'utc': utc, 'lane': 'Claude4 helper (0587 launch_order)',
        'labels': 'TESTED = recomputed here from bytes; FORMAL = mapping tables / code reading cited in EXPLAIN',
        'inputs': pins, 'inputs_all_equal_expected': pin_ok,
        'pairs': rows, 'unmatched_dryplan_records': unmatched_dp, 'unmatched_inventory_runs': unmatched_inv,
        'counts': counts, 'findings': findings,
        'all_pair_checks_true': all(v is True for v in all_checks),
        'n_pair_checks': len(all_checks),
        'blocker_differences_unexplained': unexplained,
        'fence_blocked': F.BLOCKED,
        'producer': {'path': os.path.abspath(__file__), 'sha256': sha_file(os.path.abspath(__file__))},
    }
    with open(out_path, 'x') as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({'out': out_path, 'inputs_all_equal_expected': pin_ok, 'n_pair_checks': len(all_checks),
                      'all_pair_checks_true': out['all_pair_checks_true'], 'unmatched_dp': unmatched_dp,
                      'unmatched_inv': unmatched_inv, 'unexplained': unexplained, 'blocked': F.BLOCKED}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
