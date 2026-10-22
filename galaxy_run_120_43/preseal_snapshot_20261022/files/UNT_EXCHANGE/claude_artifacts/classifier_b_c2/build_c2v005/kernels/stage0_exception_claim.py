"""A173 claim recognition only; callers must validate block identity and facts."""
MARKER = 'STAGE0_RECEIPT_RULE_EXCEPTION'


def exception_claim(diagnostics, rule_a, rule_b):
    """Return NORMAL, EXCEPTION, or BLOCK_EXCEPTION_PATH after diagnostics validation."""
    if not isinstance(diagnostics, list) or any(not isinstance(x, str) for x in diagnostics):
        raise ValueError('BLOCK_DIAGNOSTICS')
    claims = [i for i, value in enumerate(diagnostics) if value.startswith(MARKER)]
    if not claims:
        return 'NORMAL'
    if len(claims) != 1 or claims[0] != len(diagnostics) - 1:
        return 'BLOCK_EXCEPTION_PATH'
    entry = diagnostics[-1]
    prefix = MARKER + ': '
    if not entry.startswith(prefix) or not entry[len(prefix):].isidentifier():
        return 'BLOCK_EXCEPTION_PATH'
    if rule_a is not False or rule_b is not False:
        return 'BLOCK_EXCEPTION_PATH'
    return 'EXCEPTION'
