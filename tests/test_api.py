import os, sys; sys.path.insert(0, os.path.abspath("src"))
from fastapi.testclient import TestClient

from librenms_mcp.api import app


def test_openapi_json():
    client = TestClient(app)
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert 'paths' in response.json()

def test_list_devices(monkeypatch):
    def fake_get_devices(**kwargs):
        return {'devices': []}

    import librenms_mcp.api as api_mod
    monkeypatch.setattr(api_mod.client, "get_devices", fake_get_devices)
    client = TestClient(app)
    resp = client.get('/devices')
    assert resp.status_code == 200
    assert resp.json() == {'devices': []}
