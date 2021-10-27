from datetime import datetime
from time import sleep
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app import app
from app.app import on_startup

client = TestClient(app.app)
on_startup()


def status():
    response = client.get("/service/status")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_healthcheck_gtg():
    response = client.get("/service/healthcheck/gtg")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_ray_submit():
    response = client.post("/service/ray_submit")
    assert response.status_code == 200
    assert "status" in response.json()

def test_ray_result():
    response = client.get("/service/ray_result")
    assert response.status_code == 200
    assert "status" in response.json()
