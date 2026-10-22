"""A248 bound twin-watch evidence; unchanged literal transport-status vocabulary."""

def raw_status(rec, *, name, attempt, outdir, receipt, launch_pin, child_pid,
               mislaunch=None, stop=None):
    if mislaunch is not None:
        bound = (mislaunch.get("name") == name and mislaunch.get("attempt") == attempt and
                 mislaunch.get("outdir") == outdir and mislaunch.get("receipt") == receipt)
        lj = mislaunch.get("launch_json") or {}
        if lj.get("sha256") is not None:
            bound = bound and lj["sha256"] == launch_pin["sha256"]
        if lj.get("child_pid") is not None:
            bound = bound and lj["child_pid"] == child_pid
        need(bound, "MISLAUNCH_NOT_BOUND")
        return "MISLAUNCH", "INFRA"
    if name == TWIN and stop is not None:
        need(type(stop) is dict and stop.get('schema') == 'UNT_S0_TWIN_KILL_RECORD_C2V003A' and
             stop.get('reason') == 'ITERATION_0001_COMPLETED_AND_SIDECAR' and
             stop.get('outdir') == outdir and stop.get('launch_json') == launch_pin and
             type(stop.get('pgid')) is int and stop['pgid'] == child_pid and
             stop.get('result') in ('KILLED_TERM', 'KILLED_KILL') and
             isinstance(stop.get('date_u'), str) and bool(stop['date_u']), 'TWIN_STOP_NOT_BOUND')
        return 'TWIN_PLANNED_STOP', 'PLANNED_STOP'
    # A248: STOPPED_* by itself is never evidence of the designed twin stop.
    driver = rec.get("driver_status")
    need(driver is None or isinstance(driver, str), "DRIVER_STATUS_FORM")
    raw = str(rec.get("status")) + "|" + (driver if driver is not None else "NONE")
    if raw == "CHILD_FAILED|NONE":
        need(type(rec.get("exit_code")) is int, "EXIT_CODE_FORM")
        raw += "|SIGNAL" if rec["exit_code"] < 0 else "|EXIT"
    need(raw in STATUS_CLASSES, "RECEIPT_STATUS_UNMAPPED", raw)
    return raw, STATUS_CLASSES[raw]
