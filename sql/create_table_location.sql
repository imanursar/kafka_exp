CREATE TABLE table_location (
	latitude DOUBLE,
	longitude DOUBLE,
	event_ts BIGINT,
	ID VARCHAR,
	device_id VARCHAR PRIMARY KEY
) WITH (
   KAFKA_TOPIC  = 'device_location',
   VALUE_FORMAT = 'JSON',
   TIMESTAMP    = 'event_ts'
);
