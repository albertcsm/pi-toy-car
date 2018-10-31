import evdev
import threading
import time

class GamepadFrontend():

    def __init__(self, controller):
        self.car_controller = controller
        self.steering = 0
        self.forward = 0

    def get_device(self):
        paths = evdev.list_devices()
        devices = [evdev.InputDevice(path) for path in paths]
        for device in devices:
            print(device.path, device.name, device.phys)
        return devices[0] if devices else None

    def handle_event(self, event):
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == 0:
                # X-axis
                if event.value < 127:
                    self.steering = -1
                elif event.value > 127:
                    self.steering = 1
                else:
                    self.steering = 0
                self.update_car()
            elif event.code == 1:
                # Y-axis
                if event.value < 127:
                    self.forward = 1
                elif event.value > 127:
                    self.forward = -1
                else:
                    self.forward = 0
                self.update_car()

    def update_car(self):
        if self.steering < 0:
            self.car_controller.action_left()
        elif self.steering > 0:
            self.car_controller.action_right()
        elif self.forward > 0:
            self.car_controller.action_forward()
        elif self.forward < 0:
            self.car_controller.action_back()
        else:
            self.car_controller.action_stop()

    def __serve(self):
        while True:
            device = self.get_device()
            if device:
                print('Selected', device.name)
                try:
                    for event in device.read_loop():
                        self.handle_event(event)
                except IOError as e:
                    print('Error reading from device', e)
            time.sleep(1)

    def start(self):
        self.thread = threading.Thread(target=self.__serve)
        self.thread.daemon = True
        self.thread.start()
