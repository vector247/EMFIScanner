import chipwhisperer as cw
import time


class TriggerController:

    def __init__(self):
        try:
            if not self.scope.connectStatus:
                self.scope.con()
                print("ChipWhisperer existed ➡")
        except AttributeError:
            self.scope = cw.scope()
            print("ChipWhisperer found 🐺")
        self.scope.default_setup()

    def print_scope(self):
        print(self.scope)

    def setup_trigger(self):
        self.scope.glitch.num_glitches = 1
        self.scope.glitch.repeat = 37  # set glitch length to about 5ms

        self.scope.glitch.enabled = True
        self.scope.glitch.output = "enable_only"
        self.scope.glitch.trigger_src = "manual"
        self.scope.glitch.clk_src = "pll"

        self.scope.trigger.module = "basic"
        self.scope.trigger.triggers = "tio4"

        self.scope.io.hs2 = "glitch"
        self.scope.io.aux_io_mcx = "hs2"

        self.scope.adc.lo_gain_errors_disabled = True

    def arm(self):
        self.scope.arm()

    def trigger(self):
        self.scope.glitch.manual_trigger()


def main():
    myTrigger = TriggerController()

    myTrigger.setup_trigger()

    myTrigger.print_scope()

    while True:
        myTrigger.trigger()
        time.sleep(5)


if __name__ == "__main__":
    main()
# end main
