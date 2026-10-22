"""Uninstalled executor observer adapter. Root pins supplied by trusted installer.
Only supplies observations; no candidates, acceptance, cache writes or launches.
"""
import copy,re,hashlib
from pathlib import Path
from snapshot_cx1v001 import Snapshot,strict_json
from request_guard_cx1v002 import require
from natural_registered_observation_cx1v003 import observe

def make_observer(executor,*,root_binding_pin,expected_policy,expected_entry,theta_key):
 anchors=copy.deepcopy(dict(root_binding_pin=root_binding_pin,expected_policy=expected_policy,expected_entry=expected_entry))
 def callback(candidate,call):
  require(type(candidate) is dict and type(call) is dict,'OBSERVER_CALLBACK_FIELDS')
  index=call.get('call_index')
  require(type(index) is int and index>=0 and type(candidate.get('call_index')) is int and candidate['call_index']==index,'OBSERVER_CALLBACK_INDEX')
  require(candidate.get('key')==call.get('key') and type(candidate.get('spec')) is dict and candidate['spec'].get('sha256')==call.get('spec_sha256'),'OBSERVER_CALLBACK_IDENTITY')
  directory=Path(executor._external_wave_dir);match=re.fullmatch(r'wave_([0-9]{4,})',directory.name)
  require(match is not None,'OBSERVER_CALLBACK_WAVE')
  path=directory/'WAVE_PLAN.json';raw=Snapshot().read(path)
  require(strict_json(raw)==executor._external_plan,'OBSERVER_CALLBACK_COMMITTED_PLAN')
  planned=[c for c in executor._external_plan.get('calls',[]) if c.get('call_index')==index]
  require(len(planned)==1 and planned[0]==call,'OBSERVER_CALLBACK_EXACT_CALL')
  plan_pin=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest())
  return observe(ctx=executor._external_orch,lock=executor._external_lock(),wave=int(match.group(1)),call_index=index,plan_pin=plan_pin,theta_key=theta_key,**anchors)
 return callback
