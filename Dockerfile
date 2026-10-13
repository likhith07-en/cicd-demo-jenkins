# ---------- base: runtime dependencies ----------
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- test: runs unit tests; build fails if they fail ----------
FROM base AS test
COPY requirements-dev.txt pytest.ini ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY app ./app
COPY tests ./tests
RUN pytest -q

# ---------- runtime: small, non-root production image ----------
FROM base AS runtime
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
RUN useradd --system --uid 10001 appuser
COPY app ./app
USER 10001
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app.app:app"]
