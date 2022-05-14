
from flask import request, redirect

from payments.db import Token, User

AUTH_URI = 'http://localhost:10001/auth'
CLIENT = {
    "uid": '2d2ade69-cdcb-4b06-9f16-4d1fdfef9d83',
    "secret": "my-secret3",
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

def default_user(func):
    def wrapper(*args, **kwargs):
        return func(*args, user=User.query.filter_by(id=1).first(), **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper