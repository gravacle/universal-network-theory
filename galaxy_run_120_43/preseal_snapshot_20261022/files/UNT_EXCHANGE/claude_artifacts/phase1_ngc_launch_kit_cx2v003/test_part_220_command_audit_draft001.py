"""One audit over every in-process public command exercised by the full suite."""


def install_command_audit(suite):
    import functools
    M = suite.module
    state = {"depth": 0, "seen": set(), "violations": []}
    audit = SuccessorAudit(suite)
    saved = {}
    names = ("cli", "launch", "launch_resume", "close_attempt", "assemble_registry",
             "stop_outside_set", "record_monitor_refused", "status", "sampler", "write_cutoff")
    for name in names:
        function = getattr(M, name)
        saved[name] = function
        def wrap(function=function, name=name):
            @functools.wraps(function)
            def checked(*args, **kwargs):
                outermost = state["depth"] == 0
                if outermost:
                    audit.reads = []
                    audit.active = True
                state["seen"].add(name)
                state["depth"] += 1
                try:
                    return function(*args, **kwargs)
                finally:
                    state["depth"] -= 1
                    if outermost:
                        audit.active = False
                        try:
                            audit.once()
                        except Exception as error:
                            state["violations"].append({"case": suite.current_case, "command": name,
                                                        "error": repr(error)})
                            raise
            return checked
        setattr(M, name, wrap())

    def finish():
        audit.active = False
        for name, function in saved.items():
            setattr(M, name, function)
        suite.case("ALL_PUBLIC_COMMANDS_IMMUTABLE_READ_ONCE_MUST_PASS",
                   lambda: suite.eq(state["violations"], []))
        suite.case("ALL_PUBLIC_COMMANDS_AUDIT_COVERAGE_MUST_PASS",
                   lambda: suite.eq(sorted(state["seen"]), sorted(names)))
        suite.interfaces["all_public_command_read_audit"] = {
            "status": "TESTED", "commands": sorted(state["seen"]),
            "violations": state["violations"],
            "scope": ("In-process opens whose stack contains the tested executable; spelled and resolved paths. "
                      "Immutable reads at most once per outer command. Successful volatile observations and "
                      "unlisted process-counter script identity probes are separately classified. "
                      "Own executable sha reads are excepted. Child process executable reopening is outside this hook.")}
    return finish
