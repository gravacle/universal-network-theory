"""Occupancy-guided long alternating-loop ("worm") whole-path occupancy transport (Claude2, c2v001).

Proposal replacement only (ROOT_DECISIONS_A1_A2_2026-10-17_V001.md, A2 "Next sampling remedy"):
it takes the 10% current-graph cycle slot; the native target (operator V003 Hamiltonian, weights,
reads, imaginary-time measure of the pinned V006 sampler) is unchanged.  The actual pinned V006
sampler API is injected as `sampler`; the operator's public keyword-only `state_labels` is
injected as `state_labels`.  No sampler, schedule or global-function mutation.

Eligible coloured graph (a function of the WHOLE path).  An edge (A label, B label) is eligible
iff it is present in EVERY dwell's current graph and its occupancy is the same in EVERY dwell; its
colour is that occupancy (1 occupied, 0 unoccupied).  Flipping an alternating loop of eligible
edges in every dwell keeps every such edge present with constant (complemented) occupancy and
leaves every other edge untouched, so the eligible set is identical for the reverse path and the
colours differ exactly on the loop (verified, not assumed).

Walk (fixed rule, every choice uniform, never resampled).  Start vertex v0 uniform from the fixed
ORIGINAL A+B roster supplied by root; first edge uniform among the viable eligible OCCUPIED edges at
v0; then repeatedly, at the current vertex, uniform among the viable eligible edges of the alternate
colour (unoccupied after occupied, occupied after unoccupied).  The arrival edge is excluded by
colour.  Viable (declared rule LOOKAHEAD = True, one-step lookahead): the edge's other endpoint is
already visited (a closure) or has at least one eligible edge of the colour that would be required
next there; with LOOKAHEAD = False every alternate-colour eligible edge is a candidate (the literal
rule; both are exactly enumerated by the fixtures).  A visited vertex other than v0 has edges of
both colours, so viability depends only on per-vertex colour counts, which an alternating loop
preserves, and on v0; forward and reverse counts therefore coincide on a bipartite eligible graph
(FORMAL), but the reverse counts are recomputed on every proposal, never assumed, and a
mismatch is counted (worm_loop_walk_ratio_nonunit) and enters the ratio.
The walk stops at the FIRST arrival at an already visited vertex w; the loop is the closed part
w -> ... -> w (any even length >= 4, contractible or winding), the tail v0 -> w is NOT flipped.
On a bipartite graph every such closure is alternating at w (checked).  Empty start roster, dead
end and the declared step cap MAX_WALK_STEPS (tail + loop edges) are self loops.

Exact Hastings factor.  q(walk) = 1/|roster| * prod_i 1/n_i with n_i the number of uniform
candidates at step i.  The reverse walk from the transformed path that regenerates the same loop
is: same v0, same tail, then the loop in the opposite orientation, closing at w.  Its branching
counts are recomputed from scratch on the transformed reference colouring by walk_branch_product
(which also verifies every step and that the first revisit is the final arrival); if it cannot be
generated the proposal is a self loop.  The products are exact integers.

    log MH = log(prod n_forward) - log(prod n_reverse) - sum_i dt_i (D_new_i - D_old_i)
             + sum_events log(W_new / W_old)

Dwell transform.  For every dwell the labelled state from state_labels has the loop edges'
occupancy toggled and is canonicalised by the sampler (operator canonical_state_key); the new key
must differ from the old key ONLY in the incidence component, by the SAME mask in every dwell,
equal to the union of the single-bit masks of the actual native positive-rate flip marks of the
loop edges at the reference dwell (a missing native flip mark there is a contract failure).  The
labelled round trip is checked.  Every stored event is replayed with its exact kind and owner on
the transformed states (target and stored W verified on the old path, transformed target
verified, transformed W taken from the actual channel); an impossible replay is a self loop.
Times and event count are preserved; no event is inserted, so no amplitude, event-count or time
density factor enters.  Zero Metropolis rejections are expected only where D and every replayed W
are exactly invariant; this module never assumes it -- the ratio is always computed.

Atomicity follows admission_residence_transport_c3v001.py: 'before'/'between' budget checkpoints,
no mutation of the input path, cumulative read-integral diagnostics written only after the
'before ... atomic commit' checkpoint.  No mixing or ergodicity claim.
"""
import math

MODULE_VERSION = 'worm_c2v001'
PREFIX = 'worm_loop_'
MAX_WALK_STEPS = 1024  # declared cap on tail+loop edges; reaching it without closure is a self loop
LOOKAHEAD = True  # declared walk rule: one-step viability lookahead (see module docstring)
LENGTH_BUCKETS = ((4, 4), (6, 6), (8, 8), (10, 16), (18, 32), (34, 64), (66, 128), (130, None))
REFERENCE_SCAFFOLD = ('admission_residence_transport_c3v001.py '
                      '5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653')


def _other(edge, vertex):
    a, b = edge
    if vertex == a:
        return b
    if vertex == b:
        return a
    raise ValueError('vertex not on edge')


def eligible_colouring(dwell_labels):
    """{edge: colour} for edges present in every dwell with constant occupancy (colour 1/0).

    dwell_labels: sequence of mappings with labelled 'edges' and 'occupied' collections.
    Deterministic, a function of the labelled dwell configurations only.
    """
    if not dwell_labels:
        raise ValueError('at least one dwell required')
    edge_sets = [frozenset(tuple(e) for e in d['edges']) for d in dwell_labels]
    occ_sets = [frozenset(tuple(e) for e in d['occupied']) for d in dwell_labels]
    for es, os in zip(edge_sets, occ_sets):
        if not os <= es:
            raise ValueError('occupied edge outside its dwell graph')
    common = frozenset.intersection(*edge_sets)
    out = {}
    for e in sorted(common):
        c = e in occ_sets[0]
        if all((e in os) == c for os in occ_sets):
            out[e] = 1 if c else 0
    return out


def incidence_lists(colouring):
    """vertex -> (sorted unoccupied edges, sorted occupied edges) of the eligible graph."""
    inc = {}
    for e in sorted(colouring):
        c = colouring[e]
        for v in e:
            inc.setdefault(v, ([], []))[c].append(e)
    return inc


def bipartite_labelled(colouring):
    """True iff no label is both a first (A) and a second (B) endpoint, and no self edge."""
    first = {e[0] for e in colouring}
    second = {e[1] for e in colouring}
    return not (first & second) and all(e[0] != e[1] for e in colouring)


def _viable(inc, candidates, need, visited, lookahead):
    """Candidates whose far endpoint is visited or offers an eligible edge of colour 1-need."""
    if not lookahead:
        return candidates
    out = []
    for e, w in candidates:
        if w in visited or inc[w][need ^ 1]:
            out.append((e, w))
    return out


def _step_candidates(inc, vertex, need, visited, lookahead):
    cands = [(e, _other(e, vertex)) for e in inc.get(vertex, ([], []))[need]]
    return [e for e, _ in _viable(inc, cands, need, visited, lookahead)]


def grow_walk(colouring, roster, integers, max_steps, lookahead=None):
    """Sample the walk.  integers(n) must return a uniform int in [0, n).

    Returns a dict with 'status' in ('closed', 'empty_start', 'dead_end', 'length_cap'); a closed
    walk also carries start, edges (ordered), closure (index of the first loop edge), counts
    (uniform candidate count of every edge choice, start edge first) and branch_product.
    """
    lookahead = LOOKAHEAD if lookahead is None else lookahead
    start = roster[integers(len(roster))]
    inc = incidence_lists(colouring)
    position = {start: 0}
    candidates = _step_candidates(inc, start, 1, position, lookahead)
    if not candidates:
        return {'status': 'empty_start', 'start': start}
    counts = [len(candidates)]
    edge = candidates[integers(len(candidates))]
    edges = [edge]
    vertex = _other(edge, start)
    need = 0  # colour required for the next edge
    while True:
        if vertex in position:
            closure = position[vertex]
            product = 1
            for n in counts:
                product *= n
            return {'status': 'closed', 'start': start, 'edges': edges, 'closure': closure,
                    'closure_vertex': vertex, 'counts': counts, 'branch_product': product}
        if len(edges) >= max_steps:
            return {'status': 'length_cap', 'start': start, 'steps': len(edges)}
        position[vertex] = len(edges)
        candidates = _step_candidates(inc, vertex, need, position, lookahead)
        if not candidates:
            return {'status': 'dead_end', 'start': start, 'steps': len(edges)}
        counts.append(len(candidates))
        edge = candidates[integers(len(candidates))]
        edges.append(edge)
        vertex = _other(edge, vertex)
        need ^= 1


def walk_branch_product(colouring, roster, start, edges, max_steps, lookahead=None):
    """Exact integer prod n_i of generating `edges` from `start` under grow_walk, or None.

    Verifies: start in roster; every edge eligible, incident to the current vertex and of the
    required colour; no revisit before the final edge; the final edge arrives at a visited vertex;
    the step cap is respected.  The 1/|roster| start factor is common to both directions.
    """
    lookahead = LOOKAHEAD if lookahead is None else lookahead
    if start not in roster or not edges or len(edges) > max_steps:
        return None
    inc = incidence_lists(colouring)
    vertex, need, product = start, 1, 1
    seen = {start}
    for i, edge in enumerate(edges):
        if edge not in colouring or colouring[edge] != need or vertex not in edge:
            return None
        candidates = _step_candidates(inc, vertex, need, seen, lookahead)
        if edge not in candidates:
            return None
        product *= len(candidates)
        vertex = _other(edge, vertex)
        last = i == len(edges) - 1
        if (vertex in seen) != last:
            return None
        seen.add(vertex)
        need ^= 1
    return product


def reverse_edges(edges, closure):
    """Reverse walk regenerating the same loop: same tail, loop in the opposite orientation."""
    return list(edges[:closure]) + list(reversed(edges[closure:]))


def loop_contract(colouring, loop):
    """Alternating simple even loop of distinct eligible edges, every loop vertex of loop degree 2."""
    if len(loop) < 4 or len(loop) % 2 or len(set(loop)) != len(loop):
        return False
    if any(e not in colouring for e in loop):
        return False
    for a, b in zip(loop, loop[1:] + loop[:1]):
        if colouring[a] == colouring[b] or not set(a) & set(b):
            return False
    degree = {}
    for e in loop:
        for v in e:
            degree[v] = degree.get(v, 0) + 1
    return set(degree.values()) == {2} and len(degree) == len(loop)


def length_bucket(n):
    for lo, hi in LENGTH_BUCKETS:
        if n >= lo and (hi is None or n <= hi):
            return str(lo) + ('_up' if hi is None else ('' if hi == lo else '_' + str(hi)))
    return 'other'


def move(run, path, rng, diag, sampler, owner_roster, state_labels):
    """One worm-loop whole-path proposal; returns (path, 'changed') or (path, 'rejected')."""
    measurement = diag['sweeps_completed'] >= run['burn_in_sweeps']

    def tick(name, amount=1):
        key = PREFIX + name
        diag[key] = diag.get(key, 0) + amount
        if measurement:
            mkey = PREFIX + 'measurement_' + name
            diag[mkey] = diag.get(mkey, 0) + amount

    def fail(message):
        raise sampler._Stop('failed', run['stage'], message)

    def terminal(message):
        raise sampler._Stop('incomplete', run['stage'], message)

    def reject(reason):
        tick(reason)
        tick('rejected')
        return path, 'rejected'

    def key_contract(key):
        if not isinstance(key, tuple) or len(key) != 7 or any(type(v) is not int or v < 0 for v in key):
            fail('Requires actual operatorV003 seven-int canonical key')

    def mark(state, kind, owner):
        sampler._budget_check(run, 'before', 'worm-loop marked enumeration')
        groups = sampler._record_groups(run, kind, owner)
        if not groups:
            fail('Worm-loop mark has no permanent descriptor groups')
        cs, _ = sampler._palette_channels(run, state, groups)
        return sampler._unique_mark(run, cs, kind, owner, 'worm-loop replay')

    def labels_of(state):
        try:
            lab = dict(state_labels(context=run['context'], state=state))
        except sampler._Stop:
            raise
        except Exception as exc:
            fail('state_labels raised ' + type(exc).__name__ + ': ' + str(exc))
        if 'edges' not in lab or 'occupied' not in lab:
            fail('state_labels lacks labelled edges/occupied')
        return lab

    def integers(n):
        return int(rng.integers(0, n))

    sampler._budget_check(run, 'before', 'worm-loop proposal')
    if (not isinstance(owner_roster, tuple) or not owner_roster or
            len(set(owner_roster)) != len(owner_roster) or not callable(state_labels)):
        fail('Fixed unique original A+B roster and public state_labels binding required')
    segs, events, times = path['segments'], path['events'], path['times']
    k = len(events)
    if len(times) != k or len(segs) != k + 1:
        fail('Malformed closed path')
    if k > run['caps']['max_events_per_path']:
        terminal('Existing path exceeds event cap')
    sampler._check_times(run, times, run['beta'])
    if not sampler._keys_equal(run, segs[0]['key'], segs[-1]['key']):
        fail('Original path not closed')
    tick('attempts')
    labels = []
    for seg in segs:
        sampler._budget_check(run, 'between', 'worm-loop dwell labels')
        key_contract(seg['key'])
        labels.append(labels_of(seg['state']))
    try:
        colouring = eligible_colouring(labels)
    except ValueError as exc:
        fail('Eligible colouring: ' + str(exc))
    if not bipartite_labelled(colouring):
        fail('Eligible current graph is not labelled bipartite (A label, B label)')
    tick('eligible_edges_sum', len(colouring))
    walk = grow_walk(colouring, owner_roster, integers, MAX_WALK_STEPS)
    if walk['status'] != 'closed':
        return reject(walk['status'])
    start, edges, closure = walk['start'], walk['edges'], walk['closure']
    tail, loop = edges[:closure], edges[closure:]
    if not loop_contract(colouring, loop):
        fail('Worm closure is not a simple alternating even loop')
    forward_product = walk['branch_product']
    if walk_branch_product(colouring, owner_roster, start, edges, MAX_WALK_STEPS) != forward_product:
        fail('Forward walk probability is not reproducible')
    tick('closed_walk')

    # Native witness at the reference dwell: every loop edge carries the actual positive-rate flip
    # mark and toggles exactly one incidence bit; the union is the whole-path incidence mask.
    key0 = segs[0]['key']
    mask = 0
    for e in loop:
        sampler._budget_check(run, 'between', 'worm-loop native flip witness')
        ch = mark(segs[0]['state'], 'flip', ('flip', ('edge', e)))
        if ch is None:
            fail('Eligible loop edge lacks a native positive-rate flip mark at the reference dwell')
        nk = sampler._target_key(run, ch)
        key_contract(nk)
        bit = key0[2] ^ nk[2]
        if (bit <= 0 or bit & (bit - 1) or bit & mask or
                any(key0[j] != nk[j] for j in (0, 1, 3, 4, 5, 6))):
            fail('Literal native flip/key contract failed')
        mask |= bit

    loopset = frozenset(loop)
    transformed, new_labels = [], []
    for old, lab in zip(segs, labels):
        sampler._budget_check(run, 'between', 'worm-loop dwell transforms')
        edgeset = frozenset(tuple(e) for e in lab['edges'])
        occupied = frozenset(tuple(e) for e in lab['occupied'])
        if not loopset <= edgeset or any((e in occupied) != bool(colouring[e]) for e in loop):
            fail('Eligible loop edge absent or non-constant in a dwell')
        new_occupied = occupied ^ loopset
        mapping = dict(lab)
        mapping['occupied'] = tuple(sorted(new_occupied))
        new_key = sampler._state_key(run, mapping)
        key_contract(new_key)
        if (any(new_key[j] != old['key'][j] for j in (0, 1, 3, 4, 5, 6)) or
                (old['key'][2] ^ new_key[2]) != mask):
            fail('Worm whole-path key contract failed (graph/resources changed or mask differs)')
        new = sampler._segment_core(run, new_key)
        if not sampler._keys_equal(run, new['key'], new_key):
            fail('Segment canonical key differs from transformed key')
        back = labels_of(new['state'])
        if (frozenset(tuple(e) for e in back['occupied']) != new_occupied or
                frozenset(tuple(e) for e in back['edges']) != edgeset):
            fail('Transformed labelled round trip failed')
        transformed.append(new)
        new_labels.append(back)
    if not sampler._keys_equal(run, transformed[0]['key'], transformed[-1]['key']):
        fail('Transformed path not closed')
    try:
        reverse_colouring = eligible_colouring(new_labels)
    except ValueError as exc:
        fail('Transformed eligible colouring: ' + str(exc))
    if (set(reverse_colouring) != set(colouring) or
            any(reverse_colouring[e] != colouring[e] ^ (1 if e in loopset else 0) for e in colouring)):
        fail('Eligible coloured graph is not invariant up to the loop flip')
    reverse_product = walk_branch_product(reverse_colouring, owner_roster, start,
                                          reverse_edges(edges, closure), MAX_WALK_STEPS)
    if reverse_product is None:
        return reject('reverse_walk_impossible')

    ends = [0.] + list(times) + [run['beta']]
    walk_term = math.log(forward_product) - math.log(reverse_product)
    d_terms = [-(ends[i+1]-ends[i]) * (new['D']-old['D'])
               for i, (old, new) in enumerate(zip(segs, transformed))]
    w_terms, new_events = [], []
    for i, ev in enumerate(events):
        sampler._budget_check(run, 'between', 'worm-loop marked event replay')
        before = mark(segs[i]['state'], ev['kind'], ev['owner'])
        if (before is None or
                not sampler._keys_equal(run, sampler._target_key(run, before), segs[i+1]['key']) or
                before['W'] != ev['W']):
            fail('Stored primitive mark/rate inconsistent')
        after = mark(transformed[i]['state'], ev['kind'], ev['owner'])
        if after is None or not sampler._keys_equal(run, sampler._target_key(run, after), transformed[i+1]['key']):
            return reject('event_replay_guard_or_target')
        w_terms.append(math.log(after['W']) - math.log(before['W']))
        new_events.append(sampler._event_from_channel(run, after))
    log_d = math.fsum(d_terms)
    log_w = math.fsum(w_terms)
    logratio = math.fsum([walk_term] + d_terms + w_terms)
    if not math.isfinite(logratio):
        fail('Nonfinite worm-loop MH ratio')
    tick('legal_transport')
    if forward_product != reverse_product:
        tick('walk_ratio_nonunit')
    if logratio == 0.0:
        tick('log_mh_exactly_zero')
    elif logratio < 0.0:
        tick('log_mh_negative')
    diag[PREFIX + 'last_proposal'] = dict(start=start, loop_length=len(loop), tail_length=len(tail),
        forward_branch_product=forward_product, reverse_branch_product=reverse_product,
        log_walk_ratio=walk_term, log_D_ratio=log_d, log_W_ratio=log_w, log_mh_ratio=logratio)
    if logratio < 0 and not float(rng.random()) < math.exp(logratio):
        return reject('metropolis')
    delta = [math.fsum((ends[i+1]-ends[i]) * (float(new['row'][j])-float(old['row'][j]))
                       for i, (old, new) in enumerate(zip(segs, transformed)))
             for j in range(len(segs[0]['row']))]
    if not all(math.isfinite(v) for v in delta):
        fail('Nonfinite worm-loop read change')
    sampler._budget_check(run, 'before', 'worm-loop atomic commit')
    pending = {}
    for scope in [''] + (['measurement_'] if measurement else []):
        for name, values in (('read_integral_change_sum', delta),
                             ('absolute_read_integral_change_sum', [abs(v) for v in delta])):
            key = PREFIX + scope + name
            prior = diag.get(key, [0.] * len(delta))
            if len(prior) != len(delta):
                fail('Read-change diagnostic length differs from the tracked reads')
            pending[key] = [a + v for a, v in zip(prior, values)]
    if not all(math.isfinite(v) for vs in pending.values() for v in vs):
        fail('Nonfinite cumulative worm-loop read change')
    diag.update(pending)
    tick('accepted_changed')
    tick('loop_length_' + length_bucket(len(loop)) + '_accepted_changed')
    tick('accepted_loop_edges_sum', len(loop))
    tick('accepted_tail_edges_sum', len(tail))
    return {'segments': transformed, 'events': new_events, 'times': list(times)}, 'changed'
