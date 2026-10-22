from pathlib import Path
import hashlib
import json
import subprocess

E = Path("/Users/bgm/Research/UNT_EXCHANGE")
W = E / "claude_artifacts/review_wall_ceiling_cx3"
S = E / "claude_artifacts/h11_wall_ceiling_c3"


def pin(p):
    p = Path(p)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def write_new(p, body):
    with p.open("x", encoding="utf-8") as f:
        f.write(body)
    return pin(p)


now = subprocess.check_output(["/bin/date", "-u"], text=True).strip()
ir = W / "INDEPENDENT_CX3V002/TEST_RECORD.json"
cr = W / "C_AUTHOR_RERUN_CX3V001/TEST_RECORD.json"
dr = W / "D_AUTHOR_RERUN_CX3V001/TEST_RECORD.json"
i, c, d = [json.loads(p.read_bytes()) for p in (ir, cr, dr)]
assert i["passed"] == 27 and i["failed"] == 0 and i["source_bytes_unchanged"]
assert c["passed"] == c["n"] == 18 and all(c["mutants"].values())
assert d["passed"] == d["n"] == 8 and not d["builder_failures"]
assert all(v["killed"] for v in d["mutants"].values())
for value in i["sources"].values():
    assert pin(value["path"]) == value, value["path"]
sources = dict(i["sources"])
for label, path in {
    "independent_check": W / "check_walls_cx3v003.py",
    "independent_results": ir,
    "C_author_rerun": cr,
    "D_author_rerun": dr,
    "C_author_test": S / "test_build_c2v004c_c3v001.py",
    "D_author_test": S / "test_build_c2v004d_c3v001.py",
    "C_leaf_diff": S / "C2V004C_FILL_20261022T093000Z/LEAF_DIFF_S45_C2V004C.json",
    "D_leaf_diff": S / "C2V004D_FILL_20261022T093000Z/LEAF_DIFF_S45_C2V004D.json",
    "D_readme": S / "README_C2V004D_C3V001.md",
    "review_dispatch": E / "FROM_CODEX/0839_2026-10-21_codex2_narrow_review_DBP_C2V004C_due_Thu0300.md",
    "handoff": E / "FROM_CODEX/0846_2026-10-21_codex3_takes_0839_review_plus_C2V004D_then_0828_units_from_codex2.md",
    "scope_trim": E / "FROM_CODEX/0849_2026-10-21_codex3_codex1_scope_trim_unit3_and_cxv003_moved_to_codex2.md",
    "packaging_script": Path(__file__),
}.items():
    sources[label] = pin(path)

result = {
    "schema": "WALL_CEILING_NARROW_REVIEW_CX3V001",
    "date_u": now,
    "reviewer": "Codex3",
    "scope": "0839/0846, A115 honest producer/operator data-only wall review",
    "C2V004C": {
        "verdict": "PASS",
        "TESTED": [
            "W = floor(2026-12-01T05:59:00Z - 2026-10-22T09:30:00Z) = 3443340 seconds.",
            "Exactly eleven HEADLINE wall leaves plus five provenance leaves change against B.",
            "Builder reads pinned B domain bytes only; two exclusive outputs; existing output directory refuses.",
            "Rebuild reproduces C and its leaf-diff bytes exactly.",
            "All other batches, RSS/output caps, route_a_admission and case_order remain unchanged.",
            "Eleven-call checker passes and refuses wrong wall/RSS/output caps on both plan and admission, wrong order and wrong DBP SHA.",
            "Amendment assigns DBP_C and its SHA before PRELAUNCH, copies caps to both final plan and admission candidate, and checks bound outputs. Three shell blocks pass bash -n.",
        ],
        "author_rerun": {"checks_passed": 18, "checks_total": 18, "mutants_killed": 4, "mutants_total": 4},
    },
    "C2V004D": {
        "verdict": "PASS",
        "TESTED": [
            "Exactly two POST_S1 wall leaves plus five provenance leaves change against C; HEADLINE remains byte-equivalent as data.",
            "Against B, exactly thirteen wall leaves plus six provenance leaves change.",
            "Builder reads pinned B and C domain bytes only; two exclusive outputs; rebuild reproduces D and its leaf-diff bytes exactly.",
            "Other batches, RSS/output caps, route_a_admission and case_order remain unchanged.",
            "Author checker controls cover pair plan, parent admission, both child admissions and both child plans, including incorrect old caps, pin and parent binding refusals.",
            "Later D fills alter only POST_S1 walls, preserving the C HEADLINE walls.",
        ],
        "author_rerun": {
            "groups_passed": 8, "groups_total": 8, "builder_checks": 18,
            "cli_checks": 4, "checker_cases": 12, "mutants_killed": 11, "mutants_total": 11,
        },
    },
    "independent_checks": {"passed": 27, "total": 27},
    "FORMAL": [
        "guard014 compares positive integer caps with root cfg; no fixed HEADLINE wall.",
        "binder retains plan bytes and admission caps while binding the plan pin.",
        "AST-extracted launcher monitor_argv preserves W (TESTED without execution); monitor source accepts positive float wall and compares elapsed time to it.",
        "H1/apply-fields, FINAL producer, PRELAUNCH and binder sources contain no wall field; actual future H1/FINAL artifacts were not read.",
        "S1 pair guard binds caps in the parent cfg, both child admissions and both child plan calls.",
        "The prebuilt wall duration is measured from the stated earliest fill, not each actual process start; a later process start shifts its relative deadline later. This is consistent with the reviewed ceiling policy; no runtime timing claim is made.",
    ],
    "nonblocking_documentation_notes": [
        "The original command sheet retains old A248 wall-policy wording at lines 8, 136 and 155. The explicit later DBP_C copy/check amendment governs the data; update these descriptions in a successor sheet.",
        "The S1 checker/README says five records but enumerates and checks six: pair plan, parent admission, two child admissions and two child plans.",
    ],
    "test_history": [
        "The first executed independent harness blocked a lazy standard-library import, causing two harness failures. A new successor permits standard-library reads under sys.base_prefix while retaining domain-input and write fences. The reported 27/27 result is the successor rerun; the earlier record remains preserved.",
        "No reviewed source was edited. Source bytes were rehashed and confirmed unchanged before publication.",
    ],
    "UNTESTED": [
        "Root actual future H1/FINAL/plan/admission fills.",
        "Real monitor runtime or any scientific launch.",
        "Production C2V004C/C2V004D consumption or scientific outcomes.",
    ],
    "sources_sha256_from_bytes": sources,
}
rp = write_new(W / "WALL_CEILING_REVIEW_CX3V001.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
for n, letter, counts in [(698, "C", "18/18 author checks and 4/4 mutant controls"), (699, "D", "8/8 author groups (18 builder checks, 4 CLI checks, 12 checker cases) and 11/11 mutant controls")]:
    obj = sources[letter]
    body = f"""# {n:04d} — DBP C2V004{letter} narrow review PASS

From: Codex3. To: Claude2.
`date -u`: {now}

PASS in the requested A115 honest producer/operator scope. TESTED: combined independent review 27/27; C2V004{letter} rerun {counts}. W is 3,443,340 seconds. No scientific launch was performed.

Reviewed DBP: `{obj['path']}`
SHA256 from bytes: `{obj['sha256']}`.

Review result, evidence, full source pins and FORMAL/UNTESTED boundaries: `{rp['path']}`
SHA256 from bytes: `{rp['sha256']}`.

Nonblocking documentation corrections: stale A248 wall-policy wording remains in the original command sheet despite the explicit governing C amendment; the D checker description counts five records while checking six. Details and source-byte pins are in the review.

UNTESTED: actual root fills, production execution and long-running monitor behavior. This review is not a launch or adoption decision. Inbox polling continues every 60 seconds. Next Codex3 work is direct certificate lookup unit 2 only, per the scope trim pinned in the review.
"""
    p = write_new(E / f"FROM_CODEX3/{n:04d}_2026-10-21_0846_DBP_C2V004{letter}_review_PASS.md", body)
    print(json.dumps(p))
print(json.dumps(rp))
