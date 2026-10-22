"""Claude3 helper fence probe (0848 unit 3 review). compile() only: no module is executed.
Shows whether guard014's native-preflight fence admits the c2v004 ledger wrapper's module-level generated compile
(c2v004 L602-603), and that a one-entry GENERATED_COMPILE_CONTRACT extension (model of a guard015) would.
Usage: python3 -I -B probe_fence_c3h002.py <result_json_new>"""
import ast, hashlib, json, sys, types, datetime, os
RESULT = sys.argv[1]
GUARD = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py'
C2V004 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py'
GSHA = '6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d'
OWNER = '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'
def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.posix_spawn', 'os.exec', 'socket.connect', 'socket.bind'):
        raise RuntimeError('PROBE_PROCESS_OR_NETWORK_FORBIDDEN')
    if event == 'exec' and EXEC_LOCK[0]: raise RuntimeError('PROBE_EXEC_FORBIDDEN_AFTER_GUARD_LOAD')
EXEC_LOCK = [False]
sys.addaudithook(audit)
gb = open(GUARD, 'rb').read(); assert hashlib.sha256(gb).hexdigest() == GSHA
wb = open(C2V004, 'rb').read(); assert hashlib.sha256(wb).hexdigest() == OWNER
def guard():
    G = types.ModuleType('_probe_guard'); G.__file__ = GUARD; exec(compile(gb, GUARD, 'exec'), G.__dict__); return G
G = guard(); G2 = guard()
BUF = next(ast.literal_eval(n.value) for n in ast.parse(wb).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_resolve_source' for t in n.targets))
BUF_SHA = hashlib.sha256(BUF.encode('utf-8')).hexdigest()
EXEC_LOCK[0] = True   # from here on no exec() may run in this process
results = []
def check(name, fn, expect, cite):
    try: fn(); obs = 'ACCEPT'
    except Exception as e: obs = e.args[0] if type(e).__name__ == 'Refusal' and e.args else type(e).__name__ + ':' + str(e)
    results.append({'name': name, 'expected': expect, 'observed': obs, 'pass': obs == expect, 'cite': cite})
def under(Gx, sources, src):
    with Gx.fence(sources): compile(src, C2V004, 'exec')
check('D0_buffer_is_the_whitelisted_generated_buffer', lambda: None if BUF_SHA in G.GENERATED_COMPILE_CONTRACT['7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'] else (_ for _ in ()).throw(ValueError('NOT_WHITELISTED')), 'ACCEPT', 'guard014 L27-29; c2v004 L602')
check('D1_c2v004_generated_compile_under_guard014_fence', lambda: under(G, {C2V004: OWNER}, BUF), 'PREFLIGHT_COMPILE_HASH_MISMATCH', 'guard014 L140-153; c2v004 L603')
check('D2_c2v004_exact_bytes_compile_under_guard014_fence', lambda: under(G, {C2V004: OWNER}, wb), 'ACCEPT', 'guard014 L145-150')
check('D3_unpinned_c2v004_exact_bytes_compile', lambda: under(G, {}, wb), 'PREFLIGHT_COMPILE_HASH_MISMATCH', 'guard014 L148-150')
G2.GENERATED_COMPILE_CONTRACT = dict(G2.GENERATED_COMPILE_CONTRACT, **{OWNER: frozenset({BUF_SHA})})
check('D4_model_guard015_one_contract_entry_admits_it', lambda: under(G2, {C2V004: OWNER}, BUF), 'ACCEPT', 'model: guard014 L27-29 + {7c9b4248: {79e8936d}}')
out = {'schema': 'C3_FENCE_PROBE_C3H002', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'python': sys.version,
       'guard_sha256': GSHA, 'c2v004_sha256': OWNER, 'generated_buffer_sha256': BUF_SHA, 'executed_modules': ['guard014 bytes only (as launcher015/binder011 do)'],
       'compiled_not_executed': [C2V004 + ' (whole file and its L602 literal)'], 'passed': sum(r['pass'] for r in results), 'total': len(results), 'results': results}
with open(RESULT, 'xb') as f: f.write(json.dumps(out, indent=1, sort_keys=True).encode() + b'\n')
print(json.dumps({'passed': out['passed'], 'total': out['total'], 'results': [(r['name'], r['observed'], r['pass']) for r in results]}, indent=1))
