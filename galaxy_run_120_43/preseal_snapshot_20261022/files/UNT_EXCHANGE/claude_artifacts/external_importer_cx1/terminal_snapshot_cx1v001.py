"""Read-once terminal state at an authenticated original call root.
Missing receipt remains UNKNOWN, never CAP/INFRA or permission to relaunch.
Caller must supply root-bound invocation (python spelling and caps).
"""
from pathlib import Path
from terminal_association_cx1v001 import terminal_association
from request_guard_cx1v002 import require

def observe(snapshot,*,call_root,spec,driver,monitor,python,caps):
 root=Path(call_root)
 require(root.is_absolute() and str(root.resolve())==str(root),'TERMINAL_ROOT_PATH')
 receipt=root/'RECEIPT.json';launch=root/'RECEIPT.json.launch.json'
 if not receipt.exists():return {'direct_state':'UNKNOWN','outcome':None,'acceptance':None}
 # An existing but unreadable or unassociated terminal file must refuse.
 rp={'path':str(receipt),'sha256':snapshot.hash(receipt)}
 lp={'path':str(launch),'sha256':snapshot.hash(launch)}
 checked=terminal_association(snapshot,receipt_pin=rp,launch_pin=lp,spec=spec,driver=driver,monitor=monitor,python=python,outdir=str(root/'out'),caps=caps)
 outcome=checked['outcome_hint']
 return {'direct_state':'TERMINAL','outcome':None if outcome=='NEEDS_TAXONOMY' else outcome,'acceptance':None}
