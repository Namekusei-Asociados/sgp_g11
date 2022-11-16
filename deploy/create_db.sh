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
    -f /home/$USER/Documentos/IS2/sgp_g11/deploy/create_db.sql \
    --echo-all \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --set VERBOSITY=verbose \
    --set PGPASSWORD='admin' \
    --set PGOPTIONS='--client-min-messages=warning' \

echo "Base de datos creada correctamente"
exit 0