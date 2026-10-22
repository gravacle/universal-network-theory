"""A ps command may contain bytes that are not UTF-8 text."""


def ps_byte_probe(suite):
    from pathlib import Path
    M = suite.module
    f = receipt_fixture(suite, "PS_invalid_UTF8")
    original = M.subprocess.run
    source = "import sys; sys.stdout.buffer.write(b'777001 1 777001 /synthetic/unlisted \xff\\n')"
    # Keep the child argv ASCII while its captured stdout contains byte FF.
    source = source.replace("\xff", r"\xff")
    def supplied_ps(argv, *args, **kwargs):
        if argv[:2] == ["/bin/ps", "-axww"]:
            return original([M.PY, "-I", "-B", "-c", source], *args, **kwargs)
        return original(argv, *args, **kwargs)
    M.subprocess.run = supplied_ps
    try:
        rows = M.System().processes()
        suite.eq(len(rows), 1)
        suite.eq(rows[0]["command"].endswith("\udcff"), True)
        suite.eq(M.ProcessCounter(synthetic=True).count(rows), [])
        clock = [0.0]
        f.ctx.system.processes = M.System().processes
        f.ctx.system.monotonic = lambda: clock[0]
        f.ctx.system.sleep = lambda seconds: clock.__setitem__(0, clock[0] + seconds)
        work = f.root / "launch_root" / "work" / "invalid_byte"
        work.mkdir()
        plan = {"name": f.name, "attempt": 1, "outdir": f.outdir, "config": f.ctx.config_pin}
        pin = M.sampler(f.ctx, plan, str(work), poll_s=1)
        suite.eq(M.read_pin(pin)["complete"], True)
    finally:
        M.subprocess.run = original


def ps_byte_cases(suite):
    import types
    suite.case("B4_non_UTF8_ps_command_does_not_fail_sample", lambda: ps_byte_probe(suite))
    def mutant():
        def child(label, module):
            obj = object.__new__(type(suite))
            obj.__dict__ = dict(suite.__dict__)
            obj.root = suite.root / ("ps_bytes_" + label)
            obj.root.mkdir()
            obj.module, obj.rows, obj.interfaces = module, [], {}
            return obj
        ps_byte_probe(child("control", suite.module))
        source = suite.tool_path.read_text()
        old, new = 'errors="surrogateescape"', 'errors="strict"'
        suite.eq(source.count(old), 1)
        source = source.replace(old, new)
        module = types.ModuleType("_p112_ps_bytes_mutant")
        module.__file__ = str(suite.tool_path)
        exec(compile(source, str(suite.tool_path), "exec"), module.__dict__)
        failure = None
        try:
            ps_byte_probe(child("mutant", module))
        except Exception as error:
            failure = type(error).__name__
        suite.eq(failure, "UnicodeDecodeError")
        suite.interfaces["ps_bytes_restoring_mutant"] = {
            "control": "PASS", "status": "KILLED", "source_sha256": suite.module.sha(source.encode()),
            "replace": old, "with": new, "detection": failure, "imported": True}
    suite.case("CX2V002_MUTANT_strict_ps_decoding", mutant)
