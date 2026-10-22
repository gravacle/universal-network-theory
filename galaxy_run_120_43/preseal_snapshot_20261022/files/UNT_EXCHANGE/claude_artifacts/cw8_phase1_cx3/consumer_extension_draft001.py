"""Read-only full-cw8 receipt custody, composed into the roster builder."""


def _cw8_receipt_workers(doc, entry, entry_pin, record, where):
    role = entry.get("worker_role")
    name = entry.get("name")
    if role is None:
        # Existing serial and identity-twin entries retain their original
        # custody. A new-role receipt cannot masquerade as an old entry.
        _receipt_need(doc.get("worker_role") is None and record.get("worker_role") is None,
                      "CW8_ROLE_CUSTODY", where)
        return 8 if name == TWIN else 1
    _receipt_need(isinstance(role, dict) and
                  set(role) == {"kind", "column_workers", "choice"} and
                  type(role.get("column_workers")) is int and role["column_workers"] in (1, 8),
                  "CW8_ROLE_FORM", where)
    workers = role["column_workers"]
    _receipt_need(role["kind"] == ("IDENTITY_TWIN" if name == TWIN else "FULL") and
                  (name != TWIN or workers == 8) and
                  doc.get("worker_role") == role and record.get("worker_role") == role,
                  "CW8_ROLE_CUSTODY", where)
    spec, _, _ = read_json_pin(entry["spec"], where + ".worker_spec")
    try:
        leaf = spec["numerics"]["route_a"]["column_workers"]
    except (KeyError, TypeError):
        raise Refused("CW8_SPEC_LEAF", where) from None
    _receipt_need(type(leaf) is int and leaf == workers, "CW8_SPEC_LEAF", where)
    if name != TWIN:
        _receipt_need(record.get("watch_pid") is None, "CW8_FULL_CALL_TWIN_WATCHER", where)
    if role["choice"] is None:
        _receipt_need(workers == 1 or name == TWIN, "CW8_FULL_CALL_UNAUTHORIZED", where)
        return workers
    _receipt_need(name != TWIN and entry.get("schema") == "UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001",
                  "CW8_CHOICE_SCOPE", where)
    choice, _, _ = read_json_pin(role["choice"], where + ".worker_choice")
    _receipt_need(isinstance(choice, dict) and
                  choice.get("schema") == "CW8_PHASE1_CHOICE_CX3V001",
                  "CW8_CHOICE_SCHEMA", where)
    module = _p112_verifier_module(choice.get("producer"))
    _receipt_need(hasattr(module, "cw8_check_attempt"), "CW8_LAUNCHER_VERSION", where)
    try:
        # Uses the same read-only single-buffer bridge as registry assembly.
        # Context rederives PLAN/F identity, root spec pins, the license and
        # immutable selection. Nothing from a new caller can set workers=8
        # without this independent reconstruction.
        ctx = _registry_context_factory(module, entry.get("config"))
        ctx.gate()
        call = ctx.call(name)
        saved_entry, saved_pin = module.registered_entry(ctx, call)
        module.need(saved_pin == entry_pin and saved_entry == entry, "CW8_ENTRY_RECONSTRUCTION")
        module.cw8_check_attempt(ctx, call, record, doc)
        module.need(module.cw8_role(call) == role, "CW8_ROLE_CUSTODY")
    except module.Refusal as exc:
        raise Refused(exc.code, str(exc.detail)) from None
    return workers
