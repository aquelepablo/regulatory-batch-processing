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
