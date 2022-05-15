from datetime import datetime, timedelta
import re
from payments.app import app
from payments.utils import login_required

from payments.db import User, Token, db, Payment

from flask import request, redirect, make_response
import requests

from payments.structs import PydanticPayment, PydanticUser
from services.payments.utils import role_required

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

@app.route('/top-manager')
@login_required
@role_required(['admin', 'manager'])
def top_manager_view(user):
    return {
        "got-money": -1 * sum([payment.value for payment in Payment.query.all()]),
        "minus-popugs": len(filter(lambda x: x<0, [
            sum(map(lambda x: x.value, user.payments)) for user in User.query.all()
        ]))
    }

@app.route('/highest-paid-task')
@login_required
@role_required(['admin', 'manager'])
def highest_paid_task(user):
    min_time_data = Payment.query.order_by(Payment.time_created).first()
    max_time_data = Payment.query.order_by(Payment.time_created.desc()).first()

    time_delta = timedelta(
        days=1
    )
    ttime = datetime(min_time_data.year, min_time_data.month, min_time_data.day,0,0,0,0)
    max_time = datetime(max_time_data.year, max_time_data.month, max_time_data.day,0,0,0,0)

    res = []
    while ttime<max_time:
        res.append({
            "date": f"{ttime.day}.{ttime.month}",
            "value": max([payment.value for payment in Payment.query.filter(Payment.time_created >= ttime and Payment.time_created<ttime+time_delta).all()])
        })
        ttime+=time_delta

    return {
        "values": res
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