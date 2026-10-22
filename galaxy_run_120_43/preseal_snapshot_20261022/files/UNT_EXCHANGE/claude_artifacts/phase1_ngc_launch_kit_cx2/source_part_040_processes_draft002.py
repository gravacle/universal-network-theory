# Process qualification and the detached, validity-only sampler.


def parse_ps(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.strip().split(None, 3)
        need(len(parts) == 4 and all(x.isdigit() for x in parts[:3]), "PS_PARSE")
        pid, ppid, pgid = map(int, parts[:3])
        need(pid > 0 and ppid >= 0 and pgid >= 0 and parts[3], "PS_PARSE")
        rows.append({"pid": pid, "ppid": ppid, "pgid": pgid, "command": parts[3]})
    need(len({r["pid"] for r in rows}) == len(rows), "PS_DUPLICATE_PID")
    return rows


def command_argv(row):
    try:
        return shlex.split(row["command"])
    except ValueError:
        raise Refusal("PS_COMMAND_PARSE") from None


def has_arg(command, value):
    # ps command strings do not necessarily quote paths containing spaces.
    return re.search(r"(?<!\S)" + re.escape(value) + r"(?!\S)", command) is not None


def qualified_process(rows, pid, tool, outdir, role):
    if type(pid) is not int or pid <= 1:
        return None
    for row in rows:
        if row["pid"] != pid or not has_arg(row["command"], tool):
            continue
        if role == "monitor":
            matches = has_arg(row["command"], "--receipt " + outdir + ".receipt.json")
        elif role == "sampler":
            matches = has_arg(row["command"], "_sampler") and has_arg(row["command"], "--outdir " + outdir)
        elif role == "watch":
            matches = has_arg(row["command"], "--outdir " + outdir)
        elif role == "invocation":
            matches = has_arg(row["command"], "launch")
        else:
            raise Refusal("PROCESS_ROLE")
        if matches:
            return row
    return None


def matching_monitors(rows, monitor, outdir):
    return [r for r in rows if has_arg(r["command"], monitor) and
            has_arg(r["command"], "--receipt " + outdir + ".receipt.json")]


def descendants(rows, root):
    own = {root} if type(root) is int else set()
    changed = True
    while changed:
        before = len(own)
        own.update(r["pid"] for r in rows if r["ppid"] in own)
        changed = len(own) > before
    return own


class ProcessCounter:
    def __init__(self, declared=None):
        self.declared = DECLARED_TOOLS if declared is None else declared
        self.cache = {}
        self.by_real = {os.path.realpath(t["path"]): t for t in self.declared}
        self.by_sha = {t["sha256"]: t for t in self.declared}

    def identify(self, path):
        if not os.path.isabs(path):
            return None
        if os.path.realpath(path) in self.by_real:
            return self.by_real[os.path.realpath(path)]
        try:
            guard_read(path)
            # Do not inspect arbitrary data arguments. Listed tools are scripts.
            if not path.endswith((".py", ".sh")):
                return None
            st = os.stat(path)
            key = (path, st.st_mtime_ns, st.st_size)
            if key not in self.cache:
                self.cache[key] = sha(Path(path).read_bytes())
            return self.by_sha.get(self.cache[key])
        except (OSError, Refusal):
            return None

    def count(self, rows, own_root=None, excluded_pids=()):
        own = descendants(rows, own_root) | set(excluded_pids)
        found = []
        for row in rows:
            if row["pid"] in own:
                continue
            argv = command_argv(row)
            tool = None
            for index, arg in enumerate(argv):
                hit = self.identify(arg)
                if hit is None:
                    continue
                if hit["driver_only"] and (index + 1 >= len(argv) or argv[index + 1] not in ("run", "_stage")):
                    continue
                tool = hit
                break
            if tool is not None:
                found.append({"pid": row["pid"], "tool": tool["tool"]})
        return found


def monitor_command(pins, spec, outdir, caps):
    argv = [PY, "-I", "-B", pins["monitor"]["path"]]
    values = (("driver", pins["driver"]["path"]), ("driver-sha256", pins["driver"]["sha256"]),
              ("spec", spec["path"]), ("outdir", outdir), ("receipt", outdir + ".receipt.json"),
              ("wall-cap-s", str(caps["wall_cap_s"])), ("rss-cap-bytes", str(caps["rss_cap_bytes"])),
              ("output-cap-bytes", str(caps["output_cap_bytes"])))
    for flag, value in values:
        argv.extend(["--" + flag, value])
    return argv


def driver_command(pins, spec, outdir):
    return [PY, "-I", "-B", pins["driver"]["path"], "run", "--spec", spec["path"], "--outdir", outdir]


def check_monitor_command(argv, pins, spec, outdir, caps, name):
    need(argv == monitor_command(pins, spec, outdir, caps), "MONITOR_ARGV")
    for value in argv:
        if value.startswith("/"):
            path_rules(value, "monitor argv")
    need(caps["rss_cap_bytes"] == RAM * (11 if name == TWIN else 1), "RSS_CAP_NOT_CALL_CAP")
    for key, value in caps.items():
        need(type(value) is int and value > 0, "CAP_FORM", key)


def launch_checks(lj, plan, m15):
    pins = lj.get("pins", {}) if type(lj) is dict else {}
    try:
        epoch = timestamp(lj.get("utc"), whole=True)
    except (Refusal, AttributeError):
        epoch = None
    return {
        "schema": type(lj) is dict and lj.get("schema") == MONITOR_SCHEMA + "_LAUNCH",
        "command_is_planned": lj.get("command") == driver_command(plan["pins"], plan["spec"], plan["outdir"]),
        "driver_pin": pins.get("driver") == plan["pins"]["driver"],
        "spec_pin": pins.get("spec") == plan["spec"],
        "monitor_pin": pins.get("monitor") == plan["pins"]["monitor"],
        "caps": type(lj.get("caps")) is dict and all(lj["caps"].get(k) == v for k, v in plan["caps"].items()),
        "rss_cap_is_call_cap": (lj.get("caps") or {}).get("rss_cap_bytes") == RAM * (11 if plan["name"] == TWIN else 1),
        "retries_0": type(lj.get("retries_allowed")) is int and lj.get("retries_allowed") == 0,
        "child_pid": type(lj.get("child_pid")) is int and lj["child_pid"] > 1,
        "m15_record_precedes_launch": epoch is not None and epoch > int(m15["date_u_epoch_s"]),
    }


def try_launch_json(path):
    try:
        raw = Path(path).read_bytes()
        doc = strict_json(raw)
        need(type(doc) is dict, "LAUNCH_JSON_FORM")
        return raw, doc
    except (OSError, Refusal):
        return None, None


def wait_launch_json(path, system, bound=300, poll=0.2):
    first = system.monotonic()
    n = 0
    while True:
        n += 1
        raw, doc = try_launch_json(path)
        elapsed = system.monotonic() - first
        if doc is not None or elapsed >= bound:
            return raw, doc, {"polls": n, "bound_s": bound, "poll_s": poll, "waited_s": elapsed}
        system.sleep(poll)


def stop_qualified(system, pid, predicate, group=False):
    """Qualification is rechecked before each signal; unrelated PID reuse is never signalled."""
    def alive():
        return next((r for r in system.processes() if r["pid"] == pid and predicate(r)), None)
    row = alive()
    if row is None:
        return "NOT_KILLED_TARGET_REFUSED"
    need(not group or row["pgid"] == pid, "NOT_GROUP_LEADER")
    send = os.killpg if group else os.kill
    try:
        send(pid, signal.SIGTERM)
    except ProcessLookupError:
        return "ALREADY_ENDED"
    until = system.monotonic() + 15
    while system.monotonic() < until and alive() is not None:
        system.sleep(0.2)
    if alive() is not None:
        try:
            send(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        result = "KILLED_KILL"
    else:
        result = "KILLED_TERM"
    until = system.monotonic() + 15
    while system.monotonic() < until and alive() is not None:
        system.sleep(0.2)
    need(alive() is None, "PROCESS_STILL_ALIVE_AFTER_STOP")
    return result


def enforce_solo(ctx, requested_solo, rows=None):
    rows = ctx.system.processes() if rows is None else rows
    for rec in ctx.records():
        if not rec.get("solo_mode"):
            continue
        if qualified_process(rows, rec.get("monitor_pid"), rec["monitor"]["path"], rec["outdir"], "monitor"):
            raise Refusal("SOLO_RERUN_ACTIVE", rec["name"])
    if requested_solo:
        need(not ProcessCounter().count(rows), "OTHER_NGC_PROCESS_ALIVE")


def sampler(ctx, plan, work, poll_s=5):
    """Only monitor records are read. All outdir tests are existence checks."""
    need(type(poll_s) in (int, float) and 0 < poll_s <= 10, "SAMPLER_POLL")
    ctx.gate()
    name, k, outdir = plan["name"], plan["attempt"], plan["outdir"]
    need(plan["config"] == ctx.config_pin, "SAMPLER_CONFIG_BINDING")
    receipt, launch_path = outdir + ".receipt.json", outdir + ".receipt.json.launch.json"
    counter = ProcessCounter()
    first_utc = last_utc = None
    last_mono, max_gap, max_other, n = None, 0.0, 0, 0
    complete, nonzero = True, []
    own_root = None
    seen_monitor, started, ended = False, None, None
    receipt_seen_at, gone_mounted_s = None, 0.0
    last_mount_mono = None
    while True:
        tick, stamp = ctx.system.monotonic(), utc()
        ps_ok = True
        try:
            rows = ctx.system.processes()
            mons = matching_monitors(rows, ctx.pins["monitor"]["path"], outdir)
            need(len(mons) <= 1, "MULTIPLE_MONITORS")
            seen_monitor = seen_monitor or bool(mons)
            mounted = ctx.system.mounted(ctx.cfg["run_volume"])
            raw, lj = try_launch_json(launch_path) if mounted else (None, None)
            if lj is not None:
                own_root = lj.get("child_pid")
                started = lj.get("utc")
                seen_monitor = True
            elif mons:
                own_root = mons[0]["pid"]
            other = counter.count(rows, own_root, (os.getpid(),))
        except (Refusal, OSError):
            rows, mons, other = [], [], []
            mounted = ctx.system.mounted(ctx.cfg["run_volume"])
            ps_ok, complete = False, False
        n += 1
        first_utc = stamp if first_utc is None else first_utc
        last_utc = stamp
        if last_mono is not None:
            max_gap = max(max_gap, tick - last_mono)
        last_mono = tick
        max_other = max(max_other, len(other))
        if other:
            nonzero.append({"utc": stamp, "count": len(other), "processes": other})
        if n == 1:
            ctx.write(str(Path(work) / "sampler_first_sample.json"),
                      {"schema": "P112_SAMPLER_FIRST_CX2V001", "ok": ps_ok, "utc": stamp,
                       "monotonic": ctx.system.monotonic(), "sampler_pid": os.getpid(), "date_u": date_u()})
            if not ps_ok:
                return {"status": "FIRST_SAMPLE_FAILED_NO_SOLO_FILE"}
        if mounted and ps_ok:
            if os.path.isfile(receipt):
                if receipt_seen_at is None:
                    receipt_seen_at = tick
                if not mons and tick - receipt_seen_at >= 1:
                    rec = monitor_receipt(Path(receipt).read_bytes())
                    started, ended = rec["utc_start"], rec["utc_end"]
                    result = {
                        "schema": "STEP5_SOLO_SAMPLE_CX2V001", "name": name, "attempt": k, "outdir": outdir,
                        "declared_list_sha256": DECLARED_LIST_SHA, "poll_s": poll_s, "n_samples": n,
                        "first_utc": first_utc, "last_utc": last_utc, "monitor_start_utc": started,
                        "monitor_end_utc": ended, "largest_gap_s": max_gap, "complete": complete,
                        "max_other_ngc_processes": max_other, "nonzero_samples": nonzero,
                        "own_tree_root_pid": own_root, "writer": ctx.own_pin, "date_u": date_u()}
                    return ctx.write(outdir + ".solo.json", result)
            if not mons and seen_monitor and not os.path.lexists(launch_path):
                return {"status": "MONITOR_REFUSED_NO_SOLO_FILE"}
            if not mons and seen_monitor and not os.path.isfile(receipt):
                if last_mount_mono is not None:
                    gone_mounted_s += tick - last_mount_mono
                if gone_mounted_s >= 60:
                    return {"status": "MONITOR_ENDED_NO_RECEIPT_NO_SOLO_FILE"}
            else:
                gone_mounted_s = 0.0
            last_mount_mono = tick if not mons else None
            # Monitor can refuse before any sample observes it; the immutable
            # monitor_pid record plus an absent qualified process settles that.
            mp = Path(work) / "monitor_pid.json"
            if not seen_monitor and mp.exists():
                pid = strict_json(mp.read_bytes())["monitor_pid"]
                if qualified_process(rows, pid, ctx.pins["monitor"]["path"], outdir, "monitor") is None:
                    seen_monitor = True
            inv = Path(work) / "invocation.json"
            if not seen_monitor and not mp.exists():
                invocation = strict_json(inv.read_bytes()) if inv.exists() else plan
                ip, command = invocation.get("invocation_pid"), invocation.get("invocation_command")
                if ip is not None and command is not None and not any(
                        r["pid"] == ip and r["command"] == command for r in rows):
                    return {"status": "INVOCATION_ENDED_BEFORE_MONITOR_NO_SOLO_FILE"}
        else:
            last_mount_mono = None
        ctx.system.sleep(max(0.0, poll_s - (ctx.system.monotonic() - tick)))
