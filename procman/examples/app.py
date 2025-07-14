import os
import tempfile
from pathlib import Path

import redis
from flask import Flask

app = Flask(__name__)
# default is localhost
temp_dir = Path(tempfile.gettempdir()).joinpath('redis-ipc')
FLASK_DEBUG = bool(os.getenv('FLASK_DEBUG', default=False))
SOCK_PATH = os.getenv('RIPC_RUNTIME_DIR', default=temp_dir)
# rconn = redis.Redis()
rconn = redis.from_url(f"unix://{SOCK_PATH}/socket")


@app.route('/')
def hello():
    rconn.incr('hits')
    counter = str(rconn.get('hits'), 'utf-8')
    return "This webpage has been viewed " + counter + " time(s)"


if __name__ == "__main__":  # see the warning in console, DEMO only
    app.run(host="localhost", port=8000, debug=FLASK_DEBUG)
