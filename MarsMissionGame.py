import LEVEL_4.Restart_page as Restart_page
import flags as flags
#### LEVEL 4 #####
from LEVEL_4.levels import level4_1, level4_2

#### LEVEL 1 #####
#### LEVEL 2 #####
#### LEVEL 3 #####

run4_1 = True
run4_2 = True
run4_3 = True

while not flags.next_lvl_4_1.get_flag():
    if not level4_1.run_level(run4_1):
        if flags.lvl4_dog_dead_flag.get_flag():
            Restart_page.restart()
            run4_1 = True
            flags.lvl4_dog_dead_flag.set_flag(False)

while not flags.next_lvl_4_2.get_flag():
    if not level4_2.run_level(run4_2):
        if flags.lvl4_dog_dead_flag.get_flag():
            Restart_page.restart()
            run4_2 = True
            flags.lvl4_dog_dead_flag.set_flag(False)

while not flags.next_lvl_4_3.get_flag():
    print('lvl3')

#### LEVEL 5 #####

#### LEVEL 6 #####

#### LEVEL BONUS #####
