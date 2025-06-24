FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* requirements.txt* ./

RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY . .

CMD ["python", "-m", "librenms_mcp"]
