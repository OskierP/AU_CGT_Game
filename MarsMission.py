import flags
from flags import dog_dead_flag
import level4_1
import Restart_page
import level4_2

run1 = True
run2 = True


while not flags.next_lvl_1.get_flag():
    if not level4_1.run_level(run1):
        if dog_dead_flag.get_flag():
            Restart_page.restart()
            run1 = True
            dog_dead_flag.set_flag(False)

while not flags.next_lvl_2.get_flag():
    if not level4_2.run_level(run2):
        if dog_dead_flag.get_flag():
            Restart_page.restart()
            run2 = True
            dog_dead_flag.set_flag(False)

print('lvl3')
# while not level4_1.get_next_lvl():
#     if level4_1.run_level(variable, False):
#
#         variable = False
#     print('lvl1')

# if level4_2.run_level(variable) and not level4_2.get_next_lvl():
#     Restart_page.restart()
#     variable = False


