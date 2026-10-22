"""Inert scheduler integration tests. No real monitor or driver execution."""
import hashlib
import json
import types
from pathlib import Path
from datetime import datetime, timezone
import scheduler_adapter_cx1v001 as A

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'calibration_orchestrator_c2/v005/campaign_c2v005.py'

def main():
    raw = SOURCE.read_bytes()
    adapter = A.build_scheduler(raw, str(SOURCE))
    original = types.ModuleType('_inert_parent_scheduler')
    original.__file__ = str(SOURCE)
    exec(compile(raw, str(SOURCE), 'exec'), original.__dict__)
    case = ROOT / 'inert_fixtures' / datetime.now(timezone.utc).strftime('scheduler_%Y%m%dT%H%M%S%f')
    case.mkdir(parents=True, exist_ok=False)
    driver = case / 'inert_driver.txt'
    driver.write_text('NOT EXECUTABLE: inert driver placeholder')
    calls = [{'spec': {'test_point': i}} for i in range(3)]
    campaign = {'calls': calls, 'max_concurrent': 2, 'process_budget': 2, 'stage_aware': False,
                'per_call': {'wall_cap_s': 1, 'rss_cap_bytes': 100, 'output_cap_bytes': 100},
                'campaign_wall_cap_s': 10, 'driver': {'path': str(driver), 'sha256': hashlib.sha256(driver.read_bytes()).hexdigest()},
                'monitor': {'path': 'INERT_MONITOR', 'sha256': '0'*64}}
    launches = []
    class Monitor:
        @staticmethod
        def verify_receipt(p, spec_sha256, driver_sha256):
            r = json.loads(Path(p).read_bytes())
            return {'ok': r['spec_sha256'] == spec_sha256 and r['driver_sha256'] == driver_sha256,
                    'receipt': r, 'reasons': []}
    class Process:
        def __init__(self, cmd, **kw):
            # No subprocess: materialize an inert terminal receipt only.
            spec = Path(cmd[cmd.index('--spec')+1])
            receipt = Path(cmd[cmd.index('--receipt')+1])
            launches.append(spec.parent.name)
            with receipt.open('x') as f:
                json.dump({'status': 'FINISHED', 'driver_status': 'COMPLETED',
                           'spec_sha256': hashlib.sha256(spec.read_bytes()).hexdigest(),
                           'driver_sha256': campaign['driver']['sha256']}, f)
        def poll(self): return 0
    for module in (adapter, original):
        module._load_monitor = lambda *args: Monitor
        module.subprocess = types.SimpleNamespace(Popen=Process)
    baseline = original.run_campaign(campaign=campaign, campaign_dir=str(case/'baseline'))
    assert baseline['launched'] == 3
    direct = case/'direct'; direct.mkdir()
    external = {0: {'index': 0, 'status': 'OK', 'call_dir': str(direct), 'execution_origin': 'DIRECT_EXTERNAL'}}
    launches.clear()
    mixed = adapter.run_campaign(campaign=campaign, campaign_dir=str(case/'mixed'), _admitted_external=external)
    assert mixed['launched'] == 2 and launches == ['call_0001', 'call_0002']
    assert not (case/'mixed/call_0000').exists()
    assert mixed['calls'][0]['call_dir'] == str(direct)
    assert [r['index'] for r in mixed['calls']] == [0,1,2]
    launches.clear()
    resumed = adapter.run_campaign(campaign=campaign, campaign_dir=str(case/'mixed'), resume=True, _admitted_external=external)
    assert resumed['launched'] == 0 and launches == [] and resumed['n_resumed'] == 2
    assert resumed['calls'][0] == mixed['calls'][0]
    plain = adapter.run_campaign(campaign=campaign, campaign_dir=str(case/'plain'))
    assert [r['status'] for r in plain['calls']] == [r['status'] for r in baseline['calls']]
    assert plain['launched'] == baseline['launched']
    all_ext = {i: dict(external[0], index=i) for i in range(3)}
    all_result = adapter.run_campaign(campaign=campaign, campaign_dir=str(case/'all'), _admitted_external=all_ext)
    assert all_result['launched'] == 0 and not list((case/'all').glob('call_*'))
    refused = []
    badcases = [('bad_index', {3:dict(external[0],index=3)}),
                ('bad_origin', {0:dict(external[0],execution_origin='WAVE_LOCAL')}),
                ('wrong_record_index', {0:dict(external[0],index=1)}),
                ('relative_custody', {0:dict(external[0],call_dir='relative')})]
    for name, bad in badcases:
        dest=case/name
        try: adapter.run_campaign(campaign=campaign,campaign_dir=str(dest),_admitted_external=bad)
        except ValueError: refused.append(name)
        else: raise AssertionError(name)
        assert not dest.exists()
    try: adapter.run_campaign(campaign=campaign,campaign_dir=str(case/'baseline'),resume=True,_admitted_external=external)
    except ValueError: refused.append('local_conflict')
    else: raise AssertionError('local conflict')
    report={'status':'PASS','blocking_count':0,'scope':'Isolated scheduler prototype only; no admission or production readiness claim',
            'tested':['parent baseline inert execution','mixed indices/fallback launch','mixed resume without duplicate launch',
                      'no-match parent behavior','all-external no call dirs']+refused,
            'untested':['receipt/acceptance/certificate admission','whole-engine replay','production entry and identity preservation'],
            'source_sha256':hashlib.sha256(raw).hexdigest(),
            'adapter_sha256':hashlib.sha256(Path(A.__file__).read_bytes()).hexdigest(),
            'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(case/'TEST_REPORT.json')

if __name__ == '__main__':main()
