WITH param AS (
	SELECT %(job_id)s AS job_id
),
detail AS (
		SELECT COUNT(*) AS detail_count, SUM(CAST(SUBSTRING(raw_content, 12, 12) AS INTEGER)) AS detail_amount 
		FROM raw_record, param
		WHERE raw_record.job_id = param.job_id AND SUBSTRING(raw_content, 1, 1) = 'D'
),
trailer AS (
		SELECT 	raw_record_id, 
				CAST(SUBSTRING(raw_content, 2, 8) AS INTEGER) AS trailer_count,
				CAST(SUBSTRING(raw_content, 10, 14) AS INTEGER) AS trailer_amount
		FROM raw_record, param
		WHERE raw_record.job_id = param.job_id AND SUBSTRING(raw_content, 1, 1) = 'T'
)
SELECT
    trailer.raw_record_id,
    'TRAILER_TOTAL_MISMATCH' AS error_code,
    CASE
        WHEN trailer.trailer_count <> detail.detail_count
            THEN 'Trailer total records does not match detail count'
        WHEN trailer.trailer_amount <> detail.detail_amount
            THEN 'Trailer total amount does not match detail sum'
    END AS error_message
FROM trailer, detail
WHERE
    trailer.trailer_count <> detail.detail_count
 OR trailer.trailer_amount <> detail.detail_amount;
