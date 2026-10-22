#!/bin/bash
# Claude3 (FROM_CODEX/0644): the SA-CX1-B2 and SA-CX1-N1 MUST_FAIL suites (first run inline in mustfail_20261018T221642Z/b2), saved and
# re-run against the SELECTED helper and runner. Everything it writes lies under a NEW folder seal_assembly_c3/mustfail_b2n1_<UTC>/.
# c3v003 corrects two HARNESS expectations of c3v002 (its run mustfail_b2n1_20261019T000753Z, a03506db, is superseded): B2-4 with a
# plain main (no sys.path insert) cannot even find the unpinned sibling under -I, so 'not imported' (the guard's refusal OR
# ModuleNotFoundError) is the requirement, as the 22:16Z run recorded (B2_RESULTS_RUNNER_C3V002.txt dc653945; B2-4t is the binding
# control); B2-6 counts importlib loader calls with a pattern that does not match the helper's own _exec_module alias of load_pinned.
# usage: mustfail_b2_n1_c3sa_c3v003.sh HELPER_PATH HELPER_SHA RUNNER_PATH RUNNER_SHA OLD_RUNNER_PATH OLD_RUNNER_SHA
set -uo pipefail; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3; PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
HP=$1; HS=$2; RP=$3; RS=$4; OP=$5; OS=$6
S() { shasum -a 256 "$1" | cut -d' ' -f1; }
[ "$(S $HP)" = "$HS" ] && [ "$(S $RP)" = "$RS" ] && [ "$(S $OP)" = "$OS" ] || { echo "input bytes differ"; exit 1; }
UTC=$(date -u +%Y%m%dT%H%M%SZ); B=$C3/mustfail_b2n1_$UTC; mkdir $B $B/pkg $B/EMPTY_PREFIX $B/pkg/sibpkg $B/pkg/nspkg || exit 1
printf "MARKER = 'PINNED_SOURCE'\n" > $B/pkg/synthetic_pinned.py
printf "MARKER = 'PINNED_SOURCE'\n" > $B/pkg/synthetic_sibling.py
printf "import synthetic_sibling\n\ndef main(argv):\n    print('main=PINNED_SOURCE sibling=%%s' %% synthetic_sibling.MARKER)\n    return 0\n" > $B/pkg/synthetic_main.py
printf "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))   # exactly as Claude4's seal tools do\nimport synthetic_sibling\n\ndef main(argv):\n    print('main=PINNED_SOURCE sibling=%%s' %% synthetic_sibling.MARKER)\n    return 0\n" > $B/pkg/synthetic_main_toollike.py
printf "MARKER = 'X'\n" > $B/pkg/synthetic_unpinned.py
printf "import synthetic_unpinned\n\ndef main(argv):\n    return 0\n" > $B/pkg/synthetic_main_unpinned.py
printf "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))   # exactly as Claude4's seal tools do\nimport synthetic_unpinned\n\ndef main(argv):\n    return 0\n" > $B/pkg/synthetic_main_unpinned_toollike.py
printf "MARKER = 'SIBPKG_LOADED'\n" > $B/pkg/sibpkg/__init__.py; printf "MARKER = 'NSPKG_MOD_LOADED'\n" > $B/pkg/nspkg/mod.py
printf "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))\nimport sibpkg\n\ndef main(argv):\n    print('IMPORTED', sibpkg.MARKER)\n    return 0\n" > $B/pkg/main_sibpkg.py
printf "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent))\nimport nspkg.mod\n\ndef main(argv):\n    print('IMPORTED', nspkg.mod.MARKER)\n    return 0\n" > $B/pkg/main_nspkg.py
$PY -I -B - "$B" <<'PYEOF' || exit 1
import sys, os, importlib._bootstrap_external as be, importlib.util
B = sys.argv[1]; os.mkdir(B + '/pkg/__pycache__')
for n in ('synthetic_pinned', 'synthetic_sibling'):
    src = '%s/pkg/%s.py' % (B, n); st = os.stat(src)
    data = be._code_to_timestamp_pyc(compile("MARKER = 'UNPINNED_BYTECODE'\n", src, 'exec'), int(st.st_mtime), st.st_size)
    with open(importlib.util.cache_from_source(src), 'xb') as f:
        f.write(bytes(data))
PYEOF
cd /; SP=$B/pkg/synthetic_pinned.py
r1=$($PY -I -B -c "
import importlib.util,sys
spec=importlib.util.spec_from_file_location('fence_like', sys.argv[1]); F=importlib.util.module_from_spec(spec); spec.loader.exec_module(F); print(F.MARKER)" $SP)
r2=$($PY -I -B -c "
import sys,types,hashlib
src=open(sys.argv[3],'rb').read(); assert hashlib.sha256(src).hexdigest()==sys.argv[4]
H=types.ModuleType('h'); H.__file__=sys.argv[3]; exec(compile(src,H.__file__,'exec'),H.__dict__)
print(H.load_pinned(sys.argv[1],sys.argv[2],'fence_like').MARKER)" $SP $(S $SP) $HP $HS)
r3=$($PY -I -B $RP --module "synthetic_sibling=$B/pkg/synthetic_sibling.py=$(S $B/pkg/synthetic_sibling.py)" --main "$B/pkg/synthetic_main.py=$(S $B/pkg/synthetic_main.py)" --call main -- 2>&1)
r3t=$($PY -I -B $RP --module "synthetic_sibling=$B/pkg/synthetic_sibling.py=$(S $B/pkg/synthetic_sibling.py)" --main "$B/pkg/synthetic_main_toollike.py=$(S $B/pkg/synthetic_main_toollike.py)" --call main -- 2>&1)
r4=$($PY -I -B $RP --main "$B/pkg/synthetic_main_unpinned.py=$(S $B/pkg/synthetic_main_unpinned.py)" --call main -- 2>&1 | tail -1 | cut -c1-150)
r4t=$($PY -I -B $RP --main "$B/pkg/synthetic_main_unpinned_toollike.py=$(S $B/pkg/synthetic_main_unpinned_toollike.py)" --call main -- 2>&1 | tail -1 | cut -c1-150)
r5=$($PY -I -B -X "pycache_prefix=$B/EMPTY_PREFIX" -c "
import importlib.util,sys
spec=importlib.util.spec_from_file_location('kmax_compare_like', sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.MARKER)" $SP)
r6=$(grep -v '^ *#' $HP | grep -cE "spec_from_file_location|module_from_spec|\.exec_module\(|import_module\(|importlib\.")
o1=$($PY -I -B $OP --main "$B/pkg/main_sibpkg.py=$(S $B/pkg/main_sibpkg.py)" --call main -- 2>&1 | tail -1 | cut -c1-120)
o2=$($PY -I -B $OP --main "$B/pkg/main_nspkg.py=$(S $B/pkg/main_nspkg.py)" --call main -- 2>&1 | tail -1 | cut -c1-120)
n1=$($PY -I -B $RP --main "$B/pkg/main_sibpkg.py=$(S $B/pkg/main_sibpkg.py)" --call main -- 2>&1 | tail -1 | cut -c1-150)
n2=$($PY -I -B $RP --main "$B/pkg/main_nspkg.py=$(S $B/pkg/main_nspkg.py)" --call main -- 2>&1 | tail -1 | cut -c1-150)
ok=1; chk() { case "$2" in *"$3"*) echo "$1 PASS  $2";; *) echo "$1 FAIL  $2 (required: $3)"; ok=0;; esac; }
{ echo "# B2 + N1 MUST_FAIL suites c3v003 (Claude3 0644), helper $(basename $HP) $HS, runner $(basename $RP) $RS; contrast old runner $(basename $OP) $OS"
  echo "B2-1 (reproduction) importlib exec_module, stale pyc planted, no prefix: $r1 (expected UNPINNED_BYTECODE)"
  chk B2-2 "helper load_pinned with a stale pyc planted: $r2" "PINNED_SOURCE"
  chk B2-3 "runner, pinned sibling with a stale pyc: $r3" "main=PINNED_SOURCE sibling=PINNED_SOURCE"
  chk B2-3t "runner, tool-like main (sys.path insert) + pinned sibling with a stale pyc: $r3t" "main=PINNED_SOURCE sibling=PINNED_SOURCE"
  case "$r4" in *UNPINNED_SIBLING_IMPORT_REFUSED*|*"No module named 'synthetic_unpinned'"*) echo "B2-4 PASS  runner, plain main, unpinned sibling: not imported ($r4)";; *) echo "B2-4 FAIL  $r4"; ok=0;; esac
  chk B2-4t "runner, tool-like main importing an unpinned sibling: $r4t" "UNPINNED_SIBLING_IMPORT_REFUSED"
  chk B2-5 "third-party importlib under -X pycache_prefix=<empty>: $r5" "PINNED_SOURCE"
  [ -z "$(ls -A $B/EMPTY_PREFIX)" ] && echo "B2-5p PASS  the empty prefix stayed empty" || { echo "B2-5p FAIL  the prefix gained a file"; ok=0; }
  [ "$r6" = 0 ] && echo "B2-6 PASS  importlib loader calls in the helper's code (comments excluded): 0" || { echo "B2-6 FAIL  importlib loader calls: $r6"; ok=0; }
  echo "N1-1 (reproduction) OLD runner, unpinned sibling regular package: $o1"
  echo "N1-2 (reproduction) OLD runner, unpinned sibling namespace package: $o2"
  chk N1-3 "runner, unpinned sibling regular package: $n1" "UNPINNED_SIBLING_IMPORT_REFUSED"
  chk N1-4 "runner, unpinned sibling namespace package: $n2" "UNPINNED_SIBLING_IMPORT_REFUSED"
  [ $ok = 1 ] && echo "ALL_OK True" || echo "ALL_OK False"
} > $B/B2_N1_RESULTS_C3SA.txt
cat $B/B2_N1_RESULTS_C3SA.txt; shasum -a 256 $B/B2_N1_RESULTS_C3SA.txt
