from jsonschema import ValidationError
from kafka import KafkaConsumer
import json

from task_tracker.events import userCreated

from schema_registry.validator import validateMessage

KAFKA_URL = 'localhost:29092'
consumer = KafkaConsumer('User', bootstrap_servers=KAFKA_URL)

EVENT_TO_FUNC = {
    'userCreated': userCreated
}

def background_task():
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
        
        print(f"Emiting event {data}")
        EVENT_TO_FUNC[data["event_name"]](data["data"])
