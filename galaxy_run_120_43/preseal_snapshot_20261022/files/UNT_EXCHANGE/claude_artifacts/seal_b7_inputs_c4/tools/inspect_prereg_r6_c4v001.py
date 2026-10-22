# Claude4 helper (dispatch 0650, A113 P6): read-only inspection of prereg r6 (seal slots, binding_inputs.case_block) and the
# case block of record. Prints only; writes nothing. Run under tools/run_fenced_c4st2.py.
import hashlib, json, sys
from pathlib import Path

PREREG = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json'
PREREG_SHA = 'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9'
CB = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json'
CB_SHA = '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'


def pairs(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise ValueError('DUPLICATE_JSON_KEY %r' % k)
        out[k] = v
    return out


def load(path, want):
    raw = Path(path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    print('SHA', path, got, 'MATCH' if got == want else 'MISMATCH want %s' % want)
    def nc(c):
        raise ValueError('NON_FINITE %s' % c)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nc)


p = load(PREREG, PREREG_SHA)
print('PREREG_TOP_KEYS', sorted(p))
bi = p.get('binding_inputs')
print('BINDING_INPUTS_KEYS', sorted(bi) if isinstance(bi, dict) else type(bi).__name__)
print('BINDING_INPUTS.case_block', json.dumps((bi or {}).get('case_block'), sort_keys=True))
ss = p.get('seal_slots') or {}
print('SEAL_SLOTS_KEYS', sorted(ss))
for k in sys.argv[1:]:
    print('=== seal_slots.%s' % k)
    print(json.dumps(ss.get(k), indent=1, sort_keys=True)[:6000])

cb = load(CB, CB_SHA)
print('CASE_BLOCK_TOP_KEYS', sorted(cb))
print('CASE_BLOCK_HAS_key_equivalence_map', 'key_equivalence_map' in cb)
print('CASE_BLOCK_key_equivalence_map', json.dumps(cb.get('key_equivalence_map', '<ABSENT>')))
print('CASE_BLOCK_key_equivalence_map_is_list_empty', cb.get('key_equivalence_map') == [] and isinstance(cb.get('key_equivalence_map'), list))
print('CASE_BLOCK_schema', cb.get('schema'), 'route_a_mode', cb.get('route_a_mode', '<ABSENT>'))
print('CASE_BLOCK_cases', sorted(cb.get('cases') or {}))
