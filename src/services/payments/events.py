from payments.db import User, Task, Payment, db
from kafka import KafkaProducer
import json
from schema_registry.validator import validateMessage
from payments.db import StatusChoices

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
    task_instance = Task(**data, assignee_id=user.id)
    task_instance.generatePaymentValues()
    print("CREATED TASK", task_instance)
    db.session.add(task_instance)
    db.session.commit()

def taskStatusChanged(data):
    print("Creating payment", data)
    # user = User.query.filter(uid=data["user_uid"]).first()
    task = Task.query.filter_by(uid=data["task_uid"]).first()
    task.status = data["status"]
    
    payment = Payment(user_id = task.assignee_id, task_id = task.id, value=task.pay_on_finish)
    print("paymentCreated", task.assignee_id, task, payment)
    db.session.add(payment)
    db.session.commit()
    db.session.add(task)
    db.session.commit()

def taskReassigned(data):

    user = User.query.filter_by(uid=data["user_uid"]).first()
    task = Task.query.filter_by(uid=data["task_uid"]).first()
    task.assignee_id = user.id

    payment = Payment(user_id = user.id, task_id = task.id, value=task.pay_on_reassign)
    db.session.add(payment)
    db.session.commit()
    db.session.add(task)
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
        "value": payment.value
    }

    producer.send('Payment', data)