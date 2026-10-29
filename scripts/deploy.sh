#!/bin/bash
set -e

VERSION=${1:-"v1.0.0"}
echo ">>> Deploying Apex Operations API: $VERSION"

export APP_VERSION=$VERSION

docker build -t apex-operations-api:$VERSION .
docker compose up -d --no-deps api

echo "Verifying health probe..."
sleep 4
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ready || true)

if [ "$STATUS" == "200" ]; then
  echo ">>> Version $VERSION deployed and ready!"
  exit 0
else
  echo ">>> Deployment verification failed (HTTP $STATUS)!"
  exit 1
fi