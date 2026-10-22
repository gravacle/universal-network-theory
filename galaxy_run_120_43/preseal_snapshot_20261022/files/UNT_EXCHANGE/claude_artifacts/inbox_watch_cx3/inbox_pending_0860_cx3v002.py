"""Read-only 60-second root/deputy watch; only explicit outbox receipts clear pending."""
from pathlib import Path
import re, subprocess, time
B=Path('/Users/bgm/Research/UNT_EXCHANGE')
SCOPES={'FROM_CODEX':(860,'Acknowledged dispatches:','Not addressed dispatches:'),
        'FROM_CLAUDE3':(327,'Acknowledged deputy dispatches:','Not addressed deputy dispatches:')}
def clears(text,prefix):
    result=set()
    for line in text.splitlines():
        if line.startswith(prefix):
            value=line[len(prefix):].strip()
            if re.fullmatch(r'[0-9]{4}(?:, [0-9]{4})*',value):result.update(value.split(', '))
    return result
assert clears('Acknowledged dispatches: 0860, 0862','Acknowledged dispatches:')=={'0860','0862'}
assert not clears('mentions Acknowledged dispatches: 0860','Acknowledged dispatches:')
assert not clears('Acknowledged dispatches: 0860?','Acknowledged dispatches:')
seen=set()
while True:
    cleared={name:set() for name in SCOPES}
    for p in (B/'FROM_CODEX3').iterdir():
        m=re.match(r'([0-9]{4})_',p.name)
        if m and int(m[1])>=711 and p.suffix=='.md':
            text=p.read_text()
            for name,(_,ack,skip) in SCOPES.items():cleared[name]|=clears(text,ack)|clears(text,skip)
    pending=[];new=[]
    for name,(floor,_,_) in SCOPES.items():
        for p in sorted((B/name).iterdir()):
            m=re.match(r'([0-9]{4})_',p.name)
            if not m or int(m[1])<floor or p.suffix!='.md':continue
            body=p.read_text();key=(name,p.name)
            relevant=bool(re.search(r'codex3|ALL_LANES',p.name,re.I) or re.search(r'Codex3|Codex\s*\(any account\)|ALL[ _-]LANES|all lanes',body,re.I))
            if key not in seen:new.append({'scope':name,'file':p.name,'mentions_lane':relevant});seen.add(key)
            if relevant and m[1] not in cleared[name]:pending.append(str(p))
    print('PENDING_INBOX_CHECK '+subprocess.check_output(['/bin/date','-u'],text=True).strip(),flush=True)
    for x in new:print('NEW '+str(x),flush=True)
    for p in pending:print('PENDING '+p,flush=True)
    print('PENDING_COUNT '+str(len(pending)),flush=True)
    time.sleep(60)
