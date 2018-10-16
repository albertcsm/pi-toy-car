from MotorDriver import MotorDriver
Motor = MotorDriver()

from flask import Flask, send_from_directory, redirect
app = Flask(__name__)

speed = 100

@app.route('/')
def serve_root():
    return redirect("/ui/index.html", code=302)

@app.route('/ui/<path:path>')
def serve_static(path):
    return send_from_directory('ui', path)

@app.route("/action/left", methods=['POST'])
def action_left():
    Motor.MotorRun(0, 'forward', speed)
    Motor.MotorRun(1, 'backward', speed)
    return "left"

@app.route("/action/forward", methods=['POST'])
def action_forward():
    Motor.MotorRun(0, 'forward', speed)
    Motor.MotorRun(1, 'forward', speed)
    return "forward"

@app.route("/action/back", methods=['POST'])
def action_back():
    Motor.MotorRun(0, 'backward', speed)
    Motor.MotorRun(1, 'backward', speed)
    return "back"

@app.route("/action/right", methods=['POST'])
def action_right():
    Motor.MotorRun(0, 'backward', speed)
    Motor.MotorRun(1, 'forward', speed)
    return "right"

@app.route("/action/stop", methods=['POST'])
def action_stop():
    Motor.MotorRun(0, 'forward', 0)
    Motor.MotorRun(1, 'forward', 0)
    return "right"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
