from accounts.app import app

from accounts.views import *



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10001)