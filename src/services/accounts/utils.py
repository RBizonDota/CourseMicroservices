
from flask import request, redirect

from task_tracker.db import Token, User

def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return {"error":"Forbidden"}, 403

        token_instance = Token.query.filter_by(code=token).first()
        if not token_instance:
            return {"error":"Forbidden"}, 403

        return func(*args, user=User.query.filter_by(uid=token_instance.user_uid).first(), **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper