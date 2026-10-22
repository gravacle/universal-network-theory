"""Internal scheduler adapter prototype. NOT an admission validator or launch entry.
The caller must validate external records under the work-dir lock after natural
planning. No production entry uses this module yet. Sources remain untouched.
"""
import ast
import copy
import hashlib
import types

SOURCE_SHA = 'd35d5d4a62e6e5b632eb10c59bf4c82c2b1d744f6ceba609399c02baa5ecfeb2'


def build_scheduler(raw, filename):
    """Compile exactly the pinned scheduler, adding one internal skip hook.

    raw is a single byte snapshot: pin and compilation use the same buffer.
    All scheduling, fallback paths and original call indices are preserved.
    """
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError('SCHEDULER_PIN_MISMATCH')
    tree = ast.parse(raw, filename)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run_campaign']
    if len(functions) != 1:
        raise ValueError('SCHEDULER_FUNCTION_SHAPE')
    fn = functions[0]
    loops = [n for n in fn.body if isinstance(n, ast.For) and ast.unparse(n.iter) == 'enumerate(specs)']
    if len(loops) != 1:
        raise ValueError('SCHEDULER_LOOP_SHAPE')
    fn.args.kwonlyargs.append(ast.arg(arg='_admitted_external'))
    fn.args.kw_defaults.append(ast.Constant(value=None))
    # Validate all hook arguments before the parent performs any write.
    fn.body[:0] = ast.parse("_admitted_external = _checked_external(_admitted_external, campaign, campaign_dir)").body
    loops[0].body[:0] = ast.parse("""
if i in _admitted_external:
    records[i] = _admitted_external[i]
    continue
""").body
    ast.fix_missing_locations(tree)
    module = types.ModuleType('_cx1_external_scheduler_prototype')
    module.__file__ = filename
    module.__dict__['_checked_external'] = checked_external
    exec(compile(tree, filename, 'exec'), module.__dict__)
    return module


def checked_external(records, campaign, campaign_dir):
    # Structural defense only. Full receipt/certificate/acceptance validation
    # belongs to the not-yet-integrated admission layer.
    if records is None:
        return {}
    if type(records) is not dict:
        raise ValueError('EXTERNAL_RECORD_MAP')
    calls = campaign.get('calls')
    if type(calls) is not list:
        raise ValueError('EXTERNAL_CALLS')
    from pathlib import Path
    base = Path(campaign_dir).resolve()
    out = {}
    for i, record in records.items():
        if type(i) is not int or not 0 <= i < len(calls):
            raise ValueError('EXTERNAL_INDEX')
        if type(record) is not dict or record.get('index') != i:
            raise ValueError('EXTERNAL_RECORD_INDEX')
        if record.get('execution_origin') != 'DIRECT_EXTERNAL' or record.get('status') not in ('OK', 'FAILED'):
            raise ValueError('EXTERNAL_RECORD_ORIGIN_STATUS')
        original = record.get('call_dir')
        if not isinstance(original, str) or not Path(original).is_absolute():
            raise ValueError('EXTERNAL_ABSOLUTE_CUSTODY')
        d = Path(original).resolve()
        if d == base or base in d.parents or str(d) != original:
            raise ValueError('EXTERNAL_ORIGINAL_CUSTODY')
        if (base / ('call_%04d' % i)).exists():
            raise ValueError('EXTERNAL_LOCAL_CALL_CONFLICT')
        out[i] = copy.deepcopy(record)
    return out
