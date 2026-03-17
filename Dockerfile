FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /lakehouse
ENV PATH="/lakehouse/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY pipeline/ ./pipeline/

ENTRYPOINT ["uv", "run", "python", "main.py"]