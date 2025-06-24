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


def test_devices_pagination(monkeypatch):
    recorded = {}

    def fake_get_devices(**kwargs):
        recorded.update(kwargs)
        return {'devices': []}

    import librenms_mcp.api as api_mod
    monkeypatch.setattr(api_mod.client, 'get_devices', fake_get_devices)
    client = TestClient(app)
    resp = client.get('/devices?limit=10&offset=5')
    assert resp.status_code == 200
    assert recorded['limit'] == 10
    assert recorded['offset'] == 5


def test_query(monkeypatch):
    def fake_get_devices(*a, **k):
        return {'devices': [{'description': 'foo device'}]}

    def fake_get_ports(*a, **k):
        return {'ports': [{'description': 'bar port'}]}

    def fake_get_bills(*a, **k):
        return {'bills': [{'description': 'baz bill'}]}

    import librenms_mcp.api as api_mod
    monkeypatch.setattr(api_mod.client, 'get_devices', fake_get_devices)
    monkeypatch.setattr(api_mod.client, 'get_ports', fake_get_ports)
    monkeypatch.setattr(api_mod.client, 'get_bills', fake_get_bills)
    client = TestClient(app)
    resp = client.get('/query?q=foo')
    assert resp.status_code == 200
    assert resp.json()['results'][0]['type'] == 'device'
