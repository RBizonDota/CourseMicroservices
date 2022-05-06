from kafka import KafkaConsumer
import json

from task_tracker.events import userCreated

KAFKA_URL = 'localhost:29092'
consumer = KafkaConsumer('User', bootstrap_servers=KAFKA_URL)

EVENT_TO_FUNC = {
    'created': userCreated
}

def background_task():
    for msg in consumer:
        data = json.loads(msg.value)
        print(data)
        if not data.get("event"):
            continue
        
        EVENT_TO_FUNC[data["event"]](data["data"])
