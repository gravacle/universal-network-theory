# c3v007 (c3v011, c3v027): c3v027 (manifest c3v002) maps to generator c3v014 and the dry-run env 064733Z.
# c3v006 (c3v010 FINAL, c3v026): c3v026 (registry V012) maps to generator c3v013 and the final dry-run env 060546Z (root's answered inputs).
# c3v005 (c3v010 FINAL): c3v024 maps to generator c3v013 and the final dry-run env.
# c3v004 (c3v010 near-final): c3v022 maps to generator c3v012 and the near-final dry-run env.
# c3v003 (c3v010 pre-stage): c3v021 maps to generator c3v011 (stand-ins S26 registry V009, S27 disclosures V002) and the r14 dry-run env.
# c3v002 (never-run c3v001 used the copy's own draft for S08): every draft fixture starts from the TARGET's draft.
# Claude3 (c3v009 pre-stage; lead dispatch after Codex1 0117/0118, lead post 0110): ONE MUST_FAIL test per && site of ROOT_SEAL_STEPS, run
# on a COPY of the PRODUCTION script (Codex1 0118 (i): a shell fixture is not enough), and the same fixtures on the c3v016 form.
#
# THE ONE VARIABLE: TARGET (argv[2], PATH=SHA) is the production script under test: ROOT_SEAL_STEPS_c3v019.sh now, c3v020 once v004 is
# wired. Everything else is derived from TARGET's own bytes: its sites (located by statement text, not line numbers), its HELPER /
# BINDER / DRAFT / PREREG_TOR / R6_SELECTED pins, the dry-run generator that matches it (c3v009 while P13 is PENDING; c3v010, from
# c3v009_prestage/tools, once it is wired; c3v008 for the c3v016 contrast) and the root-input environment of the matching dry run.
#
# Each copy = the production script + the published dry-run scratch substitutions (the generator's S01-S18, S15, S16/S16b and, for
# c3v019 only, S24/S25; every output in a fresh scratch folder, never a real seal path) + EXACTLY ONE fixture edit, in which only the
# FIRST operand's value of the site under test is wrong + one observation line right after the site statement
# (SITE_FIXTURE_MARKER on stderr: printed only if the script went past the check) + the step calls cut after the NEXT step (step 1
# for step-0 sites, step 3a for step-3 sites), so that "a later step was reached" is observable and nothing beyond 3a can ever run
# (step 9 and the C5H run are unreachable). Each copy and its diff against the production script are kept.
#
# The verdict for TARGET at a defect site: exit != 0, the site's own "REFUSE: ..." line on stderr, STOPPED at the site's step, no
# marker, and the next step's banner absent. For the c3v016 contrast: "defect reproduced" when the marker shows the script went past
# the check. Site S02 (c3v016 L325) is a CONTROL: it had its || REFUSE fallback in c3v016 already, so it must refuse in both.
# Nothing outside OUTDIR is written; no launch; no protected path is read (fixtures are synthetic copies in OUTDIR).
# usage: python3 -I -B e1_sites_mustfail_c3v001.py OUTDIR TARGET=SHA [CONTRAST=SHA]
import hashlib, json, os, re, subprocess, sys
OUT = sys.argv[1]
TARGET, TARGET_SHA = sys.argv[2].rsplit('=', 1)
C3 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3'; W = C3 + '/c3v009_prestage'
CONTRAST, CONTRAST_SHA = (sys.argv[3].rsplit('=', 1) if len(sys.argv) > 3 else
                          (C3 + '/ROOT_SEAL_STEPS_c3v016.sh', 'dcdb746c76546169bc0b4702c832265b59115c552480f248bdd5c3f354f0a6e8'))
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
D10, D11 = C3 + '/dry_run_20261019T010953Z', C3 + '/dry_run_20261019T013957Z'
SHIM, SHIMS = C3 + '/tools/dryrun_tool_shim_c3sa_c3v007.py', 'df19ac11401d76593f3b7a03474a31c955a77ec5585475e2a5bc9588027fd135'
GENS = {'c3v008': (C3 + '/tools/make_dry_run_c3sa_c3v008.py', '0c2c0201741ce0f8e9da3fa9bd5fdab4cea0a656d9111569b8194233730350ee', D10),
        'c3v009': (C3 + '/tools/make_dry_run_c3sa_c3v009.py', '78c900ffcd984c1bc35b53c823a16b01728dcee56cfe5dbc12d48614f9681573', D11),
        'c3v010': (W + '/tools/make_dry_run_c3sa_c3v010.py', 'ab01df672987408cb18954db79698da8051097d1fd6d8ddcc66522e028fedf4c', D11),
        'c3v014f': (C3 + '/c3v010_prestage/tools/make_dry_run_c3sa_c3v014.py', 'b49181e2a57367d5fcf2c2bfb4092e9e17d12207c5b1290ce9af81a0adad815c', C3 + '/dry_run_20261019T064733Z'),
        'c3v013f': (C3 + '/c3v010_prestage/tools/make_dry_run_c3sa_c3v013.py', '379afda7382d5ac95aaa11dc9a5b646303d86e22f199ab8009d358d8f6c74c8b', C3 + '/dry_run_20261019T060546Z'),
        'c3v013': (C3 + '/c3v010_prestage/tools/make_dry_run_c3sa_c3v013.py', '379afda7382d5ac95aaa11dc9a5b646303d86e22f199ab8009d358d8f6c74c8b', C3 + '/dry_run_20261019T044217Z'),
        'c3v012': (C3 + '/c3v010_prestage/tools/make_dry_run_c3sa_c3v012.py', 'fadec8e4fec1e6c071a45acdfff2028807b859583a70b1e2f9eed355fece682c', C3 + '/c3v010_prestage/dry_run_20261019T042057Z'),
        'c3v011': (C3 + '/c3v010_prestage/tools/make_dry_run_c3sa_c3v011.py', 'a48b3602c5c36634c41abc622c45485fa1c866c244fdd97a5f5fd06d7978d543', C3 + '/c3v010_prestage/dry_run_20261019T040145Z')}
BINDER_REAL_SHA = 'f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca'
ENV0 = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
        'VECLIB_MAXIMUM_THREADS': '1', 'LANG': 'en_US.UTF-8', 'HOME': '/Users/bgm'}
REAL_OUTPUTS = [CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', CTRL + '/V007_SEAL_ASSEMBLY',
                A + '/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V011_CX3V001_BOUND_R5_V007_SEAL.json',
                A + '/v007_launch_packet_cx1/P128/LAUNCH_COMMAND_V011_CX3V001_BOUND_R5_V007_SEAL.txt',
                A + '/v007_launch_packet_cx1/ROOT_SEAL_ADMISSION_V001.json', '/Users/bgm/Research/UNT_INTERNAL_RUNS']
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def rd(p, h):
    b = open(p, 'rb').read(); assert hashlib.sha256(b).hexdigest() == h, p; return b
def wx(p, data):
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return sha(p)
assert sha(SHIM) == SHIMS
TT, CT = rd(TARGET, TARGET_SHA).decode(), rd(CONTRAST, CONTRAST_SHA).decode()
def gen_for(text):
    if 'MANIFEST_GATES_ONLY_C3SA_c3v002.json' in text:   # c3v007: c3v027 (the gates-only manifest c3v002; dry-run env 064733Z)
        return 'c3v014f'
    if 'PRODUCER_REGISTRY_C3V012.json' in text:   # c3v006: c3v026 (no stand-ins; the final dry-run env 060546Z, root's answered inputs)
        return 'c3v013f'
    if 'PRODUCER_REGISTRY_C3V011.json' in text:   # c3v005: c3v024 (no stand-ins; the final dry-run env with root's real inputs)
        return 'c3v013'
    if 'PENDING_B7_SUCCESSOR_CUSTODY_RECORD' in text:   # c3v004: c3v022 (only the custody stand-in S29; the near-final dry-run env)
        return 'c3v012'
    if 'PENDING_PRODUCER_REGISTRY_V010' in text:     # c3v003: c3v021 (stand-ins S26/S27; the r14 dry run env)
        return 'c3v011'
    if 'PENDING_SEAL_TOOLS_V004_SELECTED_FILE' in text:
        return 'c3v009'
    if 'DISCLOSURES=' not in text:
        return 'c3v008'
    return 'c3v010'
for k in (gen_for(TT), gen_for(CT)):
    assert sha(GENS[k][0]) == GENS[k][1], k
pre_absent = {p: not os.path.lexists(p) for p in REAL_OUTPUTS}
assert all(pre_absent.values()), pre_absent
os.mkdir(OUT); FX = OUT + '/fixtures'; os.mkdir(FX)
def pinval(text, var):
    m = re.search(r'^%s="([^"]*)";\s*%s_SHA="([0-9a-f]{64})"' % (var, var), text, re.M)
    assert m, var
    return m.group(1).replace('$A', A).replace('$C3', C3).replace('$PKT', A + '/v007_launch_packet_cx1'), m.group(2), m.group(0)
# ------------------------------------------------------------------------------------------------------------------- the sites
# sig = the site statement's first line (stripped), located by text; c3v016_line = the line the lead's 0109 and Codex1 0118 cite.
SITES = [
 ('S01', 298, '0', 'the HELPER and RUNNER sha check (HELPER is the first operand)', '[ "$(sha_of "$HELPER")" = "$HELPER_SHA" ] && [ "$(sha_of "$RUNNER")" = "$RUNNER_SHA" ]', 'helper', 'the helper or runner bytes differ from their pins', 'E1-1'),
 ('S02', 325, '0', 'CONTROL: the text of record binds the case block (had its || REFUSE fallback in c3v016 already)', '[ "$(jf "$PREREG_TOR" binding_inputs.case_block.path)" = "$CASE_BLOCK" ] && [ "$(jf "$PREREG_TOR" binding_inputs.case_block.sha256)" = "$CASE_BLOCK_SHA" ]', 'tor_case_block', 'the text of record does not bind the case block', ''),
 ('S03', 355, '0', 'the draft driver (driver.path first)', '[ "$(jf "$DRAFT" driver.path)" = "$DRIVER" ] && [ "$(jf "$DRAFT" driver.sha256)" = "$DRIVER_SHA" ]', ('draft', ('driver', 'path')), "the slot draft's driver is not DRIVER", 'E1-2'),
 ('S04', 356, '0', 'the draft producer registry (path first)', '[ "$(jf "$DRAFT" producer_registry.path)" = "$REGISTRY" ] && [ "$(jf "$DRAFT" producer_registry.sha256)" = "$REGISTRY_SHA" ]', ('draft', ('producer_registry', 'path')), "the slot draft's producer_registry is not REGISTRY", ''),
 ('S05', 357, '0', 'the draft BUILD_V007 pin (path first)', '[ "$(jf "$DRAFT" launch_packet.build.path)" = "$BUILD" ] && [ "$(jf "$DRAFT" launch_packet.build.sha256)" = "$BUILD_SHA" ]', ('draft', ('launch_packet', 'build', 'path')), "the slot draft's launch_packet.build is not BUILD", ''),
 ('S06', 358, '0', 'the draft admission entry (launcher.path first of four)', '[ "$(jf "$DRAFT" admission_entry.launcher.path)" = "$LAUNCHER" ] && [ "$(jf "$DRAFT" admission_entry.launcher.sha256)" = "$LAUNCHER_SHA" ]', ('draft', ('admission_entry', 'launcher', 'path')), "the slot draft's admission_entry is not LAUNCHER and GUARD", 'E1-3'),
 ('S07', 360, '0', 'the draft identity gate records (Z2 sha first of three)', '[ "$(jf "$DRAFT" identity_gate_records.Z2.sha256)" = "$IDREC_Z2_SHA" ] && [ "$(jf "$DRAFT" identity_gate_records.Z2_OFF_RO1.sha256)" = "$IDREC_Z2OFF_SHA" ]', ('draft', ('identity_gate_records', 'Z2', 'sha256')), "the slot draft's identity_gate_records are not", 'E1-4'),
 ('S08', 363, '0', 'the draft documented output paths, attempt 1 (frozen_addendum.path first of four; DRAFT_PATHS_MUST_MATCH=1 as in production)', '[ "$(jf "$DRAFT" frozen_addendum.path)" = "$FROZEN" ] && [ "$(jf "$DRAFT" driver_build_record.path)" = "$DRIVER_BUILD_RECORD" ]', 'draft_paths', "the slot draft's documented output paths are not this script's", ''),
 ('S09', 454, '3', "the binder's plan and command paths (plan.path first)", '[ "$(jf "$LOGS/STEP_03_BINDER.json" plan.path)" = "$BOUND_PLAN" ] && [ "$(jf "$LOGS/STEP_03_BINDER.json" command.path)" = "$BOUND_COMMAND" ]', ('binder', 'plan'), "the binder's plan or command path is not BOUND_PLAN / BOUND_COMMAND", ''),
 ('S10', 455, '3', "the binder's driver and frozen addendum paths (driver.path first)", '[ "$(jf "$LOGS/STEP_03_BINDER.json" driver.path)" = "$DRIVER" ] && [ "$(jf "$LOGS/STEP_03_BINDER.json" frozen_addendum.path)" = "$FROZEN" ]', ('binder', 'driver'), "the binder's driver or frozen addendum path is not DRIVER / FROZEN", ''),
 ('S11', None, '0', 'A111 (c3v017+, fallback from birth): the draft driver_check_record (path first)', '[ "$(jf "$DRAFT" driver_check_record.path)" = "$DRIVER_CHECK_RECORD" ] && [ "$(jf "$DRAFT" driver_check_record.sha256)" = "$DRIVER_CHECK_RECORD_SHA" ]', ('draft', ('driver_check_record', 'path')), "the slot draft's driver_check_record is not the A111 record", 'disclosures-suite S-8 (sha form)'),
 ('S12', None, '0', 'A111 (c3v017+, fallback from birth): the draft EPS_NGC pin (one test in the C04_EXCLUSIONS loop; path form)', '[ "$(jf "$DRAFT" "${x%%=*}.path")=$(jf "$DRAFT" "${x%%=*}.sha256")" = "${x#*=}" ]', ('draft', ('certificates', 'EPS_NGC', 'path')), "the slot draft's certificates.EPS_NGC is not the A111 record", 'disclosures-suite S-9 (sha form)'),
]
NEXT_BANNER = {'0': 'STEP 1 freeze', '3': 'STEP 3a fill'}
KEEP = {'0': ['step0_preflight', 'step1_freeze'], '3': ['step0_preflight', 'step1_freeze', 'step2_tool1', 'step2a_driver_build', 'step3_bind', 'step3a_fill']}
STOPPED_AT = {'0': 'STOPPED at step 0 ', '3': 'STOPPED at step 3 '}
def site_index(lines, sig):
    hits = [i for i, ln in enumerate(lines) if ln.strip().startswith(sig)]
    return hits
def run_env(run_file, v):
    env = dict(ENV0)
    for ln in open(run_file).read().splitlines():
        m = re.match(r'export (\w+)=("([^"]*)"|(\S+))', ln)
        if m:
            env[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(4)
    env['UNT_SEAL_DISPOSITIONS_PATH'] = v + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json'
    return env
def mkpass(v, script, script_sha, gk):
    gen, gens, dry = GENS[gk]
    for d in ('', '/scratch_ctrl', '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS', '/scratch_pkt', '/scratch_pkt/P128', '/scratch_internal'):
        os.mkdir(v + d)
    wx(v + '/scratch_pkt/bind_sealed_launch_plan_cx1v001.py', rd(dry + '/passA/scratch_pkt/bind_sealed_launch_plan_cx1v001.py', BINDER_REAL_SHA))
    wx(v + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json',
       open(dry + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json', 'rb').read())
    man = dry + '/fixtures/MANIFEST_GATES_ONLY_STANDIN.json'
    r = subprocess.run([PY, '-I', '-B', gen, script, script_sha, v, 'A', dry + '/fixtures', man, sha(man), SHIM], capture_output=True, text=True, cwd='/', env=ENV0)
    assert r.returncode == 0, r.stderr[-600:]
    return open(v + '/ROOT_SEAL_STEPS_DRYRUN_A.sh').read(), dry + '/passA/RUN_A.sh'
def fixture_edit(kind, sid, s, v, base_text):
    """returns (edited copy text, description of the one fixture edit, fixture files)"""
    files = {}
    if kind == 'helper':
        hp, hs, line = pinval(s, 'HELPER')
        fp = v + '/FIXTURE_HELPER_%s.py' % sid
        files['fixture_helper'] = wx(fp, rd(hp, hs) + b'\n# SITE FIXTURE %s (Claude3 c3v009 pre-stage): a byte-modified copy of the pinned helper; its sha is NOT HELPER_SHA. NOT a seal tool.\n' % sid.encode())
        new = line.replace('HELPER="%s"' % re.search(r'^HELPER="([^"]*)"', line).group(1), 'HELPER="%s"' % fp, 1)
        return s.replace(line, new, 1), 'HELPER -> a byte-modified copy of the pinned helper (HELPER_SHA unchanged)', files
    if kind == 'tor_case_block':
        tp, ts, tline = pinval(s, 'PREREG_TOR'); sp, ss, sline = pinval(s, 'R6_SELECTED')
        F = v + '/fixture_r6'; os.mkdir(F); os.mkdir(F + '/addendum_read')
        tor = json.loads(rd(tp, ts)); sel = json.loads(rd(sp, ss))
        bc_old = tor['entries_after_A81']['addendum_read']['byte_copy'].split(' ')[0]
        bc_new = F + '/addendum_read/' + os.path.basename(bc_old)
        files['addendum_copy'] = wx(bc_new, open(bc_old, 'rb').read())
        tor['entries_after_A81']['addendum_read']['byte_copy'] = bc_new
        tor['binding_inputs']['case_block']['path'] = tor['binding_inputs']['case_block']['path'] + '.SITE_FIXTURE_NOT_IT'   # the FIRST operand only
        tf = F + '/' + os.path.basename(tp).replace('.json', '_SITE_FIXTURE_S02.json'); files['fixture_tor'] = wx(tf, json.dumps(tor, indent=1, ensure_ascii=False) + '\n')
        sel['files']['text_of_record'] = {'path': tf, 'sha256': files['fixture_tor']}
        sel['files']['addendum_at_text_of_record'] = {'path': bc_new, 'sha256': files['addendum_copy']}
        sf = F + '/SELECTED_R6_SITE_FIXTURE_S02.json'; files['fixture_selected_r6'] = wx(sf, json.dumps(sel, indent=1, ensure_ascii=False) + '\n')
        s = s.replace(tline, 'PREREG_TOR="%s"; PREREG_TOR_SHA="%s"' % (tf, files['fixture_tor']), 1)
        s = s.replace(sline, 'R6_SELECTED="%s"; R6_SELECTED_SHA="%s"' % (sf, files['fixture_selected_r6']), 1)
        return s, ('PREREG_TOR / R6_SELECTED -> a synthetic r6 copy whose binding_inputs.case_block.path is wrong (sha right), with its addendum copy '
                   'inside its own folder, and a synthetic SELECTED naming it'), files
    if kind[0] == 'draft' or kind == 'draft_paths':
        dp, ds, dline = pinval(s, 'DRAFT')
        d = json.loads(base_text)   # c3v002: the SAME base draft (the target's) for every draft site, target and contrast alike
        if kind == 'draft_paths':
            vv = lambda name: re.search(r'^%s="([^"]*)"' % name, s, re.M).group(1)
            sd = vv('SEAL_DIR').replace('$SFX', '')
            d['frozen_addendum']['path'] = vv('FROZEN') + '.SITE_FIXTURE_NOT_IT'                                 # the FIRST operand only
            d['driver_build_record']['path'] = sd + '/DRIVER_BUILD_RECORD_R5_V007_SEAL.json'
            d['launch_packet']['bound_plan']['path'] = vv('BOUND_PLAN').replace('$SFX', '')
            d['launch_packet']['bound_command']['path'] = vv('BOUND_COMMAND').replace('$SFX', '')
            s = s.replace('DRAFT_PATHS_MUST_MATCH=0 ', 'DRAFT_PATHS_MUST_MATCH=1 ', 1)
            what = ('DRAFT_PATHS_MUST_MATCH back to 1 (as in production); DRAFT -> a draft documenting this copy\'s scratch DBR / bound plan / bound '
                    'command paths and a wrong frozen_addendum.path')
        else:
            o = d
            for k in kind[1][:-1]:
                o = o[k]
            o[kind[1][-1]] = ('f' * 64) if kind[1][-1] == 'sha256' else o[kind[1][-1]] + '.SITE_FIXTURE_NOT_IT'
            what = 'DRAFT -> the target\'s draft with only %s wrong' % '.'.join(kind[1])
        fp = v + '/FIXTURE_DRAFT_%s.json' % sid; files['fixture_draft'] = wx(fp, json.dumps(d, indent=1, ensure_ascii=False) + '\n')
        return s.replace(dline, 'DRAFT="%s";              DRAFT_SHA="%s"' % (fp, files['fixture_draft']), 1), what, files
    if kind[0] == 'binder':
        bp, bs, bline = pinval(s, 'BINDER')
        key = kind[1]
        fb = v + '/scratch_pkt/bind_sealed_launch_plan_SITE_FIXTURE_%s.py' % sid
        files['fixture_binder'] = wx(fb, rd(bp, BINDER_REAL_SHA) + ('''
# ---- SITE FIXTURE %s (Claude3 c3v009 pre-stage, MUST_FAIL only; NOT the binder of record): the real bind() runs and writes the real
# outputs; only the '%s' path in the JSON it returns (what ROOT_SEAL_STEPS reads back) is changed, so only the FIRST operand of one
# step-3 check is wrong.
_real_bind = bind
def bind(*a, **k):
    r = _real_bind(*a, **k)
    r['%s'] = dict(r['%s'], path=r['%s']['path'] + '.SITE_FIXTURE_NOT_IT')
    return r
''' % (sid, key, key, key, key)).encode())
        return s.replace(bline, 'BINDER="%s";      BINDER_SHA="%s"' % (fb, files['fixture_binder']), 1), \
            "BINDER -> the real binder plus a wrapper that changes only the %s path it reports" % key, files
    raise ValueError(kind)
def build_copy(sid, step, sig, kind, script, script_sha, label, base_draft_text):
    v = OUT + '/%s_%s' % (sid, label)
    gk = gen_for(open(script).read())
    s, run_file = mkpass(v, script, script_sha, gk)
    lines = s.split('\n')
    hits = site_index(lines, sig)
    if len(hits) != 1:
        return None, {'site_found': False, 'hits': len(hits)}
    i = hits[0]; j = i
    while lines[j].rstrip().endswith('\\'):
        j += 1
    ind = re.match(r'\s*', lines[i]).group(0)
    lines.insert(j + 1, ind + 'echo "SITE_FIXTURE_MARKER %s: the script went past this check" >&2' % sid)
    s = '\n'.join(lines)
    s, what, files = fixture_edit(kind, sid, s, v, base_draft_text)
    k = s.index('step0_preflight\nstep1_freeze\n')
    s = s[:k] + '\n'.join(KEEP[step]) + '\necho "SITE_COPY_END: the kept steps all ran (%s)"\n' % ' '.join(KEEP[step])
    cp = v + '/SITE_COPY_%s_%s.sh' % (sid, label)
    csha = wx(cp, s)
    dif = subprocess.run(['/usr/bin/diff', '-u', script, cp], capture_output=True, text=True).stdout
    dsha = wx(v + '/SITE_COPY_%s_%s.diff' % (sid, label), dif)
    return (cp, run_file, v), {'site_found': True, 'site_line_in_script': i + 1, 'generator': gk, 'fixture_edit': what, 'fixture_files': files,
                                'copy': {'path': cp, 'sha256': csha}, 'diff_vs_production': {'path': v + '/SITE_COPY_%s_%s.diff' % (sid, label), 'sha256': dsha,
                                'changed_lines': sum(1 for ln in dif.splitlines() if ln[:1] in '+-' and ln[:3] not in ('+++', '---'))}}
def run_copy(cp, run_file, v, sid, step):
    r = subprocess.run(['/bin/bash', cp], capture_output=True, text=True, cwd='/', env=run_env(run_file, v))
    refuse = next((ln for ln in r.stderr.splitlines() if ln.startswith('REFUSE:')), '')
    if not refuse:
        for ln in r.stderr.splitlines():
            if '"verdict": "REFUSE"' in ln:
                try:
                    refuse = 'HELPER REFUSE: ' + json.loads(ln).get('code', '')[:200]
                except Exception:
                    refuse = ln[:200]
                break
    m = re.search(r'STOPPED at step (\S+) ', r.stderr)
    with open(v + '/RUN_%s.stdout.txt' % os.path.basename(cp)[:-3], 'x') as f:
        f.write(r.stdout)
    with open(v + '/RUN_%s.stderr.txt' % os.path.basename(cp)[:-3], 'x') as f:
        f.write(r.stderr)
    return {'exit': r.returncode, 'refuse_line': refuse[:300], 'stopped_at_step': m.group(1) if m else None,
            'marker_seen': ('SITE_FIXTURE_MARKER %s:' % sid) in r.stderr, 'next_step_banner_seen': NEXT_BANNER[step] in r.stdout,
            'copy_end_reached': 'SITE_COPY_END' in r.stdout}
RES = []
base_draft_path, base_draft_sha, _ = pinval(TT, 'DRAFT')
base_draft_text = rd(base_draft_path, base_draft_sha).decode()
for sid, line16, step, what, sig, kind, expect, e1 in SITES:
    row = {'site': sid, 'c3v016_line': line16, 'step': step, 'what': what, 'expected_refuse': expect, 'covered_before_by': e1, 'is_control': sid == 'S02'}
    tgt, info = build_copy(sid, step, sig, kind, TARGET, TARGET_SHA, 'target', base_draft_text)
    row['target'] = info
    if tgt:
        res = run_copy(*tgt, sid, step)
        row['target'].update(res)
        row['target']['ok'] = (res['exit'] != 0 and ('REFUSE: ' + expect) in res['refuse_line'] and res['stopped_at_step'] == step
                               and not res['marker_seen'] and not res['next_step_banner_seen'] and not res['copy_end_reached'])
    else:
        row['target']['ok'] = False
    if line16 is not None:
        con, cinfo = build_copy(sid, step, sig, kind, CONTRAST, CONTRAST_SHA, 'c3v016', base_draft_text)
        row['contrast_c3v016'] = cinfo
        if con:
            cres = run_copy(*con, sid, step)
            row['contrast_c3v016'].update(cres)
            if sid == 'S02':
                row['contrast_c3v016']['no_defect_at_this_site'] = (not cres['marker_seen'] and ('REFUSE: ' + expect) in cres['refuse_line'] and cres['exit'] != 0)
            else:
                row['contrast_c3v016']['defect_reproduced'] = cres['marker_seen']
    RES.append(row)
    t = row['target']
    c = row.get('contrast_c3v016', {})
    print('%s L%s step %s | target ok=%s exit=%s stopped=%s marker=%s next=%s | %s | c3v016: marker=%s next=%s exit=%s %s' % (
        sid, line16, step, t.get('ok'), t.get('exit'), t.get('stopped_at_step'), t.get('marker_seen'), t.get('next_step_banner_seen'), t.get('refuse_line', '')[:90],
        c.get('marker_seen'), c.get('next_step_banner_seen'), c.get('exit'), (c.get('refuse_line') or '')[:70]), flush=True)
post_absent = {p: not os.path.lexists(p) for p in REAL_OUTPUTS}
defect_sites = [r for r in RES if r['c3v016_line'] is not None and not r['is_control']]
res = {'schema': 'C3SA_E1_SITES_MUSTFAIL_V001', 'target': {'path': TARGET, 'sha256': TARGET_SHA}, 'contrast': {'path': CONTRAST, 'sha256': CONTRAST_SHA},
       'generators': {k: {'path': v[0], 'sha256': v[1], 'env_dry_run': v[2]} for k, v in GENS.items()}, 'shim': {'path': SHIM, 'sha256': SHIMS},
       'real_outputs_absent_before': all(pre_absent.values()), 'real_outputs_absent_after': all(post_absent.values()), 'sites': RES,
       'n_sites': len(RES), 'n_target_ok': sum(bool(r['target'].get('ok')) for r in RES),
       'n_defect_sites': len(defect_sites), 'n_defect_reproduced_on_c3v016': sum(bool(r.get('contrast_c3v016', {}).get('defect_reproduced')) for r in defect_sites),
       'control_S02_no_defect_on_c3v016': bool(next(r for r in RES if r['site'] == 'S02').get('contrast_c3v016', {}).get('no_defect_at_this_site'))}
res['all_ok'] = (res['n_target_ok'] == res['n_sites'] and res['n_defect_reproduced_on_c3v016'] == res['n_defect_sites'] and res['control_S02_no_defect_on_c3v016']
                 and res['real_outputs_absent_after'])
with open(OUT + '/E1_SITES_RESULTS_C3SA.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
print('ALL_OK' if res['all_ok'] else 'SOME_FAIL', 'target %d/%d; defect reproduced on c3v016 %d/%d; control S02 no defect on c3v016: %s; real outputs absent: %s' % (
    res['n_target_ok'], res['n_sites'], res['n_defect_reproduced_on_c3v016'], res['n_defect_sites'], res['control_S02_no_defect_on_c3v016'], res['real_outputs_absent_after']))
