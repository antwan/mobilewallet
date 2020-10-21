#!/bin/bash

set -e

# This optional environment variable ensures the DB server is up and running prior to running further commands
if [[ "$WAIT_FOR_POSTGRES" =~ "TRUE" ]]; then
    echo "Waiting for Postgres at db"
    until PGPASSWORD=admin psql -h "db" -U "admin" -c '\l' > /dev/null 2>&1; do
        echo "."
        sleep 5
    done
    echo "Postgres is up!"
fi

/bin/bash -c "$@"
