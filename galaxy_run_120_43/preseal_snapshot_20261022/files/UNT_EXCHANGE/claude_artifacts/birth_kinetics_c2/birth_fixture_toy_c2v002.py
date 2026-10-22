"""Synthetic explicit-state toy of the injected V006 sampler API for the Birth-residence fixtures.

Never imports the native operator or sampler.  Keys mimic operator V003's seven nonnegative ints
(slots, edgeset, inc, p, q, s, donors).  Five permanent owners 0..4; Birth sites (owner, j):
(0,0), (0,1), (1,0), (2,0), (4,0); owner 3 has NO Birth site (never channel-bearing) but carries a
flip mark.  Birth owner_id = ('birth', owner, j) (owner_id[1] is the permanent owner, as natively);
flip owner_id = ('flip', ('edge', (a, b))).

Interactions make the channel-bearing owner set CHANGE across a Birth move and make the target
non-invariant:
  birth(o, j)     needs site inactive, N_act(o) <= 1 (active sites of neighbour owners), site (0,1)
                  needs (0,0) active, owner 4 needs incidence bit 0;
  birth_rev(o, j) needs site active, (0,0) needs (0,1) inactive (no gate: an inverse can be missing
                  after neighbours were born, exercising inverse_guard);
  W(birth) and W(birth_rev) depend on N_act and incidence bits, W(flip) on the active count, D on
  sites, their square and a neighbour coupling; reads are three state functions.
Flags for guard fixtures: union_W_skew, union_outside_owner, union_drop_rev, rev_wrong_target.
"""
import math

OWNERS = (0, 1, 2, 3, 4)
SITES = ((0, 0), (0, 1), (1, 0), (2, 0), (4, 0))
EDGES = ((0, 1), (2, 4), (1, 3))
NEIGHBOURS = {0: (1, 4), 1: (0, 2), 2: (1, 4), 3: (), 4: (0, 2)}


class ToyStop(Exception):
    def __init__(self, status, stage, message):
        Exception.__init__(self, message)
        self.status, self.stage, self.message = status, stage, message


class ToyBudgetStop(ToyStop):
    def __init__(self, stage, checkpoint):
        ToyStop.__init__(self, 'incomplete', stage, 'INCOMPLETE_BUDGET at ' + checkpoint)
        self.checkpoint = checkpoint


def popcount(x):
    return bin(x).count('1')


class Toy:
    _Stop = ToyStop

    def __init__(self, *, union_W_skew=False, union_outside_owner=False, union_drop_rev=False,
                 rev_wrong_target=False):
        self.site_bit = {s: i for i, s in enumerate(SITES)}
        self.a_site = [.31, .47, .22, .58, .39]
        self.c_inc = [.27, -.18, .35]
        self.h = [.5, .6, .7]
        self.union_W_skew, self.union_outside_owner = union_W_skew, union_outside_owner
        self.union_drop_rev, self.rev_wrong_target = union_drop_rev, rev_wrong_target
        self.checkpoints, self.trigger, self.checkpoint_log = 0, None, []
        self.palette_calls = 0

    # ---------------- states ------------------------------------------------------------
    def key_from(self, state):
        if not (isinstance(state, tuple) and len(state) == 7 and all(type(v) is int and v >= 0 for v in state)):
            raise ValueError('toy key must be seven nonnegative ints')
        slots, edgeset, inc, p, q, s, dm = state
        if slots >> len(SITES) or inc >> len(EDGES) or edgeset != (1 << len(EDGES)) - 1 or p or q or s:
            raise ValueError('toy key outside the toy universe')
        if self.active(slots, (0, 1)) and not self.active(slots, (0, 0)):
            raise ValueError('site (0,1) active without (0,0)')
        if dm != slots & 0b11:
            raise ValueError('donor bits not canonical')
        return state

    def make_key(self, slots, inc):
        return self.key_from((slots, (1 << len(EDGES)) - 1, inc, 0, 0, 0, slots & 0b11))

    def all_keys(self):
        out = []
        for slots in range(1 << len(SITES)):
            for inc in range(1 << len(EDGES)):
                try:
                    out.append(self.make_key(slots, inc))
                except ValueError:
                    pass
        return out

    def active(self, slots, site):
        return (slots >> self.site_bit[site]) & 1

    def owner_active(self, slots, o):
        return sum(self.active(slots, s) for s in SITES if s[0] == o)

    def n_act(self, slots, o):
        return sum(self.owner_active(slots, v) for v in NEIGHBOURS[o])

    # ---------------- native-like quantities --------------------------------------------
    def diagonal(self, key):
        slots, inc = key[0], key[2]
        act = popcount(slots)
        terms = [self.a_site[i] for i in range(len(SITES)) if (slots >> i) & 1]
        terms += [.15 * act * act]
        terms += [.07 * self.owner_active(slots, o) * self.n_act(slots, o) for o in OWNERS]
        terms += [self.c_inc[k] for k in range(len(EDGES)) if (inc >> k) & 1]
        row = [float(act), float(popcount(inc)),
               math.fsum([.5 * self.owner_active(slots, o) * (o - 2) for o in OWNERS] + [.3 * (inc & 1)])]
        return math.fsum(terms), row

    def channels(self, key):
        """Every positive-rate mark of the toy at `key` (independent of palettes)."""
        slots, edgeset, inc = key[0], key[1], key[2]
        act = popcount(slots)
        out = []
        for k, (a, b) in enumerate(EDGES):
            if k == 2 and not inc & 1:
                continue  # owner 3's only mark exists only with incidence bit 0
            out.append({'kind': 'flip', 'owner': ('flip', ('edge', (a, b))), 'W': self.h[k] * (1. + .4 * act),
                        'target': self.make_key(slots, inc ^ (1 << k)), 'has_key': True})
        for site in SITES:
            o, j = site
            bit = 1 << self.site_bit[site]
            na = self.n_act(slots, o)
            if not slots & bit:
                if na > 1 or (site == (0, 1) and not self.active(slots, (0, 0))) or (o == 4 and not inc & 1):
                    continue
                W = (.4 + .1 * o) * (1. + .3 * na + .2 * ((inc >> 1) & 1))
                out.append({'kind': 'birth', 'owner': ('birth', o, j), 'W': W,
                            'target': self.make_key(slots | bit, inc), 'has_key': True})
            else:
                if site == (0, 0) and self.active(slots, (0, 1)):
                    continue
                W = (.5 + .05 * o) * (1. + .25 * na + .15 * ((inc >> 2) & 1))
                tgt = self.make_key(slots & ~bit, inc ^ (4 if self.rev_wrong_target else 0))
                out.append({'kind': 'birth_rev', 'owner': ('birth', o, j), 'W': W, 'target': tgt,
                            'has_key': True})
        return out

    def groups_of(self, run, kind, owner):
        g = run['group']
        if kind in ('birth', 'birth_rev'):
            return frozenset((g[owner[1]],))
        a, b = owner[1][1]
        return frozenset((g[a], g[b]))

    # ---------------- sampler API subset --------------------------------------------------
    def _budget_check(self, run, phase, what):
        self.checkpoints += 1
        self.checkpoint_log.append(phase + ' ' + what)
        if self.trigger is not None and self.checkpoints == self.trigger:
            raise ToyBudgetStop(run['stage'], phase + ' ' + what)

    def _record_groups(self, run, kind, owner):
        try:
            return self.groups_of(run, kind, owner)
        except (KeyError, TypeError, IndexError, ValueError):
            raise ToyStop('failed', run['stage'], 'unclassifiable owner')

    def _palette_channels(self, run, state, groups):
        self.palette_calls += 1
        key = self.key_from(state)
        cs = [dict(c) for c in self.channels(key) if not self.groups_of(run, c['kind'], c['owner']).isdisjoint(groups)]
        union = len(groups) > 1
        if union and self.union_W_skew:
            for c in cs:
                if c['kind'] == 'birth':
                    c['W'] *= 1. + 1e-9
        if union and self.union_drop_rev:
            cs = [c for c in cs if c['kind'] != 'birth_rev']
        if union and self.union_outside_owner and any(c['kind'] == 'birth' for c in cs):
            cs.append({'kind': 'birth', 'owner': ('birth', 99, 0), 'W': 1., 'target': key, 'has_key': True})
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
            return self.key_from(state)
        except ValueError as exc:
            raise ToyStop('failed', run['stage'], 'canonical_state_key raised ' + str(exc))

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
    return {'beta': beta, 'stage': 'toy', 'caps': {'max_events_per_path': max_events},
            'burn_in_sweeps': burn_in, 'group': {o: o for o in OWNERS}}


def build_path(toy, run, x0, skeleton, times):
    """Closed path from x0 applying the (kind, owner) skeleton at `times`, or None if impossible."""
    key = toy.key_from(x0)
    segs = [toy._segment_core(run, key)]
    events = []
    for kind, owner in skeleton:
        hits = [c for c in toy.channels(key) if c['kind'] == kind and c['owner'] == owner]
        if not hits:
            return None
        events.append({'kind': kind, 'owner': owner, 'W': hits[0]['W']})
        key = hits[0]['target']
        segs.append(toy._segment_core(run, key))
    if key != segs[0]['key']:
        return None
    return {'segments': segs, 'events': events, 'times': list(times)}


def log_weight(toy, run, path):
    """Independent target: -sum dt D + sum log W from the toy's own definitions."""
    ends = [0.] + list(path['times']) + [run['beta']]
    terms = [-(ends[i+1] - ends[i]) * toy.diagonal(seg['key'])[0] for i, seg in enumerate(path['segments'])]
    terms += [math.log(ev['W']) for ev in path['events']]
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
        hits = [c for c in toy.channels(segs[i]['key']) if c['kind'] == ev['kind'] and c['owner'] == ev['owner']]
        if len(hits) != 1 or hits[0]['target'] != segs[i+1]['key'] or hits[0]['W'] != ev['W']:
            return False
    for seg in segs:
        D, row = toy.diagonal(seg['key'])
        if seg['D'] != D or list(seg['row']) != row:
            return False
    return True
