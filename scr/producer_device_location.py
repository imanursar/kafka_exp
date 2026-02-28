# filepath: kafka/scripts/producer_device_location.py
# run: python kafka/scripts/producer_device_location.py

from itertools import cycle
import json
import time

from confluent_kafka import Producer
import util.generator as generator

BOOTSTRAP_SERVERS = "kafka1:19092"
TOPIC = "device_location"

producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
    }
)


def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(
            f"✅ Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}"
        )


# Simulasi device
DEVICES = [f"dev-{i}" for i in range(1, 4)]
seq = cycle(DEVICES)
LONGLAT = [9, 107]
TOTAL_MESSAGES = 500
DELAY_SECONDS = 2

for i in range(TOTAL_MESSAGES):
    device_id = next(seq)
    payload = generator.brown_generator_location(
        LONGLAT, 1, t=10.0, delta=0.1, data_type="json"
    )
    payload["device_id"] = device_id

    producer.produce(
        topic=TOPIC,
        key=device_id,
        value=json.dumps(payload),
        callback=delivery_report,
    )

    time.sleep(DELAY_SECONDS)

producer.flush()
