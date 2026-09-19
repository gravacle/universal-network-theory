#!/usr/bin/env python3
"""Assemble PROOF_V002.md from the verified layer claim tables. The document is BUILT, not typed:
   statuses and carrier marks come from the ledger and the T-9 audit every time, so a stale mark is
   impossible to introduce by hand. Section prose that is the registrar's own lives in the .md
   fragments beside this script."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_blocks import ledger, marks, plan, render

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PROOF_V002.md")

# section title -> (layer json, [claim ids to place here] or None for "all not placed elsewhere")
SECTIONS = [
    ("1. THE DEFINITION LAYER — what a record is", "DEFINITION", None),
    ("2. THE LAWS LAYER — what a record does in time", "LAWS", None),
    ("3. THE FORMATION LAYER — how a record comes to be", "FORMATION", None),
    ("3A. THE ARROW LAYER — what the environment learns about the record", "ARROW", None),
    ("4. THE CORNER LAYER — DEF-A, the exact idealisation", "CORNER", None),
    ("5. THE GEOMETRY LAYER — the emergence increments", "GEOMETRY", "EXCEPT:P-GEO-12"),
    ("6. COMPARISON — the one place Newton is named", "GEOMETRY", "ONLY:P-GEO-12"),
    ("7. THE THREE ROLES AS ONE STATEMENT", "ROLES_AND_DEBTS", "ONLY:P-ROLES-1,P-ROLES-2,P-ROLES-3,P-ROLES-4,P-ROLES-5"),
    ("8. STANDING DEBTS — what is not established", "ROLES_AND_DEBTS", "EXCEPT:P-ROLES-1,P-ROLES-2,P-ROLES-3,P-ROLES-4,P-ROLES-5"),
    ("9. CURRENT CONDITIONAL CLOSURES AND FINITE RELATIONAL EVIDENCE", "CURRENT_RECONCILIATION", None),
    ("10. THE LIMITS — what this program is and is not (T-17)", "LIMITS", None),
]

def frag(name):
    p = os.path.join(S, name)
    return open(p).read().rstrip() + "\n" if os.path.exists(p) else ""

def main():
    st, mk, pl = ledger(), marks(), plan()
    reconciliation = json.load(open(os.path.join(S, "CURRENT_RECONCILIATION.json")))
    overrides = reconciliation.get("overrides", {})
    parts = [frag("frontmatter.md")]
    for title, layer, sel in SECTIONS:
        data = json.load(open(os.path.join(S, layer + ".json")))
        claims = [{**claim, **overrides.get(claim["id"], {})}
                  for claim in data["claims"]]
        if sel and sel.startswith("ONLY:"):
            want = set(sel[5:].split(","));  claims = [c for c in claims if c["id"] in want]
        elif sel and sel.startswith("EXCEPT:"):
            drop = set(sel[7:].split(","));  claims = [c for c in claims if c["id"] not in drop]
        elif sel and sel.startswith("PREFIX:"):
            p = sel[7:];  claims = [c for c in claims if c["id"].split("-")[1] == p]
        if not claims:
            continue
        parts.append("\n---\n\n## " + title + "\n")
        intro_file = "intro_%s.md" % title.split(".")[0]
        extra = frag(intro_file)
        if extra:
            parts.append(extra + "\n")
        elif data.get("section_intro") and sel is None:
            parts.append(data["section_intro"].strip() + "\n\n")
        elif data.get("section_intro") and sel and sel.startswith("EXCEPT:"):
            parts.append(data["section_intro"].strip() + "\n\n")
        for c in claims:
            parts.append(render(c, st, mk, pl))
    doc = "\n".join(parts).rstrip() + "\n"
    # The counts are COMPUTED from the assembled document, never typed: a proof that prints its own
    # coverage cannot quietly lose it.
    blocks = doc.count("\n### P-")
    nogate = doc.count("| **gate** | none |")
    nomodel = doc.count("| **model** | none |")
    single = doc.count("| **scope** | SINGLE-CARRIER \u2014")
    proved = sum(1 for b in doc.split("\n### P-")[1:] if "PROVED," in b.split("| **scope**")[0])
    stats = ("Of the %d claims below, **%d carry no validator gate** and **%d have no model function "
             "behind them**. **%d rest on no `TWO-CARRIER` row** and open their scope cell saying so. "
             "**%d cite a `PROVED` row.**" % (blocks, nogate, nomodel, single, proved))
    doc = doc.replace("{{STATS}}", stats)
    open(OUT, "w").write(doc)
    print("wrote", OUT, "|", stats)

if __name__ == "__main__":
    main()
