#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker n'est pas installé ou non disponible dans PATH." >&2
  exit 1
fi

echo "Building and starting containers..."
docker compose up --build -d

echo "Waiting for API health check..."
RETRIES=30
SLEEP=2
URL="http://localhost:8000/api/v1/health"
for i in $(seq 1 $RETRIES); do
  if curl -s $URL | grep -q '"status"'; then
    echo "API ready"
    docker compose ps
    exit 0
  fi
  echo "- waiting ($i/$RETRIES)"
  sleep $SLEEP
done

echo "API did not become ready in time. See logs:"
docker compose logs --tail=200 api
exit 2
