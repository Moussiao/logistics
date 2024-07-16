FROM python:3.12.4-slim-bookworm AS development_build

# Needed for fixing permissions of files created by Docker:
ARG UID=1000 GID=1000

# Set environment variables
ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_ROOT_USER_ACTION=ignore \
  # tini
  TINI_VERSION=v0.19.0 \
  # poetry
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Systems deps (we don't use exact versions becauseit is hard to update them, pin when needed):
RUN apt-get update && apt-get upgrade -y \
  && apt-get --no-install-recommends install -y \
  bash \
  build-essential \
  curl \
  gettext \
  git \
  libmariadb-dev-compat \
  pkg-config \
  tzdata \
  wait-for-it \
  # Installing `tini` utility:
  # https://github.com/krallin/tini
  # Get architecture to download appropriate tini release:
  # See https://github.com/wemake-services/wemake-django-template/issues/1725
  && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
  && curl -o /usr/local/bin/tini -sSLO "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-${dpkgArch}" \
  && chmod +x /usr/local/bin/tini && tini --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Create user and set ownership and permissions as required
RUN groupadd -g "${GID}" -r web \
  && useradd -d "/code" -g web -l -r -u "${UID}" web \
  && chown web:web -R  "/code"


# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock pyproject.toml /code/

# Installing `poetry` package manager:
# Version is taken from poetry.lock, assuming it is generated with up-to-date version of poetry
RUN pip install poetry==$(cat poetry.lock |head -n1|awk -v FS='(Poetry |and)' '{print $2}')
RUN poetry --version

# Project initialization:
RUN --mount=type=cache,target="${POETRY_CACHE_DIR}" \
  poetry version \
  # Install deps
  && poetry run pip install -U pip \
  && poetry install

# This is a special case. We need to run this script as an entry point:
COPY ./docker-entrypoint.sh /docker-entrypoint.sh

# Setting up proper permissions:
RUN chmod +x '/docker-entrypoint.sh' \
  # Replacing line separator CRLF with LF for Windows users:
  && sed -i 's/\r$//g' '/docker-entrypoint.sh'

# Running as non-root user:
USER web

# We customize how our app is loaded with the custom entrypoint:
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]

COPY --chown=web:web . /code

