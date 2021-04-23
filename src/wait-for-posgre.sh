#!/bin/sh
set -e
host="$1"
shift
cmd="$@"
echo "Postgres is up - executing command"
until nc -z host; do
  echo "Postgres $POSTGRES_DB is unavailable $POSTGRES_USER - sleeping"
  sleep 1
done
  
echo "Postgres is up - executing command"
# exec $cmd