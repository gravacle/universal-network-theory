# Claude3 seal-assembly builder (FROM_CODEX/0646 + 0647): derive ROOT_SEAL_STEPS_c3v018.sh from ROOT_SEAL_STEPS_c3v017.sh (b6037eee,
# never run) by an explicit replacement set (each old string exactly once): SA-C3-E1, every check written as an && list now ends in an
# explicit refusal, because set -e enforces only the LAST operand of an && list. Writes the new script exclusively; prints its sha.
# usage: python3 -I -B make_root_script_c3v018.py SEAL_ASSEMBLY_C3_DIR
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v017.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'b6037eee3bc018542af8f07a355773682bba5694a503290397984466ac5b88a7'
s = src.decode('utf-8')
R = []
R.append(('header', '''# ROOT_SEAL_STEPS_c3v017.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY.''',
          '''# ROOT_SEAL_STEPS_c3v018.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY.'''))
R.append(('history', '''# c3v017 supersedes ROOT_SEAL_STEPS_c3v016.sh (dcdb746c, the c3v007 pre-stage tuple).''',
          '''# c3v018 supersedes ROOT_SEAL_STEPS_c3v017.sh (b6037eee; never run, never published). SA-C3-E1, found while building c3v017: under
#   set -e, bash 3.2 does NOT stop when a NON-FINAL operand of an && list fails; only the last operand is enforced (tested). Nine
#   checks in step 0 and step 3 had that form, the HELPER sha (the root of trust) among them. Each now ends in || { REFUSE; false; }.
#   Nothing else changes; c3v017's changes (below) all stand.
# c3v017 superseded ROOT_SEAL_STEPS_c3v016.sh (dcdb746c, the c3v007 pre-stage tuple).'''))
def fix(rid, old, msg):
    R.append((rid, old, old + ' \\\n    || { echo "REFUSE: %s" >&2; false; }' % msg))
R.append(('E1 helper and runner', '''  [ "$(sha_of "$HELPER")" = "$HELPER_SHA" ] && [ "$(sha_of "$RUNNER")" = "$RUNNER_SHA" ]   # these verify everything else from bytes''',
          '''  [ "$(sha_of "$HELPER")" = "$HELPER_SHA" ] && [ "$(sha_of "$RUNNER")" = "$RUNNER_SHA" ] \\
    || { echo "REFUSE: the helper or runner bytes differ from their pins (these two verify everything else from bytes)" >&2; false; }'''))
fix('E1 draft driver', '''  [ "$(jf "$DRAFT" driver.path)" = "$DRIVER" ] && [ "$(jf "$DRAFT" driver.sha256)" = "$DRIVER_SHA" ]''',
    "the slot draft's driver is not DRIVER (path and sha)")
fix('E1 draft registry', '''  [ "$(jf "$DRAFT" producer_registry.path)" = "$REGISTRY" ] && [ "$(jf "$DRAFT" producer_registry.sha256)" = "$REGISTRY_SHA" ]''',
    "the slot draft's producer_registry is not REGISTRY (path and sha)")
fix('E1 draft build', '''  [ "$(jf "$DRAFT" launch_packet.build.path)" = "$BUILD" ] && [ "$(jf "$DRAFT" launch_packet.build.sha256)" = "$BUILD_SHA" ]''',
    "the slot draft's launch_packet.build is not BUILD (path and sha)")
fix('E1 draft admission entry', '''  [ "$(jf "$DRAFT" admission_entry.launcher.path)" = "$LAUNCHER" ] && [ "$(jf "$DRAFT" admission_entry.launcher.sha256)" = "$LAUNCHER_SHA" ] \\
    && [ "$(jf "$DRAFT" admission_entry.guard.path)" = "$GUARD" ] && [ "$(jf "$DRAFT" admission_entry.guard.sha256)" = "$GUARD_SHA" ]''',
    "the slot draft's admission_entry is not LAUNCHER and GUARD (paths and shas)")
fix('E1 draft identity records', '''  [ "$(jf "$DRAFT" identity_gate_records.Z2.sha256)" = "$IDREC_Z2_SHA" ] && [ "$(jf "$DRAFT" identity_gate_records.Z2_OFF_RO1.sha256)" = "$IDREC_Z2OFF_SHA" ] \\
    && [ "$(jf "$DRAFT" identity_gate_records.B0prime_RERUN.sha256)" = "$IDREC_B0P_SHA" ]''',
    "the slot draft's identity_gate_records are not IDREC_Z2, IDREC_Z2OFF and IDREC_B0P")
fix('E1 draft documented outputs', '''    [ "$(jf "$DRAFT" frozen_addendum.path)" = "$FROZEN" ] && [ "$(jf "$DRAFT" driver_build_record.path)" = "$DRIVER_BUILD_RECORD" ] \\
      && [ "$(jf "$DRAFT" launch_packet.bound_plan.path)" = "$BOUND_PLAN" ] && [ "$(jf "$DRAFT" launch_packet.bound_command.path)" = "$BOUND_COMMAND" ]''',
    "the slot draft's documented output paths are not this script's (attempt 1)")
fix('E1 binder plan and command', '''  [ "$(jf "$LOGS/STEP_03_BINDER.json" plan.path)" = "$BOUND_PLAN" ] && [ "$(jf "$LOGS/STEP_03_BINDER.json" command.path)" = "$BOUND_COMMAND" ]''',
    "the binder's plan or command path is not BOUND_PLAN / BOUND_COMMAND")
fix('E1 binder driver and frozen', '''  [ "$(jf "$LOGS/STEP_03_BINDER.json" driver.path)" = "$DRIVER" ] && [ "$(jf "$LOGS/STEP_03_BINDER.json" frozen_addendum.path)" = "$FROZEN" ]''',
    "the binder's driver or frozen addendum path is not DRIVER / FROZEN")
out = s
for rid, o, n in R:
    assert out.count(o) == 1, (rid, out.count(o))
    out = out.replace(o, n)
# every remaining && statement in the step code is an if-condition or already ends in an explicit refusal
for i, ln in enumerate(out.split('\n')):
    t = ln.strip()
    if '&&' in t and not t.startswith('#'):
        nxt = out.split('\n')[i + 1].strip() if i + 1 < len(out.split('\n')) else ''
        ok = t.startswith('if ') or '|| {' in t or nxt.startswith('|| {') or (t.endswith('\\') and (nxt.startswith('&&') and (out.split('\n')[i + 2].strip().startswith('|| {'))))
        assert ok, (i + 1, t[:120])
dst = C3 + '/ROOT_SEAL_STEPS_c3v018.sh'
with open(dst, 'x') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v018.sh', hashlib.sha256(out.encode()).hexdigest(), 'replacements', len(R))
