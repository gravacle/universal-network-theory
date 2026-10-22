from pathlib import Path
import ast,hashlib,json,re,subprocess
D=Path(__file__).resolve().parent
p=D/'inbox_pending_0860_cx3v003.py'
b=p.read_bytes(); tree=ast.parse(b)
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
ns={'re':re}; exec(compile(ast.Module(body=functions,type_ignores=[]),str(p),'exec'),ns)
f=ns['relevant_message']; checks=[]
def check(name,filename,body,expected):
    actual=f(filename,body); checks.append({'name':name,'expected':expected,'actual':actual,'passed':actual==expected})
check('filename_codex3','0872_codex3_dispatch.md','',True)
check('filename_any_substring_codex3','0872_toCODEX3.md','Acks: Codex3 0744',True)
check('filename_all_lanes','0872_ALL_LANES.md','',True)
check('direct_to','packet.md','From Claude2. To: Codex3.',True)
check('markdown_cc','packet.md','From **Claude3** to **Codex1**; cc **Codex3**. Acks: Codex3 0744.',True)
check('instruction_after_ack','packet.md','Acks: Codex3 0744; Codex3 must review the successor.',True)
check('instruction_next_line','packet.md','Acks: Codex3 0744.\nCodex3: review now.',True)
check('reserve_directive','packet.md','Codex3 is at 17% and keeps its reserve.',True)
check('actual_reference_outside_ack','packet.md','Codex3 0674 is evidence for this decision.',True)
check('any_account','packet.md','To Codex (any account)',True)
check('all_lanes_body','packet.md','To ALL LANES',True)
check('receipt_only','packet.md','Acks: Codex1 0291; Codex3 0744.',False)
check('receipt_markdown','packet.md','**Acks:** Codex3 0744 (no action needed).',False)
check('acknowledged_packets','packet.md','Acknowledged packets: Codex3 0744, Codex1 0270.',False)
check('acknowledged_dispatches','packet.md','Acknowledged dispatches: Codex3 0744.',False)
check('ack_singular','packet.md','Ack: Codex3 0744.',False)
check('nonnumeric_ack','packet.md','Acks: Codex3.',True)
check('short_reference_kept','packet.md','Acks: Codex3 744.',True)
check('five_digit_reference_kept','packet.md','Acks: Codex3 07440.',True)
check('unrelated','packet.md','To Codex1. No other assignment.',False)
E=D.parents[1]
fixtures=[
('FROM_CODEX','0867_',True),('FROM_CODEX','0870_',True),('FROM_CODEX','0871_',True),
('FROM_CLAUDE3','0367_',True),('FROM_CLAUDE3','0373_',True),
('FROM_CLAUDE3','0376_',False),('FROM_CLAUDE3','0377_',False)]
pins=[]
for folder,prefix,expected in fixtures:
    matches=[q for q in (E/folder).iterdir() if q.name.startswith(prefix) and q.suffix=='.md']; assert len(matches)==1
    q=matches[0]; raw=q.read_bytes(); pins.append({'path':str(q),'sha256':hashlib.sha256(raw).hexdigest()})
    check('real_'+prefix,q.name,raw.decode(),expected)
assert ns['clears']('Acknowledged dispatches: 0870, 0871','Acknowledged dispatches:')=={'0870','0871'}
assert not ns['clears']('Acknowledged dispatches: 0870?','Acknowledged dispatches:')
result={'schema':'INBOX_FILTER_CONTROLS_CX3V003','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'script':{'path':str(p),'sha256':hashlib.sha256(b).hexdigest()},'test_script':{'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'cases':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'receipt_parser_checks':2,'fixtures':pins,'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','limits':'Pure function/receipt tests only; no watcher loop or external action executed by the test.'}
record=D/'INBOX_FILTER_CONTROLS_CX3V003.json'
with record.open('x',encoding='utf-8') as h:json.dump(result,h,indent=2);h.write('\n')
print(json.dumps({'status':result['status'],'passed':result['passed'],'total':result['total'],'receipt_parser_checks':2,'record':str(record),'sha256':hashlib.sha256(record.read_bytes()).hexdigest()}))
assert result['status']=='PASS'
