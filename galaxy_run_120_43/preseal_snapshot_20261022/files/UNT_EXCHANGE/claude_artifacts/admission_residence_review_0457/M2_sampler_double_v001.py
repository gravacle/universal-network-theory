"""M2 synthetic sampler/operator double for whole-path residence transports (0457, Claude4 lane).

Helper M2 of the Claude4 independent review of 0456. NOT the project sampler and NOT the V003
operator: tiny explicit states, synthetic coefficients, no project data, no project import.
Import-inert (definitions only).

Sampler-API semantics transcribed as text from pinned V004
(SHA256 7d0798923302bb36763c6b4f6212c944872b2b9c2f50021183d918a19dbd03c9; V006 896cadbb...
re-exports these functions unchanged):
  _Stop/_BudgetStop L862-885; _budget_check L2049; _op L2101 (budget check before and after
  every operator call); _state_key L2121; _keys_equal L2125; _enumeration_tick L2188;
  _channels_from_records L2206 (amplitude 0 or multiplier 0 -> no mark, multiplier < 0 ->
  unsupported, W = |amp| * multiplier must be finite positive); _record_groups L2286;
  _palette_members L2331; _palette_channels L2353 (verification off); _segment_core L2650;
  _target_key L2704; _event_from_channel L2711; _summed_rate L2737; _no_self_loop L2749;
  _reverse_check L2760 (no fallback counter); _check_times L2794; _net_increments L2807;
  _unique_mark L3207; _kind_table L1919.
Operator-double admission rules and owner ids follow pinned V003
(SHA256 a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07) L1590-1595 and
L1781-1791: admit iff (p_v,s_v)=(0,0) -> (1,1); admit_rev iff (1,1) -> (0,0); q kept;
owner_id ("admission", ("vertex", label)) for both kinds. Other owner formats:
("birth", owner_label, cut_edge_labels), ("bind", ("vertex", label)),
("flip"|"hop", ("edge", (label_a, label_b))).
Deliberate simplifications (synthetic, not V003 physics): the lapse multiplier is an
endpoint-symmetric function of the admitted count A and active-slot count S, supplied by the
operator double in the record field 'double_mult' (not 1 + sum_alpha n_alpha w_alpha); one
diagonal record; one read_rows call; no pair/allk/whitened reads; palette verify off.
Variants (fixture-only defect/extension injections, never native): ladder, admit_rev_resets_edge,
dup_admission, nonfinite_D_when_A/S, huge_D_when_A, nonfinite_W, read_fail_when_A/S, opaque,
admission_family (non-V003 owner family name for a label; probes fail-closed owner branches).

The ORACLE section uses only the raw operator physics (ToyModel.records / D_raw), never the
sampler-API layer and never a module under test.
"""
import copy
import math
import types

import numpy as np

KIND_TABLE = {
    "flip": (0, 0, 0, "flip"),
    "hop": (0, 0, 0, "hop"),
    "bind": (1, 0, 0, "bind"),
    "admit": (0, 1, 0, "admit_rev"),
    "admit_rev": (0, -1, 0, "admit"),
    "birth": (0, 0, 1, "birth_rev"),
    "birth_rev": (0, 0, -1, "birth"),
}
READ_LABELS = ("N_adm", "N_part", "N_on", "N_slot", "N_bound")


# ----------------------------------------------------------------------------------------------
# Sampler-API double (V004 semantics)
# ----------------------------------------------------------------------------------------------


class _Stop(Exception):
    """Fail-closed termination carrying status, stage and message (V004 L862)."""

    def __init__(self, status, stage, message):
        Exception.__init__(self, message)
        self.status = status
        self.stage = stage
        self.message = message


class _BudgetStop(_Stop):
    """Cooperative budget stop: status 'incomplete' (V004 L872)."""

    def __init__(self, stage, checkpoint):
        _Stop.__init__(self, "incomplete", stage,
                       f"INCOMPLETE_BUDGET: budget_hook requested a cooperative stop at "
                       f"checkpoint '{checkpoint}'")
        self.checkpoint = checkpoint


def _budget_check(run, phase, what):
    run["budget_log"].append(f"{phase} {what}")  # double-only trace of checkpoint labels
    hook = run["budget_hook"]
    if hook is None:
        return
    run["counters"]["budget_checks"] += 1
    try:
        stop = hook()
    except Exception as exc:
        raise _Stop("failed", run["stage"],
                    f"budget_hook raised {type(exc).__name__}: {exc} at checkpoint '{phase} {what}'")
    if not isinstance(stop, (bool, np.bool_)):
        raise _Stop("failed", run["stage"],
                    f"budget_hook returned {type(stop).__name__}, not a bool, at '{phase} {what}'")
    if bool(stop):
        raise _BudgetStop(run["stage"], f"{phase} {what}")


def _op(run, name, **kwargs):
    fn = run["api"][name]
    _budget_check(run, "before", name)
    try:
        out = fn(**kwargs)
    except _Stop:
        raise
    except Exception as exc:
        raise _Stop("failed", run["stage"], f"operator {name} raised {type(exc).__name__}: {exc}")
    _budget_check(run, "after", name)
    return out


def _state_key(run, state):
    return _op(run, "canonical_state_key", context=run["context"], state=state)


def _keys_equal(run, a, b):
    try:
        eq = a == b
    except Exception as exc:
        raise _Stop("failed", run["stage"], f"canonical keys not comparable: {exc}")
    if isinstance(eq, (bool, np.bool_)):
        return bool(eq)
    raise _Stop("failed", run["stage"],
                f"canonical key comparison returned {type(eq).__name__}, not a single bool")


def _enumeration_tick(run):
    counters = run["counters"]
    if counters["channel_enumerations"] >= run["caps"]["max_channel_enumerations"]:
        raise _Stop("incomplete", run["stage"],
                    "cap max_channel_enumerations reached; computation ended (no path was rejected)")
    counters["channel_enumerations"] += 1


def _signature(changed):
    try:
        return frozenset(changed)
    except TypeError:
        return None


def _channels_from_records(run, records, source):
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], f"{source} did not return a list")
    channels = []
    for i, rec in enumerate(records):
        where = f"{source} record {i}"
        kind = rec.get("kind")
        if isinstance(kind, str) and kind == "diag":
            continue
        if kind not in run["kinds"]:
            raise _Stop("failed", run["stage"], f"{where}: unknown kind {kind!r}")
        try:
            amp = complex(rec["amplitude"])
        except Exception:
            raise _Stop("failed", run["stage"], f"{where}: amplitude not a finite complex scalar")
        if not (math.isfinite(amp.real) and math.isfinite(amp.imag)):
            raise _Stop("failed", run["stage"], f"{where}: amplitude not a finite complex scalar")
        if amp == 0:
            continue
        mag = abs(amp)
        gauged = amp * run["gauge"][kind]
        if not abs(gauged + mag) <= run["tol"]["gauge_phase"] * mag:
            raise _Stop("unsupported", run["stage"], f"{where}: gauged element not real nonpositive")
        mult = float(rec["double_mult"])
        if not math.isfinite(mult):
            raise _Stop("failed", run["stage"], f"{where}: lapse multiplier not finite")
        if mult < 0.0:
            raise _Stop("unsupported", run["stage"], f"{where}: lapse multiplier {mult!r} < 0")
        if mult == 0.0:
            run["zero_rate_directions"].add(("double_zero_multiplier", kind))
            continue  # V004 L2251-2262: zero-multiplier channel dropped, no mark
        rate = mag * mult
        if not (math.isfinite(rate) and rate > 0.0):
            raise _Stop("failed", run["stage"], f"{where}: rate {rate!r} not finite positive")
        channels.append({
            "kind": kind,
            "owner": rec["owner_id"],
            "target": rec["target_state"],
            "W": rate,
            "mult": mult,
            "weights": dict(rec["energy_weights"]),
            "sig": _signature(rec["changed_support"]),
            "key": None,
            "has_key": False,
        })
    exit_rate = math.fsum(ch["W"] for ch in channels)
    if not math.isfinite(exit_rate):
        raise _Stop("failed", run["stage"], "exit rate r(x) not finite")
    return channels, exit_rate


def _channels_at(run, state):
    _enumeration_tick(run)
    records = _op(run, "primitive_channels", context=run["context"], state=state)
    return _channels_from_records(run, records, "primitive_channels")


def _record_groups(run, kind, owner_id):
    group = run["group"]
    labels = None
    try:
        if kind in ("birth", "birth_rev"):
            if owner_id[0] == "birth":
                labels = (owner_id[1],)
        elif kind in ("flip", "hop"):
            tag, pair = owner_id[1]
            if tag == "edge" and len(pair) == 2:
                labels = (pair[0], pair[1])
        elif kind in ("bind", "admit", "admit_rev"):
            tag, vertex = owner_id[1]
            if tag == "vertex":
                labels = (vertex,)
        if labels is not None:
            return frozenset(group[lab] for lab in labels)
    except (TypeError, KeyError, IndexError, ValueError):
        pass
    raise _Stop("failed", run["stage"],
                f"primitive kind {kind!r} owner_id {owner_id!r} cannot be classified into permanent "
                "original-owner groups (palette membership must come from permanent labels)")


def _palette_members(run, records, owners, source):
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], f"{source} did not return a list")
    out = []
    dropped = 0
    for i, rec in enumerate(records):
        kind = rec.get("kind")
        owner_id = rec.get("owner_id")
        if isinstance(kind, str) and kind == "diag":
            continue
        if kind not in run["kinds"]:
            raise _Stop("failed", run["stage"], f"{source} record {i}: unknown kind {kind!r}")
        if _record_groups(run, kind, owner_id).isdisjoint(owners):
            dropped += 1
            continue
        out.append(rec)
    return out, dropped


def _palette_channels(run, state, owners):
    _enumeration_tick(run)
    run["counters"]["restricted_enumerations"] += 1
    records = _op(run, "palette_channels", context=run["context"], state=state, palette_owners=owners)
    members, dropped = _palette_members(run, records, owners, "palette_channels")
    run["counters"]["restricted_nonmember_records_dropped"] += dropped
    return _channels_from_records(run, members, "palette_channels")


def _diagonal_at(run, state):
    records = _op(run, "diagonal_terms", context=run["context"], state=state)
    if not isinstance(records, (list, tuple)):
        raise _Stop("failed", run["stage"], "diagonal_terms did not return a list")
    terms = []
    for i, rec in enumerate(records):
        if rec.get("kind") != "diag":
            raise _Stop("failed", run["stage"], f"diagonal_terms record {i}: kind is not 'diag'")
        z = complex(rec["amplitude"])
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise _Stop("failed", run["stage"], f"diagonal_terms record {i}: value not a finite scalar")
        if z.real != 0.0:
            terms.append(z.real)
    return math.fsum(terms), {}, {}, None


def _reads_at(run, state):
    rows = _op(run, "read_rows", context=run["context"], state=state)
    if not isinstance(rows, dict) or any(k not in rows for k in ("labels", "values", "presence")):
        raise _Stop("failed", run["stage"], "read_rows did not return {labels, values, presence}")
    if tuple(rows["labels"]) != tuple(run["tracked_all"]):
        raise _Stop("failed", run["stage"], "read_rows labels changed between states (must be fixed)")
    vals = np.asarray(rows["values"], dtype=np.float64)
    if vals.shape != (len(run["tracked_all"]),) or not bool(np.all(np.isfinite(vals))):
        raise _Stop("failed", run["stage"], "read_rows values not a finite aligned row")
    return {lbl: float(vals[i]) for i, lbl in enumerate(rows["labels"])}


def _segment_core(run, state):
    key = _state_key(run, state)
    d_h, _d_lapse, _d_dirs, _d_allk = _diagonal_at(run, state)
    values = _reads_at(run, state)
    src = math.fsum([-j * values[lbl] for lbl, j in run["sources"].items()])
    diag = math.fsum([d_h, src])
    if not math.isfinite(diag):
        raise _Stop("failed", run["stage"], "diagonal energy D(x) not finite")
    da = np.zeros(run["n_u"], dtype=np.float64)
    for idx, lbl in enumerate(run["source_coords"]):
        da[idx] = -values[lbl]
    row = np.array([values[lbl] for lbl in run["tracked_all"]], dtype=np.float64)
    return {"state": state, "key": key, "D": diag, "r": None, "Da": da, "row": row, "allk": None}


def _segment_at(run, state):
    seg = _segment_core(run, state)
    _channels, exit_rate = _channels_at(run, state)
    seg["r"] = exit_rate
    return seg, _channels


def _seg_rate(run, seg):
    if seg["r"] is None:
        _, exit_rate = _channels_at(run, seg["state"])
        seg["r"] = exit_rate
    return seg["r"]


def _target_key(run, ch):
    if not ch["has_key"]:
        ch["key"] = _state_key(run, ch["target"])
        ch["has_key"] = True
    return ch["key"]


def _event_from_channel(run, ch):
    rho = np.zeros(run["n_u"], dtype=np.float64)
    for cell, w in ch["weights"].items():
        idx = run["lapse_index"].get(cell)
        if idx is not None:
            rho[idx] = w / ch["mult"]
    dq, dns, dn, _ = run["kinds"][ch["kind"]]
    return {"kind": ch["kind"], "owner": ch["owner"], "W": ch["W"], "rho": rho,
            "dq": dq, "dns": dns, "dn": dn, "allk_idx": None, "allk_rho": None}


def _summed_rate(run, channels, kind, sig, target_key, use_sig):
    terms = []
    for c in channels:
        if c["kind"] != kind:
            continue
        if use_sig and (sig is None or c["sig"] != sig):
            continue
        if _keys_equal(run, _target_key(run, c), target_key):
            terms.append(c["W"])
    return math.fsum(terms)


def _no_self_loop(run, x_seg, y_seg, chosen):
    if _keys_equal(run, x_seg["key"], y_seg["key"]):
        raise _Stop("failed", run["stage"],
                    f"primitive kind {chosen['kind']!r} owner {chosen['owner']!r} maps a state to itself")


def _reverse_check(run, x_seg, x_channels, chosen, y_seg, y_channels):
    rev_kind = run["kinds"][chosen["kind"]][3]
    sig = chosen["sig"]
    fwd = rev = 0.0
    if sig is not None:
        fwd = _summed_rate(run, x_channels, chosen["kind"], sig, y_seg["key"], True)
        rev = _summed_rate(run, y_channels, rev_kind, sig, x_seg["key"], True)
    if rev == 0.0:
        fwd = _summed_rate(run, x_channels, chosen["kind"], sig, y_seg["key"], False)
        rev = _summed_rate(run, y_channels, rev_kind, sig, x_seg["key"], False)
    if rev == 0.0:
        raise _Stop("failed", run["stage"], f"reverse primitive missing for kind {chosen['kind']!r}")
    if not abs(fwd - rev) <= run["tol"]["reverse_rate"] * max(fwd, rev):
        raise _Stop("failed", run["stage"], f"reverse rate mismatch for kind {chosen['kind']!r}")


def _net_increments(events):
    dq = sum(e["dq"] for e in events) % 2
    dns = sum(e["dns"] for e in events)
    dn = sum(e["dn"] for e in events)
    return dq, dns, dn


def _unique_mark(run, channels, kind, owner, where):
    hits = [c for c in channels if c["kind"] == kind and _keys_equal(run, c["owner"], owner)]
    if len(hits) > 1:
        raise _Stop("failed", run["stage"],
                    f"{where}: (kind {kind!r}, owner {owner!r}) matches {len(hits)} positive-rate "
                    "records at one state (duplicate-key assertion; L30)")
    return hits[0] if hits else None


def _check_times(run, times, horizon):
    prev = 0.0
    for t in times:
        if not (t > prev and t < horizon):
            raise _Stop("failed", run["stage"],
                        "floating-point event-time coincidence or rounding to the circle end")
        prev = t


def _kind_table():
    return dict(KIND_TABLE)


API_NAMES = ("_Stop", "_BudgetStop", "_budget_check", "_op", "_state_key", "_keys_equal",
             "_enumeration_tick", "_signature", "_channels_from_records", "_channels_at",
             "_record_groups", "_palette_members", "_palette_channels", "_diagonal_at", "_reads_at",
             "_segment_core", "_segment_at", "_seg_rate", "_target_key", "_event_from_channel",
             "_summed_rate", "_no_self_loop", "_reverse_check", "_net_increments",
             "_unique_mark", "_check_times", "_kind_table")


def make_sampler():
    """Fresh namespace exposing the API double (so patching by a module is detectable/isolated)."""
    g = globals()
    ns = {n: g[n] for n in API_NAMES}
    ns["math"] = math
    ns["np"] = np
    return types.SimpleNamespace(**ns)


# ----------------------------------------------------------------------------------------------
# Operator double (explicit tiny states)
# ----------------------------------------------------------------------------------------------


class Opaque:
    """Hashable wrapper with equality but no indexing/iteration (detects hard-coded tuple reads)."""

    __slots__ = ("_v",)

    def __init__(self, v):
        object.__setattr__(self, "_v", v)

    def __eq__(self, other):
        return isinstance(other, Opaque) and self._v == other._v

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(("Opaque", self._v))

    def __repr__(self):
        return f"Opaque({self._v!r})"

    def __setattr__(self, name, value):
        raise AttributeError("Opaque is immutable")

    def __deepcopy__(self, memo):
        return self

    def __copy__(self):
        return self


def _popcount(x):
    return bin(x).count("1")


class ToyModel:
    """Explicit-state operator double. State tuple mirrors V003 key order
    (slots, edgeset, inc, p, q, s, dm): slots = per-birth-owner 0 (inactive) or cut_index+1;
    edgeset = derived tuple of present edge codes; inc/p/q/s = bitmasks; dm = donor bits (RR)."""

    def __init__(self, spec):
        self.spec = copy.deepcopy(spec)
        self.originals = tuple(spec["originals"])
        self.births = {o: dict(b) for o, b in spec.get("births", {}).items()}
        self.birth_owners = tuple(self.births)
        self.newborn_of = {b["newborn"]: o for o, b in self.births.items()}
        self.labels = self.originals + tuple(b["newborn"] for b in self.births.values())
        self.vidx = {lab: i for i, lab in enumerate(self.labels)}
        self.edges = tuple(tuple(e) for e in spec["edges"])
        self.newborn_edge_of = {b["newborn_edge"]: o for o, b in self.births.items()}
        n_e = len(self.edges)
        self.hop_edges = frozenset(spec.get("hop_edges", range(n_e)))
        self.flip_edges = frozenset(spec.get("flip_edges", range(n_e)))
        self.bind_vertices = frozenset(spec.get("bind_vertices", self.labels))
        self.adm_vertices = frozenset(spec.get("admission_vertices", self.labels))
        self.amp = spec["amp"]
        self.energy = spec["energy"]
        self.coef = spec["mult"]
        self.sources = dict(spec["sources"])
        self.adm_cap = spec.get("adm_cap")
        self.variants = dict(spec.get("variants", {}))
        self.opaque = bool(self.variants.get("opaque", False))
        self.group = {o: o for o in self.originals}
        for nb, o in self.newborn_of.items():
            self.group[nb] = o
        self.dm_full = (1 << (2 * len(self.birth_owners))) - 1
        self._rec_cache = {}

    # -- encoding ------------------------------------------------------------------------------
    def wrap(self, x):
        return Opaque(x) if self.opaque else x

    def unwrap(self, x):
        return x._v if isinstance(x, Opaque) else x

    def _present_edges(self, slots):
        removed, born = set(), set()
        for j, o in enumerate(self.birth_owners):
            if slots[j]:
                removed.add(self.births[o]["cuts"][slots[j] - 1])
                born.add(self.births[o]["newborn_edge"])
        out = []
        for c in range(len(self.edges)):
            if c in self.newborn_edge_of:
                if c in born:
                    out.append(c)
            elif c not in removed:
                out.append(c)
        return tuple(out)

    def _present_vertices(self, slots):
        out = list(self.originals)
        for j, o in enumerate(self.birth_owners):
            if slots[j]:
                out.append(self.births[o]["newborn"])
        return out

    def _vmask(self, slots):
        return sum(1 << self.vidx[lab] for lab in self._present_vertices(slots))

    def _emask(self, slots):
        return sum(1 << c for c in self._present_edges(slots))

    def make_state(self, slots=None, inc=(), p=(), q=(), s=()):
        slots = tuple(slots) if slots is not None else (0,) * len(self.birth_owners)
        x = (slots, self._present_edges(slots), sum(1 << c for c in set(inc)),
             sum(1 << self.vidx[l] for l in set(p)), sum(1 << self.vidx[l] for l in set(q)),
             sum(1 << self.vidx[l] for l in set(s)), self.dm_full)
        self.validate(x)
        return x

    def validate(self, x):
        slots, edgeset, inc, p, q, s, dm = x
        vm, em = self._vmask(slots), self._emask(slots)
        if edgeset != self._present_edges(slots) or inc & ~em or (p | q | s) & ~vm:
            raise ValueError(f"invalid double state {x!r}")

    def all_states(self):
        """Every valid state (bits only on present vertices/edges); tiny doubles only."""
        out = []
        slot_choices = [range(len(self.births[o]["cuts"]) + 1) for o in self.birth_owners]
        for slots in _product(slot_choices):
            pv = self._present_vertices(slots)
            pe = self._present_edges(slots)
            v_bits = [self.vidx[l] for l in pv]
            q_bits = [self.vidx[l] for l in pv if l in self.bind_vertices]
            s_bits = [self.vidx[l] for l in pv if l in self.adm_vertices]
            p_bits = [self.vidx[l] for l in pv if l in self.adm_vertices or l in self.bind_vertices
                      or any(l in self.edges[c] for c in pe if c in self.hop_edges)]
            e_bits = [c for c in pe if c in self.flip_edges or c in self.hop_edges
                      or any(c in self.births[o]["cuts"] for o in self.birth_owners)]
            del v_bits
            for inc in _subsets(e_bits):
                for p in _subsets(p_bits):
                    for q in _subsets(q_bits):
                        for s in _subsets(s_bits):
                            x = (tuple(slots), pe, inc, p, q, s, self.dm_full)
                            self.validate(x)
                            out.append(x)
        return out

    def A(self, x):
        return _popcount(x[5] & self._vmask(x[0]))

    def S(self, x):
        return sum(1 for v in x[0] if v)

    # -- multipliers (synthetic, endpoint-symmetric) --------------------------------------------
    def _mult(self, kind, x, y):
        ax, ay, sx, sy = self.A(x), self.A(y), self.S(x), self.S(y)
        c = self.coef
        if kind == "flip":
            m = (1.0 + c["flip_s"] * (sx + sy) / 2.0) * (1.0 - 0.25 * (min(ax, 2) + min(ay, 2)))
        elif kind == "hop":
            m = 1.0 + c["hop_a"] * (ax + ay) / 2.0 + c["hop_s"] * (sx + sy) / 2.0
        elif kind == "bind":
            m = 1.0 + c["bind_a"] * (ax + ay) / 2.0 + c["bind_s"] * (sx + sy) / 2.0
        elif kind in ("admit", "admit_rev"):
            if self.adm_cap is not None and max(ax, ay) > self.adm_cap:
                m = 0.0
            else:
                m = 1.0 + c["adm_a"] * (ax + ay) / 2.0 + c["adm_s"] * (sx + sy) / 2.0
        else:
            m = 1.0 + c["birth_a"] * (ax + ay) / 2.0
        nf = self.variants.get("nonfinite_W")
        if nf is not None and kind == nf[0] and ax == nf[1]:
            m = float("inf")
        return m

    # -- primitive records (V003-like order: flip, hop, bind, admission, birth) -----------------
    def records(self, x):
        if x in self._rec_cache:
            return self._rec_cache[x]
        slots, edgeset, inc, p, q, s, dm = x
        pres_e = set(self._present_edges(slots))
        pres_v = self._present_vertices(slots)
        out = []

        def add(kind, owner, y, mag, support):
            out.append({"kind": kind, "owner_id": owner, "target_state": y,
                        "amplitude": complex(-float(mag), 0.0), "changed_support": frozenset(support),
                        "energy_weights": {"cell0": 1.0}, "double_mult": self._mult(kind, x, y)})

        for c in sorted(pres_e):
            if c in self.flip_edges:
                add("flip", ("flip", ("edge", self.edges[c])), (slots, edgeset, inc ^ (1 << c), p, q, s, dm),
                    self.amp["h"][c], [("edge", c)])
        for c in sorted(pres_e):
            if c in self.hop_edges and (inc >> c) & 1:
                la, lb = self.edges[c]
                a, b = self.vidx[la], self.vidx[lb]
                if ((p >> a) & 1) != ((p >> b) & 1):
                    add("hop", ("hop", ("edge", self.edges[c])),
                        (slots, edgeset, inc, p ^ (1 << a) ^ (1 << b), q, s, dm),
                        self.amp["t"][c], [("vertex", la), ("vertex", lb)])
        for lab in pres_v:
            if lab in self.bind_vertices:
                bit = 1 << self.vidx[lab]
                if p & bit:
                    add("bind", ("bind", ("vertex", lab)), (slots, edgeset, inc, p, q ^ bit, s, dm),
                        self.amp["g"][lab], [("vertex", lab)])
        for lab in pres_v:
            if lab not in self.adm_vertices:
                continue
            bit = 1 << self.vidx[lab]
            owner = (self.variants.get("admission_family", {}).get(lab, "admission"), ("vertex", lab))
            pv, sv = bool(p & bit), bool(s & bit)
            targets = []
            if self.variants.get("ladder"):
                # fixture-only extension: level 0=(0,0), 1=(1,1), 2=(0,1); (1,0) has no mark
                if (pv, sv) == (False, False):
                    targets.append(("admit", p | bit, s | bit))
                elif (pv, sv) == (True, True):
                    targets.append(("admit", p ^ bit, s))
                    targets.append(("admit_rev", p ^ bit, s ^ bit))
                elif (pv, sv) == (False, True):
                    targets.append(("admit_rev", p | bit, s))
            else:  # V003 L1590-1595
                if not sv and not pv:
                    targets.append(("admit", p | bit, s | bit))
                elif sv and pv:
                    targets.append(("admit_rev", p ^ bit, s ^ bit))
            for kind, py, sy in targets:
                inc_y = inc
                rc = self.variants.get("admit_rev_resets_edge")
                if kind == "admit_rev" and rc is not None and rc in pres_e:
                    inc_y = inc & ~(1 << rc)  # fixture-only defect: not an exact inverse
                y = (slots, edgeset, inc_y, py, q, sy, dm)
                add(kind, owner, y, self.amp["kappa"][lab], [("vertex", lab)])
                if self.variants.get("dup_admission") == lab:
                    add(kind, owner, y, self.amp["kappa"][lab], [("vertex", lab)])
        for j, o in enumerate(self.birth_owners):
            b = self.births[o]
            if slots[j] == 0:
                if ((dm >> (2 * j)) & 3) == 3:
                    for ci, c in enumerate(b["cuts"]):
                        if c in pres_e and (inc >> c) & 1:
                            ns = slots[:j] + (ci + 1,) + slots[j + 1:]
                            add("birth", ("birth", o, (self.edges[c],)),
                                (ns, self._present_edges(ns), inc & ~(1 << c), p, q, s, dm),
                                self.amp["eps"][o], [("birth", o)])
            else:
                ci = slots[j] - 1
                c = b["cuts"][ci]
                nb = 1 << self.vidx[b["newborn"]]
                ne = b["newborn_edge"]
                if not ((p | q | s) & nb) and not ((inc >> ne) & 1):
                    ns = slots[:j] + (0,) + slots[j + 1:]
                    add("birth_rev", ("birth", o, (self.edges[c],)),
                        (ns, self._present_edges(ns), inc | (1 << c), p, q, s, dm),
                        self.amp["eps"][o], [("birth", o)])
        self._rec_cache[x] = out
        return out

    # -- diagonal energy and reads ---------------------------------------------------------------
    def d_h(self, x):
        slots, edgeset, inc, p, q, s, dm = x
        e = self.energy
        a = self.A(x)
        v = self.variants
        if v.get("nonfinite_D_when_A") is not None and a == v["nonfinite_D_when_A"]:
            return float("nan")
        if v.get("nonfinite_D_when_S") is not None and self.S(x) == v["nonfinite_D_when_S"]:
            return float("nan")
        huge = v.get("huge_D_when_A")
        if huge is not None and a in huge:
            return float(huge[a])
        terms = []
        for lab in self._present_vertices(slots):
            bit = 1 << self.vidx[lab]
            if p & bit:
                terms.append(e["p"][lab])
            if q & bit:
                terms.append(e["q"][lab])
            if s & bit:
                terms.append(e["s"][lab])
        terms.append(e["U"] * a * (a - 1) / 2.0)
        terms.append(e["slot"] * self.S(x))
        for c in self._present_edges(slots):
            if (inc >> c) & 1:
                terms.append(e["inc"][c])
        return math.fsum(terms)

    def reads(self, x):
        slots, edgeset, inc, p, q, s, dm = x
        vm, em = self._vmask(slots), self._emask(slots)
        return {"N_adm": float(self.A(x)), "N_part": float(_popcount(p & vm)),
                "N_on": float(_popcount(inc & em)), "N_slot": float(self.S(x)),
                "N_bound": float(_popcount(q & vm))}

    # -- operator API (what V004's _op calls) ------------------------------------------------------
    def api(self):
        model = self

        def canonical_state_key(context, state):
            return model.wrap(model.unwrap(state))

        def _recs(state):
            out = []
            for r in model.records(model.unwrap(state)):
                r2 = dict(r)
                r2["target_state"] = model.wrap(r["target_state"])
                out.append(r2)
            return out

        def primitive_channels(context, state):
            return _recs(state)

        def palette_channels(context, state, palette_owners):
            return _recs(state)  # V004 _palette_members filters by permanent groups

        def diagonal_terms(context, state):
            return [{"kind": "diag", "amplitude": model.d_h(model.unwrap(state)),
                     "energy_weights": {"cell0": 1.0}}]

        def read_rows(context, state):
            x = model.unwrap(state)
            rf = model.variants.get("read_fail_when_A")
            rs = model.variants.get("read_fail_when_S")
            if (rf is not None and model.A(x) == rf) or (rs is not None and model.S(x) == rs):
                raise RuntimeError("double read_rows/source evaluation failure (fixture injection)")
            vals = model.reads(x)
            return {"labels": READ_LABELS, "values": [vals[l] for l in READ_LABELS],
                    "presence": [1.0] * len(READ_LABELS)}

        return {"canonical_state_key": canonical_state_key, "primitive_channels": primitive_channels,
                "palette_channels": palette_channels, "diagonal_terms": diagonal_terms,
                "read_rows": read_rows}


def _subsets(bits):
    out = [0]
    for b in bits:
        out = out + [m | (1 << b) for m in out]
    return out


def _product(choices):
    out = [()]
    for ch in choices:
        out = [t + (c,) for t in out for c in ch]
    return out


def make_run(model, beta=1.3, budget_hook=None, caps=None, stage="M2-double"):
    c = {"max_events_per_path": 64, "max_channel_enumerations": 10 ** 9}
    if caps:
        c.update(caps)
    return {
        "stage": stage, "beta": float(beta), "caps": c, "group": dict(model.group),
        "kinds": dict(KIND_TABLE), "gauge": {k: 1.0 for k in KIND_TABLE},
        "tol": {"gauge_phase": 1e-12, "reverse_rate": 1e-12},
        "counters": {"events": 0, "channel_enumerations": 0, "restricted_enumerations": 0,
                     "restricted_nonmember_records_dropped": 0, "palette_verifications": 0,
                     "budget_checks": 0},
        "budget_hook": budget_hook, "budget_log": [],
        "api": model.api(), "context": model,
        "sources": dict(model.sources), "source_coords": tuple(model.sources),
        "tracked_all": READ_LABELS, "n_u": len(model.sources), "lapse_index": {}, "lapse_dirs": [],
        "allk": None, "zero_rate_directions": set(), "palette": {"verify": False},
    }


def build_path(run, sampler, x0, events, times, share_wrap=False):
    """Closed path from raw x0 and (kind, owner) events, through the API double (as V004
    _initial_path does): segments via _segment_core, events via _event_from_channel."""
    model = run["context"]
    if len(events) != len(times):
        raise ValueError("events/times length mismatch")
    x = model.wrap(x0)
    segs = [sampler._segment_core(run, x)]
    evs = []
    for kind, owner in events:
        cs, _ = sampler._channels_at(run, x)
        ch = sampler._unique_mark(run, cs, kind, owner, "build_path")
        if ch is None:
            raise ValueError(f"build_path: no mark {kind!r} {owner!r} at {x!r}")
        evs.append(sampler._event_from_channel(run, ch))
        x = ch["target"]
        segs.append(sampler._segment_core(run, x))
    if not sampler._keys_equal(run, segs[0]["key"], segs[-1]["key"]):
        raise ValueError("build_path: path not closed")
    if share_wrap and events:
        segs[-1] = segs[0]  # as after V004 _rotate: first and wrap segment are one object
    return {"segments": segs, "events": evs, "times": list(times)}


# ----------------------------------------------------------------------------------------------
# ORACLE (raw physics only; independent of the sampler-API layer and of any module under test)
# ----------------------------------------------------------------------------------------------


def raw_marks(model, x):
    """{(kind, owner): (target_raw, W)} with W = |amp| * multiplier; zero-multiplier dropped."""
    out = {}
    for rec in model.records(x):
        m = rec["double_mult"]
        mag = abs(rec["amplitude"])
        if mag == 0.0 or m == 0.0:
            continue
        key = (rec["kind"], rec["owner_id"])
        if key in out:
            raise ValueError(f"oracle: ambiguous mark {key!r}")
        out[key] = (rec["target_state"], mag * m)
    return out


def raw_marks_ordered(model, x):
    out = []
    for rec in model.records(x):
        if abs(rec["amplitude"]) == 0.0 or rec["double_mult"] == 0.0:
            continue
        out.append((rec["kind"], rec["owner_id"], rec["target_state"], abs(rec["amplitude"]) * rec["double_mult"]))
    return out


def D_raw(model, x):
    vals = model.reads(x)
    src = math.fsum([-j * vals[lbl] for lbl, j in model.sources.items()])
    return math.fsum([model.d_h(x), src])


def oracle_log_pi(model, beta, xs, evs, times):
    """log pi(path) = -sum_i dt_i D(x_i) + sum_k log W(event_k), from raw physics."""
    ends = [0.0] + list(times) + [float(beta)]
    terms = [-(ends[i + 1] - ends[i]) * D_raw(model, xs[i]) for i in range(len(xs))]
    for j, (kind, owner) in enumerate(evs):
        tgt, w = raw_marks(model, xs[j])[(kind, owner)]
        if tgt != xs[j + 1]:
            raise ValueError("oracle_log_pi: event does not connect dwells")
        terms.append(math.log(w))
    return math.fsum(terms)


INVERSE = {"admit": "admit_rev", "admit_rev": "admit", "birth": "birth_rev", "birth_rev": "birth"}


def roster_admission(model, x, label):
    """Contract roster: actual positive admit/admit_rev marks with owner exactly
    ("admission", ("vertex", label)) at x, in operator record order."""
    own = ("admission", ("vertex", label))
    return [(k, o) for (k, o, _t, _w) in raw_marks_ordered(model, x) if k in ("admit", "admit_rev") and o == own]


def roster_birth(model, x, label):
    """Pinned Birth roster rule (L28-29)."""
    return [(k, o) for (k, o, _t, _w) in raw_marks_ordered(model, x)
            if k in ("birth", "birth_rev") and o[0] == "birth" and o[1] == label]


ROSTER_RULES = {"admission": roster_admission, "birth": roster_birth}


def oracle_transport(model, beta, xs, evs, times, rule, label, mark_index):
    """Whole-path transport of mark roster[mark_index] at the reference dwell, from raw physics.
    Returns dict(status='legal', ys, logmh, nf, nr, terms, new_w) or dict(status=<self-loop reason>)."""
    roster_fn = ROSTER_RULES[rule]
    r0 = roster_fn(model, xs[0], label)
    if not r0:
        return {"status": "empty_reference_owner", "nf": 0}
    kind, owner = r0[mark_index]
    inv = INVERSE[kind]
    ys = []
    for x in xs:
        mk = raw_marks(model, x)
        if (kind, owner) not in mk:
            return {"status": "dwell_guard", "nf": len(r0)}
        y = mk[(kind, owner)][0]
        back = raw_marks(model, y).get((inv, owner))
        if back is None:
            return {"status": "inverse_guard", "nf": len(r0)}
        if back[0] != x:
            return {"status": "inverse_canonical_target", "nf": len(r0)}
        ys.append(y)
    if ys[0] != ys[-1]:
        return {"status": "transformed_not_closed", "nf": len(r0)}
    r1 = roster_fn(model, ys[0], label)
    if (inv, owner) not in r1 or raw_marks(model, ys[0])[(inv, owner)][0] != xs[0]:
        return {"status": "reverse_selection", "nf": len(r0)}
    ends = [0.0] + list(times) + [float(beta)]
    terms = [math.log(len(r0)) - math.log(len(r1))]
    d_terms = []
    for i, (x, y) in enumerate(zip(xs, ys)):
        d_terms.append(-(ends[i + 1] - ends[i]) * (D_raw(model, y) - D_raw(model, x)))
    w_terms, new_w = [], []
    for j, (k2, o2) in enumerate(evs):
        before = raw_marks(model, xs[j]).get((k2, o2))
        after = raw_marks(model, ys[j]).get((k2, o2))
        if after is None or after[0] != ys[j + 1]:
            return {"status": "event_replay", "nf": len(r0)}
        w_terms.append(math.log(after[1]) - math.log(before[1]))
        new_w.append(after[1])
    logmh = math.fsum(terms + d_terms + w_terms)
    logmh_pi = math.fsum([terms[0], oracle_log_pi(model, beta, ys, evs, times),
                          -oracle_log_pi(model, beta, xs, evs, times)])
    return {"status": "legal", "ys": ys, "kind": kind, "owner": owner, "nf": len(r0), "nr": len(r1),
            "logmh": logmh, "logmh_pi_form": logmh_pi, "count_term": terms[0],
            "d_term": math.fsum(d_terms), "w_term": math.fsum(w_terms), "new_w": new_w}


def path_states(model, path):
    return tuple(model.unwrap(seg["state"]) for seg in path["segments"])


# ----------------------------------------------------------------------------------------------
# Controlled RNG, budget hooks, deep comparison
# ----------------------------------------------------------------------------------------------


class RNGExhausted(BaseException):
    """Scripted RNG has no value for this draw (BaseException: not swallowed by except Exception)."""


class NeedBranch(BaseException):
    def __init__(self, low, high):
        BaseException.__init__(self, low, high)
        self.low, self.high = low, high


class NeedU(BaseException):
    pass


class ScriptedRNG:
    """numpy-Generator-like: integers/choice/random/uniform from scripted queues; logs all draws.
    branch=True turns an exhausted integer queue into NeedBranch, and u=None into NeedU."""

    def __init__(self, ints=(), reals=(), branch=False):
        self.ints = list(ints)
        self.reals = list(reals)
        self.branch = branch
        self.log = []

    def _int(self, low, high, tag):
        self.log.append((tag, int(low), int(high)))
        if not self.ints:
            if self.branch:
                raise NeedBranch(int(low), int(high))
            raise RNGExhausted((tag, low, high))
        v = self.ints.pop(0)
        if callable(v):
            v = v(int(low), int(high))
        if not (low <= v < high):
            raise RNGExhausted(("out_of_range", tag, low, high, v))
        return np.int64(v)

    def integers(self, low, high=None, size=None, dtype=None, endpoint=False):
        if size is not None:
            raise RNGExhausted(("size_unsupported",))
        if high is None:
            low, high = 0, low
        if endpoint:
            high = high + 1
        return self._int(low, high, "integers")

    def choice(self, a, size=None, replace=True, p=None):
        if size is not None or p is not None:
            raise RNGExhausted(("choice_args_unsupported",))
        if isinstance(a, (int, np.integer)):
            return self._int(0, int(a), "choice")
        seq = list(a)
        return seq[int(self._int(0, len(seq), "choice"))]

    def random(self, size=None):
        if size is not None:
            raise RNGExhausted(("size_unsupported",))
        self.log.append(("random",))
        if not self.reals:
            if self.branch:
                raise NeedU()
            raise RNGExhausted(("random",))
        return float(self.reals.pop(0))

    def uniform(self, low=0.0, high=1.0, size=None):
        return low + (high - low) * self.random(size)


class CountingHook:
    """budget_hook returning True exactly at call number `trigger` (1-based); None never stops."""

    def __init__(self, trigger=None):
        self.trigger = trigger
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return self.trigger is not None and self.calls == self.trigger


def deep_equal(a, b, where="$"):
    """Strict structural equality (types, numpy dtype/shape/values, float bits up to -0.0)."""
    if type(a) is not type(b):
        return False, f"{where}: type {type(a).__name__} != {type(b).__name__}"
    if isinstance(a, dict):
        if set(a) != set(b):
            return False, f"{where}: keys differ {sorted(map(repr, set(a) ^ set(b)))}"
        for k in a:
            ok, w = deep_equal(a[k], b[k], f"{where}[{k!r}]")
            if not ok:
                return ok, w
        return True, None
    if isinstance(a, (list, tuple)):
        if len(a) != len(b):
            return False, f"{where}: length {len(a)} != {len(b)}"
        for i, (u, v) in enumerate(zip(a, b)):
            ok, w = deep_equal(u, v, f"{where}[{i}]")
            if not ok:
                return ok, w
        return True, None
    if isinstance(a, np.ndarray):
        if a.dtype != b.dtype or a.shape != b.shape or not np.array_equal(a, b, equal_nan=True):
            return False, f"{where}: ndarray differs"
        return True, None
    if isinstance(a, float):
        if a == b or (a != a and b != b):
            return True, None
        return False, f"{where}: {a!r} != {b!r}"
    try:
        eq = a == b
    except Exception as exc:
        return False, f"{where}: not comparable ({exc})"
    if isinstance(eq, (bool, np.bool_)) and bool(eq):
        return True, None
    return False, f"{where}: {a!r} != {b!r}"


def path_ids(path):
    return (id(path), id(path["segments"]), tuple(map(id, path["segments"])), id(path["events"]),
            tuple(map(id, path["events"])), id(path["times"]))
