import datetime
import time

import click
from kafka import KafkaConsumer

def dt_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@click.command()
@click.argument("bootstrap_server")
@click.argument("topic")
@click.argument("messages_per_second", type=float)
@click.option("--group-id", default="my-consumer-group", help="Consumer group ID")
def consume_messages(bootstrap_server, topic, messages_per_second, group_id):
    """Kafka message consumer script."""
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_server,
        auto_offset_reset='earliest',  # Start from the earliest message
        enable_auto_commit=True,
        group_id=group_id,
        api_version=(3, 7, 0),
        security_protocol="SSL",
        ssl_check_hostname=True,
        request_timeout_ms=60000
    )

    try:
        print(f"[{dt_str()}][{group_id}]: Consuming messages from topic: {topic}")
        for message in consumer:
            print(f"[{dt_str()}][{group_id}]: Received: {message.value.decode('utf-8')}")
            time.sleep(1 / messages_per_second)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    consume_messages()
