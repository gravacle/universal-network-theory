# Claude4 synthesis (dispatch 0651; A116.2 E_R6_2 scope): which prereg r6 text-of-record clauses still state the r13 token set,
# and does any code read them? Read-only; run through tools/run_fenced_c4st2.py; writes one JSON under synthesis/out/.
# usage: python3 -I -B tools/run_fenced_c4st2.py synthesis/scripts/prereg_r6_wording_c4v001.py OUTNAME
import hashlib, json, sys, time
from pathlib import Path

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_compare_r14_c4/synthesis/out') / (sys.argv[1] + '.json')
TOR = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json',
       'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9')
READERS = {
    'r14_source': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py',
                   'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
    'tool4': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/build_seal_record_c4v004.py',
              '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41'),
    'tool3': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/check_slot_fill_c4v003.py',
              '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af'),
    'tool2': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/check_sealed_compare_c4v003.py',
              'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1'),
    'tool1': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/check_frozen_addendum_c4v003.py',
              'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4'),
    'seal_common': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/seal_common_c4v003.py',
                    '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21'),
    'prestage_c3v020': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/ROOT_SEAL_STEPS_c3v020.sh',
                        '36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0'),
}
R = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'ok': True, 'checks': {}}
b = Path(TOR[0]).read_bytes()
R['checks']['tor_sha_ok'] = hashlib.sha256(b).hexdigest() == TOR[1]
d = json.loads(b)
pol = d['gates_before_any_T_result']['after_seal_marker_policy']['text']
R['clauses'] = {
    'gates_before_any_T_result.after_seal_marker_policy.text': pol,
    'seal_slots.compare.rule[:200]': d['seal_slots']['compare']['rule'][:200],
    'seal_slots.producer_registry.rule[I4 clause]': d['seal_slots']['producer_registry']['rule'][
        d['seal_slots']['producer_registry']['rule'].find('BUILD_V007'):][:140],
}
R['checks']['policy_states_the_nine_and_refuses_every_other_gate'] = (
    'accepted only for the nine gates' in pol and 'for every other gate (r13)' in pol and 'I4' not in pol
    and 'r13 GATE_RECORD_AFTER_SEAL_ALLOWED L341' in pol)
R['checks']['gates_before_any_T_result_has_no_I4_key'] = not any('I4' in k for k in d['gates_before_any_T_result'])
R['readers'] = {}
for k, (p, h) in READERS.items():
    t = Path(p).read_bytes()
    R['readers'][k] = {'sha_ok': hashlib.sha256(t).hexdigest() == h,
                       'after_seal_marker_policy': t.count(b'after_seal_marker_policy'),
                       'gates_before_any_T_result': t.count(b'gates_before_any_T_result')}
R['checks']['no_reader_of_the_clause'] = all(v['sha_ok'] and v['after_seal_marker_policy'] == 0 and v['gates_before_any_T_result'] == 0
                                             for v in R['readers'].values())
R['ok'] = all(R['checks'].values())
OUT.write_text(json.dumps(R, indent=1) + '\n')
print(json.dumps(R['checks']), R['ok'])
raise SystemExit(0 if R['ok'] else 1)
