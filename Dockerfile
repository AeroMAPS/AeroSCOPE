# AeroSCOPE served by Voilà.
#
# The image carries the application only: no reverse proxy, no TLS, no domain.
# Routing, sub-path and resource limits are the deployment's business — see
# docker-compose.prod.yml in AeroMAPS_App, which builds this file and overrides
# the CMD below to serve the notebook under /aeroscope/.

FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Needed to compile the few dependencies without a manylinux wheel.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

# Install from poetry.lock, not from requirements.txt: the lock file is the one
# the repository keeps up to date, and it carries the ipywidgets/ipyvuetify
# versions that fix the widget display issue. Dependencies are a separate layer
# so that editing the notebook does not reinstall them.
COPY pyproject.toml poetry.lock /app/
RUN poetry install --only main --no-root

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
