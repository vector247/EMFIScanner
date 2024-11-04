import time

import SerialInterface


class EMFIController:
    current_duration = 5
    current_power = 0.01
    is_armed = True  # Assume worst case

    def __init__(self, interface, baudrate):
        self.controller_interface = SerialInterface.SerialInterface(interface, baudrate)
        self.controller_interface.output("d")  # Disarm, just in case
        time.sleep(3)
        self.is_armed = False
        self.controller_interface.output("c")  # Configure
        self.controller_interface.output(f"{self.current_duration}")  # Set duration
        self.controller_interface.output(f"{self.current_power}")  # Set power

    def closeController(self):
        self.controller_interface.output("d")  # Disarm
        time.sleep(3)
        self.is_armed = False
        self.controller_interface.closeInterface()

    def arm(self):
        self.controller_interface.output("a")
        self.is_armed = True
        time.sleep(2)

    def disarm(self):
        self.controller_interface.output("d")
        time.sleep(3)
        self.is_armed = False

    def pulse(self):
        if self.is_armed:
            self.controller_interface.output("p")
            time.sleep(1)

    def change_config(self, new_duration, new_power):
        self.current_duration = new_duration
        self.current_power = new_power
        self.controller_interface.output("d")  # Disarm, just in case
        time.sleep(3)
        self.is_armed = False
        self.controller_interface.output("c")  # Configure
        self.controller_interface.output(f"{self.current_duration}")  # Set duration
        self.controller_interface.output(f"{self.current_power}")  # Set power


def main():
    new_controller = EMFIController("COM23", 115200)
    new_controller.arm()
    new_controller.pulse()

    new_controller.change_config(10, 0.005)
    new_controller.arm()
    new_controller.pulse()
    new_controller.closeController()


if __name__ == "__main__":
    main()
# end main
