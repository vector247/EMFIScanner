import serial
import time


class SerialInterface:
    port = ""

    def __init__(self, interface, baudrate=115200, timeout=None):
        """
        Purpose: Opens a UART with baudrate 115200 on interface
        """
        self.port = serial.Serial(port=interface, baudrate=baudrate, timeout=timeout)
        print(f"Port opened on {self.port.name}")

    def output(self, output_string=""):
        print(f"Writing {output_string} on {self.port.name}")
        output_string += "\n\r"
        self.port.write(output_string.encode())

    def reset_input_buffer(self):
        self.port.reset_input_buffer()

    def input(self, n_bytes):
        data = b""
        data = self.port.read(n_bytes)
        print(f"Read {data} from {self.port.name}")
        return data

    def input_post_reset(self, n_bytes):
        data = b""
        self.port.reset_input_buffer()
        data = self.port.read(n_bytes)
        print(f"Read {data} from {self.port.name}")
        return data

    def check_open(self):
        return self.port.is_open

    def closeInterface(self):
        print(f"Port {self.port.name} closed")
        self.port.close()


if __name__ == "__main__":
    newInterface = SerialInterface("COM25")

    newInterface.output("G01 X Y Z")
    time.sleep(2)
    newInterface.output("G01 X0 Y0 Z25")
    time.sleep(2)
    newInterface.closeInterface()
# end main
