import pygame

import LEVEL_1.main
import LEVEL_2.level_2
import LEVEL_3n4.Restart_page
import LEVEL_5.MartianMission
import flags as flags
from LEVEL_3n4.levels import level3_1, level3_2, level4

#### LEVEL 1 #####
while not flags.next_lvl_1.get_flag():
    LEVEL_1.main.level_1()
### LEVEL 2 #####
### LEVEL 3 #####

while not flags.next_lvl_2.get_flag():
    LEVEL_2.level_2.menu(death_count=0)

#### LEVEL 4 #####
run_level_3_1 = True

while not flags.next_lvl_3_1.get_flag():
    if not level3_1.run_level(run_level_3_1):
        if flags.lvl3_dog_dead_flag.get_flag():
            LEVEL_3n4.Restart_page.restart()
            run_level_3_1 = True
            flags.lvl3_dog_dead_flag.set_flag(False)

run_level_3_2 = True
pygame.mixer.stop()
while not flags.next_lvl_3_2.get_flag():
    if not level3_2.run_level(run_level_3_2):
        if flags.lvl3_dog_dead_flag.get_flag():
            LEVEL_3n4.Restart_page.restart()
            run_level_3_2 = True
            flags.lvl3_dog_dead_flag.set_flag(False)
pygame.mixer.music.stop()

run_level_4 = True
while not flags.next_lvl_4.get_flag():
    level4.run_level(run_level_4)
pygame.mixer.stop()

#### LEVEL 5 #####
while not flags.next_lvl_5.get_flag():
    LEVEL_5.MartianMission.main()
#### LEVEL 6 #####

#### LEVEL BONUS #####


pygame.quit()
