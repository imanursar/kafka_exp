CREATE TABLE QUERYABLE_TABLE_STATUS AS
SELECT
  device_id,
  LATEST_BY_OFFSET(temperature)  AS temperature,
  LATEST_BY_OFFSET(sound)        AS sound,
  LATEST_BY_OFFSET(altitude)     AS altitude,
  LATEST_BY_OFFSET(event_ts)	 AS event_ts,
  LATEST_BY_OFFSET(id)	 		 AS id
FROM STREAM_STATUS
GROUP BY device_id;
