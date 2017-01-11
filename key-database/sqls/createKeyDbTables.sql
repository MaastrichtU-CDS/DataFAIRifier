-- Script to create the tables in the CAT key database

DROP TABLE IF EXISTS sync;
DROP TABLE IF EXISTS source;
DROP TABLE IF EXISTS key_value;
DROP TABLE IF EXISTS key_type;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS cohort;

DROP SEQUENCE IF EXISTS keyType_id_seq;
DROP SEQUENCE IF EXISTS key_id_seq;

CREATE TABLE cohort
(
  id bigserial NOT NULL,
  name character varying(20),
  description character varying,
  CONSTRAINT cohort_pkey PRIMARY KEY (id)
);

ALTER TABLE cohort
  OWNER TO key_admin;

CREATE SEQUENCE keyType_id_seq;

CREATE TABLE key_type
(
  id bigint NOT NULL DEFAULT nextval('keyType_id_seq'),
  cohort_id bigint,
  name character varying(20),
  description character varying,
  CONSTRAINT "keyType_pkey" PRIMARY KEY (id),
  CONSTRAINT "keyType_cohortId" FOREIGN KEY (cohort_id)
      REFERENCES cohort (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE key_type
  OWNER TO key_admin;

CREATE INDEX "fki_keyType_cohortId"
  ON key_type
  USING btree
  (cohort_id);

CREATE TABLE patient
(
  id character varying NOT NULL,
  cohort_id bigint,
  last_name character varying(40),
  first_name character varying(40),
  birth_date date,
  CONSTRAINT "patientId" PRIMARY KEY (id),
  CONSTRAINT "patient_cohortId" FOREIGN KEY (cohort_id)
      REFERENCES cohort (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE patient
  OWNER TO key_admin;

CREATE INDEX "fki_patient_cohortId"
  ON patient
  USING btree
  (cohort_id);

CREATE SEQUENCE key_id_seq;

CREATE TABLE key_value
(
  id bigint NOT NULL DEFAULT nextval('key_id_seq'),
  patient_id character varying,
  key_type_id bigint,
  key_value character varying(40),
  CONSTRAINT key_pkey PRIMARY KEY (id),
  CONSTRAINT "key_keyTypeId" FOREIGN KEY (key_type_id)
      REFERENCES key_type (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT "key_patientId" FOREIGN KEY (patient_id)
      REFERENCES patient (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE key_value
  OWNER TO key_admin;

CREATE TABLE source
(
  id bigserial NOT NULL,
  cohort_id bigint,
  description character varying,
  CONSTRAINT source_pkey PRIMARY KEY (id),
  CONSTRAINT "source_cohortId" FOREIGN KEY (cohort_id)
      REFERENCES cohort (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE source
  OWNER TO key_admin;

CREATE INDEX "fki_source_cohortId"
  ON source
  USING btree
  (cohort_id);

CREATE TABLE sync
(
  id bigserial NOT NULL,
  patient_id character varying,
  source_id bigint,
  date date,
  CONSTRAINT sync_pkey PRIMARY KEY (id),
  CONSTRAINT "sync_patientId" FOREIGN KEY (patient_id)
      REFERENCES patient (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT "sync_sourceId" FOREIGN KEY (source_id)
      REFERENCES source (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE sync
  OWNER TO key_admin;

CREATE INDEX "fki_sync_patientId"
  ON sync
  USING btree
  (patient_id);

CREATE INDEX "fki_sync_sourceId"
  ON sync
  USING btree
  (source_id);

