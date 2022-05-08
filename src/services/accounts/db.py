

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import Session

from accounts.app import app

from flask_sqlalchemy import SQLAlchemy

import enum

db: Session = SQLAlchemy(app)
db_path = "../local_databases/auth_db.db"

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

class OAuthClient(db.Model):
    __tablename__ = "oauth_clients"

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    secret = Column(String)
    redirect_uri = Column(String)

class OAuthCode(db.Model):
    id = Column(Integer, primary_key=True)
    user_uid = Column(String)
    code = Column(String)

class Token(db.Model):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True)
    user_uid = Column(String)
    code = Column(String)


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
        
        oauth_dicts = [
            {"uid": 'd25fc48d-ba74-40dc-a359-da80b55e1d1a', "secret":"my-secret2", "redirect_uri":"http://localhost:10002/auth/confirm"}
        ]
        for client in oauth_dicts:
            db.session.add(OAuthClient(**client))
        
    db.session.commit()

