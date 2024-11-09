import time

import SerialInterface

STEPS_PER_MM_X = 4
STEPS_PER_MM_Y = 4
STEPS_PER_MM_Z = 4


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

    def move_raster(
        self, width, height, action_callback, eval_callback, status_callback, n_rep=1
    ):
        x_start = self.x
        y_start = self.y
        z_start = self.z

        eval_result = []
        result_list = []
        task_counter = 0

        for z_iter in range((height * STEPS_PER_MM_Z) + 1):
            for y_iter in range((width * STEPS_PER_MM_Y) + 1):
                for x_iter in range((width * STEPS_PER_MM_X) + 1):
                    status_callback(
                        task_counter,
                        ((height * STEPS_PER_MM_Z) + 1)
                        * ((width * STEPS_PER_MM_Y) + 1)
                        * ((width * STEPS_PER_MM_X) + 1)
                        * n_rep,
                    )
                    self.move_to(
                        x=x_start + (x_iter / STEPS_PER_MM_X),
                        y=y_start + (y_iter / STEPS_PER_MM_Y),
                        z=z_start + (z_iter / STEPS_PER_MM_Z),
                    )
                    for n in range(n_rep):
                        action_callback()
                        eval_result.append(eval_callback())
                    if "g" in eval_result:
                        result = "g"
                    if "y" in eval_result:
                        result = "y"
                    if "r" in eval_result:
                        result = "r"
                    eval_result = []
                    result_list.append(
                        {
                            "x": x_start + (x_iter / STEPS_PER_MM_X),
                            "y": y_start + (y_iter / STEPS_PER_MM_Y),
                            "z": z_start + (z_iter / STEPS_PER_MM_Z),
                            "result": result,
                        }
                    )
                    task_counter += n_rep
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
