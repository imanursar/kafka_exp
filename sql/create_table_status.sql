CREATE TABLE table_status (
	sound DOUBLE,
	temperature DOUBLE,
	altitude DOUBLE,
	event_ts BIGINT,
	ID VARCHAR,
	device_id VARCHAR PRIMARY KEY
) WITH (
   KAFKA_TOPIC  = 'device_status',
   VALUE_FORMAT = 'JSON',
   TIMESTAMP    = 'event_ts'
);
