import pygame

import LEVEL_1.main
import LEVEL_2.level_2
import LEVEL_3n4.restart_page
import LEVEL_5.MartianMission
import flags as flags
import main_menu
import progress.save_progress
from LEVEL_3n4.levels import level3_1, level3_2, level4

level = 0
flag_list = [flags.next_lvl_1, flags.next_lvl_2, flags.next_lvl_3_1, flags.next_lvl_3_2, flags.next_lvl_4,
             flags.next_lvl_5]
while True:
    main_menu.menu()
    for flag in flag_list:
        flag.set_flag(False)
    while flags.menu_flag.get_flag():

        level = main_menu.choose_level()

        if level == 1:
            #### LEVEL 1 #####
            main_menu.splash_screen('lvl1')
            while not flags.next_lvl_1.get_flag():
                LEVEL_1.main.level_1()
            flags.next_lvl_1.set_flag(False)
            progress.save_progress.update_progress('Level_2', True)
        ### LEVEL 2 #####
        if level == 2:
            main_menu.splash_screen('lvl2')
            # while not flags.next_lvl_2.get_flag():
            LEVEL_2.level_2.menu(death_count=0)
            flags.next_lvl_2.set_flag(False)
            progress.save_progress.update_progress('Level_3_1', True)

        if level == "3_1":
            #### LEVEL 3&4 #####
            main_menu.splash_screen('lvl3')
            run_level_3_1 = True

            while not flags.next_lvl_3_1.get_flag():
                if not level3_1.run_level(run_level_3_1):
                    if flags.lvl3_dog_dead_flag.get_flag():
                        LEVEL_3n4.restart_page.restart()
                        run_level_3_1 = True
                        flags.lvl3_dog_dead_flag.set_flag(False)
            pygame.mixer.music.stop()
            flags.next_lvl_3_1.set_flag(False)
            progress.save_progress.update_progress('Level_3_2', True)

        if level == "3_2":
            main_menu.splash_screen('lvl3')
            run_level_3_2 = True
            pygame.mixer.stop()
            while not flags.next_lvl_3_2.get_flag():
                if not level3_2.run_level(run_level_3_2):
                    if flags.lvl3_dog_dead_flag.get_flag():
                        LEVEL_3n4.restart_page.restart()
                        run_level_3_2 = True
                        flags.lvl3_dog_dead_flag.set_flag(False)
            pygame.mixer.music.stop()
            flags.next_lvl_3_2.set_flag(False)
            progress.save_progress.update_progress('Level_4', True)


        if level == 4:
            main_menu.splash_screen('lvl4')
            run_level_4 = True
            while not flags.next_lvl_4.get_flag():
                if not level4.run_level(run_level_4):
                    if flags.lvl3_dog_dead_flag.get_flag():
                        LEVEL_3n4.restart_page.restart_lvl_4()
                        run_level_4 = True
                        flags.lvl3_dog_dead_flag.set_flag(False)
            pygame.mixer.stop()
            progress.save_progress.update_progress('Level_5', True)
            flags.next_lvl_4.set_flag(False)



        #### LEVEL 5 #####
        if level == 5:
            main_menu.splash_screen('lvl5')
            while not flags.next_lvl_5.get_flag():
                LEVEL_5.MartianMission.main()
            flags.next_lvl_5.set_flag(False)
        #### LEVEL 6 #####

        #### LEVEL BONUS #####

        # pygame.quit()
