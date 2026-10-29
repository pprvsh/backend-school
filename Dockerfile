FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN groupadd --system django \
    && useradd --system --gid django --home-dir /app django \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=django:django . .

# collectstatic loads Django settings, so provide build-time values.
# These are not production secrets.
RUN SECRET_KEY="build-only-placeholder-not-for-production" \
    DEBUG=False \
    ALLOWED_HOSTS="localhost" \
    python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["gunicorn", "school_core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]