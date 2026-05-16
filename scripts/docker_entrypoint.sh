#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Starting container as $(id -un)@$(hostname)"
if [ -f /app/.ml_install_failed ]; then
  echo "[entrypoint] ML dependencies were not installed during build. The API will run in degraded mode."
  echo "[entrypoint] See /tmp/ml_install.log for details if available."
fi

exec "$@"
