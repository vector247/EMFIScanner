import sys
import os


class UserInterface:

    def __init__(self):
        self.clear_screen()
        pass

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_pos(self, x, y, text):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
        sys.stdout.flush()

    def print_status(self, text):
        self.print_pos(17, 0, text)

    def print_debug(self, text):
        self.print_pos(18, 0, text)

    def print_menu(self):
        """
        Prints the keyboard menu
        """
        self.print_pos(
            1,
            0,
            "                                                                         ",
        )
        self.print_pos(
            2,
            0,
            "                               +--------------+                          ",
        )
        self.print_pos(
            3,
            0,
            "            |     |            | EMFI Scanner |                          ",
        )
        self.print_pos(
            4,
            0,
            "            |_____|            | by Vector247 |                          ",
        )
        self.print_pos(
            5,
            0,
            "              | |              +--------------+                          ",
        )
        self.print_pos(
            6,
            0,
            "               O                                                         ",
        )
        self.print_pos(
            7,
            0,
            "         ___________          Move XY         (Micro)Move Z              ",
        )
        self.print_pos(
            8,
            0,
            "        /          /          ____            ____  ____                 ",
        )
        self.print_pos(
            9,
            0,
            "       /  ____    /          /_w_/           /_i_/ /_o_/                 ",
        )
        self.print_pos(
            10,
            0,
            "      /  /   /|  /     ____ ____ ____      ____  ____                    ",
        )
        self.print_pos(
            11,
            0,
            "     /  r___/   /     /_a_//_s_//_d_/     /_k_/ /_l_/                    ",
        )
        self.print_pos(
            12,
            0,
            "^   /   |   |  / ^                                                       ",
        )
        self.print_pos(
            13,
            0,
            "|  /          / /        Quit   Home XY    Start Scan    Manual Pulse    ",
        )
        self.print_pos(
            14,
            0,
            "Z 0__________/ Y        ____     ____        ____            ____        ",
        )
        self.print_pos(
            15,
            0,
            "  X ->                 /_q_/    /_h_/       /_r_/           /_p_/        ",
        )
        self.print_pos(
            16,
            0,
            "                                                                         ",
        )


class MainLoop:
    run = False

    def __init__(self):
        self.run = True

    def end_loop(self):
        self.run = False

    def is_running(self):
        return self.run
