from analytics.app import app
from analytics.db import db

from analytics.views import *

from threading import Thread

from analytics.background_task import background_task_task, background_task_user, background_task_payment


if __name__ == '__main__':
    bg_task = Thread(target=background_task_task)
    bg_task.start()
    bg_user = Thread(target=background_task_user)
    bg_user.start()
    db_payment = Thread(target=background_task_payment)
    db_payment.start()

    app.run(host="0.0.0.0", port=10004)