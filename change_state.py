from flask import Flask, request, jsonify
import copy
import sys
import numpy as np
import random

app = Flask(__name__)


def left(a):
    check = copy.deepcopy(a)
    for i in range(4):
        for j in range(3):
            if a[i][j] is None:
                a[i][j] = a[i][j + 1]
                a[i][j + 1] = None
            elif a[i][j] == a[i][j + 1]:
                a[i][j] *= 2
                a[i][j + 1] = None
    if check != a:
        new_number(a)


def right(a):
    check = copy.deepcopy(a)
    for i in range(4):
        for j in range(3, 0, -1):
            if a[i][j] is None:
                a[i][j] = a[i][j - 1]
                a[i][j - 1] = None
            elif a[i][j] == a[i][j - 1]:
                a[i][j] *= 2
                a[i][j - 1] = None
    if check != a:
        new_number(a)


def up(a):
    check = copy.deepcopy(a)
    for j in range(4):
        for i in range(3):
            if a[i][j] is None:
                a[i][j] = a[i + 1][j]
                a[i + 1][j] = None
            elif a[i][j] == a[i + 1][j]:
                a[i][j] *= 2
                a[i + 1][j] = None
    if check != a:
        new_number(a)


def down(a):
    check = copy.deepcopy(a)
    for j in range(4):
        for i in range(3, 0, -1):
            if a[i][j] is None:
                a[i][j] = a[i - 1][j]
                a[i - 1][j] = None
            elif a[i][j] == a[i - 1][j]:
                a[i][j] *= 2
                a[i - 1][j] = None
    if check != a:
        new_number(a)


def restart(a):
    a = copy.deepcopy(start)
    return a


def new_number(a):
    options = [[i, j] for i in range(4) for j in range(4) if a[i][j] is None]
    i, j = random.choice(options)
    a[i][j] = 2

start = [[4, 4, 4, 4],
         [None, 8, None, 8],
         [None, 8, 8, None],
         [None, None, None, None]]
field = copy.deepcopy(start)


def show(a):
    for i in range(4):
        for j in range(4):
            if a[i][j] is None:
                print(a[i][j], end=" ")
            else:
                print(a[i][j], end="\t")
        print()


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

    show(field)
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


