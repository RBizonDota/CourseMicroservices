from jsonschema import ValidationError
from kafka import KafkaProducer
import json

from schema_registry.validator import validateMessage

KAFKA_URL = 'localhost:29092'
producer = KafkaProducer(bootstrap_servers=KAFKA_URL, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def sendUserCreated(user):
    sendMessage('User', {
        "event_name": "userCreated",
        "event_version": 1,
        "data": user
        })

def sendMessage(topic, data):
    try:
        validateMessage(topic, data)
        producer.send(topic, data)
    except ValidationError as e:
        print(f"Error occured while trying to send message topic={topic} |  message={data} | error={e}")
