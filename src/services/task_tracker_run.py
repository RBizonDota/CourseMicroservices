from task_tracker.app import app
from task_tracker.db import db

from task_tracker.views import *

from threading import Thread

from task_tracker.background_task import background_task


if __name__ == '__main__':
    bg_task = Thread(target=background_task)
    bg_task.start()

    app.run(host="0.0.0.0", port=10002)