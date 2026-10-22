"""Kit relaunch / retry-after-refusal custody probe: the S0 kit reuses its registry entry by spec SHA only,
while each kit invocation fills into a new $WORK/fill path (launch_s0_serial_root_c2v003a.sh L126/L141/L214;
s0_kit_c2v003a.py cmd_register). Compare cw8 successor 04dfc429 vs base cx2v004 8cec1b56 on the same saved state."""
import sys, json, ast, types, hashlib, copy
from pathlib import Path
D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_phase1_cx3')
BASE = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py'
fsp = D / 'test_selector_cx3v003.py'
cust = (D / 'test_custody_cx3v003.py').read_text()
braw = open(BASE, 'rb').read()
sys.argv[1:] = [sys.argv[1]]
src = fsp.read_text().split('\ncase("missing_license_automatic_serial"')[0]
g = {'__file__': str(fsp), '__name__': 'kitprobe'}
exec(compile(src, str(fsp) + ':definitions', 'exec'), g)
M, make_context, put, DATE, NOW = g['M'], g['make_context'], g['put'], g['DATE'], g['NOW']
g['ALLOWED'].add(BASE)
for node in ast.parse(cust).body:
    if isinstance(node, ast.FunctionDef) and node.name in ('saved_monitor',):
        exec(compile(ast.get_source_segment(cust, node), 'custody:' + node.name, 'exec'), g)
saved_monitor = g['saved_monitor']
assert hashlib.sha256(braw).hexdigest().startswith('8cec1b56')
MB = types.ModuleType('base_cx2v004'); MB.__file__ = BASE
exec(compile(braw, BASE, 'exec'), MB.__dict__)
OUT = {}
def scenario(relaunch_path):
    f = make_context()
    ctx = f.ctx
    call = ctx.call(M.TWIN)
    outdir = M.planned_outdir(ctx, M.TWIN, 1, 'KIT')
    caps = M.first_caps(M.TWIN)
    spec_for_attempt = call['spec']
    if relaunch_path:
        raw = Path(call['spec']['path']).read_bytes()
        (f.root / 'kit_work_A1_second_invocation' / 'fill').mkdir(parents=True)
        spec_for_attempt = put(f.root / 'kit_work_A1_second_invocation' / 'fill' / M.TWIN_FILE, raw, raw=True)
        assert spec_for_attempt['sha256'] == call['spec']['sha256'] and spec_for_attempt['path'] != call['spec']['path']
    attempt_call = dict(call, spec=spec_for_attempt)
    lj, ljpin, monitor, mpin = saved_monitor(ctx, attempt_call, outdir, caps)
    rec = {'schema': 'UNT_S0_LAUNCH_RECORD_C2V003A', 'name': M.TWIN, 'attempt': 1, 'outcome': 'LAUNCH',
           'outdir': outdir, 'receipt': outdir + '.receipt.json',
           'launch_json': dict(ljpin, utc=lj['utc'], child_pid=lj['child_pid']),
           'spec': spec_for_attempt, 'driver': ctx.pins['driver'], 'monitor': ctx.pins['monitor'],
           'caps': caps, 'monitor_pid': 900001, 'sampler_pid': None, 'watch_pid': None,
           'solo_mode': False, 'counted_rerun': False, 'date_u': DATE}
    put(Path(ctx.cfg['s0']['launch_root']) / 'launches' / (M.TWIN + '_LAUNCH_C2V003A_A1.json'), rec)
    res = {}
    # base: same saved state, config schema CX2V004, V006 copy with the base TOOL_PIN in an A section
    cfgb = copy.deepcopy(M.read_pin(f.config)); cfgb['schema'] = 'P112_CONFIG_CX2V004'
    text = ctx.v006_text + '\n## A999: synthetic base gate\nTOOL_PIN P112_LAUNCHER_CX2V004 %s %s\n' % (hashlib.sha256(braw).hexdigest(), BASE)
    vp = put(f.root / 'V006_BASE.md', text.encode(), raw=True)
    cfgb['v006'] = vp['path']
    cpb = put(f.root / 'CONFIG_BASE.json', cfgb)
    sysdata = M.read_pin(f.synthetic)['system']
    sb = MB.SyntheticSystem(sysdata); sb.processes = lambda: []; sb.utc = lambda: NOW
    # successor first (its gate uses the original V006 copy)
    try:
        r = M.close_attempt(ctx, M.TWIN, 1); res['successor_close'] = r['status_class']
        h = M.history(ctx, ctx.call(M.TWIN), inspect_next=False); res['successor_history_actual'] = len(h['actual'])
    except M.Refusal as e:
        res['successor'] = 'REFUSED:' + e.code
    try:
        ctxb = MB.Context(cpb, system=sb, synthetic_pins=f.overrides)
        if 'successor_close' not in res:
            r = MB.close_attempt(ctxb, M.TWIN, 1); res['base_close'] = r['status_class']
        h = MB.history(ctxb, ctxb.call(M.TWIN), inspect_next=False); res['base_history_actual'] = len(h['actual'])
    except MB.Refusal as e:
        res['base'] = 'REFUSED:' + e.code
    return res
for label, flag in (('control_same_path', False), ('kit_second_invocation_new_fill_path', True)):
    try:
        OUT[label] = scenario(flag)
    except Exception as e:
        import traceback
        OUT[label] = {'exception': type(e).__name__, 'msg': str(e)[:300], 'tb': traceback.format_exc(limit=3)[-600:]}
print(json.dumps(OUT, indent=1))
