from analytics.db import User, Task, Payment, db
from kafka import KafkaProducer
import json
from schema_registry.validator import validateMessage
from payments.db import StatusChoices

from datetime import datetime

KAFKA_URL = 'localhost:29092'
producer = KafkaProducer(bootstrap_servers=KAFKA_URL, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Consumers

def userCreated(data):
    data.pop('id', None)
    user_instance = User(**data)
    print("User created", user_instance)
    db.session.add(user_instance)
    db.session.commit()

def taskCreated(data):
    data.pop('id', None)
    assignee_uid = data.pop('assignee_uid', None)

    user = User.query.filter_by(uid=assignee_uid).first()
    task_instance = Task(**{
        "id": data["id"],
        "uid": data["uid"],
        "name": data["name"],
        "description": data["description"],
        "assignee_id": user.id
    })
    task_instance.generatePaymentValues()
    print("CREATED TASK", task_instance)
    db.session.add(task_instance)
    db.session.commit()

def paymentCreated(data):
    data.pop('id', None)

    task = Task.query.filter_by(uid=data["task_uid"]).first()
    user = Task.query.filter_by(uid=data["user_uid"]).first()

    payment = {
        "task_id":task.id,
        "user_id":user.id,
        "value": data["value"]
    }
    payment_instance = Payment(**payment)
    db.session.add(payment_instance)
    db.session.commit()

# Producers

def sendMessage(topic, data):
    # todo: валидация
    validateMessage(topic, data)
    producer.send(topic, data)

def paymentCreated(payment: Payment):
    data = {
        "user_uid": User.query.filter_by(id=payment.user_id).first().uid,
        "task_uid": Task.query.filter_by(id=payment.task_id).first().uid,
        "value": payment.value,
        "time_created": datetime.strptime(payment.time_created, "%m/%d/%Y, %H:%M:%S")
    }

    producer.send('Payment', data)