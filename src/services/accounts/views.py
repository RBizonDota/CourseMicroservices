import uuid
from accounts.app import app
from accounts.db import User, OAuthClient, OAuthCode, Token, db, RoleChoices
from accounts.structs import PydanticUser, UserCredentials, ProviderCredentials, PydanticToken
from accounts.events import sendUserCreated

from flask import request, redirect, render_template

import os

from accounts.utils import login_required

@app.route('/users')
def get_users():
    users = User.query.all()
    res = {
        "users": [PydanticUser.from_orm(user).prepare() for user in users]
    }
    return res

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return {"error": f"user with id {user_id} not found"}, 404

    res = PydanticUser.from_orm(user).prepare()
    return res

# Реализация OAuth
@app.route('/auth/oauth', methods=["POST"])
def oauth():
    client_uid = request.args.get('uid')
    if not client_uid:
        return {"error": f"client uid not provided"}, 404

    client = OAuthClient.query.filter_by(uid=client_uid).first()
    if not client:
        return {"error": f"invalid client uid"}, 400

    data = request.json
    credentials = UserCredentials(**data)
    user = User.query.filter_by(username=credentials.username, password=credentials.password).first()
    if not user:
        return {"error": f"Unable to authenticate with such credentials"}, 400

    code = str(uuid.uuid4())
    code_instance = OAuthCode(
        user_uid = user.uid,
        code = code
    )
    db.session.add(code_instance)
    db.session.commit()

    return {"redirect_to": client.redirect_uri+"?code="+code}


@app.route('/auth/confirm', methods=["POST"])
def provide_auth():
    data = request.json
    credentials = ProviderCredentials(**data)
    
    oauth_client = OAuthClient.query.filter_by(uid=credentials.client_uid, secret=credentials.secret).first()
    if not oauth_client:
        return {"error": f"invalid oauth client authentication"}, 400
    
    code_instance = OAuthCode.query.filter_by(code=credentials.code).first()
    if not code_instance:
        return {"error": f"invalid oauth code provided"}, 400

    token = str(uuid.uuid4())
    token_instance = Token(code=token, user_uid=code_instance.user_uid)
    db.session.add(token_instance)
    db.session.commit()

    return {
        "token": PydanticToken.from_orm(token_instance).dict(),
    }

@app.route('/auth')
def index():
    return render_template('accounts_oauth.html')

# TODO: регистрация

@app.route('/reg')
@login_required
def reg_index(user):
    return render_template('reg.html')

@app.route('/reg', methods=['POST'])
@login_required
def reg(user):
    if not user.role == RoleChoices.ADMIN:
        return {"error": "requester not admin"}, 403

    data = request.json
    new_user = User(username=data["username"], password=data["password"], uid=str(uuid.uuid4()), role=data["role"])
    db.session.add(new_user)
    db.session.commit()
    sendUserCreated(PydanticUser.from_orm(new_user).prepare())
    return {}, 201