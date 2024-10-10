# Kafka Producer, Consumer, and Topic Monitor Scripts

This project provides scripts for producing, consuming, and monitoring Kafka topics using the `kafka-python` library. The scripts utilize `click` for command-line argument parsing and SSL for secure communication with Kafka.

## Directory Structure

```
.
├── .gitignore
├── README.md
├── consumer.py
├── monitor_topic.py
├── producer.py
└── requirements.txt
```

## Requirements

- Python 3.x
- `kafka-python` library (version 2.0.2)
- `click` library (version 8.1.7)

## Setup

1. **Create a Virtual Environment**

   It is recommended to use a virtual environment to manage dependencies:

   ```bash
   python -m pip install --user virtualenv
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

2. **Install Dependencies**

   After activating the virtual environment, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure that your `requirements.txt` contains:

   ```
   kafka-python==2.0.2
   click==8.1.7
   ```

## Usage

### 1. Producer Script

The `producer.py` script sends messages to a specified Kafka topic at a configurable rate.

#### Command

```bash
python producer.py <bootstrap_server> <topic> <num_partitions> <messages_per_second>
```

- `<bootstrap_server>`: Kafka server address (e.g., `localhost:9092`)
- `<topic>`: Kafka topic name
- `<num_partitions>`: Number of partitions for the topic
- `<messages_per_second>`: Rate at which messages are sent

The script will recreate the topic with the specified number of partitions before starting message production.

#### Example

```bash
python producer.py localhost:9092 test_topic 3 5
```

This command creates a `test_topic` with 3 partitions and sends 5 messages per second.

### 2. Consumer Script

The `consumer.py` script consumes messages from a specified Kafka topic, with an optional consumer group.

#### Command

```bash
python consumer.py <bootstrap_server> <topic> <messages_per_second> [--group-id <group_id>]
```

- `<bootstrap_server>`: Kafka server address
- `<topic>`: Kafka topic name
- `<messages_per_second>`: Rate at which messages are processed
- `--group-id`: Consumer group ID (optional, defaults to `my-consumer-group`)

#### Example

```bash
python consumer.py localhost:9092 test_topic 2 --group-id my-consumer-group
```

This command consumes messages from `test_topic` at a rate of 2 messages per second.

### 3. Topic Monitoring Script

The `monitor_topic.py` script provides detailed statistics about a Kafka topic, including the consumer group's lag.

#### Command

```bash
python monitor_topic.py <bootstrap_server> <topic> <consumer_group> <interval>
```

- `<bootstrap_server>`: Kafka server address
- `<topic>`: Kafka topic name
- `<consumer_group>`: Consumer group ID
- `<interval>`: Interval (in seconds) between checks

#### Example

```bash
python monitor_topic.py localhost:9092 test_topic my-consumer-group 10
```

This command monitors the `test_topic` for the consumer group `my-consumer-group`, updating every 10 seconds.

## Stopping the Scripts

To stop any running script, use `Ctrl+C`.

## Important Notes

- Ensure the Kafka server is accessible and properly configured.
- Scripts use SSL by default. If SSL is not required, modify the `security_protocol` and connection settings in the scripts.
- The `monitor_topic.py` script provides partition details and calculates lag for the specified consumer group.

## Troubleshooting

- **SSL Connection Issues**: Make sure your Kafka broker is configured for SSL communication if you're using SSL.
- **Kafka Topic Not Found**: Ensure the topic exists or use the producer script to create it.
- **Lag Calculation**: If you encounter lag-related issues, check the consumer group's offset settings and Kafka configuration.
