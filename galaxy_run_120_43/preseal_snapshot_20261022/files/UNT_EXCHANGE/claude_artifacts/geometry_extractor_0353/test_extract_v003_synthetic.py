"""0353 synthetic test harness for extract_sparc_geometry_metadata_v003.py. SYNTHETIC DATA ROWS ONLY.

The extractor is NEVER run on the real MRT. End-to-end cases run scratch COPIES of the extractor whose PINS block is
replaced to point at synthetic sources (and, for publication cases, with clearly marked TEST-ONLY injections before
`def candidate_path`, as in the 0348 harness). Synthetic MRT = the real header lines 1-98 (documentation bytes, sliced up
to the 98th LF; no real data row is sliced) + synthetic data rows. The real CDS ReadMe (documentation) is referenced
read-only, or a modified scratch copy for CDS failure cases. The manifest is always synthetic.
Real-documentation preflight (booleans only): real MRT sha == pin (hash only), verify_header() on the real header lines
1-98, verify_cds() on the real ReadMe, real manifest sha == pin (hash only).
Nothing is deleted, moved or overwritten: every case writes into its own new directory under the new run directory.
Usage: python3 -I test_extract_v003_synthetic.py <extractor.py> <fixtures_0349.json> <results_0349.json>
       <audit_correction_0349.json> <new_run_dir> <new_receipt.json>
"""
import hashlib, importlib.util, json, os, re, stat, subprocess, sys
from pathlib import Path

EXT, FIX0349, RES0349, CORR0349, RUN, RECEIPT = [Path(x) for x in sys.argv[1:7]]
RUN.mkdir(parents=True, exist_ok=False)
REAL_MRT = '/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt'
REAL_CDS = '/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001/SPARC_ReadMe.html'
REAL_MAN = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json'
OUTNAME = 'SPARC_ALLOWED_GEOMETRY_METADATA_CANDIDATE_V002.json'


def sha(b):
    return hashlib.sha256(b).hexdigest()


spec = importlib.util.spec_from_file_location('v003', str(EXT))
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)
SRC_TEXT = EXT.read_text()
RES = []


def case(group, name, ok, detail=''):
    RES.append({'group': group, 'case': name, 'pass': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + group + ' ' + name + (' | ' + detail if detail else ''))


# ------------------------------------------------------------------ real documentation (header bytes only)
_b = open(REAL_MRT, 'rb').read()
REAL_SHA_OK = sha(_b) == X.SRC[1]
_pos = 0
for _ in range(98):
    _pos = _b.find(b'\n', _pos) + 1
REAL_HEADER = _b[0:_pos]          # lines 1-98 only; no data row is sliced
del _b
try:
    _note2 = X.verify_header(REAL_HEADER.split(b'\n')[:98]); hdr_ok = len(_note2) == 5
except X.Fail as e:
    hdr_ok = False
_saved_cds = X.CDS_README
try:
    X.verify_cds(); cds_ok = True
except X.Fail:
    cds_ok = False
case('R0', 'real MRT sha equals pin (hash only)', REAL_SHA_OK)
case('R0', 'real header lines 1-98 pass verify_header (order, formats, units, explanations, Notes 1-2, separator 98)', hdr_ok)
case('R0', 'real CDS ReadMe passes verify_cds (pin, lines 148-155, no ? in 144-216, Note 3)', cds_ok)
case('R0', 'real manifest sha equals pin (hash only; not parsed)', sha(open(REAL_MAN, 'rb').read()) == X.MANIFEST[1])

# ------------------------------------------------------------------ synthetic rows
TAIL = ' ' + '1.234'.rjust(7) + ' ' + '0.123'.rjust(7) + ' ' + '1.23'.rjust(5) + ' ' + '123.45'.rjust(8) + ' ' + \
       '2.34'.rjust(5) + ' ' + '456.78'.rjust(8) + ' ' + '1.234'.rjust(7) + ' ' + '12.34'.rjust(5) + ' ' + \
       '99.9'.rjust(5) + ' ' + '4.5'.rjust(5) + ' ' + '1'.rjust(3) + ' ' + 'Zz00'.ljust(14)


def hp1(name, T, D, eD, fD, Inc, eInc, tail=TAIL):
    return (name.rjust(11) + ' ' + T.rjust(2) + ' ' + D.rjust(6) + ' ' + eD.rjust(5) + ' ' + fD.rjust(2) + ' ' +
            Inc.rjust(4) + ' ' + eInc.rjust(4) + tail).encode('ascii')


NG = dict(T='4', D='42.42', eD='3.33', fD='1', Inc='66.6', eInc='7.7')      # SYNTHETIC values
DD = dict(T='10', D='7.77', eD='0.88', fD='2', Inc='55.5', eInc='4.4')      # SYNTHETIC values
LITERALS = ['42.42', '3.33', '66.6', '7.7', '7.77', '0.88', '55.5', '4.4']
ANCHOR = '42.420'   # float-equal to NGC3198 synthetic D, textually different, so its absence from outputs is testable


def filler(i):
    return hp1('SYNF%03d' % i, '3', '%d.%02d' % (10 + i, i), '1.%02d' % i, '3', '%d.0' % (40 + i), '%d.0' % (2 + i % 5))


def rows(ngc=None, ddo=None, extra=None):
    """Data rows: fillers 1-3, NGC3198, fillers 4-6, DDO154, fillers 7-9 (lines 99..109)."""
    r = [filler(1), filler(2), filler(3), ngc if ngc is not None else hp1('NGC3198', **NG),
         filler(4), filler(5), filler(6), ddo if ddo is not None else hp1('DDO154', **DD), filler(7), filler(8), filler(9)]
    if extra:
        r = extra(r)
    return r


BASE_LINES = {'NGC3198': 102, 'DDO154': 106}


def build(tag, data=None, header=None, manifest=None, cds=None, inject=None, pins=None):
    d = RUN / tag
    d.mkdir()
    mrt = (header if header is not None else REAL_HEADER) + b'\n'.join(data if data is not None else rows()) + b'\n'
    (d / 'synthetic.mrt').write_bytes(mrt)
    man = manifest if manifest is not None else json.dumps(
        {'schema': 'SYNTHETIC', 'crosscheck_massmodels': {'reference_distance_texts': [ANCHOR], 'note': 'SYNTHETIC'}}).encode()
    (d / 'synthetic_manifest.json').write_bytes(man)
    if cds is not None:
        (d / 'cds_copy.html').write_bytes(cds)
        cds_pin = (str(d / 'cds_copy.html'), sha(cds))
    else:
        cds_pin = (REAL_CDS, X.CDS_README[1])
    p = pins or {}
    block = ("# ---- PINS (TEST COPY: synthetic sources) ----\n"
             "SRC=(%r,%r)\nCDS_README=(%r,%r)\nMANIFEST=(%r,%r)\n# ---- END PINS ----" % (
                 str(d / 'synthetic.mrt'), p.get('src', sha(mrt)), cds_pin[0], p.get('cds', cds_pin[1]),
                 str(d / 'synthetic_manifest.json'), p.get('man', sha(man))))
    s = re.sub(r'# ---- PINS .*?# ---- END PINS ----', lambda m: block, SRC_TEXT, count=1, flags=re.S)
    assert s != SRC_TEXT and s.count('TEST COPY') == 1
    if inject:
        anchor = 'def candidate_path(outp):'
        assert s.count(anchor) == 1
        s = s.replace(anchor, '# ---- TEST-ONLY INJECTION ----\n' + inject + '\n# ---- END TEST-ONLY ----\n' + anchor, 1)
    (d / 'extractor_copy.py').write_text(s)
    (d / 'out').mkdir()
    return d


def run(d, name=OUTNAME, args=None):
    a = args if args is not None else [str(d / 'out' / name)]
    r = subprocess.run([sys.executable, '-I', '-B', str(d / 'extractor_copy.py')] + a, capture_output=True, text=True, cwd=str(d))
    try:
        j = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        j = {'unparsed_stdout': r.stdout[-300:], 'stderr': r.stderr[-300:]}
    return r.returncode, j, r.stdout


def no_literals(text):
    return not any(l in text for l in LITERALS) and ANCHOR not in text


def out_files(d):
    return sorted(x.name for x in (d / 'out').iterdir())


def only_bools(o):
    if isinstance(o, dict):
        return all(only_bools(v) for v in o.values())
    return o is None or isinstance(o, bool)


# ------------------------------------------------------------------ G1 success path
d = build('G1_success')
rc, j, so = run(d)
o = d / 'out' / OUTNAME
c = d / 'out' / (OUTNAME + '.candidate')
ok = rc == 0 and o.exists() and c.exists() and os.path.samefile(o, c)
case('G1', 'exit 0; candidate and output exist and are the same file', ok, 'rc=%s' % rc)
OUT = json.loads(o.read_bytes()) if ok else {}
mode = stat.S_IMODE(os.stat(c).st_mode) if ok else 0o777
case('G1', 'no write bits on the published file; reported mode equals actual', ok and mode & 0o222 == 0 and j['candidate']['mode'] == oct(mode))
case('G1', 'stdout carries no literal and no anchor text', no_literals(so))
case('G1', 'output does not contain the anchor text', ANCHOR.encode() not in o.read_bytes() if ok else False)
objs = OUT.get('objects', {})
case('G1', 'exactly the two frozen rows', sorted(objs) == ['DDO154', 'NGC3198'])
case('G1', 'exactly the five emitted fields per row; T and Galaxy listed as validated_not_emitted',
     all(sorted(objs[t]['fields']) == sorted(['D', 'e_D', 'f_D', 'Inc', 'e_Inc']) and objs[t]['validated_not_emitted'] == ['Galaxy', 'T'] for t in objs))
exp = {'NGC3198': {'D': ('42.42', [17, 21]), 'e_D': ('3.33', [24, 27]), 'f_D': ('1', [30, 30]), 'Inc': ('66.6', [32, 35]), 'e_Inc': ('7.7', [38, 40])},
       'DDO154': {'D': ('7.77', [18, 21]), 'e_D': ('0.88', [24, 27]), 'f_D': ('2', [30, 30]), 'Inc': ('55.5', [32, 35]), 'e_Inc': ('4.4', [38, 40])}}
case('G1', 'literal token strings and 1-based byte spans exact',
     all(objs[t]['fields'][f]['literal'] == v[0] and objs[t]['fields'][f]['byte_span'] == v[1] for t in exp for f, v in exp[t].items()))
case('G1', 'exact source line numbers', all(objs[t]['source_line_number'] == BASE_LINES[t] for t in objs))
case('G1', 'f_D code meaning taken from header Note (2)',
     objs['NGC3198']['fields']['f_D']['code_meaning'] == 'Hubble-Flow assuming H0=73 km/s/Mpc and correcting for Virgo-centric infall'
     and objs['DDO154']['fields']['f_D']['code_meaning'] == 'Magnitude of the Tip of the Red Giant Branch')
case('G1', 'documented units and semantics (Inc = outer-HI-disk mean per CDS Note 3; e_* catalogue mean errors, no Gaussian)',
     objs['NGC3198']['fields']['D']['units'] == 'Mpc' and objs['NGC3198']['fields']['Inc']['units'] == 'deg'
     and 'outer parts of the HI disk' in objs['NGC3198']['fields']['Inc']['kind']
     and 'not a Gaussian' in objs['DDO154']['fields']['e_D']['kind'] and 'no joint region' in objs['DDO154']['fields']['e_Inc']['kind'])
case('G1', 'declared assumptions A1, A1b, A2, A3 present and not discharged; A1b by token-2 width only',
     sorted(OUT.get('assumptions_declared_not_discharged', {})) == ['A1', 'A1b', 'A2', 'A3']
     and objs['NGC3198']['assumptions'] == {'A1': 'CLOSED_FOR_THIS_ROW_BY_C10_ANCHOR', 'A1b': 'DECLARED_NOT_DISCHARGED', 'A2': 'DECLARED_NOT_DISCHARGED', 'A3': 'DECLARED_NOT_DISCHARGED'}
     and objs['DDO154']['assumptions'] == {'A1': 'DECLARED_NOT_DISCHARGED', 'A1b': 'EXCLUDED_BY_BYTES_TOKEN2_TWO_DIGITS', 'A2': 'DECLARED_NOT_DISCHARGED', 'A3': 'DECLARED_NOT_DISCHARGED'})
case('G1', 'all check booleans true; C10 evaluated for NGC3198 only',
     all(v is True for t in objs for v in objs[t]['checks'].values()) and 'C10_anchor_token3_equal' in objs['NGC3198']['checks']
     and 'C10_anchor_token3_equal' not in objs['DDO154']['checks'])


def numbers(o, k=None, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        for kk, v in o.items():
            numbers(v, kk, acc)
    elif isinstance(o, list):
        for v in o:
            numbers(v, k, acc)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        acc.append((k, type(o).__name__))
    return acc


nums = numbers(OUT)
case('G1', 'no float anywhere in the output; integers only under byte_span, source_line_number, bytes, data_lines_from',
     all(t == 'int' and k in ('byte_span', 'source_line_number', 'bytes', 'data_lines_from') for k, t in nums), str(sorted(set(nums))))
case('G1', 'K1-K6 recorded and V001 quarantine untouched statement present',
     sorted(OUT.get('corrections_bound', {})) == ['K1', 'K2', 'K3', 'K4', 'K5', 'K6'] and 'quarantined V001' in OUT.get('nature', ''))
case('G1', 'output carries the corrected exact exposure statement and the correction note',
     OUT.get('exposure') == X.EXPOSURE and OUT.get('exposure_correction') == X.EXPOSURE_CORRECTION)
BASE_OBJS = {t: {k: v for k, v in objs[t].items()} for t in objs}

# ------------------------------------------------------------------ G2 0349 fixtures through V003 check_prefix
fx = json.loads(FIX0349.read_bytes())['fixtures']
r49 = {r['id']: r for r in json.loads(RES0349.read_bytes())['part_A_fixtures']['results']}
same = 0
for f in fx:
    line = f['line'].encode('latin-1') if any(ord(ch) > 127 for ch in f['line']) else f['line'].encode('ascii')
    codes, ck, t, sp = X.check_prefix(line[:41], f['target'], f['anchor'])
    status = 'PASS' if not codes else 'FAIL'
    eq = codes == r49[f['id']]['fail_codes'] and status == r49[f['id']]['status']
    same += eq
    detail = ','.join(codes)
    if status == 'PASS' and f['truth'] is not None:
        mis = any(f['truth'].get(k) != t[k].decode('ascii') for k in t)
        detail += ' misread=%s' % mis
    case('G2', f['id'] + ' (expect %s, 0349 codes reproduced)' % f['expect'], eq and status == f['expect'] and all(x in codes for x in f['must_include']), detail)
case('G2', 'all %d 0349 fixtures give identical status and fail codes under V003' % len(fx), same == len(fx))

# ------------------------------------------------------------------ G3 reviewer R1/R2/R2c/R3
corr = json.loads(CORR0349.read_bytes())['review_evidence']['counterexample_fixtures']
RF = {k: v.split('  (')[0] for k, v in corr.items()}
def pad41(s):
    return (s.ljust(41) + TAIL).encode('ascii')
codes, ck, t, sp = X.check_prefix(pad41(RF['R1'])[:41], 'SYNTH01')
case('G3', 'R1 T<->f_D swap: full contract PASS (misread: T token reads f_D and vice versa) -> documents A1b',
     codes == [] and t['T'] == b'3' and t['f_D'] == b'5', 'codes=%s' % codes)
for k in ('R2', 'R2c', 'R3'):
    codes, ck, t, sp = X.check_prefix(pad41(RF[k])[:41], 'SYNTH01')
    case('G3', '%s fails ONLY by C9 (K2: C9 load-bearing)' % k, codes == ['E_SPAN_ENDS'], 'codes=%s' % codes)
# end to end: R1 placed in the NGC3198 row (anchor = its D token) -> exit 0 with swapped f_D, A1b declared
r1 = pad41(RF['R1'].replace('SYNTH01', 'NGC3198'))
d = build('G3_R1_e2e', data=rows(ngc=r1), manifest=json.dumps({'crosscheck_massmodels': {'reference_distance_texts': ['11.11']}}).encode())
rc, j, so = run(d)
oo = json.loads((d / 'out' / OUTNAME).read_bytes()) if rc == 0 else {}
case('G3', 'R1 end-to-end in the NGC3198 row: exit 0, f_D literal is the swapped token, A1b DECLARED (PASS-as-misread)',
     rc == 0 and oo['objects']['NGC3198']['fields']['f_D']['literal'] == '5' and oo['objects']['NGC3198']['assumptions']['A1b'] == 'DECLARED_NOT_DISCHARGED', 'rc=%s' % rc)
r2 = pad41(RF['R2'].replace('SYNTH01', 'NGC3198'))
d = build('G3_R2_e2e', data=rows(ngc=r2), manifest=json.dumps({'crosscheck_massmodels': {'reference_distance_texts': ['1.11']}}).encode())
rc, j, so = run(d)
case('G3', 'R2 end-to-end in the NGC3198 row: exit 2, code NGC3198:E_SPAN_ENDS only, no files, no literals in stdout',
     rc == 2 and j.get('codes') == ['NGC3198:E_SPAN_ENDS'] and out_files(d) == [] and '1.11' not in so and '3.33' not in so, json.dumps(j.get('codes')))

# ------------------------------------------------------------------ G4 byte boundary (K5, bytes >= 42)
HOSTILE = b' \xff\xfe\x00\t\r NGC3198 DDO154 ---------------------------------------- 99.99 nan ? 1e9 \x80'
def hostile(r):
    out = []
    for x in r:
        out.append(x[:41] + HOSTILE)          # every data row, targets included: bytes >= 42 replaced
    return out
d = build('G4_hostile_bytes_ge_42', data=rows(extra=hostile))
rc, j, so = run(d)
ho = json.loads((d / 'out' / OUTNAME).read_bytes()) if rc == 0 else {}
case('G4', 'bytes >= 42 of every data row hostile (0xFF, NUL, TAB, CR, target names, dashes, nan): exit 0 and identical objects to G1 -> never decoded/compared',
     rc == 0 and ho['objects'] == BASE_OBJS, 'rc=%s %s' % (rc, j.get('codes')))
# slice/method logging on the source buffer
LOGP = RUN / 'G4_slice_log' / 'slice_log.json'
INJ = ("import atexit as _ax\n_LOG={'slices':[],'find':[],'methods':[]}\n"
       "class _LB(bytes):\n"
       " def __getitem__(s,k):\n"
       "  _LOG['slices'].append([k.start,k.stop] if isinstance(k,slice) else [k,k+1]);return bytes.__getitem__(s,k)\n"
       " def find(s,sub,*a):\n"
       "  _LOG['find'].append([bytes(sub).decode('latin-1')]+list(a));return bytes.find(s,sub,*a)\n"
       "def _mk(n):\n"
       " def f(s,*a,**k):\n"
       "  _LOG['methods'].append(n);return getattr(bytes,n)(s,*a,**k)\n"
       " return f\n"
       "for _n in ('split','rsplit','splitlines','decode','strip','lstrip','rstrip','count','index','rfind','rindex','startswith','endswith','replace','partition','rpartition','upper','lower','join','__iter__','__contains__','hex'):setattr(_LB,_n,_mk(_n))\n"
       "_orig_read=_read\n"
       "def _read(p):\n"
       " x=_orig_read(p)\n"
       " return _LB(x) if p==SRC[0] else x\n"
       "_ax.register(lambda:open(%r,'x').write(__import__('json').dumps(_LOG)))  # TEST-ONLY" % str(LOGP))
d = build('G4_slice_log', inject=INJ)
rc, j, so = run(d)
lg = json.loads(LOGP.read_bytes()) if LOGP.exists() else {'slices': [], 'find': [], 'methods': ['NO_LOG']}
mb = (d / 'synthetic.mrt').read_bytes()
hdr_end = len(REAL_HEADER)
starts, p0 = [], hdr_end
while p0 < len(mb):
    nl = mb.find(b'\n', p0); e0 = len(mb) if nl < 0 else nl
    starts.append((p0, e0)); p0 = e0 + 1
def legal(s, e):
    if e is not None and s is not None and s == 0 and e <= hdr_end:
        return True
    for a, b_ in starts:
        if s == a:
            return e is not None and e <= min(a + 41, b_)
    return False
bad = [x for x in lg['slices'] if not legal(*x)]
case('G4', 'every slice of the source buffer is the header (lines 1-98) or bytes 1-41 of one data line (%d slices logged)' % len(lg['slices']),
     rc == 0 and lg['slices'] and not bad, 'bad=%s' % bad[:3])
case('G4', 'no whole-buffer method other than find(LF) is called on the source buffer',
     rc == 0 and lg['methods'] == [] and all(x[0] == '\n' for x in lg['find']), 'methods=%s' % lg['methods'][:5])
# K5: dash-only DATA lines are ignored by the header logic (V002 searched lines[:200])
def dashes(r):
    return r[:1] + [b'-' * 80] + r[1:3] + [b'   ' + b'-' * 60] + r[3:]
d = build('G4_dash_data_lines', data=rows(extra=dashes))
rc, j, so = run(d)
dl = json.loads((d / 'out' / OUTNAME).read_bytes()) if rc == 0 else {}
synth = (d / 'synthetic.mrt').read_bytes().split(b'\n')
v002_rule = [i for i, l in enumerate(synth[:200]) if re.fullmatch(rb'-{20,}', l.strip())][-1] + 1
case('G4', 'K5: dash-only data lines 100 and 103: header end stays line 98; targets found at their true lines (V002 rule would pick line %d)' % v002_rule,
     rc == 0 and dl['objects']['NGC3198']['source_line_number'] == 104 and dl['objects']['DDO154']['source_line_number'] == 108 and v002_rule != 98)
hb = REAL_HEADER.split(b'\n')
hb[97] = b'This line 98 is not a separator'
d = build('G4_header_line98_not_separator', header=b'\n'.join(hb))
rc, j, so = run(d)
case('G4', 'header line 98 not a separator -> exit 2 E_HEADER_STRUCTURE, no files', rc == 2 and j.get('code') == 'E_HEADER_STRUCTURE' and out_files(d) == [])
d = build('G4_short_target_row', data=rows(ngc=hp1('NGC3198', **NG)[:38]))
rc, j, so = run(d)
case('G4', 'NGC3198 row shorter than 41 bytes -> exit 2 E_SHORT_ROW + E_BYTE41_NOT_BLANK, codes/booleans only',
     rc == 2 and 'NGC3198:E_SHORT_ROW' in j.get('codes', []) and 'NGC3198:E_BYTE41_NOT_BLANK' in j.get('codes', []) and only_bools(j.get('checks')) and no_literals(so))
d = build('G4_duplicate_target', data=rows(extra=lambda r: r + [hp1('DDO154', **DD)]))
rc, j, so = run(d)
case('G4', 'duplicate DDO154 row -> exit 2 DDO154:E_ROW_NOT_UNIQUE', rc == 2 and 'DDO154:E_ROW_NOT_UNIQUE' in j.get('codes', []) and no_literals(so))
d = build('G4_alias_only', data=rows(ngc=hp1('NGC 3198', **NG)))
rc, j, so = run(d)
case('G4', 'alias "NGC 3198" is not located -> exit 2 NGC3198:E_ROW_NOT_UNIQUE', rc == 2 and 'NGC3198:E_ROW_NOT_UNIQUE' in j.get('codes', []) and no_literals(so))

# ------------------------------------------------------------------ G5 contract failures: codes and booleans only
def fail_case(tag, ngc=None, ddo=None, manifest=None, want=None):
    dd_ = build(tag, data=rows(ngc=ngc, ddo=ddo), manifest=manifest)
    rc_, j_, so_ = run(dd_)
    case('G5', tag + ' -> exit 2 ' + str(want) + '; stdout codes/booleans only; no literal; no files',
         rc_ == 2 and all(w in j_.get('codes', []) for w in want) and only_bools(j_.get('checks')) and no_literals(so_) and out_files(dd_) == [],
         json.dumps(j_.get('codes')))
fail_case('G5_ddo_D_one_decimal', ddo=hp1('DDO154', **dict(DD, D='7.7')), want=['DDO154:E_SHAPE_D'])
fail_case('G5_ngc_fD_6', ngc=hp1('NGC3198', **dict(NG, fD='6')), want=['NGC3198:E_SHAPE_f_D'])
fail_case('G5_ngc_eInc_overrun_41', ngc=hp1('NGC3198', **NG)[:37] + b'10.55' + TAIL.encode()[1:], want=['NGC3198:E_BYTE41_NOT_BLANK'])
fail_case('G5_anchor_mismatch', manifest=json.dumps({'crosscheck_massmodels': {'reference_distance_texts': ['13.13']}}).encode(), want=['NGC3198:E_ANCHOR_T3_NOT_EQUAL'])
fail_case('G5_anchor_equals_eD', ngc=hp1('NGC3198', **dict(NG, eD='42.42')), want=['NGC3198:E_ANCHOR_OTHER_TOKEN_EQUAL'])
fail_case('G5_inc_einc_swapped', ddo=hp1('DDO154', **dict(DD, Inc='4.4', eInc='55.5')), want=['DDO154:E_RANGE_Inc', 'DDO154:E_RANGE_e_Inc'])
fail_case('G5_blank_type', ddo=hp1('DDO154', **dict(DD, T='')), want=['DDO154:E_TOKEN_COUNT_6'])

# ------------------------------------------------------------------ G6 documentation / pin failures
def doc_case(tag, want, **kw):
    dd_ = build(tag, **kw)
    rc_, j_, so_ = run(dd_)
    case('G6', tag + ' -> exit 2 ' + want, rc_ == 2 and j_.get('code') == want and out_files(dd_) == [] and no_literals(so_), json.dumps(j_)[:120])
doc_case('G6_source_pin', 'E_PIN_SOURCE', pins={'src': '0' * 64})
doc_case('G6_cds_pin', 'E_PIN_CDS', pins={'cds': '0' * 64})
doc_case('G6_manifest_pin', 'E_PIN_MANIFEST', pins={'man': '0' * 64})
doc_case('G6_manifest_duplicate_key', 'E_JSON_DUPLICATE_KEY', manifest=b'{"crosscheck_massmodels":{"reference_distance_texts":["42.42"]},"crosscheck_massmodels":{}}')
doc_case('G6_manifest_nan', 'E_JSON_NONFINITE_TOKEN', manifest=b'{"x":NaN,"crosscheck_massmodels":{"reference_distance_texts":["42.42"]}}')
doc_case('G6_anchor_two_texts', 'E_ANCHOR_TEXT', manifest=json.dumps({'crosscheck_massmodels': {'reference_distance_texts': ['42.42', '42.42']}}).encode())
doc_case('G6_anchor_not_numeric', 'E_ANCHOR_TEXT', manifest=json.dumps({'crosscheck_massmodels': {'reference_distance_texts': ['nan']}}).encode())
hb = REAL_HEADER.split(b'\n'); hb[11], hb[12] = hb[12], hb[11]
doc_case('G6_header_D_eD_lines_swapped', 'E_HEADER_ORDER', header=b'\n'.join(hb))
hb = REAL_HEADER.split(b'\n'); hb[35] = hb[35].replace(b'Cepheids', b'Cepheid')
doc_case('G6_header_note2_altered', 'E_HEADER_NOTES', header=b'\n'.join(hb))
cb = Path(REAL_CDS).read_bytes()
def alt(a, b_):
    x = cb.replace(a, b_, 1)
    assert x != cb, a
    return x
doc_case('G6_cds_dist_range_altered', 'E_CDS_ORDER', cds=alt(b'[0.98/127.8]', b'[0.98/127.9]'))
doc_case('G6_cds_null_flag_in_table1_note4', 'E_CDS_NULL_FLAG', cds=alt(b'Note (4): Where', b'Note (4): ? Where'))
doc_case('G6_cds_note3_altered', 'E_CDS_NOTE3', cds=alt(b'outer parts of the HI disk', b'inner parts of the HI disk'))

# ------------------------------------------------------------------ G7 preflight and publication paths (0348 protocol)
d = build('G7_output_exists'); (d / 'out' / OUTNAME).write_bytes(b'PRE')
rc, j, so = run(d)
case('G7', 'pre-existing output -> exit 2 E_OUTPUT_EXISTS; byte-identical; no candidate', rc == 2 and j.get('code') == 'E_OUTPUT_EXISTS' and (d / 'out' / OUTNAME).read_bytes() == b'PRE' and out_files(d) == [OUTNAME])
d = build('G7_candidate_exists'); (d / 'out' / (OUTNAME + '.candidate')).write_bytes(b'OLD')
rc, j, so = run(d)
case('G7', 'pre-existing candidate -> exit 2 E_CANDIDATE_EXISTS; old candidate byte-identical; no output', rc == 2 and j.get('code') == 'E_CANDIDATE_EXISTS' and (d / 'out' / (OUTNAME + '.candidate')).read_bytes() == b'OLD' and out_files(d) == [OUTNAME + '.candidate'])
d = build('G7_wrong_output_name')
rc, j, so = run(d, name='SPARC_ALLOWED_GEOMETRY_METADATA_V001.json')
case('G7', 'any other output name (e.g. the V001 name) -> exit 2 E_OUTPUT_NAME, no files', rc == 2 and j.get('code') == 'E_OUTPUT_NAME' and out_files(d) == [])
d = build('G7_usage')
rc, j, so = run(d, args=[])
case('G7', 'no argument -> exit 2 E_USAGE', rc == 2 and j.get('code') == 'E_USAGE')
d = build('G7_relative_path')
r = subprocess.run([sys.executable, '-I', '-B', str(d / 'extractor_copy.py'), 'out/' + OUTNAME], capture_output=True, text=True, cwd=str(d))
jr = json.loads(r.stdout.strip().splitlines()[-1])
case('G7', 'relative argument: published at the absolute preflight path and reported absolute', r.returncode == 0 and jr['output']['path'] == str(d / 'out' / OUTNAME) and jr['candidate']['path'] == str(d / 'out' / (OUTNAME + '.candidate')))


def pubcase(tag, patch, code, cand_expect, out_expect):
    dd_ = build(tag, inject=patch)
    rc_, j_, so_ = run(dd_)
    cnd = dd_ / 'out' / (OUTNAME + '.candidate'); op = dd_ / 'out' / OUTNAME
    ok_ = rc_ == 4 and j_.get('code') == code and j_.get('success_claimed') is False and no_literals(so_)
    if cand_expect == 'complete':
        ok_ &= cnd.exists() and json.loads(cnd.read_bytes())['objects'] == BASE_OBJS
    elif cand_expect == 'partial':
        ok_ &= cnd.exists() and 0 < len(cnd.read_bytes()) < j_['publication']['expected_bytes']
    elif cand_expect == 'absent':
        ok_ &= not cnd.exists() and j_['publication']['candidate_created'] is False
    elif cand_expect == 'other':
        ok_ &= cnd.read_bytes() == b'OTHER'
    if out_expect == 'absent':
        ok_ &= not op.exists() and j_['publication']['output_published'] is False
    elif out_expect == 'racer':
        ok_ &= op.read_bytes() == b'RACER'
    elif out_expect == 'published_not_claimed':
        ok_ &= op.exists() and j_['publication']['output_published'] is True
    case('G7', tag + ' -> exit 4 ' + code + ' (candidate ' + cand_expect + ', output ' + out_expect + ', nothing removed, no literal in stdout)', ok_, json.dumps(j_)[:140])


pubcase('race_output_created_before_link', "_rl=os.link\ndef _race(a,b):\n Path(b).write_bytes(b'RACER');return _rl(a,b)\nos.link=_race  # TEST-ONLY", 'E_OUTPUT_EXISTS_AT_PUBLICATION', 'complete', 'racer')
pubcase('link_unsupported', "def _nolink(a,b):raise OSError(1,'Operation not permitted (TEST-ONLY)')\nos.link=_nolink", 'E_PUBLICATION_LINK', 'complete', 'absent')
pubcase('partial_write', "_fd=os.fdopen\nclass _W:\n def __init__(s,f):s.f=f\n def __enter__(s):return s\n def __exit__(s,*a):s.f.close()\n def write(s,b):s.f.write(b[:len(b)//2]);s.f.flush();raise OSError(28,'No space left on device (TEST-ONLY)')\n def flush(s):pass\n def fileno(s):return s.f.fileno()\nos.fdopen=lambda fd,m:_W(_fd(fd,m))", 'E_CANDIDATE_WRITE', 'partial', 'absent')
pubcase('candidate_verify_mismatch', "_rb=Path.read_bytes\ndef _bad(self):\n x=_rb(self)\n return x+b' ' if self.name.endswith('.candidate') else x\nPath.read_bytes=_bad", 'E_CANDIDATE_VERIFY', 'complete', 'absent')
pubcase('candidate_create_denied', "_op=os.open\ndef _deny(p,fl,*a):\n if str(p).endswith('.candidate'):raise PermissionError(13,'denied (TEST-ONLY)')\n return _op(p,fl,*a)\nos.open=_deny", 'E_CANDIDATE_CREATE', 'absent', 'absent')
pubcase('candidate_appears_before_create', "_op=os.open\ndef _pre(p,fl,*a):\n if str(p).endswith('.candidate') and not Path(p).exists():Path(p).write_bytes(b'OTHER')\n return _op(p,fl,*a)\nos.open=_pre", 'E_CANDIDATE_EXISTS', 'other', 'absent')
pubcase('directory_fsync_fails', "_fs=os.fsync\ndef _dfs(fd):\n if stat.S_ISDIR(os.fstat(fd).st_mode):raise OSError(5,'I/O error (TEST-ONLY)')\n return _fs(fd)\nos.fsync=_dfs", 'E_DIRECTORY_FSYNC', 'complete', 'published_not_claimed')
pubcase('post_link_samefile_raises', "def _bad(a,b):raise ValueError('TEST-ONLY')\nos.path.samefile=_bad", 'E_POST_PUBLICATION_CHECK', 'complete', 'published_not_claimed')
pubcase('post_link_samefile_false', "os.path.samefile=lambda a,b:False  # TEST-ONLY", 'E_OUTPUT_NOT_SAME_FILE', 'complete', 'published_not_claimed')
pubcase('post_link_output_reread_differs', "_rb2=Path.read_bytes\ndef _bad2(self):\n x=_rb2(self)\n return x+b' ' if self.name.endswith('_CANDIDATE_V002.json') else x\nPath.read_bytes=_bad2", 'E_OUTPUT_VERIFY', 'complete', 'published_not_claimed')
d = build('G7_interrupt_validation', inject="_cp=check_prefix\ndef check_prefix(*a,**k):raise KeyboardInterrupt  # TEST-ONLY")
rc, j, so = run(d)
case('G7', 'interrupt during validation -> exit 130 FAILED_INTERRUPTED phase VALIDATION, no files', rc == 130 and j.get('status') == 'FAILED_INTERRUPTED' and j.get('phase') == 'VALIDATION' and out_files(d) == [] and no_literals(so))
d = build('G7_interrupt_publication', inject="def _ki(a,b):raise KeyboardInterrupt\nos.link=_ki  # TEST-ONLY")
rc, j, so = run(d)
case('G7', 'interrupt during publication -> exit 130 FAILED_INTERRUPTED phase PUBLICATION, candidate retained, no output', rc == 130 and j.get('phase') == 'PUBLICATION' and out_files(d) == [OUTNAME + '.candidate'] and no_literals(so))
d = build('G7_unexpected_exception', inject="def verify_cds():raise RuntimeError('TEST-ONLY')")
rc, j, so = run(d)
case('G7', 'unexpected exception in validation -> exit 3 E_UNEXPECTED phase VALIDATION, no files', rc == 3 and j.get('code') == 'E_UNEXPECTED' and j.get('phase') == 'VALIDATION' and out_files(d) == [])

# ------------------------------------------------------------------ receipt
n_pass = sum(r['pass'] for r in RES)
rec = {'schema': 'CLAUDE2_0353_SYNTHETIC_TEST_RECEIPT_V001', 'extractor': {'file': str(EXT), 'sha256': sha(EXT.read_bytes())},
       'harness': {'file': str(Path(__file__).resolve()), 'sha256': sha(Path(__file__).read_bytes())},
       'reused_evidence': {'fixtures_0349': {'file': str(FIX0349), 'sha256': sha(FIX0349.read_bytes())},
                           'results_0349': {'file': str(RES0349), 'sha256': sha(RES0349.read_bytes())},
                           'audit_correction_0349': {'file': str(CORR0349), 'sha256': sha(CORR0349.read_bytes())}},
       'run_dir': str(RUN), 'synthetic_only': True, 'real_extraction_run': False,
       'real_documentation_preflight': 'real MRT and manifest hashed only; real header lines 1-98 and real CDS ReadMe checked; no real data row sliced',
       'exposure_statement_v003': X.EXPOSURE, 'exposure_correction': X.EXPOSURE_CORRECTION,
       'harness_exposure': 'the harness hashes the real MRT and manifest, slices the real MRT only up to its 98th LF (header lines 1-98) and references the real CDS ReadMe; it never slices a real data row and never parses the real manifest',
       'groups': {g: [sum(r['pass'] for r in RES if r['group'] == g), sum(1 for r in RES if r['group'] == g)] for g in sorted(set(r['group'] for r in RES))},
       'n_cases': len(RES), 'n_pass': n_pass, 'all_pass': n_pass == len(RES), 'cases': RES}
with open(RECEIPT, 'x') as fh:
    json.dump(rec, fh, indent=1)
print(json.dumps({'n_cases': len(RES), 'n_pass': n_pass, 'receipt': str(RECEIPT)}))
