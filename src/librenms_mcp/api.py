from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Query

from .client import LibreNMSClient

logger = logging.getLogger(__name__)
app = FastAPI(title="LibreNMS MCP", version="0.1.0")
client = LibreNMSClient()


@app.get('/devices')
def list_devices(limit: int = Query(100, ge=1), offset: int = Query(0, ge=0)) -> Any:
    return client.get_devices(limit=limit, offset=offset)


@app.post('/devices')
def add_device(data: dict) -> Any:
    return client.add_device(data)


@app.get('/devices/{hostname}')
def device_detail(hostname: str) -> Any:
    try:
        return client.get_device(hostname)
    except Exception as exc:  # pragma: no cover - simplification
        logger.exception("device_detail failed")
        raise HTTPException(500, str(exc))


@app.patch('/devices/{hostname}')
def update_device(hostname: str, data: dict) -> Any:
    return client.update_device(hostname, data)


@app.patch('/devices/{hostname}/rename/{new}')
def rename_device(hostname: str, new: str) -> Any:
    return client.rename_device(hostname, new)


@app.delete('/devices/{hostname}')
def delete_device(hostname: str) -> Any:
    return client.delete_device(hostname)


@app.get('/devices/{hostname}/discover')
def discover_device(hostname: str) -> Any:
    return client.discover_device(hostname)


@app.get('/devices/{hostname}/availability')
def device_availability(hostname: str) -> Any:
    return client.get_device_availability(hostname)


@app.get('/ports')
def ports(limit: int = Query(100, ge=1), offset: int = Query(0, ge=0)) -> Any:
    return client.get_ports(limit=limit, offset=offset)


@app.get('/ports/{port_id}')
def port_detail(port_id: int) -> Any:
    return client.get_port(port_id)

# Bills endpoints
@app.get('/bills')
def bills(limit: int = Query(100, ge=1), offset: int = Query(0, ge=0)) -> Any:
    return client.get_bills(limit=limit, offset=offset)

@app.get('/bills/{bill_id}')
def bill_detail(bill_id: int) -> Any:
    return client.get_bill(bill_id)


# Additional endpoints would be defined similarly

@app.get('/query')
def natural_query(q: str, limit: int = Query(20, ge=1), offset: int = Query(0, ge=0)) -> Any:
    """Search descriptions of devices, ports and bills using a simple substring"""
    results = []
    devices = client.get_devices().get('devices', [])
    ports = client.get_ports().get('ports', [])
    bills = client.get_bills().get('bills', [])
    q_lower = q.lower()
    for d in devices:
        if q_lower in str(d.get('description', '')).lower():
            results.append({'type': 'device', 'item': d})
    for p in ports:
        if q_lower in str(p.get('description', '')).lower():
            results.append({'type': 'port', 'item': p})
    for b in bills:
        if q_lower in str(b.get('description', '')).lower():
            results.append({'type': 'bill', 'item': b})
    return {'results': results[offset:offset + limit]}

