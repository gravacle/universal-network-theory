#!/usr/bin/env bash
set -uo pipefail

status=2
"${L14_PYTHON}" -B /opt/l14/current/aws/aws_branch_once.py
status=$?
sync
echo "L14_BRANCH_WRAPPER_EXIT status=${status}; instance remains available for inspection"
exit "${status}"
