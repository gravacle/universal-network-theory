"""Inert exact whole-path admission/admit_rev residence transport (dispatch 0456, Claude3, c3v001).

No sampler, schedule or global-function mutation; the actual pinned V006 sampler API is injected as
`sampler`.  Fixed unique permanent ORIGINAL-vertex roster (graph0 A+B) supplied and frozen by root:
the vertex is chosen uniformly regardless of eligibility, then uniformly among the actual positive
admit/admit_rev primitive marks carrying that vertex's exact owner at the reference dwell.  An empty
roster or any failed guard is a self loop, never resampled.  The chosen native mark (operator V003:
admit R,p=0 -> S,p=1 with kappa_v; admit_rev the reverse; q kept; owner ('admission',
('vertex', v)), so p_v and s_v toggle together under the operator's exact guards) is applied
through the operator to EVERY dwell; each dwell must carry the actual inverse mark back to its
canonical old key.  Every stored event is replayed with its exact kind and owner on the transformed
states, verifying targets and taking the actual transformed rate; an impossible replay is a self
loop.  Times and event count are preserved.  This restricted proposal supplements existing moves;
it asserts no ergodicity or mixing by itself.

    log MH = log(N_forward/N_reverse) - sum_i dt_i (D_new_i - D_old_i) + sum_events log(W_new/W_old)

N_forward/N_reverse count the admission marks of the chosen vertex at the old/new reference dwell
(vertex selection is uniform and unchanged).  No event is inserted, so no admission amplitude,
event-count or time-density factor enters.  Segments and source derivatives/captures come only from
sampler._segment_core and sampler._event_from_channel; masks and eligibility stay operator-owned.

Reference scaffold: owned_worldline_birth_residence_transport_v001.py, sha256
6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8.  Changes from it: original-vertex
roster and admission owner filter; admit/admit_rev inverse; 'between' budget checkpoints in the
dwell and replay loops; read-integral diagnostics written only after the atomic-commit checkpoint;
admission counters replace the Birth key[6] donor diagnostic (no state-tuple index is read).
"""
import math

MODULE_VERSION = 'c3v001'
REFERENCE_BIRTH_TRANSPORT_SHA256 = '6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8'
ADMISSION_KINDS = ('admit', 'admit_rev')
ADMISSION_FAMILY = 'admission'  # operator V003 owner_id[0] for both admit and admit_rev


def move(run, path, rng, diag, sampler, owner_roster):
    def tick(name):
        key = 'admission_residence_' + name
        diag[key] = diag.get(key, 0) + 1

    def fail(message):
        raise sampler._Stop('failed', run['stage'], message)

    def reject(reason):
        tick(reason); tick('rejected')
        return path, 'rejected'

    def mark(state, kind, owner):
        sampler._budget_check(run, 'before', 'admission residence marked enumeration')
        groups = sampler._record_groups(run, kind, owner)
        cs, _ = sampler._palette_channels(run, state, groups)
        return sampler._unique_mark(run, cs, kind, owner, 'admission residence replay')

    def roster(state, vertex):
        sampler._budget_check(run, 'before', 'admission residence vertex enumeration')
        owner = (ADMISSION_FAMILY, ('vertex', vertex))
        cs, _ = sampler._palette_channels(run, state, frozenset((group[vertex],)))
        selected = []
        for ch in cs:
            if ch['kind'] not in ADMISSION_KINDS:
                continue
            if sampler._keys_equal(run, ch['owner'], owner):
                selected.append(ch)
            elif isinstance(ch['owner'], tuple) and len(ch['owner']) == 2 and ch['owner'][1] == ('vertex', vertex):
                fail('Unexpected admission owner descriptor at the chosen vertex')
        for ch in selected:
            sampler._unique_mark(run, selected, ch['kind'], ch['owner'], 'admission residence roster')
        return selected

    sampler._budget_check(run, 'before', 'admission residence proposal')
    if not isinstance(owner_roster, tuple) or not owner_roster or len(set(owner_roster)) != len(owner_roster):
        fail('Freeze unique permanent original-vertex tuple before measurement')
    group = run.get('group')
    if not isinstance(group, dict):
        fail('Permanent original-owner groups unavailable; a palette binding is required')
    for v in owner_roster:
        if v not in group or group[v] != v:
            fail('Owner roster entry is not a permanent original vertex label')
    segs, events, times = path['segments'], path['events'], path['times']
    k = len(events)
    if len(times) != k or len(segs) != k + 1:
        fail('Malformed closed path')
    if k > run['caps']['max_events_per_path']:
        raise sampler._Stop('incomplete', run['stage'], 'Existing path exceeds event cap')
    sampler._check_times(run, times, run['beta'])
    if not sampler._keys_equal(run, segs[0]['key'], segs[-1]['key']):
        fail('Original path not closed')
    tick('attempts')
    vertex = owner_roster[int(rng.integers(0, len(owner_roster)))]
    old_roster = roster(segs[0]['state'], vertex)
    if not old_roster:
        return reject('empty_reference_vertex')
    chosen = old_roster[int(rng.integers(0, len(old_roster)))]
    kind, owner = chosen['kind'], chosen['owner']
    inverse_kind = 'admit_rev' if kind == 'admit' else 'admit'
    tick(kind + '_selected')
    transformed = []
    for old in segs:
        sampler._budget_check(run, 'between', 'admission residence dwell transforms')
        ch = mark(old['state'], kind, owner)
        if ch is None:
            return reject('dwell_guard')
        new = sampler._segment_core(run, ch['target'])
        back = mark(new['state'], inverse_kind, owner)
        if back is None:
            return reject('inverse_guard')
        if not sampler._keys_equal(run, sampler._target_key(run, back), old['key']):
            return reject('inverse_canonical_target')
        transformed.append(new)
    if not sampler._keys_equal(run, transformed[0]['key'], transformed[-1]['key']):
        fail('Transformed path not closed')
    new_roster = roster(transformed[0]['state'], vertex)
    reverse = sampler._unique_mark(run, new_roster, inverse_kind, owner, 'admission residence reverse selection')
    if reverse is None or not sampler._keys_equal(run, sampler._target_key(run, reverse), segs[0]['key']):
        return reject('reverse_selection')
    ends = [0.] + list(times) + [run['beta']]
    terms = [math.log(len(old_roster)) - math.log(len(new_roster))]
    for i, (old, new) in enumerate(zip(segs, transformed)):
        terms.append(-(ends[i+1]-ends[i])*(new['D']-old['D']))
    new_events = []
    for i, ev in enumerate(events):
        sampler._budget_check(run, 'between', 'admission residence marked event replay')
        before = mark(segs[i]['state'], ev['kind'], ev['owner'])
        if before is None or not sampler._keys_equal(run, sampler._target_key(run, before), segs[i+1]['key']) or before['W'] != ev['W']:
            fail('Stored primitive mark/rate inconsistent')
        after = mark(transformed[i]['state'], ev['kind'], ev['owner'])
        if after is None or not sampler._keys_equal(run, sampler._target_key(run, after), transformed[i+1]['key']):
            return reject('event_replay_guard_or_target')
        terms.append(math.log(after['W']) - math.log(before['W']))
        new_events.append(sampler._event_from_channel(run, after))
    logratio = math.fsum(terms)
    if not math.isfinite(logratio):
        fail('Nonfinite admission residence MH ratio')
    tick('legal_transport')
    diag['admission_residence_last_proposal'] = dict(kind=kind, vertex=vertex,
        forward_count=len(old_roster), reverse_count=len(new_roster), log_mh_ratio=logratio)
    if logratio < 0 and not float(rng.random()) < math.exp(logratio):
        return reject('metropolis')
    delta = [math.fsum((ends[i+1]-ends[i])*(float(new['row'][j])-float(old['row'][j]))
                       for i, (old, new) in enumerate(zip(segs, transformed)))
             for j in range(len(segs[0]['row']))]
    if not all(math.isfinite(v) for v in delta):
        fail('Nonfinite read change')
    sampler._budget_check(run, 'before', 'admission residence atomic commit')
    net = diag.get('admission_residence_read_integral_change_sum', [0.]*len(delta))
    absolute = diag.get('admission_residence_absolute_read_integral_change_sum', [0.]*len(delta))
    if len(net) != len(delta) or len(absolute) != len(delta):
        fail('Read-change diagnostic length differs from the tracked reads')
    net = [a + v for a, v in zip(net, delta)]
    absolute = [a + abs(v) for a, v in zip(absolute, delta)]
    if not all(math.isfinite(v) for v in net + absolute):
        fail('Nonfinite cumulative read change')
    diag['admission_residence_read_integral_change_sum'] = net
    diag['admission_residence_absolute_read_integral_change_sum'] = absolute
    tick('accepted_changed'); tick(kind + '_accepted_changed')
    return {'segments': transformed, 'events': new_events, 'times': list(times)}, 'changed'
