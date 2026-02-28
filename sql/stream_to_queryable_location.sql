CREATE TABLE QUERYABLE_TABLE_LOCATION AS
SELECT
  device_id,
  LATEST_BY_OFFSET(latitude)     AS latitude,
  LATEST_BY_OFFSET(longitude)    AS longitude,
  LATEST_BY_OFFSET(event_ts)	 AS event_ts,
  LATEST_BY_OFFSET(id)	 		 AS id
FROM STREAM_LOCATION
GROUP BY device_id;
