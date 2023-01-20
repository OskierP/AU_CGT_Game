import pygame

import data.LEVEL_1.main
import data.LEVEL_2.level_2
import data.LEVEL_3n4.restart_page
import data.LEVEL_5.MartianMission
from data import main_menu, flags as flags
from data.LEVEL_3n4.levels import level4, level3_1, level3_2

level = 0
flag_list = [flags.next_lvl_1, flags.next_lvl_2, flags.next_lvl_3_1, flags.next_lvl_3_2, flags.next_lvl_4,
             flags.next_lvl_5]
while True:
    main_menu.menu()

    main_menu.splash_screen('main_story')
    for flag in flag_list:
        flag.set_flag(False)
    while flags.menu_flag.get_flag():

        level = main_menu.choose_level()

        if level == 1:
            #### LEVEL 1 #####
            main_menu.splash_screen('lvl1')
            while not flags.next_lvl_1.get_flag():
                data.LEVEL_1.main.level1()
            flags.next_lvl_1.set_flag(False)

        ### LEVEL 2 #####
        if level == 2:
            main_menu.splash_screen('lvl2')
            # while not flags.next_lvl_2.get_flag():
            data.LEVEL_2.level_2.menu(death_count=0)
            flags.next_lvl_2.set_flag(False)
            pygame.mixer.music.stop()

        if level == "3_1":
            #### LEVEL 3&4 #####
            main_menu.splash_screen('lvl3')
            run_level_3_1 = True

            while not flags.next_lvl_3_1.get_flag():
                if not level3_1.run_level(run_level_3_1):
                    if flags.lvl3_dog_dead_flag.get_flag():
                        data.LEVEL_3n4.restart_page.restart()
                        run_level_3_1 = True
                        flags.lvl3_dog_dead_flag.set_flag(False)
            pygame.mixer.music.stop()
            flags.next_lvl_3_1.set_flag(False)

        if level == "3_2":
            main_menu.splash_screen('lvl3')
            run_level_3_2 = True
            pygame.mixer.stop()
            while not flags.next_lvl_3_2.get_flag():
                if not level3_2.run_level(run_level_3_2):
                    if flags.lvl3_dog_dead_flag.get_flag():
                        data.LEVEL_3n4.restart_page.restart()
                        run_level_3_2 = True
                        flags.lvl3_dog_dead_flag.set_flag(False)
            pygame.mixer.music.stop()
            flags.next_lvl_3_2.set_flag(False)

        if level == 4:
            main_menu.splash_screen('lvl4')
            run_level_4 = True
            while not flags.next_lvl_4.get_flag():
                if not level4.run_level(run_level_4):
                    if flags.lvl3_dog_dead_flag.get_flag():
                        data.LEVEL_3n4.restart_page.restart_lvl_4()
                        run_level_4 = True
                        flags.lvl3_dog_dead_flag.set_flag(False)
            pygame.mixer.stop()
            flags.next_lvl_4.set_flag(False)

        #### LEVEL 5 #####
        if level == 5:
            main_menu.splash_screen('lvl5')
            while not flags.next_lvl_5.get_flag():
                data.LEVEL_5.MartianMission.main()
            flags.next_lvl_5.set_flag(False)
            main_menu.end_screen()
        #### LEVEL 6 #####

        #### LEVEL BONUS #####

        # pygame.quit()
