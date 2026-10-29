#!/bin/bash
set -e

TARGET=${1:-"v1.0.0"}
echo ">>> INITIATING ROLLBACK TO: $TARGET"

export APP_VERSION=$TARGET

docker compose up -d --no-deps api

sleep 3
HEALTH=$(curl -s http://localhost:8000/health | grep '"status":"UP"' || true)

if [ -n "$HEALTH" ]; then
  echo ">>> Rollback successful! System restored to stable $TARGET."
  exit 0
else
  echo ">>> Rollback failed to restore healthy status!"
  exit 1
fi