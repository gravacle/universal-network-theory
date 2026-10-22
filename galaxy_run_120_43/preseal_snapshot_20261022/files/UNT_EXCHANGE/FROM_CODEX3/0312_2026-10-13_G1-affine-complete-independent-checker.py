"""Root-only saved checker. No scientific source from Code2/root is executed.
Independent barycentric permutation action and arithmetic edge indexing.
CLI --L 4|5 --archive literal absolute six-file producer directory.
Original full process/runtime closure remains a separate root obligation.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import sys
import time

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE')
SOURCE = BASE/'lanes/P60_CODEX2/p60_exact_affine_symmetry_census_v001.py'
PRODUCER = BASE/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_AFFINE_ROOT_PRODUCER_V001.py'
THEORY = BASE/'lanes/P60_CODEX2/P60_G1_EXACT_SYMMETRY_AND_SPECTRAL_OBLIGATIONS_V001.txt'
PINS = {SOURCE: '27b427ec930ac7cb18ebb9663547a74773f97cd348d800d5a23729db1a3bb2d1',
        PRODUCER: 'c8c804054dae15c51fa4daa2063b8775d348f8a54b4ce5743a83cd386a8e1262',
        THEORY: 'ac90cab7bbea1da319c58fe31b48d9076b0fdc5bc817c51e6aa39ee7be2bc806'}
FILES = {'START.json', 'SOURCE_SNAPSHOT.py', 'ACTUAL_PRE.json',
         'PROGRESS.jsonl', 'ACTUAL_RETURN.json', 'FINISH.json'}
CONDITIONS = ['uniform real t theta0', 'uniform vertex scalar coefficients',
              'uniform kappa', 'epsilonBirth same on every eligibility state',
              'two-cut occupancy eligibility', 'blank inserted registers',
              'no extra marked source/state labels']


def need(ok, label):
    if not ok:
        raise ValueError(label)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def raw_file(path, cap):
    need(path.is_absolute() and path.resolve() == path and not path.is_symlink()
         and path.is_file() and path.stat().st_size <= cap, 'plain bounded ' + str(path))
    with path.open('rb') as stream:
        raw = stream.read(cap+1)
    need(len(raw) <= cap, 'actual read bound')
    return raw


def pairs(items):
    answer = {}
    for k, v in items:
        need(k not in answer, 'duplicate JSON key')
        answer[k] = v
    return answer


def decode(raw):
    def bad(v):
        raise ValueError('nonfinite JSON '+v)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def exact(a, b, label):
    need(type(a) is type(b), 'type '+label)
    if isinstance(b, dict):
        need(a.keys() == b.keys(), 'all keys '+label)
        for k in b:
            exact(a[k], b[k], label+'/'+k)
    elif isinstance(b, list):
        need(len(a) == len(b), 'all list entries '+label)
        for i in range(len(b)):
            exact(a[i], b[i], label+'/'+str(i))
    else:
        need(a == b, 'value '+label)


def reconstruct(L, compare, guard):
    """Stream whole candidate comparison; return full independently derived object."""
    n = L**3
    def xyz(k):
        return (k//(L*L), (k//L)%L, k%L)
    def number(v):
        return (v[0]%L)*L*L+(v[1]%L)*L+v[2]%L
    def neighbor(k, colour):
        q = list(xyz(k))
        if colour:
            q[colour-1] += 1
        return number(q)
    edges = [[k, n+neighbor(k, c)] for k in range(n) for c in range(4)]
    cut = [0, 4*L*L, 4*L, 4]
    cutset = set(cut)
    born = [[e, *edges[e]] for e in range(4*n) if e not in cutset]
    for j, e in enumerate(cut):
        a, b = edges[e]
        born.extend([[4*n+2*j, a, 2*n+1], [4*n+2*j+1, 2*n, b]])
    born.sort()
    records = []
    survivors = []
    for sigma in itertools.permutations(range(4)):
        for swap in (False, True):
            for tid in range(n):
                guard()
                t = xyz(tid)
                vertices = []
                for v in range(2*n):
                    side, k = divmod(v, n)
                    x, y, z = xyz(k)
                    coefficients = [-x-y-z+side, x, y, z]
                    barycentric = [0, 0, 0, 0]
                    for i in range(4):
                        barycentric[sigma[i]] = coefficients[i]
                    sign = -1 if swap else 1
                    target = tuple(t[a]+sign*barycentric[a+1] for a in range(3))
                    vertices.append((side ^ int(swap))*n+number(target))
                need(len(set(vertices)) == 2*n, 'independent vertex bijection')
                emap = []
                for e, (a, b) in enumerate(edges):
                    u, v = vertices[a], vertices[b]
                    if u >= n:
                        u, v = v, u
                    image = 4*u+sigma[e%4]
                    need(edges[image] == [u, v], 'every mapped endpoint and colour')
                    emap.append(image)
                need(len(set(emap)) == 4*n, 'independent edge bijection')
                broken = next((e for e in cut if emap[e] not in cutset), None)
                keep = broken is None
                # Algebraic classification is checked for every candidate,
                # separately from the complete endpoint construction above.
                need(keep == (sigma[0] == 0 and not swap and tid == 0),
                     'marked-cut subgroup theorem on every candidate')
                row = {'sigma': list(sigma), 'exchange_AB': swap, 'translation': list(t),
                       'old_graph_operator_symmetry': True,
                       'formal_uniform_old_ring_symmetry': True,
                       'marked_join_operator_symmetry': keep,
                       'all_old_edges_checked': 4*n}
                if not keep:
                    row['marked_cut_rejection_witness'] = {'edge': broken, 'mapped_edge': emap[broken]}
                else:
                    cp = [cut.index(emap[e]) for e in cut]
                    need(sorted(cp) == list(range(4)), 'cut permutation')
                    bv = vertices+[2*n, 2*n+1]
                    bmap = []
                    born_lookup = {e: [a, b] for e, a, b in born}
                    for e, a, b in born:
                        if e < 4*n:
                            dest = emap[e]
                        else:
                            j, half = divmod(e-4*n, 2)
                            dest = 4*n+2*cp[j]+half
                        need(born_lookup[dest] == [bv[a], bv[b]], 'all Born stable-ID endpoints')
                        bmap.append([e, dest])
                    need(len({b for a, b in bmap}) == len(born), 'Born edge bijection')
                    row.update(vertex_permutation_old_and_stars=bv,
                               edge_permutation_old=emap,
                               edge_permutation_Born_stable_ids=bmap,
                               four_cut_permutation=cp, term_identity_conditions=CONDITIONS)
                    survivors.append(row)
                compare(len(records), row)
                records.append(row)
    need(len(records) == 48*n and len(survivors) == 6, 'complete class and six survivors')
    return {'schema': 'P60_EXACT_AFFINE_G1_SYMMETRY_V001', 'L': L,
            'old_edges': edges, 'ordered_cuts': cut, 'Born_edges_stable_ids': born,
            'candidate_count': 48*n, 'all_candidates': records, 'joined_survivors': survivors,
            'scope': 'LATTICE_AFFINE_CLASS_NOT_ALL_ABSTRACT_GRAPH_AUTOMORPHISMS',
            'point_irrep_and_momentum_simultaneous_labels_assumed': False,
            'ice_dimension_or_spectrum_computed': False, 'physical_Gamma_release': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--L', type=int, choices=[4, 5], required=True)
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        need(rss <= 256*2**20, 'checker256MiB cap')
        need(time.monotonic()-started <= 120, 'checker120s cap')
    root = args.archive
    need(root.is_absolute() and root.resolve() == root and not root.is_symlink()
         and root.is_dir(), 'literal existing archive')
    need({p.name for p in root.iterdir()} == FILES, 'exact six files')
    sourcebytes = {p: raw_file(p, 32768) for p in PINS}
    for p in PINS:
        need(digest(sourcebytes[p]) == PINS[p], 'literal pin '+str(p))
    payload = {name: raw_file(root/name, 8*2**20) for name in FILES}
    need(sum(map(len, payload.values())) <= 8*2**20, 'whole scientific reserve')
    need(payload['SOURCE_SNAPSHOT.py'] == sourcebytes[SOURCE], 'complete raw source snapshot')
    start = decode(payload['START.json'])
    pid = start.get('pid')
    need(type(pid) is int and pid > 0, 'recorded producer PID syntax only')
    exact(start, {'schema': 'P60_AFFINE_FIXED_ROOT_CALL_V001', 'pid': pid, 'L': args.L,
                 'source': {'path': str(SOURCE), 'sha256': PINS[SOURCE]},
                 'runner_sha256': PINS[PRODUCER],
                 'caps': {'cpu': 1, 'rss_bytes': 268435456, 'seconds': 120, 'output_bytes': 16777216},
                 'external_supervisor_required': True, 'scientific_acceptance': False}, 'START')
    exact(decode(payload['ACTUAL_PRE.json']), {'function': 'census', 'arguments': [args.L],
          'callback': 'all48Lcubed affine candidates retained'}, 'PRE')
    lines = payload['PROGRESS.jsonl'].splitlines()
    need(payload['PROGRESS.jsonl'].endswith(b'\n') and len(lines) == 48*args.L**3,
         'all candidate progress records with closing newline')
    need(all(0 < len(v)+1 <= 65536 for v in lines), 'complete bounded progress lines')
    actual = decode(payload['ACTUAL_RETURN.json'])
    need(type(actual) is dict and set(actual) == {'exception', 'value'}
         and actual['exception'] is None, 'complete success only, cap refusal never accepted')
    def compare(i, row):
        exact(decode(lines[i]), row, 'PROGRESS/'+str(i))
        if (i+1)%256 == 0 or i+1 == len(lines):
            print(json.dumps({'independent_progress': 'ALL_CANDIDATES', 'completed': i+1,
                              'total': len(lines)}), flush=True)
    expected = reconstruct(args.L, compare, guard)
    exact(actual['value'], expected, 'RETURN/value')
    exact(decode(payload['FINISH.json']), {
        'status': 'RAW_AFFINE_CENSUS_PENDING_DISTINCT_SAVED_COMPARISON', 'pid': pid,
        'progress_records': len(lines), 'source_closing_bytes_match': True,
        'spectral_execution': False, 'physical_release': False}, 'FINISH')
    need({p.name for p in root.iterdir()} == FILES, 'closing file census')
    for p, raw in sourcebytes.items():
        need(raw_file(p, 32768) == raw, 'closing source bytes')
    for name, raw in payload.items():
        need(raw_file(root/name, 8*2**20) == raw, 'closing payload bytes')
    guard()
    print(json.dumps({'schema': 'P60_AFFINE_COMPLETE_INDEPENDENT_REVIEW_V001',
          'status': 'PASS_COMPLETE_PAYLOAD_PENDING_ROOT_RUNTIME_CUSTODY', 'L': args.L,
          'archive': str(root), 'author': 'Codex3', 'source_author': 'Codex2',
          'caller_author': 'Codex ROOT', 'self_review': False,
          'files': {k: {'bytes': len(v), 'sha256': digest(v)} for k, v in sorted(payload.items())},
          'complete_typed_return_and_progress_exact': True, 'candidate_count': len(lines),
          'joined_survivor_count': len(expected['joined_survivors']),
          'shared_math': 'Same declared affine simplex class; independent barycentric action and arithmetic edge indexing',
          'all_abstract_automorphisms_claimed': False, 'ice_dimension_or_spectrum_computed': False,
          'original_runtime_verified_by_this_checker': False, 'physical_Gamma_release': False},
          sort_keys=True, allow_nan=False), flush=True)


if __name__ == '__main__':
    main()
