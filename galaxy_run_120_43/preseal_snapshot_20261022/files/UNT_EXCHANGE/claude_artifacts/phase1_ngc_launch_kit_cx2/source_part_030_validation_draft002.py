# Validation component. Composed after the core and the pinned source constants.
PRIMARY = "BR_A_F10_PRIMARY"
CONFIG_KEYS = (
    "schema", "python", "v006", "v006_copy_dir", "run_volume", "run_root",
    "p112_launch_root", "s0", "host_ram_bytes_expected", "plan_output_primary",
    "plan_build_record", "selection", "fdplan", "spec_of_record", "at0a_pass",
    "members", "f_points")


def theta_key(theta):
    """Verbatim algorithm of pinned orchestrator c2v005 theta_key."""
    th = {str(k): float(v) for k, v in theta.items()}
    for k, v in th.items():
        need(math.isfinite(v), "THETA_NONFINITE", k)
    return sha(canonical({"schema": "DDO154_CALIBRATION_THETA_KEY_C2V001", "theta": th}))


def dig(obj, path):
    try:
        for key in path:
            obj = obj[key]
        return obj
    except (KeyError, TypeError):
        raise Refusal("MISSING_FIELD", ".".join(path)) from None


def check_geometry(spec, seed_spec, theta_ngc=None):
    for coord, fixed in (("distance_Mpc", 13.8), ("inclination_deg", 72.0)):
        value = dig(spec, ("physical", coord))
        equal_hex(value, fixed, "geometry." + coord)
        equal_hex(value, dig(seed_spec, ("physical", coord)), "seed." + coord)
        if theta_ngc is not None:
            # The saved PLAN is authoritative. Permit the two explicit field
            # spellings; ambiguous or missing nuisance fields fail closed.
            names = [n for n in (coord, "ngc3198_" + coord) if n in theta_ngc]
            need(len(names) == 1, "PLAN_NUISANCE_FIELD", coord)
            equal_hex(value, theta_ngc[names[0]], "PLAN.theta_ngc." + names[0])


def check_derivation(theta, spec):
    physical = spec["physical"]
    values = {
        "Eref_J": theta["Eref_base_J"], "ell_F_m": theta["ell_F_m"],
        "gamma": theta["gamma_over_Eref"] * theta["Eref_base_J"],
        "common_scale_s": theta["common_scale_s"],
        "entropy_K_factor": theta["entropy_K_factor"],
    }
    for coord, expected in values.items():
        equal_hex(physical.get(coord), expected, "spec.physical." + coord)


def check_theta_hex(theta, expected):
    need(type(expected) is dict and set(theta) == set(expected), "FDPLAN_THETA_KEY_SET")
    for coord in sorted(theta):
        need(fhex(theta[coord], coord) == expected[coord], "FDPLAN_THETA_HEX", coord)


def check_member_theta(member, fd, handoff, export, spec, seed_spec, cfg, order, builder):
    identity = (member.get("log_index"), member.get("role"), order)
    need(identity == (cfg["log_index"], cfg["role"], cfg["order"]), "MEMBER_IDENTITY")
    need(member.get("member_id") == cfg["member_id"], "MEMBER_IDENTITY")
    need(fd.get("log_index") == identity[0] and fd.get("role") == identity[1], "FDPLAN_MEMBER_IDENTITY")
    need(handoff.get("log_index") == identity[0], "HANDOFF_MEMBER_IDENTITY")
    if "order" in member:
        need(member["order"] == order, "MEMBER_ORDER")
    if "order" in fd:
        need(fd["order"] == order, "FDPLAN_MEMBER_ORDER")
    points = [p for p in export.get("admitted_points", []) if p.get("log_index") == identity[0]]
    need(len(points) == 1, "EXPORT_MEMBER_NOT_UNIQUE")
    theta = member["theta_engine"]
    equal_theta(theta, points[0]["theta_natural"], "export.theta_natural")
    check_theta_hex(theta, fd["theta_hex"])
    if "theta_natural" in fd:
        equal_theta(theta, fd["theta_natural"], "fdplan.theta_natural")
    key = theta_key(theta)
    need(key == fd["key"], "FDPLAN_POINT_KEY")
    check_derivation(theta, spec)
    check_geometry(spec, seed_spec, member["theta_ngc"])
    need(all(type(v) is float and math.isfinite(v) for v in member["theta_ngc"].values()),
         "PLAN_THETA_NGC_EXACT_FLOAT")
    return {"point_key": key, "theta_sha256": builder.theta_sha256(member["theta_ngc"]),
            "identity": list(identity), "checks": ["export_bits", "fdplan_bits", "key",
                "derived_spec_bits", "gamma_IEEE_product", "geometry_bits", "parsed_PLAN_theta_ngc_hash"]}


def check_f_theta(fd, handoff, spec, seed_spec, label):
    need(fd.get("role") == label, "F_IDENTITY")
    theta = {k: float.fromhex(v) for k, v in fd["theta_hex"].items()}
    if "theta_natural" in fd:
        equal_theta(theta, fd["theta_natural"], "F.theta_natural")
    key = theta_key(theta)
    need(key == fd["key"] == handoff["point_key"], "F_POINT_KEY")
    check_derivation(theta, spec)
    check_geometry(spec, seed_spec)
    return {"point_key": key, "theta_sha256": key, "identity": label,
            "checks": ["F_theta_hex", "handoff_point_key", "derived_spec_bits", "geometry_bits"]}


def strip_leaf(spec):
    obj = copy.deepcopy(spec)
    leaf = obj["numerics"]["route_a"].pop("column_workers")
    return obj, leaf


def fill_check(handoff, handoff_pin, serial, twin, fill_receipt, key, eps, lo, schema, synthetic=False):
    need(handoff.get("schema") == schema, "HANDOFF_SCHEMA")
    want_mode = "ADMITTED" if schema == "UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001" else "PHASE1_POINT"
    need(handoff.get("mode") == ("SYNTHETIC_DRY_ONLY" if synthetic else want_mode), "HANDOFF_MODE")
    need(handoff.get("driver_branch") == "cx3r008", "HANDOFF_DRIVER_BRANCH")
    need(handoff.get("certificate_pins") == {"eps_certificate": eps, "lo_certificate": lo},
         "HANDOFF_CERTIFICATES")
    need(fill_receipt.get("schema") == "UNT_STEP5_FILLED_SPECS_C2V001", "FILL_SCHEMA")
    need(fill_receipt.get("launch_authorized") is False, "FILL_LAUNCH_AUTHORIZED")
    need(fill_receipt.get("handoff_pin") == handoff_pin, "FILL_HANDOFF_PIN")
    need(fill_receipt.get("theta_key") == key, "FILL_POINT_KEY")
    need(fill_receipt.get("pending_certificates") == [], "FILL_PENDING_CERTIFICATES")
    for tag, spec, leaf in (("serial", serial, 1), ("twin", twin, 8)):
        need(type(dig(spec, LEAF)) is int and dig(spec, LEAF) == leaf, "SPEC_LEAF", tag)
        need(dig(spec, ("numerics", "uv_tail", "eps_certificate")) == eps, "SPEC_EPS_PIN", tag)
        need(dig(spec, ("numerics", "uv_tail", "lo_certificate")) == lo, "SPEC_LO_PIN", tag)
        need(spec.get("label") == "step5 A_K32_A2_HEADLINE theta_key=" + key, "SPEC_LABEL_KEY", tag)
    need(canonical(strip_leaf(serial)[0]) == canonical(strip_leaf(twin)[0]), "SPEC_PAIR_DIFFERENCE")
    return {"schema": "P112_FILL_CHECK_CX2V001", "ok": True, "point_key": key, "date_u": date_u()}


def dry_verdict(log, readiness, spec_pin, driver_pin):
    checks = {
        "harness_exit_0": log.get("exit") == 0,
        "no_fence_denial": log.get("blocked") == [],
        "ctx_simulate_only": bool(log.get("ctx_modes")) and set(log.get("ctx_modes")) == {"simulate"},
        "driver_sha": log.get("driver_sha256") == driver_pin["sha256"],
        "spec_sha": log.get("spec_sha256") == spec_pin["sha256"],
        "executed_stages_0": readiness.get("executed_stages") == 0,
        "binding_blockers_empty": readiness.get("binding_blockers") == [],
        "source_build_blockers_empty": readiness.get("source_build_blockers") == [],
        "future_deps_only_pending_route_a": {
            x.get("class") for x in readiness.get("future_stage_dependencies", [])} <= {"PENDING_ROUTE_A_OUTPUTS"},
        "planned_route_a": readiness.get("planned_route_a") is True,
    }
    bad = [k for k, v in checks.items() if not v]
    need(not bad, "DRY_VERDICT_REFUSED", bad)
    return {"schema": "P112_DRY_VERDICT_CX2V001", "ok": True, "checks": checks, "date_u": date_u()}


def synthetic_fence(pins, config):
    for key in ("driver", "monitor", "dry_harness"):
        need(is_pin(pins.get(key)), "SYNTHETIC_PIN_FORM", key)
        need(pins[key]["sha256"] != REAL[key]["sha256"] and
             os.path.realpath(pins[key]["path"]) != os.path.realpath(REAL[key]["path"]),
             "SYNTHETIC_REAL_TOOL", key)
    need(not re.search(r"root_monitor_c2v[0-9]+\.py", pins["monitor"]["path"]),
         "SYNTHETIC_REAL_MONITOR_NAME")
    def visit(obj):
        if isinstance(obj, str):
            need(not obj.startswith("/Volumes/") and obj != "/Volumes", "SYNTHETIC_VOLUMES")
        elif isinstance(obj, dict):
            for value in obj.values():
                visit(value)
        elif isinstance(obj, list):
            for value in obj:
                visit(value)
    visit(pins)
    visit(config)


class System:
    """Production OS interface; a synthetic subclass must fence all executable pins."""
    synthetic = False

    def mounted(self, volume):
        return os.path.realpath(volume) == volume and os.path.ismount(volume)

    def free(self, volume):
        return shutil.disk_usage(volume).free

    def ram(self):
        return int(subprocess.check_output(["/usr/sbin/sysctl", "-n", "hw.memsize"], text=True).strip())

    def processes(self):
        p = subprocess.run(["/bin/ps", "-axww", "-o", "pid=,ppid=,pgid=,command="],
                           capture_output=True, text=True, timeout=30)
        need(p.returncode == 0, "PS_FAILED")
        return parse_ps(p.stdout)

    def monotonic(self):
        return time.monotonic()

    def sleep(self, seconds):
        time.sleep(seconds)


def mount_first(config, origin, system):
    volume = attempt_volume(config, origin)
    need(system.mounted(volume), "RUN_VOLUME_NOT_MOUNTED", volume)
    need(os.path.realpath(volume) == volume, "RUN_VOLUME_NOT_MOUNTED", volume)
    return volume


def disk_check(config, outdir, caps, system):
    volume = mount_first(config, "P112", system)
    paths = absent_paths(outdir)
    if not os.path.lexists(paths["launch_json"]) and (
            os.path.lexists(paths["receipt_stdout"]) or os.path.lexists(paths["receipt_stderr"])):
        raise Refusal("MONITOR_STARTED_NO_LAUNCH_JSON")
    need(not os.path.lexists(paths["launch_json"]), "LAUNCH_RECORD_MISSING")
    for label, path in paths.items():
        need(not os.path.lexists(path), "OUTPUT_EXISTS", label)
    free = system.free(volume)
    need(free >= caps["output_cap_bytes"] + DISK_RESERVE, "DISK_FREE")
    return {"mount_point": volume, "free_bytes": free, "required_bytes": caps["output_cap_bytes"] + DISK_RESERVE}


def read_v006(path):
    # Named path exception: unlike ordinary pins this file contains ngc3198.
    need(os.path.isabs(path) and os.path.realpath(path) == path, "V006_PATH")
    return Path(path).read_bytes()


def compact_pin(parsed):
    return {k: parsed[k] for k in ("path", "sha256")}


class Context:
    def __init__(self, config_pin, *, system=None, synthetic_pins=None):
        self.system = system or System()
        self.config_pin = config_pin
        self.cfg = read_pin(config_pin)
        c = self.cfg
        keys(c, CONFIG_KEYS, "config")
        need(c["schema"] == "P112_CONFIG_CX2V001", "CONFIG_SCHEMA")
        need(c["python"] == PY, "CONFIG_PYTHON")
        need(c["host_ram_bytes_expected"] == RAM, "CONFIG_RAM")
        keys(c["s0"], ("launch_root", "run_root"), "config.s0")
        for key in ("run_root", "p112_launch_root", "v006_copy_dir", "run_volume"):
            path_rules(c[key], key)
            need(os.path.realpath(c[key]) == c[key], "CONFIG_SYMLINK", key)
        for key in ("launch_root", "run_root"):
            path_rules(c["s0"][key], "s0." + key)
        need(Path(c["run_root"]).parent == Path(c["run_volume"]) and
             Path(c["run_root"]).name.startswith("NGC_"), "RUN_ROOT_LAYOUT")
        need(not c["p112_launch_root"].startswith("/Volumes/"), "LAUNCH_ROOT_EXTERNAL")
        for root in (c["run_root"], c["s0"]["run_root"]):
            need(not c["v006_copy_dir"].startswith(root + "/") and c["v006_copy_dir"] != root,
                 "CUTOFF_COPY_IN_RUN_TREE")
        self.pins = dict(REAL)
        if synthetic_pins is not None:
            need(self.system.synthetic, "SYNTHETIC_SYSTEM_REQUIRED")
            synthetic_fence(synthetic_pins, c)
            self.pins.update(synthetic_pins)
        else:
            need(not self.system.synthetic, "SYNTHETIC_PINS_REQUIRED")
        self.synthetic = self.system.synthetic
        READ_RUN_ROOTS.update((c["run_root"], c["s0"]["run_root"]))
        self.own_pin = pin_of(str(Path(__file__).resolve()))
        self.v006_raw = read_v006(c["v006"])
        self.v006_text = self.v006_raw.decode()
        writer = load_verified(self.pins["writer"], "_p112_verified_pin_parser")
        self.vpins = writer.parse_v006_pins(self.v006_raw)["pins"]
        self.builder = load_verified(self.pins["builder"], "_p112_verified_builder")
        self._calls = None

    def gate(self):
        return tool_gate(self.v006_text, self.own_pin)

    def residuals(self):
        return residual_lines(self.v006_text)

    def write(self, path, obj):
        path = str(path)
        path_rules(path, "output")
        kit_launches = self.cfg["s0"]["launch_root"] + "/launches"
        need(path != kit_launches and not path.startswith(kit_launches + "/"), "WRITE_KIT_LAUNCHES")
        allowed = (path.startswith(self.cfg["p112_launch_root"] + "/") or
                   path.startswith(self.cfg["v006_copy_dir"] + "/"))
        for root, origin in ((self.cfg["run_root"], "P112"), (self.cfg["s0"]["run_root"], "KIT")):
            if str(Path(path).parent) == root and path.endswith((".solo.json", ".attempt_receipt.json")):
                mount_first(self.cfg, origin, self.system)
                allowed = True
        need(allowed, "WRITE_SCOPE")
        return write_x(path, obj)

    def record_paths(self, name=None):
        result = []
        for root, regex, origin in (
                (self.cfg["s0"]["launch_root"], KIT_ATTEMPT_RE, "KIT"),
                (self.cfg["p112_launch_root"], OWN_ATTEMPT_RE, "P112")):
            folder = Path(root) / "launches"
            if not folder.is_dir():
                continue
            for p in sorted(folder.iterdir()):
                m = regex.fullmatch(p.name)
                if m and (name is None or m["name"] == name):
                    result.append({"path": str(p), "name": m["name"], "outcome": m["kind"],
                                   "attempt": int(m["k"]), "origin": origin})
        return sorted(result, key=lambda r: (r["name"], r["attempt"], r["origin"]))

    def records(self, name=None):
        records, seen = [], set()
        for row in self.record_paths(name):
            key = row["name"], row["attempt"]
            need(key not in seen, "ATTEMPT_RECORD_NOT_UNIQUE", key)
            seen.add(key)
            pin = pin_of(row["path"])
            obj = read_pin(pin)
            need(obj.get("name") == row["name"] and obj.get("attempt") == row["attempt"],
                 "ATTEMPT_FILENAME_BINDING")
            schema = ("UNT_P112_" + row["outcome"] + "_RECORD_CX2V001" if row["origin"] == "P112" else
                      "UNT_S0_" + row["outcome"] + "_RECORD_C2V003A")
            need(obj.get("schema") == schema, "ATTEMPT_RECORD_SCHEMA")
            records.append(dict(obj, origin=row["origin"], outcome=row["outcome"], record_pin=pin))
        return records

    def seed_check(self):
        p = Path(self.cfg["s0"]["launch_root"]) / "M15_PRELAUNCH_RECORD_C2V001.json"
        pin = pin_of(p)
        obj = read_pin(pin)
        need(obj.get("schema") == "UNT_M15_PRELAUNCH_RECORD_C2V001", "M15_SCHEMA")
        need(any(r["outcome"] == "LAUNCH" for r in self.record_paths("S0_SEED_SERIAL")
                 if r["origin"] == "KIT"), "SEED_SERIAL_NOT_LAUNCHED_FIRST")
        return pin, obj

    def kit_entries(self):
        result = {}
        folder = Path(self.cfg["s0"]["launch_root"]) / "registry"
        for name in ("S0_SEED_SERIAL", "S0_J0_SERIAL", "S0_J1_SERIAL", "S0_J2_SERIAL", TWIN):
            p = folder / (name + "_C2V003A.json")
            if not p.exists():
                continue
            pin = pin_of(p)
            entry = read_pin(pin)
            need(entry.get("schema") == "UNT_S0_LAUNCH_REGISTRY_ENTRY_C2V003A" and entry.get("name") == name,
                 "KIT_REGISTRY_SCHEMA")
            result[name] = (entry, pin)
        return result

    def get_vpin(self, kind, name):
        pin = self.vpins[kind].get(name)
        need(pin is not None, "V006_PIN_MISSING", kind + " " + name)
        return compact_pin(pin)

    def calls(self):
        if self._calls is not None:
            return self._calls
        c = self.cfg
        plan = read_pin(c["plan_output_primary"])
        build = read_pin(c["plan_build_record"])
        selection = read_pin(c["selection"])
        fd = read_pin(c["fdplan"])
        at0 = read_pin(c["at0a_pass"])
        need(at0.get("schema") == "PHASE1_AT0A_C2V001" and at0.get("outcome") == "PASS", "AT0A_NOT_PASS")
        need(build.get("status") == "BUILT" and build.get("stage") == "PLAN" and
             build.get("phase") == "PHASE_1", "PLAN_BUILD_RECORD")
        need(c["spec_of_record"] == self.pins["spec_of_record"], "SPEC_OF_RECORD")
        read_pin(c["spec_of_record"], decode=False)
        need(plan.get("ok") is True and plan.get("budget") == 0 and plan.get("evaluations_used") == 0,
             "PLAN_NOT_BUDGET_ZERO")
        members = plan.get("members")
        need(type(members) is list and members and all(m.get("evaluated") is False for m in members),
             "PLAN_NOT_VALUE_FREE")
        need(fd.get("schema") == "PHASE1_FDPLAN_C2V001", "FDPLAN_SCHEMA")
        need(len(members) == len(c["members"]) == len(fd["members"]), "MEMBER_COUNT")
        sel = selection.get("points")
        need(type(sel) is list and len(sel) == len(members), "SELECTION_MEMBERS")
        kit = self.kit_entries()
        need("S0_SEED_SERIAL" in kit, "SEED_REGISTRY_MISSING")
        seed_spec = read_pin(kit["S0_SEED_SERIAL"][0]["spec"])
        calls, seen = [], {}
        for order, (m, fdm, cfg, sm) in enumerate(zip(members, fd["members"], c["members"], sel)):
            keys(cfg, ("log_index", "role", "order", "member_id", "handoff", "fill_dir", "eps", "gq"), "member")
            need((sm.get("log_index"), sm.get("role")) == (m.get("log_index"), m.get("role")), "SELECTION_IDENTITY")
            name = "P1_M%04d" % cfg["log_index"]
            handoff = read_pin(cfg["handoff"])
            export = read_pin(handoff["source_export_pin"])
            spec, sp, fill, fc = self.read_fill(cfg)
            check = check_member_theta(m, fdm, handoff, export, spec, seed_spec, cfg, order, self.builder)
            call = self.finish_call(name, cfg, handoff, spec, sp, fill, fc, check, "MEMBER", PRIMARY,
                                    m["member_id"], kit)
            need(check["point_key"] not in seen, "DUPLICATE_MEMBER_POINT")
            seen[check["point_key"]] = call
            calls.append(call)
        need([f["label"] for f in c["f_points"]] == ["F0", "F1", "F2"], "F_LABELS")
        need(len(fd["F"]) == 3, "F_COUNT")
        for fdm, cfg in zip(fd["F"], c["f_points"]):
            keys(cfg, ("label", "handoff", "fill_dir", "eps", "gq"), "F")
            handoff = read_pin(cfg["handoff"])
            need(handoff.get("source_pin") == c["fdplan"], "F_SOURCE_FDPLAN")
            spec, sp, fill, fc = self.read_fill(cfg)
            check = check_f_theta(fdm, handoff, spec, seed_spec, cfg["label"])
            call = self.finish_call("P1_" + cfg["label"], cfg, handoff, spec, sp, fill, fc,
                                    check, "OTHER", None, cfg["label"], kit)
            if check["point_key"] in seen:
                seen[check["point_key"]].setdefault("serves", []).append(cfg["label"])
            else:
                calls.append(call)
                seen[check["point_key"]] = call
        need(TWIN in kit, "TWIN_REGISTRY_MISSING")
        entry, ep = kit[TWIN]
        spec = read_pin(entry["spec"])
        need(entry.get("theta_key") == SEED_KEY and dig(spec, LEAF) == 8, "TWIN_REGISTRY_BINDING")
        need(entry["spec"] == self.get_vpin("SPEC_PIN", TWIN), "TWIN_SPEC_V006")
        calls.append({"name": TWIN, "kind": "OTHER", "alternative": None, "key": TWIN, "point_key": SEED_KEY,
                      "theta_sha256": SEED_KEY, "entry": entry, "entry_pin": ep, "spec": entry["spec"],
                      "spec_doc": spec, "origin": "KIT"})
        self._calls = calls
        return calls

    def read_fill(self, cfg):
        folder = path_rules(cfg["fill_dir"], "fill_dir")
        need(Path(folder).is_dir() and os.path.realpath(folder) == folder, "FILL_DIR_REAL")
        for k in ("eps", "gq"):
            read_pin(cfg[k])  # Only point.key is interpreted by finish_call.
        read_pin(self.pins["lo"], decode=False)
        pins = {name: pin_of(Path(folder) / name) for name in (SERIAL_FILE, TWIN_FILE, FILL_FILE)}
        serial, twin, receipt = (read_pin(pins[name]) for name in (SERIAL_FILE, TWIN_FILE, FILL_FILE))
        return serial, pins[SERIAL_FILE], (serial, twin, receipt), pins[FILL_FILE]

    def finish_call(self, name, cfg, handoff, spec, spec_pin, fill, fill_pin, check, kind, alternative, key, kit):
        point_key = check["point_key"]
        for certificate in ("eps", "gq"):
            obj = read_pin(cfg[certificate])
            need(dig(obj, ("point", "key")) == point_key, "CERTIFICATE_POINT_KEY", certificate)
        schema = ("UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001" if kind == "MEMBER" else
                  "UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001")
        fc = fill_check(handoff, cfg["handoff"], *fill, point_key, cfg["eps"], self.pins["lo"], schema, self.synthetic)
        hits = [(n, e, p) for n, (e, p) in kit.items() if n != TWIN and e.get("theta_key") == point_key]
        need(len(hits) <= 1, "KIT_POINT_DUPLICATE")
        entry, ep = None, None
        original_name = name
        if hits:
            name, entry, ep = hits[0]
            kit_spec = read_pin(entry["spec"])
            # Equal key is not sufficient: independently compare every physical bit.
            need(set(kit_spec["physical"]) == set(spec["physical"]), "KIT_PHYSICAL_KEYS")
            for coord in spec["physical"]:
                equal_hex(kit_spec["physical"][coord], spec["physical"][coord], "kit.spec." + coord)
            need(entry["spec"] == self.get_vpin("SPEC_PIN", name), "KIT_SPEC_V006")
            spec_pin, spec = entry["spec"], kit_spec
            hp = entry["v006_handoff_pin"]
        else:
            hp = self.get_vpin("HANDOFF_PIN", name)
            need(hp == cfg["handoff"], "HANDOFF_V006_PIN")
            need(spec_pin == self.get_vpin("SPEC_PIN", name), "SPEC_V006_PIN")
        return {"name": name, "configured_name": original_name, "kind": kind, "alternative": alternative, "key": key,
                "point_key": point_key, "theta_sha256": check["theta_sha256"], "theta_check": check,
                "fill_check": fc, "fill_receipt": fill_pin, "spec": spec_pin, "spec_doc": spec,
                "handoff": cfg["handoff"], "v006_handoff_pin": hp, "v006_spec_pin": self.get_vpin("SPEC_PIN", name),
                "certificates": {"eps": cfg["eps"], "gq": cfg["gq"], "lo": self.pins["lo"]},
                "entry": entry, "entry_pin": ep, "origin": "KIT" if hits else "P112"}

    def call(self, name):
        hits = [c for c in self.calls() if c["name"] == name]
        need(len(hits) == 1, "CALL_NOT_IN_ACTUAL_SET", name)
        return hits[0]
