"""0361 source-document evidence (CLAUDE2 helper 0361-A). Read-only; stdlib only; no network.

1. SPARC master paper (Lelli, McGaugh & Schombert 2016, AJ 152:157), pinned by sha256:
   * per-page structure flags (vector path-operator count = figure indicator, table-caption presence, digit fraction) used to decide
     which pages may be rendered (pages 3 and 5 were rendered with the Read tool; page 4 = Table 1, page 6 carries a Table 2 excerpt,
     pages 7-13 carry figures including mass models: NOT rendered);
   * text-layer decoding with each font's ToUnicode CMap (Symbol-encoded glyphs translated), used ONLY to assert that the quoted
     sentences occur on their stated pages and to count marker terms over all pages. No page text is emitted except the quotes.
2. Bounded local filename search (/Users/bgm/Research, excluding .git and scratch) for Leroy 2008 paper / Appendix E / printed
   Table 7 and for the Archangel / Schombert & McGaugh 2014b documentation (names only; forbidden names counted, never listed).
3. Bibliographic identifiers for Leroy 2008 from local documents (CDS ReadMe lines, secondary-note link lines).
Usage: python3 -I -B source_document_evidence_0361_v001.py <new_output.json>
"""
import hashlib, html, json, os, re, sys, zlib

UNT = '/Users/bgm/Research/Universal Network Theory'
JPC = UNT + '/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PDF = (JPC + '/sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf', '87fa39590a0cded15e6dc7a51355fa2354eea8a130f477b92e4cee15c4e36a19')
PDF_SIDECAR = (PDF[0] + '.SOURCE.json', '0413b81940409e9bba28c4956b1683259084b3b4f227f50868725ce263a850f4')
PROBE_0356 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_semantics_0356/PROBE_EVIDENCE_0356_V002.json',
              '0d4c5ec46cc1c340897b41b2dc18bbd059c4bf9ca1b25a5d91b9f97b63e6d00d')
LEROY_README = (JPC + '/leroy2008_ReadMe.html', 'cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48')
READINESS = (JPC + '/GALAXY_INPUT_READINESS.md', '6e23d981e7bf0450a1e51169d29a9d54b6f2d1e4fd014432255988e018e0ec6c')
RENDERED = {3: 'rendered with the Read tool (text only, no figure, no table)', 5: 'rendered with the Read tool (text only, no figure, no table)'}
QUOTES = [
    {'id': 'SP-1', 'page': 3, 'section': '3.1 Surface Photometry', 'topic': 'photometry software',
     'text': 'The cleaned frames were analyzed using the Archangel software (Schombert 2011).'},
    {'id': 'SP-2', 'page': 3, 'section': '3.1 Surface Photometry', 'topic': 'procedure reference',
     'text': 'we derived homogeneous surface photometry at 3.6 μm following the procedures of Schombert & McGaugh (2014b).'},
    {'id': 'SP-3', 'page': 3, 'section': '3.1 Surface Photometry', 'topic': 'sky error',
     'text': 'The absolute sky value and its error were estimated using multiple sky boxes'},
    {'id': 'SP-4', 'page': 5, 'section': '3.1 Surface Photometry', 'topic': 'surface-brightness profile errors',
     'text': 'The errors in the surface brightness profiles, however, are dominated by the uncertainties in the sky value rather than variations around each ellipse.'},
    {'id': 'SP-5', 'page': 5, 'section': '3.1 Surface Photometry', 'topic': 'distribution of the profiles',
     'text': 'All surface brightness profiles are available for download at astroweb.cwru.edu/SPARC.'},
    {'id': 'SP-6', 'page': 6, 'section': '3.3 Mass Models', 'topic': 'outer stellar-profile policy',
     'text': 'calculated using the observed [3.6] surface brightness profile and extrapolating the exponential fit to R → ∞, unless the profile shows a clear truncation.',
     'sentence_subject': 'The stellar contribution',
     'text_layer_order': 'the limit R → ∞ is a separate equation fragment: the text layer stores the arrow and infinity glyphs (EuclidSymbol; ToUnicode F0AE and 00A5 = Symbol arrowright and infinity) before the italic R, which is drawn to their left',
     'text_layer_variant': 'The stellar contribution is calculated using the observed [3.6] surface brightness profile and extrapolating the exponential fit to → ∞R, unless the profile shows a clear truncation.',
     'quote_is_suffix_of_asserted_sentence': True},
    {'id': 'SP-7', 'page': 14, 'section': 'References', 'topic': 'Archangel reference',
     'text': 'Schombert, J. 2011, ARCHANGEL: Galaxy Photometry System, Astrophysics Source Code Library, ascl:1107.011'},
    {'id': 'SP-8', 'page': 14, 'section': 'References', 'topic': 'procedure reference',
     'text': 'Schombert, J. M., & McGaugh, S. 2014b, PASA, 31, 11'}]
ABSENCE_TERMS = ['kill', 'comment', 'sfb', '#', 'masked row', 'error column', 'kill flag']
SYMBOL = {0xAE: '→', 0xA5: '∞', 0xB1: '±', 0xB4: '×', 0xE1: '〈', 0xF1: '〉', 0x2B: '+', 0x2D: '−', 0x3D: '=', 0x73: 'σ', 0x6D: 'μ',
          0xA3: '≤', 0xB3: '≥', 0x7E: '∼', 0xBB: '≈'}
FORBIDDEN = re.compile(r'Newton|FIELD_|RESPONSE|ROTATION|FIT|TRIAL|MOM1|rotmod|MassModels')
SEARCH = {'leroy_2008_paper_appendix_E_or_printed_table7': r'(?i)(0810[._]2556|leroy.*\.(pdf|ps|tex|djvu|txt|md)$|appendix[_ -]?e(?![a-z])|star.?formation.?efficiency|2008aj.*136.*2782)',
          'archangel_or_schombert_mcgaugh_2014b': r'(?i)(archangel|ascl.?1107|schombert.*(2014|pasa)|pasa.*31.*11)'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pinned(p, h):
    b = open(p, 'rb').read()
    if sha(b) != h:
        raise SystemExit('E_PIN ' + p)
    return b


class Pdf:
    def __init__(self, b):
        self.o = {}
        for m in re.finditer(rb'(\d+)\s+0\s+obj(.*?)endobj', b, re.S):
            self.o[int(m.group(1))] = m.group(2)
        for n, body in list(self.o.items()):
            if b'/ObjStm' in body.split(b'stream')[0]:
                s = self.stream(body)
                N = int(re.search(rb'/N\s+(\d+)', body).group(1)); first = int(re.search(rb'/First\s+(\d+)', body).group(1))
                h = s[:first].split()
                pr = [(int(h[2 * i]), int(h[2 * i + 1])) for i in range(N)]
                for i, (on, off) in enumerate(pr):
                    end = pr[i + 1][1] if i + 1 < N else len(s) - first
                    self.o.setdefault(on, s[first + off:first + end])
        cat = [body for body in self.o.values() if re.search(rb'/Type\s*/Catalog', body)][0]
        self.pages = []
        self._walk(int(re.search(rb'/Pages\s+(\d+)\s+0\s+R', cat).group(1)))

    def stream(self, body):
        m = re.search(rb'stream\r?\n(.*?)\r?\nendstream', body, re.S)
        if not m:
            return None
        d = m.group(1)
        if b'/FlateDecode' in body.split(b'stream')[0]:
            try:
                return zlib.decompress(d)
            except Exception:
                return zlib.decompressobj().decompress(d)
        return d

    def _walk(self, n):
        body = self.o[n]
        if re.search(rb'/Type\s*/Pages', body):
            for k in re.findall(rb'(\d+)\s+0\s+R', re.search(rb'/Kids\s*\[(.*?)\]', body, re.S).group(1)):
                self._walk(int(k))
        else:
            self.pages.append(n)

    def deref(self, x):
        m = re.match(rb'\s*(\d+)\s+0\s+R', x)
        return self.o[int(m.group(1))] if m else x

    def contents(self, n):
        m = re.search(rb'/Contents\s*(\[(.*?)\]|(\d+)\s+0\s+R)', self.o[n], re.S)
        refs = [int(x) for x in re.findall(rb'(\d+)\s+0\s+R', m.group(2))] if m.group(2) is not None else [int(m.group(3))]
        return b'\n'.join(self.stream(self.o[r]) or b'' for r in refs)

    def fonts(self, n):
        body = self.o[n]
        m = re.search(rb'/Resources\s*(\d+\s+0\s+R|<<)', body)
        res = self.deref(m.group(1)) if m and m.group(1) != b'<<' else body
        fm = re.search(rb'/Font\s*(\d+\s+0\s+R|<<(.*?)>>)', res, re.S)
        fd = self.deref(fm.group(1)) if fm.group(2) is None else fm.group(2)
        out = {}
        for name, ref in re.findall(rb'/([\w.+-]+)\s+(\d+)\s+0\s+R', fd):
            fo = self.o[int(ref)]
            cmap = {}
            tu = re.search(rb'/ToUnicode\s+(\d+)\s+0\s+R', fo)
            if tu:
                s = self.stream(self.o[int(tu.group(1))]) or b''
                for blk in re.findall(rb'beginbfchar(.*?)endbfchar', s, re.S):
                    for a, u in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
                        cmap[int(a, 16)] = bytes.fromhex(u.decode()).decode('utf-16-be', 'replace')
                for blk in re.findall(rb'beginbfrange(.*?)endbfrange', s, re.S):
                    for a, z, u in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
                        for k in range(int(a, 16), int(z, 16) + 1):
                            cmap[k] = chr(int(u, 16) + k - int(a, 16))
            out[name.decode()] = {'two_byte': b'/Type0' in fo, 'symbol': b'Symbol' in fo, 'cmap': cmap}
        return out

    def text(self, n):
        fonts = self.fonts(n)
        cs = self.contents(n)
        cur = None
        parts = []
        tok = re.compile(rb'/([\w.+-]+)\s+[-\d.]+\s+Tf|\[((?:\\.|[^\]\\])*)\]\s*TJ|(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f]*>)\s*Tj|(T\*|Td|TD|Tm|ET)\b', re.S)
        for m in tok.finditer(cs):
            if m.group(1):
                cur = fonts.get(m.group(1).decode())
            elif m.group(4):
                parts.append(' ')
            else:
                arr = m.group(2) if m.group(2) is not None else m.group(3)
                for s in re.finditer(rb'\(((?:\\.|[^\\)])*)\)|<([0-9A-Fa-f]*)>|(-?[\d.]+)', arr):
                    if s.group(3) is not None:
                        if float(s.group(3)) <= -200:
                            parts.append(' ')
                        continue
                    raw = bytes.fromhex(s.group(2).decode()) if s.group(2) is not None else re.sub(
                        rb'\\([0-7]{1,3}|.)', lambda e: bytes([int(e.group(1), 8)]) if e.group(1)[:1].isdigit() else
                        {b'n': b'\n', b'r': b'\r', b't': b'\t'}.get(e.group(1), e.group(1)), s.group(1))
                    step = 2 if cur and cur['two_byte'] else 1
                    for i in range(0, len(raw), step):
                        code = int.from_bytes(raw[i:i + step], 'big')
                        ch = cur['cmap'].get(code) if cur else None
                        if ch is None:
                            ch = chr(code) if code < 256 else '?'
                        if cur and cur['symbol']:
                            o = ord(ch[0]) if ch else 0
                            ch = SYMBOL.get(o & 0xFF, ch) if (o < 256 or 0xF000 <= o <= 0xF0FF) else ch
                        parts.append({'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}.get(ch, ch))
        return re.sub(r'\s+', ' ', ''.join(parts))


def squash(s):
    # whitespace (incl. thin space, no-break space and the Symbol-font space U+F0A0) removed; hyphens and minus removed so that
    # line-break hyphenation (down-load) matches; used only to assert that a quote occurs on its page
    return re.sub('[\\s\u2009\u00a0\uf0a0]+', '', s).replace('\u2212', '').replace('-', '').replace('\u2019', "'")


def name_search():
    rx = {k: re.compile(v) for k, v in SEARCH.items()}
    hits = {k: [] for k in rx}
    hidden = {k: 0 for k in rx}
    for dp, dns, fns in os.walk('/Users/bgm/Research'):
        dns[:] = sorted(d for d in dns if d != '.git')
        for n in sorted(fns):
            for k, r in rx.items():
                if r.search(n):
                    p = os.path.join(dp, n)
                    if FORBIDDEN.search(p):
                        hidden[k] += 1
                    else:
                        hits[k].append(p.replace(UNT, '<UNT>'))
    return {'root': '/Users/bgm/Research (directories named .git skipped)', 'method': 'os.walk over file names only; no content read',
            'results': {k: {'pattern': SEARCH[k], 'matches': hits[k], 'forbidden_name_matches_not_listed': hidden[k]} for k in rx}}


def main(out):
    b = pinned(*PDF)
    sc = pinned(*PDF_SIDECAR)
    pr = json.loads(pinned(*PROBE_0356))['sparc_paper_pdf']
    assert pr['path'] == PDF[0] and pr['sha256'] == PDF[1] and pr['sidecar']['sha256'] == PDF_SIDECAR[1]
    pdf = Pdf(b)
    pages = []
    texts = {}
    for i, n in enumerate(pdf.pages, 1):
        cs = pdf.contents(n)
        t = pdf.text(n)
        texts[i] = t
        nd = sum(c.isdigit() for c in t); na = sum(c.isalpha() for c in t)
        pages.append({'page': i, 'vector_path_operators': len(re.findall(rb'\s(?:l|c|re)\s', cs)),
                      'table_caption_present': bool(re.search(r'Table \d', t)), 'digit_fraction_permille': round(1000 * nd / max(1, nd + na)),
                      'handling': RENDERED.get(i, 'not rendered; text layer used only for quote assertion and term counts')})
    quotes = []
    for q in QUOTES:
        found = squash(q.get('text_layer_variant', q['text'])) in squash(texts[q['page']])
        quotes.append(dict(q, found_on_stated_page=found, words=len(q['text'].split())))
    allt = ' '.join(texts.values()).lower()
    absence = {t: allt.count(t) for t in ABSENCE_TERMS}
    rl = html.unescape(re.sub(r'<[^>]+>', '', pinned(*LEROY_README).decode('utf-8', 'replace'))).splitlines()
    rd = pinned(*READINESS).decode('utf-8').splitlines()
    bib = {'cds_readme': {'path': LEROY_README[0], 'sha256': LEROY_README[1], 'line_method': 'tags removed, html.unescape, splitlines; 1-based',
                          'lines': {str(n): rl[n - 1].strip() for n in (58, 59, 60, 61, 62, 63, 64)}},
           'secondary_note_arxiv_links': {'path': READINESS[0], 'sha256': READINESS[1],
                                          'lines_with_arxiv_0810_2556': [i for i, l in enumerate(rd, 1) if 'arxiv.org/pdf/0810.2556' in l]},
           'doi_in_local_documents': 'doi' in pinned(*LEROY_README).decode('utf-8', 'replace').lower()}
    res = {'schema': 'CLAUDE2_0361_SOURCE_DOCUMENT_EVIDENCE_V001',
           'sparc_paper': {'path': PDF[0], 'sha256': PDF[1], 'bytes': len(b), 'sidecar': {'path': PDF_SIDECAR[0], 'sha256': PDF_SIDECAR[1], 'content': json.loads(sc)},
                           'resolved_from_0356_evidence': {'path': PROBE_0356[0], 'sha256': PROBE_0356[1], 'pointer': '/sparc_paper_pdf', 'match': True},
                           'n_pages': len(pdf.pages), 'pages': pages},
           'quotes': quotes, 'all_quotes_found': all(q['found_on_stated_page'] for q in quotes),
           'whole_paper_term_counts_text_layer': absence,
           'leroy_2008_identifiers_local': bib,
           'bounded_filename_search': name_search()}
    with open(out, 'x', encoding='utf-8') as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(json.dumps({'ok': True, 'all_quotes_found': res['all_quotes_found'], 'term_counts': absence,
                      'quotes': {q['id']: q['found_on_stated_page'] for q in quotes}}))


if __name__ == '__main__':
    main(sys.argv[1])
