"""Independent validation of root gate and commitment records; no IO.
Gate document hashes permit uppercase hex, matching v003g/V-F1 contract.
"""
import re
class ContractDefect(ValueError):pass

def exact(value,keys):
    if type(value) is not dict or set(value)!=set(keys):raise ContractDefect('keys')

def text(value):
    if type(value) is not str or not value:raise ContractDefect('text')

def gate_index(record):
    exact(record,('schema','gates'))
    if record['schema']!='GATE_STATUS_LIST_C4V001' or type(record['gates']) is not list:raise ContractDefect('schema')
    result={}
    for gate in record['gates']:
        exact(gate,('gate_sha256','status','pinned_by_entry'))
        sha=gate['gate_sha256']
        if type(sha) is not str or re.fullmatch('[0-9a-fA-F]{64}',sha) is None:raise ContractDefect('sha')
        sha=sha.lower()
        if sha in result:raise ContractDefect('duplicate gate')
        if gate['status'] not in ('ON-TIME','LATE'):raise ContractDefect('status')
        text(gate['pinned_by_entry'])
        result[sha]=gate['status']
    return result

def commitment(record):
    # This is never a classification stop and blanks no scientific output.
    try:
        exact(record,('schema','status','stops_or_changes'))
        if record['schema']!='PHASE2_COMMITMENT_STATUS_C4V001':raise ContractDefect('schema')
        status=record['status'];changes=record['stops_or_changes']
        if type(changes) is not list:raise ContractDefect('changes')
        if status not in ('COMMITTED','EXPLORATORY'):raise ContractDefect('status')
        if (status=='COMMITTED') != (len(changes)==0):raise ContractDefect('status changes disagreement')
        for change in changes:
            exact(change,('what','entry'));text(change['what']);text(change['entry'])
        return status,None
    except ContractDefect:
        return 'EXPLORATORY','COMMITMENT_STATUS_DEFECT'
