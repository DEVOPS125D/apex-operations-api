from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_health_check_returns_200():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "UP"


@patch("app.main.check_db_connection", return_value=True)
def test_readiness_healthy(mock_check):
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "READY"


@patch("app.main.check_db_connection", return_value=False)
def test_readiness_degraded(mock_check):
    res = client.get("/ready")
    assert res.status_code == 503


@patch("app.main.redis_client")
def test_create_operation_valid(mock_redis):
    mock_redis.incr.return_value = 1
    mock_redis.hset.return_value = 1
    payload = {"task_name": "Sync Pods", "operator": "Bilal", "priority": "HIGH"}
    res = client.post("/api/v1/operations", json=payload)
    assert res.status_code == 201
    assert res.json()["id"] == 1


def test_create_operation_invalid_payload():
    payload = {"task_name": "X", "operator": "B"}
    res = client.post("/api/v1/operations", json=payload)
    assert res.status_code == 422