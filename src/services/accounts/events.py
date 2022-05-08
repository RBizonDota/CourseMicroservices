from kafka import KafkaProducer
import json

KAFKA_URL = 'localhost:29092'
producer = KafkaProducer(bootstrap_servers=KAFKA_URL, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def sendUserCreated(user):
    producer.send('User', {
        "event": "created",
        "data": user
        })

