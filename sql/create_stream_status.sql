CREATE STREAM stream_status (
	sound DOUBLE,
	temperature DOUBLE,
	altitude DOUBLE,
	event_ts BIGINT,
	ID VARCHAR,
	device_id VARCHAR
) WITH (
	KAFKA_TOPIC  = 'device_status',
	VALUE_FORMAT = 'JSON',
	TIMESTAMP    = 'event_ts'
);
