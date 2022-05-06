from task_tracker.app import app
from task_tracker.utils import login_required

from task_tracker.db import User, Task, Token, db, RoleChoices, StatusChoices
from task_tracker.events import taskCreated, taskStatusChanged, taskReassigned

from flask import request, redirect, render_template, make_response
import requests

from .utils import AUTH_URI, CLIENT, role_required
import uuid
import random

@app.route('/tasks/my')
@login_required
def get_my_tasks(user):
    tasks = user.tasks
    return {"tasks":tasks}

@app.route('/tasks')
@login_required
def get_tasks(user):
    tasks = Task.query.all()
    return {"tasks":tasks}

@app.route('/tasks', methods=['POST'])
@login_required
def create_tasks(user):
    data = request.json
    new_task = Task(name=data["name"], description=data["desc"], assignee_id=data["user_id"], uid=str(uuid.uuid4()))
    db.session.add(new_task)
    db.session.commit()
    assginee = User.query.filter_by(id=new_task.assignee_id).first()
    taskCreated(new_task, assginee)
    return {}, 201

@app.route('/tasks/shuffle', methods=['POST'])
@login_required
@role_required([RoleChoices.ADMIN, RoleChoices.MANAGER])
def shuffle_tasks(user):
    tasks = Task.query.filter_by(status=StatusChoices.OPENED)
    users = User.query.filter(User.role.not_in(('manager','admin'))).all()

    for task in tasks:
        assignee_id = task.assignee_id
        assign_user = random.choice(users)
        if assignee_id != assign_user.id:
            task.assignee_id = assign_user.id
            db.session.add(task)
            db.session.commit()
            taskReassigned(task, assign_user)
    return {}
        


@app.route('/tasks/<task_id>/close', methods=['POST'])
@login_required
def close_task(task_id, user):
    task = Task.query.filter_by(id=task_id).first()
    if task.assignee_id == user.id or user.role in [RoleChoices.ADMIN, RoleChoices.MANAGER]:
        task.status = StatusChoices.FINISHED
        db.session.add(task)
        db.session.commit()
        taskStatusChanged(task)
        return {}, 201

    return {"error": "You don't have permission to perform this action"}, 403
    

@app.route('/')
@login_required
def index(user):
    return render_template('task_tracker.html', context={
        "can_edit":user.role in [RoleChoices.ADMIN, RoleChoices.MANAGER], 
        "users": User.query.filter(User.role.not_in(('manager','admin'))).all(),
        "tasks": Task.query.all()
    })

@app.route('/my')
@login_required
def my_index(user):
    return render_template('task_my_tracker.html', context={
        "can_edit":user.role in ['admin', 'manager'], 
        "users": User.query.filter(User.role.not_in(('manager','admin'))).all(),
        "tasks": user.tasks
    })

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