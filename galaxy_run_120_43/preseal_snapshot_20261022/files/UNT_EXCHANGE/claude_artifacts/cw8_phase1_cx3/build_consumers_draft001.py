"""Exclusive consumer successors. Source-only composition, no tool execution."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ART = HERE.parent
PINS = {}


def read(path, expected=None):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert expected is None or digest == expected, (path, digest)
    PINS[str(path)] = digest
    return raw.decode()


def write(path, source):
    ast.parse(source)
    with path.open("x") as f:
        f.write(source)
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


read(Path(__file__).resolve())
launcher = HERE / "phase1_ngc_launch_cx3cw8_draft001.py"
read(launcher, "ca833882bcfd66d0cf79beb57d232c16a94f21f6a0fe36ea0ca990fcf2d37bcb")
parent = ART / "runbook_v002_c2v007_cx2/roster_builder_c2v007_a253_v001.py"
source = read(parent, "799fb2d002ba39885326f161e1efbe3ad35dd2b66d3c84f961ddce910e9cd15b")
extension = read(HERE / "consumer_extension_draft001.py")
changes = []


def replace(old, new):
    global source
    assert source.count(old) == 1, (old, source.count(old))
    source = source.replace(old, new)
    changes.append({"old": old, "new": new})


replace("BUILDER_NAME = 'roster_builder_c2v007'",
        "BUILDER_NAME = 'roster_builder_c2v007_cx3cw8v001'")
replace("P112_REVIEWED_SHA = '8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9'",
        "P112_REVIEWED_SHA = " + repr(PINS[str(launcher)]) + "\n"
        "P112_REVIEWED_SHAS = frozenset((P112_REVIEWED_SHA,\n"
        "    '8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9'))")
replace("if norm['sha256'] != P112_REVIEWED_SHA:",
        "if norm['sha256'] not in P112_REVIEWED_SHAS:")
replace("evidence.update({'call_name': name, 'solo_mode': doc['solo_mode']})",
        "evidence.update({'call_name': name, 'solo_mode': doc['solo_mode'],\n"
        "                     'column_workers': _cw8_receipt_workers(doc, entry, entry_pin, record, where)})")
replace("(11 if b.get('call_name') == TWIN else 1)",
        "(11 if b.get('call_name') == TWIN or b.get('column_workers') == 8 else 1)")
replace("'RSS equals RAM, twin eleven RAM'",
        "'RSS equals RAM; identity twin and authorized full cw8 use eleven RAM'")
replace("'equals host RAM (eleven RAM for the twin). Wall caps are not doubled: '",
        "'equals host RAM (eleven RAM for the twin or licensed full cw8). Wall caps are not doubled: '")
replace("if __name__ == '__main__':\n    sys.exit(main(sys.argv[1:]))",
        extension + "\n\nif __name__ == '__main__':\n    sys.exit(main(sys.argv[1:]))")
builder = write(HERE / "roster_builder_c2v007_cx3cw8_draft001.py", source)
g26parent = ART / "g26_freeze_script_cx2/g26_freeze_cx2v001.py"
source = read(g26parent, "663d4c2b19a90490c4b1ad9f0902d485146dccdcef4f84f595520dff92b96bea")
replace("BUILDER_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2v007_cx2/roster_builder_c2v007_a253_v001.py'",
        "BUILDER_PATH = " + repr(builder["path"]))
replace("BUILDER_SHA256 = '799fb2d002ba39885326f161e1efbe3ad35dd2b66d3c84f961ddce910e9cd15b'",
        "BUILDER_SHA256 = " + repr(builder["sha256"]))
g26 = write(HERE / "g26_freeze_cx3cw8_draft001.py", source)
record = {"date_u": subprocess.check_output(["/bin/date", "-u"], text=True).strip(),
          "inputs": PINS, "outputs": [builder, g26], "changes": changes}
with (HERE / "CONSUMER_BUILD_DRAFT001.json").open("x") as f:
    json.dump(record, f, indent=2, sort_keys=True)
    f.write("\n")
print(json.dumps(record["outputs"], sort_keys=True))
