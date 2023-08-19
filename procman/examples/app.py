import os
from flask import Flask
import redis

app = Flask(__name__)
# default is localhost
SOCK_PATH = os.getenv('RIPC_RUNTIME_DIR', default='/tmp')
#rconn = redis.Redis()
rconn = redis.from_url(f"unix://{SOCK_PATH}/socket")

@app.route('/')
def hello():
    rconn.incr('hits')
    counter = str(rconn.get('hits'),'utf-8')
    return "This webpage has been viewed "+counter+" time(s)"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
