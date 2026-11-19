# AeroSCOPE served by Voilà.
#
# The image carries the application only: no reverse proxy, no TLS, no domain.
# Routing, sub-path and resource limits are the deployment's business — see
# docker-compose.prod.yml in AeroMAPS_App, which builds this file and overrides
# the CMD below to serve the notebook under /aeroscope/.

FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Needed to compile the few dependencies without a manylinux wheel.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.20 /uv /usr/local/bin/uv

WORKDIR /app

# Install from uv.lock so the image runs the versions CI tests, including the
# ipywidgets/ipyvuetify ones that fix the widget display. The project itself is
# not installed: Voila runs the notebook from /app, and a git archive gives
# setuptools_scm no version. Dependencies are their own layer so that editing
# the notebook does not reinstall them.
COPY pyproject.toml uv.lock /app/
RUN uv sync --locked --no-install-project --no-default-groups --no-cache

COPY . /app

EXPOSE 8080

# Standalone default: AeroSCOPE at the root of port 8080.
CMD ["voila", "/app/aeroscope/AeroSCOPE.ipynb", \
     "--port=8080", \
     "--Voila.ip=0.0.0.0", \
     "--no-browser", \
     "--MappingKernelManager.cull_idle_timeout=600", \
     "--MappingKernelManager.cull_interval=120", \
     "--VoilaConfiguration.file_whitelist=['.*\\.(png|jpg|gif|xlsx|ico|pdf|json|zip)']"]
