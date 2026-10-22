"""Synthetic explicit-state toy of the injected V006 sampler API and operator labels (fixture only).

Never imports the native operator or sampler.  Keys mimic operator V003: seven nonnegative ints
(slots, edgeset, inc, p, q, s, donors) over fixed codes.  The toy target deliberately is NOT
invariant under alternating loops: edge-dependent Delta_e and a source on an edge-weighted read
enter D, and every event rate depends on the occupancy of specific neighbouring edges, so the
Metropolis ratio and event-W replay are exercised.  Births rewire two cut edges into two children
(each child inherits one cut bit; census exactly one occupied), so the graph changes along paths.
"""
import math


class ToyStop(Exception):
    def __init__(self, status, stage, message):
        Exception.__init__(self, message)
        self.status, self.stage, self.message = status, stage, message


class ToyBudgetStop(ToyStop):
    def __init__(self, stage, checkpoint):
        ToyStop.__init__(self, 'incomplete', stage, 'INCOMPLETE_BUDGET at ' + checkpoint)
        self.checkpoint = checkpoint


def _bits(x):
    i = 0
    while x:
        if x & 1:
            yield i
        x >>= 1
        i += 1


class Toy:
    """Toy model + the sampler API subset used by the worm module."""
    _Stop = ToyStop

    def __init__(self, *, A, B, base_edges, births=(), zero_h=(), wrong_key=False,
                 Ud=.3, lam=.2, j=.15, t=.7, eps=.4, flip_occ=.05, hop_occ=.25):
        self.A, self.B = tuple(A), tuple(B)
        self.vertices = self.A + self.B
        self.vid = {v: i for i, v in enumerate(self.vertices)}
        universe = set(tuple(e) for e in base_edges)
        self.births = []
        for n, b in enumerate(births):
            cut, children = tuple(map(tuple, b['cut'])), tuple(map(tuple, b['children']))
            universe |= set(cut) | set(children)
            self.births.append({'j': n, 'cut': cut, 'children': children})
        self.universe = tuple(sorted(universe))
        self.code = {e: i for i, e in enumerate(self.universe)}
        self.base_mask = sum(1 << self.code[tuple(e)] for e in base_edges)
        for e in self.universe:
            if e[0] not in self.A or e[1] not in self.B:
                raise ValueError('toy edges must be ordered (A, B)')
        n = len(self.universe)
        self.Delta = [.3 + .17 * ((7 * i) % 5) for i in range(n)]
        self.c1 = [((3 * i) % 7 - 3) / 5. for i in range(n)]
        self.c2 = [.2 + .11 * ((5 * i) % 4) for i in range(n)]
        self.h = [0. if self.universe[i] in set(map(tuple, zero_h)) else .5 + .1 * (i % 3) for i in range(n)]
        self.Ud, self.lam, self.j, self.t, self.eps = Ud, lam, j, t, eps
        self.flip_occ, self.hop_occ = flip_occ, hop_occ
        self.wrong_key = wrong_key
        self.checkpoints = 0
        self.trigger = None
        self.checkpoint_log = []
        self.context = object()

    # ---------------- labelled states -------------------------------------------------
    def labels_from_key(self, key):
        slots, edgeset, inc, p, q, s, dm = key
        return (('slots', tuple(sorted(_bits(slots)))),
                ('edges', tuple(self.universe[c] for c in _bits(edgeset))),
                ('occupied', tuple(self.universe[c] for c in _bits(inc))),
                ('carriers', tuple(self.vertices[v] for v in _bits(p))),
                ('records', tuple(self.vertices[v] for v in _bits(q))),
                ('spent', tuple(self.vertices[v] for v in _bits(s))),
                ('donors_ready', tuple(sorted(_bits(dm)))))

    def key_from(self, state):
        if isinstance(state, tuple) and len(state) == 7 and all(type(x) is int for x in state):
            key = state
        else:
            m = dict(state)
            edgeset = 0
            for e in m['edges']:
                edgeset |= 1 << self.code[tuple(e)]
            inc = 0
            for e in m['occupied']:
                inc |= 1 << self.code[tuple(e)]
            slots = sum(1 << x for x in m['slots'])
            p = sum(1 << self.vid[v] for v in m['carriers'])
            q = sum(1 << self.vid[v] for v in m['records'])
            s = sum(1 << self.vid[v] for v in m['spent'])
            dm = sum(1 << x for x in m['donors_ready'])
            key = (slots, edgeset, inc, p, q, s, dm)
        slots, edgeset, inc, p, q, s, dm = key
        if inc & ~edgeset:
            raise ValueError('occupied edge outside graph')
        for b in self.births:
            child = all((edgeset >> self.code[e]) & 1 for e in b['children'])
            cut = all((edgeset >> self.code[e]) & 1 for e in b['cut'])
            if child == cut or bool((slots >> b['j']) & 1) != child:
                raise ValueError('slot/graph inconsistency')
        return key

    def state_labels(self, *, context, state):
        if context is not self.context:
            raise ValueError('wrong context')
        return self.labels_from_key(self.key_from(state))

    # ---------------- toy native quantities ---------------------------------------------
    def degrees(self, key):
        d = {v: 0 for v in self.vertices}
        present = set()
        for c in _bits(key[1]):
            present.update(self.universe[c])
        for c in _bits(key[2]):
            a, b = self.universe[c]
            d[a] += 1
            d[b] += 1
        return d, present

    def occ(self, key, e):
        return (key[2] >> self.code[e]) & 1

    def present(self, key, e):
        return (key[1] >> self.code[e]) & 1

    def neighbour_load(self, key, e):
        """sum c2_f over OCCUPIED present edges f != e sharing an endpoint with e."""
        tot = []
        for c in _bits(key[2]):
            f = self.universe[c]
            if f != e and set(f) & set(e):
                tot.append(self.c2[c])
        return math.fsum(tot)

    def diagonal(self, key):
        d, present = self.degrees(key)
        p = key[3]
        terms = [self.Delta[c] for c in _bits(key[2])]
        terms += [self.Ud * (d[v] - 2) ** 2 for v in present]
        terms += [self.lam * d[self.vertices[v]] for v in _bits(p)]
        r1 = math.fsum(self.c1[c] for c in _bits(key[2]))
        terms.append(-self.j * r1)
        terms.append(.2 * bin(key[0]).count('1'))
        row = [r1, float(sum((d[v] - 2) ** 2 for v in present)), float(bin(key[2]).count('1'))]
        return math.fsum(terms), row

    def channels(self, key):
        out = []
        slots, edgeset, inc, p, q, s, dm = key
        for c in _bits(edgeset):
            e = self.universe[c]
            if self.h[c] > 0:
                W = self.h[c] * (1. + self.flip_occ * self.neighbour_load(key, e))
                out.append({'kind': 'flip', 'owner': ('flip', ('edge', e)),
                            'target': (slots, edgeset, inc ^ (1 << c), p, q, s, dm), 'W': W, 'has_key': True})
        for c in _bits(inc):
            a, b = self.universe[c]
            pa, pb = (p >> self.vid[a]) & 1, (p >> self.vid[b]) & 1
            if pa != pb:
                W = self.t * (1. + self.hop_occ * self.neighbour_load(key, (a, b)))
                out.append({'kind': 'hop', 'owner': ('hop', ('edge', (a, b))),
                            'target': (slots, edgeset, inc, p ^ (1 << self.vid[a]) ^ (1 << self.vid[b]), q, s, dm),
                            'W': W, 'has_key': True})
        for bth in self.births:
            jj, cut, ch = bth['j'], bth['cut'], bth['children']
            owner = ('birth', jj, cut)
            if not (slots >> jj) & 1:
                if all(self.present(key, e) for e in cut) and not any(self.present(key, e) for e in ch):
                    if sum(self.occ(key, e) for e in cut) == 1:
                        ne, ni = edgeset, inc
                        for e_cut, e_ch in zip(cut, ch):
                            bit = self.occ(key, e_cut)
                            ne = (ne & ~(1 << self.code[e_cut])) | (1 << self.code[e_ch])
                            ni = (ni & ~(1 << self.code[e_cut])) | (bit << self.code[e_ch])
                        W = self.eps * (1. + .3 * math.fsum(self.neighbour_load(key, e) for e in cut))
                        out.append({'kind': 'birth', 'owner': owner,
                                    'target': (slots | (1 << jj), ne, ni, p, q, s, dm), 'W': W, 'has_key': True})
            else:
                if all(self.present(key, e) for e in ch) and sum(self.occ(key, e) for e in ch) == 1:
                    ne, ni = edgeset, inc
                    for e_cut, e_ch in zip(cut, ch):
                        bit = self.occ(key, e_ch)
                        ne = (ne & ~(1 << self.code[e_ch])) | (1 << self.code[e_cut])
                        ni = (ni & ~(1 << self.code[e_ch])) | (bit << self.code[e_cut])
                    W = self.eps * (1. + .3 * math.fsum(self.neighbour_load(key, e) for e in ch))
                    out.append({'kind': 'birth_rev', 'owner': owner,
                                'target': (slots & ~(1 << jj), ne, ni, p, q, s, dm), 'W': W, 'has_key': True})
        return out

    # ---------------- sampler API subset -------------------------------------------------
    def _budget_check(self, run, phase, what):
        self.checkpoints += 1
        self.checkpoint_log.append(phase + ' ' + what)
        if self.trigger is not None and self.checkpoints == self.trigger:
            raise ToyBudgetStop(run['stage'], phase + ' ' + what)

    def _record_groups(self, run, kind, owner):
        return frozenset((0,))

    def _palette_channels(self, run, state, groups):
        cs = self.channels(self.key_from(state))
        return cs, math.fsum(c['W'] for c in cs)

    def _unique_mark(self, run, channels, kind, owner, where):
        hits = [c for c in channels if c['kind'] == kind and c['owner'] == owner]
        if len(hits) > 1:
            raise ToyStop('failed', run['stage'], where + ': duplicate mark')
        return hits[0] if hits else None

    def _target_key(self, run, ch):
        return ch['target']

    def _state_key(self, run, state):
        self._budget_check(run, 'before', 'canonical_state_key')
        try:
            key = self.key_from(state)
        except ValueError as exc:
            raise ToyStop('failed', run['stage'], 'operator canonical_state_key raised ' + str(exc))
        if self.wrong_key:
            key = key[:5] + (key[5] ^ 1,) + key[6:]
        return key

    def _segment_core(self, run, state):
        key = self._state_key(run, state)
        D, row = self.diagonal(key)
        return {'state': state, 'key': key, 'D': D, 'r': None, 'row': row}

    def _event_from_channel(self, run, ch):
        return {'kind': ch['kind'], 'owner': ch['owner'], 'W': ch['W']}

    def _keys_equal(self, run, a, b):
        return a == b

    def _check_times(self, run, times, horizon):
        prev = 0.
        for t in times:
            if not (prev < t < horizon):
                raise ToyStop('failed', run['stage'], 'time coincidence')
            prev = t


def make_run(beta=1., max_events=50, burn_in=0):
    return {'beta': beta, 'context': None, 'stage': 'toy', 'caps': {'max_events_per_path': max_events},
            'burn_in_sweeps': burn_in}


def build_path(toy, run, x0, skeleton, times):
    """Closed path from x0 applying the (kind, owner) skeleton at `times`, or None if impossible."""
    key = toy.key_from(x0)
    segs = [toy._segment_core(run, key)]
    events = []
    for kind, owner in skeleton:
        ch = toy._unique_mark(run, toy.channels(key), kind, owner, 'build')
        if ch is None:
            return None
        events.append(toy._event_from_channel(run, ch))
        key = ch['target']
        segs.append(toy._segment_core(run, key))
    if key != segs[0]['key']:
        return None
    return {'segments': segs, 'events': events, 'times': list(times)}


def log_weight(toy, run, path):
    """Independent target: -sum dt D + sum log W from the toy's own definitions (not the module)."""
    ends = [0.] + list(path['times']) + [run['beta']]
    terms = []
    for i, seg in enumerate(path['segments']):
        terms.append(-(ends[i+1] - ends[i]) * toy.diagonal(seg['key'])[0])
    for ev in path['events']:
        terms.append(math.log(ev['W']))
    return math.fsum(terms)


def path_signature(path):
    return (tuple(s['key'] for s in path['segments']),
            tuple((e['kind'], e['owner'], e['W']) for e in path['events']), tuple(path['times']))


def validate_path(toy, run, path):
    """Independent validity: every event is the actual toy mark from its dwell to the next."""
    segs, events = path['segments'], path['events']
    if len(segs) != len(events) + 1 or segs[0]['key'] != segs[-1]['key']:
        return False
    for i, ev in enumerate(events):
        ch = toy._unique_mark(run, toy.channels(segs[i]['key']), ev['kind'], ev['owner'], 'validate')
        if ch is None or ch['target'] != segs[i+1]['key'] or ch['W'] != ev['W']:
            return False
    for seg in segs:
        D, row = toy.diagonal(seg['key'])
        if seg['D'] != D or list(seg['row']) != row:
            return False
    return True


# ---------------- graphs ------------------------------------------------------------------
def cube_q3():
    """Q3 = K44 minus a perfect matching: 3-regular bipartite, six 4-cycles. A=0..3, B=4..7."""
    A, B = (0, 1, 2, 3), (4, 5, 6, 7)
    edges = [(a, b) for a in A for b in B if b != a + 4]
    births = [{'cut': ((0, 5), (1, 4)), 'children': ((0, 4), (1, 5))}]
    return A, B, edges, births


def honeycomb_torus(L1, L2):
    """Periodic honeycomb: A(i,j)-B(i,j), A(i,j)-B(i-1,j), A(i,j)-B(i,j-1). Returns geometry too."""
    def a(i, j):
        return (i % L1) * L2 + (j % L2)
    n = L1 * L2
    A = tuple(range(n))
    B = tuple(range(n, 2 * n))
    edges, shift = [], {}
    for i in range(L1):
        for j in range(L2):
            for s in ((0, 0), (1, 0), (0, 1)):
                e = (a(i, j), n + a(i - s[0], j - s[1]))
                if e in shift:
                    raise ValueError('not simple')
                edges.append(e)
                shift[e] = s
    return A, B, edges, shift, (L1, L2)


def diamond_torus(L):
    """Periodic diamond (FCC two-site) as in the adapter: A(cell)-B(cell-shift), 4 shifts."""
    cells = [(x, y, z) for x in range(L) for y in range(L) for z in range(L)]
    idx = {c: i for i, c in enumerate(cells)}
    n = len(cells)
    shifts = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    edges, shift = [], {}
    for c in cells:
        for s in shifts:
            o = tuple((c[k] - s[k]) % L for k in range(3))
            e = (idx[c], n + idx[o])
            if e in shift:
                raise ValueError('not simple')
            edges.append(e)
            shift[e] = s
    return tuple(range(n)), tuple(range(n, 2 * n)), edges, shift, (L, L, L)


def winding(loop_vertices_edges, shift, periods):
    """Winding vector of an oriented closed edge sequence starting at vertex v (list of (v, e))."""
    tot = [0] * len(periods)
    for v, e in loop_vertices_edges:
        s = shift[e]
        sign = -1 if v == e[0] else 1  # A->B moves by -shift, B->A by +shift
        for k in range(len(periods)):
            tot[k] += sign * s[k]
    if any(t % p for t, p in zip(tot, periods)):
        raise ValueError('loop displacement not a lattice period')
    return tuple(t // p for t, p in zip(tot, periods))
