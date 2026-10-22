"""SOURCE ONLY. Root executes under 1CPU/256MiB/120s/16MiB.
Full six-file L2 method comparison, tuple-frontier reconstruction plus a
separate bipartite vertex-choice meet-in-the-middle enumeration on COMPLETE.
Never imports or executes the producer's scientific source.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import sys
import time

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE')
SCIENCE = BASE/'lanes/P60_CODEX2/p60_exact_ice_fixedpoint_count_v001.py'
CALLER = BASE/'KNOWLEDGE/ROOT_EXECUTION_BLOCK_V001/P60_FIXEDPOINT_L2_ROOT_PRODUCER_V001.py'
PINS = {SCIENCE: '9bfed34cbc4c8695ecf8528598f6532f6980de91de12c139cea2e58332952533',
        CALLER: '758ca2c8e8b1da8c7c82cdec53ff7f21203fdbfee34296410147523ac7db5d45'}
FILES = {'START.json', 'SOURCE_SNAPSHOT.py', 'ACTUAL_PRE.json',
         'PROGRESS.jsonl', 'ACTUAL_RETURN.json', 'FINISH.json'}
CAPS = {'cpu': 1, 'rss_bytes': 268435456, 'seconds': 120, 'output_bytes': 16777216}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pairs(items):
    result = {}
    for k, v in items:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result


def decode(raw):
    def bad(value):
        raise ValueError('nonfinite JSON '+value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)


def exact(actual, expected, label):
    need(type(actual) is type(expected), 'type '+label)
    if isinstance(expected, dict):
        need(actual.keys() == expected.keys(), 'keys '+label)
        for k in expected:
            exact(actual[k], expected[k], label+'/'+k)
    elif isinstance(expected, list):
        need(len(actual) == len(expected), 'length '+label)
        for i, v in enumerate(expected):
            exact(actual[i], v, label+'/'+str(i))
    else:
        need(actual == expected, 'value '+label)


def graph(sector, axes):
    """L2 arithmetic bit coordinates, not product-point lookup source code."""
    shifts = (0, 4, 2, 1)
    cuts = (0, 16, 8, 4)
    records = []
    for edge in range(32):
        origin, colour = divmod(edge, 4)
        if sector == 'old' or edge not in cuts:
            records.append([edge, origin, 8+(origin ^ shifts[colour])])
    if sector == 'Born':
        for j, edge in enumerate(cuts):
            origin = edge//4
            records.extend([[32+2*j, origin, 17], [33+2*j, 16, 8+origin]])
    records.sort()
    def vertex(v):
        if v >= 16:
            return v
        side, number = divmod(v, 8)
        out = sum(((number >> (2-a)) & 1) << (2-axes[a]) for a in range(3))
        return 8*side+out
    by_endpoints = {(a, b): edge for edge, a, b in records}
    image = {edge: by_endpoints[vertex(a), vertex(b)] for edge, a, b in records}
    need(set(image) == set(image.values()), 'independent full edge bijection')
    remaining = set(image)
    orbits = []
    while remaining:
        first = min(remaining)
        orbit = [first]
        following = image[first]
        while following != first:
            need(following not in orbit, 'edge cycle simple')
            orbit.append(following)
            following = image[following]
        remaining.difference_update(orbit)
        orbits.append(sorted(orbit))
    boundary = [set() for _ in range(3)]
    for edge, a, b in records:
        if edge < 32:
            cell, colour = divmod(edge, 4)
            if colour and cell & shifts[colour]:
                boundary[colour-1].add(edge)
    return records, image, orbits, boundary, set(cuts)


def frontier(sector, axes, records, image, orbits, boundary, cuts, guard):
    """Ordinary tuple exponents, no producer packed degrees/base-radix key.
    Retain a fixed full vertex tuple with discharged coordinates zeroed.
    Cap/refusal depends on the first orbit exceeding the unique-key bound,
    not on the order in which equal coefficients are added.
    """
    nv = 16 if sector == 'old' else 18
    ends = {edge: (a, b) for edge, a, b in records}
    incidence = []
    last = [-1]*nv
    for index, orbit in enumerate(orbits):
        contribution = [0]*nv
        for edge in orbit:
            for v in ends[edge]:
                contribution[v] += 1
                last[v] = index
        incidence.append(contribution)
    need(all(i >= 0 for i in last), 'all vertices incident')
    table = {((0,)*nv, (0, 0, 0), 0): 1}
    peak = 1
    progress = []
    for index, orbit in enumerate(orbits):
        retiring = tuple(v for v in range(nv) if last[v] == index)
        dk = tuple(len(set(orbit) & boundary[a]) for a in range(3))
        dy = len(set(orbit) & cuts) if sector == 'old' else 0
        output = {}
        for ordinal, ((degrees, winding, marked), coefficient) in enumerate(table.items()):
            if ordinal % 256 == 0:
                guard()
            for take in (0, 1):
                d = [value+take*incidence[index][v] for v, value in enumerate(degrees)]
                if any(value > 2 for value in d) or any(d[v] != 2 for v in retiring):
                    continue
                k = tuple(winding[a]+take*dk[a] for a in range(3))
                if any(value > 4 for value in k):
                    continue
                y = marked+take*dy
                need(0 <= y <= 4, 'complete marked cut degree')
                for v in retiring:
                    d[v] = 0
                key = (tuple(d), k, y)
                if key not in output and len(output) == 65536:
                    return {'schema': 'P60_EXACT_ICE_FIXEDPOINT_V001',
                            'status': 'COUNT_CAP_REFUSAL', 'L': 2, 'sector': sector,
                            'axis_permutation': axes,
                            'message': 'complete coefficient live-table cap65536',
                            'completed_orbits': index, 'total_orbits': len(orbits),
                            'peak_completed_live_keys': peak, 'live_cap': 65536,
                            'dimension_inferred_from_partial_table': False,
                            'spectrum_authorized': False, 'physical_release': False}, progress
                output[key] = output.get(key, 0)+coefficient
        table = output
        peak = max(peak, len(table))
        progress.append({'kind': 'EXACT_COEFFICIENT_FRONTIER',
                         'completed_orbits': index+1, 'total_orbits': len(orbits),
                         'live_keys': len(table), 'live_cap': 65536,
                         'partial_table_is_dimension': False})
        guard()
    counts, eligible = {}, {}
    for (degrees, k, y), coefficient in table.items():
        need(not any(degrees), 'all degree constraints discharged')
        name = ','.join(map(str, k))
        counts[name] = counts.get(name, 0)+coefficient
        if sector == 'old' and y == 2:
            eligible[name] = eligible.get(name, 0)+coefficient
    return {'schema': 'P60_EXACT_ICE_FIXEDPOINT_V001', 'status': 'COMPLETE_EXACT_COUNT',
            'L': 2, 'sector': sector, 'axis_permutation': axes,
            'all_edges_stable_ids': records,
            'edge_permutation': [[edge, image[edge]] for edge in sorted(image)],
            'complete_edge_orbits': orbits, 'all_K_fixed_counts': counts,
            'all_K_eligible_old_fixed_counts': eligible,
            'total_fixed_configurations': sum(counts.values()),
            'peak_live_keys': peak, 'completed_orbits': len(orbits),
            'scope': 'S3_SUBGROUP_ICE_FIXEDPOINTS_NOT_COMPLETE_OLD_RING_MOMENTUM_IRREPS',
            'physical_release': False}, progress


def vertex_enumeration(sector, records, orbits, boundary, cuts, guard):
    """Independent full edge masks: choose two of four edges at EACH A vertex.
    A choices are disjoint edge sets. Group each half by B degrees; join only
    complementary vectors adding to2. Each ice configuration appears once.
    Then filter the complete masks by permutation invariance, not by an
    orbit-polynomial recurrence. No numerical oracle is supplied externally.
    """
    left = list(range(8)) + ([16] if sector == 'Born' else [])
    right = list(range(8, 16)) + ([17] if sector == 'Born' else [])
    ridx = {v: i for i, v in enumerate(right)}
    choices = []
    for vertex in left:
        incident = [(edge, ridx[b]) for edge, a, b in records if a == vertex]
        need(len(incident) == 4, 'independent four-valent A vertex')
        choices.append(list(itertools.combinations(incident, 2)))
    def half(rows):
        groups = {}
        for ordinal, selection in enumerate(itertools.product(*rows)):
            if ordinal % 256 == 0:
                guard()
            degrees = [0]*len(right)
            mask = 0
            for pair in selection:
                for edge, b in pair:
                    degrees[b] += 1
                    mask |= 1 << edge
            if max(degrees) <= 2:
                groups.setdefault(tuple(degrees), []).append(mask)
        return groups
    middle = len(choices)//2
    first = half(choices[:middle])
    second = half(choices[middle:])
    orbit_masks = [sum(1 << edge for edge in orbit) for orbit in orbits]
    kmasks = [sum(1 << edge for edge in edges) for edges in boundary]
    cutmask = sum(1 << edge for edge in cuts)
    counts, eligible = {}, {}
    complete_ice = 0
    fixed = 0
    for degrees, left_masks in first.items():
        complement = tuple(2-d for d in degrees)
        for a in left_masks:
            for b in second.get(complement, ()):
                complete_ice += 1
                if complete_ice % 256 == 0:
                    guard()
                mask = a | b
                if any(mask & orbit not in (0, orbit) for orbit in orbit_masks):
                    continue
                fixed += 1
                name = ','.join(str(bin(mask & m).count('1')) for m in kmasks)
                counts[name] = counts.get(name, 0)+1
                if sector == 'old' and bin(mask & cutmask).count('1') == 2:
                    eligible[name] = eligible.get(name, 0)+1
    # Complementing every edge preserves degree2, fixedness and eligible y2.
    for table in (counts, eligible):
        for name, value in table.items():
            opposite = ','.join(str(4-int(k)) for k in name.split(','))
            need(table.get(opposite, 0) == value, 'complete complement bijection')
    guard()
    return counts, eligible, {'all_ice_masks_examined': complete_ice,
                              'all_fixed_masks_counted': fixed,
                              'full_vertex_choice_enumeration': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sector', choices=['old', 'Born'], required=True)
    parser.add_argument('--axes', choices=['012', '021', '102', '120', '201', '210'], required=True)
    args = parser.parse_args()
    started = time.monotonic()
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        need(time.monotonic()-started <= 120 and rss <= 268435456, 'checker actual caps')
    def raw_file(path, cap):
        guard()
        need(path.is_absolute() and path.resolve() == path and not path.is_symlink()
             and path.is_file() and path.stat().st_size <= cap, 'plain bounded input '+str(path))
        with path.open('rb') as stream:
            raw = stream.read(cap+1)
        need(len(raw) <= cap, 'read byte cap')
        return raw
    need(args.archive.is_absolute() and args.archive.resolve() == args.archive
         and args.archive.is_dir() and not args.archive.is_symlink(), 'literal archive')
    need(args.output.is_absolute() and args.output.resolve() == args.output
         and not args.output.exists() and not args.output.is_symlink(), 'fresh literal output')
    need({p.name for p in args.archive.iterdir()} == FILES, 'complete six-file census')
    sources = {path: raw_file(path, 32768) for path in PINS}
    for path, raw in sources.items():
        need(sha(raw) == PINS[path], 'complete source pin '+str(path))
    saved = {name: raw_file(args.archive/name, 8*2**20) for name in FILES}
    need(sum(map(len, saved.values())) <= 8*2**20, 'whole scientific cap')
    need(saved['SOURCE_SNAPSHOT.py'] == sources[SCIENCE], 'full source snapshot')
    start = decode(saved['START.json'])
    pid = start.get('pid')
    need(type(pid) is int and pid > 0, 'original PID metadata')
    exact(start, {'schema': 'P60_FIXEDPOINT_L2_ROOT_CALL_V001', 'pid': pid,
                  'source': {'path': str(SCIENCE), 'sha256': PINS[SCIENCE]},
                  'runner_sha256': PINS[CALLER], 'caps': CAPS,
                  'external_supervisor_required': True, 'scientific_acceptance': False}, 'START')
    axes = list(map(int, args.axes))
    exact(decode(saved['ACTUAL_PRE.json']), {'function': 'fixed_point', 'L': 2,
          'sector': args.sector, 'axis_permutation': axes, 'live_cap': 65536,
          'retention': 'all final counts and graph/orbits; progress stores orbit summaries, not intermediate tables'}, 'PRE')
    records, image, orbits, boundary, cuts = graph(args.sector, axes)
    expected, progress = frontier(args.sector, axes, records, image, orbits, boundary, cuts, guard)
    lines = saved['PROGRESS.jsonl'].splitlines()
    need(not saved['PROGRESS.jsonl'] or saved['PROGRESS.jsonl'].endswith(b'\n'), 'complete progress newline')
    need(all(lines) and len(lines) <= 36, 'bounded nonempty progress records')
    exact([decode(line) for line in lines], progress, 'every orbit progress')
    enumeration = {'full_vertex_choice_enumeration': False,
                   'reason': 'refusal contains no dimension to certify'}
    if expected['status'] == 'COMPLETE_EXACT_COUNT':
        counts, eligible, enumeration = vertex_enumeration(args.sector, records, orbits, boundary, cuts, guard)
        exact(expected['all_K_fixed_counts'], counts, 'independent complete vertex enumeration')
        exact(expected['all_K_eligible_old_fixed_counts'], eligible, 'independent eligible vertex enumeration')
        need(sum(counts.values()) == expected['total_fixed_configurations'], 'all counts summed')
    exact(decode(saved['ACTUAL_RETURN.json']), {'exception': None, 'value': expected}, 'complete RETURN')
    manifest = {name: {'bytes': len(raw), 'sha256': sha(raw)} for name, raw in saved.items() if name != 'FINISH.json'}
    exact(decode(saved['FINISH.json']), {'status': 'RAW_L2_METHOD_PENDING_DISTINCT_SAVED_COMPARISON',
          'pid': pid, 'progress_records': len(progress), 'source_closing_bytes_match': True,
          'files_before_finish': manifest, 'subgroup_dimensions_called': False,
          'native_L4_L5_release': False, 'physical_release': False}, 'FINISH')
    for path, raw in sources.items():
        need(raw_file(path, 32768) == raw, 'source closing bytes')
    for name, raw in saved.items():
        need(raw_file(args.archive/name, 8*2**20) == raw, 'every saved file closing bytes')
    need({p.name for p in args.archive.iterdir()} == FILES, 'closing whole census')
    report = {'schema': 'CODEX3_P60_L2_COMPLETE_INDEPENDENT_COMPARISON_V001',
              'status': 'PASS_COMPLETE_SAVED_COMPARISON', 'L': 2, 'sector': args.sector,
              'axis_permutation': axes, 'actual_scientific_status': expected['status'],
              'positive_complete_count_case': expected['status'] == 'COMPLETE_EXACT_COUNT',
              'all_six_scientific_files_compared': True, 'all_completed_orbit_summaries_compared': len(progress),
              'independent_enumeration': enumeration,
              'complete_actual_return': expected,
              'input_files': {name: {'bytes': len(raw), 'sha256': sha(raw)} for name, raw in saved.items()},
              'source_pins': {str(path): digest for path, digest in PINS.items()},
              'intermediate_tables_archived_claim': False,
              'producer_actual_runtime_authenticated_here': False,
              'root_external_runtime_and_twelve_case_gate_required': True,
              'subgroup_dimensions_authorized': False, 'native_L4_L5_release': False,
              'physical_release': False}
    data = (json.dumps(report, indent=2, allow_nan=False)+'\n').encode()
    need(len(data) <= 8*2**20, 'complete checker scientific output cap')
    guard()
    args.output.mkdir(exist_ok=False)
    with (args.output/'INDEPENDENT_REPORT.json').open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({'status': report['status'], 'actual_scientific_status': expected['status'],
                      'report_sha256': sha(data)}, sort_keys=True))


if __name__ == '__main__':
    main()
