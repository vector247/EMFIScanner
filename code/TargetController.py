import SerialInterface
import phywhisperer.usb as pw
import time


class TargetController:
    interface = ""
    baudrate = 0

    def __init__(self, interface, baudrate):
        self.interface = interface
        self.baudrate = baudrate
        self.phy = pw.Usb()
        self.phy.con()
        self.phy.set_power_source("host")
        time.sleep(1)
        self.controller_interface = SerialInterface.SerialInterface(
            interface, baudrate, timeout=5
        )

    def reset_target(self):
        self.phy.set_power_source("off")
        time.sleep(0.2)
        self.phy.set_power_source("host")
        time.sleep(1)
        self.controller_interface = SerialInterface.SerialInterface(
            self.interface, self.baudrate, timeout=5
        )

    def close_controller(self):
        self.controller_interface.closeInterface()
        self.phy.close()

    def read(self, n_bytes):
        return self.controller_interface.input(n_bytes)

    def reset_read_buffer(self):
        self.controller_interface.reset_input_buffer()

    def reestablish_connection(self, interface, baudrate):
        self.controller_interface = SerialInterface.SerialInterface(interface, baudrate)

    def check_open(self):
        return self.controller_interface.check_open()
