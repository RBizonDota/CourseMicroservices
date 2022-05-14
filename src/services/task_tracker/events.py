from task_tracker.db import User, Task, db
from kafka import KafkaProducer
import json
from schema_registry.validator import validateMessage

KAFKA_URL = 'localhost:29092'
producer = KafkaProducer(bootstrap_servers=KAFKA_URL, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Consumers

def userCreated(data):
    data.pop('id', None)
    user_instance = User(**data)
    db.session.add(user_instance)
    db.session.commit()

# Producers

def sendMessage(topic, data):
    # todo: валидация
    validateMessage(topic, data)
    producer.send(topic, data)

def taskCreated(task, assignee):
    time_updated = ""
    if task.time_updated:
        time_updated = task.time_updated.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "uid": task.uid,
        "name": task.name,
        "description": task.description,
        "assignee_uid": assignee.uid, 
        "status": task.status,
        "time_created": task.time_created.strftime("%Y-%m-%d %H:%M:%S"),
        "time_updated": time_updated
    }

    sendMessage('Task', {
        "event_name": "taskCreated",
        "event_version": 1,
        "data": data
        })

def taskStatusChanged(task: Task):
    data = {
        "task_uid": task.uid,
        "status": task.status,
    }
    sendMessage('Task', {
        "event_name": "statusChanged",
        "event_version": 1,
        "data": data
        })

def taskReassigned(task: Task, user: User):
    data = {
        "task_uid": task.uid,
        "user_uid": user.uid
    }
    sendMessage('Task', {
        "event_name": "taskReassigned",
        "event_version": 1,
        "data": data
        })