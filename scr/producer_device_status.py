# filepath: kafka/scripts/producer_device_status.py
# run: python kafka/scripts/producer_device_status.py

from itertools import cycle
import json
import time

from confluent_kafka import Producer
import util.generator as generator

BOOTSTRAP_SERVERS = "kafka1:19092"
TOPIC = "device_status"

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
TOTAL_MESSAGES = 2000
DELAY_SECONDS = 0.5

for i in range(TOTAL_MESSAGES):
    device_id = next(seq)
    payload = generator.brown_generator_status(1, data_type="json")
    payload["device_id"] = device_id

    producer.produce(
        topic=TOPIC,
        key=device_id,
        value=json.dumps(payload),
        callback=delivery_report,
    )

    time.sleep(DELAY_SECONDS)

producer.flush()
