from flask import Flask, request, jsonify
import copy
import sys
import numpy as np

app = Flask(__name__)


def left(a):
    for i in range(4):
        for j in range(3):
            if a[i][j] is None:
                a[i][j] = a[i][j + 1]
                a[i][j + 1] = None
            elif a[i][j] == a[i][j + 1]:
                a[i][j] *= 2
                a[i][j + 1] = None


def right(a):
    for i in range(4):
        for j in range(3, 0, -1):
            if a[i][j] is None:
                a[i][j] = a[i][j - 1]
                a[i][j - 1] = None
            elif a[i][j] == a[i][j - 1]:
                a[i][j] *= 2
                a[i][j - 1] = None


def up(a):
    for j in range(4):
        for i in range(3):
            if a[i][j] is None:
                a[i][j] = a[i + 1][j]
                a[i + 1][j] = None
            elif a[i][j] == a[i + 1][j]:
                a[i][j] *= 2
                a[i + 1][j] = None


def down(a):
    for j in range(4):
        for i in range(3, 0, -1):
            if a[i][j] is None:
                a[i][j] = a[i - 1][j]
                a[i - 1][j] = None
            elif a[i][j] == a[i - 1][j]:
                a[i][j] *= 2
                a[i - 1][j] = None


def restart(a):
    a = copy.deepcopy(start)
    return a

start = [[4, 4, 4, 4],
         [None, 8, None, 8],
         [None, 8, 8, None],
         [None, None, None, None]]
field = copy.deepcopy(start)


@app.route('/', methods=["POST"])
def change_state():
    post = request.get_json()
    user, action = post["user"], post["action"]
    allowed_actions = ["up", "left", "right", "down", "restart"]
    if action not in allowed_actions:
        return response_client_error()
    # result = get_state()
    if action == "up":
        up(field)
    elif action == "down":
        down(field)
    elif action == "left":
        left(field)
    elif action == "right":
        right(field)

    #show(field)
    out_field = np.array(field)
    out_field.resize(16)
    out_field = jsonify({"field": list(out_field)})
    return response_ok(out_field)


def response_client_error(message=""):
    return message, 401


def response_ok(message=""):
    return message, 200


def response_server_error(message=""):
    return message, 500


if __name__ == "__main__":
    app.run(host="localhost", port=5000)


