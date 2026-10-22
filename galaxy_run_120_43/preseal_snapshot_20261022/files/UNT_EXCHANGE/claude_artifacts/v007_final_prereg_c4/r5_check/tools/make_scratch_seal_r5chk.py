# make_scratch_seal_r5chk.py -- builds the SCRATCH rehearsal inputs for the r12 rerun (r5_check helper, Claude4).
# usage: python3 -I -B make_scratch_seal_r5chk.py OUTDIR UTC
# Reads named files only; imports no program module; writes only under OUTDIR (inside r5_check/scratch), each by exclusive create.
# Nothing here is a seal input of record: every file is a SCRATCH stand-in, named *_R5CHK*, and lives in the r5_check folder.
import sys, os, json, hashlib, re, copy
OUT, UTC = sys.argv[1], sys.argv[2]
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_f(p): return sha_b(open(p, 'rb').read())
def pin(p, s=None):
    h = sha_f(p)
    if s is not None and h != s:
        raise SystemExit('PIN_MISMATCH %s %s != %s' % (p, h, s))
    return {'path': p, 'sha256': h}
def xwrite(name, data):
    p = os.path.join(OUT, name)
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return p
def jtext(o): return json.dumps(o, indent=1, ensure_ascii=False) + '\n'
os.mkdir(OUT)
R5 = A + '/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'; R5S = '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393'
R12 = A + '/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'; R12S = '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'
inputs = {'prereg_r5': pin(R5, R5S), 'compare_r12_reviewed': pin(R12, R12S)}
# 1. scratch frozen copy of the open V005 (a STAND-IN for root's FROZEN copy)
openv5 = CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
b = open(openv5, 'rb').read()
fz = xwrite('ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', b)
inputs['open_v005_at_copy'] = {'path': openv5, 'sha256': sha_b(b), 'bytes': len(b), 'utc': UTC}
frozen = pin(fz)
# 2. driver BUILD record: byte copy of the rehearsal draft (2a3e4308)
dsrc = A + '/seal_rehearsal_c4/run/scratch/rehearsal_b/DRIVER_BUILD_R5_REHEARSAL_DRAFT_C4V001.json'
db = open(dsrc, 'rb').read()
assert sha_b(db) == '2a3e4308d1738cf3f55bf88a1af9a4384dded7ed8ba7ae926d7510f8fb3f35da'
dbr = pin(xwrite('DRIVER_BUILD_R5_DRAFT_COPY_R5CHK.json', db))
inputs['driver_build_record_source'] = {'path': dsrc, 'sha256': sha_b(db)}
check = pin(A + '/tail_scheme_impl_c2/driver_r5/check/CHECK.md', '89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632')
assert json.loads(db)['check_record'] == check, 'draft check_record is not CHECK.md'
reg = pin(A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json', '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8')
# 3. placeholders for the bound plan and command (the binder runs only at the seal: GAP placeholders, like rehearsal Run B)
bp = pin(xwrite('GAP_PLACEHOLDER_BOUND_PLAN_R5CHK.json', jtext({'note': 'GAP placeholder (r5_check rehearsal): the build-only binder writes the bound plan at the seal (A81 RI-25)'})))
bc = pin(xwrite('GAP_PLACEHOLDER_BOUND_COMMAND_R5CHK.txt', '# GAP placeholder (r5_check rehearsal): the binder writes the bound command at the seal\n'))
PEND = 'PENDING_ROOT_AT_SEAL_ASSEMBLY'
r5 = json.load(open(R5))
nc = r5['seal_slots']['certificates']['named_candidates_verified_from_bytes']
certs = {'EPS': pin(nc['EPS']['path'], nc['EPS']['sha256']), 'LO': pin(nc['LO']['path'], nc['LO']['sha256']),
         'GQ': pin(nc['GQ']['path'], nc['GQ']['sha256']), 'DOUBLING': pin(nc['DOUBLING_merged']['path'], nc['DOUBLING_merged']['sha256']),
         'EPS_NGC': pin(nc['EPS_NGC_91']['path'], nc['EPS_NGC_91']['sha256']), 'LO_NGC': pin(nc['LO_NGC']['path'], nc['LO_NGC']['sha256']),
         'I1T_NGC': pin(nc['I1T_NGC']['path'], nc['I1T_NGC']['sha256'])}
ig = r5['seal_slots']['identity_gate_records']['named_candidates_verified_from_bytes']
idr = {k: pin(ig[k]['path'], ig[k]['sha256']) for k in ('Z2', 'Z2_OFF_RO1', 'B0prime_RERUN')}
drv = r5['seal_slots']['driver']['named_candidates_verified_from_bytes']['r5']
lpn = r5['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']['build']
icn = r5['seal_slots']['identity_comparator']['named_candidates_verified_from_bytes']['c2v007r2']
common = {'schema': 'UNT_V007_SEAL_SLOTS_C4V001', 'driver_branch': 'r5', 'ngc_gas_M_s': 96,
          'driver': pin(drv['path'], drv['sha256']), 'driver_check_record': check,
          'compare_reviewed_source': pin(R12, R12S), 'identity_comparator': pin(icn['path'], icn['sha256']),
          'identity_gate_records': idr, 'certificates': certs, 'producer_registry': reg, 'cache_directory_r6_only': 'NOT_APPLICABLE_R5'}
pend_pin = lambda path: {'path': path, 'sha256': PEND}
slotsA = dict(common, frozen_addendum=pend_pin(r5['seal_slots']['frozen_addendum']['path_to_be']),
              driver_build_record=pend_pin('PENDING_ROOT_DRIVER_BUILD_RECORD (created at seal assembly, checklist B2a)'),
              launch_packet={'build': pin(lpn['path'], lpn['sha256']), 'bound_plan': pend_pin('PENDING_ROOT_BOUND_PLAN (binder, B3)'),
                             'bound_command': pend_pin('PENDING_ROOT_BOUND_COMMAND (binder, B3)')})
slotsB = dict(common, frozen_addendum=frozen, driver_build_record=dbr,
              launch_packet={'build': pin(lpn['path'], lpn['sha256']), 'bound_plan': bp, 'bound_command': bc})
def sealed_prereg(slots):
    d = copy.deepcopy(r5)
    m = {'frozen_addendum': 'frozen_addendum', 'driver': 'driver', 'compare': 'compare_reviewed_source', 'identity_comparator': 'identity_comparator',
         'identity_gate_records': 'identity_gate_records', 'launch_packet': 'launch_packet', 'certificates': 'certificates',
         'producer_registry': 'producer_registry', 'cache_directory_r6_only': 'cache_directory_r6_only'}
    for pk, sk in m.items():
        d['seal_slots'][pk]['value'] = slots[sk]
    return d
out = {'schema': 'R5CHK_SCRATCH_SEAL_INPUTS_V001', 'utc': UTC, 'label': 'SCRATCH stand-ins for a seal rehearsal on r5 + r12; not seal inputs of record',
       'inputs': inputs, 'files': {}}
for tag, slots in (('A', slotsA), ('B', slotsB)):
    sp = xwrite('SLOTS_%s_R5CHK.json' % tag, jtext(slots))
    pp = xwrite('KMAX_TAIL_PREREG_V007_SEALED_SCRATCH_%s_R5CHK.json' % tag, jtext(sealed_prereg(slots)))
    out['files']['slots_' + tag] = pin(sp); out['files']['sealed_prereg_' + tag] = pin(pp)
# 4. scratch sealed compares (r12 reviewed source with ONLY the five A82 pin lines set)
src = open(R12, 'rb').read().decode('utf-8')
lines = src.splitlines(keepends=True)
def sealed_compare(pins, name):
    seen = {}
    new = []
    for ln in lines:
        hit = None
        for k in pins:
            if ln.startswith(k + ' = None'):
                hit = k
        if hit and pins[hit] is not None:
            assert hit not in seen
            seen[hit] = 1
            new.append(ln.replace(hit + ' = None', hit + ' = ' + repr(pins[hit]), 1))
        else:
            new.append(ln)
    want = {k for k, v in pins.items() if v is not None}
    assert set(seen) == want, (seen, want)
    return pin(xwrite(name, ''.join(new)))
pinsP = {'V007_PREREG_SHA256': out['files']['sealed_prereg_A']['sha256'], 'PIN_ADDENDUM_V005': None, 'PIN_DRIVER_BUILD_RECORD': None,
         'PIN_V010_R5_CHECK': (check['path'], check['sha256']), 'PIN_PRODUCER_REGISTRY': (reg['path'], reg['sha256'])}
pinsB = {'V007_PREREG_SHA256': out['files']['sealed_prereg_B']['sha256'], 'PIN_ADDENDUM_V005': frozen['sha256'],
         'PIN_DRIVER_BUILD_RECORD': (dbr['path'], dbr['sha256']), 'PIN_V010_R5_CHECK': (check['path'], check['sha256']),
         'PIN_PRODUCER_REGISTRY': (reg['path'], reg['sha256'])}
out['files']['sealed_compare_P'] = sealed_compare(pinsP, 'kmax_tail_compare_c2v007_r12_SEALED_SCRATCH_P_R5CHK.py')
out['files']['sealed_compare_B'] = sealed_compare(pinsB, 'kmax_tail_compare_c2v007_r12_SEALED_SCRATCH_B_R5CHK.py')
out['pins_P'] = {k: v for k, v in pinsP.items()}; out['pins_B'] = {k: v for k, v in pinsB.items()}
# 5. gates-only manifest: the 13 registered pre-seal records of registry C3V009; NO case, identity-run or R-PAIR directory
rj = json.load(open(reg['path']))
br = json.load(open(A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009_BUILD_REPORT.json'))
gates = {}
for g, shas in sorted(rj['gate_records'].items()):
    if isinstance(shas, list) and shas:
        rec = br['records'][g]
        assert rec['sha256'] == shas[0] and sha_f(rec['path']) == shas[0], g
        gates[g] = rec['path']
man = {'schema': 'UNT_KMAX_TAIL_V007_MANIFEST_C2V002', 'cases': {}, 'identity_runs': {}, 'gates': gates, 'rpair': {},
       'note': 'r5_check rehearsal: only the 13 pre-seal gate records registered in C3V009 (each sha from bytes); no case, identity-run or R-PAIR directory is named, so no run directory is read.'}
out['files']['gates_only_manifest'] = pin(xwrite('GATES_ONLY_MANIFEST_R5CHK.json', jtext(man)))
out['manifest_gates'] = sorted(gates)
# 6. mutation preregs for the CLI case-block path (test mode): r5 with only binding_inputs.case_block changed
mut = A + '/v007_final_prereg_c4/r5_check/scratch/cb_mut'
cbd = json.load(open(A + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json'))
drop = copy.deepcopy(cbd); drop['cases'].pop('C4T-KHI')
dropp = xwrite('CB_DROP_C4T_KHI_R5CHK.json', jtext(drop))
def bind(name, path, sha):
    d = copy.deepcopy(r5); d['binding_inputs']['case_block'] = {'path': path, 'sha256': sha}
    return pin(xwrite(name, jtext(d)))
out['files']['prereg_bind_keymap_origsha'] = bind('PREREG_R5_BIND_KEYMAP_ORIGSHA_R5CHK.json', mut + '/CB_KEYMAP_WELLFORMED_R5CHK.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
out['files']['prereg_bind_dupkey'] = bind('PREREG_R5_BIND_DUPKEY_R5CHK.json', mut + '/CB_DUP_CASE_C4T_R5CHK.json', sha_f(mut + '/CB_DUP_CASE_C4T_R5CHK.json'))
out['files']['prereg_bind_dropcase'] = bind('PREREG_R5_BIND_DROPCASE_R5CHK.json', dropp, sha_f(dropp))
out['files']['prereg_bind_keymap_ownsha'] = bind('PREREG_R5_BIND_KEYMAP_OWNSHA_R5CHK.json', mut + '/CB_KEYMAP_WELLFORMED_R5CHK.json', sha_f(mut + '/CB_KEYMAP_WELLFORMED_R5CHK.json'))
xwrite('SCRATCH_INPUTS_R5CHK.json', jtext(out))
print(json.dumps({k: v['sha256'][:8] for k, v in out['files'].items()}))
print('open V005 at copy', inputs['open_v005_at_copy']['sha256'], 'manifest gates', out['manifest_gates'])
