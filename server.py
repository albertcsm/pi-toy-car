import time

from MotorDriver import MotorDriver
Motor = MotorDriver()

MAX_SPEED = 100

class CarController():

    def action_left(self):
        Motor.MotorRun(0, 'forward', MAX_SPEED)
        Motor.MotorRun(1, 'backward', MAX_SPEED)

    def action_forward(self):
        Motor.MotorRun(0, 'forward', MAX_SPEED)
        Motor.MotorRun(1, 'forward', MAX_SPEED)

    def action_back(self):
        Motor.MotorRun(0, 'backward', MAX_SPEED)
        Motor.MotorRun(1, 'backward', MAX_SPEED)

    def action_right(self):
        Motor.MotorRun(0, 'backward', MAX_SPEED)
        Motor.MotorRun(1, 'forward', MAX_SPEED)

    def action_move(self, instruction):
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

    def action_stop(self):
        Motor.MotorRun(0, 'forward', 0)
        Motor.MotorRun(1, 'forward', 0)


if __name__ == "__main__":
    car_controller = CarController()

    from webfrontend import WebFrontend
    web_frontend = WebFrontend(car_controller)
    web_frontend.start()

    from gamepadfrontend import GamepadFrontend
    gamepad_frontend = GamepadFrontend(car_controller)
    gamepad_frontend.start()
    
    print('Started')
    while True:
        time.sleep(1)
