import json
import threading

from flask import Flask, send_from_directory, redirect, request
app = Flask(__name__)
car_controller = None


@app.route('/')
def serve_root():
    return redirect("/ui/index.html", code=302)

@app.route('/ui/<path:path>')
def serve_static(path):
    return send_from_directory('ui', path)

@app.route("/action/left", methods=['POST'])
def action_left():
    car_controller.action_left()
    return "left"

@app.route("/action/forward", methods=['POST'])
def action_forward():
    car_controller.action_forward()
    return "forward"

@app.route("/action/back", methods=['POST'])
def action_back():
    car_controller.action_back()
    return "back"

@app.route("/action/right", methods=['POST'])
def action_right():
    car_controller.action_right()
    return "right"

@app.route("/action/move", methods=['POST'])
def action_move():
    instruction = json.loads(request.data)
    car_controller.action_move(instruction)
    return "move"

@app.route("/action/stop", methods=['POST'])
def action_stop():
    car_controller.action_stop()
    return "right"


class WebFrontend():

    def __init__(self, controller):
        global car_controller
        car_controller = controller
    
    def __serve(self):
        app.run(host="0.0.0.0", port=5000)

    def start(self):
        self.thread = threading.Thread(target=self.__serve)
        self.thread.daemon = True
        self.thread.start()
