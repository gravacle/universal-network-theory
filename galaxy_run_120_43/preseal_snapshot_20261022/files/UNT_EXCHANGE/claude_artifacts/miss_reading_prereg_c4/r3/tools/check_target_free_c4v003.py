# Claude4 (dispatches 0585, 0606 and 0619/A98.2) target-free check v003 for the miss-reading prereg r3 (tools-builder revision,
# with the r3 fix-stage changes for refute findings RF-B1/TF-B1, TF-S1, TF-S2 and TF-S3; the file name is kept).
# Read-only apart from --out (exclusive create). It never opens target data, so it cannot compare the text with target values.
# It checks mechanically, against fixed deny-lists and a listed-value inventory (not a proof), that the bundle carries none:
#  T1 no deny-listed term (also split by spaces, underscores, hyphens, dots or slashes for the split-able names), data-file
#     extension, unpinned NGC3198-named file (also n3198 and 'NGC 3198'), URL (also file:/ and hxxp), HTML entity or comment,
#     disallowed non-ASCII letter or unexpected bundle file. Scanned: the three texts, INDEX, the provenance JSON and the two
#     entry-table JSONs, each in three variants (NFKC minus Cf/Mn/Me; entities and %XX decoded and markup removed; a Latin
#     skeleton of confusable letters).
#  T2 no velocity-unit token at all, with or without a number (km/s, m/s, cm/s, km s^-1 in any exponent markup, kms, kmps,
#     kpc/Gyr, pc/Myr, km/h, mi/s, AU/yr, words), on the same files and all three variants.
#  T3 no target symbol (v_q, sigma_q, v_obs, V_c, Vflat, v_circ, V_last, e_v, 'observed rotation speed', ...) in a decorated
#     form (code span, escaped, braced, indexed, hyphen-subscripted) followed within one clause by a relation (=, ~, ≈, ≃, ≡, :=,
#     ≔, ≒, <, ≤, ≦, ⩾, →, ∈, is, of, below, between, ...) and a number; a number followed by a relation and such a symbol; or a
#     markdown table with such a symbol heading a column that holds a number. All three variants are scanned.
#  T4 every numeric token of the three texts and of the JSON notes (the entry tables' and the provenance's note) is listed in
#     the provenance, every listed value occurs, and every category is in the closed list CATEGORIES and passes its
#     verification. A number is also counted when its digits are grouped by underscores or thousands commas, when it starts
#     with a dot, or when a prime or markdown emphasis follows it; a backslash before a decimal point is markup. Digits glued
#     to identifiers or to § are counted unless the identifier is a registered shape, occurs in a pinned source or is declared;
#     § is skipped only before a section number of the prereg. Markup between digits, non-ASCII digits and number words fail.
#     The census gives every occurrence with context.
#  T5 every §11 row carrying a sha parses; every pinned source has a target-free path and hashes as stated; each CITED_PINNED
#     V005 entry hashes as pinned, with an exact, allow-listed end-marker whose following bytes are pinned as a tail row; every
#     V005 or V006 entry the texts cite is CITED_PINNED in its table.
#  T6 every clause tag in the prereg has exactly one map row and vice versa.
#  T7 (currency, not target-freeness) the rendered V005 entry table covers every '## ' heading of the V005 bytes exactly once,
#     in file order, with the exact heading text; every entry section, the tail and the whole file still hash as read; the
#     entry-table JSON agrees with the rendered table. The rendered V006 table does the same for every V006 heading before
#     this text's seal entry, the first V006 heading whose section names the sha256 of the bundle's prereg (sections are hashed
#     with trailing newlines removed; before a seal entry exists the whole file must hash as read, after it the bytes before
#     its heading, trimmed, must hash to the trimmed sha read).
# Exit codes: 0 both verdicts PASS; 2 target-free FAIL; 3 target-free PASS and currency FAIL.
# The audit hook (make_hook) refuses target-like opens and listings (the raw path before any '..' is collapsed, NFKC- and
# case-folded and separator-squashed, then the realpath of every prefix), writes other than --out, mkdir, truncate, symlink,
# link, chmod, utime, exec, fork, spawn, subprocess, deletes, renames and network. LIMITS lists what is left.
# usage: python3 -I -B check_target_free_c4v003.py --dir R3DIR --provenance NUMBER_PROVENANCE_R3.json --slots SLOTS.json
#        --expect-slots-sha H --nodes NODES.json --expect-nodes-sha H [--v005 V005_COPY.md] [--v006 V006_COPY.md]
#        [--out RESULT.json]
import argparse, hashlib, html, json, os, re, sys, unicodedata
from urllib.parse import unquote as _pct_decode           # decoding only; no request is made

SCHEMA = 'UNT_MISS_READING_R3_TARGET_FREE_CHECK_C4V003'
ETAB_SCHEMA = 'UNT_MISS_READING_V005_ENTRY_TABLE_C4V001'
ETAB6_SCHEMA = 'UNT_MISS_READING_V006_ENTRY_TABLE_C4V001'
PREREG, CSM, ROOT = 'PREREG_MISS_READING_R3.md', 'CLAUSE_SOURCE_MAP_R3.md', 'ROOT_ITEMS_R3.md'
PROV, ETAB, INDEX = 'NUMBER_PROVENANCE_R3.json', 'V005_ENTRY_TABLE_R3.json', 'INDEX_R3.md'
ETAB6 = 'V006_ENTRY_TABLE_R3.json'
TEXT_FILES = (PREREG, CSM, ROOT)
AUX_FILES = (INDEX, PROV, ETAB, ETAB6)
OUTPUT_FILES = ('TARGET_FREE_CHECK_R3.json', 'TARGET_FREE_MUTATION_TEST_R3.json', 'HASHES_R3.txt')
TOOL_FILES = ('check_target_free_c4v003.py', 'test_check_target_free_c4v003.py', 'make_miss_reading_c4v004.py')
EXCHANGE = '/Users/bgm/Research/UNT_EXCHANGE/'
OUTBOXES = ('FROM_CODEX', 'FROM_CODEX1', 'FROM_CODEX2', 'FROM_CODEX3', 'FROM_CLAUDE2', 'FROM_CLAUDE3', 'FROM_CLAUDE4')
DISPATCH_DIR = EXCHANGE + 'FROM_CODEX/'
ART = EXCHANGE + 'claude_artifacts/'
CLAUDE2_DIR = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
ROOTS = {
    '…/FIRST_CONSTRUCTION_REVIEW_2026-10-13/': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/',
    '.../FIRST_CONSTRUCTION_REVIEW_2026-10-13/': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/',
    '…/CLAUDE2/': CLAUDE2_DIR,
    '.../CLAUDE2/': CLAUDE2_DIR,
    'claude_artifacts/': ART,
}
DECISIONS = {'V003': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md',
             'V004': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
             'V005': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md',
             'V006': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'}
V005_PATH = CLAUDE2_DIR + DECISIONS['V005']
V006_PATH = CLAUDE2_DIR + DECISIONS['V006']
OPEN_ADDENDA = ('decisions V005', 'decisions V006')   # whole-file shas compared by T7, not T5
END_MARKER_ALLOW = {'A65': '**Lanes.**'}          # the only entry whose pin may end before its next heading
DISPOSITIONS = ('CITED_PINNED', 'NO_CHANGE')
ETAB_HEADER = '| entry | heading (verbatim, without the leading `## `) | disposition | reason | ends before | section sha256 |'
ETAB6_HEADER = '| V006 entry | heading (verbatim, without the leading `## `) | disposition | reason | ends before | section sha256 |'
ETAB_SEP = '|---|---|---|---|---|---|'
LEGACY_HEADER = '| entry | used for | ends before | section sha256 |'
NEXT_HEADING = 'next heading'
TAIL_SUFFIX = ' tail'

LIMITS = [
    'os.stat, os.lstat, os.path.exists, os.path.isfile and os.path.realpath raise no audit event, so the hook cannot refuse a '
    'stat; the code tests every path against the deny-list before it stats or opens it, lexically first on the raw path '
    '(before any ".." is collapsed; NFKC- and case-folded, invisible marks removed, separators squashed; no filesystem call) '
    'and then by the realpath of every prefix, whose symlink resolution uses lstat and readlink (a link target is lstat-ed '
    'while it is resolved) but never opens the resolved path',
    'the hook sees Python-level events only: native code, descriptors opened before it was installed and an open relative to '
    'a dir_fd are outside its path test; the check starts no process',
    'the deny-list and the unit, symbol and identifier patterns are fixed lists; they are not exhaustive',
    'T4 checks token values, not each occurrence; the census lists every occurrence with its context for review',
    'categories come from a closed list; quoted values are located in pinned source bytes, which is a weak test for small '
    'integers; HEADING_OR_ITEM_NUMBER, INDEX and REVIEW_COUNT are shape-checked only; post numbers are checked against the '
    'exchange folders',
    'an identifier chain is skipped when it matches a registered shape, occurs in a pinned source or is declared in the '
    'provenance; a value glued into such a chain is not seen',
    'T4 does not value-check bare numbers in the provenance uses strings (they derive the listed values) or in INDEX (written '
    'by the generator from counts and shas); T1 to T3 still scan both for terms, units and symbol-value pairs',
    'number words below eleven, roman numerals, clock-shaped ratios, a middle dot between digits (read as multiplication, as '
    'in a square root times a number) and digit-for-letter spellings are not value-checked',
    'T5 judges a pinned source target-free by its path; content target-freeness rests on the source registration',
    'T7 compares against the V005 and V006 bytes it reads; a currency PASS is meaningful only against the live files or the '
    'frozen copies; V006 is found by its registered file name, and its seal entry by the prereg sha it names',
    'the check never opens target data, so it cannot compare the text with target values',
]

# ---------------------------------------------------------------------------------------------------------------- deny lists
DENY_TERMS = ('rotmod', 'vobs', 'v_obs', 'vrot_obs', 'massmodel', 'sparc', 'lelli', 'begeman', 'vgas', 'vdisk', 'vbul',
              'e_vobs', 'errv', 'rotcur', 'rotation_curve', 'deblok', 'de_blok', 'albada', 'gentile', 'karukes',
              'observed_curve', 'observed_velocit', 'observedcurve', 'observedvelocit', 'kmax_a2f10_c5h', 'c5h_run')
_SEP = r'[\s_\-./\\]*'                     # the separators a split name may carry (fix stage: dots and slashes added)
DENY_RES = [re.compile(p, re.I) for p in (
    r'\bv\s*[-_./\\]?\s*obs\b', r'mass' + _SEP + r'models?\b', r'\bde' + _SEP + r'blok\b', r'\bvan' + _SEP + r'albada\b',
    r'rotation' + _SEP + r'curve' + _SEP + r'(?:data|tables?|files?)\b', r'\brot' + _SEP + r'mod\b',
    r'\bs[\s.]{0,2}p[\s.]{0,2}a[\s.]{0,2}r[\s.]{0,2}c\b', r'\bkmax' + _SEP + r'a2f10' + _SEP + r'c5h', r'\bc5h' + _SEP + r'run\b',
    r'\bc5h_', r'\buvt_[a-z0-9]', r'\buvt[\s\-./]+[a-z0-9]{1,8}[\s_\-./]+a2f10',
    r'\bthings\s+(?:survey|data|cubes?|curves?|tables?|catalog(?:ue)?|velocit\w*|rotation|hi)\b')] + [
    re.compile(r'\bTHINGS\b'), re.compile(r'\bT\.\s?H\.\s?I\.\s?N\.\s?G\.\s?S\b')]
DATA_EXT = re.compile(r'\.(?:dat\w*|data|mrt|csv|tsv|fits?|fts|tbl|ecsv|vot(?:able)?|ipac|rdb|txt|asc|xlsx?|h5|hdf5?|npy|'
                      r'parquet|pkl|pickle|sav|sqlite|db)(?![A-Za-z0-9])', re.I)
EXT_EXEMPT = re.compile(r'^HASHES(?:_[A-Za-z0-9_]+)?\.txt$')
NGC_FILE = re.compile(r'[^\s`\'"|()\[\]<>]*(?<![A-Za-z])(?:ngc|n)[_\- ]?3198[^\s`\'"|()\[\]<>]*\.[A-Za-z][A-Za-z0-9]{0,7}'
                      r'(?![A-Za-z0-9])', re.I)
URL = re.compile(r'\b(?:https?|ftp|file)://|\bwww\.|\bfile:/|\bh[tx]{2}ps?://', re.I)
ENTITY = re.compile(r'&(?:#\d{1,7}|#[xX][0-9A-Fa-f]{1,6}|[A-Za-z][A-Za-z0-9]{1,31});')
COMMENT = re.compile(r'<!--')
ALLOWED_GREEK = set('αβγδεζηθλμξπρσςτφχψωΓΔΘΛΞΠΣΦΨΩ')
CONFUSABLE = {'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x', 'к': 'k', 'м': 'm', 'т': 't', 'в': 'b',
              'н': 'h', 'і': 'i', 'ј': 'j', 'ѕ': 's', 'ԁ': 'd', 'ɡ': 'g', 'һ': 'h', 'ӏ': 'l', 'ο': 'o', 'α': 'a', 'ρ': 'p',
              'ν': 'v', 'τ': 't', 'κ': 'k', 'ι': 'i', 'υ': 'u', 'χ': 'x', 'ε': 'e', 'β': 'b', 'А': 'A', 'В': 'B', 'Е': 'E',
              'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'У': 'Y', 'Ѕ': 'S', 'І': 'I',
              'Ј': 'J', 'Α': 'A', 'Β': 'B', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Ι': 'I', 'Κ': 'K', 'Μ': 'M', 'Ν': 'N', 'Ο': 'O',
              'Ρ': 'P', 'Τ': 'T', 'Υ': 'Y', 'Χ': 'X', 'ı': 'i', 'ℓ': 'l'}
UNIT_RES = [re.compile(p, re.I) for p in (
    r'(?<![A-Za-z])(?:k?m|cm|mm)\s*[/∕⁄÷]\s*s(?:ec(?:onds?)?)?(?![A-Za-z])',
    r'(?<![A-Za-z])(?:k?m|cm)\s*(?:[·⋅.*×]\s*)?s\s*(?:\^|\*\*)?\s*\(?\s*[-−–‐‑‒—]\s*1\s*\)?(?![0-9])',
    r'(?<![A-Za-z])kms(?:\s*[-−–]?\s*1)?(?![A-Za-z])',
    r'(?<![A-Za-z])kmps(?![A-Za-z])',
    r'kilomet(?:re|er)s?\s*(?:per|/|∕|⁄)\s*s(?:ec(?:ond)?s?)?\b',
    r'(?<![A-Za-z])(?:k?m|cm)\s+per\s+s(?:ec(?:ond)?s?)?\b',
    r'(?<![A-Za-z])met(?:re|er)s?\s*(?:per|/|∕|⁄)\s*s(?:ec(?:ond)?s?)?\b',
    r'(?<![A-Za-z])(?:k|M)?pc\s*(?:[/∕⁄]|\s+per\s+)\s*(?:G|M|k)?yrs?(?![A-Za-z])',
    # fix stage (TF-S2 unit classes): inverse-time exponents, other distance/time pairs, big or fullwidth solidus, emphasis
    r'(?<![A-Za-z])(?:k|M)?pc\s*(?:[·⋅.*×]\s*)?(?:G|M|k)?yrs?\s*(?:\^|\*\*)?\s*\(?\s*[-−–‐‑‒—]\s*1\s*\)?(?![0-9])',
    r'(?<![A-Za-z])(?:k?m|cm|mm|mi|au|ly|k?pc)\s*[/∕⁄÷⧸／]\s*[_*]*\s*(?:s|secs?|seconds?|h|hrs?|hours?|yrs?|years?|myr|gyr)'
    r'[_*]*(?![A-Za-z])',
    r'(?<![A-Za-z])(?:kilomet(?:re|er)s?|met(?:re|er)s?|miles?)\s+(?:a|an|each|every|per)\s+(?:sec(?:ond)?|hour)s?\b')]
_SYMB = (r'(?:[vV][_\-‐]?(?:q|obs|rot|flat|c|circ|max|out|outer|meas|measured|observed|true|inf|∞|last|first|end|edge|tail|'
         r'target|data|q\d{1,2})'
         r'|[vV](?:obs|rot|flat|circ|max|last)|[σΣς]_?(?:q|v|obs|rot|vobs)|sigma_?(?:q|v|obs|rot)|e_?v(?:_?obs|_?q)?|err_?v\w*)')
SYM = (r'(?:(?<![A-Za-z0-9])' + _SYMB + r'(?![A-Za-z0-9])'
       r'|observed\s+(?:rotation\s+|circular\s+)?(?:speeds?|velocity|velocities)|(?:rotation|circular)\s+(?:speed|velocity)'
       r'|(?:outer|outermost|inner|flat|orbital)\s+(?:speeds?|velocity|velocities))')
_RELSYM = r'(?:=|≈|≃|≅|~|∼|≡|<|≤|>|≥|≲|≳|⩽|⩾|≦|≧|≒|≓|≐|≑|≔|≕|→|⟶|↦|⇒|∈|≪|≫|≍|:)'
REL = (r'(?:' + _RELSYM[3:-1] + r'|\b(?:is|was|are|of|equals?|reads?|below|above|under|over|about|around|nearly|near|'
       r'approx(?:imately)?|than|at|exceeds?|roughly|reach(?:es|ing)?|between|within)\b)')
T3_RE = re.compile(SYM + r'(?:\s*\([^()\n]{0,40}\))?(?:(?![.;](?:\s|$))[^\n]){0,48}?' + REL
                   + r'[\s(\[~∼≈≃=:<>≤≥\-−+$*_]*\d+(?:[.,]\d+)*(?:[eE][-+−]?\d+)?', re.I)
# value first: a number, a symbolic relation (or "is"/"equals") and a target symbol, within a short span
T3_REV = re.compile(r'(?<![\w.])\d+(?:[.,]\d+)*(?:[eE][-+−]?\d+)?\s*[*_`$]*\s*(?:' + _RELSYM[3:-1] + r'|\b(?:is|equals?)\b)'
                    + r'\s*[(\[{`*_$\\]*\s*' + SYM, re.I)
NUMBER_WORDS = re.compile(r'\b(?:eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|'
                          r'forty|fifty|sixty|seventy|eighty|ninety|hundreds?|thousands?|millions?)\b', re.I)
MARKUP_DIGITS = re.compile(r'\d(?:\*+|`+|~~|<!--.*?-->|<[^>\n]{0,40}>|&[#\w]+;|\\[.,;:! ]|\$)+\d')

# ------------------------------------------------------------------------------------------------- T4 tokens and identifiers
HEX64 = re.compile(r'(?<![0-9A-Fa-f])[0-9a-f]{64}(?![0-9A-Fa-f])')
TAG = re.compile(r'\[(C-[A-Za-z0-9.]+)\]')
ISO = re.compile(r'(?<![0-9:.])20\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?:T(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?Z?)?(?![0-9:])'
                 r'|(?<![\w:.])~?(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?Z?(?![\w:])'
                 r'|(?<![\w:.])(?:[01]\d|2[0-3])[0-5]\dZ(?![\w:])')
UPLUS = re.compile(r'\bU\+[0-9A-Fa-f]{4,6}\b')
SECTION_REF = re.compile(r'§\s*(\d+(?:\.\d+)*)')
CODE_SPAN = re.compile(r'`([^`\n]+)`')
HEX_RUN = re.compile(r'(?<![0-9A-Za-z])[0-9a-f]{6,63}(?![0-9A-Za-z])')
NUM_SCI = re.compile(r'(?<![\w′.])\d+(?:\.\d+)?[eE][-+−]?\d+(?![\w′])')
HEX_LIT = re.compile(r'(?<![\w′])0[xX][0-9A-Fa-f]+(?![\w′])')
CHAIN = re.compile(r'(?<![\w′])[\w′]+(?:[-.][\w′]+)*')
NUM = re.compile(r'(?<![\w′.])\d+(?:\.\d+)?(?![\w′])')          # the pinned-source corpus form (unchanged)
# the final T4 pass (fix stage, TF-S2): underscores, primes and emphasis around a number no longer hide it; digit groups
# joined by underscores or by thousands commas, a leading-dot number and a backslash-hidden decimal are one token each
NUM_T4 = re.compile(r'(?<![A-Za-z0-9.\\])(\.\d+|\d{1,3}(?:,\d{3})+(?![\d])(?:\.\d+)?|\d+(?:_\d+)*(?:\\?\.\d+(?:_\d+)*)*)(?![A-Za-z0-9])')


def canon_num(tok):
    """The token key of a final-pass number: group separators and escapes removed."""
    return tok.replace('_', '').replace('\\', '').replace(',', '')
DIGITS = re.compile(r'\d+')
LETTER = re.compile(r'[^\W\d_]')
FAMILY = re.compile('(?:' + '|'.join((
    r'NGC3198-Q(?:0[1-9]|[1-3]\d|4[0-3])', r'Q(?:0[1-9]|[1-3]\d|4[0-3])', r'A\d{1,3}(?:\.\d{1,2})*[a-z]?',
    r'[MID]-\d{1,2}', r'P(?:\d|1[0-5])g?', r'C-\d{1,2}(?:\.\d{1,2})*', r'C-[A-Z][0-9]?', r'(?:R|DT|UT|BH|CA|RI|P|SEM|S0)-[A-Za-z0-9]{1,8}',
    r'SA-[A-Z]{1,4}-\d{2}', r'L-C\d{2}', r'[A-Z]-\d{2}', r'B-\d{1,2}', r'R2[ABC]-[A-Z]?\d{1,2}', r'CX2(?:-[A-Z0-9]+){1,4}',
    r'[A-PR-UW-Z]\d{1,2}[a-z]?′?', r'(?!V)[A-Z]{2,4}\d{1,2}[a-z]?′?', r'[A-Z]\d[A-Z][a-z]?', r'T120L', r'DDO154', r'NGC3198',
    r'K(?:8|16|32|64|128)', r'[Vv]0\d{1,2}[a-z]?', r'[a-z]{1,3}\d[vr]0\d{2}[a-z]?(?:r\d)?', r'[A-Z]{1,3}\d[VR]0\d{2}[A-Z]?',
    r'r(?:[1-9]|1\d)', r'round[1-9]', r'R[1-9]', r'(?:Claude|Codex|CLAUDE|CODEX)[1-4]', r'sha256', r'U\+[0-9A-F]{4,5}',
    r'N[0-4]′?', r'C[1-4]′?', r'E[1-3]b?', r'GL(?:4|10)', r'h_NN', r'M5')) + ')')
PIECE = re.compile('(?:' + '|'.join((r'(?!V)[A-Z]{1,4}\d{1,2}[a-z]?′?', r'[Vv]0\d{1,2}[a-z]?', r'[a-z]{1,3}\d[vr]0\d{2}[a-z]?',
                                     r'[A-Z]{1,3}\d[VR]0\d{2}[A-Z]?', r'r(?:[1-9]|1\d)', r'R[1-9]', r'round[1-9]')) + ')')

CATEGORIES = {
    'QUERY_RADIUS': 'BYTES: equals Rad_text of each named query id in the slots query block',
    'NODE_RADIUS': 'BYTES: equals radii_kpc[node_index] of the GL4 nodes, rounded to the shown decimals',
    'NODE_DERIVED': 'BYTES: equals the stated formula on registered node radii and query radii, rounded',
    'MODEL_DIAGNOSTIC': 'LOCATED: occurs as a number in a pinned source',
    'NUMERICS_RULING': 'LOCATED',
    'GEOMETRY_REGISTERED': 'LOCATED',
    'BARYON_MODEL_REGISTERED': 'LOCATED',
    'RULE_CONSTANT': 'LOCATED',
    'ROW_COUNT': 'LOCATED',
    'MODEL_COUNT': 'LOCATED',
    'HEADING_OR_ITEM_NUMBER': 'SHAPE: n or n.m with at most two digits each',
    'INDEX': 'SHAPE: an integer 0 to 99',
    'REVIEW_COUNT': 'SHAPE: an integer below 1000 (verified by review)',
    'DISPATCH_OR_POST_NUMBER': 'EXCHANGE: four digits with a leading zero, and a message with that number exists in an outbox',
    'TEXT_EXAMPLE_VALUE': 'LOCATED: an example value quoted from a pinned earlier text (an option it named); not a quantity of this text',
}
LOCATED = {k for k, v in CATEGORIES.items() if v.startswith('LOCATED')}


# ----------------------------------------------------------------------------------------------------------------- the hook
_DENY_PATH = ('rotmod', 'vobs', 'v_obs', 'massmodel', 'mass_model', 'sparc', 'lelli', 'begeman', 'things', 'deblok', 'de_blok',
              'albada', 'gentile', 'karukes', 'observed_curve', 'observed_velocit', 'rotation_curve', 'rotcur',
              'kmax_a2f10_c5h', 'c5h_run')
REFUSED_EVENTS = frozenset((
    'os.truncate', 'os.ftruncate', 'os.symlink', 'os.link', 'os.chmod', 'os.lchmod', 'os.chown', 'os.lchown', 'os.chflags',
    'os.lchflags', 'os.utime', 'os.remove', 'os.unlink', 'os.rename', 'os.replace', 'os.rmdir', 'os.removedirs', 'shutil.rmtree',
    'shutil.move', 'shutil.chown', 'shutil.make_archive', 'shutil.unpack_archive', 'os.exec', 'os.fork', 'os.forkpty',
    'os.posix_spawn', 'os.spawn', 'os.system', 'os.startfile', 'os.kill', 'os.killpg', 'signal.pthread_kill', 'pty.spawn',
    'os.mkfifo', 'os.mknod', 'os.add_dll_directory', 'socket.__new__', 'socket.connect', 'socket.bind', 'socket.getaddrinfo',
    'socket.gethostbyname', 'socket.gethostbyaddr', 'socket.sendto', 'socket.sendmsg', 'urllib.Request', 'http.client.connect',
    'ftplib.connect', 'smtplib.connect', 'poplib.connect', 'imaplib.open', 'nntplib.connect', 'webbrowser.open', 'ctypes.dlopen',
    'ctypes.dlsym', 'ctypes.call_function', 'sqlite3.connect', 'tempfile.mkstemp', 'tempfile.mkdtemp'))


def _fold_path(q):
    """NFKC, invisible and combining marks removed, confusable letters mapped, then full case folding: the same name this
    case-insensitive volume would resolve (the long s folds to s, the Kelvin sign to k)."""
    q = unicodedata.normalize('NFKC', q)
    q = ''.join(ch for ch in q if unicodedata.category(ch) not in ('Cf', 'Mn', 'Me'))
    q = ''.join(CONFUSABLE.get(ch, ch) for ch in q)
    return q.casefold()


def _denied_text(q):
    """True when the folded path, or its separator-squashed components, contain a deny term, or a component starts 'uvt'
    followed by a separator. The module-level _DENY_PATH is read at call time."""
    f = _fold_path(q)
    comps = f.split(os.sep)
    squashed = os.sep.join(re.sub(r'[\s_\-.]+', '', c) for c in comps)
    if any(w in f for w in _DENY_PATH):
        return True
    if any(re.sub(r'[\s_\-.]+', '', w) in squashed for w in _DENY_PATH):
        return True
    return any(re.match(r'uvt[\s_\-.]', c) for c in comps)


def path_denied(p):
    """True when the raw path (before any '..' is collapsed), its cwd-joined form, or the realpath of any prefix of it is
    deny-named. The lexical tests come first and need no filesystem call, so a deny-named path is refused before anything
    stats it; the prefix realpaths (lstat and readlink only) then catch a clean-looking symlink that resolves into a
    deny-named place, even when a later '..' would lead out of it again."""
    raw = os.fsdecode(p)
    if _denied_text(raw):
        return True
    a = raw if os.path.isabs(raw) else os.path.join(os.getcwd(), raw)
    if _denied_text(a):
        return True
    parts = a.split(os.sep)
    for i in range(2, len(parts) + 1):
        pre = os.sep.join(parts[:i])
        if pre and _denied_text(os.path.realpath(pre)):
            return True
    return False


def _under(p, roots):
    r = os.path.realpath(p)
    return any(r == d or r.startswith(d + os.sep) for d in roots)


def make_hook(write_files=(), write_dirs=(), mkdir_dirs=(), exec_ok=None):
    """An audit hook: target-like opens and listings refused by lexical path and realpath; writes only to write_files or
    under write_dirs (realpath); mkdir only under mkdir_dirs; subprocess only when exec_ok(args) is true; REFUSED_EVENTS refused."""
    wf = {os.path.realpath(x) for x in write_files} | {os.devnull}
    wd = [os.path.realpath(x) for x in write_dirs]
    md = [os.path.realpath(x) for x in mkdir_dirs]

    def hook(event, args):
        if event == 'open':
            path = args[0] if args else None
            if path is None or isinstance(path, int):
                return
            p = os.fsdecode(path)
            if path_denied(p):
                raise PermissionError('refused target-like or protected path: %s' % p)
            mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
            flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
            writing = any(c in mode for c in 'wax+') or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
            if writing and not (os.path.realpath(p) in wf or _under(p, wd)):
                raise PermissionError('write refused: %s' % p)
        elif event in ('os.listdir', 'os.scandir', 'glob.glob', 'glob.glob/2'):
            path = args[0] if args else '.'
            if path is None:
                path = '.'
            if isinstance(path, int):
                return
            if path_denied(os.fsdecode(path)):
                raise PermissionError('refused listing of a target-like or protected path: %s' % os.fsdecode(path))
        elif event == 'os.mkdir':
            if not _under(os.fsdecode(args[0]), md):
                raise PermissionError('mkdir refused: %s' % os.fsdecode(args[0]))
        elif event == 'subprocess.Popen':
            if not (exec_ok and exec_ok(args)):
                raise PermissionError('refused: subprocess %r' % (args[1],))
        elif event in REFUSED_EVENTS:
            raise PermissionError('refused: %s' % event)
    return hook


# ------------------------------------------------------------------------------------------------------------ normalization
def norm(t):
    t = unicodedata.normalize('NFKC', t)
    return ''.join(ch for ch in t if unicodedata.category(ch) not in ('Cf', 'Mn', 'Me'))


def strip_markup(t):
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<[^>\n]{0,80}>', '', t)
    t = re.sub(r'\\(?:mathrm|rm|text|textrm|mathit|operatorname)\b', '', t)
    t = re.sub(r'\\[,;:! ]', ' ', t)
    t = t.replace('\\', '')
    for s in ('**', '__', '~~', '*', '`', '$', '{', '}'):
        t = t.replace(s, '')
    return t


def skeleton(t):
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(ch for ch in t if unicodedata.category(ch) not in ('Mn', 'Me', 'Cf'))
    return ''.join(CONFUSABLE.get(ch, ch) for ch in t)


def variants(raw):
    a = norm(raw)
    b = norm(strip_markup(html.unescape(_pct_decode(raw))))
    return {'normalized': a, 'unmarked': b, 'skeleton': skeleton(b)}


def strict_load(path):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('duplicate key %r in %s' % (k, path))
            d[k] = v
        return d
    with open(path, 'rb') as f:
        return json.loads(f.read().decode('utf-8'), object_pairs_hook=hook,
                          parse_constant=lambda c: (_ for _ in ()).throw(ValueError('non-finite %s' % c)))


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    with open(path, 'rb') as f:
        return sha_bytes(f.read())


def blank(t, spans):
    if not spans:
        return t
    chars = list(t)
    for s, e in spans:
        for i in range(s, e):
            if chars[i] != '\n':
                chars[i] = ' '
    return ''.join(chars)


# ---------------------------------------------------------------------------------------------------------------- V005 model
def entry_id(heading_line):
    """The entry id of a '## ' heading: the text before its first ':', else the whole heading text."""
    h = heading_line[3:]
    return (h.split(':', 1)[0] if ':' in h else h).strip()


def v005_headings(text):
    """[(line_index, heading_line, entry_id)] for every line starting with '## ', in file order."""
    return [(i, l, entry_id(l)) for i, l in enumerate(text.split('\n')) if l.startswith('## ')]


def natural_sections(text):
    """{line_index_of_heading: (start, end)} where end is the next '## ' line index or the line count."""
    lines = text.split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith('## ')]
    return {i: (i, starts[j + 1] if j + 1 < len(starts) else len(lines)) for j, i in enumerate(starts)}


def join_lines(lines, s, e):
    body = '\n'.join(lines[s:e])
    if e < len(lines):
        body += '\n'
    return body


def entry_parts(text, heading_index, marker=''):
    """(main, tail, marker_problem) bytes of the entry whose heading is at heading_index. Without a marker, main is the natural
    section and tail is None. With a marker, exactly one line of the natural section after the heading must equal the marker
    (the exact end-marker); main ends before that line and tail runs from it to the end of the natural section."""
    lines = text.split('\n')
    s, e = natural_sections(text)[heading_index]
    if not marker:
        return join_lines(lines, s, e), None, None
    hits = [k for k in range(s + 1, e) if lines[k] == marker]
    if len(hits) != 1:
        return None, None, 'end-marker %r is %d lines of the section (exactly one whole line required)' % (marker, len(hits))
    k = hits[0]
    return join_lines(lines, s, k), join_lines(lines, k, e), None


def split_cells(line):
    """Cells of a strict markdown row '| a | b |': no trailing blank, unescaped '|' separators; None if not strict."""
    if not (line.startswith('| ') and line.endswith(' |')) or line != line.rstrip() or '\t' in line:
        return None
    inner = line[2:-2]
    parts = re.split(r'(?<!\\) \| ', inner)
    return [p.replace('\\|', '|') for p in parts]


def esc_cell(s):
    return s.replace('|', '\\|')


def section11_span(text):
    """The sources section: the '## <n>. Sources' heading (any n), else '## 11.', up to the next '## ' heading or EOF."""
    hs = re.findall(r'^## \d+\.\s+Sources\b.*$', text, re.M)
    if len(hs) > 1:
        return None
    m = re.search(r'^## \d+\.\s+Sources\b.*$', text, re.M) or re.search(r'^## 11\..*$', text, re.M)
    if not m:
        return None
    n = re.search(r'^## ', text[m.end():], re.M)
    return m.start(), (m.end() + n.start()) if n else len(text)


def parse_v005_tables(prereg):
    """Parse the rendered entry table and the optional legacy pin table in §11. Returns (rows, legacy, problems, spans), where
    spans are (start, end) offsets of every V005 table line in the prereg (excluded from the citation scan)."""
    rows, legacy, problems, spans = [], [], [], []
    sp = section11_span(prereg)
    if sp is None:
        return rows, legacy, ['no unique sources section ("## <n>. Sources" or "## 11.")'], spans
    s0, s1 = sp
    body = prereg[s0:s1]
    lines = body.split('\n')
    offs, o = [], s0
    for l in lines:
        offs.append(o)
        o += len(l) + 1
    n_header, n_legacy = 0, 0
    mode = None
    for i, l in enumerate(lines):
        if l == ETAB_HEADER:
            n_header += 1
            mode = 'etab'
            spans.append((offs[i], offs[i] + len(l)))
            continue
        if l == LEGACY_HEADER:
            n_legacy += 1
            mode = 'legacy'
            spans.append((offs[i], offs[i] + len(l)))
            continue
        if l == ETAB6_HEADER:
            mode = 'v006'                          # the V006 table is parsed by parse_v006_table
            continue
        if mode == 'v006':
            if not l.startswith('|'):
                mode = None
            continue
        if mode and l.startswith('|'):
            spans.append((offs[i], offs[i] + len(l)))
            if re.fullmatch(r'\|(?:-+\|)+', l):
                continue
            cells = split_cells(l)
            want = 6 if mode == 'etab' else 4
            if cells is None or len(cells) != want:
                problems.append('unparsable V005 %s row: %r' % ('entry-table' if mode == 'etab' else 'pin', l[:160]))
                continue
            if mode == 'etab':
                ent, head, disp, reason, marker, shac = cells
                hstart = offs[i] + l.index(' | ') + 3
                rec = {'entry': ent, 'heading': head, 'disposition': disp, 'reason': reason, 'ends_before': marker,
                       'sha_cell': shac, 'line': l, 'heading_span': (hstart, hstart + len(esc_cell(head)))}
            else:
                ent, reason, marker, shac = cells
                rec = {'entry': ent, 'heading': None, 'disposition': 'TAIL_PINNED' if ent.endswith(TAIL_SUFFIX) else 'CITED_PINNED',
                       'reason': reason, 'ends_before': marker, 'sha_cell': shac, 'line': l}
            m = re.fullmatch(r'`([0-9a-f]{64})`', shac)
            if not m:
                problems.append('V005 row %r: the sha cell is not one backticked sha256' % ent)
                continue
            rec['sha'] = m.group(1)
            mk = rec['ends_before']
            if mk == NEXT_HEADING:
                rec['marker'] = ''
            elif mode == 'legacy' and rec['disposition'] == 'TAIL_PINNED':
                mm = re.fullmatch(r'from `([^`]+)` to the next heading or end of file', mk)
                rec['marker'] = mm.group(1) if mm else None
            else:
                mm = re.fullmatch(r'`([^`]+)`', mk)
                rec['marker'] = mm.group(1) if mm else None
            if rec['marker'] is None:
                problems.append('V005 row %r: unparsable end-marker cell %r' % (ent, mk))
                continue
            if mode == 'etab' and disp not in DISPOSITIONS + ('TAIL_PINNED',):
                problems.append('V005 row %r: unknown disposition %r' % (ent, disp))
                continue
            (rows if mode == 'etab' else legacy).append(rec)
            continue
        if mode and not l.startswith('|'):
            mode = None
        if not mode and re.match(r'^\|\s*A\s?\d{1,3}[a-z]?(?: tail)?\s*\|', l):
            problems.append('V005-like row outside the entry table: %r' % l[:160])
    if n_header != 1:
        problems.append('the V005 entry table header must occur exactly once in §11 (found %d)' % n_header)
    if n_legacy > 1:
        problems.append('the legacy V005 pin table occurs %d times' % n_legacy)
    return rows, legacy, problems, spans


def parse_v006_table(prereg):
    """Parse the rendered V006 entry table in §11. Returns (rows, problems, spans, n_header). Rows carry entry, heading,
    disposition, reason, sha and heading_span; a V006 row's end-marker must be 'next heading' (no V006 allow-list)."""
    rows, problems, spans = [], [], []
    sp = section11_span(prereg)
    if sp is None:
        return rows, ['no unique sources section'], spans, 0
    s0, s1 = sp
    body = prereg[s0:s1]
    lines = body.split('\n')
    offs, o = [], s0
    for l in lines:
        offs.append(o)
        o += len(l) + 1
    n_header, mode = 0, False
    for i, l in enumerate(lines):
        if l == ETAB6_HEADER:
            n_header += 1
            mode = True
            spans.append((offs[i], offs[i] + len(l)))
            continue
        if not mode:
            continue
        if not l.startswith('|'):
            mode = False
            continue
        spans.append((offs[i], offs[i] + len(l)))
        if re.fullmatch(r'\|(?:-+\|)+', l):
            continue
        cells = split_cells(l)
        if cells is None or len(cells) != 6:
            problems.append('unparsable V006 entry-table row: %r' % l[:160])
            continue
        ent, head, disp, reason, marker, shac = cells
        hstart = offs[i] + l.index(' | ') + 3
        m = re.fullmatch(r'`([0-9a-f]{64})`', shac)
        if not m:
            problems.append('V006 row %r: the sha cell is not one backticked sha256' % ent)
            continue
        if marker != NEXT_HEADING:
            problems.append('V006 row %r: the end-marker must be %r' % (ent, NEXT_HEADING))
            continue
        if disp not in DISPOSITIONS:
            problems.append('V006 row %r: unknown disposition %r' % (ent, disp))
            continue
        rows.append({'entry': ent, 'heading': head, 'disposition': disp, 'reason': reason, 'sha': m.group(1), 'marker': '',
                     'line': l, 'heading_span': (hstart, hstart + len(esc_cell(head)))})
    if n_header > 1:
        problems.append('the V006 entry table header occurs %d times in §11' % n_header)
    return rows, problems, spans, n_header


def v006_sections(text):
    """[(heading_line, entry_id, section_text, start_offset)] of a V006 text, sections running to the next '## ' line."""
    lines = text.split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith('## ')]
    offs, o = [], 0
    for l in lines:
        offs.append(o)
        o += len(l) + 1
    out = []
    for j, i in enumerate(starts):
        e = starts[j + 1] if j + 1 < len(starts) else len(lines)
        out.append((lines[i], entry_id(lines[i]), join_lines(lines, i, e), offs[i]))
    return out


def trimmed_sha(s):
    """sha256 of a V006 section or prefix with its trailing newlines removed (appending a later entry leaves it unchanged)."""
    if isinstance(s, str):
        s = s.encode('utf-8')
    return sha_bytes(s.rstrip(b'\n'))


def cited_v005(texts, v005_ids, exclude):
    """{entry: [contexts]} for every V005 entry a text cites: 'A<n>' or 'A<n><letter>' whose entry exists in V005 (a suffix
    letter falls back to the base entry), outside the excluded spans (the V005 tables of §11)."""
    out = {}
    for name, t in texts.items():
        ex = exclude.get(name, [])
        for m in re.finditer(r'(?<![\w-])A(\d{1,3})([a-z]?)(?![a-zA-Z0-9])', t):
            if any(s <= m.start() < e for s, e in ex):
                continue
            ent = 'A' + m.group(1) + m.group(2)
            if ent not in v005_ids:
                ent = 'A' + m.group(1)
                if ent not in v005_ids:
                    continue
            ctx = ' '.join(t[max(0, m.start() - 50):m.end() + 50].split())
            out.setdefault(ent, []).append('%s: …%s…' % (name, ctx))
    return out


# ------------------------------------------------------------------------------------------------------------- §11 sources
def expand(p):
    for k, v in ROOTS.items():
        if p.startswith(k):
            return v + p[len(k):]
    return p


def parse_sources(prereg, v005_override=None, v006_override=None):
    """Every non-entry-table row of §11 that carries a sha256 -> (label, path, sha). Rows that cannot be parsed are problems."""
    sp = section11_span(prereg)
    out, problems = [], []
    if sp is None:
        return out, ['no unique sources section ("## <n>. Sources" or "## 11.")']
    body = prereg[sp[0]:sp[1]]
    mode = None
    for l in body.split('\n'):
        if l in (ETAB_HEADER, LEGACY_HEADER, ETAB6_HEADER):
            mode = 'v005'
            continue
        if mode == 'v005':
            if l.startswith('|'):
                continue
            mode = None
        shas = re.findall(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])', l)
        if not shas:
            continue
        if l.startswith('**Target-free query manifest**'):
            m = re.search(r'`([^`]+\.json)`, `([0-9a-f]{64})`', l)
            if m:
                out.append(('query_manifest', expand(m.group(1)), m.group(2)))
            else:
                problems.append('unparsable sha line: %r' % l[:160])
            continue
        cells = split_cells(l)
        if cells is None:
            problems.append('unparsable sha line (not a strict table row): %r' % l[:160])
            continue
        hm = re.fullmatch(r'`([0-9a-f]{64})`(?: \([^()`]*\))?', cells[-1])
        if not hm:
            problems.append('row whose last cell is not a backticked sha256: %r' % l[:160])
            continue
        h = hm.group(1)
        first = cells[0]
        if re.fullmatch(r'0\d{3}', first):
            names = [n for n in os.listdir(DISPATCH_DIR) if n.startswith(first + '_')]
            if len(names) != 1:
                problems.append('dispatch %s: %d files' % (first, len(names)))
                continue
            out.append(('dispatch ' + first, DISPATCH_DIR + names[0], h))
        elif first[:4] in DECISIONS and first.startswith('V00'):
            p = CLAUDE2_DIR + DECISIONS[first[:4]]
            if first[:4] == 'V005' and v005_override:
                p = v005_override
            if first[:4] == 'V006' and v006_override:
                p = v006_override
            out.append(('decisions ' + first[:4], p, h))
        else:
            m = None
            for c in cells[:-1]:
                m = re.fullmatch(r'`([^`]+\.(?:py|json|md|npz|txt))`(?: \(.*\))?', c)
                if m:
                    break
            if not m:
                problems.append('unparsable source row: %r' % l[:160])
                continue
            p = m.group(1)
            if not p.startswith(('/', '…', '...', 'claude_artifacts/')):
                p = ART + p
            out.append((first, expand(p), h))
    return out, problems


# -------------------------------------------------------------------------------------------------------------------- T1-T3
def scan_terms(name, vs, pinned_basenames):
    hits = []
    for vn, t in vs.items():
        low = t.lower()
        hits += ['%s [%s]: term %r' % (name, vn, w) for w in DENY_TERMS if w in low]
        hits += ['%s [%s]: pattern %r' % (name, vn, m.group(0)) for r in DENY_RES for m in r.finditer(t)]
        if vn == 'skeleton':
            continue
        for m in DATA_EXT.finditer(t):
            s = m.start()
            while s > 0 and not t[s - 1].isspace() and t[s - 1] not in '`|()[]<>"\'':
                s -= 1
            e = m.end()
            while e < len(t) and not t[e].isspace() and t[e] not in '`|()[]<>"\',;':
                e += 1
            tok = t[s:e].rstrip('.')
            base = tok.rsplit('/', 1)[-1]
            if EXT_EXEMPT.match(base) or base in pinned_basenames:
                continue
            hits.append('%s [%s]: data-like file %r' % (name, vn, tok))
        for m in NGC_FILE.finditer(t):
            base = m.group(0).rsplit('/', 1)[-1]
            if base not in pinned_basenames:
                hits.append('%s [%s]: NGC3198-named file not pinned in §11: %r' % (name, vn, m.group(0)))
        hits += ['%s [%s]: URL %r' % (name, vn, m.group(0)) for m in URL.finditer(t)]
    raw_like = vs['normalized']
    hits += ['%s: HTML entity %r' % (name, m.group(0)) for m in ENTITY.finditer(raw_like)]
    hits += ['%s: HTML comment' % name for _ in COMMENT.finditer(raw_like)]
    bad = sorted({ch for ch in raw_like if ord(ch) > 127 and LETTER.match(ch) and ch not in ALLOWED_GREEK
                  and not unicodedata.name(ch, '').startswith('LATIN')})
    hits += ['%s: disallowed non-ASCII letter %r (U+%04X %s)' % (name, ch, ord(ch), unicodedata.name(ch, '?')) for ch in bad]
    return sorted(set(hits))


def scan_units(name, vs):
    out = []
    for vn in ('normalized', 'unmarked', 'skeleton'):
        out += ['%s [%s]: %r' % (name, vn, m.group(0)) for r in UNIT_RES for m in r.finditer(vs[vn])]
    return sorted(set(out))


_SYM_RE = re.compile(SYM, re.I)
_HAS_NUM = re.compile(r'(?<![A-Za-z])\d')


def table_symbol_hits(t):
    """Markdown tables (runs of lines starting with '|'): a header cell naming a target symbol over a column whose data cells
    hold a number, or a row whose first cell names a target symbol and whose other cells hold a number."""
    out = []
    block = []
    for l in t.split('\n') + ['']:
        if l.startswith('|'):
            block.append(l)
            continue
        if len(block) >= 2:
            rows = [re.split(r'(?<!\\)\|', b.strip())[1:-1] for b in block]
            head = rows[0]
            cols = [k for k, c in enumerate(head) if _SYM_RE.search(c)]
            for r in rows[1:]:
                if all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in r):
                    continue
                for k in cols:
                    if k < len(r) and _HAS_NUM.search(r[k]):
                        out.append('column %r: %r' % (head[k].strip(), r[k].strip()))
                if r and _SYM_RE.search(r[0]) and any(_HAS_NUM.search(c) for c in r[1:]):
                    out.append('row %r: %r' % (r[0].strip(), ' | '.join(c.strip() for c in r[1:])[:80]))
        block = []
    return out


def scan_symbols(name, vs):
    out = []
    for vn in ('normalized', 'unmarked', 'skeleton'):
        out += ['%s [%s]: %r' % (name, vn, ' '.join(m.group(0).split())) for m in T3_RE.finditer(vs[vn])]
        out += ['%s [%s]: value first %r' % (name, vn, ' '.join(m.group(0).split())) for m in T3_REV.finditer(vs[vn])]
        out += ['%s [%s]: table %s' % (name, vn, h) for h in table_symbol_hits(vs[vn])]
    return sorted(set(out))


# ------------------------------------------------------------------------------------------------------------------------ T4
def section_numbers(prereg):
    nums = set(re.findall(r'^#{2,4}\s+(\d+(?:\.\d+)*)\.?\s', prereg, re.M))
    nums |= set(re.findall(r'\[C-(\d+(?:\.\d+)*)\]', prereg))
    return nums


def build_corpus(source_texts):
    """Identifier chains and pieces (letters with digits), standalone numbers, and long-decimal floats in the pinned sources."""
    chains, pieces, numbers, floats = set(), set(), set(), []
    for t in source_texts:
        t = norm(t)
        for m in CHAIN.finditer(t):
            c = m.group(0)
            if LETTER.search(c) and re.search(r'\d', c) and not re.fullmatch(r'\d+(?:\.\d+)?[eE][-+]?\d+', c):
                chains.add(c)
                for p in re.split(r'[-._]', c) + re.split(r'[-_]', c):
                    if LETTER.search(p) and re.search(r'\d', p):
                        pieces.add(p)
        for m in NUM.finditer(t):
            tok = m.group(0)
            numbers.add(tok)
            if '.' in tok and len(tok.split('.')[1]) > 4:
                floats.append(float(tok))
    return chains, pieces, numbers, sorted(set(floats))


def located(tok, numbers, floats):
    if tok in numbers:
        return True
    if '.' in tok:
        dp = len(tok.split('.')[1])
        if dp >= 4:
            v = float(tok)
            lo, hi = v - 10 ** -dp, v + 10 ** -dp
            import bisect
            i = bisect.bisect_left(floats, lo)
            while i < len(floats) and floats[i] <= hi:
                if '%.*f' % (dp, floats[i]) == tok:
                    return True
                i += 1
    return False


def numeric_tokens(t, full_shas, sections, pinned_paths, corpus, declared):
    """[(token, position, origin)] of one normalized text, after position-preserving blanking."""
    chains, pieces = corpus[0], corpus[1]
    spans = [m.span() for m in HEX64.finditer(t)]
    spans += [m.span() for m in TAG.finditer(t)]
    spans += [m.span() for m in ISO.finditer(t)]
    spans += [m.span() for m in UPLUS.finditer(t)]
    spans += [m.span() for m in SECTION_REF.finditer(t) if m.group(1) in sections]
    for m in CODE_SPAN.finditer(t):
        c = m.group(1).strip()
        c2 = re.sub(r'^(?:…|\.\.\.)/', '', c)
        if c2 and ('/' in c2 or re.search(r'\.(?:py|json|md|npz|txt)$', c2)) and any(
                p == c2 or p.endswith('/' + c2.lstrip('/')) or p.endswith('/' + c2.rstrip('/')) or ('/' + c2.strip('/') + '/') in p
                for p in pinned_paths):
            spans.append(m.span())
    t = blank(t, spans)
    sp2 = []
    for m in HEX_RUN.finditer(t):
        r = m.group(0)
        tail = t[m.end():m.end() + 3]
        if any(h.startswith(r) for h in full_shas) and (re.search(r'[a-f]', r) or tail.startswith(('...', '…'))):
            sp2.append(m.span())
    t = blank(t, sp2)
    toks = []
    sp3 = []
    for rx, origin in ((NUM_SCI, 'scientific'), (HEX_LIT, 'hex literal')):
        for m in rx.finditer(t):
            toks.append((m.group(0), m.start(), origin))
            sp3.append(m.span())
    t = blank(t, sp3)
    sp4 = []
    for m in CHAIN.finditer(t):
        c = m.group(0)
        if not (LETTER.search(c) and re.search(r'\d', c)):
            continue
        sp4.append(m.span())
        if FAMILY.fullmatch(c) or c in chains or c in declared:
            continue
        pos = m.start()
        for pm in re.finditer(r'[^-_]+', c):                       # pieces between '-' and '_'
            p, ppos = pm.group(0), pos + pm.start()
            if not re.search(r'\d', p):
                continue
            if re.fullmatch(r'\d+(?:\.\d+)?', p):
                toks.append((p, ppos, 'identifier part of %r' % c))
                continue
            if PIECE.fullmatch(p) or FAMILY.fullmatch(p) or p in pieces or p in declared:
                continue
            for sm in re.finditer(r'[^.]+', p):                    # then between dots
                s = sm.group(0)
                if not re.search(r'\d', s):
                    continue
                if s.isdigit():
                    toks.append((s, ppos + sm.start(), 'identifier part of %r' % c))
                elif not (PIECE.fullmatch(s) or FAMILY.fullmatch(s) or s in pieces or s in declared):
                    for dm in DIGITS.finditer(s):
                        toks.append((dm.group(0), ppos + sm.start() + dm.start(), 'digits glued in %r' % c))
    t = blank(t, sp4)
    for m in NUM_T4.finditer(t):
        raw_tok = m.group(1)
        tok = canon_num(raw_tok)
        toks.append((tok, m.start(1), 'number' if tok == raw_tok else 'number written %r' % raw_tok))
    return toks


def tok_key(x):
    try:
        return (0, float(x), x)
    except ValueError:
        try:
            return (1, float(int(x, 16)), x)
        except ValueError:
            return (2, 0.0, x)


def verify_category(tok, entry, rad, node_kpc, corpus, posts):
    cat = entry.get('category')
    if cat not in CATEGORIES:
        return 'category %r is not in the closed list' % cat
    if not isinstance(entry.get('uses'), list) or not entry['uses'] or not all(isinstance(u, str) and u for u in entry['uses']):
        return 'uses must be a non-empty list of strings'
    if cat == 'QUERY_RADIUS':
        ids = entry.get('query_ids', [])
        if not ids or any(rad.get(q) != tok for q in ids):
            return 'claimed %s, slots give %s' % (ids, [rad.get(q) for q in ids])
    elif cat == 'NODE_RADIUS':
        idx = entry.get('node_index')
        dp = len(tok.split('.')[1]) if '.' in tok else 0
        if not isinstance(idx, int) or not (0 <= idx < len(node_kpc)) or ('%.*f' % (dp, node_kpc[idx])) != tok:
            return 'node %r does not round to it' % (idx,)
    elif cat == 'NODE_DERIVED':
        dp = len(tok.split('.')[1]) if '.' in tok else 0
        f = entry.get('formula')
        try:
            if f is None:
                m = re.search(r'midpoint of nodes (\d+) and (\d+)', ' '.join(entry['uses']))
                if not m:
                    return 'NODE_DERIVED needs a formula (midpoint, query_minus_node, node_minus_query)'
                a, b = int(m.group(1)), int(m.group(2))
                val = (node_kpc[a] + node_kpc[b]) / 2
            elif f == 'midpoint':
                a, b = entry['node_indices']
                val = (node_kpc[a] + node_kpc[b]) / 2
            elif f in ('query_minus_node', 'node_minus_query'):
                q, k = entry['query_id'], entry['node_index']
                val = float(rad[q]) - node_kpc[k]
                val = val if f == 'query_minus_node' else -val
            else:
                return 'unknown NODE_DERIVED formula %r' % f
        except (KeyError, IndexError, TypeError, ValueError) as e:
            return 'NODE_DERIVED formula inputs invalid: %s' % e
        if '%.*f' % (dp, val) != tok:
            return 'formula gives %s' % ('%.*f' % (dp, val))
    elif cat in LOCATED:
        if not located(tok, corpus[2], corpus[3]):
            return 'not located as a number in any pinned source'
    elif cat == 'HEADING_OR_ITEM_NUMBER':
        if not re.fullmatch(r'\d{1,2}(?:\.\d{1,2})?', tok):
            return 'not a section or item number shape'
    elif cat == 'INDEX':
        if not re.fullmatch(r'\d{1,2}', tok):
            return 'not an index 0-99'
    elif cat == 'REVIEW_COUNT':
        if not re.fullmatch(r'\d{1,3}', tok):
            return 'not an integer below 1000'
    elif cat == 'DISPATCH_OR_POST_NUMBER':
        if not re.fullmatch(r'0\d{3}', tok) or tok not in posts:
            return 'no exchange message numbered %s' % tok
    return None


def exchange_numbers():
    nums = set()
    for box in OUTBOXES:
        d = EXCHANGE + box
        if path_denied(d) or not os.path.isdir(d):
            continue
        for n in os.listdir(d):
            m = re.match(r'(0\d{3})_', n)
            if m:
                nums.add(m.group(1))
    return nums


# ----------------------------------------------------------------------------------------------------------------------- run
def run(a):
    res = {'schema': SCHEMA, 'checks': {}, 'files': {}, 'limits': LIMITS}
    v005_override = getattr(a, 'v005', None)
    raw, texts = {}, {}
    for name in TEXT_FILES:
        p = os.path.join(a.dir, name)
        with open(p, 'rb') as f:
            raw[name] = f.read().decode('utf-8')
        texts[name] = norm(raw[name])
        res['files'][name] = sha(p)
    aux = {}
    for name in AUX_FILES:
        p = os.path.join(a.dir, name)
        if os.path.isfile(p):
            with open(p, 'rb') as f:
                aux[name] = f.read().decode('utf-8')
            res['files'][name] = sha(p)
    prereg = raw[PREREG]

    # §11 sources, V005 and V006 bytes and their entry tables (shared by T1, T4, T5, T7)
    v006_override = getattr(a, 'v006', None)
    srcs, src_problems = parse_sources(prereg, v005_override, v006_override)
    rows, legacy, table_problems, table_spans = parse_v005_tables(prereg)
    rows6, table6_problems, table6_spans, n6_header = parse_v006_table(prereg)
    pinned_paths = [p for _, p, _ in srcs]
    pinned_basenames = {os.path.basename(p) for p in pinned_paths}
    v005_path = v005_override or V005_PATH
    v005_text = None
    if not path_denied(v005_path) and os.path.isfile(v005_path):
        with open(v005_path, 'rb') as f:
            v005_bytes = f.read()
        v005_text = v005_bytes.decode('utf-8')
    heads = v005_headings(v005_text) if v005_text is not None else []
    v005_ids = {h[2] for h in heads}
    v006_path = v006_override or V006_PATH
    v006_text, v006_bytes = None, None
    if not path_denied(v006_path) and os.path.isfile(v006_path):
        with open(v006_path, 'rb') as f:
            v006_bytes = f.read()
        v006_text = v006_bytes.decode('utf-8')
    secs6 = v006_sections(v006_text) if v006_text is not None else []
    prereg_sha = res['files'][PREREG]
    cut6 = next((k for k, s in enumerate(secs6) if prereg_sha in s[2]), None)      # this text's seal entry, if written
    covered6 = secs6[:cut6] if cut6 is not None else secs6
    v006_ids = {s[1] for s in covered6}

    # T1
    hits = []
    allowed = set(TEXT_FILES) | set(AUX_FILES) | set(OUTPUT_FILES) | {'tools'}
    for n in sorted(os.listdir(a.dir)):
        if n not in allowed:
            hits.append('unexpected file in the bundle: %r' % n)
            q = os.path.join(a.dir, n)
            if path_denied(q):
                hits.append('unexpected bundle file %r has a target-like name (not opened)' % n)
            elif os.path.isfile(q):
                try:
                    with open(q, 'rb') as f:
                        extra = f.read().decode('utf-8')
                    hits += scan_terms(n, variants(extra), pinned_basenames)
                except UnicodeDecodeError:
                    hits.append('unexpected file %r is not UTF-8 text' % n)
    td = os.path.join(a.dir, 'tools')
    if os.path.isdir(td):
        extra_tools = sorted(set(os.listdir(td)) - set(TOOL_FILES))
        hits += ['unexpected file in tools/: %r' % n for n in extra_tools]
    scanned = dict(raw)
    scanned.update(aux)
    vs = {n: variants(t) for n, t in scanned.items()}
    for n in scanned:
        hits += scan_terms(n, vs[n], pinned_basenames)
    res['checks']['T1_FORBIDDEN_TERMS'] = {'pass': not hits, 'hits': hits, 'files_scanned': sorted(scanned)}

    # T2, T3
    unit_hits = [h for n in scanned for h in scan_units(n, vs[n])]
    res['checks']['T2_NO_VELOCITY_UNIT'] = {'pass': not unit_hits, 'hits': unit_hits, 'files_scanned': sorted(scanned)}
    sym_hits = [h for n in scanned for h in scan_symbols(n, vs[n])]
    res['checks']['T3_NO_TARGET_SYMBOL_VALUE'] = {'pass': not sym_hits, 'hits': sym_hits, 'files_scanned': sorted(scanned)}

    # source bytes (read once, after the deny test) for T4's corpus and T5
    src_bytes, src_status = {}, []
    for label, p, h in srcs:
        if path_denied(p) or any(w in p.lower() for w in DENY_TERMS) or any(r.search(p) for r in DENY_RES) or (
                DATA_EXT.search(p) and not EXT_EXEMPT.match(os.path.basename(p))):
            src_status.append((label, p, h, 'target-like or protected path (not opened)'))
            continue
        if not os.path.isfile(p):
            src_status.append((label, p, h, 'missing'))
            continue
        with open(p, 'rb') as f:
            src_bytes[p] = f.read()
        src_status.append((label, p, h, None))
    corpus_texts = []
    for p, b in src_bytes.items():
        if p.endswith('.npz'):
            continue
        try:
            corpus_texts.append(b.decode('utf-8'))
        except UnicodeDecodeError:
            pass
    if v005_text is not None:
        corpus_texts.append(v005_text)
    if v006_text is not None:
        corpus_texts.append(v006_text)
    corpus = build_corpus(corpus_texts)

    # T4
    prov = strict_load(a.provenance)
    slots_sha, nodes_sha = sha(a.slots), sha(a.nodes)
    slots = strict_load(a.slots)
    nodes = strict_load(a.nodes)
    rad = {r['query_id']: r['Rad_text'] for r in slots['query_block']['rows']}
    units = {r['Rad_unit'] for r in slots['query_block']['rows']}
    node_kpc = nodes['orders']['4']['radii_kpc']
    full_shas = set()
    for t in texts.values():
        full_shas |= set(HEX64.findall(t))
    for t in corpus_texts:
        full_shas |= set(HEX64.findall(t))
    sections = section_numbers(prereg)
    declared = prov.get('identifiers', {}) if isinstance(prov.get('identifiers', {}), dict) else {}
    # a heading cell that equals its V005 heading line verbatim is a verified quote of pinned bytes: it is blanked on the raw
    # prereg (before NFKC) and so never enters the number scan; every other cell, the reasons included, is scanned
    v005_heading_text = {h[2]: h[1][3:] for h in heads}
    heading_spans = [r['heading_span'] for r in rows
                     if r['disposition'] in DISPOSITIONS and v005_heading_text.get(r['entry']) == r['heading']]
    v006_heading_text = {s[1]: s[0][3:] for s in secs6}
    heading_spans += [r['heading_span'] for r in rows6 if v006_heading_text.get(r['entry']) == r['heading']]
    t4_texts = dict(texts)
    t4_texts[PREREG] = norm(blank(raw[PREREG], heading_spans))
    # the hand-written JSON notes are prose that no table renders: their numbers are value-checked too (fix stage, TF-S2)
    for jn in (ETAB, ETAB6, PROV):
        if jn in aux:
            try:
                jd = json.loads(aux[jn])
            except ValueError:
                continue
            if isinstance(jd, dict) and isinstance(jd.get('note'), str) and jd['note']:
                t4_texts[jn + ' note'] = norm(jd['note'])
    res['checks_info'] = {'t4_heading_cells_blanked': len(heading_spans),
                          't4_json_notes_scanned': sorted(k for k in t4_texts if k.endswith(' note'))}
    allc, origins = {}, {}
    used_declared = set()
    for name, t in t4_texts.items():
        for tok, pos, origin in numeric_tokens(t, full_shas, sections, pinned_paths, corpus, declared):
            ctx = t[max(0, pos - 45):pos + len(tok) + 45]
            allc.setdefault(tok, []).append('%s: …%s…' % (name, ' '.join(ctx.split())))
            if origin != 'number':
                origins.setdefault(tok, set()).add(origin)
        for d in declared:
            if d in t:
                used_declared.add(d)
    toks = sorted(allc, key=tok_key)
    listed = prov.get('numbers', {})
    missing = [x for x in toks if x not in listed]
    unused = [k for k in listed if k not in allc]
    posts = exchange_numbers()
    bad_cat, radius_bad = [], []
    for k, v in listed.items():
        if not isinstance(v, dict):
            bad_cat.append('%s: entry is not an object' % k)
            continue
        why = verify_category(k, v, rad, node_kpc, corpus, posts)
        if why:
            (radius_bad if v.get('category') in ('QUERY_RADIUS', 'NODE_RADIUS', 'NODE_DERIVED') else bad_cat).append('%s: %s' % (k, why))
    undeclared_cats = sorted(set(prov.get('categories', {})) - set(CATEGORIES))
    markup = ['%s: %r' % (n, m.group(0)) for n, t in t4_texts.items() for m in MARKUP_DIGITS.finditer(t)]
    nonascii_digits = ['%s: %r' % (n, ch) for n, t in raw.items() for ch in sorted(set(t)) if ch.isdigit() and ord(ch) > 127]
    words = ['%s: %r' % (n, m.group(0)) for n, t in t4_texts.items() for m in NUMBER_WORDS.finditer(t)]
    bad_decl = sorted(d for d in declared if not (LETTER.search(d) and re.search(r'\d', d)) or d not in used_declared)
    t4 = (not missing and not unused and not bad_cat and not radius_bad and not undeclared_cats and not markup
          and not nonascii_digits and not words and not bad_decl and slots_sha == a.expect_slots_sha
          and nodes_sha == a.expect_nodes_sha and units == {'kpc'})
    res['checks']['T4_NUMBER_PROVENANCE'] = {
        'pass': t4, 'numeric_tokens': toks, 'missing_from_provenance': missing, 'listed_but_absent': unused,
        'bad_category': bad_cat, 'radius_mismatch': radius_bad, 'categories_not_in_closed_list': undeclared_cats,
        'markup_between_digits': markup, 'non_ascii_digits': nonascii_digits, 'number_words': words,
        'declared_identifiers_unused_or_invalid': bad_decl, 'declared_identifiers': sorted(declared),
        'token_origins_other_than_plain_number': {k: sorted(v) for k, v in sorted(origins.items(), key=lambda kv: tok_key(kv[0]))},
        'closed_category_list': CATEGORIES, 'slots_sha256': slots_sha, 'nodes_sha256': nodes_sha, 'rad_units': sorted(units)}
    res['census'] = {k: allc[k] for k in toks}

    # T5
    bad, notes, entry_results = list(src_problems), [], []
    bad += table_problems
    for label, p, h, why in src_status:
        if why:
            bad.append('%s: %s %s' % (label, why, p))
            continue
        got = sha_bytes(src_bytes[p])
        if label in OPEN_ADDENDA:
            if got != h:
                notes.append('%s whole-file sha is now %s (stated %s at assembly): see T7' % (label[-4:], got, h))
            continue
        if got != h:
            bad.append('%s: %s sha %s, stated %s' % (label, p, got, h))
    if not any(l == 'decisions V005' for l, _, _ in srcs):
        bad.append('no V005 row in §11')
    if v005_text is None:
        bad.append('V005 bytes not readable at %s' % v005_path)
    head_index = {}
    for i, l, e in heads:
        head_index.setdefault(e, []).append(i)
    pinned, by_table = {}, {}          # entry -> its pin (the entry table's preferred); (table, entry) -> pin
    for tname, trows in (('entry table', rows), ('legacy', legacy)):
        for r in trows:
            if r['disposition'] != 'CITED_PINNED' or v005_text is None:
                continue
            ent = r['entry']
            idx = head_index.get(ent, [])
            if len(idx) != 1:
                bad.append('V005 %s: %d headings with this entry id' % (ent, len(idx)))
                continue
            mk = r['marker']
            if mk and END_MARKER_ALLOW.get(ent) != mk:
                bad.append('V005 %s: end-marker %r is not allow-listed (allowed: %s)' % (ent, mk, END_MARKER_ALLOW))
                continue
            main, tail, prob = entry_parts(v005_text, idx[0], mk)
            if prob:
                bad.append('V005 %s: %s' % (ent, prob))
                continue
            cur = sha_bytes(main.encode('utf-8'))
            entry_results.append({'entry': ent, 'table': tname, 'ends_before': mk or NEXT_HEADING,
                                  'stated': r['sha'], 'current': cur, 'match': cur == r['sha']})
            if cur != r['sha']:
                bad.append('V005 %s section changed: %s, stated %s' % (ent, cur, r['sha']))
            pin = {'sha': r['sha'], 'marker': mk, 'tail': tail}
            if (tname, ent) in by_table:
                bad.append('V005 %s: two CITED_PINNED rows in the %s' % (ent, tname))
            by_table[(tname, ent)] = pin
            if ent in pinned and (pinned[ent]['sha'] != r['sha'] or pinned[ent]['marker'] != mk):
                bad.append('V005 %s: the entry table and the legacy pin table disagree' % ent)
            pinned.setdefault(ent, pin)
    tails = {}
    for tname, trows in (('entry table', rows), ('legacy', legacy)):
        for r in trows:
            if r['disposition'] != 'TAIL_PINNED':
                continue
            base = r['entry'][:-len(TAIL_SUFFIX)] if r['entry'].endswith(TAIL_SUFFIX) else None
            pin = by_table.get((tname, base))
            if base is None or pin is None or not pin['marker']:
                bad.append('tail row %r in the %s has no CITED_PINNED row with an end-marker there' % (r['entry'], tname))
                continue
            if r['marker'] not in ('', pin['marker']):
                bad.append('tail row %r: marker %r differs from the entry\'s %r' % (r['entry'], r['marker'], pin['marker']))
            cur = sha_bytes(pin['tail'].encode('utf-8')) if pin['tail'] is not None else None
            entry_results.append({'entry': r['entry'], 'table': tname, 'stated': r['sha'], 'current': cur, 'match': cur == r['sha']})
            if cur != r['sha']:
                bad.append('V005 %s changed: %s, stated %s' % (r['entry'], cur, r['sha']))
            if (tname, base) in tails:
                bad.append('V005 %s: two tail rows in the %s' % (r['entry'], tname))
            tails[(tname, base)] = r['sha']
    for (tname, ent), pin in by_table.items():
        if pin['marker'] and (tname, ent) not in tails:
            bad.append('V005 %s: the bytes after its end-marker %r are not pinned by a tail row in the %s' % (ent, pin['marker'], tname))
    etab_disp = {r['entry']: r['disposition'] for r in rows}
    for r in legacy:
        if r['disposition'] == 'CITED_PINNED' and etab_disp.get(r['entry']) != 'CITED_PINNED':
            bad.append('V005 %s has a legacy pin row but is %s in the entry table' % (r['entry'], etab_disp.get(r['entry'], 'absent')))
    if not pinned:
        bad.append('no CITED_PINNED V005 entry found in §11')
    excl = {PREREG: table_spans + table6_spans}
    cited = cited_v005({n: raw[n] for n in TEXT_FILES}, v005_ids, excl)
    unpinned = sorted(set(cited) - set(pinned), key=lambda e: (int(re.sub(r'\D', '', e) or 0), e))
    for ent in unpinned:
        bad.append('V005 %s is cited but not CITED_PINNED: %s' % (ent, cited[ent][0]))
    # V006 (fix stage, RF-B1/TF-B1): CITED_PINNED V006 rows hash as pinned (trimmed sections); every V006 entry the texts
    # cite, before this text's seal entry, is CITED_PINNED in the V006 table
    bad += table6_problems
    if v006_text is not None and not any(l == 'decisions V006' for l, _, _ in srcs):
        bad.append('a V006 addendum exists but §11 has no V006 row')
    sec6_by_id = {}
    for s in covered6:
        sec6_by_id.setdefault(s[1], []).append(s)
    pinned6 = {}
    for r in rows6:
        if r['disposition'] != 'CITED_PINNED':
            continue
        ss = sec6_by_id.get(r['entry'], [])
        if len(ss) != 1:
            bad.append('V006 %s: %d headings with this entry id before the seal entry' % (r['entry'], len(ss)))
            continue
        cur = trimmed_sha(ss[0][2])
        entry_results.append({'entry': r['entry'], 'table': 'V006 entry table', 'ends_before': NEXT_HEADING,
                              'stated': r['sha'], 'current': cur, 'match': cur == r['sha']})
        if cur != r['sha']:
            bad.append('V006 %s section changed: %s, stated %s' % (r['entry'], cur, r['sha']))
        pinned6[r['entry']] = r['sha']
    cited6 = cited_v005({n: raw[n] for n in TEXT_FILES}, v006_ids, excl)
    for ent in sorted(set(cited6) - set(pinned6), key=lambda e: (int(re.sub(r'\D', '', e) or 0), e)):
        bad.append('V006 %s is cited but not CITED_PINNED: %s' % (ent, cited6[ent][0]))
    m6 = re.search(r'The cited entries are ((?:A\d{1,3}[a-z]?)(?:(?:, |,? and )A\d{1,3}[a-z]?)*)\.', raw[ROOT])
    m6_list = sorted(set(re.findall(r'A\d{1,3}[a-z]?', m6.group(1))), key=lambda e: int(re.sub(r'\D', '', e))) if m6 else None
    if m6_list is not None and set(m6_list) != set(pinned):
        bad.append('ROOT_ITEMS seal list "The cited entries are ..." %s differs from the CITED_PINNED set %s' % (
            m6_list, sorted(pinned, key=lambda e: int(re.sub(r'\D', '', e) or 0))))
    res['checks']['T5_SOURCES_TARGET_FREE_AND_PINNED'] = {
        'pass': not bad and len(srcs) >= 1, 'n_sources': len(srcs), 'problems': bad, 'notes': notes, 'v005_entries': entry_results,
        'cited_v005_entries': sorted(cited, key=lambda e: (int(re.sub(r'\D', '', e) or 0), e)),
        'pinned_v005_entries': sorted(pinned, key=lambda e: (int(re.sub(r'\D', '', e) or 0), e)),
        'pinned_not_cited': sorted(set(pinned) - set(cited)), 'root_items_seal_list': m6_list,
        'v005_bytes': {'path': v005_path, 'override': bool(v005_override)},
        'cited_v006_entries': sorted(cited6), 'pinned_v006_entries': sorted(pinned6),
        'v006_bytes': {'path': v006_path, 'override': bool(v006_override), 'exists': v006_text is not None},
        'sources': [{'label': l, 'path': p, 'sha256': h} for l, p, h in srcs]}

    # T6
    tags = TAG.findall(prereg)
    dup_text = sorted({t for t in tags if tags.count(t) > 1})
    maprows = re.findall(r'^\| (C-[A-Za-z0-9.]+) \|', raw[CSM], re.M)
    dup_map = sorted({r for r in maprows if maprows.count(r) > 1})
    no_row = sorted(set(tags) - set(maprows))
    no_tag = sorted(set(maprows) - set(tags))
    res['checks']['T6_CLAUSE_TAGS_MAPPED'] = {'pass': not (dup_text or dup_map or no_row or no_tag), 'n_tags': len(set(tags)),
                                              'duplicate_in_text': dup_text, 'duplicate_in_map': dup_map,
                                              'tag_without_map_row': no_row, 'map_row_without_tag': no_tag}

    # T7 (currency)
    cur_problems, cur_notes = [], []
    stated_v005 = [h for l, _, h in srcs if l == 'decisions V005']
    if v005_text is None:
        cur_problems.append('V005 bytes not readable')
    else:
        whole = sha_bytes(v005_bytes)
        if not stated_v005 or stated_v005[0] != whole:
            cur_problems.append('V005 whole-file sha %s differs from the sha read at assembly %s: the file changed since the entry '
                                'table was read' % (whole, stated_v005[0] if stated_v005 else None))
        etab_heads = [r for r in rows if r['disposition'] in DISPOSITIONS]
        file_ids = [h[2] for h in heads]
        table_ids = [r['entry'] for r in etab_heads]
        for e in sorted(set(file_ids)):
            if file_ids.count(e) > 1:
                cur_problems.append('V005 has %d headings with entry id %r' % (file_ids.count(e), e))
        for e in sorted(set(table_ids)):
            if table_ids.count(e) != 1:
                cur_problems.append('entry %r has %d rows in the entry table (exactly one required)' % (e, table_ids.count(e)))
        for i, l, e in heads:
            if e not in table_ids:
                cur_problems.append('V005 heading not in the entry table: %r' % l[:160])
        for r in etab_heads:
            if r['entry'] not in v005_ids:
                cur_problems.append('entry-table row %r matches no V005 heading' % r['entry'])
        if [x for x in table_ids if x in v005_ids] != [x for x in file_ids if x in table_ids]:
            cur_problems.append('the entry table is not in V005 file order')
        for r in etab_heads:
            idx = head_index.get(r['entry'], [])
            if len(idx) != 1:
                continue
            line = v005_text.split('\n')[idx[0]]
            if line[3:] != r['heading']:
                cur_problems.append('entry %r: heading cell differs from the V005 heading line' % r['entry'])
            if r['disposition'] == 'NO_CHANGE':
                if r['marker']:
                    cur_problems.append('NO_CHANGE entry %r has an end-marker' % r['entry'])
                    continue
                main, _, _ = entry_parts(v005_text, idx[0], '')
                cur = sha_bytes(main.encode('utf-8'))
                if cur != r['sha']:
                    cur_problems.append('NO_CHANGE entry %r changed since it was read: %s, read %s' % (r['entry'], cur, r['sha']))
            else:
                if r['marker'] and END_MARKER_ALLOW.get(r['entry']) != r['marker']:
                    cur_problems.append('entry %r: end-marker not allow-listed' % r['entry'])
                    continue
                main, _, prob = entry_parts(v005_text, idx[0], r['marker'])
                if prob or sha_bytes(main.encode('utf-8')) != r['sha']:
                    cur_problems.append('CITED_PINNED entry %r changed: %s' % (r['entry'], prob or 'section sha differs'))
        for r in rows:
            if r['disposition'] == 'TAIL_PINNED':
                base = r['entry'][:-len(TAIL_SUFFIX)]
                if base in pinned and pinned[base]['tail'] is not None and sha_bytes(pinned[base]['tail'].encode('utf-8')) != r['sha']:
                    cur_problems.append('tail %r changed' % r['entry'])
        like = [l for l in v005_text.split('\n') if re.match(r'^\s{0,3}(?:#{1,6}\s*|\*\*)\s*(?:entry\s+)?[Aa]\s?\d', l) and not l.startswith('## ')]
        if like:
            cur_notes.append('heading-like lines that are not "## " headings (covered by the whole-file sha): %s' % [x[:80] for x in like])
    if ETAB not in aux:
        cur_problems.append('%s is not in the bundle' % ETAB)
    else:
        try:
            et = json.loads(aux[ETAB], object_pairs_hook=lambda pairs: _no_dup(pairs, ETAB))
            jp = check_entry_table_json(et, rows, stated_v005[0] if stated_v005 else None)
            cur_problems += jp
        except ValueError as e:
            cur_problems.append('%s: %s' % (ETAB, e))
    # V006 (fix stage, RF-B1/TF-B1): "a V006 exists" is no longer a failure; every V006 heading before this text's seal entry
    # must be covered by the hand-written V006 table, read from bytes that have not changed since
    stated_v006 = [h for l, _, h in srcs if l == 'decisions V006']
    et6 = None
    if ETAB6 in aux:
        try:
            et6 = json.loads(aux[ETAB6], object_pairs_hook=lambda pairs: _no_dup(pairs, ETAB6))
        except ValueError as e:
            cur_problems.append('%s: %s' % (ETAB6, e))
    if v006_text is None:
        if rows6 or (isinstance(et6, dict) and et6.get('entries')):
            cur_problems.append('the V006 entry table has rows, but no V006 bytes are readable at %s' % v006_path)
    else:
        if et6 is None:
            cur_problems += ['V006 heading not covered (no %s in the bundle): %r' % (ETAB6, s[0][:160]) for s in covered6]
            if not covered6:
                cur_problems.append('%s is not in the bundle' % ETAB6)
        else:
            cur_problems += check_entry_table6_json(et6, rows6, stated_v006[0] if stated_v006 else None)
            if n6_header != 1:
                cur_problems.append('the V006 entry table header must occur exactly once in §11 (found %d)' % n6_header)
            file6 = [s[1] for s in covered6]
            tab6 = [r['entry'] for r in rows6]
            for e in sorted(set(file6)):
                if file6.count(e) > 1:
                    cur_problems.append('V006 has %d headings with entry id %r before the seal entry' % (file6.count(e), e))
            for e in sorted(set(tab6)):
                if tab6.count(e) != 1:
                    cur_problems.append('V006 entry %r has %d rows in the V006 table (exactly one required)' % (e, tab6.count(e)))
            for s in covered6:
                if s[1] not in tab6:
                    cur_problems.append('V006 heading not covered: %r' % s[0][:160])
            for r in rows6:
                if r['entry'] not in file6:
                    cur_problems.append('V006 table row %r matches no V006 heading before the seal entry' % r['entry'])
            if [x for x in tab6 if x in file6] != [x for x in file6 if x in tab6]:
                cur_problems.append('the V006 table is not in V006 file order')
            for r in rows6:
                ss = sec6_by_id.get(r['entry'], [])
                if len(ss) != 1:
                    continue
                if ss[0][0][3:] != r['heading']:
                    cur_problems.append('V006 entry %r: heading cell differs from the V006 heading line' % r['entry'])
                if trimmed_sha(ss[0][2]) != r['sha']:
                    cur_problems.append('%s V006 entry %r changed since it was read: %s, read %s' % (
                        r['disposition'], r['entry'], trimmed_sha(ss[0][2]), r['sha']))
            if cut6 is None:
                if not stated_v006 or sha_bytes(v006_bytes) != stated_v006[0]:
                    cur_problems.append('V006 whole-file sha %s differs from the sha read at assembly %s: the file changed since the '
                                        'V006 table was read' % (sha_bytes(v006_bytes), stated_v006[0] if stated_v006 else None))
            else:
                prefix = v006_bytes[:len(v006_text[:secs6[cut6][3]].encode('utf-8'))]
                if trimmed_sha(prefix) != (et6.get('v006_trimmed_sha256') if isinstance(et6, dict) else None):
                    cur_problems.append('the V006 bytes before the seal entry, trimmed, hash %s, not the trimmed sha read at assembly %s'
                                        % (trimmed_sha(prefix), et6.get('v006_trimmed_sha256') if isinstance(et6, dict) else None))
                cur_notes.append('V006 seal entry found: %r; it and %d later heading(s) lie outside the V006 table' % (
                    secs6[cut6][0][:120], len(secs6) - cut6 - 1))
        like6 = [l for l in v006_text.split('\n') if re.match(r'^\s{0,3}(?:#{1,6}\s*|\*\*)\s*(?:entry\s+)?[Aa]\s?\d', l)
                 and not l.startswith('## ')]
        if like6:
            cur_notes.append('V006 heading-like lines that are not "## " headings (covered by the whole-file or prefix sha): %s'
                             % [x[:80] for x in like6])
    res['checks']['T7_V005_CURRENCY'] = {
        'pass': not cur_problems, 'problems': cur_problems, 'notes': cur_notes,
        'n_v005_headings': len(heads), 'v005_bytes': {'path': v005_path, 'override': bool(v005_override)},
        'n_v006_headings': len(secs6), 'n_v006_headings_covered': len(covered6), 'v006_seal_entry_found': cut6 is not None,
        'v006_bytes': {'path': v006_path, 'override': bool(v006_override), 'exists': v006_text is not None},
        'note': ('currency only (the key name is kept from r3; it covers V005 and V006): a FAIL means an addendum changed after '
                 'its entry table was read, or a table does not cover it')}
    tf = [k for k in res['checks'] if k != 'T7_V005_CURRENCY']
    res['verdict_target_free'] = 'PASS' if all(res['checks'][k]['pass'] for k in tf) else 'FAIL'
    res['verdict_currency'] = 'PASS' if res['checks']['T7_V005_CURRENCY']['pass'] else 'FAIL'
    res['verdict'] = res['verdict_target_free']
    return res


def _no_dup(pairs, name):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('duplicate key %r' % k)
        d[k] = v
    return d


ETAB_FIELDS = {'entry', 'heading', 'disposition', 'reason', 'section_sha256', 'end_marker', 'tail_sha256', 'tail_reason'}


def norm_marker(m):
    """end_marker as in the r2 pin rows: absent, '', 'next heading' or '—' mean the next '## ' heading; otherwise the marker
    text, optionally in backticks. None when the field is not a string."""
    if m is None:
        return ''
    if not isinstance(m, str):
        return None
    m = m.strip()
    if m in ('', NEXT_HEADING, '—', '-'):
        return ''
    if len(m) > 2 and m.startswith('`') and m.endswith('`'):
        m = m[1:-1]
    return m


def check_entry_table_json(et, rows, stated_sha):
    """Problems where the entry-table JSON and the rendered table disagree."""
    p = []
    if not isinstance(et, dict) or et.get('schema') != ETAB_SCHEMA:
        return ['entry-table JSON schema is not %s' % ETAB_SCHEMA]
    if set(et) - {'schema', 'v005_sha256_read', 'read_utc', 'entries', 'note'}:
        p.append('entry-table JSON has unknown top-level fields %s' % sorted(set(et) - {'schema', 'v005_sha256_read', 'read_utc', 'entries', 'note'}))
    if et.get('v005_sha256_read') != stated_sha:
        p.append('entry-table JSON v005_sha256_read %s differs from the §11 V005 sha %s' % (et.get('v005_sha256_read'), stated_sha))
    if not isinstance(et.get('read_utc'), str) or not re.fullmatch(r'20\d\d-\d\d-\d\dT\d\d:\d\d(?::\d\d)?Z', et.get('read_utc', '')):
        p.append('entry-table JSON read_utc is not an ISO UTC time')
    ents = et.get('entries')
    if not isinstance(ents, list):
        return p + ['entry-table JSON entries is not a list']
    heads = [r for r in rows if r['disposition'] in DISPOSITIONS]
    if len(ents) != len(heads):
        p.append('entry-table JSON has %d entries, the rendered table %d' % (len(ents), len(heads)))
    for j, (e, r) in enumerate(zip(ents, heads)):
        if not isinstance(e, dict) or set(e) - ETAB_FIELDS:
            p.append('JSON entry %d has unknown fields' % j)
            continue
        h = e.get('heading', '')
        h = h[3:] if isinstance(h, str) and h.startswith('## ') else h
        if (e.get('entry'), h, e.get('disposition'), e.get('reason')) != (r['entry'], r['heading'], r['disposition'], r['reason']):
            p.append('JSON entry %d (%r) differs from rendered row %r' % (j, e.get('entry'), r['entry']))
        if e.get('disposition') == 'CITED_PINNED':
            if e.get('section_sha256') != r['sha'] or norm_marker(e.get('end_marker')) != r['marker']:
                p.append('JSON entry %r: section_sha256 or end_marker differs from the rendered pin' % e.get('entry'))
        elif e.get('section_sha256') or norm_marker(e.get('end_marker')) or e.get('tail_sha256') or e.get('tail_reason'):
            p.append('JSON NO_CHANGE entry %r carries pin fields' % e.get('entry'))
    return p


ETAB6_TOP = {'schema', 'v006_sha256_read', 'v006_trimmed_sha256', 'read_utc', 'entries', 'note'}
ETAB6_FIELDS = {'entry', 'heading', 'disposition', 'reason', 'section_sha256', 'end_marker'}


def check_entry_table6_json(et, rows6, stated_sha):
    """Problems where the V006 entry-table JSON and the rendered V006 table disagree (fix stage, RF-B1/TF-B1)."""
    p = []
    if not isinstance(et, dict) or et.get('schema') != ETAB6_SCHEMA:
        return ['V006 entry-table JSON schema is not %s' % ETAB6_SCHEMA]
    if set(et) - ETAB6_TOP:
        p.append('V006 entry-table JSON has unknown top-level fields %s' % sorted(set(et) - ETAB6_TOP))
    if et.get('v006_sha256_read') != stated_sha:
        p.append('V006 entry-table JSON v006_sha256_read %s differs from the §11 V006 sha %s' % (et.get('v006_sha256_read'), stated_sha))
    if not isinstance(et.get('v006_trimmed_sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', et.get('v006_trimmed_sha256', '')):
        p.append('V006 entry-table JSON v006_trimmed_sha256 is not a sha256')
    if not isinstance(et.get('read_utc'), str) or not re.fullmatch(r'20\d\d-\d\d-\d\dT\d\d:\d\d(?::\d\d)?Z', et.get('read_utc', '')):
        p.append('V006 entry-table JSON read_utc is not an ISO UTC time')
    ents = et.get('entries')
    if not isinstance(ents, list):
        return p + ['V006 entry-table JSON entries is not a list']
    if len(ents) != len(rows6):
        p.append('V006 entry-table JSON has %d entries, the rendered V006 table %d' % (len(ents), len(rows6)))
    for j, (e, r) in enumerate(zip(ents, rows6)):
        if not isinstance(e, dict) or set(e) - ETAB6_FIELDS:
            p.append('V006 JSON entry %d has unknown fields' % j)
            continue
        h = e.get('heading', '')
        h = h[3:] if isinstance(h, str) and h.startswith('## ') else h
        if (e.get('entry'), h, e.get('disposition'), e.get('reason')) != (r['entry'], r['heading'], r['disposition'], r['reason']):
            p.append('V006 JSON entry %d (%r) differs from rendered row %r' % (j, e.get('entry'), r['entry']))
        if e.get('disposition') == 'CITED_PINNED':
            if e.get('section_sha256') != r['sha'] or norm_marker(e.get('end_marker')) != '':
                p.append('V006 JSON entry %r: section_sha256 or end_marker differs from the rendered pin' % e.get('entry'))
        elif e.get('section_sha256') or norm_marker(e.get('end_marker')):
            p.append('V006 JSON NO_CHANGE entry %r carries pin fields' % e.get('entry'))
    return p


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--dir', required=True)
    p.add_argument('--provenance', required=True)
    p.add_argument('--slots', required=True)
    p.add_argument('--expect-slots-sha', required=True)
    p.add_argument('--nodes', required=True)
    p.add_argument('--expect-nodes-sha', required=True)
    p.add_argument('--v005', default=None, help='read these V005 bytes instead of the live addendum (a byte copy)')
    p.add_argument('--v006', default=None, help='read these V006 bytes instead of the live addendum (a byte copy)')
    p.add_argument('--out')
    p.add_argument('--no-hook', action='store_true')
    a = p.parse_args()
    if not a.no_hook:
        sys.addaudithook(make_hook(write_files=[a.out] if a.out else []))
    res = run(a)
    res['hooked'] = not a.no_hook
    text = json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    if a.out:
        with open(a.out, 'x', encoding='utf-8') as f:
            f.write(text)
    sys.stdout.write(text)
    if res['verdict_target_free'] != 'PASS':
        return 2
    return 0 if res['verdict_currency'] == 'PASS' else 3


if __name__ == '__main__':
    raise SystemExit(main())
