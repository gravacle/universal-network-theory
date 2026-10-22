"""0551 memory-pressure parsing; synthetic admission; no launch."""
import contextlib,hashlib,importlib.util,io,json
from pathlib import Path
r=Path(__file__).parent;p=r/'route_a_token_launcher_cx1v005.py';sp=importlib.util.spec_from_file_location('adaptive_parser_test',p);M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
M.G.admission=lambda *a,**k:{};original=M.subprocess.check_output;checks=[]
for name,text,want in [('zero','System-wide memory free percentage: 0%\n',0),('boundary','System-wide memory free percentage: 25%\n',25),('full','System-wide memory free percentage: 100%\n',100),('too_high','System-wide memory free percentage: 101%\n',None),('duplicate','System-wide memory free percentage: 50%\nSystem-wide memory free percentage: 40%\n',None),('missing','free memory 90%\n',None)]:
 M.subprocess.check_output=lambda *a,**k:text
 with contextlib.redirect_stdout(io.StringIO()):got=M.memory_free_percent()
 checks.append({'name':name,'passed':got==want})
def fail(*a,**k):raise TimeoutError('synthetic')
M.subprocess.check_output=fail
with contextlib.redirect_stdout(io.StringIO()):checks.append({'name':'timeout_refuses','passed':M.memory_free_percent() is None})
M.subprocess.check_output=original;actual=M.memory_free_percent();checks.append({'name':'actual_macos_read_only','passed':type(actual) is int and 0<=actual<=100,'free_percent':actual})
with (r/'MEMORY_PRESSURE_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED parsing and read-only macOS query; admission mocked; no launches','source':{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'checks':checks},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
