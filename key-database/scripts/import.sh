#!/bin/sh

psql -b --set ON_ERROR_STOP=on -h localhost -U postgres < /opt/sqls/createKeyDb.sql
psql -b --set ON_ERROR_STOP=on -h localhost -U postgres -d key_db < /opt/sqls/createKeyDbPatientIdFunction.sql
psql -b --set ON_ERROR_STOP=on -h localhost -U postgres -d key_db < /opt/sqls/createKeyDbTables.sql
psql -b --set ON_ERROR_STOP=on -h localhost -U postgres  < /opt/sqls/createKeyDbUsers.sql

psql -b --set ON_ERROR_STOP=on -h localhost -U postgres -c "ALTER USER key_admin WITH PASSWORD '$key_admin_PASS'"
psql -b --set ON_ERROR_STOP=on -h localhost -U postgres -c "ALTER USER spoon_key_db_select WITH PASSWORD '$spoon_select_PASS'"
psql -b --set ON_ERROR_STOP=on -h localhost -U postgres -c "ALTER USER spoon_key_db_update WITH PASSWORD '$spoon_update_PASS'"
psql -b --set ON_ERROR_STOP=on -h localhost -U postgres -c "ALTER USER ctp_key_db_select WITH PASSWORD '$ctp_key_select_PASS'"
