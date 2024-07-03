#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

: "${DJANGO_DATABASE_HOST:=db}"
: "${DJANGO_DATABASE_PORT:=3306}"

# We need this line to make sure that this container is started
# after the one with postgres:
wait-for-it \
  --host=${DJANGO_DATABASE_HOST} \
  --port=${DJANGO_DATABASE_PORT} \
  --timeout=90 \
  --strict

echo "DB ${DJANGO_DATABASE_HOST}:${DJANGO_DATABASE_PORT} is up"

# Evaluating passed command (do not touch):
exec $cmd

