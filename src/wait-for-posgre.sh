#!/bin/sh
set -e
host="$1"
shift
cmd="$@"
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$hostpsq" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres $POSTGRES_DB is unavailable $POSTGRES_USER - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"
# exec $cmd