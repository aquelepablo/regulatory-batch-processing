/*
DROP TABLE validation_error;
DROP TABLE raw_record;
DROP TABLE processing_job;
*/

CREATE TABLE processing_job(
	job_id 				BIGSERIAL PRIMARY KEY,
	file_name 			TEXT NOT NULL,
	received_at 		TIMESTAMPTZ NOT NULL,
	started_at 			TIMESTAMPTZ,
	finished_at 		TIMESTAMPTZ,
	status 				VARCHAR(50) NOT NULL 
		CHECK (status IN (
			'RECEIVED',
			'PROCESSING',
			'PROCESSED',
			'PROCESSED_WITH_ERRORS',
			'REJECTED'
		)),
	total_records 		BIGINT NOT NULL DEFAULT 0,
	total_errors 		BIGINT NOT NULL DEFAULT 0,
	general_error_message TEXT
);

CREATE TABLE raw_record(
	raw_record_id 	BIGSERIAL PRIMARY KEY,
	job_id 			BIGINT NOT NULL,
	line_number 	INT NOT NULL,
	raw_content 	TEXT NOT NULL,
	parsed_ok 		BOOLEAN NOT NULL DEFAULT FALSE,
	
	CONSTRAINT fk_raw_record_job
		FOREIGN KEY (job_id)
	        REFERENCES processing_job(job_id),
	
	CONSTRAINT uq_job_line
	    UNIQUE (job_id, line_number)
);

CREATE TABLE validation_error(
	error_id BIGSERIAL PRIMARY KEY,
	job_id BIGINT NOT NULL,
	raw_record_id BIGINT,
	error_type VARCHAR(50) NOT NULL
		CHECK (error_type IN (
	      'FILE_STRUCTURE',
	      'BUSINESS_VALIDATION',
	      'JOB'
	    )),
	error_code TEXT,
	error_message TEXT NOT NULL,

	CONSTRAINT fk_error_job
		FOREIGN KEY (job_id)
	        REFERENCES processing_job(job_id),

	--raw_record_id
	CONSTRAINT fk_error_raw_record
		FOREIGN KEY (raw_record_id)
	        REFERENCES raw_record(raw_record_id)
			
);

SELECT * FROM processing_job;
SELECT * FROM raw_record;
SELECT * FROM validation_error;

--SAMPLE INSERTS
DO $$
DECLARE v_job_id BIGINT;
		v_raw_record_id BIGINT;

BEGIN

	--FILE 1
	INSERT INTO processing_job(file_name, received_at, status) VALUES('file1', NOW(), 'RECEIVED') RETURNING job_id INTO v_job_id;
	INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message) VALUES(v_job_id, NULL, 'FILE_STRUCTURE', 'X01', 'FILE EMPTY');
	
	--FILE 2
	INSERT INTO processing_job(file_name, received_at, status) VALUES('file2', NOW(), 'RECEIVED') RETURNING job_id INTO v_job_id;
	
	INSERT INTO raw_record(job_id, line_number, raw_content) VALUES(v_job_id, 1, 'asdf') RETURNING raw_record_id INTO v_raw_record_id;
	INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message) VALUES(v_job_id, v_raw_record_id, 'BUSINESS_VALIDATION', 'B01', 'INCORRECT DATA');
	
	INSERT INTO raw_record(job_id, line_number, raw_content) VALUES(v_job_id, 2, 'asdf');
	INSERT INTO raw_record(job_id, line_number, raw_content) VALUES(v_job_id, 3, 'asdf');
	INSERT INTO raw_record(job_id, line_number, raw_content) VALUES(v_job_id, 4, 'asdf') RETURNING raw_record_id INTO v_raw_record_id;
	INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message) VALUES(v_job_id, v_raw_record_id, 'BUSINESS_VALIDATION', 'B01', 'INCORRECT DATA');
	
	INSERT INTO raw_record(job_id, line_number, raw_content) VALUES(v_job_id, 5, 'asdf') RETURNING raw_record_id INTO v_raw_record_id;

END $$