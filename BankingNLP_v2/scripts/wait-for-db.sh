#!/usr/bin/env bash
host="$1"
port="$2"
shift 2
until nc -z "$host" "$port"; do
  echo "Waiting for postgres..."
  sleep 1
done
exec "$@"
