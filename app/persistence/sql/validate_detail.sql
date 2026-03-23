WITH param AS (
	SELECT %(job_id)s AS job_id
),
detail AS (
	SELECT 
		raw_record_id,
		SUBSTRING(raw_content, 2, 10) AS account_number,
		SUBSTRING(raw_content, 12, 12) AS amount,
		SUBSTRING(raw_content, 24, 7) AS line_number
	FROM raw_record
	JOIN param ON raw_record.job_id = param.job_id
	WHERE SUBSTRING(raw_content, 1, 1) = 'D'
),
detail_validated as (
	SELECT
		raw_record_id,
		CASE 
			WHEN account_number ~ '^[0-9]+$' THEN CAST(account_number AS BIGINT) 
			ELSE NULL 
		END AS account_number,
		CASE 
			WHEN amount ~ '^[0-9]+$' THEN CAST(amount AS BIGINT) 
			ELSE NULL 
		END AS amount,
		CASE 
			WHEN line_number ~ '^[0-9]+$' THEN CAST(line_number AS INTEGER) 
			ELSE NULL 
		END AS line_number
	FROM detail
),
update_lines AS (
	UPDATE raw_record
	SET parsed_ok = TRUE
	FROM detail_validated
	WHERE detail_validated.raw_record_id = raw_record.raw_record_id
	AND detail_validated.account_number IS NOT NULL
	AND detail_validated.amount IS NOT NULL
	AND detail_validated.line_number IS NOT NULL
	RETURNING detail_validated.raw_record_id
),
insert_error AS (
	INSERT INTO validation_error(job_id, raw_record_id, error_type, error_code, error_message)
	SELECT 
		param.job_id,
		dv.raw_record_id,
		'BUSINESS_VALIDATION' AS error_type,
		CASE
			WHEN dv.account_number IS NULL THEN 'account_error'
			WHEN dv.amount IS NULL THEN 'amount_error'
			WHEN dv.line_number IS NULL THEN 'line_error'
		END AS error_code,
		CASE
			WHEN dv.account_number IS NULL THEN 'Account number invalid '
			WHEN dv.amount IS NULL THEN 'Amount invalid'
			WHEN dv.line_number IS NULL THEN 'Line number invalid'
		END AS error_message
	FROM detail_validated dv
	CROSS JOIN param
	WHERE dv.account_number IS NULL OR dv.amount IS NULL OR dv.line_number IS NULL
	RETURNING error_id
)
SELECT
	COUNT(*) AS error_count
FROM insert_error;