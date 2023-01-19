import pygame

import LEVEL_1.main
import LEVEL_2.level_2
import LEVEL_3n4.restart_page
import LEVEL_5.MartianMission
import flags as flags
import main_menu
from LEVEL_3n4.levels import level3_1, level3_2, level4

level = 0
flag_list = [flags.next_lvl_1, flags.next_lvl_2, flags.next_lvl_3_1, flags.next_lvl_3_2, flags.next_lvl_4,
             flags.next_lvl_5]
while True:
    main_menu.menu()

    main_menu.splash_screen('main_story')
    for flag in flag_list:
        flag.set_flag(False)