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
        return True
    return False


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
        return True
    return False


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
        return True
    return False


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
        return True
    return False


def restart(a):
    for i in range(4):
        for j in range(4):
            a[i][j] = start[i][j]


def new_number(a):
    options = [[i, j] for i in range(4) for j in range(4) if a[i][j] is None]
    i, j = random.choice(options)
    a[i][j] = 2

start = [[4, 4, 4, 4],
         [None, 8, None, 8],
         [None, 8, 8, None],
         [None, None, None, None]]
field = copy.deepcopy(start)


def end_condition_check(a):
    test_a = copy.deepcopy(a)
    if not right(test_a) and not up(test_a) and not left(test_a) and not down(test_a):
        return True
    return False


def serialize(a):
    field = np.array(a)
    field.resize(16)
    return jsonify({"field": list(field)})


@app.route('/', methods=["POST"])
def change_state():
    post = request.get_json()
    user, action = post["user"], post["action"]
    allowed_actions = ["up", "left", "right", "down", "restart"]
    if action not in allowed_actions:
        return response_client_error()
    # field = get_state()
    if action == "up":
        move = up(field)
    elif action == "down":
        move = down(field)
    elif action == "left":
        move = left(field)
    elif action == "right":
        move = right(field)
    else:
        restart(field)
        result = serialize(field)
        return response_ok(result)

    if move is True:
        new_number(field)
    elif end_condition_check(field):
        data = np.array(field)
        data.resize(16)
        score = max(data)
        return response_ok("Game is over")
    else:
        return response_ok()
    #show(field)
    result = serialize(field)
    return response_ok(result)


def response_client_error(message=""):
    return message, 401


def response_ok(message=""):
    return message, 200


def response_server_error(message=""):
    return message, 500


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
