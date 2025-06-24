from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests

from .config import get_settings

logger = logging.getLogger(__name__)


class LibreNMSClient:
    def __init__(self, api_url: Optional[str] = None, api_token: Optional[str] = None) -> None:
        settings = get_settings()
        self.api_url = api_url or settings.api_url
        self.api_token = api_token or settings.api_token
        self.session = requests.Session()
        self.session.headers.update({'X-Auth-Token': self.api_token})

    def _url(self, path: str) -> str:
        return f"{self.api_url.rstrip('/')}/{path.lstrip('/')}"

    def request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        url = self._url(path)
        logger.debug("Request %s %s", method, url)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    # Devices
    def get_devices(self, *, limit: int | None = None, offset: int | None = None,
                    **params: Any) -> Dict[str, Any]:
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return self.request('GET', '/api/v0/devices', params=params)

    def add_device(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.request('POST', '/api/v0/devices', json=data)

    def get_device(self, hostname: str) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/devices/{hostname}')

    def update_device(self, hostname: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.request('PATCH', f'/api/v0/devices/{hostname}', json=data)

    def rename_device(self, hostname: str, new: str) -> Dict[str, Any]:
        return self.request('PATCH', f'/api/v0/devices/{hostname}/rename/{new}')

    def delete_device(self, hostname: str) -> Dict[str, Any]:
        return self.request('DELETE', f'/api/v0/devices/{hostname}')

    def discover_device(self, hostname: str) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/devices/{hostname}/discover')

    def get_device_availability(self, hostname: str) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/devices/{hostname}/availability')

    # Ports
    def get_ports(self, *, limit: int | None = None, offset: int | None = None,
                  **params: Any) -> Dict[str, Any]:
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return self.request('GET', '/api/v0/ports', params=params)

    def search_ports(self, search: str, field: Optional[str] = None,
                     *, limit: int | None = None, offset: int | None = None,
                     **params: Any) -> Dict[str, Any]:
        if field:
            path = f'/api/v0/ports/search/{field}/{search}'
        else:
            path = f'/api/v0/ports/search/{search}'
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return self.request('GET', path, params=params)

    def get_port_by_mac(self, mac: str, **params: Any) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/ports/mac/{mac}', params=params)

    def get_port(self, port_id: int, **params: Any) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/ports/{port_id}', params=params)

    def get_port_ips(self, port_id: int) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/ports/{port_id}/ip')

    def get_transceiver(self, port_id: int) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/ports/{port_id}/transceiver')

    def get_port_description(self, port_id: int) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/ports/{port_id}/description')

    def set_port_description(self, port_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.request('PATCH', f'/api/v0/ports/{port_id}/description', json=data)

    # Bills
    def get_bills(self, *, limit: int | None = None, offset: int | None = None,
                  **params: Any) -> Dict[str, Any]:
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return self.request('GET', '/api/v0/bills', params=params)

    def get_bill(self, bill_id: int) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/bills/{bill_id}')

    # Routing
    def get_bgp(self) -> Dict[str, Any]:
        return self.request('GET', '/api/v0/bgp')

    def get_bgp_peer(self, peer_id: int) -> Dict[str, Any]:
        return self.request('GET', f'/api/v0/bgp/{peer_id}')

    def edit_bgp_peer(self, peer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.request('POST', f'/api/v0/bgp/{peer_id}', json=data)

    def get_cbgp(self) -> Dict[str, Any]:
        return self.request('GET', '/api/v0/routing/bgp/cbgp')

    def get_ip_resources(self) -> Dict[str, Any]:
        return self.request('GET', '/api/v0/resources/ip/addresses')
