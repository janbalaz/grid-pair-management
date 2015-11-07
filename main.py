from flask import Flask
from enum import Enum

app = Flask(__name__)

MNGMT_TYPE = Enum('MNGMT_TYPE', 'matrix hashed')


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
