from pynput import keyboard
import time

import PositionController
import EMFIController
import TargetController
import Plot

# Configuration Parameter
POSITION_CONTROLLER_PORT = "COM25"  # Serial port connected to position controller
EMFI_PROBE_PORT = "COM23"  # Serial port connected to EMFI probe
EMFI_PROBE_BAUD = 115200  # Baudrate of EMFI probe
TARGET_PROBE_PORT = "COM24"  # Serial port connected to target
TARGET_PROBE_BAUD = 115200  # Baudrate of target
TARGET_CHIP_WIDTH = 2
TARGET_SCAN_HEIGHT = 0


class MainLoop:
    run = False

    def __init__(self):
        self.run = True

    def end_loop(self):
        self.run = False

    def is_running(self):
        return self.run


# Global Variables
main_loop = MainLoop()
pos_controller = PositionController.PositionController(POSITION_CONTROLLER_PORT)
emfi_controller = EMFIController.EMFIController(EMFI_PROBE_PORT, EMFI_PROBE_BAUD)
target_controller = TargetController.TargetController(
    TARGET_PROBE_PORT, TARGET_PROBE_BAUD
)


# Functions
def print_menu():
    """
    Prints the keyboard menu
    """
    print("                                                                         ")
    print("                               +--------------+                          ")
    print("            |     |            | EMFI Scanner |                          ")
    print("            |_____|            | by Vector247 |                          ")
    print("              | |              +--------------+                          ")
    print("               O                                                         ")
    print("         ___________          Move XY         Move Z                     ")
    print("        /          /          ____             ____                      ")
    print("       /  ____    /          /_w_/            /_o_/                      ")
    print("      /  /   /|  /     ____ ____ ____        ____                        ")
    print("     /  r___/   /     /_a_//_s_//_d_/       /_l_/                        ")
    print("^   /   |   |  / ^                                                       ")
    print("|  /          / /        Quit   Home XY    Start Scan    Manual Pulse    ")
    print("Z 0__________/ Y        ____     ____        ____            ____        ")
    print("  X ->                 /_q_/    /_h_/       /_r_/           /_p_/        ")
    print("                                                                         ")


def on_press(key):
    """
    Handles keyboard input
    """
    if key == keyboard.KeyCode(char="w"):
        pos_controller.move_rel(y=1)
    if key == keyboard.KeyCode(char="s"):
        pos_controller.move_rel(y=-1)
    if key == keyboard.KeyCode(char="d"):
        pos_controller.move_rel(x=1)
    if key == keyboard.KeyCode(char="a"):
        pos_controller.move_rel(x=-1)
    if key == keyboard.KeyCode(char="o"):
        pos_controller.move_rel(z=1)
    if key == keyboard.KeyCode(char="l"):
        pos_controller.move_rel(z=-1)
    if key == keyboard.KeyCode(char="b"):
        target_controller.read(10, 5)
    if key == keyboard.KeyCode(char="r"):
        emfi_controller.arm()
        results = pos_controller.move_raster(
            width=TARGET_CHIP_WIDTH,
            height=TARGET_SCAN_HEIGHT,
            action_callback=handle_pulse,
            eval_callback=handle_target,
        )
        emfi_controller.disarm()
        Plot.plot_results(results)
    if key == keyboard.KeyCode(char="h"):
        pos_controller.home_xy()
    if key == keyboard.KeyCode(char="p"):
        emfi_controller.arm()
        emfi_controller.pulse()
        emfi_controller.disarm()
    if key == keyboard.KeyCode(char="q"):
        pos_controller.close_controller()
        emfi_controller.close_controller()
        target_controller.close_controller()
        main_loop.end_loop()


def handle_pulse():
    """
    Callback function handling the pulse generation
    """
    time.sleep(1)
    emfi_controller.pulse()
    # time.sleep(2)


def handle_target():
    # if target_controller.check_open() == False:
    #    target_controller.reestablish_connection(TARGET_PROBE_PORT, TARGET_PROBE_BAUD)
    #    return "b"
    data = target_controller.read(16).decode()
    print(data)  # TODO: Debug
    if len(data) < 16:
        return "y"
    values = data.split("\r\n", 3)
    print(values)  # TODO: Debug
    if (int(values[0]) + 1 == int(values[1])) and (
        int(values[1]) + 1 == int(values[2])
    ):
        return "g"
    return "r"


def main():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print_menu()

    while main_loop.is_running():
        pass


if __name__ == "__main__":
    main()
# end main
