#!/usr/bin/env bash
set -euo pipefail

exec "${L14_PYTHON:?}" -B "${L14_CODE_ROOT:?}/aws/performance_preflight.py"
