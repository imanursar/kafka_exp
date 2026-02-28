CREATE STREAM stream_location (
	latitude DOUBLE,
	longitude DOUBLE,
	event_ts BIGINT,
	ID VARCHAR,
	device_id VARCHAR
) WITH (
	KAFKA_TOPIC  = 'device_location',
	VALUE_FORMAT = 'JSON',
	TIMESTAMP    = 'event_ts'
);
