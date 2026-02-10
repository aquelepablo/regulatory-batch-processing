WITH param AS (
	SELECT %(job_id)s AS job_id
),
),
detail_amount AS (
	SELECT 
		SUBSTRING(raw_content, 12, 12) AS amount
	FROM raw_record
	JOIN param ON raw_record.job_id = param.job_id
	WHERE SUBSTRING(raw_content, 1, 1) = 'D'
),
detail_validated as (
	SELECT
		CASE 
			WHEN amount ~ '^[0-9]+$' THEN CAST(amount AS BIGINT) 
			ELSE 0 
		END AS amount
	FROM detail_amount
),
detail_sum as (
	SELECT 
		COUNT(*) AS detail_count,
		SUM(amount) AS detail_amount
	FROM detail_validated
),
trailer AS (
		SELECT 	
			raw_record_id, 
			SUBSTRING(raw_content, 2, 8) AS trailer_count,
			SUBSTRING(raw_content, 10, 14) AS trailer_amount
		FROM raw_record, param
		WHERE raw_record.job_id = param.job_id AND SUBSTRING(raw_content, 1, 1) = 'T'
),
trailer_validated AS (
		SELECT 	
			raw_record_id, 
			CASE WHEN trailer_count ~ '^[0-9]+$' THEN CAST(trailer_count AS INTEGER) 
				ELSE 0 
			END AS trailer_count,
			CASE 
				WHEN trailer_amount ~ '^[0-9]+$' THEN CAST(trailer_amount AS INTEGER) 
				ELSE 0 
			END AS trailer_amount
		FROM trailer
)
SELECT
    t.raw_record_id,
    'TRAILER_TOTAL_MISMATCH' AS error_code,
    CASE
        WHEN t.trailer_count <> d.detail_count
            THEN 'Trailer total records does not match detail count'
        WHEN t.trailer_amount <> d.detail_amount
            THEN 'Trailer total amount does not match detail sum'
    END AS error_message
FROM trailer_validated t, detail_sum d
WHERE
    t.trailer_count <> d.detail_count
 OR t.trailer_amount <> d.detail_amount;
