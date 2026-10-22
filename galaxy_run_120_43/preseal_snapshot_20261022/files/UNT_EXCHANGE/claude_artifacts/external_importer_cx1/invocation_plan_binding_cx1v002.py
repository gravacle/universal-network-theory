"""Invocation prerequisite only. plan_pin must come from independent root authority.
No native-preflight/admission approval is inferred; no run contents are read.
"""
from pathlib import Path
from register_two_stage_cx1v003 import pin
from request_guard_cx1v002 import require
LAUNCHER_SHA='cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b'
MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'

def bind(snapshot,*,plan_pin,entry,driver,monitor):
 require(pin(plan_pin) and pin(driver) and pin(monitor),'INVOCATION_PINS')
 require(type(entry) is dict and pin(entry.get('launcher')) and pin(entry.get('spec')),'INVOCATION_ENTRY')
 require(entry['launcher']['sha256']==LAUNCHER_SHA and monitor['sha256']==MONITOR_SHA,'INVOCATION_SELECTED_CODE')
 snapshot.pin(entry['launcher']);snapshot.pin(monitor)
 plan=snapshot.document(plan_pin)
 require(type(plan) is dict and plan.get('schema')=='UNT_STEP4_LAUNCH_PLAN_CX1V001' and plan.get('binding_status')=='ROOT_BOUND','INVOCATION_BOUND_PLAN')
 require('template_status' not in plan and 'template_metadata' not in plan,'INVOCATION_TEMPLATE')
 require(plan.get('launcher')==entry['launcher'] and plan.get('monitor')==monitor,'INVOCATION_PLAN_CODE')
 calls=plan.get('calls');require(type(calls) is list and all(type(c) is dict for c in calls),'INVOCATION_CALLS')
 selected=[c for c in calls if c.get('point_key')==entry.get('key')]
 require(len(selected)==1,'INVOCATION_UNIQUE_KEY');c=selected[0]
 require(type(c.get('row')) is int and type(entry.get('row')) is int and c.get('row')==entry.get('row') and c.get('spec')==entry['spec'] and c.get('driver')==driver,'INVOCATION_CALL_IDENTITY')
 require(c.get('spec_status')=='ROOT_FINAL' and c.get('pending')==[],'INVOCATION_FINAL_SPEC')
 root=entry.get('call_root');require(type(root) is str and Path(root).is_absolute() and str(Path(root).resolve())==root,'INVOCATION_ROOT')
 require(c.get('outdir')==str(Path(root)/'out') and c.get('receipt')==str(Path(root)/'RECEIPT.json') and c.get('monitor_log')==str(Path(root)/'monitor.log'),'INVOCATION_LAYOUT')
 caps={k:c.get(k) for k in ('wall_cap_s','rss_cap_bytes','output_cap_bytes')}
 require(type(caps['wall_cap_s']) is int and caps['wall_cap_s']>0,'INVOCATION_WALL')
 for k in ('rss_cap_bytes','output_cap_bytes'):require(type(caps[k]) is int and caps[k]>0,'INVOCATION_CAP:'+k)
 caps['poll_s']=2.0
 return dict(prerequisites_only=True,python=PYTHON,caps=caps,call_root=root,plan=dict(plan_pin))
