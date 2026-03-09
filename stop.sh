#!/bin/bash
set -euo pipefail

PID_DIR="pids"
if [[ -f "$PID_DIR/backend.pid" ]]; then
  kill "$(cat "$PID_DIR/backend.pid")" >/dev/null 2>&1 || true
  rm -f "$PID_DIR/backend.pid"
fi
if [[ -f "$PID_DIR/frontend.pid" ]]; then
  kill "$(cat "$PID_DIR/frontend.pid")" >/dev/null 2>&1 || true
  rm -f "$PID_DIR/frontend.pid"
fi
