from pynput import keyboard
import time

import PositionController
import EMFIController
import TargetController
import Plot
import TUI

# Configuration Parameter
POSITION_CONTROLLER_PORT = "COM25"  # Serial port connected to position controller
EMFI_PROBE_PORT = "COM23"  # Serial port connected to EMFI probe
EMFI_PROBE_BAUD = 115200  # Baudrate of EMFI probe
EMFI_PULSE_DURATION = 5
EMFI_PULSE_POWER = 0.005
TARGET_PROBE_PORT = "COM24"  # Serial port connected to target
TARGET_PROBE_BAUD = 115200  # Baudrate of target
TARGET_CHIP_WIDTH = 2
TARGET_SCAN_HEIGHT = 0


# Global Variables
main_loop = TUI.MainLoop()
user_interface = TUI.UserInterface()
pos_controller = PositionController.PositionController(POSITION_CONTROLLER_PORT)
emfi_controller = EMFIController.EMFIController(EMFI_PROBE_PORT, EMFI_PROBE_BAUD)
target_controller = TargetController.TargetController(
    TARGET_PROBE_PORT, TARGET_PROBE_BAUD
)


# Functions
def on_press(key):
    """
    Handles keyboard input
    """
    if key == keyboard.KeyCode(char="w"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(y=1)
    if key == keyboard.KeyCode(char="s"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(y=-1)
    if key == keyboard.KeyCode(char="d"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(x=1)
    if key == keyboard.KeyCode(char="a"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(x=-1)
    if key == keyboard.KeyCode(char="o"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(z=1)
    if key == keyboard.KeyCode(char="l"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(z=-1)
    if key == keyboard.KeyCode(char="i"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(z=0.25)
    if key == keyboard.KeyCode(char="k"):
        user_interface.print_debug("Busy...          ")
        pos_controller.move_rel(z=-0.25)
    if key == keyboard.KeyCode(char="b"):
        user_interface.print_debug("Busy...          ")
        target_controller.read(10, 5)
    if key == keyboard.KeyCode(char="r"):
        user_interface.print_debug("Busy...          ")
        start_time = time.time()
        emfi_controller.arm()
        results = pos_controller.move_raster(
            width=TARGET_CHIP_WIDTH,
            height=TARGET_SCAN_HEIGHT,
            action_callback=handle_pulse,
            eval_callback=handle_target,
            status_callback=handle_status,
            n_rep=4,
        )
        emfi_controller.disarm()
        Plot.plot_results(results)
        user_interface.print_status(
            "Scan required " + time.time() - start_time + " seconds"
        )
    if key == keyboard.KeyCode(char="h"):
        user_interface.print_debug("Busy...              ")
        pos_controller.home_xy()
    if key == keyboard.KeyCode(char="p"):
        user_interface.print_debug("Busy...              ")
        emfi_controller.arm()
        emfi_controller.pulse()
        emfi_controller.disarm()
    if key == keyboard.KeyCode(char="q"):
        user_interface.print_debug("Closing interfaces           ")
        pos_controller.close_controller()
        emfi_controller.close_controller()
        target_controller.close_controller()
        main_loop.end_loop()
    user_interface.print_debug("Awaiting input")


def handle_status(current_task, total_tasks):
    user_interface.print_status(
        "Progress: "
        + str(round(current_task / total_tasks * 100, 2))
        + "% done                "
    )


def handle_pulse():
    """
    Callback function handling the pulse generation
    """
    time.sleep(1)
    target_controller.reset_read_buffer()
    emfi_controller.pulse()
    # time.sleep(2)


def handle_target():
    data = target_controller.read(24).decode()
    if len(data) < 24:
        target_controller.reset_target()
        return "y"
    values = data.split("\r\n", 3)
    if (int(values[0]) + 1 == int(values[1])) and (
        int(values[1]) + 1 == int(values[2])
    ):
        return "g"
    return "r"


def main():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    user_interface.print_menu()
    user_interface.print_debug("Awaiting input")

    emfi_controller.change_config(EMFI_PULSE_DURATION, EMFI_PULSE_POWER)
    user_interface.print_status(
        "EMFI Probe set to Duration = "
        + str(EMFI_PULSE_DURATION)
        + " Power = "
        + str(EMFI_PULSE_POWER)
    )

    while main_loop.is_running():
        pass


if __name__ == "__main__":
    main()
# end main
