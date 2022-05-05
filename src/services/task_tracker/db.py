

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import Session

from task_tracker.app import app

from flask_sqlalchemy import SQLAlchemy, relationship

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
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(Enum(RoleChoices))

    tasks = relationship("Task")

class StatusChoices(str, enum.Enum):
    OPENED = 'opened'
    FINISHED = 'finished'

class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(StatusChoices))
