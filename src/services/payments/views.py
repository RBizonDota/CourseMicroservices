from payments.app import app
from payments.utils import login_required

from payments.db import User, Token, db, Payment

from flask import request, redirect, make_response
import requests

from payments.structs import PydanticPayment, PydanticUser

from .utils import AUTH_URI, CLIENT

@app.route('/')
# @role_required(['admin', 'manager'])
def get_all():
    print(Payment.query.all())
    users = User.query.all()
    return {
        "data":[
            {
                "user": PydanticUser.from_orm(user).dict(),
                "balance": sum(map(lambda x: x.value, user.payments)),
                "audit": [PydanticPayment.from_orm(el).dict() for el in user.payments]
            } for user in users
        ]
    }
    return {
        "payments":[PydanticPayment.from_orm(el).dict() for el in Payment.query.all()]
        }

@app.route('/my')
@login_required
def get_current_balance(user):
    return {
        "balance": sum(map(lambda x: x.value, user.payments)),
        "audit": [PydanticPayment.from_orm(el).dict() for el in user.payments]
    }


@app.route('/auth/confirm')
def oauth_confirm():
    code = request.args.get('code')
    resp = requests.post(AUTH_URI+'/confirm', json={
        "secret": CLIENT["secret"],
        "client_uid": CLIENT["uid"],
        "code":code
    })
    if resp.status_code!=200:
        print(resp.text)
        return {"error": "Error while getting access_token"}, 400

    token = resp.json()["token"]
    tonen_instance = Token(code=token["code"], user_uid=token["user_uid"])
    db.session.add(tonen_instance)
    db.session.commit()
    
    res = make_response(redirect('/'))
    res.set_cookie('token', token["code"])
    
    return res