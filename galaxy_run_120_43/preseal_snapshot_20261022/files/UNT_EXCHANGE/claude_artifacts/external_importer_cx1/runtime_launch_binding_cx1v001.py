"""D005 timestamp/interpreter associations. Root authority of supplied pins is external."""
from datetime import datetime
from register_two_stage_cx1v002 import pin,sha
from request_guard_cx1v002 import require

def utc(value):
 try:
  require(type(value) is str,'CAPTURE_UTC_TYPE')
  t=datetime.fromisoformat(value.replace('Z','+00:00'))
  require(t.tzinfo is not None,'CAPTURE_UTC_TIMEZONE');return t
 except (ValueError,TypeError,AttributeError):require(False,'CAPTURE_UTC_FORMAT')

def check_launches(snapshot,*,freeze_pin,launch_pin,register_pin,binding,direct_pin,campaign_pin,direct,campaign):
 freeze=snapshot.document(freeze_pin);launch=snapshot.document(launch_pin)
 require(type(freeze) is dict and set(freeze)=={'schema','utc','policy','entry'} and freeze['schema']=='CX1_IMPORTER_FREEZE_V001','FREEZE_SCHEMA')
 require(pin(freeze['policy']) and pin(freeze['entry']),'FREEZE_CODE_PINS')
 require(type(launch) is dict and set(launch)=={'schema','utc','register','runtime_capture','interpreter','freeze'} and launch['schema']=='SPECULATIVE_LAUNCH_L2_V001','DIRECT_LAUNCH_SCHEMA')
 require(launch['register']==register_pin and launch['runtime_capture']==direct_pin,'DIRECT_LAUNCH_ASSOCIATION')
 require(binding.get('campaign_capture')==campaign_pin,'CAMPAIGN_LAUNCH_ASSOCIATION')
 for label,record,event in [('direct',direct,launch),('campaign',campaign,binding)]:
  require(event.get('freeze')==freeze_pin,'LAUNCH_FREEZE_ASSOCIATION:'+label)
  identity=event.get('interpreter')
  require(type(identity) is dict and set(identity)=={'realpath','sha256'} and type(identity['realpath']) is str and identity['realpath'].startswith('/') and sha(identity['sha256']),'LAUNCH_INTERPRETER:'+label)
  actual=record.get('interpreter') or {}
  require(all(actual.get(k)==v for k,v in identity.items()),'CAPTURE_INTERPRETER_ASSOCIATION:'+label)
  require(utc(freeze['utc'])<utc(record.get('captured_utc'))<utc(event.get('utc')),'CAPTURE_OUTSIDE_LAUNCH_WINDOW:'+label)
 return {'prerequisites_only':True,'launch_association_verified':True,'authority':'caller-authenticated root pins'}
