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

    def closeController(self):
        self.controller_interface.closeInterface()

    def homeXY(self):
        self.controller_interface.output(f"G01 X Y Z40")
        self.controller_interface.output(f"G01 X0 Y0 Z40")
        self.controller_interface.output(f"G01 X Y Z0")
        self.x = 0
        self.y = 0

    def moveTo(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.controller_interface.output(f"G01 X{x} Y{y} Z{z}")
        # time.sleep(1)

    def moveRel(self, x=0, y=0, z=0):
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

    def moveRaster(self, width, height, action_callback):
        x_start = self.x
        y_start = self.y
        z_start = self.z

        result_list = []

        for z_iter in range(height + 1):
            for y_iter in range(width + 1):
                for x_iter in range(width + 1):
                    self.moveTo(
                        x=x_start + x_iter, y=y_start + y_iter, z=z_start + z_iter
                    )
                    action_callback()
                    result_list.append(
                        {
                            "x": x_start + x_iter,
                            "y": y_start + y_iter,
                            "z": z_start + z_iter,
                            "result": "r",
                        }
                    )
                    time.sleep(1)
        self.moveTo(x=x_start, y=y_start, z=z_start)
        return result_list


def main():
    newController = PositionController("COM25")
    newController.moveTo(50, 50, 10)
    newController.moveTo(0, 10, 10)
    newController.moveTo(0, 0, 0)


if __name__ == "__main__":
    main()
# end main
