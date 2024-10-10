import datetime
import time

import click
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import UnknownTopicOrPartitionError


def dt_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def recreate_topic(bootstrap_server, topic, num_partitions):
    """Delete the existing Kafka topic if it exists, then create a new one with the specified number of partitions."""
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_server,
        api_version=(3, 7, 0),
        security_protocol="SSL",
    )

    # Try to delete the topic if it exists
    try:
        admin_client.delete_topics([topic])
        print(f"[{dt_str()}]: Topic '{topic}' deleted.")
        # Allow some time for the topic deletion to propagate
        time.sleep(2)
    except UnknownTopicOrPartitionError:
        print(f"[{dt_str()}]: Topic '{topic}' does not exist. Creating a new one.")

    # Define the topic configuration
    topic_config = NewTopic(
        name=topic, num_partitions=num_partitions, replication_factor=1
    )

    # Create the topic
    admin_client.create_topics([topic_config])
    print(f"[{dt_str()}]: Topic '{topic}' created with {num_partitions} partitions.")

    admin_client.close()


@click.command()
@click.argument("bootstrap_server")
@click.argument("topic")
@click.argument("num_partitions", type=int)
@click.argument("messages_per_second", type=float)
def produce_messages(bootstrap_server, topic, num_partitions, messages_per_second):
    """Kafka message producer script."""
    # Recreate the topic with the specified number of partitions
    recreate_topic(bootstrap_server, topic, num_partitions)

    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_server,
        api_version=(3, 7, 0),
        security_protocol="SSL",
        ssl_check_hostname=True,
        request_timeout_ms=60000,
    )
    interval = 1 / messages_per_second
    message_number = 0
    start_time = time.time()

    try:
        while True:
            message_number += 1
            message = f"[{dt_str()}]: Message {message_number}".encode("utf-8")
            producer.send(topic, message)
            print(f"[{dt_str()}]: Sent msg: {message}")

            # Maintain the desired sending rate
            next_send_time = start_time + message_number * interval
            sleep_time = next_send_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()


if __name__ == "__main__":
    produce_messages()
