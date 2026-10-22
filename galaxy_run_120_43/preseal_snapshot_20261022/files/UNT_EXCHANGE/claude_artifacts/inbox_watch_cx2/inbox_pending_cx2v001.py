"""Inbox checks only. Seen is never acknowledged; immutable outbox packets are the ack ledger.

This lists pending dispatches. It does not claim to execute them or keep a model
active through a paused/interrupted turn. Use --once in the foreground every minute.
"""
import argparse
import datetime
import hashlib
from pathlib import Path
import re
import time

ROOT = Path('/Users/bgm/Research/UNT_EXCHANGE')
INBOX = ROOT/'FROM_CODEX'
OUTBOX = ROOT/'FROM_CODEX2'
BASELINE = 833  # Read/handled through this number before the interruption.
NUMBERED = re.compile(r'^(\d{4,})_')
ADDRESSEE = re.compile(r'Codex2\b|Codex\s*\(any account\)', re.I)
ACK = re.compile(r'^Acknowledged dispatches:\s*([0-9, ]+)\s*$', re.M)

def number(name):
    hit = NUMBERED.match(name)
    return int(hit[1]) if hit else None

def addressed(text):
    lines = text.splitlines()
    title = next((line for line in lines if line.startswith('# ')), '')
    if ADDRESSEE.search(title):
        return True
    # Multi-lane dispatches may address Codex2 in a dedicated paragraph.
    return any(re.match(r'^(?:\*\*|#{1,6}\s*)?\s*(?:To:\s*)?(?:Codex2\b|Codex\s*\(any account\))',
                        line, re.I) for line in lines)

def acknowledgments(texts):
    found = set()
    for text in texts:
        for hit in ACK.finditer(text):
            found.update(int(token.strip()) for token in hit[1].split(',') if token.strip())
    return found

def pending(documents, ack):
    return sorted((n, item) for n, item in documents.items()
                  if n > BASELINE and n not in ack and addressed(item['text']))

def scan():
    documents = {}
    for p in sorted(INBOX.iterdir()):
        n = number(p.name)
        if n is None or n <= BASELINE or not p.is_file():
            continue
        raw = p.read_bytes()
        documents[n] = {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(),
                        'text': raw.decode('utf-8')}
    texts = []
    for p in sorted(OUTBOX.iterdir()):
        if number(p.name) is not None and p.suffix == '.md' and p.is_file():
            texts.append(p.read_text())
    ack = acknowledgments(texts)
    rows = pending(documents, ack)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y')
    print(stamp+' | latest=%s | pending_unacknowledged=%d' % (max(documents, default=BASELINE), len(rows)), flush=True)
    for n, item in rows:
        title = next((line for line in item['text'].splitlines() if line.startswith('# ')), '')
        print('PENDING %04d %s SHA256=%s\n%s' % (n, item['path'], item['sha256'], title), flush=True)
    return rows

def self_test():
    docs = {
        834: {'text': '# 0834 — Claude3: item for another lane'},
        837: {'text': '# 0837 — Codex1 and Codex2: shared dispatch'},
        839: {'text': '# 0839 — Codex2: urgent review'},
        846: {'text': '# 0846 — Codex3 takes over\n\n**Codex2:** post status only.'},
        848: {'text': '# 0848 — Codex2: new work'},
        849: {'text': '# 0849 — Codex (any account): common work'},
    }
    want = [837, 839, 846, 848, 849]
    assert [n for n, _ in pending(docs, set())] == want
    # Reading/scanning repeatedly never removes a pending dispatch.
    assert [n for n, _ in pending(docs, set())] == want
    # Unrelated mention/quoted acknowledgment does not acknowledge a dispatch.
    assert acknowledgments(['Read 0837.\n> Acknowledged dispatches: 0839']) == set()
    ack = acknowledgments(['Acknowledged dispatches: 0837, 0839, 0846, 0848\n'])
    assert [n for n, _ in pending(docs, ack)] == [849]
    # Restart has no cursor to lose: the same immutable ledger gives the same pending set.
    assert [n for n, _ in pending(docs, acknowledgments([
        'Acknowledged dispatches: 0837, 0839, 0846, 0848\n']))] == [849]
    print('TESTED: 5/5 pending/ack/restart checks; no dispatch execution claimed.', flush=True)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--once', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return
    while True:
        try:
            scan()
        except Exception as exc:
            print('INBOX_SCAN_ERROR '+type(exc).__name__+': '+str(exc), flush=True)
            if args.once:
                raise
        if args.once:
            return
        time.sleep(60)

if __name__ == '__main__':
    main()
