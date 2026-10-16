# syntax=docker/dockerfile:1

ARG PYTHON_IMAGE=python:3.13-slim-bookworm
FROM ${PYTHON_IMAGE}

ARG AERODROME_REF=v3.4.136

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/aerodrome

RUN curl -fsSL "https://github.com/preston-peterson/aerodrome/archive/refs/tags/${AERODROME_REF}.tar.gz" -o /tmp/aerodrome.tar.gz \
    && tar -xzf /tmp/aerodrome.tar.gz --strip-components=1 -C /opt/aerodrome \
    && rm /tmp/aerodrome.tar.gz

RUN python -m venv "$VIRTUAL_ENV" \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.py /usr/local/bin/docker-entrypoint.py
RUN chmod +x /usr/local/bin/docker-entrypoint.py

VOLUME ["/data"]
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.py"]
CMD ["/opt/venv/bin/python", "main.py", "start"]
