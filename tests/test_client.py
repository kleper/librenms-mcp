import os, sys; sys.path.insert(0, os.path.abspath("src"))
from librenms_mcp.client import LibreNMSClient


def test_client_base_url():
    client = LibreNMSClient(api_url="http://example.com", api_token="t")
    assert client._url('/test') == 'http://example.com/test'

def test_request_build(monkeypatch):
    calls = []

    class FakeResponse:
        def __init__(self):
            self.status_code = 200
        def raise_for_status(self):
            pass
        def json(self):
            return {'ok': True}

    def fake_request(method, url, **kwargs):
        calls.append((method, url))
        return FakeResponse()

    client = LibreNMSClient(api_url='http://example.com', api_token='t')
    monkeypatch.setattr(client.session, 'request', fake_request)
    resp = client.get_devices()
    assert calls[0][0] == 'GET'
    assert calls[0][1] == 'http://example.com/api/v0/devices'
    assert resp == {'ok': True}

def test_update_device(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {'updated': True}

    def fake_request(method, url, **kwargs):
        assert method == 'PATCH'
        assert url.endswith('/api/v0/devices/test')
        assert kwargs['json'] == {'foo': 'bar'}
        return FakeResponse()

    client = LibreNMSClient(api_url='http://example.com', api_token='t')
    monkeypatch.setattr(client.session, 'request', fake_request)
    resp = client.update_device('test', {'foo': 'bar'})
    assert resp == {'updated': True}

def test_delete_device(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {'deleted': True}

    def fake_request(method, url, **kwargs):
        assert method == 'DELETE'
        assert url.endswith('/api/v0/devices/test')
        return FakeResponse()

    client = LibreNMSClient(api_url='http://example.com', api_token='t')
    monkeypatch.setattr(client.session, 'request', fake_request)
    resp = client.delete_device('test')
    assert resp == {'deleted': True}

def test_other_calls(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {}

    def fake_request(method, url, **kwargs):
        return FakeResponse()

    client = LibreNMSClient(api_url='http://example.com', api_token='t')
    monkeypatch.setattr(client.session, 'request', fake_request)
    client.rename_device('host', 'new')
    client.discover_device('host')
    client.get_device_availability('host')
    client.get_ports()
    client.get_port(1)
    client.get_bills()
    client.get_bill(1)
    client.get_bgp()
    client.get_bgp_peer(1)
    client.edit_bgp_peer(1, {})
    client.get_cbgp()
    client.get_ip_resources()
