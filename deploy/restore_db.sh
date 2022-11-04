#!/bin/bash

set -e
set -u

export DBHOST=localhost
export DBPORT=5432

psql \
    -X \
    -U postgres \
    password=admin \
    -h $DBHOST \
    -f /home/$USER/Documents/is2/sgp_g11/deploy/create_db.sql \
    --echo-all \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --set VERBOSITY=verbose \
    --set PGPASSWORD='admin' \
    --set PGOPTIONS='--client-min-messages=warning' \


PGPASSWORD="admin" /usr/bin/pg_restore --host "localhost" --port "5432" --username "postgres" --dbname "sgp_db" --verbose "/home/$USER/Documents/is2/sgp_g11/copy_con_2_users"

#cd ..

#sh ./scripts/Permisos.sh

echo "sql script successful"
exit 0

