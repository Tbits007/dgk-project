from app.main.config import KafkaConfig
from faststream.kafka import KafkaBroker


def new_broker(kafka_config: KafkaConfig) -> KafkaBroker:
    return KafkaBroker(
        bootstrap_servers=kafka_config.uri(),
    )