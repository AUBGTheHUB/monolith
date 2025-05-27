#!/bin/sh
set -e

# Read the Cloudflare API token from the Docker secret file and export it as an environment variable.
# Default to an empty string if the secret file doesn't exist, though Docker Swarm should always create it if
# configured.
# https://docs.docker.com/engine/swarm/secrets/
# https://caddyserver.com/docs/caddyfile/concepts#environment-variables
SECRET_FILE_PATH="/run/secrets/cloudflare-api-token"

if [ -f SECRET_FILE_PATH ]; then
  CLOUDFLARE_API_TOKEN=$(cat "$SECRET_FILE_PATH")
  export CLOUDFLARE_API_TOKEN
else
  echo "WARNING: Cloudflare API token secret file '$SECRET_FILE_PATH' not found."
  export CLOUDFLARE_API_TOKEN=""
fi

# https://stackoverflow.com/questions/32255814/what-purpose-does-using-exec-in-docker-entrypoint-scripts-serve/32261019#32261019
# https://man7.org/linux/man-pages/man3/exec.3.html
exec "$@"
