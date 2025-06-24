from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .client import LibreNMSClient

logger = logging.getLogger(__name__)
app = FastAPI(title="LibreNMS MCP", version="0.1.0")
client = LibreNMSClient()


@app.get('/devices')
def list_devices() -> Any:
    return client.get_devices()


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
def ports() -> Any:
    return client.get_ports()


@app.get('/ports/{port_id}')
def port_detail(port_id: int) -> Any:
    return client.get_port(port_id)


# Additional endpoints would be defined similarly
