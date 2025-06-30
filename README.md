# LibreNMS MCP

This project provides a Python SDK and a micro API to interact with a LibreNMS deployment.

## Requirements
- Python 3.12
- Docker / Docker Compose

## Quick start (dev)
1. Clone the repository.
2. Create a `.env` file with `LIBRENMS_API_URL` and `LIBRENMS_API_TOKEN`.
3. Build the Docker image: `docker-compose build`.
4. Run the development stack: `docker-compose up`.
5. Access the API at `http://localhost:8000/docs`.
6. Endpoints support pagination via `limit` and `offset` query params.
7. Search descriptions using `/query?q=your+text`.
8. Run tests with `docker-compose run --rm app pytest --cov`.


## Production
1. Build the image: `docker-compose --profile prod build`.
2. Start: `docker-compose --profile prod up -d`.

