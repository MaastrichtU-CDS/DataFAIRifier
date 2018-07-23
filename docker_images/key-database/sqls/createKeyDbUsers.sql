
CREATE USER spoon_key_db_select WITH PASSWORD 'changeme';
GRANT CONNECT ON DATABASE key_db TO spoon_key_db_select;
GRANT SELECT ON ALL TABLES IN SCHEMA public to spoon_key_db_select;

CREATE USER spoon_key_db_update WITH PASSWORD 'changeme';
GRANT CONNECT ON DATABASE key_db TO spoon_key_db_update;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE, TRIGGER ON ALL TABLES IN SCHEMA public to spoon_key_db_update;
GRANT SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public to spoon_key_db_update;

CREATE USER ctp_key_db_select WITH PASSWORD 'changeme';
GRANT CONNECT ON DATABASE key_db TO ctp_key_db_select;
GRANT SELECT ON ALL TABLES IN SCHEMA public to ctp_key_db_select;

