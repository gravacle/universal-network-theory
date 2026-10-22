#!/usr/bin/env python3
"""hashes_stage0_successor_c2v002 -- writes HASHES_V002.txt: sha256 (from bytes) and size of every c2v002 file.

No directory is walked. The files are: the explicitly named c2v002 and c2v001 top-level files (c2v001's own
HASHES.txt covers its dev/ and test_runs/ trees), the explicitly named dev_v002 files, every file listed in each
named run directory's FILES_WRITTEN_test_stage0_successor_c2v002.json (each re-hashed and checked against the
recorded sha256), and the mutation copies named in dev_v002/mutation/MUTATION_SUMMARY_C2V002.json.
Usage: python3 -I -B hashes_stage0_successor_c2v002.py   (writes HASHES_V002.txt next to this script, exclusive)
"""
import datetime
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
FW = 'FILES_WRITTEN_test_stage0_successor_c2v002.json'

TOP_V002 = ['README_STAGE0_SUCCESSOR_C2V002.md', 'AST_IDENTITY_STAGE0_SUCCESSOR_C2V002.md',
            'DIFF_v003g_to_stage0_successor_c2v002.diff', 'DIFF_stage0_successor_c2v001_to_c2v002.diff',
            'prediction_freeze_c2v003g_stage0_c2v002.py', 'build_stage0_successor_c2v002.py',
            'test_stage0_successor_c2v002.py', 'make_reports_stage0_successor_c2v002.py',
            'hashes_stage0_successor_c2v002.py']
TOP_V001 = ['README_STAGE0_SUCCESSOR_C2V001.md', 'AST_IDENTITY_STAGE0_SUCCESSOR_C2V001.md',
            'DIFF_v003g_to_stage0_successor_c2v001.diff', 'prediction_freeze_c2v003g_stage0_c2v001.py',
            'build_stage0_successor_c2v001.py', 'test_stage0_successor_c2v001.py',
            'make_reports_stage0_successor_c2v001.py', 'HASHES.txt']
RECORD_RUNS = ['test_runs_c2v002/run_1_20261019T171802Z', 'test_runs_c2v002/run_2_20261019T171842Z']
DEV_FILES = ['dev_v002/build_stage0_successor_c2v002_draft01.py', 'dev_v002/test_stage0_successor_c2v002_draft01.py',
             'dev_v002/mutate_stage0_successor_c2v002.py',
             'dev_v002/draft_01/prediction_freeze_c2v003g_stage0_c2v002.py',
             'dev_v002/draft_02/prediction_freeze_c2v003g_stage0_c2v002.py',
             'dev_v002/reports_check/DIFF_v003g_to_stage0_successor_c2v002.diff',
             'dev_v002/reports_check/DIFF_stage0_successor_c2v001_to_c2v002.diff',
             'dev_v002/reports_check/AST_IDENTITY_STAGE0_SUCCESSOR_C2V002.md',
             'dev_v002/mutation/MUTATION_SUMMARY_C2V002.json']
DEV_RUNS = ['dev_v002/run_draft01_a', 'dev_v002/run_draft02_a', 'dev_v002/run_draft02_b']
MUTATION_DIR = 'dev_v002/mutation'


def file_line(rel):
    with open(os.path.join(HERE, rel), 'rb') as fh:
        raw = fh.read()
    return '%s  %d  %s' % (hashlib.sha256(raw).hexdigest(), len(raw), rel), hashlib.sha256(raw).hexdigest()


def run_lines(run_rel, problems):
    lines = [file_line(os.path.join(run_rel, FW))[0]]
    with open(os.path.join(HERE, run_rel, FW), 'rb') as fh:
        listing = json.loads(fh.read().decode('utf-8'))
    for f in listing['files']:
        rel = os.path.join(run_rel, f['path'])
        if f['kind'] == 'symlink':
            target = os.readlink(os.path.join(HERE, rel))
            if target != f['target']:
                problems.append('symlink target changed: %s' % rel)
            lines.append('symlink  ->  %s  %s' % (target, rel))
        else:
            line, digest = file_line(rel)
            if digest != f['sha256']:
                problems.append('sha256 differs from the run record: %s' % rel)
            lines.append(line)
    return lines


def main():
    if not (sys.flags.isolated and sys.flags.dont_write_bytecode):
        raise SystemExit('run with python3 -I -B')
    problems = []
    sections = [('c2v002 deliverables', [file_line(r)[0] for r in TOP_V002]),
                ('c2v001 top-level files (unadopted; unchanged; HASHES.txt covers c2v001 dev/ and test_runs/)',
                 [file_line(r)[0] for r in TOP_V001])]
    for run in RECORD_RUNS:
        sections.append(('record run %s (files from its FILES_WRITTEN list)' % run, run_lines(run, problems)))
    sections.append(('dev_v002 named files', [file_line(r)[0] for r in DEV_FILES]))
    for run in DEV_RUNS:
        sections.append(('dev run %s (files from its FILES_WRITTEN list)' % run, run_lines(run, problems)))
    with open(os.path.join(HERE, MUTATION_DIR, 'MUTATION_SUMMARY_C2V002.json'), 'rb') as fh:
        summary = json.loads(fh.read().decode('utf-8'))
    for m in summary['mutations']:
        name = m['mutation']
        mlines = [file_line(os.path.join(MUTATION_DIR, name, 'prediction_freeze_c2v003g_stage0_c2v002.py'))[0],
                  file_line(os.path.join(MUTATION_DIR, name, 'MUTATION_RESULT.json'))[0]]
        mlines += run_lines(os.path.join(MUTATION_DIR, 'run_' + name), problems)
        sections.append(('mutation %s' % name, mlines))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    n = sum(len(lines) for _t, lines in sections)
    out = ['# HASHES_V002 -- stage0_successor_c2, written %s by hashes_stage0_successor_c2v002.py' % stamp,
           '# sha256 from bytes and size of every c2v002 file (and the c2v001 top-level files), from explicit name '
           'lists and the runs\' own FILES_WRITTEN lists; no directory walk. This file does not list itself.',
           '# Format: sha256  bytes  relative_path   |   symlink  ->  target  relative_path',
           '# entries: %d; FILES_WRITTEN cross-check: %s' % (n, 'all match' if not problems else
                                                              'PROBLEMS %s' % problems[:5]), '']
    for title, lines in sections:
        out.append('## ' + title)
        out.extend(lines)
        out.append('')
    with open(os.path.join(HERE, 'HASHES_V002.txt'), 'xb') as fh:
        fh.write('\n'.join(out).encode('utf-8'))
    print('wrote HASHES_V002.txt: %d entries; problems: %s' % (n, problems or 'none'))
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main())
