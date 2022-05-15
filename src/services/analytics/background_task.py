from jsonschema import ValidationError
from kafka import KafkaConsumer
import json

from analytics.events import userCreated, taskCreated, paymentCreated

from schema_registry.validator import validateMessage

KAFKA_URL = 'localhost:29092'

EVENT_TO_FUNC = {
    'userCreated': userCreated,
    'taskCreated': taskCreated,
    'paymentCreated': paymentCreated,
}

def background_task_task():
    consumer = KafkaConsumer('Task', bootstrap_servers=KAFKA_URL)
    for msg in consumer:
        data = json.loads(msg.value)
        print(data)
        if not data.get("event_name"):
            continue
        
        try:
            validateMessage('Task', data)
        except ValidationError as e:
            print(f"Error occured error={e}")
            continue
        
        EVENT_TO_FUNC[data["event_name"]](data["data"])

def background_task_user():
    consumer = KafkaConsumer('User', bootstrap_servers=KAFKA_URL)
    for msg in consumer:
        data = json.loads(msg.value)
        print(data)
        if not data.get("event_name"):
            continue
        
        try:
            validateMessage('User', data)
        except ValidationError as e:
            print(f"Error occured error={e}")
            continue
        
        EVENT_TO_FUNC[data["event_name"]](data["data"])

def background_task_payment():
    consumer = KafkaConsumer('Payment', bootstrap_servers=KAFKA_URL)
    for msg in consumer:
        data = json.loads(msg.value)
        print(data)
        if not data.get("event_name"):
            continue
        
        try:
            validateMessage('Payment', data)
        except ValidationError as e:
            print(f"Error occured error={e}")
            continue
        
        EVENT_TO_FUNC[data["event_name"]](data["data"])
