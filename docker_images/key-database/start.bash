#!/bin/bash

# Example usage: ./start.bash  password_for_postgres

DATA_FOLDER=$(pwd)

docker run --net="host" --name keyDB \
    -v $DATA_FOLDER/data:/opt/data \
    -e PGDATA=/opt/data \
    -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=$1 -e POSTGRES_DB=postgres \
    -e key_admin_PASS='foo' \
    -e spoon_select_PASS='foo' \
    -e spoon_update_PASS='foo' \
    -e ctp_key_select_PASS='foo' \
    -ti  datafairifier/postgres

