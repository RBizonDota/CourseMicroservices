
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Session

from task_tracker.app import app

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import enum

db: Session = SQLAlchemy(app)
db_path = "../local_databases/auth_db.db"

# From auth app
class RoleChoices(str, enum.Enum):
    WORKER = 'worker'
    ACCOUNTANT = 'accountant'
    MANAGER = 'manager'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(Enum(RoleChoices))

    tasks = relationship("Task")

class Token(db.Model):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_uid = Column(String)
    code = Column(String)

class StatusChoices(str, enum.Enum):
    OPENED = 'opened'
    FINISHED = 'finished'

class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(StatusChoices), default=StatusChoices.OPENED)

    name = Column(String)
    description = Column(String, default="")

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

@app.before_first_request
def create_tables():
    db.create_all()

    if not User.query.filter_by(id=1).first():
        user_dict = {
            "id":1,
            "uid": '1fe47968-8e2a-44b3-9301-0f663e2af56d',
            "username":"123123",
            "password":"123123",
            "email":"123",
            "role":RoleChoices.ADMIN,
        }
        new_user = User(**user_dict)
        db.session.add(new_user)

    db.session.commit()