"""SOURCE ONLY. Newword same-seed ancestry, full payload AND runtime closure.
Oldq11/PILOT_A reuse authorizations intentionally fail this family interface.
Root injects pinned old custody plus new0323 preparations, never mutates either.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from types import SimpleNamespace


def make(C, P, energy_reference_pin):
    """energy_reference_pin is complete acceptedC157census, pinned in request.
    This facade merely cites that accepted classification; it does not rerun it.
    Root runner must authenticate source identities and the actual C157 gate.
    """
    C.require(set(energy_reference_pin) == {'path', 'sha256'}, 'literal accepted energy-census reference')

    def energy_diagnostics():
        return {'family': 'P64_NEW15_INITIAL_WORDS_V001',
                'accepted_complete_initial_moment_census': energy_reference_pin,
                'full20_state_pairs': 190, 'unequal_first_two_moment_witnesses': 185,
                'remaining_pairs_energy_measure_matching': 'NOT_ESTABLISHED',
                'old_q11_means_reused_for_newwords': False,
                'label': 'PAIRWISE_C157_CLASSIFICATION_NOT_ENERGY_CONTROLLED_PREPARATIONS',
                'energy_independent_memory': False}

    def full_namespace(root, expected, size, guard):
        base = Path(root)
        C.require(base.is_absolute() and base.resolve() == base and not base.is_symlink()
                  and base.is_dir(), 'literal original namespace')
        files = {}
        for p in base.rglob('*'):
            C.require(not p.is_symlink(), 'no namespace symlink')
            if p.is_file():
                files[str(p.relative_to(base))] = p
        C.require(set(files) == set(expected), 'complete recursive original namespace census')
        for name, p in files.items():
            meta = expected[name]
            C.require(set(meta) == {'bytes', 'sha256'} and p.stat().st_size == meta['bytes']
                      and C.digest(p, guard) == meta['sha256'], 'complete original namespace file '+name)
        C.require(sum(v['bytes'] for v in expected.values()) == size, 'whole original namespace byte total')

    def assert_closed_archive(root, closure, guard):
        base = Path(root)
        C.require(closure['returncode'] == 0 and closure['cap_stop'] is None
                  and closure['all_opening_pins_checked'] is True and closure['all_closing_pins_match'] is True
                  and all(v is True for v in closure['closing_pins'].values()), 'whole successful original process pins')
        C.require(closure['payload_root'] == str(base) and base.name == 'PAYLOAD'
                  and closure['runtime_root'] == str(base.parent/'RUNTIME'), 'both original namespaces same owned job')
        full_namespace(base, closure['outputs'], closure['output_bytes'], guard)
        full_namespace(Path(closure['runtime_root']), closure['runtime_outputs'], closure['runtime_output_bytes'], guard)
        C.require(closure['whole_output_bytes_before_closure'] == closure['output_bytes']+closure['runtime_output_bytes']
                  and closure['whole_output_bytes_before_closure'] <= closure['whole_output_cap_bytes'],
                  'whole original payload plusruntime output cap')
        return closure['outputs']

    def load_ancestor_chain(chain, seed, stage, guard):
        P.identity(seed)
        C.require(type(stage) is int and stage in range(5) and isinstance(chain, list) and len(chain) == stage,
                  'whole newword same-seed ancestry')
        checkpoint, pins, archives = None, {}, []
        for index, descriptor in enumerate(chain):
            C.require(descriptor['kind'] == 'NEW_WORD_STAGE_V001' and descriptor['seed'] == seed
                      and descriptor['stage'] == index, 'literal ordered newword stage descriptor')
            auth = C.pinned_json(descriptor['root_reuse_authorization'], guard)
            C.require(auth['schema'] == 'P64_NEW_WORD_STAGE_REUSE_AUTHORIZATION_V001'
                      and auth['status'] == 'ROOT_ACCEPTED_FOR_NEW_WORD_STAGE_REUSE'
                      and auth['issued_by'] == '/root' and auth['reviewer_id'] not in (None, 'Codex3'),
                      'actual distinct newword authorization, no inherited oldseed gate')
            C.require(auth['seed'] == seed and auth['stage'] == index and auth['archive_root'] == descriptor['archive_root']
                      and auth['complete_original_output_review'] is True and auth['whole_ancestry_review'] is True
                      and auth['process_closure'] == descriptor['process_closure']
                      and auth['independent_report'] == descriptor['independent_report'], 'complete newword accepted scope')
            closure = C.pinned_json(descriptor['process_closure'], guard)
            report = C.pinned_json(descriptor['independent_report'], guard)
            C.require(report['complete_saved_reconstruction'] is True and report['seed'] == seed and report['stage'] == index
                      and report['whole_original_output_checked'] is True and report['whole_same_seed_ancestry_checked'] is True,
                      'whole independent newword arithmetic and ancestry report')
            files = assert_closed_archive(descriptor['archive_root'], closure, guard)
            C.require('CHECKPOINT.json' in files and 'RESULT.json' in files, 'complete newword saved artifacts')
            current = json.loads((Path(descriptor['archive_root'])/'CHECKPOINT.json').read_text())
            C.validate_checkpoint(current, seed, index, checkpoint)
            cap = P.resource_prospect(index)['producer_complete_output_cap_per_seed']
            C.require(closure['wall_seconds'] <= 600 and closure['exact_wait4_peak_rss_bytes'] <= 2*2**30
                      and closure['output_bytes'] <= cap and closure['runtime_output_bytes'] <= 16*2**20
                      and closure['whole_output_cap_bytes'] <= cap+16*2**20, 'newword original producer whole caps')
            checkpoint = current
            archives.append((descriptor['archive_root'], closure))
            for role in ('root_reuse_authorization', 'process_closure', 'independent_report'):
                pin = descriptor[role]
                if pin['path'] in pins:
                    C.require(pins[pin['path']] == pin['sha256'], 'same pinned ancestry bytes')
                pins[pin['path']] = pin['sha256']
        return checkpoint, pins, archives

    return SimpleNamespace(__file__=__file__, require=C.require, wire=C.wire,
                           digest=C.digest, pinned_json=C.pinned_json, rehash=C.rehash,
                           save_json=C.save_json, validate_checkpoint=C.validate_checkpoint,
                           load_ancestor_chain=load_ancestor_chain,
                           assert_closed_archive=assert_closed_archive,
                           energy_diagnostics=energy_diagnostics)
