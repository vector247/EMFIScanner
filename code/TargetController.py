import SerialInterface


class TargetController:
    def __init__(self, interface, baudrate):
        self.controller_interface = SerialInterface.SerialInterface(
            interface, baudrate, timeout=5
        )

    def close_controller(self):
        self.controller_interface.closeInterface()

    def read(self, n_bytes):
        return self.controller_interface.input(n_bytes)

    def reestablish_connection(self, interface, baudrate):
        self.controller_interface = SerialInterface.SerialInterface(interface, baudrate)

    def check_open(self):
        return self.controller_interface.check_open()
