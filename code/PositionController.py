import time

import SerialInterface


class PositionController:
    x = 0
    y = 0
    z = 0

    def __init__(self, interface):
        self.controller_interface = SerialInterface.SerialInterface(interface, 250000)
        self.controller_interface.output("G01 X Y Z")
        self.x = 0
        self.y = 0
        self.z = 0
        # time.sleep(2)

    def close_controller(self):
        self.controller_interface.closeInterface()

    def home_xy(self):
        self.controller_interface.output(f"G01 X Y Z40")
        self.controller_interface.output(f"G01 X0 Y0 Z40")
        self.controller_interface.output(f"G01 X Y Z0")
        self.x = 0
        self.y = 0

    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.controller_interface.output(f"G01 X{x} Y{y} Z{z}")
        # time.sleep(1)

    def move_rel(self, x=0, y=0, z=0):
        self.x += x
        if self.x < 0:
            self.x = 0
        self.y += y
        if self.y < 0:
            self.y = 0
        self.z += z
        if self.z < 0:
            self.z = 0
        self.controller_interface.output(f"G01 X{self.x} Y{self.y} Z{self.z}")
        # time.sleep(1)

    def move_raster(self, width, height, action_callback):
        x_start = self.x
        y_start = self.y
        z_start = self.z

        result_list = []

        for z_iter in range((height * 4) + 1):
            for y_iter in range((width * 4) + 1):
                for x_iter in range((width * 4) + 1):
                    self.move_to(
                        x=x_start + (x_iter / 4),
                        y=y_start + (y_iter / 4),
                        z=z_start + (z_iter / 4),
                    )
                    action_callback()
                    result_list.append(
                        {
                            "x": x_start + (x_iter / 4),
                            "y": y_start + (y_iter / 4),
                            "z": z_start + (z_iter / 4),
                            "result": "r",
                        }
                    )
                    time.sleep(1)
        self.move_to(x=x_start, y=y_start, z=z_start)
        return result_list


def main():
    newController = PositionController("COM25")
    newController.move_to(50, 50, 10)
    time.sleep(3)
    newController.move_to(0, 10, 10)
    time.sleep(3)
    newController.move_to(0, 0, 0)
    time.sleep(1)
    newController.move_to(0.25, 0, 0)
    time.sleep(1)
    newController.move_to(0.25, 0.25, 0)
    time.sleep(1)
    newController.move_to(0, 0, 0)
    newController.close_controller()


if __name__ == "__main__":
    main()
# end main
