"""write_i4_record_c3v003.py -- the I4 gate-record producer (Claude3 lane; root A114, FROM_CODEX/0651; RI-33; compare r14).
c3v003 = c3v002 (2a315da2) with exactly three fixes (Claude3 0142, Claude4 0147; root A115):
  D1 (A115 (b)).  Check C6 no longer calls the comparator's check_ro1_armed (052da0fe L1889), which also requires fired false and
     events [] (an RO1 firing identical in the honest N1 and N8 runs made the record FAIL and r14 read I4 FAIL).  Prereg r6 B0_RO1:
     RO1 firing in a T-run is recorded, not an invalidity; the A47 I4 condition is the V8c-F1 fix plus tail-ON serial == parallel
     bitwise.  C6 now checks per side only the RO1 rule, armed true, the exact registered key set (RO1_KEYS) and the side's own
     worker_sha256 / binding_sha256 pins (ro1_armed_side_pins).  fired / events are compared like every other field of the result
     records (result.json route_a_outcome and identity.route_a.outcome, the route-A attempt result), so a one-sided or a different
     firing still FAILs there.
  D2 (A115 (a)).  A file names the other run's root only where that root is followed by a path boundary: '/', the end of the
     file, a JSON / quote delimiter (double or single quote, comma, colon, closing bracket or brace, JSON whitespace) or a JSON
     escape that writes one (a backslash followed by a double quote, slash, n, r, t, b or f).  The comparator's substring scan
     (Store.hash_scan, L553-571) stays the first pass; a file it hits is re-read by the producer's boundary_scan (same bytes: its
     sha must equal the first sha).  Sibling roots where one name extends the other (.../C2T_RUN vs .../C2T_RUN_N1) no longer
     FAIL; a genuine reference still does.  The comparator file is not modified.
  D3 (A115 (a)).  Stage logs (stages/<stage>/stdout.txt and stderr.txt, driver run_stages L1844-1847) are logs, not results: a log
     whose bytes differ is compared as the SET OF DISTINCT LINES after the comparator's own Side normalization (run root and stage
     directories, file shas, ledger tokens); a distinct line present on one side only FAILs.  Python prints a warning once per
     process per site, so a serial run and a numerically identical parallel run may differ in line multiplicity and order only.
     Both files' shas (and line counts) are recorded in the record's comparison.stage_logs.
  Nothing else changes: the custody rule, the V8c-F1 check, the N1 spec pin 8ae6e2db, the driver pin, the g_I4 record fields and
  every refusal keep their behaviour.

c3v002 = c3v001 (4d6263f6) with one change (A115 (a): an honest run under a symlinked ancestor, e.g. CLAUDE2/runs_ext -> External1,
was refused): run, receipt and output paths are resolved component by component as the comparator's guarded_resolve does
(every partial path and every link target checked by name BEFORE it is looked up, at most 40 hops), symlinks are refused only
INSIDE the run trees, and the run-root spelling used for normalization is the run's own (finish.json result_path, driver cmd_run
L3594), which must resolve to the given directory.  Nothing else changes.

WHAT IT WRITES.  One gate record of the FIELDS shape compare r14 g_I4 reads (schema UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002,
gate I4, producer {path, sha256} = this file from bytes): tail, driver_sha256, serial_result_sha256, parallel_result_sha256,
v8c_f1_fix_confirmed, bitwise_equal, differences_outside_custody, verdict; plus detail blocks g_I4 does not read (runs, specs,
custody, comparison, checks, v8c_f1).  verdict = PASS_SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON (r13/r14 GATE_PASS_VERDICTS['I4'])
only when no clause fails, else FAIL (r14 GATE_FAIL_VERDICTS['I4'] = ('FAIL',)).  Exclusive create; nothing is overwritten.
serial_result_sha256 / parallel_result_sha256 = sha256 of the bytes of <run dir>/result.json (checked equal to <run
dir>/finish.json result_sha256 and to <run dir>.receipt.json result.sha256).

THE PAIR (A114 item 3).  --serial is the C2T N1 companion run (spec C2T_N1_SPEC_DRAFT_C3V001.json, pinned below: C2T's registered
spec with route_a.column_workers 1, every other byte identical); --parallel is the V007 C2T T-run itself (spec
C2T_P128_MS128_R5_CX1V004.FILLED.json 84933cad, SPEC_REGISTRY_R5_MS128_CX1V004 c7023846 entry C2T).  Both under driver v010 r5
b5cc62af with the tail ON.  A run whose inputs/call_spec.json bytes, start.json / result.json call_spec_sha256 or receipt spec pin
is not its pinned spec is REFUSED; so is a run that does not record b5cc62af in start.json (driver path and sha), result.json and
its receipt.

THE CUSTODY LIST (the identity comparator's definition, applied to one driver).  The comparator of record c2v007r2
(run_identity_compare_c2v007.py 052da0fe; registry identity_comparators) is loaded INERT from its verified bytes and its machinery
is used unchanged: Tree (lstat walk, canonical stage paths), Store (every file hashed once; only declared files parsed, strictly),
Side (the injective normalizer: <RUN>/<STAGE:>, the FILE_SHA and RA_SHA hex names, MASK_KEYS, RECORD_DROP, ledger tokens), the
closed DECLARED_DIFFER list D01-D18 with each entry's allowed normalization classes, the attempt-ledger pairing, apply_declared,
strict_pins, pair_norm, mask_cmp, compare_jsonl, cm_read, ro1_block, RO1_KEYS and driver_tables (restricted AST of the driver bytes;
the driver is never executed; c3v003 D1: check_ro1_armed is no longer called).  The comparator's AUTO_CUSTODY pair for route A -- the stage script and the solver the driver
plans for the run's column_workers (expected_scripts / expected_solver, RO1-gate semantics) -- is derived BY RULE from the sealed
driver's tables: worker RO1_ROUTE_A worker (column_workers 1) vs worker_parallel (8) [driver L2854-2856], solver AUX_UVT solver vs
solver_parallel [driver L2836-2838].  Under ONE driver both members of each pair also appear, identically, in the run's table
listings on BOTH sides (result.json uv_tail.code, driver uvt_plan L1110-1111; start.json static_pins, uvt_static_pins
L1215-1223), so the pair is NOT a free substring token here (that would break those listings); it is admitted where a run
records its OWN route-A implementation, in three forms, and nowhere else:
  F1 a pin-dict entry {path: sha} of the side's member when that dict holds exactly one member of the pair on each side;
  F2 a {path, sha256} pin object equal to the side's member;
  F3 the scalar positions route-A request / its result.json stage_records copy: script, script_sha256, the argv values after
     --solver and --solver-sha256; attempt start.json worker_pin; route_a_outcome.ro1.worker_sha256 and
     identity.route_a.outcome.ro1.worker_sha256.
Each admission fires the comparator's CUSTODY_TOKEN class, so the comparator's per-entry class policy still decides where route-A
custody may appear at all (D01, D02, D07, D16, D17 allow it).  I4 adds only what a serial-vs-parallel pair of one driver, with
the tail ON on both sides, needs, each read from the bytes named (DECLARED, closed, listed in the record):
  R1 the spec leaf numerics.route_a.column_workers 1 vs 8: inputs/call_spec.json, start.json and result.json normalized_spec
     (PAIR; the spec pins prove it is the only spec difference);
  R2 result.json identity.route_a.implementation.column_workers 1 vs 8 and .kind UVTAIL_RO1_SERIAL_C2V001 vs
     UVTAIL_RO1_PARALLEL_C2V001 (driver L2864-2871; PAIR, as the comparator's IMPL_KIND_PAIRS rule);
  R3 route-A argv: '--column-workers', '8' inserted once, right after '--start-iteration', '0', on the parallel side only (driver
     L2842-2843), in stages/route_a/request.json and its result.json stage_records copy (route-A custody: CUSTODY_TOKEN class);
  R4 stages/route_a/attempt_000/start.json key column_workers = 8 on the parallel side only (RO1 parallel worker 869ce387 L124);
  R5 start.json static_pins: exactly the two PARALLEL_ROUTE_A entries (worker 9dbdaf11, solver aed4dd59) on the parallel side only,
     each hashed from bytes (driver all_static_pins L3391-3393; the comparator's SF3 admission, narrowed to that table);
  R6 the tail-ON files the comparator knew only as Z2 new-only files (DECLARED_NEW_ONLY['Z2']) are both-side files here: entries
     I01-I06 with their allowed classes; SIDECAR_IDENTITY.json identity_sha256 is a derived digest, verified per side as the
     controller's sha256(_canon(identity)) (controller c5bdd055 L75, L363) before it is named; the sidecar iteration records are
     compared on 'payload' only, 'diagnostics' (wall-clock seconds and per-process cache-build counters) being the controller's
     own non-identity part (controller L421-423, L494-506: a resume compares 'payload' only);
  R7 the tail-ON code's timing keys are masked like MASK_KEYS_BASE: build_seconds (owned_uv_tail_lapse_v002 L647, L692, L795),
     begin_seconds and complete_seconds (controller L502); uv_tail / uv_tail_tap are NOT masked (the comparator masks them only
     for its tail-ON-vs-tail-OFF gates; here both sides carry the tail, so the tail records are compared);
  R8 IDENTITY.json: identity_sha256 and caller.sha256 verified per side as the checkpoint module's digests (c2v003 069b3935), the
     encoded caller replaced by its decoded content (the comparator's RA_IDENTITY); D17 additionally admits STAGE_DIR (the decoded
     caller keeps numerical_controls.uv_tail.sidecar_directory, which the comparator's tail-ON caller_norm removed).
Everything else must be byte-equal, or (a declared file) equal after the declared normalization, or (a stage log, c3v003 D3) equal
as a set of distinct normalized lines.  A file or directory present on one side only, a byte difference in an undeclared file
that is not a stage log, a stage log with a distinct line on one side only, a declared file unequal after normalization, a
normalization class firing in a file whose entry does not allow it, or a file of one run naming the other run's root on a path
boundary (c3v003 D2), is a difference OUTSIDE custody: its canonical relative path is listed in differences_outside_custody
(sorted).  bitwise_equal = no such difference AND every custody check C1-C11 holds (both runs ran exactly the driver-planned
serial / parallel worker and solver, RO1 armed with the registered key set and the side's worker and binding 86af6198 (c3v003
D1: whether RO1 fired is compared in the result records, not required false), R1-R5 present exactly, both runs' numerics the case
block's C2T numerics up to the leaf, the same stage directories by number and name).

V8C-F1.  The fix (REVIEW_DRIVER_V008_C4_V001 sec 6, f0987f41; CHECK_V001 7eb2e136 T8; V005 A47 I4 condition) is confirmed from bytes:
the parallel run's solver -- request argv --solver/--solver-sha256 = result.json identity.route_a.implementation.solver =
identity.route_a.custody.solver_code = checkpoint IDENTITY code.solver -- must be the driver's AUX_UVT solver_parallel entry, its
file must hash to that sha now, and its _pump must hold exactly one pickle.loads call, inside exactly one try statement whose AST
equals the AST of the review's fix text (try: msg=pickle.loads(raw); self._accept(w,msg) / except ColumnPoolError: raise /
except Exception as exc: self._lost(w,'MALFORMED_REPLY %s'%type(exc).__name__); break).  The review text itself is pinned and
must carry the three fragments verbatim.  Never hard-coded true.

REFUSALS (exit 2, no record): a CLI defect; a pin mismatch; a relative path; a run path, a receipt or the output path that is, or
resolves under, a protected path (a component starting 'uvt_', the C5H marker or either registered C5H directory spelling, '/.vol',
an NGC-target name), checked by name BEFORE each lookup and on every symlink target, never stat-ing a protected path; a symlink
INSIDE a run tree; a run whose own recorded root (finish.json result_path) does not resolve to the given directory; a special file; a stage-directory or canonical-path defect; a missing required file; a duplicate JSON key or an
unparseable JSON in any parsed file; the wrong driver; the wrong spec; a run not COMPLETED / valid, or a receipt not FINISHED,
exit 0, no stop reason, for this result; a normalization that is not injective; a comparator A71 last-wins hit; a tree that
changed during the comparison; numpy absent (the checkpoint module needs it).

INERT on import.  It reads two completed run trees, their receipts and pinned files; it executes no driver, run, stage, solver or
seal tool (the comparator and the checkpoint module are loaded from verified bytes for their functions only).

  PY -I -B write_i4_record_c3v003.py --serial N1_RUN_DIR --parallel N8_RUN_DIR --out I4_RECORD.json
"""
import ast
import copy
import hashlib
import json
import os
import re
import stat
import sys
import types
import unicodedata
from pathlib import Path

SCHEMA = 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'      # compare r14 GATE_SCHEMA
GATE = 'I4'
PASS_VERDICT = 'PASS_SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON'   # compare r13/r14 GATE_PASS_VERDICTS['I4']
FAIL_VERDICT = 'FAIL'                                    # compare r14 GATE_FAIL_VERDICTS['I4']
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
COMPARATOR = (ART + '/tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py',
              '052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e')
DRIVER = (ART + '/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',
          'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')
CASE_BLOCK = (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
              '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
SPEC_REGISTRY = (ART + '/v007_launch_packet_cx1/SPEC_REGISTRY_R5_MS128_CX1V004.json',
                 'c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90')
N8_SPEC = (ART + '/v007_launch_packet_cx1/P128/specs/C2T_P128_MS128_R5_CX1V004.FILLED.json',
           '84933cad8fa19bd9d8e95893e19ce744f8d19d3b44c937eb9ddf599c5c333bf2')
N1_SPEC = (ART + '/ri33_c3/i4/C2T_N1_SPEC_DRAFT_C3V001.json',
           '8ae6e2db8a1c721fa347d960c5aabe50bef20878ef8cefa047fabfed576c7ee7')
V8C_REVIEW = (ART + '/review_driver_v008_c4/synthesis/REVIEW_DRIVER_V008_C4_V001.md',
              'f0987f41df2067acde7bbecc80504cdd33ff2c49bb87a2a2227b28d584ec15ec')
V8C_FRAGMENTS = ('try: msg=pickle.loads(raw); self._accept(w,msg)', 'except ColumnPoolError: raise',
                 "except Exception as exc: self._lost(w,'MALFORMED_REPLY %s'%type(exc).__name__); break")
RECEIPT_SCHEMA = 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001'     # compare r14 RECEIPT_SCHEMA
RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'       # compare r14 RESULT_SCHEMA
T_CASES = ('C2T', 'C3T', 'C4T', 'C6T', 'S4T', 'C4T-D5', 'C4T-C5c', 'C4T-KLO', 'C4T-KHI', 'C4T-A')   # compare r14 L371
LEAF = ('numerics', 'route_a', 'column_workers')
SERIAL_N, PARALLEL_N = 1, 8
IMPL_KIND = ('UVTAIL_RO1_SERIAL_C2V001', 'UVTAIL_RO1_PARALLEL_C2V001')   # driver L2869-2871 (continuum_v001 tail)
I4_TIMING_KEYS = ('build_seconds', 'begin_seconds', 'complete_seconds')  # R7
C5H_DIRS = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/'
            'KMAX_A2F10_C5H_RUN_V001',
            '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
            'runs_ext/KMAX_A2F10_C5H_RUN_V001')                         # compare r14 C5H_REGISTERED_RUN_DIRS
C5H_MARKER = 'kmax_a2f10_c5h'                                             # comparator C5H_MARKER
NGC_WORDS = ('target', 'velocit', 'vobs', 'v_obs', 'rotcur', 'observed')
FIRMLINK = '/system/volumes/data'
REQUIRED = ('result.json', 'finish.json', 'start.json', 'progress.jsonl', 'inputs/call_spec.json', 'stages/route_a/request.json',
            'stages/route_a/attempt_000/start.json', 'stages/route_a/attempt_000/result.json',
            'stages/route_a/attempt_000/finish.json', 'stages/route_a/checkpoint/IDENTITY.json')
IDENTITY_REL = 'stages/route_a/checkpoint/IDENTITY.json'
SIDECAR_IDENTITY_REL = 'stages/route_a/uv_tail_sidecar/SIDECAR_IDENTITY.json'
ITER_RE = re.compile(r'stages/route_a/checkpoint/iteration_[^/]+/[^/]+\.json')
SIDECAR_ITER_RE = re.compile(r'stages/route_a/uv_tail_sidecar/iteration_[0-9]{4}\.json')
# R6: the comparator's DECLARED_NEW_ONLY['Z2'] JSON files, both sides under I4 (closed; (id, canonical regex, classes, why)).
I4_ENTRIES = (
    ('I01', r'inputs/uv_tail_config\.json', ('FILE_SHA', 'RUN_PATH'), 'driver L1091 ctx.write_input(uv_tail_config.json); both sides tail ON'),
    ('I02', r'inputs/uv_tail_route_a_request\.json', ('FILE_SHA', 'RUN_PATH'), 'driver L1092 ctx.write_input(uv_tail_route_a_request.json)'),
    ('I03', r'stages/route_a/uv_tail_sidecar/SIDECAR_IDENTITY\.json', ('FILE_SHA', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'),
     'controller L336-363: identity carries checkpoint_identity_sha256 (RA_SHA); identity_sha256 a verified derived digest'),
    ('I04', r'stages/route_a/uv_tail_sidecar/iteration_[0-9]{4}\.json', ('DECLARED_RULE', 'FILE_SHA', 'MASKED_KEY', 'RA_SHA'),
     'controller L494-506: payload compared; diagnostics MASK (the controller resume identity excludes it; its R7 timing keys mask)'),
    ('I05', r'stages/route_a/uv_tail_sidecar/finish_[0-9]{3,4}\.json', ('FILE_SHA', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'),
     'controller L552-562: route-A tail record (checkpoint identity) and the sidecar file map (file shas)'),
    ('I06', r'stages/route_a_tail_manifest/manifest/(ROUTE_A_TAIL_MANIFEST|finish)\.json',
     ('FILE_SHA', 'MASKED_KEY', 'RA_SHA', 'RUN_PATH', 'STAGE_DIR'),
     'manifest writer 44b31a8b L164-187, L249: identity / start-payload shas, in-tree paths and file shas, elapsed_seconds'),
)
I4_CLASS_DELTA = {'D17': ('STAGE_DIR',)}   # R8
# c3v003 D2: the byte after the other run's root that makes an occurrence name that root (a path boundary), and the escaped bytes
# that make a backslash one (a JSON escape writing a delimiter)
ROOT_BOUNDARY_NEXT = frozenset(b'/"\',:]} \t\r\n')
ROOT_BOUNDARY_ESCAPED = frozenset(b'"/nrtbf')
XREF_RULE = ('c3v003 D2: a file names the other run\'s root (its own spelling or its resolved path) when an occurrence is followed '
             'by a path boundary: /, the end of the file, a JSON / quote delimiter " \' , : ] } or JSON whitespace, or a backslash '
             'escaping " / n r t b f; an occurrence that continues a longer name is not a reference')
# c3v003 D3: the driver's stage logs (run_stages L1844-1847), canonical relative paths
STAGE_LOG_RE = re.compile(r'stages/[a-z0-9_]+/(stdout|stderr)\.txt')
STAGE_LOG_RULE = ('c3v003 D3: a stage log whose bytes differ is compared as the set of its distinct lines (UTF-8, surrogateescape; '
                  'split on newline) after the comparator\'s Side normalization of each line; a distinct line on one side only is '
                  'a difference outside custody; both files\' shas are recorded')


class Refused(SystemExit):
    def __init__(self, code, detail=''):
        self.code_name = code
        super().__init__('REFUSED: %s%s' % (code, (' ' + detail) if detail else ''))


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def pinned_bytes(pin, code):
    try:
        raw = Path(pin[0]).read_bytes()
    except OSError as exc:
        raise Refused(code, '%s unreadable (%s)' % (pin[0], type(exc).__name__))
    if sha_b(raw) != pin[1]:
        raise Refused(code, '%s is not %s' % (pin[0], pin[1][:12]))
    return raw


class _Dup(ValueError):
    pass


def _pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise _Dup('DUPLICATE_JSON_KEY')
        d[k] = v
    return d


def strict_json(raw, what):
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs)
    except _Dup:
        raise Refused('DUPLICATE_JSON_KEY', what)
    except (ValueError, UnicodeDecodeError) as exc:
        raise Refused('UNPARSEABLE_JSON', '%s (%s)' % (what, type(exc).__name__))


# ---------------------------------------------------------------- protected paths (by name; nothing protected is stat-ed)
def _fold(s):
    return unicodedata.normalize('NFC', s).casefold()


def protected_reason(p):
    f = _fold(os.path.normpath(p))
    if f == FIRMLINK or f.startswith(FIRMLINK + '/'):
        f = f[len(FIRMLINK):] or '/'
    if f == '/.vol' or f.startswith('/.vol/'):
        return 'VOL_INODE_ALIAS'
    parts = [x for x in f.split('/') if x]
    if any(x.startswith('uvt_') for x in parts):
        return 'UVT_RUN_TREE'
    if any(C5H_MARKER in x for x in parts):
        return 'C5H_MARKER'
    for reg in C5H_DIRS:
        r = _fold(reg)
        if f == r or f.startswith(r + '/'):
            return 'C5H_REGISTERED_RUN'
    if any('ngc' in x for x in parts) and any(w in x for x in parts for w in NGC_WORDS):
        return 'NGC_TARGET'
    return None


def guarded_resolve(p, what):
    """The comparator's guarded_resolve rule, by name only (nothing protected is ever looked up): resolve the absolute path p
    component by component; each partial path and each symlink target is checked by name BEFORE its lstat / readlink; '..' is
    applied by the walk; at most 40 hops.  Returns the real path."""
    if not isinstance(p, str) or not os.path.isabs(p):
        raise Refused('RELATIVE_OR_MISSING_PATH', what)
    why = protected_reason(p)
    if why:
        raise Refused('PROTECTED_PATH', '%s: %s' % (what, why))
    queue, cur, hops = list(Path(p).parts[1:]), '/', 0
    while queue:
        name = queue.pop(0)
        if name in ('', '.'):
            continue
        if name == '..':
            cur = os.path.dirname(cur) or '/'
            continue
        nxt = os.path.join(cur, name)
        why = protected_reason(nxt)
        if why:
            raise Refused('PROTECTED_PATH', '%s: %s' % (what, why))
        try:
            m = os.lstat(nxt).st_mode
        except FileNotFoundError:
            raise Refused('MISSING_PATH', '%s: %s' % (what, nxt))
        if stat.S_ISLNK(m):
            hops += 1
            if hops > 40:
                raise Refused('SYMLINK_LOOP', what)
            t = os.readlink(nxt)
            why = protected_reason(t if os.path.isabs(t) else os.path.join(cur, t))
            if why:
                raise Refused('PROTECTED_PATH', '%s: symlink target: %s' % (what, why))
            parts = list(Path(t).parts)
            if os.path.isabs(t):
                cur, parts = '/', parts[1:]
            queue = parts + queue
            continue
        cur = nxt
    why = protected_reason(cur)
    if why:
        raise Refused('PROTECTED_PATH', '%s: %s' % (what, why))
    return cur


def checked_path(p, what, kind):
    """guarded_resolve, then the kind of the resolved last component ('dir' or 'file'); returns the real path."""
    real = guarded_resolve(p, what)
    m = os.lstat(real).st_mode
    if kind == 'dir' and not stat.S_ISDIR(m):
        raise Refused('NOT_A_DIRECTORY', what)
    if kind == 'file' and not stat.S_ISREG(m):
        raise Refused('NOT_A_REGULAR_FILE', what)
    return real


def own_root(real, what):
    """The run's own spelling of its root: the directory of finish.json result_path (driver cmd_run L3594 writes
    str(out / 'result.json') with out = os.path.abspath(outdir), lexical); it must resolve to the given run directory."""
    fp = os.path.join(real, 'finish.json')
    try:
        m = os.lstat(fp).st_mode
    except FileNotFoundError:
        raise Refused('MISSING_REQUIRED_FILE', '%s: finish.json' % what)
    if stat.S_ISLNK(m):
        raise Refused('SYMLINK_IN_TREE', '%s: finish.json' % what)
    if not stat.S_ISREG(m):
        raise Refused('NOT_A_REGULAR_FILE', '%s finish.json' % what)
    fin = strict_json(Path(fp).read_bytes(), '%s finish.json' % what)
    rp = fin.get('result_path') if isinstance(fin, dict) else None
    if not (isinstance(rp, str) and os.path.isabs(rp) and os.path.basename(rp) == 'result.json' and os.path.normpath(rp) == rp):
        raise Refused('FINISH_RESULT_PATH', what)
    root = os.path.dirname(rp)
    if guarded_resolve(root, '%s recorded root' % what) != real:
        raise Refused('RUN_ROOT_SPELLING_DOES_NOT_RESOLVE_TO_THE_GIVEN_RUN', what)
    return root


# ---------------------------------------------------------------- pinned code (loaded from verified bytes; functions only)
def load_module(pin, name):
    raw = pinned_bytes(pin, 'PIN_MISMATCH')
    m = types.ModuleType(name)
    m.__file__ = pin[0]
    exec(compile(raw, pin[0], 'exec'), m.__dict__)
    return m


# ---------------------------------------------------------------- V8c-F1 from bytes
def v8c_f1_site(src_bytes):
    """(ok, detail): _pump holds exactly one pickle.loads, inside exactly one try statement whose AST equals the review's fix."""
    det = {}
    try:
        tree = ast.parse(src_bytes.decode('utf-8'))
    except (SyntaxError, UnicodeDecodeError) as exc:
        return False, {'why': 'unparseable solver (%s)' % type(exc).__name__}
    want = ast.parse('\n'.join(V8C_FRAGMENTS) + '\n').body
    if len(want) != 1 or not isinstance(want[0], ast.Try):
        return False, {'why': 'fix text is not one try statement'}
    want_dump = ast.dump(want[0], annotate_fields=True, include_attributes=False)
    pumps = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == '_pump']
    det['pump_functions'] = len(pumps)
    if len(pumps) != 1:
        return False, dict(det, why='expected exactly one _pump')

    def is_loads(c):
        return (isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr == 'loads'
                and isinstance(c.func.value, ast.Name) and c.func.value.id == 'pickle')
    loads = [n for n in ast.walk(pumps[0]) if is_loads(n)]
    tries = [n for n in ast.walk(pumps[0]) if isinstance(n, ast.Try) and any(is_loads(x) for s in n.body for x in ast.walk(s))]
    det['pickle_loads_calls_in_pump'] = len(loads)
    det['try_statements_around_pickle_loads'] = len(tries)
    if len(tries) != 1 or len(loads) != 1:
        return False, dict(det, why='pickle.loads must occur exactly once, inside one try')
    det['line'] = tries[0].lineno
    det['ast_equal_to_review_fix_text'] = ast.dump(tries[0], annotate_fields=True, include_attributes=False) == want_dump
    return det['ast_equal_to_review_fix_text'], det


# ---------------------------------------------------------------- route-A custody admission (F1 F2 F3, R3)
class Custody:
    """The serial / parallel route-A members (worker, solver) from the driver tables; admissions are counted per file."""

    def __init__(self, worker, solver):
        self.pairs = {'worker': worker, 'solver': solver}   # what -> ((serial path, sha), (parallel path, sha))
        self.count = {}

    def obj(self, side, what):
        p = self.pairs[what][side]
        return {'path': str(p[0]), 'sha256': p[1]}

    def admit(self, x, y, fire, rel):
        """F1 / F2 on normalized copies, in place; returns the number of admissions."""
        n = [0]

        def f2(a, b):
            for what in self.pairs:
                if a == self.obj(0, what) and b == self.obj(1, what):
                    return '<ROUTE_A_%s_PIN>' % what.upper()
            return None

        def walk(a, b):
            if isinstance(a, dict) and isinstance(b, dict):
                for what, (s, p) in self.pairs.items():
                    ks, kp = str(s[0]), str(p[0])
                    if ks in a and kp not in a and kp in b and ks not in b and a[ks] == s[1] and b[kp] == p[1]:
                        del a[ks]
                        del b[kp]
                        n[0] += 1
                for k in sorted(set(a) & set(b), key=str):
                    lab = f2(a[k], b[k])
                    if lab:
                        a[k] = b[k] = lab
                        n[0] += 1
                    else:
                        walk(a[k], b[k])
            elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
                for i in range(len(a)):
                    lab = f2(a[i], b[i])
                    if lab:
                        a[i] = b[i] = lab
                        n[0] += 1
                    else:
                        walk(a[i], b[i])
        walk(x, y)
        if n[0]:
            fire('CUSTODY_TOKEN')
            self.count[rel] = self.count.get(rel, 0) + n[0]
        return n[0]

    def request(self, x, y, fire, rel):
        """F3 + R3 on a route-A request (or its stage_records copy): returns (x', y', why or None)."""
        if not isinstance(x, dict) or not isinstance(y, dict):
            return x, y, 'request not an object'
        x, y = dict(x), dict(y)
        (ws, wp), (ss, sp) = self.pairs['worker'], self.pairs['solver']
        if [x.get('script'), x.get('script_sha256')] != [str(ws[0]), ws[1]] or [y.get('script'), y.get('script_sha256')] != [str(wp[0]), wp[1]]:
            return x, y, 'route-A script is not the driver-planned serial / parallel worker'
        x['script'] = y['script'] = '<SCRIPT_ROUTE_A_PATH>'
        x['script_sha256'] = y['script_sha256'] = '<SCRIPT_ROUTE_A_SHA>'
        ok3, yargv, why = strip_column_workers(x.get('argv'), y.get('argv'))
        if not ok3:
            return x, y, why
        xa, ya = list(x['argv']), list(yargv)
        for argv, sol in ((xa, ss), (ya, sp)):
            for flag, val, lab in (('--solver', str(sol[0]), '<ROUTE_A_SOLVER>'), ('--solver-sha256', sol[1], '<ROUTE_A_SOLVER_SHA256>')):
                idx = [i for i in range(0, len(argv) - 1) if argv[i] == flag]
                if len(idx) != 1 or argv[idx[0] + 1] != val:
                    return x, y, 'route-A argv %s is not the driver-planned solver' % flag
                argv[idx[0] + 1] = lab
        x['argv'], y['argv'] = xa, ya
        fire('CUSTODY_TOKEN')
        self.count[rel] = self.count.get(rel, 0) + 1
        return x, y, None


def strip_column_workers(ra, rb):
    """(ok, rb without the R3 pair, why): ra has no --column-workers; rb has it exactly once, value '8', right after the
    '--start-iteration', '0' pair (driver L2842-2843)."""
    if not isinstance(ra, list) or not isinstance(rb, list):
        return False, rb, 'argv not a list'
    if '--column-workers' in ra:
        return False, rb, 'serial argv carries --column-workers'
    if rb.count('--column-workers') != 1:
        return False, rb, 'parallel argv carries --column-workers %d times' % rb.count('--column-workers')
    i = rb.index('--column-workers')
    if i + 1 >= len(rb) or rb[i + 1] != str(PARALLEL_N):
        return False, rb, 'parallel --column-workers value is not %d' % PARALLEL_N
    if i < 2 or rb[i - 2:i] != ['--start-iteration', '0']:
        return False, rb, '--column-workers is not right after --start-iteration 0 (driver L2842-2843)'
    return True, rb[:i] + rb[i + 2:], None


def leaf_diff(a, b, path=()):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(('/'.join(map(str, path + (k,))), 'KEY_ON_ONE_SIDE'))
            else:
                out += leaf_diff(a[k], b[k], path + (k,))
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += leaf_diff(x, y, path + (i,))
    elif type(a) is not type(b) or a != b:
        out.append(('/'.join(map(str, path)), [a, b] if not isinstance(a, (dict, list)) else 'STRUCTURE'))
    return out


def _get(o, path):
    for k in path:
        if not isinstance(o, dict) or k not in o:
            return None
        o = o[k]
    return o


def _sanitize(det):
    """Difference details keep WHERE (JSON paths, rule names, pin keys) and never record values (no row value, no number from a
    run record enters the gate record)."""
    if isinstance(det, dict):
        out = {}
        for k, v in det.items():
            if k in ('values', 'new_value', 'value', 'first', 'second'):
                continue
            if k == 'differing' and isinstance(v, list):
                out[k] = [x[0] if isinstance(x, (tuple, list)) and x else str(x)[:200] for x in v]
            else:
                out[k] = _sanitize(v)
        return out
    if isinstance(det, (list, tuple)):
        return [_sanitize(x) for x in det]
    if isinstance(det, str):
        return det[:300]
    if det is None or isinstance(det, bool):
        return det
    return type(det).__name__


def _refuse_parse_problems(*stores):
    for S in stores:
        if S.problems:
            bad = S.problems[0]
            raise Refused('DUPLICATE_JSON_KEY' if 'DUPLICATE_JSON_KEY' in str(bad.get('error', '')) else 'UNPARSEABLE_JSON',
                          '%s %s' % (S.tag, bad.get('file')))


# ---------------------------------------------------------------- c3v003 D1: RO1 custody per side (a firing is compared, not refused)
def ro1_armed_side_pins(cmp, ro1, expected_worker, binding_sha):
    """C6: the comparator's check_ro1_armed (052da0fe L1889) without its fired False / events [] clauses: the block has exactly the
    registered key set (RO1_KEYS), rule RO1, armed true, and this side's own worker and binding pins.  Whether RO1 fired, and its
    events, are compared with the rest of the result records (prereg r6 B0_RO1: firing in a T-run is recorded, not an invalidity)."""
    return bool(isinstance(ro1, dict) and set(ro1) == set(cmp.RO1_KEYS) and ro1.get('rule') == 'RO1' and ro1.get('armed') is True
                and ro1.get('worker_sha256') == expected_worker and ro1.get('binding_sha256') == binding_sha)


# ---------------------------------------------------------------- c3v003 D2: the other run's root, on a path boundary only
def boundary_scan(p, needles, chunk=1 << 22):
    """(sha256 of the bytes read, the needles that occur followed by a path boundary), in one streamed read.  Every occurrence is
    examined: it counts when the next byte is in ROOT_BOUNDARY_NEXT, or is a backslash whose next byte is in ROOT_BOUNDARY_ESCAPED,
    or the file ends there; an occurrence that continues a longer name (.../C2T_RUN inside .../C2T_RUN_N1) is passed over and the
    search goes on."""
    h, found, buf, eof = hashlib.sha256(), set(), b'', False
    keep = max(len(n) for n in needles) + 1          # an occurrence and its two-byte lookahead may cross a chunk edge
    with open(p, 'rb') as f:
        while not eof:
            b = f.read(chunk)
            eof = not b
            h.update(b)
            buf += b
            for nd in needles:
                i = -1 if nd in found else buf.find(nd)
                while i >= 0:
                    j = i + len(nd)
                    if j + 2 > len(buf) and not eof:
                        break                         # undecided in this window; the kept tail holds it for the next one
                    nb = buf[j:j + 1]
                    if (not nb or nb[0] in ROOT_BOUNDARY_NEXT
                            or (nb == b'\\' and len(buf) > j + 1 and buf[j + 1] in ROOT_BOUNDARY_ESCAPED)):
                        found.add(nd)
                        break
                    i = buf.find(nd, i + 1)
            buf = buf[-keep:]
    return h.hexdigest(), found


def cross_run_hits(S, p, needles):
    """The comparator's Store.hash_scan (the file's first sha; substring hits of the other run's root), then, only for a file it
    hits, boundary_scan of the same bytes (the sha must equal the first sha).  Returns (substring hits, boundary hits)."""
    _, hit = S.hash_scan(p, needles)
    if not hit:
        return set(), set()
    d2, found = boundary_scan(p, sorted(hit))
    if d2 != S.sha.get(str(p)):
        raise Refused('TREE_CHANGED_DURING_COMPARISON', '%s %s' % (S.tag, S.rel(p)))
    return set(hit), found


# ---------------------------------------------------------------- c3v003 D3: a stage log as its set of distinct lines
def log_lines(side, store, p):
    """(the set of distinct lines of one stage log after the side's normalization -- the comparator's Side.s: run root and stage
    directories, file shas, ledger tokens --, the number of lines).  The store's read (its sha must equal the first sha); UTF-8
    with surrogateescape (lossless); split on newline, the final newline ending the last line."""
    raw = store.read(p)
    if raw is None:
        return None, 0
    lines = raw.decode('utf-8', 'surrogateescape').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return {side.s(x, '<stage log line>') for x in lines}, len(lines)


# ---------------------------------------------------------------- one declared JSON file
def compare_declared_json(cmp, R, N, x0, y0, rel, cust, rules=(), allow_new=None, request=False, stage_records=False, drop=()):
    """The comparator's compare_json_file order (pair_norm, strict_pins, apply_declared, mask_cmp, seq) with the route-A custody
    admission (F1 F2 F3) between normalization and the pin check.  Returns (ok, detail, rules report, pin notes)."""
    x, y, mr_, mn_ = cmp.pair_norm(R, N, x0, y0, rel, drop)
    x, y = copy.deepcopy(x), copy.deepcopy(y)
    fire = lambda cls, _N=N, _rel=rel: _fire_at(_N, _rel, cls)
    why = None
    if request:
        x, y, why = cust.request(x, y, fire, rel)
    if stage_records and isinstance(x, dict) and isinstance(y, dict):
        sx, sy = x.get('stage_records'), y.get('stage_records')
        if isinstance(sx, list) and isinstance(sy, list):
            ix = [i for i, r in enumerate(sx) if isinstance(r, dict) and r.get('name') == 'route_a']
            iy = [i for i, r in enumerate(sy) if isinstance(r, dict) and r.get('name') == 'route_a']
            if len(ix) == 1 and len(iy) == 1:
                rx, ry, why = cust.request(sx[ix[0]], sy[iy[0]], fire, rel)
                sx, sy = list(sx), list(sy)
                sx[ix[0]], sy[iy[0]] = rx, ry
                x['stage_records'], y['stage_records'] = sx, sy
            else:
                why = 'the route_a stage record is not there exactly once'
    cust.admit(x, y, fire, rel)
    notes, viol = [], []
    cmp.strict_pins(x, y, rel, allow_new or {}, notes, viol)
    with N.at_file(rel):
        x2, y2, rep, bad = cmp.apply_declared(x, y, list(rules), fire=N._fire)
    mok, mdet = cmp.mask_cmp(mr_, mn_, rel, rep)
    ok = cmp.seq(x2, y2) and not viol and not bad and mok and why is None
    det = None if ok else {'differing': cmp.diffs(x2, y2)[:6], 'pin_violations': viol[:4], 'rule_violations': bad[:4],
                           'custody_rule': why, 'masked_key_paths_equal': mok}
    return ok, det, rep, notes


def _fire_at(S, rel, cls):
    with S.at_file(rel):
        S._fire(cls)


# ---------------------------------------------------------------- main producer
def produce(serial, parallel, out):
    try:
        import numpy  # noqa: F401  (the pinned checkpoint module needs it)
    except ImportError:
        raise Refused('NUMPY_UNAVAILABLE', 'run with the program interpreter')
    me = Path(__file__).resolve()
    me_sha = sha_f(me)
    # ---- pins
    cmp = load_module(COMPARATOR, 'run_identity_compare_c2v007_for_i4')
    if tuple(cmp.DRIVERS['r5']) != DRIVER:
        raise Refused('PIN_MISMATCH', 'comparator r5 driver pin is not b5cc62af')
    cmp.DRIVER[:] = list(DRIVER)
    cmp.DRIVER_RAW[:] = [None, None]
    cmp.SELECTED_PIN_ENTRIES[:] = [None, None]
    drv_raw = pinned_bytes(DRIVER, 'PIN_MISMATCH')
    tables = cmp.driver_tables(drv_raw, DRIVER[0])
    for t in ('RO1_ROUTE_A', 'AUX_UVT', 'AUX', 'PARALLEL_ROUTE_A'):
        if t not in tables:
            raise Refused('DRIVER_TABLE_UNREADABLE', t)
    W_S, W_P = tables['RO1_ROUTE_A']['worker'], tables['RO1_ROUTE_A']['worker_parallel']
    S_S, S_P = tables['AUX_UVT']['solver'], tables['AUX_UVT']['solver_parallel']
    BINDING = tables['RO1_ROUTE_A']['binding']
    PAR_PINS = [tables['PARALLEL_ROUTE_A']['worker'], tables['PARALLEL_ROUTE_A']['solver']]
    if tuple(tables['AUX']['checkpoint_module']) != tuple(cmp.CKPT):
        raise Refused('PIN_MISMATCH', 'driver checkpoint module is not the comparator CKPT pin')
    # the comparator's own expected_scripts / expected_solver give the same pairs (RO1-gate semantics, column workers 1 / 8)
    if (tuple(cmp.expected_scripts('Z2', 'route_a', SERIAL_N, tables, tables, ())[1]) != tuple(W_S)
            or tuple(cmp.expected_scripts('Z2', 'route_a', PARALLEL_N, tables, tables, ())[1]) != tuple(W_P)
            or tuple(cmp.expected_solver('Z2', SERIAL_N, tables, tables)[1]) != tuple(S_S)
            or tuple(cmp.expected_solver('Z2', PARALLEL_N, tables, tables)[1]) != tuple(S_P)):
        raise Refused('CUSTODY_DERIVATION_MISMATCH')
    for p_, s_ in [W_S, W_P, S_S, S_P, BINDING] + PAR_PINS:
        if not cmp.file_ok(p_, s_):
            raise Refused('CUSTODY_FILE_BYTES', p_)
    cust = Custody((W_S, W_P), (S_S, S_P))
    cm = cmp.load_cm()                                            # checkpoint module c2v003 069b3935 from verified bytes
    cb = strict_json(pinned_bytes(CASE_BLOCK, 'PIN_MISMATCH'), 'case block')
    reg = strict_json(pinned_bytes(SPEC_REGISTRY, 'PIN_MISMATCH'), 'spec registry')
    c2t = [e for e in reg.get('specs', []) if e.get('case') == 'C2T']
    if (len(c2t) != 1 or c2t[0].get('filled') != {'path': N8_SPEC[0], 'sha256': N8_SPEC[1]}
            or reg.get('driver') != {'path': DRIVER[0], 'sha256': DRIVER[1]}):
        raise Refused('SPEC_REGISTRY_C2T_ENTRY')
    o8 = strict_json(pinned_bytes(N8_SPEC, 'PIN_MISMATCH'), 'N8 spec')
    o1 = strict_json(pinned_bytes(N1_SPEC, 'PIN_MISMATCH'), 'N1 spec')
    if leaf_diff(o8, o1) != [('/'.join(LEAF), [PARALLEL_N, SERIAL_N])]:
        raise Refused('N1_SPEC_NOT_C2T_WITH_ONE_LEAF', str(leaf_diff(o8, o1))[:200])
    review = pinned_bytes(V8C_REVIEW, 'PIN_MISMATCH').decode('utf-8')
    if not all(review.count('`%s`' % f) == 1 for f in V8C_FRAGMENTS):
        raise Refused('V8C_REVIEW_TEXT', 'the review does not carry the fix fragments verbatim')
    # ---- paths (each checked by name before any lookup)
    serial_real = checked_path(serial, '--serial', 'dir')
    parallel_real = checked_path(parallel, '--parallel', 'dir')
    if serial_real == parallel_real or serial_real.startswith(parallel_real + '/') or parallel_real.startswith(serial_real + '/'):
        raise Refused('RUNS_NOT_DISTINCT')
    serial, parallel = own_root(serial_real, 'serial'), own_root(parallel_real, 'parallel')
    rec_s = checked_path(serial + '.receipt.json', 'serial receipt', 'file')
    rec_p = checked_path(parallel + '.receipt.json', 'parallel receipt', 'file')
    if not isinstance(out, str) or not os.path.isabs(out) or os.path.normpath(out) != out or protected_reason(out):
        raise Refused('OUT_PATH', 'an absolute, normal, unprotected path is required')
    out_real = os.path.join(checked_path(os.path.dirname(out), 'output directory', 'dir'), os.path.basename(out))
    for r in (serial, parallel, serial_real, parallel_real):
        if out == r or out.startswith(r + '/') or out_real == r or out_real.startswith(r + '/'):
            raise Refused('OUT_INSIDE_A_RUN')
    if os.path.lexists(out):
        raise Refused('OUT_EXISTS', 'exclusive create')
    # ---- trees (comparator Tree: lstat walk; links and special files listed, never followed or opened)
    cmp.MASK_KEYS.clear()
    cmp.MASK_KEYS.update(set(cmp.MASK_KEYS_BASE) | set(I4_TIMING_KEYS))   # R7
    del cmp.LAST_WINS[:]
    TR, TN = cmp.Tree(Path(serial)), cmp.Tree(Path(parallel))
    for tag, T in (('serial', TR), ('parallel', TN)):
        if T.links:
            raise Refused('SYMLINK_IN_TREE', '%s: %s' % (tag, T.links[:5]))
        if T.special:
            raise Refused('SPECIAL_FILE_IN_TREE', '%s: %s' % (tag, [x[0] for x in T.special[:5]]))
        if T.problems:
            raise Refused('STAGE_DIRECTORY_DEFECT', '%s: %s' % (tag, str(T.problems[:3])[:300]))
        if T.inv_collisions:
            raise Refused('CANONICAL_PATH_COLLISION', tag)
        miss = [r for r in REQUIRED if r not in T.inv]
        if miss:
            raise Refused('MISSING_REQUIRED_FILE', '%s: %s' % (tag, miss))
    SR, SN = cmp.Store(Path(serial), 'reference', TR), cmp.Store(Path(parallel), 'new', TN)
    root_s, root_p = serial.encode(), parallel.encode()
    needles_s = tuple(sorted({serial.encode(), serial_real.encode()}))
    needles_p = tuple(sorted({parallel.encode(), parallel_real.encode()}))
    xref = {'reference': {}, 'new': {}}               # c3v003 D2: store tag -> {raw path: (substring hits, boundary hits)}
    for T, S, other in ((TR, SR, needles_p), (TN, SN, needles_s)):
        for rel in T.files:
            sub, bnd = cross_run_hits(S, T.run / rel, other)
            if sub:
                xref[S.tag][str(T.run / rel)] = (sub, bnd)
    inv_r, inv_n = TR.inventory(), TN.inventory()
    # ---- attempt ledger (the comparator's grouping rule)
    led_r, led_n, lbad = {}, {}, []
    for T, inv, led in ((TR, inv_r, led_r), (TN, inv_n, led_n)):
        seen = {}
        for rel in sorted(inv):
            m = cmp.ATTEMPT_RE.fullmatch(rel)
            if not m:
                continue
            key = (m.group(1), m.group(2), m.group(3))
            if key in seen:
                lbad.append({'kind': 'LEDGER_GROUPED_KEY_COLLISION', 'raw_paths': [seen[key], rel]})
                continue
            seen[key] = rel
        for key, rel in sorted(seen.items()):
            led.setdefault(key[0], {}).setdefault(key[1], {})[key[2]] = inv.pop(rel)
    led_tokens = []
    for d in sorted(set(led_r) | set(led_n)):
        tr_, tn_ = sorted((led_r.get(d) or {}).items()), sorted((led_n.get(d) or {}).items())
        if len(tr_) != len(tn_):
            lbad.append({'dir': d, 'tokens': [len(tr_), len(tn_)]})
            continue
        for i, ((ta, _), (tb, _)) in enumerate(zip(tr_, tn_)):
            if not (cmp.ATTEMPT_TOKEN_RE.fullmatch(ta) and cmp.ATTEMPT_TOKEN_RE.fullmatch(tb)):
                lbad.append({'dir': d, 'kind': 'ATTEMPT_TOKEN_FORMAT'})
                continue
            if ta != tb:
                led_tokens.append([ta, tb, '<ATTEMPT_TOKEN_%s_%d>' % (d.split('/')[1].upper(), i), 'LEDGER_TOKEN'])
    led_files = {str(p) for led in (led_r, led_n) for v in led.values() for kk in v.values() for p in kk.values()}
    # ---- classification: equal bytes first; the closed declared list (D01-D18 + I01-I06) may differ; nothing else
    entries = cmp.declared_entries('Z2') + [(i, re.compile(rx), tuple(cl), why) for i, rx, cl, why in I4_ENTRIES]
    allowed_cls = {i: set(cl) | set(I4_CLASS_DELTA.get(i, ())) for i, _, cl, _ in entries}
    outside, why_out = set(), {}

    def flag(rel, why):
        outside.add(rel)
        why_out.setdefault(rel, why)
    both = sorted(set(inv_r) & set(inv_n))
    for rel in sorted(set(inv_r) - set(inv_n)):
        flag(rel, 'SERIAL_ONLY_FILE')
    for rel in sorted(set(inv_n) - set(inv_r)):
        flag(rel, 'PARALLEL_ONLY_FILE')
    for rel in sorted(set(TR.dinv) ^ set(TN.dinv)):
        flag(rel + '/', 'DIRECTORY_ON_ONE_SIDE')
    for b in lbad:
        flag('%s/<attempt ledger>' % b.get('dir', 'stages/route_a/checkpoint/attempts'), 'ATTEMPT_LEDGER')
    decl_rel = {}
    for rel in both:
        e = cmp.declared_entry(entries, rel)
        if e is not None and e[0] == 'AMBIGUOUS':
            raise Refused('DECLARED_LIST_AMBIGUOUS', rel)
        if e is not None:
            decl_rel[rel] = e
    SR.allow = {str(inv_r[r]) for r in decl_rel} | {p for p in led_files if p.startswith(serial + '/')}
    SN.allow = {str(inv_n[r]) for r in decl_rel} | {p for p in led_files if p.startswith(parallel + '/')}
    # ---- the two runs' own records (strict; the required files are declared files)
    st_s, st_p = SR.json(inv_r['start.json']), SN.json(inv_n['start.json'])
    rs_s, rs_p = SR.json(inv_r['result.json']), SN.json(inv_n['result.json'])
    fi_s, fi_p = SR.json(inv_r['finish.json']), SN.json(inv_n['finish.json'])
    cs_s, cs_p = SR.json(inv_r['inputs/call_spec.json']), SN.json(inv_n['inputs/call_spec.json'])
    _refuse_parse_problems(SR, SN)
    rc_s = strict_json(Path(rec_s).read_bytes(), 'serial receipt')
    rc_p = strict_json(Path(rec_p).read_bytes(), 'parallel receipt')
    runs = {}
    for tag, root, real, inv, S, st, rs, fi, rc, rcp, spec in (
            ('serial', serial, serial_real, inv_r, SR, st_s, rs_s, fi_s, rc_s, rec_s, N1_SPEC),
            ('parallel', parallel, parallel_real, inv_n, SN, st_p, rs_p, fi_p, rc_p, rec_p, N8_SPEC)):
        for name, o in (('start.json', st), ('result.json', rs), ('finish.json', fi), ('receipt', rc)):
            if not isinstance(o, dict) or isinstance(o, cmp.Unparseable):
                raise Refused('RECORD_NOT_AN_OBJECT', '%s %s' % (tag, name))
        rsha = S.sha_of(inv['result.json'])
        drv_seen = [st.get('driver'), st.get('driver_sha256'), rs.get('driver_sha256'),
                    ((rc.get('pins') or {}).get('driver') or {}).get('sha256')]
        if drv_seen != [DRIVER[0], DRIVER[1], DRIVER[1], DRIVER[1]]:
            raise Refused('DRIVER_NOT_B5CC62AF', '%s records %s' % (tag, [str(x)[-24:] for x in drv_seen]))
        csha = S.sha_of(inv['inputs/call_spec.json'])
        spec_seen = [csha, st.get('call_spec_sha256'), rs.get('call_spec_sha256'), ((rc.get('pins') or {}).get('spec') or {}).get('sha256')]
        if spec_seen != [spec[1]] * 4:
            raise Refused('N1_SPEC_NOT_THE_PINNED_DRAFT' if tag == 'serial' else 'N8_SPEC_NOT_C2T_REGISTERED',
                          '%s records %s' % (tag, [str(x)[:12] for x in spec_seen]))
        if rs.get('schema') != RESULT_SCHEMA or rs.get('status') != 'COMPLETED' or rs.get('valid') is not True:
            raise Refused('RUN_NOT_COMPLETED', '%s status %r valid %r' % (tag, rs.get('status'), rs.get('valid')))
        if fi.get('result_sha256') != rsha or fi.get('status') != 'COMPLETED':
            raise Refused('FINISH_NOT_THIS_RESULT', tag)
        res = rc.get('result') if isinstance(rc.get('result'), dict) else {}
        rp_ok = isinstance(res.get('path'), str) and (os.path.normpath(res['path']) == os.path.join(root, 'result.json') or (
            os.path.isabs(res['path']) and guarded_resolve(res['path'], '%s receipt result path' % tag) == os.path.join(real, 'result.json')))
        if (rc.get('schema') != RECEIPT_SCHEMA or res.get('sha256') != rsha or not rp_ok or rc.get('driver_status') != 'COMPLETED'
                or rc.get('status') != 'FINISHED' or rc.get('exit_code') != 0 or isinstance(rc.get('exit_code'), bool)
                or rc.get('stop_reason') is not None):
            raise Refused('RECEIPT_NOT_FINISHED_FOR_THIS_RESULT', tag)
        runs[tag] = {'path': root, 'resolved': real, 'result': {'path': os.path.join(root, 'result.json'), 'sha256': rsha},
                     'call_spec_sha256': csha, 'driver_sha256': DRIVER[1],
                     'receipt': {'path': rcp, 'sha256': sha_f(rcp), 'status': rc.get('status'), 'exit_code': rc.get('exit_code'),
                                 'driver_status': rc.get('driver_status'), 'stop_reason': rc.get('stop_reason')}}
    # ---- normalizer: ledger tokens only (route-A custody is admitted structurally, F1 F2 F3); RA and derived names
    pairs, tok_bad, _ = cmp.build_tokens(led_tokens)
    if tok_bad:
        raise Refused('TOKEN_RELATION_DEFECT', str(tok_bad[:2])[:300])
    markers = cmp.NORMALIZER_MARKERS + tuple(sorted({t[2] for t in led_tokens})) + (
        '<ROUTE_A_WORKER_PIN>', '<ROUTE_A_SOLVER_PIN>', '<SCRIPT_ROUTE_A_PATH>', '<SCRIPT_ROUTE_A_SHA>', '<ROUTE_A_SOLVER>',
        '<ROUTE_A_SOLVER_SHA256>')
    names, derived = {'reference': {}, 'new': {}}, {}
    for tag, T, S, inv in (('reference', TR, SR, inv_r), ('new', TN, SN, inv_n)):
        for rel in T.files:
            c = T.canon(rel)
            if not re.fullmatch(r'stages/route_a/checkpoint/.*\.json', c) or str(T.run / rel) not in S.allow:
                continue
            body = S.json(T.run / rel)
            if isinstance(body, dict) and not isinstance(body, cmp.Unparseable):
                ps, ids = body.get('payload_sha256', ''), body.get('identity_sha256', '')
                if isinstance(ps, str) and cmp.SHA_RE.fullmatch(ps):
                    names[tag].setdefault(ps, set()).add('P:' + c)
                if isinstance(ids, str) and cmp.SHA_RE.fullmatch(ids):
                    names[tag].setdefault(ids, set()).add('I')
        ok_sid = None
        if SIDECAR_IDENTITY_REL in inv and str(inv[SIDECAR_IDENTITY_REL]) in S.allow:
            sid = S.json(inv[SIDECAR_IDENTITY_REL])
            ident = sid.get('identity') if isinstance(sid, dict) else None
            h = sid.get('identity_sha256') if isinstance(sid, dict) else None
            ok_sid = bool(isinstance(ident, dict) and isinstance(h, str) and cmp.SHA_RE.fullmatch(h)
                          and sha_b(json.dumps(ident, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()) == h)
            if ok_sid:
                names[tag].setdefault(h, set()).add('D:SIDECAR_IDENTITY')
        derived[tag] = {'sidecar_identity_sha256_verified': ok_sid}
    _refuse_parse_problems(SR, SN)
    R = cmp.Side(TR, SR, [(r, l, 'LEDGER_TOKEN') for r, n, l in pairs], markers, names['reference'])
    N = cmp.Side(TN, SN, [(n, l, 'LEDGER_TOKEN') for r, n, l in pairs], markers, names['new'])
    if False in (derived['reference']['sidecar_identity_sha256_verified'], derived['new']['sidecar_identity_sha256_verified']):
        flag(SIDECAR_IDENTITY_REL, 'SIDECAR_IDENTITY_DIGEST_NOT_VERIFIED')
    # ---- declared rules R1, R2, R4, R6, F3 scalars (per canonical file); R3 inside the request admission; R5 below
    pair_rule = lambda path, pairs_, why: {'path': path, 'rule': 'PAIR', 'pairs': pairs_, 'why': why}
    cw = [(SERIAL_N, PARALLEL_N)]
    file_rules = {
        'inputs/call_spec.json': [pair_rule(LEAF, cw, 'R1 the one spec leaf (pinned specs)')],
        'start.json': [pair_rule(('normalized_spec',) + LEAF, cw, 'R1')],
        'stages/route_a/attempt_000/start.json': [
            {'path': ('column_workers',), 'rule': 'NEW_ONLY', 'value': PARALLEL_N, 'why': 'R4 RO1 parallel worker 869ce387 L124'},
            pair_rule(('worker_pin',), [(W_S[1], W_P[1])], 'F3 the attempt worker pin')],
        'result.json': [pair_rule(('normalized_spec',) + LEAF, cw, 'R1'),
                        pair_rule(('identity', 'route_a', 'implementation', 'column_workers'), cw, 'R2 driver L2864-2866'),
                        pair_rule(('identity', 'route_a', 'implementation', 'kind'), [IMPL_KIND], 'R2 driver L2869-2871'),
                        pair_rule(('route_a_outcome', 'ro1', 'worker_sha256'), [(W_S[1], W_P[1])], 'F3 RO1 worker'),
                        pair_rule(('identity', 'route_a', 'outcome', 'ro1', 'worker_sha256'), [(W_S[1], W_P[1])], 'F3 RO1 worker')],
    }
    sidecar_rule = [{'path': ('diagnostics',), 'rule': 'MASK', 'why': 'R6 controller L494-506 (payload is the identity)'}]
    r5_new = {}
    rules_applied, n_equal, n_semantic, by_entry, r5_seen = [], 0, 0, {}, None
    stage_logs, n_log_sets = {}, 0                    # c3v003 D3: canonical log path -> evidence (both shas)
    for rel in both:
        p, q = inv_r[rel], inv_n[rel]
        e = decl_rel.get(rel)
        if e is None:
            if SR.sha[str(p)] == SN.sha[str(q)]:
                n_equal += 1
                if STAGE_LOG_RE.fullmatch(rel):
                    stage_logs[rel] = {'serial_sha256': SR.sha[str(p)], 'parallel_sha256': SN.sha[str(q)], 'bytes_equal': True}
            elif STAGE_LOG_RE.fullmatch(rel):                  # c3v003 D3: a log, not a result
                ls, ns = log_lines(R, SR, p)
                lp, np_ = log_lines(N, SN, q)
                same = ls is not None and lp is not None and ls == lp
                stage_logs[rel] = {'serial_sha256': SR.sha[str(p)], 'parallel_sha256': SN.sha[str(q)], 'bytes_equal': False,
                                   'lines': [ns, np_], 'distinct_lines': [len(ls or ()), len(lp or ())],
                                   'distinct_lines_on_one_side_only': [len((ls or set()) - (lp or set())), len((lp or set()) - (ls or set()))],
                                   'distinct_line_sets_equal': same}
                if same:
                    n_log_sets += 1
                else:
                    flag(rel, 'STAGE_LOG_DISTINCT_LINES_DIFFER')
            else:
                flag(rel, 'UNDECLARED_BYTE_DIFFERENCE')
            continue
        n_semantic += 1
        by_entry[e[0]] = by_entry.get(e[0], 0) + 1
        suf = Path(rel).suffix
        det = None
        if rel == IDENTITY_REL:
            ok, det = compare_identity(cmp, cm, R, N, SR, SN, p, q, rel, cust)
        elif ITER_RE.fullmatch(rel):
            x, y, mr_, mn_ = cmp.pair_norm(R, N, SR.json(p), SN.json(q), rel, cmp.RECORD_DROP)
            mok, _ = cmp.mask_cmp(mr_, mn_, rel)
            ok = cmp.seq(x, y) and mok
            det = None if ok else {'differing': cmp.diffs(x, y)[:3]}
        elif suf == '.jsonl':
            ok, det = (cmp.compare_jsonl(rel, p, q, R, N, extra_mask=('elapsed',)) if rel == 'progress.jsonl'
                       else cmp.compare_jsonl(rel, p, q, R, N))
        elif suf == '.json':
            rules = list(file_rules.get(rel, [])) + (sidecar_rule if SIDECAR_ITER_RE.fullmatch(rel) else [])
            if rel == 'start.json':
                r5_new = {N.s(str(pp), '<R5 key>'): N.s(ss, '<R5 value>') for pp, ss in PAR_PINS}
            ok, det, rep, notes = compare_declared_json(
                cmp, R, N, SR.json(p), SN.json(q), rel, cust, rules, r5_new if rel == 'start.json' else {},
                request=(rel == 'stages/route_a/request.json'), stage_records=(rel == 'result.json'))
            if rep:
                rules_applied.append({'file': rel, 'rules': _sanitize(rep)})
            if rel == 'start.json':
                r5_seen = sorted(k for nt in notes for k in nt.get('declared_new_only', []))
                if r5_seen != sorted(r5_new):
                    ok = False
                    det = dict(det or {}, r5='the parallel-only static pins are not exactly the PARALLEL_ROUTE_A entries')
        else:
            ok, det = False, 'DECLARED_ENTRY_FOR_A_NON_JSON_FILE'
        if not ok:
            flag(rel, 'NOT_EQUAL_AFTER_DECLARED_NORMALIZATION')
            why_out[rel] = {'why': 'NOT_EQUAL_AFTER_DECLARED_NORMALIZATION', 'detail': _sanitize(det)}
    _refuse_parse_problems(SR, SN)
    # attempt ledger content (paired by order; RECORD_DROP + masks, as the comparator)
    for d in sorted(set(led_r) & set(led_n)):
        tr_, tn_ = sorted(led_r[d].items()), sorted(led_n[d].items())
        if len(tr_) != len(tn_):
            continue
        for (ta, ka), (tb, kb) in zip(tr_, tn_):
            if set(ka) != set(kb):
                flag('%s/<attempt ledger>' % d, 'ATTEMPT_LEDGER_KINDS')
                continue
            for k in sorted(ka):
                rel = '%s/<attempt>.%s.json' % (d, k)
                x, y, mr_, mn_ = cmp.pair_norm(R, N, SR.json(ka[k]), SN.json(kb[k]), rel, cmp.RECORD_DROP)
                mok, _ = cmp.mask_cmp(mr_, mn_, rel)
                if not cmp.seq(x, y) or not mok:
                    flag(rel, 'ATTEMPT_LEDGER_RECORD')
    # declared classes: a class may fire only in a file whose entry allows it (+ the I4 delta)
    led_rels = {'%s/<attempt>.%s.json' % (d, k) for d in set(led_r) | set(led_n) for k in ('start', 'end')}
    cls_viol = []
    for S in (R, N):
        for rel, fired in sorted(S.fired.items()):
            allow = set(cmp.LEDGER_CLASSES) if rel in led_rels else (allowed_cls.get(decl_rel[rel][0]) if rel in decl_rel else None)
            if allow is None or fired - allow:
                cls_viol.append({'side': S.store.tag, 'file': rel, 'classes_not_allowed': sorted(fired - (allow or set()))})
                flag(rel, 'NORMALIZATION_CLASS_NOT_DECLARED_FOR_THIS_FILE')
    # cross-run references (a file of one run naming the other run's root on a path boundary; c3v003 D2)
    xref_ev = {'rule': XREF_RULE}
    for tag, T, S in (('serial', TR, SR), ('parallel', TN, SN)):
        on_b, sub_only = [], []
        for k, (sub, bnd) in sorted(xref[S.tag].items()):
            c = T.canon(os.path.relpath(k, str(T.run)))
            if bnd:
                flag(c, 'NAMES_THE_OTHER_RUN_ROOT')
                on_b.append(c)
            else:
                sub_only.append(c)
        xref_ev[tag] = {'files_naming_the_other_root_on_a_boundary': sorted(on_b)[:200], 'n_on_a_boundary': len(on_b),
                        'files_with_a_substring_hit_only_not_a_reference': sorted(sub_only)[:200], 'n_substring_only': len(sub_only)}
    # ---- integrity (refusals, not differences)
    _refuse_parse_problems(SR, SN)
    for S in (SR, SN):
        if S.surface:
            raise Refused('PARSE_SURFACE', str(S.surface[:2])[:300])
    if R.collisions or N.collisions or R.roundtrip_bad or N.roundtrip_bad:
        raise Refused('NORMALIZATION_NOT_INJECTIVE', str((R.collisions + N.collisions + R.roundtrip_bad + N.roundtrip_bad)[:2])[:300])
    if cmp.LAST_WINS:
        raise Refused('A71_LAST_WINS', str(cmp.LAST_WINS[:2])[:300])
    # ---- custody checks (explicit; bitwise_equal needs every one)
    q_s, q_p = SR.json(inv_r['stages/route_a/request.json']), SN.json(inv_n['stages/route_a/request.json'])
    am_s, am_p = cmp.argv_map(q_s.get('argv') or [], 'serial route_a'), cmp.argv_map(q_p.get('argv') or [], 'parallel route_a')
    ast_s = SR.json(inv_r['stages/route_a/attempt_000/start.json'])
    ast_p = SN.json(inv_n['stages/route_a/attempt_000/start.json'])
    try:
        id_s = cmp.cm_read(cm, SR, inv_r[IDENTITY_REL], 'identity')
        id_p = cmp.cm_read(cm, SN, inv_n[IDENTITY_REL], 'identity')
    except cm.CheckpointError:
        id_s = id_p = {}
    impl_s = _get(rs_s, ('identity', 'route_a', 'implementation')) or {}
    impl_p = _get(rs_p, ('identity', 'route_a', 'implementation')) or {}
    pin = lambda x: {'path': str(x[0]), 'sha256': x[1]}
    ro1_ok_s = ro1_armed_side_pins(cmp, cmp.ro1_block(rs_s), W_S[1], BINDING[1])      # c3v003 D1
    ro1_ok_p = ro1_armed_side_pins(cmp, cmp.ro1_block(rs_p), W_P[1], BINDING[1])
    sp_s = st_s.get('static_pins') if isinstance(st_s.get('static_pins'), dict) else {}
    sp_p = st_p.get('static_pins') if isinstance(st_p.get('static_pins'), dict) else {}
    num_c2t = (((cb.get('cases') or {}).get('C2T') or {}).get('normalized_spec_equal') or {}).get('/numerics')
    num_s, num_p = _get(rs_s, ('normalized_spec', 'numerics')), _get(rs_p, ('normalized_spec', 'numerics'))
    checks = {
        'C1_route_a_worker_is_the_driver_planned_one': ([q_s.get('script'), q_s.get('script_sha256')] == [str(W_S[0]), W_S[1]]
                                                       and [q_p.get('script'), q_p.get('script_sha256')] == [str(W_P[0]), W_P[1]]),
        'C2_route_a_solver_is_the_driver_planned_one': ([am_s.get('--solver'), am_s.get('--solver-sha256')] == [str(S_S[0]), S_S[1]]
                                                       and [am_p.get('--solver'), am_p.get('--solver-sha256')] == [str(S_P[0]), S_P[1]]),
        'C3_argv_column_workers_serial_absent_parallel_8': strip_column_workers(q_s.get('argv'), q_p.get('argv'))[0],
        'C4_implementation_records': (impl_s == {'column_workers': SERIAL_N, 'kind': IMPL_KIND[0], 'worker': pin(W_S), 'solver': pin(S_S)}
                                      and impl_p == {'column_workers': PARALLEL_N, 'kind': IMPL_KIND[1], 'worker': pin(W_P), 'solver': pin(S_P)}),
        'C5_solver_code_in_custody_and_checkpoint_identity': (
            _get(rs_s, ('identity', 'route_a', 'custody', 'solver_code')) == pin(S_S) == _get(id_s, ('identity', 'code', 'solver'))
            and _get(rs_p, ('identity', 'route_a', 'custody', 'solver_code')) == pin(S_P) == _get(id_p, ('identity', 'code', 'solver'))),
        'C6_ro1_rule_armed_key_set_and_the_side_worker_and_binding': bool(ro1_ok_s and ro1_ok_p),
        'C7_attempt_start_worker_pin_and_column_workers': (isinstance(ast_s, dict) and isinstance(ast_p, dict)
                                                           and ast_s.get('worker_pin') == W_S[1] and ast_p.get('worker_pin') == W_P[1]
                                                           and 'column_workers' not in ast_s and ast_p.get('column_workers') == PARALLEL_N),
        'C8_parallel_only_static_pins_are_exactly_PARALLEL_ROUTE_A': (
            sorted((k, v) for k, v in sp_p.items() if k not in sp_s) == sorted((str(p_), s_) for p_, s_ in PAR_PINS)
            and not [k for k in sp_s if k not in sp_p] and all(sp_s[k] == sp_p[k] for k in sp_s)),
        'C9_normalized_column_workers_1_and_8': (
            _get(st_s, ('normalized_spec',) + LEAF) == SERIAL_N and _get(rs_s, ('normalized_spec',) + LEAF) == SERIAL_N
            and _get(st_p, ('normalized_spec',) + LEAF) == PARALLEL_N and _get(rs_p, ('normalized_spec',) + LEAF) == PARALLEL_N
            and _get(cs_s, LEAF) == SERIAL_N and _get(cs_p, LEAF) == PARALLEL_N),
        'C10_run_numerics_are_the_case_block_C2T_numerics_up_to_the_leaf': bool(
            isinstance(num_c2t, dict) and json.dumps(num_p, sort_keys=True) == json.dumps(num_c2t, sort_keys=True)
            and leaf_diff(num_c2t, num_s) == [('/'.join(LEAF[1:]), [PARALLEL_N, SERIAL_N])]),
        'C11_stage_directories_identical_by_number_and_name': TR.order == TN.order and TR.name2dir == TN.name2dir,
    }
    if not checks['C11_stage_directories_identical_by_number_and_name']:
        flag('stages/<stage directory order>', 'STAGE_ORDER_OR_NUMBERING_DIFFERS')
    # ---- tail ON (both runs' configs)
    def tail_on(cs, st, rs, a_st):
        return bool(_get(cs, ('numerics', 'uv_tail', 'enabled')) is True
                    and _get(st, ('normalized_spec', 'numerics', 'uv_tail', 'enabled')) is True
                    and _get(rs, ('normalized_spec', 'numerics', 'uv_tail', 'enabled')) is True
                    and _get(rs, ('uv_tail', 'enabled')) is True and _get(a_st, ('uv_tail', 'enabled')) is True)
    tail_detail = {'serial': tail_on(cs_s, st_s, rs_s, ast_s), 'parallel': tail_on(cs_p, st_p, rs_p, ast_p),
                   'rule': 'inputs/call_spec.json numerics.uv_tail.enabled, start.json and result.json normalized_spec.numerics.uv_tail'
                           '.enabled, result.json uv_tail.enabled and the route-A attempt start.json uv_tail.enabled are all true'}
    tail = 'ON' if tail_detail['serial'] and tail_detail['parallel'] else 'OFF'
    # ---- V8c-F1 from bytes (the parallel run's solver)
    used = {'request_argv': [am_p.get('--solver'), am_p.get('--solver-sha256')],
            'implementation_solver': impl_p.get('solver'),
            'custody_solver_code': _get(rs_p, ('identity', 'route_a', 'custody', 'solver_code')),
            'checkpoint_identity_code_solver': _get(id_p, ('identity', 'code', 'solver'))}
    same_solver = (used['request_argv'] == [str(S_P[0]), S_P[1]] and used['implementation_solver'] == pin(S_P)
                   and used['custody_solver_code'] == pin(S_P) and used['checkpoint_identity_code_solver'] == pin(S_P))
    try:
        sol_raw = Path(S_P[0]).read_bytes()
    except OSError:
        sol_raw = b''
    site_ok, site = v8c_f1_site(sol_raw) if sha_b(sol_raw) == S_P[1] else (False, {'why': 'solver bytes are not the driver pin'})
    v8c = bool(same_solver and site_ok)
    # ---- the driver every T-case registers (the g_I4 clause, checked here too)
    drv_reg = all(DRIVER[1] in ((cb.get('cases') or {}).get(c) or {}).get('drivers_allowed', []) for c in T_CASES)
    # ---- integrity at the end: every recorded file re-hashed
    unstable = SR.unstable + SN.unstable + SR.verify() + SN.verify()
    if unstable:
        raise Refused('TREE_CHANGED_DURING_COMPARISON', str(unstable[:2])[:300])
    if sha_f(me) != me_sha:
        raise Refused('PRODUCER_CHANGED_DURING_RUN')
    diff_list = sorted(outside)
    custody_ok = all(v is True for v in checks.values())
    bitwise = bool((not diff_list) and custody_ok)
    fails = []
    if tail != 'ON':
        fails.append('I4_TAIL_NOT_ON')
    if not drv_reg:
        fails.append('I4_DRIVER_NOT_REGISTERED_FOR_EVERY_T_CASE')
    if not v8c:
        fails.append('I4_V8C_F1_FIX_NOT_CONFIRMED')
    if not bitwise:
        fails.append('I4_SERIAL_PARALLEL_NOT_BITWISE_EQUAL')
    if diff_list:
        fails.append('I4_DIFFERENCES_OUTSIDE_CUSTODY')
    rec = {
        'schema': SCHEMA, 'gate': GATE,
        'producer': {'path': str(me), 'sha256': me_sha},
        'verdict': PASS_VERDICT if not fails else FAIL_VERDICT,
        'tail': tail,
        'driver_sha256': DRIVER[1],
        'serial_result_sha256': runs['serial']['result']['sha256'],
        'parallel_result_sha256': runs['parallel']['result']['sha256'],
        'v8c_f1_fix_confirmed': v8c,
        'bitwise_equal': bitwise,
        'differences_outside_custody': diff_list,
        'failing_clauses': fails,
        'result_record_definition': ('serial_result_sha256 / parallel_result_sha256 = sha256 of the bytes of <run dir>/result.json, '
                                     'equal to <run dir>/finish.json result_sha256 and to <run dir>.receipt.json result.sha256 (checked)'),
        'runs': runs,
        'specs': {'n1_serial': {'path': N1_SPEC[0], 'sha256': N1_SPEC[1]}, 'n8_parallel': {'path': N8_SPEC[0], 'sha256': N8_SPEC[1]},
                  'spec_registry': {'path': SPEC_REGISTRY[0], 'sha256': SPEC_REGISTRY[1], 'case': 'C2T'},
                  'one_leaf': '/' + '/'.join(LEAF), 'values': {'serial': SERIAL_N, 'parallel': PARALLEL_N}},
        'custody': {
            'comparator': {'path': COMPARATOR[0], 'sha256': COMPARATOR[1], 'use': 'loaded inert from verified bytes; its machinery and declared list'},
            'driver': {'path': DRIVER[0], 'sha256': DRIVER[1], 'tables_read_by_restricted_ast': sorted(tables)},
            'checkpoint_module': {'path': cmp.CKPT[0], 'sha256': cmp.CKPT[1]},
            'case_block': {'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]},
            'route_a_pairs': {'worker': {'serial': pin(W_S), 'parallel': pin(W_P)}, 'solver': {'serial': pin(S_S), 'parallel': pin(S_P)},
                              'admitted_as': 'F1 pin-dict entry (one member per side), F2 {path, sha256} pin object, F3 declared scalar positions'},
            'ledger_tokens': [{'serial': t[0], 'parallel': t[1], 'label': t[2]} for t in led_tokens],
            'declared_entries': [e[0] for e in entries], 'i4_entries': [list(x) for x in I4_ENTRIES],
            'i4_class_delta': {k: list(v) for k, v in I4_CLASS_DELTA.items()},
            'masked_keys': sorted(cmp.MASK_KEYS), 'record_drop': sorted(cmp.RECORD_DROP),
            'rules': ['R1 spec leaf PAIR', 'R2 implementation column_workers / kind PAIR', 'R3 argv --column-workers 8 after --start-iteration 0',
                      'R4 attempt start column_workers NEW_ONLY 8', 'R5 parallel-only static pins = PARALLEL_ROUTE_A, bytes verified',
                      'R6 tail-ON both-side files I01-I06 (sidecar identity digest verified; sidecar diagnostics MASK)',
                      'R7 timing keys build_seconds / begin_seconds / complete_seconds masked', 'R8 IDENTITY digests verified, caller decoded'],
            'parallel_route_a_static_pins': [pin(x) for x in PAR_PINS]},
        'comparison': {'files': [len(TR.files), len(TN.files)], 'both_sides': len(both), 'equal_bytes_undeclared': n_equal,
                       'declared_compared_semantically': n_semantic, 'declared_by_entry': dict(sorted(by_entry.items())),
                       'stage_logs_equal_as_distinct_line_sets': n_log_sets,
                       'stage_logs': {'rule': STAGE_LOG_RULE, 'files': dict(sorted(stage_logs.items()))},
                       'cross_run_root_references': xref_ev,
                       'custody_admissions_by_file': dict(sorted(cust.count.items())),
                       'r5_parallel_only_static_pins_seen': r5_seen,
                       'classes_fired': ({'serial': {k: sorted(v) for k, v in sorted(R.fired.items())},
                                          'parallel': {k: sorted(v) for k, v in sorted(N.fired.items())}}
                                         if len(R.fired) + len(N.fired) < 600 else 'omitted (large)'),
                       'class_violations': cls_viol[:40], 'rules_applied': rules_applied[:40],
                       'outside_custody_reasons': {k: why_out[k] for k in diff_list[:200]},
                       'derived_digests': derived},
        'checks': checks,
        'tail_detail': tail_detail,
        'v8c_f1': {'source': {'path': V8C_REVIEW[0], 'sha256': V8C_REVIEW[1], 'fragments': list(V8C_FRAGMENTS)},
                   'driver_solver_parallel': pin(S_P), 'parallel_run_solver': used, 'same_solver_everywhere': same_solver,
                   'site': site, 'confirmed': v8c},
        'driver_registered_for_every_T_case': drv_reg,
        'scope': ('Computed by the producer from the two trees\' bytes; it reads no target velocity, and difference details record '
                  'paths only (no row or other run value). '
                  'Not a compare verdict: compare r14 evaluate_gate reads this record (I4 is PRODUCED_AFTER_THE_SEAL).'),
    }
    data = (json.dumps(rec, indent=1, sort_keys=False, allow_nan=False) + '\n').encode('utf-8')
    with open(out, 'xb') as f:
        f.write(data)
    return rec, sha_b(data)


def compare_identity(cmp, cm, R, N, SR, SN, p, q, rel, cust):
    """R8: the comparator's RA_IDENTITY body comparison: digests verified per side, caller decoded, whole identity compared, with the
    route-A custody admission (F1 F2) and no new-only pin."""
    try:
        br = cmp.cm_read(cm, SR, p, 'identity')
        bn = cmp.cm_read(cm, SN, q, 'identity')
        dig = {}
        for tag, body in (('serial', br), ('parallel', bn)):
            ident, caller = body['identity'], body['identity'].get('caller') or {}
            dig[tag] = bool(isinstance(body.get('identity_sha256'), str) and cm._sha(cm._canonical(ident)) == body['identity_sha256']
                            and isinstance(caller.get('sha256'), str) and caller['sha256'] == cm.digest(cm.decode(caller['record']))
                            and set(body) <= {'format', 'identity', 'identity_sha256', 'kind', 'payload_sha256'}
                            and set(caller) <= {'record', 'sha256'})
        x0 = dict(br['identity'], caller=cm.decode(br['identity']['caller']['record']))
        y0 = dict(bn['identity'], caller=cm.decode(bn['identity']['caller']['record']))
    except (cm.CheckpointError, KeyError, TypeError, ValueError) as exc:
        return False, 'IDENTITY unreadable: %s' % type(exc).__name__
    ok, det, _, _ = compare_declared_json(cmp, R, N, x0, y0, rel, cust)
    ok = ok and all(dig.values())
    return ok, (None if ok else dict(det or {}, digests_verified=dig))


STRICT_FLAGS = ('--serial', '--parallel', '--out')


def parse_cli(argv):
    seen, out, i = {}, {}, 0
    while i < len(argv):
        f = argv[i]
        if f not in STRICT_FLAGS:
            raise Refused('CLI', 'argument %d is not one of %s (no abbreviation, no --flag=value)' % (i, list(STRICT_FLAGS)))
        if f in seen:
            raise Refused('CLI', 'flag %s given twice' % f)
        if i + 1 >= len(argv) or argv[i + 1].startswith('--'):
            raise Refused('CLI', 'flag %s has no value' % f)
        seen[f] = i
        out[f] = argv[i + 1]
        i += 2
    miss = [f for f in STRICT_FLAGS if f not in out]
    if miss:
        raise Refused('CLI', 'missing %s' % miss)
    return out


def main(argv=None):
    try:
        a = parse_cli(list(sys.argv[1:] if argv is None else argv))
        rec, sh = produce(a['--serial'], a['--parallel'], a['--out'])
    except Refused as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps({'out': a['--out'], 'sha256': sh, 'verdict': rec['verdict'], 'tail': rec['tail'],
                      'bitwise_equal': rec['bitwise_equal'], 'v8c_f1_fix_confirmed': rec['v8c_f1_fix_confirmed'],
                      'n_differences_outside_custody': len(rec['differences_outside_custody'])}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
