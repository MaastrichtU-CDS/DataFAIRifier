CREATE OR REPLACE FUNCTION fn_getpatientid(IN keyvalue character varying, IN keytypeid bigint, OUT newpatientid bigint)
  RETURNS bigint AS
$BODY$DECLARE
-- =============================================
-- Author: Andre Dekker
-- Create date: 8 July 2013
-- Description:	function that checks if a
-- patient is already registered based on the
-- key value and type. If patient is already
-- registered, the function return the patientId
-- If not the function generates a new patientId
-- =============================================

    lower integer := 100000000;
    upper integer := 999999999;
    newPatientIdExist bit :=1;
    existingPatientId bigint;

BEGIN
SELECT patient_id INTO existingPatientId FROM key_value WHERE key_value=keyValue AND key_type_id=keyTypeId;
IF existingPatientId IS NULL
	-- Patient not yet registered
	THEN
	WHILE newPatientIdExist LOOP
		-- generate random newPatientId
		newPatientId := round( CAST(((upper-lower)*random()+lower) AS numeric),0);
		-- check if newPatientId does not exist yet
		SELECT id INTO existingPatientId FROM patient WHERE id=CAST(newPatientId AS character varying);
		IF existingPatientId IS NULL
			THEN newPatientIdExist :=0;
		END IF;
	END LOOP;
	-- Patient already registered
	ELSE newPatientId := existingPatientId;
	END IF;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION fn_getpatientid(character varying, bigint)
  OWNER TO key_admin;

