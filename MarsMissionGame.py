import LEVEL_3.level_3
import LEVEL_4.Restart_page
import flags as flags
from LEVEL_4.levels import level4_1, level4_2, level4_3

#### LEVEL 1 #####
#### LEVEL 2 #####
#### LEVEL 3 #####
run3 = True

while not flags.next_lvl_3.get_flag():
    LEVEL_3.level_3.menu(death_count=0)

#### LEVEL 4 #####
run4_1 = True

while not flags.next_lvl_4_1.get_flag():
    if not level4_1.run_level(run4_1):
        if flags.lvl4_dog_dead_flag.get_flag():
            LEVEL_4.Restart_page.restart()
            run4_1 = True
            flags.lvl4_dog_dead_flag.set_flag(False)

run4_2 = True

while not flags.next_lvl_4_2.get_flag():
    if not level4_2.run_level(run4_2):
        if flags.lvl4_dog_dead_flag.get_flag():
            LEVEL_4.Restart_page.restart()
            run4_2 = True
            flags.lvl4_dog_dead_flag.set_flag(False)

run4_3 = True
while not flags.next_lvl_4_3.get_flag():
    if not level4_3.run_level(run4_3):
        if flags.lvl4_dog_dead_flag.get_flag():
            LEVEL_4.Restart_page.restart_lvl_3()
            run4_3 = True
            flags.lvl4_dog_dead_flag.set_flag(False)

#### LEVEL 5 #####

#### LEVEL 6 #####

#### LEVEL BONUS #####
