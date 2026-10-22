"""Source component for the P112 successor; composed into its verified namespace.

No import side effects. Every runtime input goes through P112's single-buffer
reader. Only metadata selection is added; the root retains launch ownership.
"""

CW8_LICENSE_SCHEMA = "CW8_PHASE1_LICENSE_CX3V001"
CW8_FORECAST_SCHEMA = "CW8_PHASE1_FORECAST_CX3V001"
CW8_CHOICE_SCHEMA = "CW8_PHASE1_CHOICE_CX3V001"
CW8_EQUAL = "SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON"
CW8_RSS_MULTIPLIER = 11  # Proposed A177 accounting; requires the root license.
CW8_MAX_FORECAST_AGE_S = 900
CW8_SCOPE_KEYS = ("plan_output_primary", "plan_build_record", "selection", "fdplan",
                  "spec_of_record", "at0a_pass", "members", "f_points")
CW8_COSTS = {
    "expectation": {"serial_h": 31.90, "parallel_a_h": 5.84, "parallel_tail_h": 15.74},
    "upper": {"serial_h": 84.77, "parallel_a_h": 17.52, "parallel_tail_h": 34.33},
}

# CW8_SOURCE_PINS is inserted by the build script, from exact source bytes.


def cw8_scope(ctx):
    return {key: ctx.cfg[key] for key in CW8_SCOPE_KEYS}


def cw8_root_license_pin(text):
    """One exact root registration, inside an A-numbered section."""
    section, found = None, []
    for line in text.splitlines():
        if line.startswith("## "):
            match = re.match(r"## (A[0-9]+)(?=[:\s]|$)", line)
            section = match[1] if match else None
        if not line.startswith("CW8_LICENSE_PIN"):
            continue
        match = re.fullmatch(r"CW8_LICENSE_PIN path=(/.*\S) sha256=([0-9a-f]{64})", line)
        need(match is not None and section is not None, "CW8_LICENSE_REGISTRATION_FORM")
        found.append({"path": match[1], "sha256": match[2]})
    need(len(found) <= 1, "CW8_LICENSE_REGISTRATION_DUPLICATE")
    return found[0] if found else None


def cw8_leaf_span(raw):
    """Locate the JSON value structurally, without reserializing any other byte."""
    text = raw.decode("utf-8")
    strict_json(raw)  # Duplicate keys and nonfinite numbers refuse first.
    decoder, spans = json.JSONDecoder(), []

    def ws(i):
        while i < len(text) and text[i] in " \t\r\n":
            i += 1
        return i

    def walk(i, path):
        i = ws(i)
        start = i
        if text[i] == "{":
            i = ws(i + 1)
            while text[i] != "}":
                key, i = decoder.raw_decode(text, i)
                i = ws(i)
                need(text[i] == ":", "CW8_SPEC_JSON")
                i = ws(walk(i + 1, path + (key,)))
                if text[i] == "}":
                    break
                need(text[i] == ",", "CW8_SPEC_JSON")
                i = ws(i + 1)
            end = i + 1
        elif text[i] == "[":
            i, index = ws(i + 1), 0
            while text[i] != "]":
                i = ws(walk(i, path + (index,)))
                index += 1
                if text[i] == "]":
                    break
                need(text[i] == ",", "CW8_SPEC_JSON")
                i = ws(i + 1)
            end = i + 1
        else:
            _, end = decoder.raw_decode(text, i)
        if path == LEAF:
            spans.append((len(text[:start].encode("utf-8")),
                          len(text[:end].encode("utf-8"))))
        return end

    walk(0, ())
    need(len(spans) == 1, "CW8_SPEC_LEAF_NOT_UNIQUE")
    return spans[0]


def cw8_spec_pair(serial_raw, parallel_raw):
    serial, parallel = strict_json(serial_raw), strict_json(parallel_raw)
    need(type(dig(serial, LEAF)) is int and dig(serial, LEAF) == 1, "CW8_SERIAL_LEAF")
    need(type(dig(parallel, LEAF)) is int and dig(parallel, LEAF) == 8, "CW8_PARALLEL_LEAF")
    start, end = cw8_leaf_span(serial_raw)
    need(serial_raw[start:end] == b"1" and
         serial_raw[:start] + b"8" + serial_raw[end:] == parallel_raw,
         "CW8_NONWORKER_BYTES_CHANGED")
    return parallel


def cw8_authenticate(ctx, license_pin):
    """A root-pinned comparator attestation, never its underlying run trees."""
    need(is_pin(license_pin), "CW8_LICENSE_MISSING")
    need(cw8_root_license_pin(ctx.v006_text) == license_pin, "CW8_LICENSE_NOT_ROOT_PINNED")
    obj = read_pin(license_pin)
    keys(obj, ("schema", "date_u", "scope", "comparator_record", "source_pins",
               "seed_serial_spec", "seed_twin_spec", "full_rss_multiplier"), "cw8 license")
    need(obj["schema"] == CW8_LICENSE_SCHEMA and obj["scope"] == "FULL_MEMBER_F_CALLS_ONLY",
         "CW8_LICENSE_SCOPE")
    need(type(obj["full_rss_multiplier"]) is int and
         obj["full_rss_multiplier"] == CW8_RSS_MULTIPLIER, "CW8_RSS_RULING_REQUIRED")
    need(obj["source_pins"] == CW8_SOURCE_PINS, "CW8_WORKER_SOURCE_PINS")
    need(ctx.pins["driver"] == CW8_SOURCE_PINS["driver"], "CW8_DRIVER_PIN")
    serial_pin = ctx.get_vpin("SPEC_PIN", "S0_SEED_SERIAL")
    twin_pin = ctx.get_vpin("SPEC_PIN", TWIN)
    need(obj["seed_serial_spec"] == serial_pin and obj["seed_twin_spec"] == twin_pin,
         "CW8_SEED_SPEC_PINS")
    # Verify the seed pair's actual spec bytes without opening either run.
    cw8_spec_pair(read_pin(serial_pin, decode=False), read_pin(twin_pin, decode=False))
    record = read_pin(obj["comparator_record"])
    need(record.get("schema") == "UNT_STEP5_NGC_IDENTITY_PAIR_RECORD_C2V001",
         "CW8_COMPARATOR_SCHEMA")
    need(record.get("verdict") == CW8_EQUAL, "CW8_COMPARATOR_" + str(record.get("verdict")))
    need(record.get("bitwise_equal") is True, "CW8_COMPARATOR_NOT_BITWISE_EQUAL")
    need(record.get("iterations_compared") == [0, 1] and
         all(type(x) is int for x in record["iterations_compared"]), "CW8_TWO_ITERATIONS_REQUIRED")
    expected = {"driver": CW8_SOURCE_PINS["driver"],
                "checkpoint_module": CW8_SOURCE_PINS["checkpoint_module"],
                "tool": CW8_SOURCE_PINS["comparator"],
                "serial_spec": serial_pin, "twin_spec": twin_pin}
    need(record.get("pins") == expected, "CW8_COMPARATOR_PINS")
    checks = record.get("checks")
    need(type(checks) is dict and checks and all(v is True for v in checks.values()) and
         record.get("differing_files") == [] and record.get("not_ready") == [] and
         record.get("values_printed") is False, "CW8_COMPARATOR_CHECKS")
    # The comparator attests worker/solver custody. Verify the fixed source bytes
    # as well; none is imported or executed by this authorization check.
    for source_pin in CW8_SOURCE_PINS.values():
        read_pin(source_pin, decode=False)
    return obj


def cw8_schedule(n, available_cores, workers, cost):
    """0818 uniform-call planning model: eight-core A then one-core tail."""
    need(type(n) is int and 1 <= n <= 3, "CW8_MODEL_COHORT_OUT_OF_SCOPE")
    need(type(available_cores) is int and 12 <= available_cores <= 18,
         "CW8_MODEL_LOAD_OUT_OF_SCOPE")
    if workers == 1:
        return cost["serial_h"]  # At most three calls, at least twelve cores.
    need(workers == 8, "CW8_MODEL_WORKERS")
    # All tails retain a core immediately when their A stage finishes. An A
    # completion releases seven cores. The next A starts only if eight are free.
    time, pending, active, completion = 0.0, n, [], []
    while pending or active:
        busy = sum(item[1] for item in active)
        while pending and busy + 8 <= available_cores:
            active.append((time + cost["parallel_a_h"], 8, "A"))
            busy += 8
            pending -= 1
        need(active, "CW8_MODEL_NO_FEASIBLE_SCHEDULE")
        time = min(item[0] for item in active)
        ended, active = ([x for x in active if x[0] == time],
                         [x for x in active if x[0] != time])
        for _, cores, stage in ended:
            if stage == "A":
                active.append((time + cost["parallel_tail_h"], 1, "TAIL"))
            else:
                completion.append(time)
    return max(completion)


def cw8_predict(forecast, names, now_utc):
    keys(forecast, ("schema", "date_u", "observed_utc", "calls", "host_cores",
                    "cores_in_use", "remaining_barrier_h", "scope"), "cw8 forecast")
    need(forecast["schema"] == CW8_FORECAST_SCHEMA, "CW8_FORECAST_SCHEMA")
    need(type(forecast["calls"]) is list and forecast["calls"] == sorted(names),
         "CW8_FORECAST_CALL_SET")
    need(forecast["host_cores"] == 18 and type(forecast["host_cores"]) is int,
         "CW8_MODEL_HOST")
    used = forecast["cores_in_use"]
    need(type(used) is int and 0 <= used <= 6, "CW8_MODEL_LOAD_OUT_OF_SCOPE")
    age = timestamp(now_utc) - timestamp(forecast["observed_utc"])
    need(0 <= age <= CW8_MAX_FORECAST_AGE_S, "CW8_FORECAST_STALE_OR_FUTURE")
    barrier = forecast["remaining_barrier_h"]
    need(type(barrier) is dict and set(barrier) == set(CW8_COSTS),
         "CW8_FORECAST_BARRIER")
    predictions = {}
    for scenario, cost in CW8_COSTS.items():
        r = barrier[scenario]
        need(type(r) in (int, float) and math.isfinite(r) and r >= 0, "CW8_FORECAST_BARRIER")
        serial = max(r, cw8_schedule(len(names), 18 - used, 1, cost))
        parallel = max(r, cw8_schedule(len(names), 18 - used, 8, cost))
        predictions[scenario] = {
            "serial_makespan_h": serial, "cw8_makespan_h": parallel,
            "predicted_saving_h": serial - parallel,
        }
    # No gain hidden behind S0 and no expectation/upper tradeoff.
    choose = all(v["predicted_saving_h"] > 0 for v in predictions.values())
    return {"column_workers": 8 if choose else 1,
            "reason": "PREDICTED_MAKESPAN_SHORTER" if choose else "NO_STRICT_MAKESPAN_GAIN",
            "scenarios": predictions, "model": "0818_UNIFORM_CALLS_1_TO_3_CORES_12_TO_18",
            "measured_speedup": False}


def cw8_choice_directory(ctx):
    return Path(ctx.cfg["p112_launch_root"]) / "worker_choices"


def cw8_saved_choices(ctx):
    directory = cw8_choice_directory(ctx)
    if not directory.exists():
        return {}
    need(directory.is_dir() and os.path.realpath(directory) == str(directory), "CW8_CHOICE_DIRECTORY")
    found = {}
    for path in sorted(directory.glob("CHOICE_*.json")):
        pin, doc = read_record(path)
        need(doc.get("schema") == CW8_CHOICE_SCHEMA and doc.get("scope") == cw8_scope(ctx),
             "CW8_CHOICE_SCOPE")
        need(doc.get("producer") == ctx.own_pin, "CW8_CHOICE_PRODUCER")
        rows = doc.get("calls")
        need(type(rows) is list and rows, "CW8_CHOICE_CALLS")
        for row in rows:
            name = row.get("name")
            need(type(name) is str and NAME_RE.fullmatch(name) and not name.startswith("S0_"),
                 "CW8_CHOICE_NAME")
            need(name not in found, "CW8_CHOICE_DUPLICATE", name)
            found[name] = (row, doc, pin)
    return found


def cw8_apply_choice(ctx, call):
    if call["origin"] != "P112":
        return call  # S0 ownership and worker/spec history are unchanged.
    found = cw8_saved_choices(ctx)
    if call["name"] not in found:
        return call
    row, doc, choice_pin = found[call["name"]]
    keys(row, ("name", "point_key", "theta_sha256", "serial_spec", "spec",
               "column_workers"), "cw8 choice row")
    need(row["serial_spec"] == call["spec"] and row["point_key"] == call["point_key"] and
         row["theta_sha256"] == call["theta_sha256"], "CW8_CHOICE_CALL_BINDING")
    workers = row["column_workers"]
    need(type(workers) is int and workers in (1, 8), "CW8_CHOICE_WORKERS")
    if workers == 1:
        need(row["spec"] == call["spec"], "CW8_SERIAL_SPEC_CHANGED")
    else:
        cw8_authenticate(ctx, doc.get("license"))
        forecast = read_pin(doc["forecast"])
        need(forecast.get("scope") == cw8_scope(ctx), "CW8_FORECAST_SCOPE")
        prediction = cw8_predict(forecast, [r["name"] for r in doc["calls"]],
                                 doc["selected_at_utc"])
        need(prediction == doc.get("prediction") and prediction["column_workers"] == 8 and
             all(r.get("column_workers") == 8 for r in doc["calls"]), "CW8_CHOICE_NOT_DERIVED")
        chosen_pin = ctx.get_vpin("SPEC_PIN", call["name"] + "_FULL_CW8")
        need(row["spec"] == chosen_pin, "CW8_FULL_SPEC_ROOT_PIN")
        chosen_spec = cw8_spec_pair(read_pin(call["spec"], decode=False),
                                    read_pin(chosen_pin, decode=False))
        call = dict(call, spec=chosen_pin, spec_doc=chosen_spec, v006_spec_pin=chosen_pin)
    return dict(call, worker_choice=choice_pin, serial_spec=row["serial_spec"])


def cw8_workers(call):
    workers = dig(call["spec_doc"], LEAF)
    need(type(workers) is int and workers in (1, 8), "CW8_WORKER_LEAF")
    if call["name"] == TWIN:
        need(workers == 8 and call["origin"] == "KIT", "CW8_TWIN_IDENTITY")
    elif workers == 8:
        need(call["origin"] == "P112" and is_pin(call.get("worker_choice")),
             "CW8_FULL_CALL_UNAUTHORIZED")
    return workers


def cw8_role(call):
    return {"kind": "IDENTITY_TWIN" if call["name"] == TWIN else "FULL",
            "column_workers": cw8_workers(call), "choice": call.get("worker_choice")}


def cw8_check_role(call, saved, *, allow_legacy=True):
    expected = cw8_role(call)
    if saved is None and allow_legacy and call.get("worker_choice") is None:
        return expected  # Original serial or authentic S0 twin custody.
    need(saved == expected, "CW8_ROLE_CUSTODY")
    return expected


def cw8_rss(name, workers=1):
    need(type(workers) is int and workers in (1, 8), "CW8_RSS_WORKERS")
    return RAM * (CW8_RSS_MULTIPLIER if name == TWIN or workers == 8 else 1)


def cw8_plan_workers(plan):
    role = plan.get("worker_role")
    if role is None:
        return 8 if plan["name"] == TWIN else 1
    need(type(role) is dict and set(role) == {"kind", "column_workers", "choice"},
         "CW8_PLAN_ROLE")
    workers = role["column_workers"]
    need(type(workers) is int and workers in (1, 8), "CW8_PLAN_WORKERS")
    need(role["kind"] == ("IDENTITY_TWIN" if plan["name"] == TWIN else "FULL"),
         "CW8_PLAN_ROLE")
    need(dig(read_pin(plan["spec"]), LEAF) == workers, "CW8_PLAN_SPEC_LEAF")
    if workers == 8 and plan["name"] != TWIN:
        need(is_pin(role["choice"]), "CW8_PLAN_UNAUTHORIZED")
        choice = read_pin(role["choice"])
        rows = [r for r in choice.get("calls", []) if r.get("name") == plan["name"]]
        need(len(rows) == 1 and rows[0].get("spec") == plan["spec"] and
             rows[0].get("column_workers") == 8, "CW8_PLAN_CHOICE_BINDING")
    return workers


def cw8_admission_clear(ctx, call):
    need(call["origin"] == "P112" and not call["name"].startswith("S0_"),
         "CW8_EXISTING_S0_ROLE")
    name = call["name"]
    need(not ctx.record_paths(name) and not any(n == name for n, _ in ctx.residuals()) and
         not Path(own_registry_path(ctx, name)).exists(), "CW8_ROLE_ALREADY_STARTED")
    # Includes early refusal plans and dry preparation. A choice must precede
    # any preparatory plan so restart cannot see two candidate worker roles.
    work = Path(ctx.cfg["p112_launch_root"]) / "work"
    need(not work.exists() or not any(work.glob(name + "_A*")), "CW8_ROLE_ALREADY_PREPARED")


@read_scope
def select_workers(ctx, forecast_pin=None, *, serial_name=None):
    """Root-invoked metadata operation. Writes one immutable cohort record."""
    ctx.gate()
    calls = ctx.calls()
    saved = cw8_saved_choices(ctx)
    if serial_name is not None:
        call = ctx.call(serial_name)
        if serial_name in saved:
            return {"status": "ALREADY_SELECTED", "choice": saved[serial_name][2]}
        selected = [call]
    else:
        selected = [c for c in calls if c["origin"] == "P112" and c["name"] not in saved and
                    not ctx.record_paths(c["name"]) and
                    not Path(own_registry_path(ctx, c["name"])).exists()]
    need(selected, "CW8_NO_NEW_CALLS")
    for call in selected:
        cw8_admission_clear(ctx, call)
    now = ctx.system.utc()
    license_pin, prediction = None, {"column_workers": 1, "reason": "NO_SELECTION_INPUT"}
    if serial_name is None:
        try:
            license_pin = cw8_root_license_pin(ctx.v006_text)
            cw8_authenticate(ctx, license_pin)
            need(is_pin(forecast_pin), "CW8_FORECAST_MISSING")
            forecast = read_pin(forecast_pin)
            need(forecast.get("scope") == cw8_scope(ctx), "CW8_FORECAST_SCOPE")
            prediction = cw8_predict(forecast, [c["name"] for c in selected], now)
            if prediction["column_workers"] == 8:
                for call in selected:
                    pin = ctx.get_vpin("SPEC_PIN", call["name"] + "_FULL_CW8")
                    cw8_spec_pair(read_pin(call["spec"], decode=False), read_pin(pin, decode=False))
        except (Refusal, OSError, ValueError, KeyError, TypeError) as exc:
            prediction = {"column_workers": 1,
                          "reason": exc.code if isinstance(exc, Refusal) else type(exc).__name__}
    workers = prediction["column_workers"]
    rows = []
    for call in sorted(selected, key=lambda c: c["name"]):
        rows.append({key: call[key] for key in ("name", "point_key", "theta_sha256")})
        rows[-1].update(serial_spec=call["spec"], column_workers=workers,
                        spec=(ctx.get_vpin("SPEC_PIN", call["name"] + "_FULL_CW8")
                              if workers == 8 else call["spec"]))
    record = {"schema": CW8_CHOICE_SCHEMA, "producer": ctx.own_pin, "scope": cw8_scope(ctx),
              "selected_at_utc": now, "date_u": date_u(), "license": license_pin,
              "forecast": forecast_pin, "prediction": prediction, "calls": rows}
    directory = cw8_choice_directory(ctx)
    if not directory.exists():
        directory.mkdir()
    need(directory.is_dir() and os.path.realpath(directory) == str(directory), "CW8_CHOICE_DIRECTORY")
    # One cohort record is the authority for every row. There is no multi-file
    # commit window in which a partial cohort could be silently re-optimized.
    destination = directory / ("CHOICE_" + sha(canonical(record)) + ".json")
    pin = ctx.write(str(destination), record)
    ctx._calls = None
    ctx.calls()  # Reconstruct using the durable bytes before returning.
    return {"status": "SELECTED", "choice": pin, "column_workers": workers,
            "reason": prediction["reason"], "names": [r["name"] for r in rows]}


def cw8_ensure_default(ctx, call):
    """A new root launch with no selection gets an explicit serial record."""
    if call["origin"] != "P112" or call.get("worker_choice") is not None:
        return call
    name = call["name"]
    work = Path(ctx.cfg["p112_launch_root"]) / "work"
    if (ctx.record_paths(name) or Path(own_registry_path(ctx, name)).exists() or
            any(n == name for n, _ in ctx.residuals()) or
            (work.exists() and any(work.glob(name + "_A*")))):
        return call  # Historical serial custody/preparation cannot be upgraded.
    select_workers(ctx, serial_name=call["name"])
    return ctx.call(call["name"])


def cw8_check_attempt(ctx, call, record, closed=None):
    role = cw8_check_role(call, record.get("worker_role"))
    need(record.get("spec", call["spec"]) == call["spec"], "CW8_ATTEMPT_RAW_SPEC")
    need(record["caps"]["rss_cap_bytes"] == cw8_rss(call["name"], role["column_workers"]),
         "CW8_ATTEMPT_RSS")
    if call["name"] != TWIN:
        need(record.get("watch_pid") is None, "CW8_FULL_CALL_TWIN_WATCHER")
    if closed is not None:
        cw8_check_role(call, closed.get("worker_role"))
    return role["column_workers"]
