

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
    id = Column(Integer, primary_key=True)
    user_uid = Column(String)
    code = Column(String)


@app.before_first_request
def create_tables():
    db.create_all()

    user_dict = {
        "id":1,
        "uid": "1589a65e-29f7-4ced-aff7-8b3123460ada",
        "username":"123",
        "password":"123",
        "email":"123",
        "role":RoleChoices.WORKER,
    }
    new_user = User(**user_dict)
    db.session.add(new_user)
    
    oauth_dicts = [
        {"id":1, "uid": '37ff02f5-96df-4744-b9fc-0acf73162d4d', "secret":"my-secret", "redirect_uri":"http://localhost:4444/redirected/uri"},
        {"id":2, "uid": 'd25fc48d-ba74-40dc-a359-da80b55e1d1a', "secret":"my-secret2", "redirect_uri":"http://localhost:5555/redirected/uri2"}
    ]
    for client in oauth_dicts:
        db.session.add(OAuthClient(**client))
    
    db.session.commit()

