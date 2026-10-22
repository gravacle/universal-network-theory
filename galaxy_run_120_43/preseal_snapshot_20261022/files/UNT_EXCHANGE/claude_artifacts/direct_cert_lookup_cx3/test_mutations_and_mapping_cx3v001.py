"""Focused mutation and source-equivalence checks; saved synthetic metadata only."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
ART = HERE.parent
FIX = HERE / "DIRECT_LOOKUP_TESTS_CX3V001"
OUT = HERE / "MUTATION_MAPPING_TESTS_CX3V001.json"
READS = {}


def audit(event, args):
    if event.startswith(("subprocess.", "socket.")) or event in (
        "os.system", "os.fork", "os.posix_spawn", "os.rename", "os.remove", "os.rmdir"
    ):
        raise RuntimeError("TEST_FENCE: " + event)
    if event != "open" or not isinstance(args[0], (str, bytes)):
        return
    p = Path(os.fsdecode(args[0]))
    if any(x in str(p).lower() for x in (
        "ngc3198", "/runs/", "/runs_ext/", "/.codex/", "v007_postseal_records"
    )):
        raise RuntimeError("PROTECTED_PATH: " + str(p))
    flags = args[2]
    if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC):
        if p != OUT or p.exists() or not flags & os.O_EXCL:
            raise RuntimeError("EXCLUSIVE_REPORT_ONLY")
    elif p.is_relative_to(ART):
        if not p.is_relative_to(FIX) and p.suffix != ".py":
            raise RuntimeError("SYNTHETIC_OR_SOURCE_ONLY: " + str(p))
        READS[str(p)] = True


sys.addaudithook(audit)


def pin(p):
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def module(raw, path, name):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    sys.modules[name] = m
    exec(compile(raw, str(path), "exec"), m.__dict__)
    return m


lp = HERE / "direct_cert_lookup_cx3v001.py"
ap = HERE / "direct_preflight_cert_cx3v001.py"
lookup_source = lp.read_text()
adapter_source = ap.read_text()
request_pin = pin(FIX / "REQUEST.json")
request = json.loads((FIX / "REQUEST.json").read_bytes())
manifest_pin = pin(FIX / "PUBLISHED/MANIFEST.json")
custody = json.loads((FIX / "BUNDLE_0.json").read_bytes())["custody"]
cases = []


def check(name, passed, detail=None):
    cases.append({"name": name, "passed": bool(passed), "detail": detail})


def lookup(text, name):
    m = module(text, lp, name)
    m.C1, m.GENESIS = request["c1"], request["genesis_registry"]
    return m


def snapshot(m):
    class SyntheticSnapshot(m.Snapshot):
        def module(self, ref, name):
            obj = super().module(ref, name)
            if ref == m.ASSEMBLER:
                obj.A.real_custody_fn = lambda ref: lambda spec: custody
            return obj
    return SyntheticSnapshot()


def changed(source, before, after):
    assert source.count(before) == 1, before
    result = source.replace(before, after)
    ast.parse(result)
    return result


def refuses(m, fn):
    try:
        fn()
    except m.Refusal:
        return True
    return False


baseline = lookup(lookup_source, "lookup_baseline")
for name, before, after, filename in [
    ("frozen_C1_gate", "req['c1'] == C1 and req['genesis_registry'] == GENESIS",
     "True", "M01_REQUEST.json"),
    ("genesis_eps_digest_gate",
     "records.get('eps_source_pins_digest') == gen['eps_source_pins_digest']",
     "True", "M08_REQUEST.json"),
    ("verification_boolean_gate", "verification.get('ok') is True and",
     "True and", "M14_REQUEST.json"),
]:
    mutant_source = changed(lookup_source, before, after)
    m = lookup(mutant_source, "mutant_" + name)
    rp = pin(FIX / filename)
    base_reject = refuses(baseline, lambda: baseline.validate(snapshot(baseline), rp))
    mutant_reject = refuses(m, lambda: m.validate(snapshot(m), rp))
    check("mutation_" + name, base_reject and not mutant_reject,
          {"baseline_refuses": base_reject, "mutant_refuses": mutant_reject,
           "mutant_source_sha256": hashlib.sha256(mutant_source.encode()).hexdigest()})


def replay_control(m):
    s = snapshot(m)
    result = m.validate(s, request_pin)
    result["verification"]["points"][0]["wrapper_replica"]["block"]["block_sha256"] = "0" * 64
    return refuses(m, lambda: m.replay(s, result))


mutant_source = changed(lookup_source,
    "actual == expected and rep.get('ok') is True",
    "rep.get('ok') is True")
m = lookup(mutant_source, "mutant_replay")
check("mutation_full_verifier_replay_equality",
      replay_control(baseline) and not replay_control(m),
      {"mutant_source_sha256": hashlib.sha256(mutant_source.encode()).hexdigest()})


class ReachedPublication(Exception):
    pass


def publication_control(m):
    s = snapshot(m)
    result = m.validate(s, request_pin)
    old_mkdir = os.mkdir
    def stopped(*args, **kwargs):
        raise ReachedPublication()
    os.mkdir = stopped
    try:
        m.publish(s, result, str(HERE / "NEVER_CREATED_MUTATION_OUTPUT"))
    except m.Refusal:
        return "REFUSED"
    except ReachedPublication:
        return "REACHED_WRITE_WITHOUT_REPLAY"
    finally:
        os.mkdir = old_mkdir
    raise AssertionError("unexpected publication return")


mutant_source = changed(lookup_source,
    "result.get('_replayed_binding') == replay_binding(result)", "True")
m = lookup(mutant_source, "mutant_publication")
check("mutation_publication_requires_replay",
      publication_control(baseline) == "REFUSED" and
      publication_control(m) == "REACHED_WRITE_WITHOUT_REPLAY",
      {"mutant_source_sha256": hashlib.sha256(mutant_source.encode()).hexdigest(),
       "no_output_directory_created": not (HERE / "NEVER_CREATED_MUTATION_OUTPUT").exists()})

prepared = baseline.validate(snapshot(baseline), request_pin)
p = prepared["points"][0]
pending = json.loads(Path(p["pending_spec"]["path"]).read_bytes())
mutant_source = changed(lookup_source,
    "for field in SLOTS:\n        exact_pin(rec[field])",
    "for field in SLOTS[:1]:\n        exact_pin(rec[field])")
m = lookup(mutant_source, "mutant_lo_slot")
check("mutation_both_mapper_slots_required",
      baseline.fill(pending, p["record"]) == p["raw"] and
      m.fill(pending, p["record"]) != p["raw"],
      {"mutant_source_sha256": hashlib.sha256(mutant_source.encode()).hexdigest()})

# Only the bridge lookup/config binding is exercised here. Native certificate,
# sensitivity and normalizer behavior has its separate 71-case replay evidence.
cfg = {"tail_readiness": json.loads(Path(request["c1"]["path"]).read_bytes())["tail_readiness"]}
admission = {"direct_certificate_lookup": {"request": request_pin, "manifest": manifest_pin}}
class InertBase:
    pass


def bridge_build(source, config):
    a = module(source, ap, "bridge_" + hashlib.sha256(source.encode()).hexdigest()[:12])
    def base_build(C, config, **kwargs):
        b = InertBase()
        b.cfg = config
        return b
    def load(ref, admission, name):
        if ref == a.LOOKUP:
            assert ref == pin(lp)
            return baseline
        assert ref == a.BASE_ADAPTER
        return types.SimpleNamespace(build=base_build)
    sg = types.SimpleNamespace(require=baseline.need, load=load)
    c = types.SimpleNamespace(O=None, M=None, G=None, Error=ValueError,
        DRIVER_SHA=baseline.DRIVER_SHA, validate_block=lambda x: None,
        point_identity=baseline.point_identity)
    return a.build(c, config, guard=sg, admission=admission)


wrong = json.loads(p["raw"])
wrong["label"] += " changed"
mutant_source = changed(adapter_source, "L.json_bytes(spec)==p['raw']", "True")
base_bridge = bridge_build(adapter_source, cfg)
mutant_bridge = bridge_build(mutant_source, cfg)
check("mutation_bridge_exact_final_bytes",
      refuses(baseline, lambda: base_bridge._direct_certificate_record(p["record"]["identity"], wrong))
      and mutant_bridge._direct_certificate_record(p["record"]["identity"], wrong) == p["record"],
      {"mutant_source_sha256": hashlib.sha256(mutant_source.encode()).hexdigest()})
bad_cfg = copy.deepcopy(cfg)
bad_cfg["tail_readiness"]["approved_certificate_producers"].reverse()
mutant_source = changed(adapter_source,
    "config.get('tail_readiness',{}).get(field)==frozen[field]", "True")
base_refuses = refuses(baseline, lambda: bridge_build(adapter_source, bad_cfg))
mutant_refuses = refuses(baseline, lambda: bridge_build(mutant_source, bad_cfg))
check("mutation_bridge_frozen_C1_config", base_refuses and not mutant_refuses,
      {"mutant_source_sha256": hashlib.sha256(mutant_source.encode()).hexdigest()})

# Reproduce the preserved four source AST comparisons using current bytes.
comparisons = [
    ("Mapper", ART / "calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py",
     ART / "h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_core_cx2v006r12_c4.py"),
    ("point_identity", ART / "calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py",
     ART / "h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_core_cx2v006r12_c4.py"),
    ("Mapper", ART / "h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py",
     ART / "h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py"),
    ("points_manifest", ART / "h3_campaign_path_c2/h3_campaign_entry_c2v004.py",
     ART / "h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py"),
]
for name, before, after in comparisons:
    def selected(p):
        matches = [n for n in ast.parse(p.read_bytes()).body
                   if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == name]
        assert len(matches) == 1
        return ast.dump(matches[0], include_attributes=False)
    b, a = selected(before), selected(after)
    check("r12_AST_" + name + "_" + before.name, b == a,
          {"source": pin(before), "r12_template": pin(after),
           "AST_sha256": hashlib.sha256(b.encode()).hexdigest()})

all_inputs = [pin(Path(p)) for p in sorted(READS)]
result = {
    "schema": "DIRECT_MUTATION_MAPPING_CX3V001", "status": "TESTED",
    "n": len(cases), "passed": sum(x["passed"] for x in cases),
    "mutants_killed": sum(x["passed"] for x in cases if x["name"].startswith("mutation_")),
    "mutants_total": 8, "cases": cases, "inputs_sha256_from_bytes": all_inputs,
    "scope": "Eight in-memory source mutants; three saved synthetic points; four source AST comparisons.",
    "UNTESTED": ["production W3 inputs and outputs", "real custody or numerical searches",
                 "production Context construction", "scientific launches"],
}
raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
with OUT.open("xb") as f:
    f.write(raw)
print(json.dumps({"report": {"path": str(OUT), "sha256": hashlib.sha256(raw).hexdigest()},
                  "passed": result["passed"], "n": len(cases), "mutants_killed": result["mutants_killed"]}))
raise SystemExit(0 if result["passed"] == len(cases) else 1)
