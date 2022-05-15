from payments.app import app
from payments.db import db

from payments.views import *

from threading import Thread

from payments.background_task import background_task_task, background_task_user


if __name__ == '__main__':
    bg_task = Thread(target=background_task_task)
    bg_task.start()
    bg_user = Thread(target=background_task_user)
    bg_user.start()

    app.run(host="0.0.0.0", port=10003)