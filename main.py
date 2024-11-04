from pynput import keyboard
import time

import PositionController
import EMFIController
import Plot

posControl = PositionController.PositionController("COM25")
emfiController = EMFIController.EMFIController("COM23", 115200)
local_end = False


def on_press(key):
    if key == keyboard.KeyCode(char="w"):
        posControl.moveRel(y=1)
    if key == keyboard.KeyCode(char="s"):
        posControl.moveRel(y=-1)
    if key == keyboard.KeyCode(char="d"):
        posControl.moveRel(x=1)
    if key == keyboard.KeyCode(char="a"):
        posControl.moveRel(x=-1)
    if key == keyboard.KeyCode(char="o"):
        posControl.moveRel(z=1)
    if key == keyboard.KeyCode(char="l"):
        posControl.moveRel(z=-1)
    if key == keyboard.KeyCode(char="r"):
        emfiController.arm()
        results = posControl.moveRaster(width=2, height=1, action_callback=handle_pulse)
        emfiController.disarm()
        Plot.plot_results(results)
    if key == keyboard.KeyCode(char="h"):
        posControl.homeXY()
    if key == keyboard.KeyCode(char="p"):
        emfiController.arm()
        emfiController.pulse()
        emfiController.disarm()
    if key == keyboard.KeyCode(char="q"):
        posControl.closeController()
        emfiController.closeController()
        local_end = True


def handle_pulse():
    time.sleep(1)
    emfiController.pulse()
    # time.sleep(2)


def main():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while local_end != True:  # TODO: Find good way to end the script peacefully
        pass


if __name__ == "__main__":
    main()
# end main
