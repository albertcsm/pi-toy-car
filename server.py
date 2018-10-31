from MotorDriver import MotorDriver
Motor = MotorDriver()

from flask import Flask, send_from_directory, redirect, request
app = Flask(__name__)

import json

MAX_SPEED = 100

@app.route('/')
def serve_root():
    return redirect("/ui/index.html", code=302)

@app.route('/ui/<path:path>')
def serve_static(path):
    return send_from_directory('ui', path)

@app.route("/action/left", methods=['POST'])
def action_left():
    Motor.MotorRun(0, 'forward', MAX_SPEED)
    Motor.MotorRun(1, 'backward', MAX_SPEED)
    return "left"

@app.route("/action/forward", methods=['POST'])
def action_forward():
    Motor.MotorRun(0, 'forward', MAX_SPEED)
    Motor.MotorRun(1, 'forward', MAX_SPEED)
    return "forward"

@app.route("/action/back", methods=['POST'])
def action_back():
    Motor.MotorRun(0, 'backward', MAX_SPEED)
    Motor.MotorRun(1, 'backward', MAX_SPEED)
    return "back"

@app.route("/action/right", methods=['POST'])
def action_right():
    Motor.MotorRun(0, 'backward', MAX_SPEED)
    Motor.MotorRun(1, 'forward', MAX_SPEED)
    return "right"

@app.route("/action/move", methods=['POST'])
def action_move():
    instruction = json.loads(request.data)

    speed0 = 0
    speed1 = 0

    if instruction['steering'] < 0:
        speed1 -= MAX_SPEED * 1.5 * abs(instruction['steering'])
    else:
        speed0 -= MAX_SPEED * 1.5 * abs(instruction['steering'])

    basicSpeed = MAX_SPEED * 1.5 * abs(instruction['forward']) - (speed0 + speed1) / 2

    direction = instruction['forward'] / abs(instruction['forward'])
    speed0 = (speed0 + basicSpeed) * direction
    speed1 = (speed1 + basicSpeed) * direction

    if speed0 >= 0:
        Motor.MotorRun(0, 'forward', min(speed0, MAX_SPEED))
    else:
        Motor.MotorRun(0, 'backward', min(-speed0, MAX_SPEED))
    if speed1 >= 0:
        Motor.MotorRun(1, 'forward', min(speed1, MAX_SPEED))
    else:
        Motor.MotorRun(1, 'backward', min(-speed1, MAX_SPEED))
    return "move"

@app.route("/action/stop", methods=['POST'])
def action_stop():
    Motor.MotorRun(0, 'forward', 0)
    Motor.MotorRun(1, 'forward', 0)
    return "right"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
