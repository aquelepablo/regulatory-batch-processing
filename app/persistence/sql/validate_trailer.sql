WITH param AS (
	SELECT %(job_id)s AS job_id
),
detail AS (
		SELECT COUNT(*) AS total FROM raw_record, param
		WHERE raw_record.job_id = param.job_id AND SUBSTRING(raw_content, 1, 1) = 'D'
),
trailer AS (
		SELECT raw_record_id, CAST(SUBSTRING(raw_content, 2, 8) AS INTEGER) AS total FROM raw_record, param
		WHERE raw_record.job_id = param.job_id AND SUBSTRING(raw_content, 1, 1) = 'T'
)
SELECT trailer.total = detail.total AS total_records_is_valid, raw_record_id, 'Trailer total records different from total detail records'
FROM trailer, detail;
