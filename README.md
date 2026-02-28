# kafka_exp

## Real-Time Object Intelligence Platform

Imagine the ability to monitor any moving asset—whether an animal, vehicle, drone, satellite, or fleet unit—with precise spatial and temporal awareness. By embedding **GPS trackers**, we can capture exactly **where** an object is and **when** it was there.

But location is only the baseline.

By integrating **additional sensors**—temperature, acoustic signals, altitude, vibration, and other environmental parameters—we move beyond tracking into **contextual intelligence**. These multidimensional signals allow us to understand the real-time condition, behavior, and operational environment of the asset.

**System Architecture**: To operationalize this, we implement a streaming-first data platform:
1. **Apache Kafka**: Event backbone for ingesting and orchestrating high-throughput GPS and sensor streams.
2. **ksqlDB**: Real-time stream processing: joins, time-window aggregations, event correlation, and anomaly detection.
3. **PostgreSQL** (Data Warehouse layer): Persistent storage for historical records and latest-state snapshots.
4. **FastAPI**: High-performance API layer for real-time data access from streaming topics or warehouse storage.

## Business Impact

This architecture enables continuous tracking, live analytics, and operational decision support in scenarios such as:

1. Fleet management optimization
2. Wildlife behavior research
3. Real-Live survey
4. Expedition, diving and hiking group safety monitoring
5. Drone, unmanned aerial or marine vehicle and satellite operations surveillance

Outcome: A unified, real-time intelligence system that transforms raw movement data into actionable insight.


## How to install and to use

install kafka containers

`docker compose  --profile kafka  up  -d`

install postgresql container

`docker-compose up -d --build postgres`

access the container with

`docker exec -it ksqldb-server ksql`

`docker exec -it etl_kafka sh`

run the generator

`python producer_device_status.py`

`python producer_device_location.py`

run the FastAPI with

`uvicorn main:app --host 0.0.0.0 --port 8080 --reload`
