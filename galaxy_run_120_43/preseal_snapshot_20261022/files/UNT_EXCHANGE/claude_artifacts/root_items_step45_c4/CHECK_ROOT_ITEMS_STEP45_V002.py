# Self-check of a staged ROOT_ITEMS_STEP45_V002 pair against V001. Reads only the two V001 files and the staged pair.
# Usage: python3 -I -B check_v002.py <stage_dir>
import json, re, sys, collections

STAGE = sys.argv[1]
V1 = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_items_step45_c4/ROOT_ITEMS_STEP45_V001"
def hook(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise SystemExit("DUPKEY " + k)
        d[k] = v
    return d
def load(p):
    return json.loads(open(p, encoding="utf-8").read(), object_pairs_hook=hook,
                      parse_constant=lambda c: (_ for _ in ()).throw(SystemExit("NONFINITE " + c)))
j1 = load(V1 + ".json"); md1 = open(V1 + ".md", encoding="utf-8").read()
j2 = load(STAGE + "/ROOT_ITEMS_STEP45_V002.json"); md2 = open(STAGE + "/ROOT_ITEMS_STEP45_V002.md", encoding="utf-8").read()
P = []; F = []
def ok(c, msg):
    (P if c else F).append(msg)

i1 = {i["id"]: i for i in j1["items"]}; i2 = {i["id"]: i for i in j2["items"]}
ok(set(i2) - set(i1) == {"S4-R-B4a", "S4-R-B7"}, "new ids are exactly S4-R-B4a, S4-R-B7: %s" % sorted(set(i2) - set(i1)))
ok(set(i1) - set(i2) == set(), "no V001 id dropped")
ok(all(i2[k]["title"] == i1[k]["title"] for k in i1 if k not in ("RI45-31", "S4-R-D8")), "titles unchanged except RI45-31, S4-R-D8")
# flags that must have changed
exp = {"RI45-14": ("BEFORE_FIRST_RESULT", "5"), "RI45-27": ("BEFORE_FIRST_RESULT", "5"), "RI45-28": ("BEFORE_FIRST_RESULT", "5"),
       "S4-R-B4a": ("BLOCKS_START", "4"), "S4-R-B7": ("LATER", "4")}
for k, (b, s) in exp.items():
    ok((i2[k]["blocks"], i2[k]["blocks_step"]) == (b, s), "%s flag %s (step %s)" % (k, b, s))
changed_flags = sorted(k for k in i1 if (i1[k]["blocks"], i1[k]["blocks_step"]) != (i2[k]["blocks"], i2[k]["blocks_step"]))
ok(changed_flags == ["RI45-14", "RI45-27", "RI45-28"], "only RI45-14/27/28 flags changed among V001 items: %s" % changed_flags)
# phases: V001 phase p -> V002 p+1 for p>=5, except RI45-14 (8 -> 8)
bad = []
for k in i1:
    p1 = i1[k]["launch_phase"]; p2 = i2[k]["launch_phase"]
    want = 8 if k == "RI45-14" else (p1 + 1 if p1 >= 5 else p1)
    if p2 != want: bad.append((k, p1, p2))
ok(not bad, "phase renumbering consistent: %s" % bad)
# by-reference table
r1 = {r["id"]: r for r in j1["step4_by_reference"]}; r2 = {r["id"]: r for r in j2["step4_by_reference"]}
ok(len(r2) == 37 and set(r1) == set(r2), "37 by-reference rows, same ids")
ch = sorted(k for k in r1 if r1[k]["blocks_here"] != r2[k]["blocks_here"])
ok(ch == ["R-A4", "R-A5", "R-C2", "R-D3", "R-D4"], "by-reference flags changed for exactly the five H3 items: %s" % ch)
ok(all(r2[k]["blocks_here"] == "BEFORE_FIRST_RESULT" for k in ch), "the five are BEFORE_FIRST_RESULT")
ok("S4-R-B4a" in r2["R-B4"]["note"] and "S4-R-B4b" in r2["R-B4"]["note"], "R-B4 row names the split")
# summary
S1 = j1["summary_blockers_in_launch_order"]; S2 = j2["summary_blockers_in_launch_order"]
c2 = collections.Counter(r["blocks"] for r in S2)
ok(len(S2) == 68 and c2["BLOCKS_START"] == 25 and c2["BEFORE_FIRST_RESULT"] == 43, "summary 68 rows, 25 BS, 43 BFR: %d %s" % (len(S2), dict(c2)))
ids2 = [r["id"] for r in S2]
for k in ("S4-R-B4a", "S4-R-B4b", "S4-R-R-A4" if False else "S4-R-A4", "S4-R-A5", "S4-R-C2", "S4-R-D3", "S4-R-D4"):
    ok(k in ids2, "summary has " + k)
ok("S4-R-B4" not in ids2, "no bare S4-R-B4 row")
ph = {r["id"]: r["phase"] for r in S2}
ok(all(ph[k] == 5 for k in ("S4-R-A4", "S4-R-A5", "S4-R-C2", "S4-R-D3", "S4-R-D4")), "H3 rows in phase 5")
ok(ph["RI45-14"] == 8 and ph["S4-R-B4a"] == 2, "RI45-14 in phase 8; S4-R-B4a in phase 2")
ok([r["phase"] for r in S2] == sorted(r["phase"] for r in S2), "summary sorted by phase")
ok([r["order"] for r in S2] == list(range(1, len(S2) + 1)), "summary order 1..n")
start4 = sorted(r["id"] for r in S2 if r["blocks"] == "BLOCKS_START" and r["blocks_step"] == "4")
ok(len(start4) == 12, "12 step-4 start rows: %s" % start4)
ok(sorted(j2["step4_start_items"]) == start4, "step4_start_items matches the summary")
# MD twin: every item heading, its Blocks line, and the section-9 table
for k, it in i2.items():
    h = "### %s. %s" % (k, it["title"])
    ok(h in md2, "MD heading " + k)
    ok(("**Blocks:** `%s` (step %s)." % (it["blocks"], it["blocks_step"])) in md2, "MD blocks line " + k)
n_rec = md2.count("- **Recommended ruling (RECOMMENDATION).**")
ok(n_rec == len(i2) == 55, "55 recommendation lines: %d" % n_rec)
sec9 = md2.split("## 9. Summary: every blocker, in launch order")[1].split("## 10.")[0]
rows = [l for l in sec9.splitlines() if re.match(r"^\| \d+ \|", l)]
ok(len(rows) == len(S2), "MD section 9 has %d rows (JSON %d)" % (len(rows), len(S2)))
for l, r in zip(rows, S2):
    cells = [c.strip() for c in l.strip("|").split("|")]
    if not (cells[0] == str(r["order"]) and cells[1] == r["must_close_by"] and cells[2] == r["id"] and cells[4] == "`%s` (step %s)" % (r["blocks"], r["blocks_step"])):
        F.append("section 9 row mismatch " + l[:80]); break
else:
    P.append("section 9 rows equal the JSON summary")
# fix content present
def has(k, *subs):
    t = json.dumps(i2[k], ensure_ascii=False)
    miss = [s for s in subs if s not in t]
    ok(not miss, "%s contains %s" % (k, miss if miss else "all phrases"))
has("RI45-01", "guarded plan and admission provenance", "post-state acceptance", "point-scoped certificate validity", "MUST_FAIL", "R-B5", "missing or refused")
has("S4-R-D8", "1.80 GiB", "cap 1", "17.1%", "depart from the record", "3.22 GiB", "no after-route-A RSS record")
has("RI45-14", "r006 fallback", "also blocks step 6")
has("RI45-20", "no text fallback", "JSONDecodeError is a typed refusal", "bounded parse_int", "parse_constant", "parse_float", "nesting depth", "A71", "A102", "PAR8-N6")
has("RI45-12", "4de87df9", "K32/T120L", "UNTESTED", "no automatic retry", "0.6", "45 GiB")
has("S4-R-A1", "0105", "producer v003", "PR-SF1", "escalate", "0 BLOCKING")
has("S4-R-D17", "Codex1 adds both checks", "A105.3", "80 GB")
has("S4-R-B4a", "native_preflight", "PRELAUNCH_REPLAY_MISMATCH", "any lane", "Codex1")
has("S4-R-B7", "UNT_STEP4_DIII_POLICY_CX1V001", "post_adoption_only", "cb42a5a3")
has("RI45-29", "line 598", "line 242", "re-render", "0120", "0125")
has("RI45-30", "CLOSED")
has("RI45-27", "0124", "0119", "b0fba984", "FB-3", "A112")
has("RI45-28", "classifier: none", "0120")
has("RI45-24", "section sha", "verbatim", "disposition")
has("RI45-31", "§2 rule set")
has("RI45-34", "A17_C3")
has("RI45-15", "slots successor")
has("RI45-10", "RI45-09", "RI45-20")
has("RI45-08", "LAUNCH_ORDER_CX3V002 step 1")
has("RI45-06", "UNTESTED", "NGC91_K32_MS96")
has("S4-R-D11", "from the step-2 launch onward")
# stale phrases gone
for s in ("Pending the final r3 and Codex1's delta", "running since 00:25Z", "text fallback only on JSONDecodeError",
          "does not exist yet (TESTED, ls at 01:33Z)", "2, unless that reading shows 3", "exactly what A98.1 asks for",
          "one V006 entry closes it", "BLOCKS_START` (step 6)"):
    ok(s not in md2 and s not in json.dumps(j2, ensure_ascii=False), "stale phrase gone: " + s)
# maps
g1 = {m["source_item"]: m for m in j2["groups"][0]["source_item_map"]}
ok(any(k.startswith("0074 blocker (3)") for k in g1), "group-1 map has 0074 blocker (3)")
ok(g1["H7_DRIVER_CONSUMER_SELECTION"]["status_there"].startswith("V002: OPEN_IF_SUCCESSOR_SELECTED"), "H7 shows both statuses")
ok("{ref:" not in md2 and "{ref:" not in json.dumps(j2), "no unresolved refs")
ok(j2["schema"] == "UNT_ROOT_ITEMS_STEP45_C4V002" and j2["launch_authorized"] is False, "schema and launch_authorized")
print("PASS %d" % len(P)); print("FAIL %d" % len(F))
for m in F: print("  FAIL:", m)
sys.exit(1 if F else 0)
