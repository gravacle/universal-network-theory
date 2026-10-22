"""SOURCE ONLY. Root injects literal pinned modules and durable audit callback.
Calls original execute_stage/kernel unchanged with explicit newword roles.
Root must supply a NEW reviewed runtime/caller; oldfive bootstrap not authorized.
"""
from pathlib import Path
import os
import resource
import sys
import time

EX = Path('/Users/bgm/Research/UNT_EXCHANGE')
BASE = EX/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001'
LANE = EX/'lanes/P49_CODEX2'
OUT = EX/'FROM_CODEX3'
PINNED = {
    'kernel': (LANE/'history_interval_propagator_v002.py', 'c699cc31a84f5b5190d851f9e1b581c2f0322e9c8b563edbf98bc8a99c648b96'),
    'binding': (LANE/'history_interval_binding_and_sink_v003.py', 'c7ed5b97f0e77a456c8450ffc6e86f3e34156006c71f09f77c458972e0bd8347'),
    'old_custody': (LANE/'history_stage_custody_v002.py', 'a05c79f0f04e60a662da731fd46c199d29156bc613abd84d990e1d78e4b9fe7e'),
    'executor': (LANE/'held_history_stage_executor_v001.py', 'cc7893236f5c6bb5dfb290f83cac6763505fec36832ed51d02c01bc6e8285f8c'),
    'new_preparations': (OUT/'0323_2026-10-13_new15-word-preparations-and-schedule.py', '17d092ba48a79d021b0726c6a9d120df1a69e4dd78b7d85ef5cd08020b65bb44'),
    'new_custody': (OUT/'0324_2026-10-13_new15-word-ancestry-custody.py', '35e956d7448cb47c84afc3108b8cf7de0671575149cadaa3f3a7dd0adbe90528')}
C157 = {'path': str(BASE/'P64_NATIVE_EXACT_READ_ACCEPTANCE_V001.json'), 'sha256': '2574982b6064be5a802453d34faf4f60f00c99b9de022e5f9c6886ac1c199444'}
ENERGY = {'path': str(BASE/'P64_NATIVE_CENSUS_OUTPUT_V001/ACTUAL_RETURN.json'), 'sha256': 'c190b863f63c8c93077b5b31742f6edd1b8c32e970d1f19621798a00ed1692cd'}


def execute_word_stage(K, B, C0, E, N, NC, request_pin, release_pin, output, audit):
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        C0.require(time.monotonic()-started <= 600 and rss <= 2*2**30, 'whole newword adapter600s2GiB')
    C0.require(callable(audit), 'root durable before/return callback required')
    request = C0.pinned_json(request_pin, guard)
    C0.require(set(request) == {'schema', 'stage', 'seed', 'native_paths', 'frozen_native_pin_manifest',
                               'role_sources', 'expected_hashes', 'ancestor_chain', 'family',
                               'family_source_gate', 'storage_gate', 'c157_acceptance', 'energy_reference_pin'},
               'closed newword request fields')
    C0.require(request['schema'] == 'P49_HELD_STAGE_REQUEST_V001'
               and request['family'] == 'P64_NEW15_INITIAL_WORDS_V001', 'explicit new family on original executor wire')
    word, preparation_type = N.identity(request['seed'])
    stage = request['stage']
    C0.require(type(stage) is int and 0 <= stage < 4, 'newword four-stage schedule')
    modules = {'kernel': K, 'binding': B, 'old_custody': C0, 'executor': E, 'new_preparations': N, 'new_custody': NC}
    hashes = request['expected_hashes']
    for name, module in modules.items():
        path, sha = PINNED[name]
        C0.require(Path(module.__file__).resolve() == path and hashes.get(str(path)) == sha
                   and C0.digest(path, guard) == sha, 'literal actual injected source '+name)
    own = str(Path(__file__).resolve())
    C0.require(own in hashes and C0.digest(own, guard) == hashes[own], 'new held adapter source pin')
    expected_roles = {'kernel': str(PINNED['kernel'][0]), 'binding': str(PINNED['binding'][0]),
                      'executor': str(PINNED['executor'][0]), 'prospect': str(PINNED['new_preparations'][0]),
                      'preparations': str(PINNED['new_preparations'][0]), 'custody': str(PINNED['new_custody'][0])}
    C0.require(request['role_sources'] == expected_roles, 'actual new-role identity, no oldseed module impersonation')
    C0.require(request['c157_acceptance'] == C157 and request['energy_reference_pin'] == ENERGY, 'literal accepted20state moment census')
    for field in ('family_source_gate', 'storage_gate', 'c157_acceptance', 'energy_reference_pin'):
        pin = request[field]
        C0.require(hashes.get(pin['path']) == pin['sha256'], 'newfamily gate/ancestry in closing hash domain')
    for field in ('family_source_gate', 'storage_gate'):
        C0.require(Path(request[field]['path']).parent == BASE, 'root-owned newfamily gate')
    accepted = C0.pinned_json(C157, guard)
    census = C0.pinned_json(ENERGY, guard)
    C0.require(accepted['claim'] == 'C-157' and accepted['acceptor'] == '/root'
               and accepted['status'] == 'ROOT_ACCEPTED_COMPLETE_EXACT_SAVED_READS'
               and accepted['complete_original_runtime_custody'] is True
               and accepted['census_states'] == 20
               and accepted['pair_status_counts'] == {'UNEQUAL_PROVED': 185, 'NOT_ESTABLISHED': 5}
               and census['case'] == 'census' and census['exception'] is None, 'actual C157 qualification, no trajectory reuse')
    gate = C0.pinned_json(request['family_source_gate'], guard)
    needed_hashes = {str(p): s for p, s in PINNED.values()}
    needed_hashes[own] = hashes[own]
    C0.require(gate['schema'] == 'P64_NEW15_DISTINCT_BINDING_SOURCE_GATE_V001'
               and gate['acceptor'] == '/root' and str(gate['status']).startswith('PASS')
               and gate['source_author'] == 'Codex3' and gate['reviewer_id'] != 'Codex3'
               and gate['source_hashes'] == needed_hashes and gate['full15_binding_controls_accepted'] is True,
               'distinct entire newbinding/control gate')
    storage = C0.pinned_json(request['storage_gate'], guard)
    prospect = N.campaign_storage_prospect()
    C0.require(storage['schema'] == 'P64_NEW15_ROOT_STORAGE_RELEASE_V001' and storage['issued_by'] == '/root'
               and storage['status'] == 'ROOT_FULL_CAMPAIGN_AND_CURRENT_WAVE_SPACE_ACCEPTED'
               and storage['scientific_prospect'] == prospect
               and storage['full_campaign_scientific_and_runtime_bytes'] >= prospect['all_stage_scientific_caps_sum']+120*16*2**20
               and storage['full_campaign_opening_free_bytes'] >= storage['full_campaign_scientific_and_runtime_bytes']
               and storage['completed_jobs_distinctly_root_accepted'] is True,
               'whole120job storage freeze and completed-prefix gate')
    current = N.resource_prospect(stage)['producer_complete_output_cap_per_seed']+16*2**20
    C0.require(storage['seed'] == request['seed'] and storage['stage'] == stage
               and storage['remaining_scientific_and_runtime_bytes'] >= current
               and storage['remaining_scientific_and_runtime_bytes'] <= storage['full_campaign_scientific_and_runtime_bytes'],
               'literal current remaining-wave storage release')
    destination = Path(output)
    C0.require(destination.is_absolute() and destination.resolve() == destination and BASE in destination.parents
               and not destination.exists() and destination.parent.is_dir(), 'fresh root-owned newword output')
    fs = os.statvfs(destination.parent)
    C0.require(fs.f_bavail*fs.f_frsize >= storage['remaining_scientific_and_runtime_bytes'], 'actual remaining family free-space before root call')
    P, S = N.roles()
    C = NC.make(C0, N, ENERGY)
    pre = {'schema': 'P64_NEW15_ACTUAL_PRE_CALL_V001', 'executor': '/root', 'pid': os.getpid(),
           'function': 'execute_word_stage', 'request_pin': request_pin, 'release_pin': release_pin,
           'role_sources': expected_roles, 'adapter_sources': needed_hashes, 'output': str(destination),
           'initial_word': word, 'preparation_type': preparation_type,
           'source_gate': request['family_source_gate'], 'storage_gate': request['storage_gate'],
           'unchanged_original_execute_stage': True, 'original_q11_reuse_authorized': False}
    audit('PRE', pre)
    try:
        result = E.execute_stage(K, B, P, S, C, request_pin, release_pin, destination)
        guard()
        audit('RETURN', {'schema': 'P64_NEW15_ACTUAL_RETURN_V001', 'executor': '/root', 'pid': os.getpid(),
                         'exception': None, 'value': C0.wire(result)})
        return result
    except BaseException as error:
        audit('RETURN', {'schema': 'P64_NEW15_ACTUAL_RETURN_V001', 'executor': '/root', 'pid': os.getpid(),
                         'exception': type(error).__name__, 'message': str(error)})
        raise
