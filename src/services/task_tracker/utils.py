
from flask import request, redirect

from task_tracker.db import Token, User

AUTH_URI = 'http://localhost:10001/auth'
CLIENT = {
    "uid": 'd25fc48d-ba74-40dc-a359-da80b55e1d1a',
    "secret": "my-secret2",
}

def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return redirect(AUTH_URI+f'?uid={CLIENT["uid"]}', code=302)

        token_instance = Token.query.filter_by(code=token).first()
        if not token_instance:
            return redirect(AUTH_URI+f'?uid={CLIENT["uid"]}', code=302)

        return func(*args, user=User.query.filter_by(uid=token_instance.user_uid).first(), **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def role_required(role_list):
    def role_required_wrapper(func):
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            for role in role_list:
                if user.role == role:
                    return func(*args, **kwargs)
            
            return {"error": "You do not have permission to perform this action"}, 403
        wrapper.__name__ = func.__name__
        return wrapper
    return role_required_wrapper
