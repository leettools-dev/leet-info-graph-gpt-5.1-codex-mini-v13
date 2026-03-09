#!/bin/bash
set -euo pipefail

LOG_DIR="logs"
PID_DIR="pids"
mkdir -p "$LOG_DIR" "$PID_DIR"

stop_old() {
  if [[ -f "$PID_DIR/backend.pid" ]]; then
    kill "$(cat "$PID_DIR/backend.pid")" >/dev/null 2>&1 || true
    rm -f "$PID_DIR/backend.pid"
  fi
  if [[ -f "$PID_DIR/frontend.pid" ]]; then
    kill "$(cat "$PID_DIR/frontend.pid")" >/dev/null 2>&1 || true
    rm -f "$PID_DIR/frontend.pid"
  fi
}

stop_old

env | grep -i "PORT" || true

python -m backend.app.main &> "$LOG_DIR/backend.log" &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$PID_DIR/backend.pid"

npm --prefix frontend run dev &> "$LOG_DIR/frontend.log" &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$PID_DIR/frontend.pid"

wait_deps() {
  while ! nc -z localhost "${BACKEND_PORT:-8000}"; do
    sleep 0.5
  done
}

wait_deps

cat <<EOF
Frontend: http://localhost:${FRONTEND_PORT:-3000}
Backend: http://localhost:${BACKEND_PORT:-8000}
EOF
