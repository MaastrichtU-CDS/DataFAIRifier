-- Script to create the key database for CAT installation
-- Create the KEY DB owner
CREATE USER key_admin WITH PASSWORD 'changeme';

CREATE DATABASE key_db
  WITH OWNER = key_admin
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       CONNECTION LIMIT = -1;
GRANT ALL ON DATABASE key_db TO key_admin;
COMMIT;
