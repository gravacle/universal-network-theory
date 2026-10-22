"""Generate fill_c1_pin_c2v003_c3v001.py from the pinned fill_c1_pin_c2v002.py (3faf4a6c) by exact, counted string
replacements: constants and their labels only. Claude3, root deputy (A292; root 0857 item 2). Exclusive create.
usage: python3 -I -B make_fill_v003_c3v001.py OUT_PATH"""
import hashlib, os, sys
SRC = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/fill_c1_pin_c2v002.py'
SRC_SHA = '3faf4a6c423ecc14f330329e9495c4d79786b8bcfe66a2ae339dbf88440305ec'
NEW_DIGEST = '3c03bae3473954fdeb842de508c64702602c981675f839d604c7156b8c5db030'
REPL = [
 ('"""Fill C1 (H1) from draft C2V002: set', '"""Fill the C1 (H1) successor from draft C2V003: set'),
 ("read-only otherwise. The written C1 becomes the frozen C1 when root records it in V006 after the c3v005 verify of record\n"
  "passes (A209 item 4; A134 Q9(b)3). Never edit it.\n",
  "read-only otherwise. The written C1 becomes the frozen C1 when root records it in V006 (A298; root states any verify of\n"
  "record there). Never edit it.\n\n"
  "v003_c3v001 = v002 (3faf4a6c) with constants and their labels only (A298; Claude3 as root deputy, root 0857 item 2):\n"
  "DRAFT_SCHEMA, C1_SCHEMA, SYNTHETIC_SCHEMA, TR_DIGEST_EXCLUDING_REVIEW (3c03bae3: the six producers plus the A296 EPS\n"
  "bridge 1eb94a51 as entry 7), GUARD_PIN (the A296 b1 guard 3939bc47 that the A296 wrapper loads), the C1 status text,\n"
  "one refusal code, one label and the synthetic fixture text. Every check and code path is v002's.\n"),
 ('claude_artifacts, and writes schema UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002, never the C1 schema.',
  'claude_artifacts, and writes schema UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V003, never the C1 schema.'),
 ('python3 -I -B fill_c1_pin_c2v002.py --draft', 'python3 -I -B fill_c1_pin_c2v003_c3v001.py --draft'),
 ("DRAFT_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_DRAFT_C2V002'", "DRAFT_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_DRAFT_C2V003'"),
 ("C1_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_C2V001'", "C1_SCHEMA = 'UNT_DDO154_C1_TAIL_READINESS_H1_C2V002'"),
 ("SYNTHETIC_SCHEMA = 'UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002'", "SYNTHETIC_SCHEMA = 'UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V003'"),
 ("TR_DIGEST_EXCLUDING_REVIEW = '6dc87838fc0e44ff5a8bd8067281644cf2bc2ddab0e367baca180eddeee335aa'   # draft v001 = v002",
  "TR_DIGEST_EXCLUDING_REVIEW = '%s'   # draft v003 (A298)" % NEW_DIGEST),
 ("GUARD_PIN = {'path': ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py',\n"
  "             'sha256': '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'}         # wrapper q5b1 L30",
  "GUARD_PIN = {'path': ART + '/eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py',\n"
  "             'sha256': '3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25'}         # A296 wrapper L32; a296_binding GUARD"),
 ("read_file(GUARD_PIN['path'], GUARD_PIN['sha256'], ART, 'guard b1')", "read_file(GUARD_PIN['path'], GUARD_PIN['sha256'], ART, 'guard b1 a296')"),
 ("'DRAFT_TAIL_READINESS_DIGEST_IS_NOT_6DC87838'", "'DRAFT_TAIL_READINESS_DIGEST_IS_NOT_3C03BAE3'"),
 ("out['synthetic_fixture'] = 'fill_c1_pin_c2v002 --synthetic-test output; not a C1'",
  "out['synthetic_fixture'] = 'fill_c1_pin_c2v003_c3v001 --synthetic-test output; not a C1'"),
 ("            out['status'] = ('C1 (H1), filled from the signed review. It is the frozen C1 once root records it in V006 after '\n"
  "                             'the registry_assembler_c3v005 verify of record passes 31/31 (A209 item 4; A134 Q9(b)3). '\n"
  "                             'Never edited (A134 Q9).')",
  "            out['status'] = ('C1 (H1) successor C2V002 (A298), filled from the signed re-review. It is the frozen C1 once '\n"
  "                             'root records it in V006. Never edited (A134 Q9).')"),
]
raw = open(SRC, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == SRC_SHA, 'SOURCE_PIN'
text = raw.decode()
for old, new in REPL:
    n = text.count(old); assert n == 1, (n, old[:60]); text = text.replace(old, new)
out = sys.argv[1]
with open(out, 'x') as f: f.write(text)
print(out, hashlib.sha256(text.encode()).hexdigest())
