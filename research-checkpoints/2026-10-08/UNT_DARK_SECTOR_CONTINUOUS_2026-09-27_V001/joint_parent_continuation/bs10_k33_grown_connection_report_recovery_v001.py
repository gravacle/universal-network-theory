#!/usr/bin/env python3
"""Finish the missing report from sealed data; no scientific replay or imports."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, socket, sys

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
CP=J/'bs10_k33_grown_connection_v001_checkpoints'
RESULT=J/'BS10_K33_GROWN_CONNECTION_V001_RESULT.json'
REPORT=J/'BS10_K33_GROWN_CONNECTION_V001_RESULT.md'
RECEIPT=CP/'report_recovery_receipt_v001.json'
RAW='0ee08b31c2f9455e2d27b9fe14da349a8c3eff2dd0843b629905049a0d390a31'
CANON='b573b645dace83b518da98e27a528c3076b0e4b74d81c7e6bd1a357dd0356823'
ERROR='1da6e20cec2c34ae4cf404eb5cf634b1cc86340c6e820dcb9f93f0f7f3a69e0d'

def sha(p):
    p=Path(p).resolve()
    if not p.is_relative_to(ROOT):raise RuntimeError('Outside sole project root')
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def canon(o):
    return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def exclusive(p,o):
    with p.open('x',encoding='utf-8') as f:
        json.dump(o,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def event(name,**kw):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=name,pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())

def recover():
    if sys.platform!='darwin' or REPORT.exists() or RECEIPT.exists():raise RuntimeError('Same Mac; exclusive missing-report recovery only')
    if sha(RESULT)!=RAW or sha(CP/'error.json')!=ERROR:raise RuntimeError('Sealed result/error changed')
    a=json.loads(RESULT.read_text());base=dict(a);claim=base.pop('canonical_payload_sha256')
    if claim!=CANON or canon(base)!=CANON or a['status']!='QUALIFIED_ARITHMETIC' or a['passed_count']!=7215 or a['failed_count'] or len(a['rows'])!=16:raise RuntimeError('Scientific seal/status mismatch')
    manifest=a['manifest']
    if manifest['host']!=socket.gethostname() or json.loads((CP/'manifest.json').read_text())!=manifest:raise RuntimeError('Manifest/host mismatch')
    events=[json.loads(s) for s in (CP/'events.jsonl').read_text().splitlines() if s]
    if not any(e['event']=='started' and e.get('manifest_sha256')==sha(CP/'manifest.json') for e in events):raise RuntimeError('Original start seal missing')
    if not any(e['event']=='result_saved' and e.get('sha256')==RAW and e.get('canonical_payload_sha256')==CANON for e in events):raise RuntimeError('Original result seal missing')
    if not any(e['event']=='error' and e.get('sha256')==ERROR for e in events):raise RuntimeError('Original formatter error seal missing')
    inputs=dict(manifest['input_sha256'])
    inputs.update({str(RESULT):RAW,str(CP/'error.json'):ERROR,str(CP/'manifest.json'):sha(CP/'manifest.json'),str(Path(__file__).resolve()):sha(__file__)})
    gp=CP/'graph_flags.json';gh=sha(gp)
    if not any(e['event']=='graph_flags_saved' and e.get('sha256')==gh and e.get('failed')==0 for e in events):raise RuntimeError('Graph checkpoint seal missing')
    inputs[str(gp)]=gh
    for r in a['rows']:
        p=CP/(r['key']+'.json');h=sha(p)
        if json.loads(p.read_text())!=r or r['failed_count']:raise RuntimeError('Saved row mismatch')
        if not any(e['event']=='row_complete' and e.get('key')==r['key'] and e.get('sha256')==h and e.get('failed')==0 for e in events):raise RuntimeError('Row journal mismatch')
        inputs[str(p)]=h
    for p,h in inputs.items():
        if sha(p)!=h:raise RuntimeError('Input changed: '+p)
    original_journal_hash=sha(CP/'events.jsonl')
    event('report_recovery_started',original_result_sha256=RAW,original_error_sha256=ERROR,original_journal_sha256=original_journal_hash,recovery_source_sha256=sha(__file__))
    lines=['# Encoded N4 initial connection dynamics V001: recovered report','',f"{a['status']}; {a['passed_count']}/7215 controls; all16 preparations.",'',a['qualification'],'',
        'The numerical producer exited3 after sealing every scientific row and the final JSON. Its report formatter requested a nonexistent P0 key. This report uses the sealed raw_target_initial_connected_probability field. Original source, protocol, result, rows and error are preserved; no scientific calculation was replayed.','',
        f"Conditional original-state endpoint change census: {json.dumps(a['conditional_endpoint_change_counts'],sort_keys=True)}.",
        f"Conditional original-state initial slope census: {json.dumps(a['conditional_initial_slope_counts'],sort_keys=True)}.",'',
        '| g | seed | age | target P0 | P1 | P2 | normalized stored polynomial at .01 | conditional original probability band | conditional change |',
        '|---|---:|---:|---:|---:|---:|---:|---|---|']
    for r in a['rows']:
        b=r['bands'];lines.append(f"|{r['g']}|{r['start']}|{r['age']}|{r['raw_target_initial_connected_probability']:.10g}|{r['P1']:.10g}|{r['P2']:.10g}|{b['normalized_stored_polynomial']:.10g}|{b['conditional_original_exact_probability_band']}|{b['conditional_original_change_status']}|")
    lines+=['','All16 finite-endpoint changes are INCONCLUSIVE under the frozen remainder. The six mature-cycle initial slopes qualify as positive. These are different conclusions. Signed bridge/healing terms and all norms/conditional allowances remain in the sealed JSON.',
        'The876.096|t|³ bound holds throughout0<=t<=.01. Assigned floating and arithmetic budgets remain conditional; probability bands are not clipped. No later trajectory, physical clock/volume, pressure, metric or cosmology was computed.',
        f"Scientific runtime {a['runtime_seconds']:.6f}s; original PID{a['pid']}.",f'Original raw result SHA256: {RAW}',f'Original canonical payload SHA256: {CANON}',f'Preserved formatter error SHA256: {ERROR}',f'Recovery source SHA256: {sha(__file__)}','No rerun, scheduler or automatic resumption.']
    for p,h in inputs.items():
        if sha(p)!=h:raise RuntimeError('Input changed before report seal: '+p)
    with REPORT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    receipt=dict(status='REPORT_RECOVERED_NO_SCIENTIFIC_REPLAY',pid=os.getpid(),host=socket.gethostname(),original_producer_pid=a['pid'],original_producer_exit_code=3,input_sha256=inputs,original_journal_sha256=original_journal_hash,report_sha256=sha(REPORT),no_original_bytes_rewritten=True,no_scientific_import_or_execution=True)
    exclusive(RECEIPT,receipt);event('report_saved',sha256=sha(REPORT),recovered=True,recovery_receipt_sha256=sha(RECEIPT),original_formatter_error_sha256=ERROR)
    print(json.dumps(dict(status=receipt['status'],report_sha256=receipt['report_sha256'],receipt_sha256=sha(RECEIPT),pid=os.getpid())))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',required=True,action='store_true');p.parse_args();recover()
